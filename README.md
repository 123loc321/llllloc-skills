# llllloc skills

The skills of **llllloc**, the Claude workflow of Loc's video, motion and design studio, shared with friends. One Claude Code plugin named `llllloc`: a router, about 90 skills, the core rule and the hooks that keep Claude on it. Every skill loads as `llllloc:<name>`.

This repo is a read-only copy. It is refreshed once a week, and Claude Code picks up the new version by itself.

## Set it up (best way: make it your own)

The skills work best inside the llllloc folder, which holds the rules, an empty memory and the maps they use.

1. Get the shared `Claude` folder from the Google Drive link Loc sent you. Put it on your Desktop.
2. In the Claude desktop app, open the Code tab and start a new session in that folder.
3. Type `set me up`. Claude asks your name and a name for your own system, renames everything to it, and sets up your own GitHub repo, a Google Drive backup, the weekly tasks and your apps.
4. Every Tuesday Claude lists what Loc changed here. You pick what to take into your own system.

## Only the plugin, Loc's names, his updates by themselves

In a Claude Code session, type these two lines one after the other:

```
/plugin marketplace add https://github.com/123loc321/llllloc-skills.git
/plugin install llllloc@llllloc-skills
```

Then open `/plugin`, go to Marketplaces, pick `llllloc-skills` and turn on auto-update.
You need no GitHub account: the repo is public.

## Good to know

- With this route you cannot change the skills: they come from this repo. To change them, make the system your own (above).
- Some skills say "commit and push to GitHub". That is Loc's own repo. You cannot push here, and you do not need to.
- Docs: [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).
