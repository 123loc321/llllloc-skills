/* llloc-prefs.js  —  v2  —  settings that actually survive a Premiere restart.
   ------------------------------------------------------------------------------
   Panels keep their settings in localStorage. In CEP that lives inside the CEF
   cache, which Premiere is free to clear between sessions - and which every one
   of our own installers deletes on purpose to make a manifest change visible. So
   a user who picks "light" can find themselves back on "dark" after a restart.

   This mirrors localStorage to a real file in the user's own data folder:

     macOS    ~/Library/Application Support/CSXS/llllllloc/<panel>.json
     Windows  %APPDATA%\CSXS\llllllloc\<panel>.json

   On load, anything present on disk but missing from localStorage is restored -
   so a cleared cache costs nothing. After that every write is mirrored.
   Nothing else in a panel has to change: every existing localStorage call keeps
   working, and gets persistence for free.

   Loaded BEFORE the panel script on purpose: panels read their settings while
   parsing, so the restore has to have already happened.

   ---------------------------------------------------------------------------
   WHAT v1 GOT WRONG, 6 August 2026. Read this before touching the path code.

   v1 used window.__adobe_cep__.getSystemPath("userData") RAW. That call does not
   return a path. It returns a percent-encoded file:// URI:

       file:///Users/you/Library/Application%20Support

   Adobe's own CSInterface.getSystemPath() runs decodeURI() over it and strips the
   scheme before handing it to anyone - this module could not call that, because
   it loads BEFORE CSInterface.js on purpose, and it never did the work itself.

   So every path it built was a URI with a %20 in it, cep.fs refused all of them,
   readFile and writeFile failed silently, and the mirror never worked ON ANY MAC.
   Settings were localStorage-only the whole time, which is exactly the state this
   file exists to prevent. It is written into PLUGIN-LOG section 7 as a known trap
   and this module walked straight into it.

   Two rules bought by that:
     1. NEVER pass a getSystemPath result to cep.fs without nativePath() below.
     2. cep.fs.writeFile does not throw - it returns an error code. Check the
        code AND read the file back. v1 checked the code and believed it.
   --------------------------------------------------------------------------- */
(function () {
  "use strict";

  var VERSION = 2;
  var NAME = (window.LLLOC_PANEL || "PANEL").toLowerCase();
  var fs = null, dir = null, file = null;
  var last = null, timer = null, pending = null;
  var STORE_OK = false, WHY = "not tried";

  function log(m) {
    try { if (window.console && console.log) console.log("[" + NAME + " prefs] " + m); } catch (e) {}
  }

  /* ---- the trap, handled once, here ---------------------------------------
     file:///Users/you/Library/Application%20Support  ->  /Users/you/Library/Application Support
     file:///C:/Users/you/AppData/Roaming              ->  C:/Users/you/AppData/Roaming
     A build that already hands back a plain path passes straight through. */
  function nativePath(u) {
    var p = String(u || "");
    if (!p) return "";
    try { p = decodeURI(p); } catch (e) {}
    try { if (p.indexOf("%") !== -1) p = decodeURIComponent(p); } catch (e2) {}
    if (p.indexOf("file:///") === 0) {
      p = p.substring(8);
      /* POSIX just lost its leading slash; a Windows drive letter did not. */
      if (!/^[A-Za-z]:/.test(p)) p = "/" + p;
    } else if (p.indexOf("file://") === 0) {
      p = p.substring(7);
      if (p.charAt(0) !== "/" && !/^[A-Za-z]:/.test(p)) p = "/" + p;
    }
    return p.split("\\").join("/");
  }

  /* ---- locate the store -------------------------------------------------- */
  try {
    fs = (window.cep && window.cep.fs) ? window.cep.fs : null;
    var raw = window.__adobe_cep__ ? window.__adobe_cep__.getSystemPath("userData") : "";
    var base = nativePath(raw);
    if (!fs) WHY = "cep.fs missing";
    else if (!base) WHY = "no userData path";
    if (fs && base) {
      dir = base + "/CSXS/llllllloc";
      file = dir + "/" + NAME + ".json";
    }
  } catch (e) { fs = null; WHY = "path lookup threw"; }

  function ensureDir() {
    if (!fs || !dir) return false;
    try {
      /* makedir does not create intermediate folders, so walk the path. */
      var parts = dir.split("/"), path = "", i;
      for (i = 0; i < parts.length; i++) {
        if (!parts[i]) { path = ""; continue; }
        path = (path === "" && /^[A-Za-z]:$/.test(parts[i])) ? parts[i] : path + "/" + parts[i];
        try { fs.makedir(path); } catch (e2) {}
      }
      return true;
    } catch (e) { return false; }
  }

  /* ---- read / write ------------------------------------------------------ */
  function readDisk() {
    if (!fs || !file) return null;
    try {
      var r = fs.readFile(file);
      if (!r || r.err !== 0 || !r.data) return null;
      return JSON.parse(r.data);
    } catch (e) { return null; }
  }

  function snapshot() {
    var out = {}, i, k;
    try {
      for (i = 0; i < localStorage.length; i++) {
        k = localStorage.key(i);
        if (k === null) continue;
        /* keep the panel's own keys and the shared llloc ones; skip nothing else
           of consequence, these stores are small */
        out[k] = localStorage.getItem(k);
      }
    } catch (e) { return null; }
    return out;
  }

  /* writeFile NEVER throws - it returns a code. And a code of 0 is still only a
     claim, so the first write of a session is read back before it is believed. */
  var proved = false;
  function writeDisk(obj) {
    if (!fs || !file) return false;
    var text;
    try { text = JSON.stringify(obj); } catch (eJ) { return false; }
    try {
      ensureDir();
      var r = fs.writeFile(file, text);
      if (!(r && r.err === 0)) {
        STORE_OK = false;
        WHY = "writeFile err " + ((r && r.err) !== undefined ? r.err : "?");
        return false;
      }
      if (!proved) {
        var back = fs.readFile(file);
        if (!back || back.err !== 0 || String(back.data) !== text) {
          STORE_OK = false;
          WHY = "wrote, but it did not read back";
          return false;
        }
        proved = true;
        STORE_OK = true;
        WHY = "ok";
        log("settings file proved at " + file);
      }
      return true;
    } catch (e) {
      STORE_OK = false;
      WHY = "writeFile threw";
      return false;
    }
  }

  /* ---- restore anything the cache lost ----------------------------------- */
  var disk = readDisk();
  if (disk) {
    var restored = 0, k;
    for (k in disk) {
      if (!disk.hasOwnProperty(k)) continue;
      try {
        if (localStorage.getItem(k) === null) {
          localStorage.setItem(k, disk[k]);
          restored++;
        }
      } catch (e) {}
    }
    if (restored) log("restored " + restored + " setting(s) the cache had lost");
  }
  last = JSON.stringify(snapshot() || {});

  /* ---- keep the file in step -------------------------------------------- */
  function persist(force) {
    var snap = snapshot();
    if (!snap) return;
    var now = JSON.stringify(snap);
    if (!force && now === last) return;
    if (writeDisk(snap)) last = now;
  }

  /* Mirror the moment a setting changes, not up to a second later. Premiere can
     be quit within that second, and the click that gets lost is the last one the
     user made - which is the one they care about. Debounced so a panel writing
     in a loop does not write a file per key. */
  try {
    var nativeSet = localStorage.setItem;
    localStorage.setItem = function (kk, vv) {
      var out = nativeSet.apply(localStorage, arguments);
      try {
        if (pending) window.clearTimeout(pending);
        pending = window.setTimeout(function () { pending = null; persist(false); }, 250);
      } catch (e2) {}
      return out;
    };
  } catch (e) { log("could not hook setItem - falling back to the poll alone"); }

  timer = window.setInterval(function () { persist(false); }, 1000);

  /* Belt and braces: also write when the panel loses focus or goes away, so a
     change made a moment before quitting Premiere is not lost. */
  try { window.addEventListener("blur", function () { persist(false); }); } catch (e) {}
  try { window.addEventListener("beforeunload", function () { persist(false); }); } catch (e) {}
  try {
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) persist(false);
    });
  } catch (e) {}

  /* First write shortly after boot, so a brand new install gets a file. */
  window.setTimeout(function () { persist(true); }, 1500);

  window.LLLOC_PREFS = {
    version: VERSION,
    path: function () { return file || "(localStorage only)"; },
    /* true once a write has been read back. The only honest answer to
       "are my settings actually being kept?" */
    ok: function () { return STORE_OK; },
    why: function () { return WHY; },
    save: function () { persist(true); },
    /* Wipe both copies - used by a "reset settings" action if a panel wants one. */
    reset: function () {
      try {
        var keys = [], i;
        for (i = 0; i < localStorage.length; i++) keys.push(localStorage.key(i));
        for (i = 0; i < keys.length; i++) localStorage.removeItem(keys[i]);
      } catch (e) {}
      writeDisk({});
      last = "{}";
    }
  };

  if (!fs) log("file store unavailable (" + WHY + ") - settings will use localStorage only");
})();
