---
name: references-design
description: 'Reads a design reference (poster, deck page, layout, UI screenshot, app screen, Figma file, PDF) the way a senior art director would: grid, type scale, hierarchy, color shares, spacing rhythm and the mechanisms that make it read premium, measured with tools before judged. Writes the system in DESIGN.md and DTCG token shape so llllloc:task-design can build on it. Loads with llllloc:references, which holds the shared rules and the dossier. Runs when the user types its name or when /llllloc:router picks it for a dropped design to analyze or learn from, a look to follow in a layout, slides or UI, or ''is this good'' on a design. Never for a photo or a single image with no layout: that is llllloc:references-photo. A live website''s code is llllloc:references-code.'
---

# llllloc:references-design (split from llllloc:references, 17 Oct 2026)

A design is read as a system: a grid, a type scale, a color budget, a spacing unit and a hierarchy that tells the eye where to go. The output is that system, written so a new piece for a new client can be built on it. Shared rules, modes, the dossier and the reply: `llllloc:references`.

## TOP RULES

1. The system first. Scale, grid, ratios and mechanisms transfer from any reference. Headlines, images, logos, illustrations and copy transfer from his and the client's files as given; from an outside reference, when he says so.
2. Never guess a font name. Report the class (grotesque, geometric, humanist, serif, slab, mono), the traits (x-height, stroke contrast, single or double storey a and g, terminal shape) and a closest match with a confidence. A guessed name sends `llllloc:task-design` to the wrong file.
3. Never guess a hex. Hexes come from the quantize step below, with their share. A hex by eye does not exist.
4. A critique is anchored. Each point names the region (top left, the CTA, the second column), the standard it misses, the gap and the fix. "Clean" and "modern" are not findings.

## MEASURE (run first, raw output to `_batches/`)

- **A PDF or a deck:** no OCR. `python3 -c "import pdfplumber;p=pdfplumber.open('<file>').pages[0];print(sorted({(c['fontname'],round(c['size'],1)) for c in p.chars}))"` gives exact font names and sizes; `p.chars` also carries positions and colors. `pip install pdfplumber` (ask first, core rule 1).
- **A screenshot or an export:** `tesseract <file> out --psm 3 tsv` (or `pytesseract.image_to_data`) gives every word's left, top, width and height. Cluster the heights into distinct sizes, sort them, take the ratio between neighbors and name the scale (a modular ratio such as 1.25 or 1.333, or a hand-tuned set like 12 14 16 18 20 24 30 36 48 60 72). Cap height is about 0.7 em: an inference, mark it.
- **Grid and spacing:** a vertical projection profile (ink per column; the valleys are gutters), left edges of all text and image boxes clustered within 3 px (the columns and margins), vertical gaps between blocks clustered (the spacing unit, usually 4 or 8 px, and its multiples). `cv2.HoughLinesP` after Canny for rules and dividers.
- **Palette with share:** `Image.quantize(colors=6, method=Image.Quantize.MEDIANCUT).getcolors()` over the pixel count. Report the 60/30/10 as measured, and the deviation from it.
- **Contrast:** WCAG G17 relative luminance, ratio (L1 + 0.05) / (L2 + 0.05). Under 4.5:1 on body text is a finding.
- **A Figma file:** `Figma:get_metadata` for the outline, `Figma:get_variable_defs` for variables and styles on the selection, `Figma:get_screenshot` for the picture. Read only; never edit the file (core rule 3).
- **A live site:** `llllloc:references-code` owns the tokens (`dembrandt`), this skill reads its screenshots.

## THE PRO READ

| Field | What to write |
|---|---|
| FORMAT | Poster, deck page, landing page, app screen, packaging, book. Size or viewport. |
| GRID | Columns, margins, gutters, fields (a grid is fields, not only columns: Müller-Brockmann), what breaks the grid and why. |
| TYPE | Families by class and traits, weights, the size scale with its ratio, tracking, leading, measure. The pairing logic. |
| HIERARCHY | First, second, third read, and the mechanism of each: size, weight, color, position, space. Weight and color beat size in premium work (Refactoring UI). |
| COLOR | The measured shares with hexes, roles (dominant, secondary, accent), neutrals (pure black or gray is a finding), contrast on the main text. |
| SPACE | The spacing unit and its multiples, density, white space, rhythm between blocks, alignment. |
| SURFACE | Radius, borders, shadows (small and tight is close, large and soft is lifted), fills, grain, gradients, glass. |
| IMAGE | How images and illustration sit in the system: crop, treatment, ratio to type. |
| MOTION HINT | For a UI: what looks like it moves, handed to `llllloc:references-motion`. |
| WHAT READS PREMIUM | The three to five choices, each with the number that proves it. Also what reads generic: system fonts, gray on color, nested cards, purple gradients, a default palette (impeccable's list). |

## THE OUTPUT SHAPE

The dossier (`llllloc:references`) carries the recipe. The system itself is written in two files the job skills read: `DESIGN.md` in the Google design.md shape (frontmatter name, description, colors, typography, rounded, spacing, components; sections Overview, Colors, Typography, Layout, Elevation and Depth, Shapes, Components, Do's and Don'ts) and `tokens.json` in DTCG 2025.10 shape (`$value`, `$type` color, dimension, fontFamily, fontWeight, shadow, typography). They go to the job's `*_CLAUDE/3_Design/` when a job is named, else beside the dossier.

## RESEARCH (with `llllloc:task-research`)

The studio or designer and their stated method, the type families once identified (foundry, licence), the pattern name (editorial grid, Swiss, brutalist, bento, glassmorphism), whether it is durable or a trend, what breaks when people copy it (contrast, readability at size, the system without the craft). Cache: `llllloc/5_Research cache/jobs/design/_TOPICS.md`, then the one topic file.

## HAND-OFF

`llllloc:task-design` builds from DESIGN.md and tokens.json, with `llllloc:impeccable` on every design job. `llllloc:tool-figma` and `llllloc:task-app-builder` take the tokens. A motion hint goes to `llllloc:references-motion`. A critique of a layout runs CRAFT with this read and TASTE with the DESIGN dossier.
