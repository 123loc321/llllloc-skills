# A SLIDES FILE — park a slide, the grid and rows, picture rows

Part of `llllloc:tool-figma`. The section numbers are the ones every rule in the skill uses, so "section 5 or 9" in any rule points here.

## 1 (SLIDES). PARK, NEVER HIDE

SLIDES FILE, park, never hide:

```js
const dup = original.clone();       // lands next to its original, same row
original.isSkippedSlide = true;     // stays in the grid, greyed, skip badge
original.visible = true;            // never leave a slide invisible
```

`slide.visible = false` takes a slide OUT OF THE GRID, so the kept version reads as never made. A SLIDE is parked with `isSkippedSlide`. A LAYER is retired with `visible = false`, and that is correct.

- Do not name a parked slide. `slide.name` accepts the write, then Figma overwrites it from the running order. Put meaning in the SLIDE_ROW name.
- Merging is parking two and building one: clone the first, read the second's text off the live node BEFORE parking, park both, build from the clone.
- Park into NAMED rows at the end of the grid, one row per round. Hold back the row that records what he rejected (`LAYOUT OPTIONS`) and say so in the reply.
- End every job with a sweep for `visible !== true` across the deck.

## 5. THE GRID AND ROWS

- Read the grid from the node tree: `figma.currentPage.children.find(c => c.type === 'SLIDE_GRID').children`, then `row.name` and `row.children`. `getSlideGrid()` misses a slide cloned this session and reads stale after `setSlideGrid`.
- `setSlideGrid` needs the WHOLE grid and drops any row left empty, name included. Re-apply every row name by index after a regroup.
- Move a slide between rows with `row.appendChild(slide)`.
- Open a new row with `figma.createSlide(grid.children.length, 0)`, rename `grid.children[i].name`, `appendChild` the real slides, park the seed slide.
- A new slide reads `Frame` for a moment before Figma numbers it. A read taken at once is stale, not wrong forever.
- SLIDE_GRID and SLIDE_ROW are opaque. Only `SLIDE_ROW.name` is settable.

## 9. PICTURES

One auto layout, never nested: a `Pictures` frame, `layoutMode HORIZONTAL`, `layoutWrap 'WRAP'`, itemSpacing 12, counterAxisSpacing 12, width FIXED, height HUG, pictures as direct children at fixed size.

Justify like Flickr does:

1. Read every true aspect ratio with `figma.getImageByHash(hash).getSizeAsync()`.
2. Split into r rows by a balanced cut: walk the running aspect sum and cut where it crosses `k * total / r`. A greedy fill silently returns fewer rows.
3. Row height = `(W - 4 - gap*(n-1)) / sum(aspect ratios in the row)`. The 4px slack stops the wrap pushing the last picture down.
4. Try r = 1 to 5. Keep the largest total that still fits the band.
5. Floor every width and height to a whole pixel. Center the block vertically in the band.

Never crop a reference: `scaleMode: 'FIT'` at the true aspect ratio. Layout slides may use FILL.

