---
name: tool-plasticity
description: "How Claude drives Plasticity 26.1.3 (3D CAD) on his Mac through the community Plasticity MCP (Mesteriis/plasticity-mcp, connector plasticity) for llllloc and the studio. Runs when the user types its name, or when /llllloc:router picks it for one request: any job that reads, models, edits, measures, screenshots, imports or exports a model in Plasticity. Holds universal rules only: the link check, how to start Plasticity with the link, the version lock, read before write, the save rule, test rules and his own rules. A job's look and build notes live in the job folder, never here. Never updates Plasticity, saves over his file, closes his Plasticity or retries a dead link on its own."
---

# llllloc:tool-plasticity

Claude drives his live Plasticity through the community MCP `plasticity` (Mesteriis/plasticity-mcp v0.2.2, MIT). He reviews in the Plasticity window. Units are millimetres and degrees.

This skill holds universal Plasticity knowledge only (22 Oct 2026). A job's look lives in its `*_CLAUDE/3_Art Direction/DesignSystem_<Name>_V<N>.md`. Its build notes live in `*_CLAUDE/7_Motion/PLASTICITY-BUILD.md`. His exact words go to `*_CLAUDE/FEEDBACK-LOG.md`. A rule here changes only when he says so in words.

## TOP RULES
1. Version lock. The tool works with Plasticity 26.1.3 only. Never update Plasticity, never tell him to. A newer version: stop and say the tool must support it first.
2. Check the link first. Plasticity must be started WITH the link (loopback port 9223). Opened from the Dock it has no link, and every call fails.
3. Never close his Plasticity. If it runs without the link, ask him to save (Cmd+S) and quit (Cmd+Q).
4. Read before you write. List windows, connect to the one he means, read status and bodies before any change. Address bodies by the ids just read. After every change, read again: face and edge ids change.
5. No save over his file unless he says so. After a checked change round, tell him to press Cmd+S.
7. A new version never touches the old one (HIS RULES). Duplicate first, edit only the copy, and never hide the old one. Why: he compares versions side by side and goes back to an old one.
6. One dead call, one stop. Send LINK DOWN. Never retry in a burst. After a timeout during a change, run `plasticity_reconcile` before the next change.

## HIS RULES
His own rules for Plasticity go here, one dated line each, in his words made short (core rule 8).
- 22 Oct 2026: every new version starts as a duplicate. `plasticity_duplicate_bodies` on ALL bodies of the old version (shared parts too), group the copies as `<asset>_V<N+1>`, place them one slot right of the newest version, then edit only the copies. Never scale, move, fillet or Boolean a body of the old version.
- 22 Oct 2026: never hide an old version. Every version stays visible, lined up left to right, oldest first, with a gap between boxes. Duplicate with a translation (`translationMm`) so the copy lands in its slot.

## START OF EVERY PLASTICITY TURN
```
- [ ] 1 plasticity tools loaded in one ToolSearch
- [ ] 2 Window found and connected
- [ ] 3 Status and bodies read, target named
- [ ] 4 Job files read
- [ ] 5 New version: old bodies duplicated, only copies edited
```
1. Load the tools in one ToolSearch call (`select:` with a comma list of `mcp__plasticity__*`). The core set is list_windows, connect, status, list_bodies, body_info, current_selection, changes_since, reconcile, screenshot, capture_snapshot, call.
2. `plasticity_list_windows`, then `plasticity_connect` on the window he means. No window: send LINK DOWN. Go back to step 2 only after he says it runs.
3. `plasticity_status` and `plasticity_list_bodies`. Never assume the scene.
4. First Plasticity turn of a job: read the newest DesignSystem file and `PLASTICITY-BUILD.md`. None yet: create it when the first build decision lands.
5. Before the first edit of a new version, duplicate and group (HIS RULES). Check: the old group's bounds are unchanged after the round. Changed: undo that edit and go back to step 5.

## MORE TOOLS
Every other operation (box, curves, extrude, revolve, sweep, loft, boolean, fillet, chamfer, mirror, offset, STEP, STL, SVG export, undo) runs through `plasticity_call`. `catalog` ignores its search word (22 Oct 2026), so call a guessed name with `{}`: the error lists the fields. Known names: `plasticity_move` (`ids`, `deltaMm`), `plasticity_move_to_group` (`bodyIds`, `destinationGroupId`), `plasticity_duplicate_bodies` (`ids`, `translationMm`).

## TRAPS (RB06, 22 Oct 2026)
- Mirror cuts any body that crosses the mirror plane. Undo, and build those bodies directly.
- A Boolean with several tools uses their union: intersect one tool at a time.
- Body bounds of curved faces are loose. Check sizes with `find_edges` bounds.
- A copy lands in its source's group. Moving his view changes the revision: reuse the one the error gives.
- Every change returns the whole scene (about 10,000 words). Plan few, large steps. A big `find_edges` result is saved to a file: pick edges from it with a script.

## LINK DOWN: WHAT TO SEND HIM
1. Save and quit Plasticity if it is open (Cmd+S, Cmd+Q).
2. Open the Terminal app, paste this line, press Return:
`cd "$HOME/Desktop/PERSONAL PROJECT/CODE/plasticity-mcp" && PATH=/opt/homebrew/opt/node@24/bin:$PATH npm run start:plasticity`
3. Tell me when Plasticity is open.
Or he says "start Plasticity for Claude", and Claude runs that line in the background (29 Oct 2026). A Plasticity started from a Claude session closes when the Claude app quits.

## SETUP FACTS (22 Oct 2026)
- Plasticity 26.1.3 at `/Applications/Plasticity.app`, Apple Silicon.
- Tool at `~/Desktop/PERSONAL PROJECT/CODE/plasticity-mcp`, release v0.2.2. Runs on Node 24 at `/opt/homebrew/opt/node@24/bin` (Homebrew `node@24`, beside Node 22, which other tools keep).
- Entry `plasticity` in his Claude app config. A config change needs a Claude app restart. Claude cannot write that file: send him the whole checked file, never a block to paste.
- The link is loopback only: only programs on his Mac can reach it.

## MODELLING ORDER
Block the big forms first, then refine, then merge with booleans, fine detail and fillets last. Fillet and chamfer only after reading fresh edge ids. Check the result with a screenshot and with numbers from `plasticity_body_info`.

## CHECKING THE PICTURE
- `plasticity_screenshot` works only when the Plasticity window is in front. A refusal: ask him to bring Plasticity to the front, then try once more.
- Check by numbers too: bounds and sizes from `plasticity_list_bodies` or `plasticity_body_info`.

## TESTS AND SAFETY
- A test runs only in a new, empty window, or in a window he named. It undoes its own work and saves nothing.
- His Mac's safety guard refuses a Plasticity change approved only by a card tap. Ask him to type the go-ahead in words.
- Export to the job folder only, path from a map row or an `ls` (core rule 5).

## REPLY
Lead with done or not done. Name the body or file to look at. State every default you picked that he did not give. Flag what was not checked. Say whether the file is saved.