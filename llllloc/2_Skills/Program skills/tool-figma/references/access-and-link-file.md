# ACCESS AND THE FIGMA LINK FILE

Part of `llllloc:tool-figma`. "Section 0 or 12" in any rule of the skill points here.

## 0. ACCESS

The Figma MCP acts as ONE Figma account, not always the one his desktop app uses. When a file refuses, run `whoami` first. The refusal "you don't have edit access to this file" points at the share box, and the share box is not the cause: Figma needs a file permission AND an editor seat in the team that holds the file, so "Anyone can edit" changes nothing for the MCP. The fix: in Claude, Customize, Connectors, disconnect Figma, connect again, sign in with the email that owns the file. If the sign-in page flashes past, sign out of Figma in the browser first.

## 12. THE FIGMA LINK FILE

A link file replaces the `.fig` save, so one click opens the file in his Figma desktop app (23 Sep 2026).

Every project with a Figma file keeps one link file per Figma file in its `***_DESIGN FILES` folder. Write it the first time a job touches that file. Skip it when it already exists with the same URL.

1. Resolve the folder, never type it: `ls -d "<full path from the map row>"/*/*DESIGN\ FILES`. Drive not mounted or empty listing: stop and tell him.
2. Name: `<Figma file name>_FIGMA.webloc`. Content: an Apple plist with one key, `URL`, set to the bare file address from the LINKS row of `llllloc/3_Project maps/Project map_Creatives.md`. Write it with Bash.
3. A click opens the Figma desktop app only when Figma Preferences > "Open links in desktop app" is on. Else it opens the browser. No `figma://` scheme is documented.
4. A link file is not a backup. A `.fig` backup is his own step (File > Save Local Copy…). Never run it through computer use unasked.

