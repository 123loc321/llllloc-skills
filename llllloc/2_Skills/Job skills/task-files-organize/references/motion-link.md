# MOTION link and moving an old film

Moved from SKILL.md, THE MOTION RULE, on 21 Oct 2026, word for word.

- THE LINK, until the app reads `#`: MOTION cannot read a media path with `#`, and the drive is `CREATIVE #1`. So the media lives only in the project, and MOTION reads it through a link at `~/Movies/MOTION/media/<FILM>` that points to `**_MOTION/<FILM>/media`. Every `src` in the film uses the link path. Method and test: `llllloc:task-motion` Reference N, paths.
- Moving an old film: copy its media, check every size, move the old media folder to a `_DELETE` folder beside it, make the link, then open the film in MOTION and take one snapshot. Missing picture: put the old folder back and say so.
