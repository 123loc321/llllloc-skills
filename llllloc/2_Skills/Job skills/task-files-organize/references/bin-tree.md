# The bin tree: one shape in every app (25 Oct 2026)

His words, 25 Oct 2026: the folder structure in the project bin panel across AE, PR, DaVinci and Cavalry, and how items are organized in it, should be similar to each other.
Apps: Premiere (Project panel bins), After Effects (Project panel folders), Cavalry (Assets panel groups), DaVinci Resolve (Media Pool bins under `Master`), FilmCraft (Project panel bins, added 26 Oct 2026, his words: same rules as AE, DaVinci, PR and Cavalry).
Source of the tree: DEFTREE in his SORT panel (`CODE/PR Plugin/SORT/SORT-V<newest>-INSTALLER/SORT/index.html`). SORT builds it in Premiere. Claude builds the same tree in the other apps.

## The tree, top to bottom

```
**_EXPORT
  <Video>/                    current comp, sequence or timeline: <Video>_<APP>_V<n>
    OLD VERSIONS/<version>/   what he saw before: <Video>_<APP>_V<n> (+ its precomps in AE)
0_SEQUENCE / LINKED, NESTED, *Sequence_Unsure
1_VISUAL ASSET / **_Ref, *Video_Unsure, *Image_Unsure   (+ his own sub-bins, mirrored from disk)
2_GRAPHIC ASSET / *Graphic_Unsure
3_SOUND ASSET / MUSIC, SFX, VO, *Sound_Unsure
4_RENDERS
5_OTHER / Solid, *Other_Unsure
```

- `<Video>` is the deliverable's name, the same as its `**_MOTION` folder when it has one: `L01_top`, `Act 1`, `SCENE-2_COUNTRY-CARDS`.
- `<APP>` tags: `AE`, `CAV`, `PR`, `DVR` (DaVinci Resolve), `FC` (FilmCraft). Each app counts its own versions. `_V<n>` stays last: SORT learns export prefixes from `^(.+?_)V\d`.
- `OLD VERSIONS` sits last inside its `<Video>` bin, one bin per version inside it.
- SORT also makes a top-level `**_EXPORT/OLD VERSIONS` in Premiere. Leave it. Archives go in the per-video `OLD VERSIONS`.

## Where each item goes

| Item | Premiere | After Effects | Cavalry | DaVinci | FilmCraft | Bin |
|---|---|---|---|---|---|---|
| The deliverable | sequence | main comp | main comp | timeline | sequence | `**_EXPORT/<Video>/` |
| Inside it | nested sequence | precomp | precomp, 3D comp | compound clip, Fusion clip | nested sequence | `0_SEQUENCE/NESTED` |
| From another app | AE comp (Dynamic Link) | PR sequence | - | - | imported XML, AAF or OTIO sequence | `0_SEQUENCE/LINKED` |
| Video, stills | footage | footage | image, video asset | clip | movie, still | `1_VISUAL ASSET` (refs in `**_Ref`) |
| Logos, vectors, alpha PNG, `.ai` layers | graphic | graphic (`.ai` folder by file name) | SVG, image | still | still | `2_GRAPHIC ASSET` |
| Music, effects, voice | audio | audio | sound asset | audio clip | audio | `3_SOUND ASSET/MUSIC`, `SFX`, `VO` |
| A final render brought back in | clip | footage | asset | clip | movie | `4_RENDERS` |
| Solids, mattes, adjustment layers, generators | item | solid | - | generator, matte | colour matte, adjustment layer | `5_OTHER/Solid` |
| No clear home | | | | | | the family's `*_Unsure` |

## Versions, every app

1. The first call of a change round archives what he saw. The copy goes to `**_EXPORT/<Video>/OLD VERSIONS/<version>/`, named `<Video>_<APP>_V<n>`.
2. The working one takes the next number: `V1` becomes `V1.1`, then `V1.2`. Edit only the working one.
3. How each app makes the copy: AE and Cavalry, their skill's VERSIONS section (AE copies the whole precomp tree). Premiere, `create_sequence_checkpoint` or `duplicate_sequence`, then rename and move. DaVinci, duplicate the timeline. FilmCraft, `fc_sort.py archive` (`llllloc:tool-filmcraft` VERSIONS).
4. Check: each `<Video>` bin holds one working item, and every older one sits in `OLD VERSIONS/<version>/`.

## Rules

- Never delete an item or a bin. A loose item is filed, not removed.
- Keep his own sub-bins (example: `MAPS`). Skip app-only bins: SORT's Premiere-only `*SORT CLEANUP`, `ADJUST SOURCES`, `Premiere Composer Files`. DaVinci: Smart Bins, Power Bins and the MCP's own `Archive` bin stay where the app puts them.
- Labels: AE current comps red, folders green. Premiere keeps SORT's labels, and items Claude places are pink (`llllloc:tool-premiere-pro`). Cavalry's API sets no label. DaVinci clip colors: leave them.
- SORT CHECK, the last step of every turn that added, renamed or moved an item, in any app: build any missing bin, file every loose item, then list the top level. Anything at the top besides the seven bins (plus the app-only bins above), or a deliverable loose in `**_EXPORT`, is a fail: file it and list again. The reply says `Bins sorted`.
