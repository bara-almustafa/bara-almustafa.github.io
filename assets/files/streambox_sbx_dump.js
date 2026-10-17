var mod = Process.getModuleByName("libstreamboxdec.so");
var base = mod.base;
console.log("[*] base="+base);
var g_info = base.add(0x2a670);
var g_token = base.add(0x2a648);
var SESS_OFF = 0x5c00;   // Δ for this process
var del = mod.getExportByName ? mod.getExportByName("oapvd_delete") : Module.getExportByName("libstreamboxdec.so","oapvd_delete");
Interceptor.attach(del, {
  onEnter: function(args){
    try {
      var infop = g_info.readPointer();
      var arena = infop.add(0x30).readPointer();
      console.log("[hook] oapvd_delete; arena="+arena+" token=0x"+g_token.readU32().toString(16));
      var p = arena.add(SESS_OFF);
      console.log("  session[0x00..0x20] = "+hexdump(p, {length:32, ansi:false}));
      console.log("  is_premium(+8)=0x"+arena.add(SESS_OFF+8).readU32().toString(16)+
                  "  handler(+0xc)=0x"+arena.add(SESS_OFF+0xc).readU32().toString(16));
      // also dump row just inside buffer (row 0) and row 184 start raw
    } catch(e){ console.log("  ERR "+e); }
  }
});
console.log("[*] hook armed on oapvd_delete");
