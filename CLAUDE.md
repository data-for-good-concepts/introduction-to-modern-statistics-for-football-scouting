# CLAUDE.md — Statistics for Football Scouting

A Quarto book: the football-scouting adaptation of *Introduction to Modern Statistics* (IMS, CC BY-SA 4.0). 27 chapters + 6 appendices, one fictional club (Northbridge United FC), real StatsBomb data. Two documents govern all content work — consult the relevant parts **before** editing any chapter:

- `chapter-contract.md` — binding per-chapter rules (professor voice, structure, callout types, licensing footers). The IMS source it cites (`data/ims/<name>.qmd`) is not in this repo — it lives upstream in [openintro/ims](https://github.com/OpenIntroStat/ims); fidelity checks need that checkout separately.
- `translation-map.md` — the design ledger: cast & datasets (§1.1–1.2), notation ledger (§1.4), verified facts and the penalty convention (§1.5), per-chapter specs with AS BUILT blocks (§2), hard rules (§3).

Both predate the file renumbering and refer to chapters by slug (`data-hello.qmd`); files are now `NN-<slug>.qmd` / `A<N>-<slug>.qmd`. Slugs, section anchors, exercise filenames, and figure basenames were **not** renamed.

## The rule that outranks all others

**Every number in this book is baked output from a real R run.** Code blocks are display-only (` ```r ` fences — never executable ` ```{r} `); `#>` lines are pasted from actual runs. Never adjust a number, `#>` line, or downstream statistical claim by hand. To change one:

1. Blocks within a chapter share RNG state — to reproduce block N, run blocks 1..N−1 first, in order. Reference environment (no lockfile yet): R 4.6.1 with dplyr, tidyr, readr, ggplot2, infer, broom, purrr, patchwork, ggridges; run from the repo root so `data/derived/...` paths resolve.
2. Seeds follow `set.seed(100*chapter + k)`; appendices use the 90xx block. Never reuse a seed.
3. If an edit changes any block's state, re-run and re-bake everything downstream in that chapter — and regenerate the affected figures.

## Figures

Pre-rendered PNGs in `figures/`, named `<slug>-<k>.png` (pre-rename slug: `figures/inf-model-slr-13.png` belongs to `24-inf-model-slr.qmd`), inserted after their code block as `![](figures/...){fig-alt="..." width=85%}`. Regenerate by running the chapter's blocks sequentially to the right state, then `ggsave(width = 7, height = 4.5, dpi = 150)`. Before extending a chapter's figures, regenerate an existing one first: byte-identical output proves you reached the right RNG state. (Byte-identity only holds on matching machine and library versions — cross-platform, fall back to diffing the `#>` lines, which are the real ground truth, plus a visual figure check.)

## House style (non-negotiable)

- "statistically discernible" / "discernibility level" — never "significant".
- **The penalty convention** (map §1.5): every comparison affected by penalties or shoot-out kicks is shown pens-in AND pens-out; the *pair* of verdicts is the finding. Never reduce one to a single verdict.
- Notation: each symbol is decomposed symbol-by-symbol exactly once, in its owning chapter per the ledger (map §1.4); recall-only afterwards. Keep `A4-appendix-reference.qmd`'s notation index in sync.
- IMS-inherited anchors (`sec-case-study-stents-strokes`, camelCase strays, ...) are deliberate crossref bridges back to IMS — do not rename or "clean up".
- Real players appear only through their recorded StatsBomb events — never invent quotes, opinions, injuries, or transfers for real people. Invented narrative belongs to the fictional Northbridge cast: Marta Vidal (sporting director), Emil Sørensen (head scout, 48-scout network), Priya Rao (analyst), Jonas Beck (academy director).

## One continuous story

The book is a single narrative, not 27 isolated example sets: storylines build on each other (the one-on-one pricing thread runs from ch 8's model through ch 16's agent pitch to ch 27's capstone; ch 11's dossier48 audit is replicated in ch 17; the GPS load/vendor arc spans chs 21, 24, A6), and headline results recur *verbatim* downstream (ch 11's p = 0.084/0.385 pair, ch 20's T = 4.27/0.37 pair — quoted in later chapters and A4's penalty ledger). Consequences:

- Before editing any example, grep its dataset name and key numbers across the repo (exclude `.claude/` — local session artifacts shadow repo files): recurring results ripple, and a change at the source desynchronizes every quotation.
- When adding, prefer extending an existing storyline over minting an unconnected scenario — map §2 shows what each chapter inherits and hands forward; §1.1 has the cast and org chart.

## Adding new content

Book-original additions beyond the IMS mirror are allowed (precedent: ch 21's panel-review CYUs, ch 25's external-validation subsection, the S1 exercises, appendices A1–A6) — but only if registered: add an AS BUILT note to the chapter's map §2 entry (seeds used *and* skipped, realized numbers, figure indices, the deviation and why) and register any new dataset in map §1.2 before minting a name. Before claiming a seed, grep the whole repo — some spec'd seeds are reserved but unused (e.g. 502 in ch 5); record skipped seeds, never silently reuse them.

## Exercises

Triplets in `exercises/`: `_NN-ex-*` (questions), `_NN-sa-*` (odd worked solutions), `_NN-ea-*` (even bare answers). They flow into the book via `{{< include >}}` — questions at the end of chapter NN, worked solutions into A2, even answers into A3 — so an edit to one file lands everywhere it is included. Even answers stay **bare** deliberately (they double as tutor mastery-check material). IMS exercise numbering is preserved; book-original additions are labeled "S1" outside the numbering.

**Trap:** "programme" in the `_04-*` and `_22-*` exercise files is a *data value* with padding-sensitive baked output — do not correct the spelling.

## Build & verify

- `quarto render --to html` from the repo root must finish with zero warnings and zero unresolved crossrefs. (PDF is untested.) A single-file render reports cross-chapter references as unresolved — an artifact of standalone rendering, not a defect; the full-book render is the real check.
- After any content change: re-run the touched chapter's blocks and diff every `#>` line against the file; verify new anchors resolve.
- `_book/`, `.quarto/`, `*_files/` are gitignored — never commit them.
- `data/derived/*.csv` are the only data files chapters read; they regenerate from the StatsBomb open-data repo via `scripts/derive_statsbomb_tables.py`.

## Licensing

Text CC BY-SA 4.0 (IMS derivative — keep the per-chapter adaptation footers required by the contract). Match data: [StatsBomb open data](https://github.com/statsbomb/open-data), CC BY-NC-SA 4.0 (non-commercial).
