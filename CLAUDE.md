# CLAUDE.md — Statistics for Football Scouting

A Quarto book: the football-scouting adaptation of *Introduction to Modern Statistics* (IMS, CC BY-SA 4.0). 27 chapters + 6 appendices, one fictional club (Northbridge United FC), real StatsBomb data. Two documents govern all content work — consult the relevant parts **before** editing any chapter:

- `chapter-contract.md` — binding per-chapter rules (voice, structure, callout types, licensing footers).
- `translation-map.md` — the design ledger: cast & datasets (§1.1–1.2), notation ledger (§1.4), verified facts and the penalty convention (§1.5), per-chapter specs with AS BUILT blocks (§2), hard rules (§3).

Both documents predate the file renumbering and refer to chapters by slug (`data-hello.qmd`); files are now `NN-<slug>.qmd` and `A<N>-<slug>.qmd`. Slugs, section anchors, exercise filenames, and figure basenames were **not** renamed.

## The rule that outranks all others

**Every number in this book is baked output from a real R run.** Code blocks are display-only (` ```r ` fences — never executable ` ```{r} `); `#>` lines are pasted from actual runs. Never adjust a number, `#>` line, or downstream statistical claim by hand. To change one:

1. Blocks within a chapter share RNG state — to reproduce block N, run blocks 1..N−1 first, in order (R 4.6.1; packages: dplyr, tidyr, readr, ggplot2, infer, broom, purrr, patchwork, ggridges; run from the repo root so `data/derived/...` paths resolve).
2. Seeds follow `set.seed(100*chapter + k)`; appendices use the 90xx block. Never reuse a seed within a chapter.
3. If an edit changes any block's state, re-run and re-bake everything downstream in that chapter — and regenerate the affected figures.

## Figures

Pre-rendered PNGs in `figures/`, named `<slug>-<k>.png` (pre-rename slug, e.g. `figures/inf-model-slr-13.png` for `24-inf-model-slr.qmd`), inserted after their code block as `![](figures/...){fig-alt="..." width=85%}`. Regenerate by running the chapter's blocks sequentially to the right state, then `ggsave(width = 7, height = 4.5, dpi = 150)`. Before extending a chapter's figures, regenerate an existing one and confirm it is byte-identical — that proves you reached the right RNG state.

## House style (non-negotiable)

- "statistically discernible" / "discernibility level" — never "significant".
- **The penalty convention** (map §1.5): every comparison affected by penalties or shoot-out kicks is shown pens-in AND pens-out; the *pair* of verdicts is the finding. Never "simplify" one of these to a single verdict.
- Notation: each symbol is decomposed symbol-by-symbol exactly once, in its owning chapter per the ledger (map §1.4); recall-only afterwards. Keep `A4-appendix-reference.qmd`'s notation index in sync.
- IMS-inherited anchors (`sec-case-study-stents-strokes`, camelCase strays, ...) are deliberate crossref bridges back to IMS — do not rename or "clean up".
- Cast: Marta Vidal (sporting director), Emil Sørensen (head scout, 48-scout network), Priya Rao (analyst), Jonas Beck (academy director). Dataset names are minted once and registered in map §1.2 — check it before naming anything new.

## Exercises

Triplets in `exercises/`: `_NN-ex-*` (questions), `_NN-sa-*` (odd worked solutions → A2), `_NN-ea-*` (even bare answers → A3). Even answers stay **bare** deliberately — they double as tutor mastery-check material. IMS exercise numbering is preserved; book-original additions are labeled "S1" outside the numbering.

**Trap:** "programme" in the `_04-*` and `_22-*` exercise files is a *data value* with padding-sensitive baked output — do not correct the spelling.

## Adding new content

Book-original additions beyond the IMS mirror are allowed — precedent: ch 21's panel-review CYUs, ch 25's external-validation subsection, the S1 exercises, appendices A1–A6 — but only if registered. When you add content: record an AS BUILT note in the chapter's `translation-map.md` §2 entry (seeds used *and* skipped, realized numbers, figure indices added, the deviation and why); register any new dataset in map §1.2 before minting a name. Before claiming a seed, grep the whole repo — some spec'd seeds were reserved but never used (e.g. 502 in ch 5), and skipped seeds must be recorded, not silently reused.

## Environment caveats

- There is no lockfile yet; R 4.6.1 plus the package list above is the reference environment. The byte-identical figure check assumes the same machine and library versions — on a different platform, fall back to diffing the `#>` lines (the real ground truth) and comparing figures visually.
- The IMS source text the contract cites (`data/ims/<name>.qmd`) is **not** part of this repository — it lives in the upstream [openintro/ims](https://github.com/OpenIntroStat/ims) repo (CC BY-SA). Fidelity checks against IMS need that checkout separately.

## Build & verify

- `quarto render --to html` from the repo root; it must finish with zero warnings and zero unresolved crossrefs. (PDF is untested.)
- `_book/`, `.quarto/`, `*_files/` are gitignored — never commit them.
- After any content change: re-run the touched chapter's blocks and diff every `#>` line against the file; render at least the touched chapter; verify new anchors resolve.
- `data/derived/*.csv` are the only files chapters read; they regenerate from the StatsBomb open-data repo via `scripts/derive_statsbomb_tables.py`.

## Licensing

Text CC BY-SA 4.0 (IMS derivative — keep the per-chapter adaptation footers required by the contract). Match data: [StatsBomb open data](https://github.com/statsbomb/open-data), CC BY-NC-SA 4.0 (non-commercial).
