# PLUGIN-LOG.md — canonical structure

## Contents
- Per-panel subsection shape (section 3)
- Section 15 entry shape
- Health markers
- Update history row format
- Where the file lives
- Tone

Line 1 is always the machine-readable stamp. Nothing goes above it.

```
<!-- LOG-UPDATED: YYYY-MM-DDTHH:MM+07:00 -->
```

Keep this section order. Don't add top-level sections without asking the studio.

| # | Section | Holds | Update behaviour |
|---|---|---|---|
| 0 | HOW TO USE THIS FILE | Read-first / ask-for-zip protocol | Rarely |
| 1 | WHO THIS IS FOR | the studio, commercial intent, the three product rules | Rarely |
| 2 | THE SUITE AT A GLANCE | Version table, health column | **Every run** |
| 3 | THE PANELS IN DETAIL | One subsection per panel | When a panel is touched |
| 4 | SHARED ARCHITECTURE | Folder layout, shared modules, blank-panel fix | Occasionally |
| 5 | IDs AND PORTS | Extension IDs, debug ports | When confirmed |
| 6 | DESIGN SYSTEM | llloc-UI tokens, shells, drift rule | When the system moves |
| 7 | CEP HARD LIMITS | Settled platform constraints | **Append-mostly, never prune** |
| 8 | CODE RULES | ES3, CSS, load order, packaging traps | Occasionally |
| 9 | RELEASE GATES | Pre-ship checklist | When a gate is added |
| 10 | HOW the studio WORKS | Communication and working preferences | Rarely |
| 11 | OPEN QUESTIONS | Unresolved items | **Every run — add and delete** |
| 12 | UPDATE HISTORY | One row per run, newest first, keep ~20 | **Every run** |
| 13 | KEEPING THIS FILE CURRENT | The update loop, where it runs, the session rule | Rarely |
| 14 | `_CLAUDE/Shared` | Canonical modules, the release gate, the StartOn policy | When the gate moves |
| 15 | MISTAKES AND THE RULES THEY BOUGHT | What went wrong building, why, and the rule | **Every run — append-mostly, never prune** |

## Per-panel subsection shape (section 3)

```
### PANEL — Vx.y · status

**Does:** one paragraph, plain English.

**Works:** confirmed-working features.

**Hard constraint:** platform limits specific to this panel, and the workaround.

**Bugs fixed, root causes:** symptom -> actual cause.

**the studio corrections - do not reintroduce:** explicitly rejected or corrected things.

**Untested / open:** shipped but unverified.
```

## Section 15 entry shape

One per mistake, newest first. Six lines. See `mistakes-pass.md` for what qualifies.

```
### The mistake, in one line

**Happened:** what shipped or was said, and how it surfaced.
**Real cause:** the habit underneath, not the typo on top.
**The rule now:** an instruction a future session can actually follow.
**Would have caught it:** the check, question or test that was missing.
```

Merge entries that share a cause. Never delete one; correct it in place if it is
superseded. If a rule became a gate check, name the check so nobody re-litigates it.

## Health markers

- OK Stable - the studio confirmed working, no open bugs
- ACTIVE - currently being built or debugged
- WARN Shipped, lightly tested - delivered but not proven in real use

(In the file itself these render as the emoji already in use: white-check, hammer, warning.)

## Update history row format

| When (ICT) | What changed |
|---|---|
| 2026-08-05 18:00 | Versions first, then findings. One sentence per item. Name the panel. |

Keep rows short. The detail lives in the sections; this is an index of runs.

## Where the file lives

One copy, on disk (29 Oct 2026):

```
CODE/PR Plugin/_CLAUDE/          (16 Oct 2026: SKILL.md THE FOLDER has the full tree)
└── PLUGIN LOG/
    ├── PLUGIN-LOG.md                         <- the live file
    └── _previous/
        └── PLUGIN-LOG-YYYY-MM-DD-HHMM.md     <- every version it replaced
```

The outgoing file is snapshotted into `_previous/` before it is overwritten.

## Tone

Written for a clever non-expert. Plain English, no jargon without a one-line gloss.
Short sentences. Read under time pressure at the start of a build session - scannable,
not admired.


## 6f cascade (moved from SKILL.md step 6f, 21 Oct 2026)

A changed shape, size or name makes these six pointers wrong. Fix all six now, never next time:

| File | Check |
|---|---|
| Core section 0 | the map: every part, what it holds, who reads it |
| `PLUGIN LOG/STATE.md` | the where-to-look table, lines and cap per file |
| `README.md` | the folder tree and the one-home table |
| `llllloc:project-code` (the code rules) | step 4, the ONE HOME table |
| `CODE/PR Plugin/_CLAUDE/PLUGIN LOG/` and `MISTAKES.md` | every line on how to READ the log |
| this skill and its METHOD file | the folder map, the caps, step 1, the scripts |

## 7 asserts (moved from SKILL.md step 7, 21 Oct 2026)

4. **THE SAME SCRIPT ASSERTS WHAT IT WROTE**, and stops before saving unless ALL hold: core line 1 matches `<!-- LOG-UPDATED: YYYY-MM-DDTHH:MM+07:00 -->`, each part's line 1 is `# PLUGIN LOG · PART NN · TITLE`, the `## N ·` headings of the core and each part match the list from before, every row of one table has one pipe count, the 6c counts moved only as intended, every file is under its cap with no invisible character, and the code rules (`llllloc:project-code`), when touched, are 3,000 words or fewer. Then it reads each file back and compares.
