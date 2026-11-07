/* PLUGIN-NAME — host backend (ExtendScript, ES3 only).
   No const/let/arrow/forEach/template-literals. Return JSON strings to the panel. */

var PLUGIN = (function () {

  function esc(s) {
    s = String(s); var out = "", i, c;
    for (i = 0; i < s.length; i++) {
      c = s.charAt(i);
      if (c === "\\") out += "\\\\";
      else if (c === '"') out += '\\"';
      else if (c === "\n" || c === "\r" || c === "\t") out += " ";
      else out += c;
    }
    return out;
  }
  function ok(extra) { return '{"ok":true' + (extra ? "," + extra : "") + "}"; }
  function err(m) { return '{"ok":false,"error":"' + esc(m) + '"}'; }

  /* Confirms the bridge is alive and reports the host version. */
  function ping() {
    try { return ok('"host":"' + esc(app.version) + '"'); }
    catch (e) { return err(e.toString()); }
  }

  /* EXAMPLE action — replace with real work against the host app's API.
     Called from the panel as: PLUGIN.doThing('some text'). */
  function doThing(arg) {
    try {
      // ... use the host API here ...
      return ok('"echo":"' + esc(arg) + '"');
    } catch (e) {
      return err(e.toString());
    }
  }

  return { ping: ping, doThing: doThing };
})();
