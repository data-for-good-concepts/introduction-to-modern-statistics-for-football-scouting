# Chapter contract — Statistics for Football Scouting

Every chapter is a faithful adaptation of the corresponding IMS chapter
(`data/ims/<name>.qmd`). A chapter is DONE only if it satisfies every rule here.

## Fidelity to IMS

- Mirror the IMS chapter's section structure and heading order. Keep the same
  section anchors (`{#sec-...}`) so cross-references keep working.
- Every term IMS defines must be defined, meaning-identical. Inside definition
  callouts, keep IMS's wording wherever it doesn't reference a non-football
  example (CC BY-SA permits this; loose paraphrase of definitions is a bug).
- Keep IMS terminology: "statistically discernible", "discernibility level"
  (with the footnote that many texts say significant/significance).
- End with the chapter review: summary + alphabetized terms list, mirroring IMS.

## Football-exclusive content

- Every case study, example, aside, and exercise lives in football scouting/
  recruitment or adjacent club operations (academy, injury screening, doping
  control). No banks, no medical trials, no juries — the US-court analogy for
  hypothesis testing becomes a VAR review ($H_0$: the on-field call stands;
  overturn only on clear evidence).
- Real-data examples read from `data/derived/` CSVs (wc2022_shots,
  weuro2025_shots, wc2022_matches, weuro2025_matches) relative to the repo
  root. Synthetic examples must be generated in visible, seeded R code and
  framed as a constructed scouting scenario — never presented as real data.
- Recurring cast, datasets, and terminology come from `book/translation-map.md`.
  Use them; do not invent parallel conventions ad hoc.

## Persona: the statistics professor

- Voice: a professor addressing a scout/analyst student. Rigorous, direct,
  cumulative — explicitly recall earlier chapters ("recall from @sec-...").
- Rigor before intuition: formal definition + notation first, football second.
  The analogy supplements the math, never replaces it.
- Symbol-by-symbol decomposition: the first time ANY symbol appears in the book
  ($P(\cdot)$, $H_0$, $\alpha$, $\hat{p}$, $\sim$, subscripts, $\mid$), name
  each piece in plain words before using the full expression. The notation
  ledger in translation-map.md tracks what earlier chapters already introduced
  — never re-explain, never skip.
- After each non-trivial concept: a "Check your understanding" callout with a
  short question, answer included collapsed or immediately after a rule, like
  IMS's guided practice.

## Math and format

- Quarto markdown. LaTeX with `$...$` / `$$...$$` only.
- Callout mapping from IMS divs:
  `.important` → `::: {.callout-important}` (definitions),
  `.workedexample` → `::: {.callout-note title="Worked example"}`,
  `.guidedpractice` → `::: {.callout-tip title="Check your understanding"}`.
- R code: display-only fenced blocks (```` ```r ````, not executable `{r}`
  cells). Tidyverse: native pipe `|>`, snake_case, `read_csv("data/derived/...")`.
  Show output as `#>` comment lines copied from a real run.
- EVERY number in prose, output, or solution must be reproducible — computed
  from the derived CSVs or from seeded simulation shown in the code. No invented
  statistics presented as real. Verifiers will recompute; mismatches are defects.

## Exercises

- `book/exercises/_NN-ex-<name>.qmd`: every IMS exercise gets a football-
  scouting counterpart testing the same statistical skill, same numbering.
- `book/exercises/_NN-sa-<name>.qmd`: worked solutions following IMS's
  convention (solutions to odd-numbered exercises), showing the computation.

## Attribution

Every chapter ends with the footer: "Adapted from *Introduction to Modern
Statistics* by Çetinkaya-Rundel & Hardin (CC BY-SA 4.0); this adaptation is
likewise CC BY-SA 4.0. Match data: StatsBomb open data."
