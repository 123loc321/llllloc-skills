/* llloc-revive.js v3.8  —  CEP blank-panel recovery + boot journal + host guard.

   v3.8, 11 August 2026, same evening. THE GOODBYE NEVER GOT OUT. the studio closed a
   panel with the window's own close button and the dot stayed lit: "it only
   work when close a panel using double click funtion actually."

   MEASURED LIVE: when Premiere closes a panel window itself, the page's
   pagehide and unload handlers never deliver a CEP event. The teardown is
   ahead of them. So v3.8 does two things:

     1. It also announces from beforeunload, the earliest exit event there is,
        while the CEP bridge has the best chance of still being alive. This is
        an ATTEMPT - it could not be verified outside Premiere either.
     2. It stops being the only line of defense. DOCK V3.29 now re-asks
        who-is-there when the studio looks at it, and clears any dot nobody answers
        for. The dots are correct whenever he can see them, even if every
        goodbye dies.

   v3.7, 11 August 2026. EVERY PANEL NOW SAYS WHETHER IT IS OPEN. the studio: "when a
   panel being opened, I want the icon of that panel being highlighted, so the
   user know it's being opened."

   DOCK cannot ask Premiere which panels are open - no API for it exists. So the
   panels say so themselves, on the same event lane the close request already
   uses, and DOCK lights the icons. Three announcements, one dispatch each:

     open   - at boot, as soon as the host can say who this panel is
     open   - again whenever DOCK asks "who is there" (a restarted DOCK finds
              panels already open, so it has to be able to ask)
     closed - when the page goes away, however it goes: the double-click close,
              the window's own close button, or Premiere quitting

   Nothing polls. Nothing runs on the click path. A page too wedged to speak
   simply keeps its last known state on the rail - which is "open", and that is
   true: its window is still there.

   v3.6, 9 August 2026. THE REBUILD IS FAST NOW. the studio: "double-click actualy close
   and reopen it but too too slow."

   v3.5 worked but DOCK waited a fixed 2.6 seconds before reopening, because it had
   no way to know when the panel had actually gone. It does now: a panel SAYS SO
   before it closes. DOCK reopens 300ms after hearing that instead of waiting out
   a timer, so the whole rebuild takes about as long as the close itself.

   Two changes, both about speed:
     1. doClose() dispatches com.llllllloc.dock.closing, carrying this panel's id,
        immediately before it closes. That is the signal DOCK waits for.
     2. The request file is read every 350ms instead of every 1000ms. It is a small
        read on a filesystem the panel already uses, and it was the slowest link.

   SPEED IS A FEATURE. Nothing here runs on the everyday click path.

   v3.5, 9 August 2026. STOPS A LOOP v3.4 CAUSED. the studio: "now it just keep open
   and close randomly without me clicking on anything."

   v3.4 let DOCK ask a panel to close by writing a request file, and treated a
   request as live for 20 seconds. The panel closed, DOCK opened it again, and
   the NEW page read the SAME request - still inside those 20 seconds, and with
   no memory of having already obeyed it - so it closed itself again. Open,
   close, open, close, with nobody touching anything.

   Three guards now, because one was clearly not enough:

   1. A request is live for FOUR seconds, not twenty. Long enough for a
      once-a-second read to catch it, too short to survive a reopen.
   2. The panel writes down which request it has obeyed, in localStorage, which
      SURVIVES the reopen. The same request can never be obeyed twice.
   3. DOCK clears the file after it reopens the panel.

   The rule this bought: a request that triggers an action must be consumed by
   that action. A file that merely goes stale is a loop waiting to happen.

   v3.4, 9 August 2026. THE CLOSE REQUEST NOW ARRIVES TWO WAYS, AND SAYS SO.

   the studio clicked a rail button a second time and nothing happened: "it doesnt
   close the panel, I still have to close it by hand." DOCK asks a panel to
   close by sending a CEP event. Two things could break that and they need
   opposite fixes - the event never arrives, or the event arrives and Premiere
   ignores closeExtension(). Nothing recorded which, so nobody could say.

   Both are covered now:

   1. A SECOND ROUTE. DOCK also writes the request to a small file, and every
      panel reads that file once a second. No CEP event delivery involved. If
      only the messaging was broken, this alone fixes it.
   2. THE JOURNAL ANSWERS THE QUESTION. The panel writes close:asked when it
      hears the request by either route, and close:IGNORED two seconds later if
      it is somehow still running - which is proof that Premiere refused. That
      line is the difference between "fix the delivery" and "this cannot be
      automated", and it costs one mark to have it.

   v3.3, 9 August 2026. TWO ADDITIONS, AND ONE HARD FINDING BEHIND THEM.

   THE FINDING. the studio sent EASEUP's Startup report from a session where the panel
   came up grey. It reads:

       "marks":["script@0ms","dom@95ms","frame@166ms","load@168ms"]

   The blank session PAINTED A FRAME in 166ms, and there is not one revive mark
   in it. The three healthy sessions beside it are byte-identical in shape. So a
   blank panel and a working panel look EXACTLY THE SAME from inside the page.

   Everything in the recovery ladder below hangs off one question - did a frame
   paint? - and for this failure the answer is yes while the user stares at grey.
   THE LADDER CANNOT FIRE FOR IT. Neither could the rescue built on the same
   question. Do not build a third thing on that question.

   1. THE INSTRUMENT. look() writes what the page can actually see - hidden,
      visibilityState, window size, document size, focus - into the journal at
      every check. Two leads worth testing, both unproven: a panel Premiere is
      not really showing may report document.hidden true, and framePainted()
      calls hidden "alive" by design; or the window may have no size. Neither is
      recorded before now, so nobody can say which. The next grey panel names
      its own cause.

   2. CLOSE ON REQUEST. A dead surface is only cured by a NEW surface, and only
      closing the panel and opening it again makes one. A panel cannot do that
      to itself - closeExtension() ends its script. DOCK can. So every panel now
      answers com.llllllloc.dock.rescue by closing itself, and DOCK opens it
      again. In DOCK that is a right-click on the rail button: one click instead
      of five. It is a manual fix on purpose, because no detector we have works.

   v3.2 ADDS THE HOST GUARD, AND IT IS THE IMPORTANT ONE. 6 August 2026.

   the studio: "sometime when I open up a plug in from DOCK or from extension menu of
   pr, the plugin come out blank."

   Reproduced in a real Chromium, not guessed. Adobe's CSInterface.js line 480:

       CSInterface.prototype.hostEnvironment =
         window.__adobe_cep__ ? JSON.parse(window.__adobe_cep__.getHostEnvironment()) : null;

   That runs at PARSE TIME, at the top level, outside any try. The ternary only
   checks that __adobe_cep__ EXISTS. CEP injects that object early but does not
   finish wiring the host behind it, so there is a window where the object is
   there and getHostEnvironment() answers "" or null or half a string. JSON.parse
   throws, CSInterface.js dies mid-file, and every script after it - which is the
   entire panel - never runs. The panel opens blank.

   It is a RACE, which is why it is "sometime": it depends on whether the host is
   ready when the page loads. Opening a panel while Premiere is busy, which is
   exactly what opening from DOCK or from a cold Extensions menu does, is when it
   loses. Measured: with the host not ready, EASEUP's page height came out 0.

   So this module - which loads FIRST, before prefs and before CSInterface -
   wraps the host calls that get JSON.parsed and makes them always answer
   parseable JSON. CSInterface then loads, the panel script runs, and the panel
   paints. The real value passes through untouched the moment the host can give
   one, so nothing is faked for longer than it has to be.

   Adobe's CSInterface.js is NOT modified. It stays byte-for-byte Adobe's, which
   is what _SHARED promises and what makes the next Adobe update a drop-in.

   When the guard has to substitute, it writes a mark in the boot journal, so the
   Startup report can say "the host was not ready" instead of leaving the next
   person to guess.

   v3.1: when the user runs Fix blank panel and the ladder still cannot bring the
   surface back, say so in a native dialog instead of failing quietly. Reopening
   is the step that normally works, but requestOpenExtension on a panel that is
   ALREADY OPEN just brings it forward - it does not build a new surface - so on
   a docked panel that step can do nothing at all. The only thing left then is to
   close the panel and open it again from Window > Extensions, and the user has
   no way to know that unless they are told. A host dialog still appears even
   when the page cannot paint, which is exactly when it is needed.

   v3 FIXES A FALSE POSITIVE THAT REOPENED HEALTHY PANELS.
   "Visible but no frame" is a good detector for a dead surface only while the
   panel is meant to be painting. A panel that is OPEN BUT OCCLUDED - behind
   another tab in its group, or a floating window behind the main one - has its
   requestAnimationFrame throttled to nothing while document.hidden stays false.
   The old code read that as a dead surface, escalated to step 3, and reopened
   the panel, which threw it to the front. Because the focus handler runs it,
   this happened EVERY TIME the user came back to Premiere from another app, on
   whichever panel was hiding behind something - which reads exactly like "the
   last plugin I opened keeps opening itself".

   The genuine failure it was written for happens at load, and the checks at
   1.2s / 4s / 9s catch it. So the expensive steps - reopen and reload - are now
   allowed only in that opening window, or when the user asks for them from the
   panel menu. After that a check may still nudge the compositor, but it can
   never yank the panel to the front again.
   ------------------------------------------------------------------------------
   TWO JOBS

   1. RECOVERY. When Premiere restarts, a restored panel's browser surface can
      fail to composite: the page runs and lays out, but nothing paints. A reload
      reuses that same dead surface, so only a genuinely new surface fixes it.
      requestAnimationFrame only runs while the compositor runs, so "visible but
      no frame" is the detector. Escalation, cheapest first:
        1 repaint kick   - reflow + compositor layer change
        2 resizeContent  - ask the host to re-lay-out the panel
        3 reopen         - requestOpenExtension on ourselves, i.e. exactly what
                           Window > Extensions does, the one fix known to work
        4 reload         - same surface, so last, and only once

   2. JOURNAL. Recovery only helps if the page actually runs. To find out whether
      it does, every session writes timestamped marks to localStorage. After a
      blank restart the user reopens the panel by hand - that works - and the
      panel then reports what the previous session managed to do. No marks at all
      means the page never executed and no in-page fix can ever work; marks but no
      "frame" means the surface died. Either way: evidence, not another guess.
*/
(function () {
  "use strict";

  /* ---- HOST GUARD -----------------------------------------------------------
     Must run before CSInterface.js is parsed. See the header. Everything below
     it depends on the page still being alive, so this goes first, and it is
     wrapped so the guard itself can never be what kills the page. */
  var HOST_WAS_NOT_READY = "";
  (function guardHost() {
    try {
      var cep = window.__adobe_cep__;
      if (!cep) return;                       /* not in Premiere - nothing to guard */

      /* Enough of the real shape that anything reading it gets sane values.
         Premiere's own answer replaces this the moment it can give one. */
      var FALLBACK_ENV = '{"appName":"PPRO","appVersion":"0.0.0","appLocale":"en_US",' +
        '"appUILocale":"en_US","appId":"PPRO","isAppOnline":false,' +
        '"appSkinInfo":{"baseFontFamily":"Adobe Clean","baseFontSize":11,' +
        '"appBarBackgroundColor":{"type":1,"color":{"red":50,"green":50,"blue":50,"alpha":255}},' +
        '"panelBackgroundColor":{"type":1,"color":{"red":50,"green":50,"blue":50,"alpha":255}},' +
        '"appBarBackgroundColorSRGB":{"type":1,"color":{"red":50,"green":50,"blue":50,"alpha":255}},' +
        '"panelBackgroundColorSRGB":{"type":1,"color":{"red":50,"green":50,"blue":50,"alpha":255}},' +
        '"systemHighlightColor":{"red":240,"green":72,"blue":30,"alpha":255}}}';

      function guard(name, fallback) {
        var native = cep[name];
        if (typeof native !== "function") {
          cep[name] = function () { HOST_WAS_NOT_READY += name + "(missing) "; return fallback; };
          return;
        }
        cep[name] = function () {
          var v = null;
          try { v = native.apply(cep, arguments); } catch (e) { v = null; }
          if (typeof v === "string" && v !== "") {
            try { JSON.parse(v); return v; } catch (e2) {}
          }
          /* unusable: "" , null, or half a string. Answer something parseable so
             the caller lives, and record that we had to. */
          HOST_WAS_NOT_READY += name + " ";
          return fallback;
        };
      }

      /* Only the calls whose result gets JSON.parsed. getHostEnvironment is the
         one that runs at parse time and is therefore the one that blanks panels.
         The other two are called from methods, but a throw there is just as
         pointless, and guarding costs nothing. */
      guard("getHostEnvironment", FALLBACK_ENV);
      guard("getHostCapabilities", "{}");
      guard("getCurrentApiVersion", '{"major":9,"minor":0,"micro":0}');
    } catch (eGuard) { /* a guard that throws would BE the bug it prevents */ }
  })();

  var NAME = (window.LLLOC_PANEL || "PANEL");
  var KEY = "llloc.boot." + NAME.toLowerCase();
  var t0 = (new Date()).getTime();
  var session = { start: t0, at: "", marks: [], ua: "" };
  var stage = 0;
  /* reopen / reload are only honest while a panel is still coming up */
  var REOPEN_WINDOW_MS = 15000;
  var manualRecovery = false;
  function mayReopen() {
    if (manualRecovery) return true;
    return ((new Date()).getTime() - t0) < REOPEN_WINDOW_MS;
  }
  var recovering = false;

  try { session.ua = (navigator.userAgent || "").slice(0, 120); } catch (e) {}
  try { session.at = (new Date()).toString().slice(0, 24); } catch (e) {}

  function log(msg) {
    try { if (window.console && console.log) console.log("[" + NAME + " revive] " + msg); } catch (e) {}
  }

  /* ---- boot journal ------------------------------------------------------ */
  function mark(what) {
    try {
      session.marks.push(what + "@" + ((new Date()).getTime() - t0) + "ms");
      save();
    } catch (e) {}
  }
  function save() {
    try {
      var all = [];
      try { all = JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) {}
      if (!all.length || all[all.length - 1].start !== session.start) all.push(session);
      else all[all.length - 1] = session;
      while (all.length > 6) all.shift();
      localStorage.setItem(KEY, JSON.stringify(all));
    } catch (e) {}
  }
  function previous() {
    try {
      var all = JSON.parse(localStorage.getItem(KEY) || "[]"), i;
      for (i = all.length - 1; i >= 0; i--) {
        if (all[i].start !== session.start) return all[i];
      }
    } catch (e) {}
    return null;
  }
  window.LLLOC_REPORT = function () {
    try { return localStorage.getItem(KEY) || "[]"; } catch (e) { return "[]"; }
  };
  window.LLLOC_MARK = mark;

  mark("script");
  /* If the guard had to substitute, that IS the diagnosis for a blank panel -
     put it in the journal so the Startup report names it. */
  if (HOST_WAS_NOT_READY) {
    mark("hostNotReady:" + HOST_WAS_NOT_READY.replace(/\s+$/, "").split(" ").join(","));
    log("the CEP host was not ready at load (" + HOST_WAS_NOT_READY.replace(/\s+$/, "") +
        ") - guarded, so the panel still runs");
  }
  try { document.addEventListener("DOMContentLoaded", function () { mark("dom"); }); } catch (e) {}
  try { window.addEventListener("load", function () { mark("load"); }); } catch (e) {}
  try {
    if (window.requestAnimationFrame) {
      window.requestAnimationFrame(function () { mark("frame"); });
    }
  } catch (e) {}

  /* ---- is the compositor alive? ------------------------------------------
     Resolves true if a frame is painted within `ms`. A hidden panel is not a
     fault - nothing is meant to paint - so treat it as alive. */
  function framePainted(ms, cb) {
    var done = false;
    try { if (document.hidden) { cb(true); return; } } catch (e) {}
    if (!window.requestAnimationFrame) { cb(true); return; }
    var t = window.setTimeout(function () {
      if (!done) { done = true; cb(false); }
    }, ms);
    window.requestAnimationFrame(function () {
      if (!done) { done = true; window.clearTimeout(t); cb(true); }
    });
  }

  /* ---- step 1: make the page dirty enough to force a new frame ---------- */
  function repaintKick() {
    var h = document.documentElement, b = document.body;
    try {
      h.style.transform = "translateZ(0)";
      void h.offsetHeight;
      h.style.transform = "";
      if (b) {
        var d = b.style.display;
        b.style.display = "none";
        void b.offsetHeight;
        b.style.display = d || "";
        b.style.opacity = "0.999";
        void b.offsetHeight;
        b.style.opacity = "";
      }
      window.dispatchEvent(new Event("resize"));
    } catch (e) {}
  }

  /* ---- step 2: ask the host to re-layout our content -------------------- */
  function hostResize() {
    try {
      var cep = window.__adobe_cep__;
      if (!cep || !cep.resizeContent) return false;
      var w = window.innerWidth || 300, ht = window.innerHeight || 500;
      cep.resizeContent(w, Math.max(60, ht - 1));
      window.setTimeout(function () { try { cep.resizeContent(w, ht); } catch (e) {} }, 60);
      return true;
    } catch (e) { return false; }
  }

  /* ---- step 4: the programmatic Window > Extensions > <panel> ----------- */
  function reopenSelf() {
    try {
      var cep = window.__adobe_cep__;
      if (!cep || !cep.requestOpenExtension || !cep.getExtensionId) return false;
      var id = cep.getExtensionId();
      if (!id) return false;
      cep.requestOpenExtension(id, "");
      return true;
    } catch (e) { return false; }
  }

  function escalate() {
    if (recovering) return;
    recovering = true;
    stage++;
    mark("revive" + stage);
    log("surface not painting - recovery step " + stage);

    /* Order matters. Reopening is the one fix known to work, because it is
       literally what the user does from Window > Extensions - a new surface.
       A reload reuses the same dead surface, so it comes last. */
    if (stage === 1) {
      repaintKick();
    } else if (stage === 2) {
      repaintKick();
      hostResize();
    } else if (stage === 3) {
      if (!mayReopen()) {
        /* Past the opening window an unpainted surface almost always means the
           panel simply is not on screen. Stop here rather than reopen it. */
        log("not painting, but the panel has been up a while - treating as off-screen, not dead");
        stage = 0; recovering = false; return;
      }
      if (!reopenSelf()) log("reopen unavailable on this host");
    } else if (stage === 4) {
      var n = 0;
      try {
        var m = /v(\d+)/.exec(window.location.hash || "");
        if (m) n = parseInt(m[1], 10);
      } catch (e) {}
      if (!mayReopen()) { stage = 0; recovering = false; return; }
      if (n < 1) {
        try {
          window.location.hash = "v" + (n + 1);
          window.location.reload();
        } catch (e2) {}
        /* If the reload really happened this timer dies with the document. If it
           did not, carry on escalating instead of hanging here. */
        window.setTimeout(function () { recovering = false; escalate(); }, 2500);
        return;
      }
    } else if (stage === 5) {
      if (!mayReopen()) { stage = 0; recovering = false; return; }
      reopenSelf();
    } else {
      log("giving up - use the panel menu > Fix blank panel");
      recovering = false;
      if (manualRecovery) {
        manualRecovery = false;
        /* Asked for by hand and still dead: the page is running, so a dialog
           will show even though nothing paints. Tell them the one move left. */
        try {
          window.alert(NAME + " could not be revived from inside the panel.\n\n" +
            "The page is running - this dialog proves it - but the surface will " +
            "not paint, and reopening an already-open panel only brings it " +
            "forward rather than rebuilding it.\n\n" +
            "Close this panel (its \u2261 menu > Close Panel), then reopen it from " +
            "Window > Extensions. That builds a new surface and always works.");
        } catch (e) {}
      }
      return;
    }

    window.setTimeout(function () {
      recovering = false;
      framePainted(900, function (alive) {
        if (alive) { mark("alive" + stage); log("recovered at step " + stage); stage = 0; }
        else { escalate(); }
      });
    }, 700);
  }

  /* WHAT THE PAGE CAN ACTUALLY SEE. Recorded, never acted on - acting on any of
     these today would be a guess, and this module has already shipped one guess
     that could not fire. Read it out of the Startup report. */
  function look(alive) {
    try {
      var d = document, e = d.documentElement;
      var r = (e && e.getBoundingClientRect) ? e.getBoundingClientRect() : { width: 0, height: 0 };
      var f = "?";
      try { f = (d.hasFocus && d.hasFocus()) ? "1" : "0"; } catch (x) {}
      mark("look paint=" + (alive ? 1 : 0) +
           " hid=" + (d.hidden ? 1 : 0) +
           " vis=" + (d.visibilityState || "?") +
           " win=" + (window.innerWidth | 0) + "x" + (window.innerHeight | 0) +
           " doc=" + ((e && e.offsetWidth) | 0) + "x" + ((e && e.offsetHeight) | 0) +
           " box=" + Math.round(r.width || 0) + "x" + Math.round(r.height || 0) +
           " foc=" + f);
    } catch (e2) {}
  }

  function check(waitMs) {
    framePainted(waitMs || 1200, function (alive) {
      look(alive);
      if (!alive) escalate();
    });
  }

  /* First check once the panel has had a moment to come up, then a couple of
     later passes: a restored panel can go dead after its first frame. */
  window.setTimeout(function () { check(1500); }, 1200);
  window.setTimeout(function () { check(1200); }, 4000);
  window.setTimeout(function () { check(1200); }, 9000);
  /* Past the reopen window, so this one can only ever record. A panel that is
     grey when the user finally looks at it is the case with no reading at all. */
  window.setTimeout(function () { check(1200); }, 20000);

  /* Coming back to Premiere is the moment a dead surface shows itself. */
  window.addEventListener("focus", function () {
    window.setTimeout(function () { check(1000); }, 300);
  });
  document.addEventListener("visibilitychange", function () {
    if (!document.hidden) window.setTimeout(function () { check(1000); }, 300);
  });

  /* ---- close when DOCK asks -------------------------------------------
     The only cure for a surface that will not paint is a NEW surface, and only
     closing the panel and opening it again builds one. This panel cannot do
     that to itself: closeExtension() ends the script before it could reopen
     anything. DOCK can, so DOCK drives it and this end just goes quietly.

     DOCK sends the TARGET's extension id as the payload, so a panel acts only
     on its own name. Nothing here fires on its own - a person clicks. */
  function closeSelf() {
    try { sayBye(); } catch (eB) {}
    try { if (window.__adobe_cep__ && window.__adobe_cep__.closeExtension) window.__adobe_cep__.closeExtension(); } catch (e) {}
    window.setTimeout(function () {
      try { window.close(); } catch (e) {}
    }, 200);
  }
  var closeAsked = false;
  function myExtId() {
    try { return String(window.__adobe_cep__.getExtensionId() || ""); } catch (e) { return ""; }
  }
  /* getSystemPath returns a percent-encoded file:// URI, not a path. cep.fs
     wants a native path. This cost the suite a week once - see DOCK. */
  function nativePath(kind) {
    var p = "";
    try { p = String(window.__adobe_cep__.getSystemPath(kind) || ""); } catch (e) { return ""; }
    if (!p) return "";
    if (p.indexOf("%") > -1) { try { p = decodeURI(p); } catch (e2) {} }
    if (p.indexOf("file:///") === 0) p = "/" + p.substring(8);
    else if (p.indexOf("file://") === 0) p = p.substring(7);
    if (/^\/[A-Za-z]:/.test(p)) p = p.substring(1);
    return p;
  }
  /* Tell DOCK we are going, so it can reopen the moment we are gone instead of
     waiting out a timer. CSEvent comes from CSInterface.js, which loads AFTER
     this module - by the time anyone clicks it is there, but never assume it. */
  function sayClosing(me) {
    var ev = null;
    try { ev = new CSEvent("com.llllllloc.dock.closing", "APPLICATION", "", ""); }
    catch (e) {
      ev = { type: "com.llllllloc.dock.closing", scope: "APPLICATION",
             appId: "", extensionId: "" };
    }
    try { ev.data = me; window.__adobe_cep__.dispatchEvent(ev); } catch (e2) {}
  }
  function doClose(how) {
    if (closeAsked) return;
    closeAsked = true;
    mark("close:asked via " + how);
    log("DOCK asked this panel to close (" + how + ")");
    sayClosing(myExtId());
    window.setTimeout(closeSelf, 0);
    /* STILL HERE? Then Premiere refused, and that is the whole answer. A page
       that is running two seconds after closeExtension() proves the call did
       nothing, and neither closeExtension nor window.close ever reports it. */
    window.setTimeout(function () {
      mark("close:IGNORED - still running, Premiere refused to close this panel");
      log("close was ignored - the panel is still running");
    }, 2000);
  }

  /* route 1: the CEP event */
  try {
    var cep0 = window.__adobe_cep__;
    if (cep0 && cep0.addEventListener) {
      cep0.addEventListener("com.llllllloc.dock.rescue", function (ev) {
        var me = myExtId();
        if (!me || !ev || String(ev.data) !== me) return;
        doClose("event");
      });
    }
  } catch (e) {}

  /* route 2: a file DOCK writes and every panel reads. No event delivery in the
     way. One small read a second, on a filesystem the panel already uses. */
  try {
    var REQ = "";
    var base = nativePath("userData");
    if (base) { REQ = base + "/CSXS/llllllloc/dock-request.json"; }
    var lastSeen = 0;
    if (REQ && window.cep && window.cep.fs && window.cep.fs.readFile) {
      window.setInterval(function () {
        if (closeAsked) return;
        var r = null;
        try { r = window.cep.fs.readFile(REQ); } catch (e) { return; }
        if (!r || r.err !== 0 || !r.data) return;
        var o = null;
        try { o = JSON.parse(r.data); } catch (e2) { return; }
        if (!o || !o.close || !o.at) return;
        if (o.at === lastSeen) return;
        var me = myExtId();
        if (String(o.close) !== me) { lastSeen = o.at; return; }
        /* GUARD 1: four seconds, not twenty. A request must not outlive the
           reopen it triggers, or the new page obeys it all over again. */
        var age = (new Date()).getTime() - Number(o.at);
        if (!(age >= -3000 && age < 4000)) { lastSeen = o.at; return; }
        /* GUARD 2: have we already obeyed this exact request? localStorage
           survives the panel being closed and opened again, which is the whole
           point - the in-page lastSeen above does not. */
        var seenKey = "llloc.obeyed." + me;
        try {
          if (String(localStorage.getItem(seenKey) || "") === String(o.at)) {
            lastSeen = o.at; return;
          }
          localStorage.setItem(seenKey, String(o.at));
        } catch (e3) {}
        lastSeen = o.at;
        doClose("file");
      }, 350);
    }
  } catch (e) {}

  /* ---- presence: this panel tells DOCK whether it is open ----------------
     See the v3.7 header note. One dispatch per announcement, no polling. */
  var P_OPEN = "com.llllllloc.presence.open";
  var P_CLOSED = "com.llllllloc.presence.closed";
  var P_WHOIS = "com.llllllloc.presence.whois";
  function sendPresence(type) {
    var me = myExtId();
    if (!me) return false;
    var ev = null;
    try { ev = new CSEvent(type, "APPLICATION", "", ""); }
    catch (e) {
      ev = { type: type, scope: "APPLICATION", appId: "", extensionId: "" };
    }
    try { ev.data = me; window.__adobe_cep__.dispatchEvent(ev); return true; }
    catch (e2) { return false; }
  }
  /* boot: the host may not know who this panel is yet - keep trying briefly,
     then stop for good. DOCK's who-is-there covers a boot slower than this. */
  (function bootPresence() {
    var tries = 0;
    function go() {
      tries++;
      if (sendPresence(P_OPEN)) { mark("presence:open"); return; }
      if (tries < 6) window.setTimeout(go, 700);
    }
    try { go(); } catch (e) {}
  })();
  /* DOCK asks, every live panel answers */
  try {
    var cepW = window.__adobe_cep__;
    if (cepW && cepW.addEventListener) {
      cepW.addEventListener(P_WHOIS, function () { sendPresence(P_OPEN); });
    }
  } catch (e) {}
  /* gone is gone, whoever closed it - the traffic light included */
  var saidBye = false;
  function sayBye() {
    if (saidBye) return;
    saidBye = true;
    sendPresence(P_CLOSED);
  }
  try { window.addEventListener("beforeunload", sayBye); } catch (e) {}
  try { window.addEventListener("pagehide", sayBye); } catch (e) {}
  try { window.addEventListener("unload", sayBye); } catch (e) {}

  /* Exposed so the panel menu can force a full recovery by hand. */
  window.LLLOC_REVIVE = function () {
    manualRecovery = true; stage = 0; recovering = false; escalate();
  };

  /* ---- flyout menu --------------------------------------------------------
     Owned here rather than in the panel script, because the whole point is to
     still work on a panel whose script never ran. Panels add their own items
     with LLLOC_MENU_ADD. */
  var MENU = [];
  function buildMenu() {
    try {
      var xml = "<Menu>", i;
      for (i = 0; i < MENU.length; i++) {
        if (MENU[i].sep) { xml += '<MenuItem Label="---"/>'; continue; }
        xml += '<MenuItem Id="' + MENU[i].id + '" Label="' + MENU[i].label +
               '" Enabled="true" Checked="false"/>';
      }
      xml += "</Menu>";
      window.__adobe_cep__.invokeSync("setPanelFlyoutMenu", xml);
      return true;
    } catch (e) { return false; }
  }
  function onMenu(ev) {
    var id = "", i;
    try { id = (ev && ev.data && ev.data.menuId) ? ev.data.menuId : ""; } catch (e) {}
    for (i = 0; i < MENU.length; i++) {
      if (MENU[i].id === id && MENU[i].fn) { try { MENU[i].fn(); } catch (e2) {} return; }
    }
  }
  window.LLLOC_MENU_ADD = function (id, label, fn) {
    MENU.push({ id: id, label: label, fn: fn });
    buildMenu();
  };
  MENU.push({ id: "llrReport", label: "Startup report", fn: function () { showReport(); } });
  MENU.push({ id: "llrFix", label: "Fix blank panel", fn: function () { window.LLLOC_REVIVE(); } });
  MENU.push({ id: "llrReload", label: "Reload panel", fn: function () { window.location.reload(); } });
  MENU.push({ sep: true });
  try {
    window.__adobe_cep__.addEventListener("com.adobe.csxs.events.flyoutMenuClicked", onMenu);
  } catch (e) {}
  buildMenu();
  window.setTimeout(buildMenu, 1500);

  /* ---- the report, on demand --------------------------------------------- */
  function showReport() {
   try {
    var prev = previous(), txt = "";
    try { txt = NAME + " | " + session.at + "\n" + session.ua + "\n\n" + window.LLLOC_REPORT(); } catch (e) {}
    var verdict;
    if (!prev) {
      verdict = "No earlier session on record. If the panel was blank before this " +
                "one, that means the page never ran at all - Premiere did not load it.";
    } else {
      var marks = (prev.marks || []).join(" ");
      if (marks.indexOf("frame@") >= 0) {
        verdict = "The previous session started at " + (prev.at || "?") +
                  " and painted normally.";
      } else {
        verdict = "The previous session ran but never painted a frame - its panel " +
                  "surface was dead.";
      }
    }
    var old = document.getElementById("llrBox");
    if (old) { try { old.parentNode.removeChild(old); } catch (e) {} }
    var box = document.createElement("div");
    box.id = "llrBox";
    box.setAttribute("style",
      "position:fixed;left:0;right:0;bottom:0;top:0;z-index:99999;background:#171613;color:#EDEBE4;" +
      "padding:12px;font:400 10px/1.5 monospace;overflow:auto");
    box.innerHTML =
      '<div style="font-weight:700;letter-spacing:.1em;color:#F0481E;margin-bottom:6px">STARTUP REPORT</div>' +
      '<div style="color:#8F8E86;margin-bottom:8px">' + verdict + '</div>' +
      '<textarea id="llrTxt" readonly style="width:100%;height:150px;background:#201F1B;color:#EDEBE4;' +
      'border:1px solid #33322D;font:400 9px/1.4 monospace;padding:6px"></textarea>' +
      '<div style="margin-top:8px">' +
      '<button id="llrCopy2" style="font:700 9px monospace;letter-spacing:.08em;padding:7px 11px;' +
      'background:#F0481E;color:#fff;border:none;cursor:pointer;margin-right:6px">COPY REPORT</button>' +
      '<button id="llrClose" style="font:700 9px monospace;letter-spacing:.08em;padding:7px 11px;' +
      'background:#2B2A25;color:#EDEBE4;border:1px solid #3C3B35;cursor:pointer">CLOSE</button></div>';
    try { document.body.appendChild(box); } catch (e) { return; }
    var ta = document.getElementById("llrTxt");
    if (ta) ta.value = txt;
    var c = document.getElementById("llrCopy2");
    if (c) c.onclick = function () {
      try { ta.select(); document.execCommand("copy"); c.textContent = "COPIED"; }
      catch (e) { c.textContent = "COPY FAILED"; }
    };
    var x = document.getElementById("llrClose");
    if (x) x.onclick = function () { try { box.parentNode.removeChild(box); } catch (e) {} };
   } catch (err) { log("report failed: " + err); }
  }
  window.LLLOC_SHOWREPORT = showReport;

  /* ---- report on the previous session ------------------------------------
     Shown only when the last session looks wrong, so a healthy panel never
     nags. The user reopened this panel by hand precisely because the previous
     one was blank - this is the moment to tell them what happened. */
  function reportPrevious() {
   try {
    /* Only stay quiet when this session itself painted AND the previous one did
       too. Anything else is worth surfacing - including "there is no previous
       session", which is what a restart that never ran the page looks like. */
    var p = previous();
    var marks = p ? (p.marks || []).join(" ") : "";
    var painted = marks.indexOf("frame@") >= 0;
    var mine = (session.marks || []).join(" ");
    if (p && painted) return;
    if (!p && mine.indexOf("frame@") >= 0 && !window.LLLOC_FORCE_REPORT) {
      /* genuinely the first run on this machine - nothing to report */
      return;
    }
    var verdict = p
      ? "the previous session ran but never painted a frame - its surface was dead"
      : "no earlier session on record - if the panel was blank before this, the page never ran";

    var box = document.createElement("div");
    box.setAttribute("style",
      "position:fixed;left:0;right:0;bottom:0;z-index:9999;background:#201F1B;color:#EDEBE4;" +
      "border-top:2px solid #F0481E;padding:9px 11px;font:400 10px/1.5 monospace");
    box.innerHTML =
      '<div style="font-weight:700;letter-spacing:.1em;color:#F0481E;margin-bottom:4px">LAST STARTUP WAS BLANK</div>' +
      '<div style="color:#8F8E86;margin-bottom:7px">' + verdict + '</div>' +
      '<button id="llrCopy" style="font:700 9px monospace;letter-spacing:.08em;padding:6px 10px;' +
      'background:#F0481E;color:#fff;border:none;cursor:pointer;margin-right:6px">COPY REPORT</button>' +
      '<button id="llrHide" style="font:700 9px monospace;letter-spacing:.08em;padding:6px 10px;' +
      'background:#2B2A25;color:#EDEBE4;border:1px solid #3C3B35;cursor:pointer">DISMISS</button>';
    try { document.body.appendChild(box); } catch (e) { return; }

    var c = document.getElementById("llrCopy");
    if (c) c.onclick = function () {
      try {
        var ta = document.createElement("textarea");
        ta.value = NAME + " | " + session.ua + "\n" + window.LLLOC_REPORT();
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        document.body.removeChild(ta);
        c.textContent = "COPIED";
      } catch (e) { c.textContent = "COPY FAILED"; }
    };
    var hd = document.getElementById("llrHide");
    if (hd) hd.onclick = function () { try { box.parentNode.removeChild(box); } catch (e) {} };
   } catch (err) { log("report failed: " + err); }
  }
  window.setTimeout(reportPrevious, 2500);
})();
