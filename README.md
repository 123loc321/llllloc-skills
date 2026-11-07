# llllloc skills

The skills of **llllloc**, the Claude workflow of Loc's video, motion and design studio, shared with friends. One Claude Code plugin named `llllloc`: a router, about 90 skills, the core rule and the hooks that keep Claude on it. Every skill loads as `llllloc:<name>`.

This repo is a read-only copy. It is refreshed once a week, and Claude Code picks up the new version by itself.

## Set it up (best way: the full shared copy)

The skills work best inside the llllloc folder, which holds the rules, the empty memory and the maps they use.

1. Get the shared `Claude` folder from the Google Drive link Loc sent you. Put it on your Desktop.
2. In the Claude desktop app, open the Code tab and start a new session in that folder.
3. Type `set me up`. Claude runs the setup. It turns on this plugin from this repo, with auto-update on.
4. Start a new session in the same folder. Done.

## Only the plugin

In a Claude Code session, type these two lines one after the other:

```
/plugin marketplace add 123loc321/llllloc-skills
/plugin install llllloc@llllloc-skills
```

Then open `/plugin`, go to Marketplaces, pick `llllloc-skills` and turn on auto-update.
No GitHub SSH key on your Mac? Add `"CLAUDE_CODE_PLUGIN_PREFER_HTTPS": "1"` under `"env"` in `~/.claude/settings.json` first. The setup in the full copy does this for you.

## Good to know

- Your own edits to the skills inside your folder do not load while this plugin is on. To use your own versions, run the setup with `--local`: `python3 -I "llllloc/1_Core rule/setup_mac.py" --local`. Auto-update then stops.
- Some skills say "commit and push to GitHub". That is Loc's own repo. You cannot push here, and you do not need to.
- Docs: [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).
