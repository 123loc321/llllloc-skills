#!/usr/bin/env python3
"""Check a built Lord Of The Prompt deck. Every check is a measurement.

    python3 scripts/test-deck.py "<job>/*_CLAUDE/5_Prompts/MyDeck.html"

Tabs, keyboard, search across tabs, text contrast in BOTH themes, line length,
hit-box sizes, page scroll at L / M / S, sideways overflow from 1440 to 390,
the overflow fade, and print.

It needs playwright. Without it the script says so and exits 0 — a missing test
tool is not a broken deck. Exit 1 means a real failure, and the failing line
names what to fix.
"""
import sys, pathlib

if len(sys.argv) < 2:
    sys.exit("usage: test-deck.py <deck.html>")
DECK = pathlib.Path(sys.argv[1]).resolve()
if not DECK.is_file():
    sys.exit("no deck at %s" % DECK)
URL = DECK.as_uri()

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("playwright is not installed — skipping the gate. The deck still ships.")
    raise SystemExit(0)

# APCA-W3 0.1.9. It is not a pass/fail gate here - WCAG 2.2 is still the
# standard and the standard is what the gate enforces. This reports how the
# same pairs score perceptually, because WCAG 2 is known to be unreliable
# exactly where this deck lives: small type, and a near-black dark theme.
APCA = r"""
(()=>{const Y=s=>{const m=s.match(/\d+/g).map(Number);
  const f=c=>Math.pow(c/255,2.4);
  return 0.2126729*f(m[0])+0.7151522*f(m[1])+0.0721750*f(m[2]);};
const lc=(txt,bg)=>{let t=Y(txt),b=Y(bg);
  const TH=0.022,CL=1.414;
  t=t>TH?t:t+Math.pow(TH-t,CL); b=b>TH?b:b+Math.pow(TH-b,CL);
  if(Math.abs(b-t)<0.0005) return 0;
  let o;
  if(b>t){o=(Math.pow(b,0.56)-Math.pow(t,0.57))*1.14; o=o<0.1?0:o-0.027;}
  else   {o=(Math.pow(b,0.65)-Math.pow(t,0.62))*1.14; o=o>-0.1?0:o+0.027;}
  return o*100;};
// same compositing as the contrast probe: a translucent fill read raw is a
// near-black lie, and here it collapsed the prompt block's score to Lc0.
const rgba=s=>{const m=(s||'').match(/[\d.]+/g); if(!m) return null;
  return [+m[0],+m[1],+m[2], m.length>3 ? +m[3] : 1];};
const bgOf=el=>{const stack=[]; let n=el;
  while(n&&n!==document.documentElement){
    const c=rgba(getComputedStyle(n).backgroundColor);
    if(c&&c[3]>0){stack.push(c); if(c[3]>=1) break;}
    n=n.parentElement;}
  const root=rgba(getComputedStyle(document.documentElement).backgroundColor)||[255,255,255,1];
  if(!stack.length||stack[stack.length-1][3]<1) stack.push(root);
  let out=stack.pop();
  while(stack.length){const t=stack.pop(), a=t[3];
    out=[t[0]*a+out[0]*(1-a), t[1]*a+out[1]*(1-a), t[2]*a+out[2]*(1-a), 1];}
  return 'rgb('+Math.round(out[0])+', '+Math.round(out[1])+', '+Math.round(out[2])+')';};
const st=document.createElement('style');
st.textContent='#scroller .card{content-visibility:visible !important}';
document.head.appendChild(st); void document.body.offsetHeight;
const out=[];
document.querySelectorAll('.prompt-text,.chars,.spec .k,.spec .v,.tbn .tl,.foot,.meta>summary')
 .forEach(el=>{const r=el.getBoundingClientRect(); if(!r.width) return;
   const s=getComputedStyle(el);
   out.push({n:(el.className||el.tagName).trim().split(' ')[0],
             px:parseFloat(s.fontSize), v:Math.abs(lc(s.color,bgOf(el)))});});
st.remove();
const seen={}; out.forEach(o=>{if(!seen[o.n]||o.v<seen[o.n].v) seen[o.n]=o;});
return Object.values(seen).sort((a,b)=>a.v-b.v)
       .map(o=>o.n+' '+o.px+'px Lc'+o.v.toFixed(0));})()
"""

fails = []


def chk(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + ("   " + str(detail) if detail != "" else ""))
    if not cond:
        fails.append(name)


# Walk every text node, read its computed color against the nearest PAINTED
# background, and compare. Small text needs 4.5:1. Large text (24px, or 18.66px
# bold) needs 3:1. This is the probe that found seven failures in the light
# theme that eighteen days of looking at it did not.
CONTRAST = r"""
(()=>{
// A content-visibility:auto subtree that is off screen is NOT rendered, and
// getComputedStyle on it returns STALE values - a card below the fold kept the
// dark theme's grey after a switch to light and read as a contrast failure that
// does not exist. The pixel it actually paints is correct; only the query is
// stale. An INLINE style does not clear it. Injecting a STYLESHEET does,
// because that forces a recalculation the browser cannot skip.
const st=document.createElement('style');
st.textContent='#scroller .card{content-visibility:visible !important}';
document.head.appendChild(st);
void document.body.offsetHeight;
const restore=()=>st.remove();
const lin=c=>{c/=255;return c<=0.04045?c/12.92:Math.pow((c+0.055)/1.055,2.4)};
const L=s=>{const m=s.match(/\d+/g).map(Number);return 0.2126*lin(m[0])+0.7152*lin(m[1])+0.0722*lin(m[2])};
const cr=(a,b)=>{const x=L(a),y=L(b),h=Math.max(x,y),l=Math.min(x,y);return (h+0.05)/(l+0.05)};
// A TRANSLUCENT BACKGROUND MUST BE COMPOSITED BEFORE IT IS MEASURED.
// rgba(23,23,23,.035) over white is #F7F7F7, but a naive reader takes the first
// three numbers and calls it near-black - a contrast failure that does not
// exist. Walk up, blend each layer onto the one behind it, stop at opaque.
const rgba=s=>{const m=(s||'').match(/[\d.]+/g); if(!m) return null;
  return [+m[0],+m[1],+m[2], m.length>3 ? +m[3] : 1];};
const bgOf=el=>{const stack=[]; let n=el;
  while(n&&n!==document.documentElement){
    const c=rgba(getComputedStyle(n).backgroundColor);
    if(c&&c[3]>0){stack.push(c); if(c[3]>=1) break;}
    n=n.parentElement;}
  const root=rgba(getComputedStyle(document.documentElement).backgroundColor)||[255,255,255,1];
  if(!stack.length||stack[stack.length-1][3]<1) stack.push(root);
  let out=stack.pop();
  while(stack.length){const t=stack.pop(), a=t[3];
    out=[t[0]*a+out[0]*(1-a), t[1]*a+out[1]*(1-a), t[2]*a+out[2]*(1-a), 1];}
  return 'rgb('+Math.round(out[0])+', '+Math.round(out[1])+', '+Math.round(out[2])+')';};
const out=[];
const sel='.tbn .tl,.tbn .tn,.prompt-text,.chars,.spec .k,.spec .v,'
        + '.copy-btn,.now,.badge-new,.sub,.eyebrow,.foot,.archive>summary,.meta>summary,.tab,.dim';
document.querySelectorAll(sel).forEach(el=>{
  const r=el.getBoundingClientRect(); if(!r.width||!r.height) return;
  const s=getComputedStyle(el); const ratio=cr(s.color,bgOf(el));
  const px=parseFloat(s.fontSize), bold=parseInt(s.fontWeight,10)>=700;
  const need=(px>=24||(bold&&px>=18.66))?3:4.5;
  if(ratio<need-0.02) out.push((el.className||el.tagName).trim()+'  '+px+'px w'+s.fontWeight
                               +'  '+ratio.toFixed(2)+':1  needs '+need);});
restore();
return out.filter((v,i,a)=>a.indexOf(v)===i);})()
"""


def run():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 860})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL)
        pg.wait_for_timeout(900)
        chk("no JS errors", not errs, errs[:2])

        units = pg.eval_on_selector_all("#scroller > .card, #scroller > .group", "e=>e.length")
        tabs = pg.eval_on_selector_all(".tbn", "e=>e.length")

        if units < 2:
            chk("one prompt: the strip hides itself",
                pg.eval_on_selector("#tabs", "e=>getComputedStyle(e).display") == "none")
        else:
            chk("one tab for each prompt, plus ALL", tabs == units + 1,
                "{} tabs / {} prompts".format(tabs, units))
            chk("ALL is pinned outside the rail",
                pg.eval_on_selector_all("#trail .allb", "e=>e.length") == 0)
            chk("exactly one tab selected",
                pg.eval_on_selector_all('.tbn[aria-selected="true"]', "e=>e.length") == 1)
            chk("ALL shows every prompt",
                pg.eval_on_selector_all("#scroller > .card, #scroller > .group",
                                        "e=>e.filter(x=>getComputedStyle(x).display!=='none').length") == units)

        # the rest of the tab checks need a built strip. An older deck has none,
        # so skip them and let the contrast and measure checks speak instead.
        if tabs >= 2:
            pg.eval_on_selector_all(".tbn", "e=>e[1].click()")
            pg.wait_for_timeout(200)
            chk("a tab shows exactly one prompt",
                pg.eval_on_selector_all("#scroller > .card, #scroller > .group",
                                        "e=>e.filter(x=>getComputedStyle(x).display!=='none').length") == 1)

            # compare the INDEX, not the label. Two prompts may legitimately
            # share a name, and a label comparison then reads a real move as no
            # move - which is exactly what the starter deck did.
            sel = '''()=>[...document.querySelectorAll('.tbn')]
                     .findIndex(t=>t.getAttribute('aria-selected')==='true')'''
            first = pg.evaluate(sel)
            pg.eval_on_selector('.tbn[aria-selected="true"]', "e=>e.focus()")
            pg.keyboard.press("ArrowRight")
            pg.wait_for_timeout(180)
            chk("one press moves ONE tab", pg.evaluate(sel) == first + 1,
                "{} -> {}".format(first, pg.evaluate(sel)))
            pg.keyboard.press("Home")
            pg.wait_for_timeout(180)
            chk("Home returns to ALL",
                pg.eval_on_selector('.tbn[aria-selected="true"] .tl', "e=>e.textContent") == "All")
            chk("roving tabindex: one keyboard stop",
                pg.eval_on_selector_all(".tbn", "e=>e.filter(x=>x.tabIndex===0).length") == 1)

            # A SEARCH STEERS THE STRIP.
            # One match -> the strip goes to that prompt's tab. Several or none
            # -> ALL, which is what lets a search reach across hidden panels.
            pg.eval_on_selector_all(".tbn", "e=>e[e.length-1].click()")
            pg.wait_for_timeout(160)
            uniq = pg.evaluate("""()=>{
              const us=[...document.querySelectorAll('#scroller > .card, #scroller > .group')];
              const texts=us.map(u=>(u.textContent||'').toLowerCase());
              const words=texts[0].split(/\\s+/).filter(w=>w.length>6 && /^[a-z]+$/.test(w));
              for(const w of words) if(texts.filter(t=>t.includes(w)).length===1) return w;
              return '';}""")
            if uniq:
                pg.fill("#q", uniq); pg.wait_for_timeout(300)
                st = pg.evaluate("""()=>{
                  const sel=[...document.querySelectorAll('.tbn')].findIndex(
                              t=>t.getAttribute('aria-selected')==='true');
                  const vis=[...document.querySelectorAll('#scroller > .card, #scroller > .group')]
                            .filter(x=>getComputedStyle(x).display!=='none').length;
                  return {sel:sel, vis:vis};}""")
                chk("one match jumps to that prompt's tab",
                    st["sel"] == 1 and st["vis"] == 1, st)

            # a word every prompt shares must fall back to ALL
            pg.fill("#q", "a"); pg.wait_for_timeout(300)
            sel = pg.evaluate("""()=>[...document.querySelectorAll('.tbn')]
                    .findIndex(t=>t.getAttribute('aria-selected')==='true')""")
            chk("several matches fall back to ALL", sel == 0, sel)

            # a tab NAME is searchable, even though it is not inside the card
            name = pg.eval_on_selector("#trail .tbn .tl", "e=>e.textContent")
            pg.fill("#q", name.split(" ")[-1].lower()); pg.wait_for_timeout(300)
            found = pg.eval_on_selector_all(
                "#scroller > .card, #scroller > .group",
                "e=>e.filter(x=>getComputedStyle(x).display!=='none').length")
            chk("a tab name is searchable", found >= 1, "'" + name + "' -> " + str(found))

            pg.fill("#q", ""); pg.wait_for_timeout(260)
            chk("clearing the search returns to ALL",
                pg.evaluate("""()=>[...document.querySelectorAll('.tbn')]
                    .findIndex(t=>t.getAttribute('aria-selected')==='true')""") == 0)


        # CONTRAST IS MEASURED ON A FRESH LOAD PER THEME, in its own page.
        # Toggling the theme at runtime gave a false failure twice: a card below
        # the fold sits in a content-visibility:auto subtree that the browser
        # does not restyle while it is off screen, so getComputedStyle returned
        # the OLD theme's grey. The pixel it paints is correct - only the query
        # was stale. A fresh load has no stale subtree, no transition mid-flight
        # and no hover state, and it is how the file is really opened.
        for theme in ("dark", "light"):
            tp = b.new_page(viewport={"width": 1000, "height": 900})
            tp.add_init_script(
                "try{localStorage.setItem('lotp.theme','%s')}catch(e){}" % theme)
            tp.goto(URL)
            tp.wait_for_timeout(900)
            bad = tp.evaluate(CONTRAST)
            chk("text contrast passes in " + theme, not bad, bad[:5])
            # APCA ADVISORY, never a failure. The APCA author's own note: once
            # the brighter colour is darker than #a0a0a0, the WCAG 2 formula
            # degrades until it stops being useful, and it OVERSTATES contrast
            # when both colours are dark. Our dark page is #171717, so every
            # dark-mode number above sits in that range. Report the perceptual
            # score so the weakest pairs are visible even though WCAG 2 passes.
            lc = tp.evaluate(APCA)
            if lc:
                print("         apca advisory (" + theme + ", lowest first): "
                      + "; ".join(lc[:4]))
            tp.close()

        # the measure, taken inside the content box with letter-spacing counted
        ch = pg.evaluate("""()=>{const pre=document.querySelector('.prompt-text'),s=getComputedStyle(pre);
          const probe=document.createElement('span');
          probe.style.cssText='position:absolute;visibility:hidden;white-space:pre';
          probe.style.font=s.font; probe.style.letterSpacing=s.letterSpacing;
          probe.textContent='0'.repeat(200); pre.appendChild(probe);
          const adv=probe.getBoundingClientRect().width/200; probe.remove();
          const zoom=parseFloat(getComputedStyle(document.getElementById('zoomRoot')).zoom)||1;
          return Math.floor((pre.clientWidth-parseFloat(s.paddingLeft)
                            -parseFloat(s.paddingRight))/(adv/zoom));}""")
        chk("prompt line <= 80 characters (WCAG 1.4.8)", ch <= 80, "{} chars".format(ch))

        # THE MEASURE HOLDS AT EVERY PANEL WIDTH AND EVERY UI SIZE.
        # The column fills the panel now, so the type is what holds the line to
        # 80 characters. One reading at one width proves nothing.
        MEASURE = """()=>{const pre=document.querySelector('#scroller .prompt-text'),
          s=getComputedStyle(pre);
          const probe=document.createElement('span');
          probe.style.cssText='position:absolute;visibility:hidden;white-space:pre';
          probe.style.font=s.font; probe.style.letterSpacing=s.letterSpacing;
          probe.textContent='0'.repeat(200); pre.appendChild(probe);
          const adv=probe.getBoundingClientRect().width/200; probe.remove();
          const z=parseFloat(getComputedStyle(document.getElementById('zoomRoot')).zoom)||1;
          return Math.floor((pre.clientWidth-parseFloat(s.paddingLeft)
                            -parseFloat(s.paddingRight))/(adv/z));}"""
        wide = []
        for w in (600, 780, 1000, 1400, 1920):
            pg.set_viewport_size({"width": w, "height": 860})
            for _ in range(3):
                pg.wait_for_timeout(200)
                n = pg.evaluate(MEASURE)
                lab = pg.eval_on_selector("#sizeBtn", "e=>e.textContent")
                if n > 80:
                    wide.append("{}px {} = {} chars".format(w, lab, n))
                pg.eval_on_selector("#sizeBtn", "e=>e.click()")
            pg.wait_for_timeout(200)
        chk("the measure holds at every width and UI size", not wide, wide)

        # AND THE PANEL IS USED. A column that stops far short of the panel is
        # the gap the studio rejected twice. Allow the margin, not a third of the width.
        pg.set_viewport_size({"width": 1000, "height": 860})
        pg.wait_for_timeout(260)
        fill = pg.evaluate("""()=>{const a=document.querySelector('.app');
          const z=parseFloat(getComputedStyle(document.getElementById('zoomRoot')).zoom)||1;
          return Math.round(a.getBoundingClientRect().width/window.innerWidth*100);}""")
        chk("the column uses the panel width", fill >= 80, "{}% of a 1000px panel".format(fill))
        pg.set_viewport_size({"width": 1280, "height": 860})
        pg.wait_for_timeout(220)

        # SC 2.5.8 counts the CLICKABLE AREA, not the icon. And layout pixels
        # are not visual pixels under CSS zoom, so divide the rect by the zoom.
        small = pg.evaluate("""()=>{const out=[];
          const zoom=parseFloat(getComputedStyle(document.getElementById('zoomRoot')).zoom)||1;
          document.querySelectorAll('.tbn,.tnav.show,.copy-btn,.tb,.hbtn,.ck').forEach(el=>{
            const r=el.getBoundingClientRect(); let h=r.height/zoom, w=r.width/zoom;
            const a=getComputedStyle(el,'::after');
            if(a&&a.content&&a.content!=='none'){
              const ah=parseFloat(a.height),aw=parseFloat(a.width);
              if(!isNaN(ah)&&ah>h)h=ah; if(!isNaN(aw)&&aw>w)w=aw;}
            if(h<23.5||w<23.5) out.push(el.className+' '+w.toFixed(0)+'x'+h.toFixed(0));});
          return out;}""")
        chk("every hit box clears 24x24 (SC 2.5.8)", not small, small)

        # NO BOX INSIDE A BOX. the studio reported this by eye on 29 August 2026 and
        # the design system already forbade it. A rule that is written down and
        # broken anyway needs an instrument, not a fourth rewrite. This is the
        # instrument: walk every painted element and fail if its nearest painted
        # ancestor inside the deck is also painted.
        nested = pg.evaluate("""()=>{const out=[];
          const painted=el=>{const b=getComputedStyle(el).backgroundColor;
            return b && b!=='rgba(0, 0, 0, 0)' && b.indexOf(', 0)')<0;};
          document.querySelectorAll('#scroller .prompt-text,#scroller .card,#scroller .meta,#scroller .rail,#scroller .warn')
            .forEach(el=>{ if(!painted(el)) return;
              let n=el.parentElement;
              while(n && n.id!=='scroller'){ if(painted(n)){
                out.push((el.className||el.tagName)+' inside '+(n.className||n.tagName)); break;} n=n.parentElement;}});
          return out.filter((v,i,a)=>a.indexOf(v)===i);}""")
        chk("no filled box inside a filled box", not nested, nested)

        # NEVER LEAVE A GAP. the studio, 29 August 2026: "never leave a gap like this,
        # it must adapt to the width". Two width caps fighting each other is what
        # makes one - a 1040px page holding a 78-character block. There is now
        # ONE cap, the column, and every child of the scroll region must reach it.
        gaps = pg.evaluate("""()=>{const out=[];
          const sc=document.getElementById('scroller'), scs=getComputedStyle(sc);
          const zoom=parseFloat(getComputedStyle(document.getElementById('zoomRoot')).zoom)||1;
          const col=sc.clientWidth-parseFloat(scs.paddingLeft)-parseFloat(scs.paddingRight);
          // an archived card is indented 14px on purpose. That is a hierarchy
          // mark, not a gap, so it is out of scope for this check.
          sc.querySelectorAll('.prompt-text,.sub,.meta,.card-head').forEach(el=>{
            if(el.closest('.archive')) return;
            const r=el.getBoundingClientRect(); if(!r.width) return;
            const w=r.width/zoom;
            if(col-w>6) out.push((el.className||el.tagName).trim()+' '+Math.round(w)
                                  +' of '+Math.round(col)+'px');});
          return out.filter((v,i,a)=>a.indexOf(v)===i);}""")
        chk("nothing stops short of the column", not gaps, gaps)

        # ONE CONTROL HEIGHT PER ROW. A row of controls at three heights reads
        # as three systems. the studio: "align the buttons sizes".
        heights = pg.evaluate("""()=>{const out=[];
          document.querySelectorAll('.card-head').forEach(h=>{
            const hs=new Set();
            h.querySelectorAll('.tab,.now,.badge-new,.copy-btn').forEach(c=>{
              const r=c.getBoundingClientRect(); if(r.height) hs.add(Math.round(r.height));});
            if(hs.size>1) out.push([...hs].join('/'));});
          return out.filter((v,i,a)=>a.indexOf(v)===i);}""")
        chk("one control height per card head", not heights, heights)

        # THE BOTTOM BAR KEEPS ITS NAME. It was silently emptied by a zoom
        # rounding bug for every width. Never let that ship again.
        foot = pg.evaluate("""()=>{const f=document.querySelector('.foot');
          const b=f.querySelector('.fbrand'), c=f.querySelector('.chip');
          const vis=e=>e&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().width>0;
          return {brand:vis(b), version:vis(c),
                  text:(b?b.textContent.trim():'')+' '+(c?c.textContent.trim():'')};}""")
        chk("the bottom bar keeps its name and version",
            foot["brand"] and foot["version"], foot["text"])

        # a prompt changed this turn is marked ON ITS TAB, not only inside it
        if units >= 2:
            dots = pg.evaluate("""()=>{
              const newUnits=[...document.querySelectorAll('#scroller > .card, #scroller > .group')]
                              .map(u=>u.getAttribute('data-new')==='1');
              const tabs=[...document.querySelectorAll('#trail .tbn')]
                              .map(t=>!!t.querySelector('.tdot'));
              return {want:newUnits, got:tabs};}""")
            chk("an updated prompt carries a dot on its tab",
                dots["want"] == dots["got"], dots)

        # the count is written by the engine, so it can never disagree with COPY
        bad_count = pg.evaluate("""()=>{const out=[];
          document.querySelectorAll('.card').forEach(c=>{
            const pre=c.querySelector('.prompt-text'), el=c.querySelector('.card-head .chars');
            if(!pre||!el) return;
            const want=String(pre.textContent.length)+' CHARS';
            if(el.textContent!==want) out.push(el.textContent+' != '+want);});
          return out;}""")
        chk("the character count matches what COPY copies", not bad_count, bad_count)

        # NO STRAY INDENTATION IN A PROMPT. A <pre> keeps every space in the
        # markup, so the lines after the name line pick up the indentation of
        # the surrounding HTML. It shows as a gap before the first word and it
        # goes onto the clipboard. the studio caught it by eye on 29 August 2026.
        indent = pg.evaluate("""()=>{const out=[];
          const ind=l=>l.length-l.replace(/^[ \\t]+/,'').length;
          document.querySelectorAll('.prompt-text').forEach(p=>{
            const lines=p.textContent.split('\\n');
            if(!lines.length) return;
            if(ind(lines[0])>0){out.push('name line indented');return;}
            const body=lines.slice(1).filter(l=>l.trim()).map(ind);
            if(body.length && Math.min(...body)>0)
              out.push(lines[0].trim().slice(0,24)+' +'+Math.min(...body));
            if(!lines[0].trim()||!lines[lines.length-1].trim())
              out.push(lines[0].trim().slice(0,24)+' blank edge');});
          return out;}""")
        chk("no stray indentation in a prompt", not indent, indent)

        # A LIST DIVIDES BY A RULE BETWEEN ITEMS, and the first item has none.
        # :first-child cannot do it - a unit hidden by the tab strip still
        # counts as a child. render() marks the first VISIBLE unit .lead.
        pg.eval_on_selector_all(".tbn", "e=>e[0].click()")
        pg.wait_for_timeout(200)
        # THE RULE BELONGS TO THE ROW ABOVE IT (Tufte). Every row closes with a
        # rule underneath; none carries one on top. And the space BELOW the rule
        # must exceed the space above it, or the rule floats between two rows -
        # which is what the studio rejected twice.
        div = pg.evaluate("""()=>{
          const u=[...document.querySelectorAll('#scroller > .card, #scroller > .group')]
                   .filter(x=>getComputedStyle(x).display!=='none');
          const n=x=>parseFloat(x)||0;
          const bad=[];
          u.forEach(x=>{const s=getComputedStyle(x);
            if(n(s.borderBottomWidth)===0) bad.push('no rule under a row');
            if(n(s.borderTopWidth)>0)      bad.push('a rule on top of a row');
            if(n(s.marginBottom)<=n(s.paddingBottom))
              bad.push('rule floats: '+s.paddingBottom+' above / '+s.marginBottom+' below');});
          return {bad:[...new Set(bad)], rows:u.length,
                  head_filled: u.length ? getComputedStyle(
                    u[0].querySelector('.card-head')).backgroundColor : ''};}""")
        chk("the rule sits under its row, with more air below than above",
            not div["bad"], div["bad"])
        chk("the card head carries no fill of its own",
            div["head_filled"] in ("rgba(0, 0, 0, 0)", "transparent"), div["head_filled"])

        # THE MASTHEAD IS THE TITLE ALONE. the studio removed the eyebrow and the
        # description line on 29 August 2026; the classes went with them, so a
        # body that still carries one would render unstyled.
        old = pg.eval_on_selector_all(".eyebrow, .sub", "e=>e.length")
        chk("no eyebrow and no description line in the masthead", old == 0, old)

        # SPEC IS A TABLE: no fill, and a rule between its rows.
        spec = pg.evaluate("""()=>{const m=document.querySelector('.meta');
          if(!m) return {ok:true};
          const rows=[...m.querySelectorAll('.spec')];
          return {fill:getComputedStyle(m).backgroundColor,
                  ruled:rows.filter(r=>parseFloat(getComputedStyle(r).borderTopWidth)>0).length,
                  rows:rows.length};}""")
        if not spec.get("ok"):
            chk("the SPEC sheet carries no fill",
                spec["fill"] in ("rgba(0, 0, 0, 0)", "transparent"), spec["fill"])
            chk("every SPEC row is ruled like a table",
                spec["ruled"] == spec["rows"], spec)

        # HOVER ANSWERS WITH MARKS, NOT A BLOCK. An element with no container
        # takes an ink shift, not a state layer (eBay playbook). The head row
        # has no container, so a fill appearing under it is the wrong species.
        pg.hover("#scroller .card .card-head .tab")
        pg.wait_for_timeout(260)
        hov = pg.evaluate("""()=>{const h=document.querySelector('#scroller .card .card-head');
          const chip=h.querySelector('.tab');
          return {head_bg:getComputedStyle(h).backgroundColor,
                  chip_bg:getComputedStyle(chip).backgroundColor,
                  chip_ink:getComputedStyle(chip).color};}""")
        pg.mouse.move(2, 2); pg.wait_for_timeout(120)
        rest_ink = pg.eval_on_selector("#scroller .card .card-head .tab",
                                       "e=>getComputedStyle(e).color")
        chk("hover puts no fill behind the head row",
            hov["head_bg"] in ("rgba(0, 0, 0, 0)", "transparent"), hov["head_bg"])
        # the ID is TEXT now, not a chip: hover answers by darkening it, and it
        # must still carry NO fill of its own.
        chk("the ID carries no box",
            hov["chip_bg"] in ("rgba(0, 0, 0, 0)", "transparent"), hov["chip_bg"])
        chk("hover darkens the ID text", hov["chip_ink"] != rest_ink,
            hov["chip_ink"] + " hovered vs " + rest_ink + " at rest")

        # THE DIVIDER IS STRUCTURE, NOT STATE. Hover must not touch it, or the
        # ladder twitches as the pointer runs down the page.
        hov2 = pg.evaluate("""()=>{const u=document.querySelector('#scroller > .card');
          return getComputedStyle(u).borderBottomColor;}""")
        pg.mouse.move(2, 2); pg.wait_for_timeout(260)
        rest = pg.evaluate("""()=>{const u=document.querySelector('#scroller > .card');
          return getComputedStyle(u).borderBottomColor;}""")
        chk("hover leaves the divider alone", hov2 == rest, hov2 + " vs " + rest)

        # THE SELECTED TAB MUST READ, and in dark the fill alone was a whisper.
        tabs_on = pg.evaluate("""()=>{const on=document.querySelector('.tbn[aria-selected="true"]');
          const off=[...document.querySelectorAll('.tbn')].find(t=>t!==on);
          if(!on||!off) return null;
          const a=getComputedStyle(on), b=getComputedStyle(off);
          return {fill_differs:a.backgroundColor!==b.backgroundColor,
                  label_differs:a.color!==b.color
                    || getComputedStyle(on.querySelector('.tl')).color
                       !==getComputedStyle(off.querySelector('.tl')).color,
                  weight_differs:getComputedStyle(on.querySelector('.tl')).fontWeight
                       !==getComputedStyle(off.querySelector('.tl')).fontWeight,
                  rule:parseFloat(a.borderBottomWidth)>0};}""")
        if tabs_on:
            marks = sum(1 for v in tabs_on.values() if v)
            chk("the selected tab carries at least three marks", marks >= 3, tabs_on)

        # CLICKING THE PROMPT COPIES IT - but never while text is selected.
        clicked = pg.evaluate("""async()=>{
          const pre=document.querySelector('#scroller .card .prompt-text');
          const btn=pre.closest('.card').querySelector('.copy-btn');
          const wait=ms=>new Promise(r=>setTimeout(r,ms));
          btn.className='copy-btn';
          pre.click(); await wait(120);
          const plain=btn.className;
          btn.className='copy-btn';
          const r=document.createRange(); r.selectNodeContents(pre);
          const s=window.getSelection(); s.removeAllRanges(); s.addRange(r);
          pre.click(); await wait(120);
          const withSel=btn.className;
          s.removeAllRanges();
          return {plain:plain, withSel:withSel, cursor:getComputedStyle(pre).cursor};}""")
        chk("clicking the prompt copies it",
            "copied" in clicked["plain"], clicked["plain"])
        chk("a click that ends a text selection does NOT copy",
            "copied" not in clicked["withSel"], clicked["withSel"])

        # EVERY PROMPT BLOCK CARRIES THE ACCENT RULE, in both themes. It used to
        # mark the just-updated prompt; the studio asked for it on all of them on
        # 29 August 2026, so the update state is carried by its badge and its
        # tab dot instead. In dark the shorthand `border` nearly ate it.
        for theme in ("dark", "light"):
            tp = b.new_page(viewport={"width": 1000, "height": 900})
            tp.add_init_script(
                "try{localStorage.setItem('lotp.theme','%s')}catch(e){}" % theme)
            tp.goto(URL); tp.wait_for_timeout(800)
            rules = tp.evaluate("""()=>{const out=[];
              const st=document.createElement('style');
              st.textContent='#scroller .card{content-visibility:visible !important}';
              document.head.appendChild(st); void document.body.offsetHeight;
              // THE PIXEL-KIND TRAP, AGAIN. Under CSS zoom a 2px border reads
              // back as 1.724px (2 / 1.16). Multiply by the zoom before you
              // compare, or the check fails on a border that is correct.
              const z=parseFloat(getComputedStyle(document.getElementById('zoomRoot')).zoom)||1;
              // READ THE TOKEN, NEVER A LITERAL. This check hardcoded the old
              // vermilion and failed the moment the palette changed - a test
              // that pins a VALUE has to be edited on every rebrand, which is
              // the same mistake as naming a token after its value.
              const probe=document.createElement('span');
              probe.style.color='var(--accent)'; document.body.appendChild(probe);
              const ACCENT=getComputedStyle(probe).color; probe.remove();
              document.querySelectorAll('.prompt-text').forEach(p=>{
                const s=getComputedStyle(p);
                if(parseFloat(s.borderLeftWidth)*z<1.9 || s.borderLeftColor!==ACCENT)
                  out.push((parseFloat(s.borderLeftWidth)*z).toFixed(2)+'px '+s.borderLeftColor
                           +' (accent is '+ACCENT+')');});
              st.remove(); return out;}""")
            chk("every prompt carries the accent rule in " + theme, not rules, rules[:3])

            # ONE ORANGE ON SCREEN. Two shades of the accent a step apart read as
            # a mistake, not a system - the studio: "this color is so weird". Every
            # accent painted on a VISIBLE element must be the accent token
            # itself. The darker text step is legal, but only where the accent
            # has to carry small TEXT, and nothing on screen at rest does.
            oranges = tp.evaluate("""()=>{
              const probe=document.createElement('span');
              probe.style.color='var(--accent)'; document.body.appendChild(probe);
              const ACCENT=getComputedStyle(probe).color; probe.remove();
              const st=document.createElement('style');
              st.textContent='#scroller .card{content-visibility:visible !important}';
              document.head.appendChild(st); void document.body.offsetHeight;
              const bad=[];
              const orange=c=>{const m=(c||'').match(/\\d+/g); if(!m) return false;
                const [r,g,b]=m.map(Number); return r>150 && r-g>40 && g>=b;};
              document.querySelectorAll('*').forEach(e=>{
                const r=e.getBoundingClientRect(); if(!r.width||!r.height) return;
                const s=getComputedStyle(e);
                [s.color,s.backgroundColor,s.borderTopColor,s.borderLeftColor,
                 s.borderBottomColor,s.borderRightColor].forEach(c=>{
                  if(orange(c) && c!==ACCENT)
                    bad.push((e.className||e.tagName).trim().split(' ')[0]+' '+c);});});
              st.remove(); return {bad:[...new Set(bad)], accent:ACCENT};}""")
            chk("one orange on screen in " + theme, not oranges["bad"],
                oranges["bad"][:4] or oranges["accent"])

            # THE STATE BADGE IS AN OUTLINE, NOT A FILL. A filled accent
            # rectangle in a stack of ten rows shouts louder than the content.
            # The accent carries a 1px border and a 5px dot; the label is ink.
            badge = tp.evaluate("""()=>{const b=document.querySelector('.badge-new');
              if(!b) return {none:true};
              const s=getComputedStyle(b), d=b.querySelector('.bdot');
              return {fill:s.backgroundColor, border:parseFloat(s.borderTopWidth),
                      dot:!!d, dot_round:d?getComputedStyle(d).borderRadius:'',
                      old_pill:document.querySelectorAll('.now').length};}""")
            if not badge.get("none"):
                chk("the state badge is an outline, not a fill in " + theme,
                    badge["fill"] in ("rgba(0, 0, 0, 0)", "transparent")
                    and badge["border"] > 0, badge)
                chk("the badge carries a round dot in " + theme,
                    badge["dot"] and "50%" in badge["dot_round"], badge)
                chk("the retired CURRENT pill is gone in " + theme,
                    badge["old_pill"] == 0, badge["old_pill"])

            # every accent MARK is round now - a 5px square with a 1.5px radius
            # reads as a third shape nobody chose.
            shapes = tp.evaluate("""()=>{const bad=[];
              document.querySelectorAll('.tbn .tdot,.badge-new .bdot').forEach(e=>{
                if(!getComputedStyle(e).borderRadius.includes('50%'))
                  bad.push(e.className+' '+getComputedStyle(e).borderRadius);});
              return [...new Set(bad)];}""")
            chk("every accent dot is round in " + theme, not shapes, shapes)

            # a class whose only rule was scoped to a deleted parent still
            # RENDERS - at the inherited size. Nothing else catches that.
            sizes = tp.evaluate("""()=>{const bad=[];
              document.querySelectorAll('.card-head span, .card-head button').forEach(e=>{
                if(!e.textContent.trim()) return;   // a .dot has no text; its size is moot
                const px=parseFloat(getComputedStyle(e).fontSize);
                const r=e.getBoundingClientRect();
                if(r.width && px>12) bad.push((e.className||e.tagName)+' '+px+'px');});
              return [...new Set(bad)];}""")
            chk("nothing in a head row inherits the body size in " + theme,
                not sizes, sizes)
            tp.close()

        # A WHEEL OVER THE STRIP PANS IT, and never changes the selection.
        # Selecting on a wheel cannot be smooth: the smallest step is a whole
        # tab, so every notch is a leap. Panning maps input to output 1:1.
        if units >= 2:
            pg.set_viewport_size({"width": 470, "height": 860})
            pg.wait_for_timeout(320)
            pan = pg.evaluate("""()=>{const r=document.getElementById('trail');
              const s=document.getElementById('tabs');
              const sel=()=>[...document.querySelectorAll('.tbn')]
                             .findIndex(t=>t.getAttribute('aria-selected')==='true');
              if(r.scrollWidth-r.clientWidth<3) return {skip:true};
              r.scrollLeft=0; const before=sel();
              s.dispatchEvent(new WheelEvent('wheel',{deltaY:120,bubbles:true,cancelable:true}));
              return {moved:r.scrollLeft, sel_before:before, sel_after:sel()};}""")
            if not pan.get("skip"):
                chk("a wheel pans the rail", pan["moved"] > 0, pan)
                chk("a wheel never changes the selection",
                    pan["sel_before"] == pan["sel_after"], pan)
            # with nothing to pan, the wheel must fall through to the page
            pg.set_viewport_size({"width": 1280, "height": 860})
            pg.wait_for_timeout(300)
            through = pg.evaluate("""()=>{const r=document.getElementById('trail');
              if(r.scrollWidth-r.clientWidth>3) return 'still overflows';
              const e=new WheelEvent('wheel',{deltaY:120,bubbles:true,cancelable:true});
              document.getElementById('tabs').dispatchEvent(e);
              return e.defaultPrevented;}""")
            chk("with nothing to pan the wheel falls through to the page",
                through is False or through == "still overflows", through)

        # ONE fold button, and it toggles
        chk("one fold toggle, not two buttons",
            pg.eval_on_selector_all("#colAll,#openAll", "e=>e.length") == 0
            and pg.eval_on_selector_all("#foldAll", "e=>e.length") == 1)
        before = pg.eval_on_selector_all("details.card[open]", "e=>e.length")
        pg.eval_on_selector("#foldAll", "e=>e.click()"); pg.wait_for_timeout(200)
        folded = pg.eval_on_selector_all("details.card[open]", "e=>e.length")
        pg.eval_on_selector("#foldAll", "e=>e.click()"); pg.wait_for_timeout(200)
        again = pg.eval_on_selector_all("details.card[open]", "e=>e.length")
        chk("the fold toggle closes and opens", folded == 0 and again == before,
            "{} -> {} -> {}".format(before, folded, again))

        for _ in range(3):
            lab = pg.eval_on_selector("#sizeBtn", "e=>e.textContent")
            ov = pg.evaluate("document.documentElement.scrollHeight-window.innerHeight")
            chk("the page does not scroll at " + lab, ov <= 0, ov)
            pg.eval_on_selector("#sizeBtn", "e=>e.click()")
            pg.wait_for_timeout(260)

        for w in (1440, 1280, 1024, 820, 600, 390):
            pg.set_viewport_size({"width": w, "height": 860})
            pg.wait_for_timeout(230)
            ov = pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
            chk("no sideways overflow at {}px".format(w), ov <= 0, ov)

        if units >= 2 and tabs >= 2:
            pg.set_viewport_size({"width": 520, "height": 860})
            pg.wait_for_timeout(360)
            st = pg.evaluate("""()=>{const r=document.getElementById('trail');
              return {over:r.scrollWidth-r.clientWidth, cls:r.className,
                      arrows:document.querySelectorAll('.tnav').length};}""")
            if st["over"] > 2:
                chk("overflow shows the fade", "fadeR" in st["cls"], st)
            chk("no arrow buttons on the strip", st["arrows"] == 0, st["arrows"])

        pg.set_viewport_size({"width": 1280, "height": 860})
        pg.wait_for_timeout(220)
        pg.emulate_media(media="print")
        pg.wait_for_timeout(260)
        chk("print shows every prompt",
            pg.eval_on_selector_all("#scroller > .card, #scroller > .group",
                                    "e=>e.filter(x=>getComputedStyle(x).display!=='none').length") == units, units)
        if units >= 2 and tabs >= 2:
            chk("print hides the tab strip",
                pg.eval_on_selector("#tabs", "e=>getComputedStyle(e).display") == "none")
        chk("print hides the tab strip",
                pg.eval_on_selector("#tabs", "e=>getComputedStyle(e).display") == "none")
        # SPEED IS A GATE, NOT A HOPE. RAIL: process input in under 50ms so the
        # paint lands under 100. These run in single digits, and the check is
        # here so a future change that adds a delay fails instead of shipping.
        speed = pg.evaluate("""async()=>{
          const one=()=>new Promise(r=>requestAnimationFrame(r));
          const t=[],tabs=[...document.querySelectorAll('.tbn')];
          for(let i=0;i<10;i++){const ix=tabs.length>1?1+(i%(tabs.length-1)):0;
        const t0=performance.now(); tabs[ix].click(); t.push(performance.now()-t0);}
          const q=document.getElementById('q'), k=[];
          for(const s of ['b','br','bra','']){
        const t0=performance.now(); q.value=s;
        q.dispatchEvent(new Event('input',{bubbles:true})); k.push(performance.now()-t0);}
          const f=document.getElementById('foldAll'), g=[];
          for(let i=0;i<4;i++){const t0=performance.now(); f.click(); g.push(performance.now()-t0);}
          await one();
          const avg=a=>a.reduce((x,y)=>x+y,0)/a.length;
          const durs=new Set();
          [...document.querySelectorAll('*')].forEach(e=>{
        const d=getComputedStyle(e).transitionDuration;
        if(d&&d!=='0s') d.split(', ').forEach(x=>durs.add(x));});
          return {tab:+avg(t).toFixed(2), key:+avg(k).toFixed(2), fold:+avg(g).toFixed(2),
              durations:[...durs]};}""")
        chk("input work stays under RAIL's 50ms budget",
        speed["tab"] < 50 and speed["key"] < 50 and speed["fold"] < 50,
        "tab {}ms, keystroke {}ms, fold {}ms".format(speed["tab"], speed["key"], speed["fold"]))
        chk("every transition reads the one speed token",
        len(speed["durations"]) <= 1, speed["durations"])

        pg.emulate_media(media="screen")
        b.close()


run()
print("")
if fails:
    print("FAILED: " + ", ".join(fails))
    raise SystemExit(1)
print("ALL PASS")
