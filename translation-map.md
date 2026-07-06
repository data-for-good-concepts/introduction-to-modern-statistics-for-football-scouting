# Translation map — Statistics for Football Scouting

SPEC for all chapter writers. Read together with `book/chapter-contract.md`.
Book chapter N = Nth file in the IMS order listed in §2. Cite as `@sec-...`
using the IMS anchors. All real numbers below were computed from
`data/derived/*.csv` on 2026-07-05; recompute in your chapter's own R code —
never copy from here into prose without a matching code block.

## 1. GLOBAL CONVENTIONS

### 1.1 The cast

Real world (observational data only — never claim causation from it):

- **2022 Men's World Cup** (`wc2022_*`): 32 teams, 64 matches, **1,494 shots,
  195 goals (13.05%)**. The book's workhorse dataset.
- **2025 Women's Euro** (`weuro2025_*`): 16 teams, 31 matches, **913 shots,
  123 goals (13.47%)**. Second tournament: used for replication, contrast
  ("does the pattern hold in a different competition?"), and external
  validation/holdout.
- Recurring real anchors (use these rather than a new team each time):
  **Argentina** (champion, deep run = many shots), **Morocco** (surprise
  semifinalist, low-block/counter profile), **England Women's** (WEuro
  champion). When a single player is needed, pick a high-volume shooter from
  the data (verify shot counts in code) and stay with them within a chapter.

Fictional world (ALL synthetic / experimental scenarios live here, so the book
feels like one club):

- **Northbridge United FC** — a fictional mid-table club, always the employer
  of the reader ("you, the analyst").
- **Marta Vidal**, sporting director: commissions questions, makes the
  sign/pass call, worries about the transfer budget.
- **Emil Sørensen**, head of scouting: runs the network of **48 regional
  scouts** (48 on purpose — chapter 11's flagship experiment uses the whole
  network, mirroring IMS's 48 bank supervisors).
- **Priya Rao**, lead data analyst: the professor's stand-in inside the story;
  designs the club's randomized interventions.
- **Jonas Beck**, academy director: hosts all training-intervention RCTs
  (finishing drills, load management, recovery protocols).
- **Agnes Whitmore**, Northbridge's founding chief scout (historical, deceased):
  one-off figure for period quotes/anecdotes (introduced ch. 4 ex. 8 as the
  Nightingale analogue). Do NOT mint further historical club figures; reuse her.

ORG CHART (canonical — writers must not contradict it): Jonas Beck runs
Northbridge's academy — one academy, his. The club additionally maintains a
set of **partner academies** (deliberately unnumbered; do NOT fix a count).
Youth intake runs through the club's **regional intake assessment** centres
(ch 22's North/Central/South). Any study too large for one club's staff or
player pool is hosted at federation/consortium level (multi-academy RCTs,
registration cohorts) and framed that way — never as Northbridge-internal.

Every randomized experiment in the book is a *club-internal randomizable
intervention* at Northbridge (report-format A/B tests, dossier audits,
academy drill trials, GPS-vendor comparisons, survey experiments). Never
present a synthetic scenario as real; always show the seeded R that builds it.

### 1.2 Running datasets

Real CSVs, read as `read_csv("data/derived/<name>.csv")`:

- `wc2022_shots.csv`, `weuro2025_shots.csv` — one row per shot. Columns:
  `competition, match_id, match_date, stage, team, opponent, player, position,
  period, minute, second, play_pattern, shot_type, body_part, technique,
  first_time, under_pressure, one_on_one, statsbomb_xg, outcome, goal`.
  `goal` is logical; `outcome` levels include Goal/Saved/Blocked/Off T/Wayward.
- `wc2022_matches.csv` (64 rows), `weuro2025_matches.csv` (31 rows):
  `competition, match_id, match_date, stage, home_team, away_team, home_score,
  away_score, result`.

Canonical derived objects (define with identical code in the first chapter
that uses them; later chapters rebuild with the same code, same name):

- `shots50` — `set.seed(101); slice_sample(wc2022_shots, n = 50)`. The book's
  `loan50`. Introduced ch. 1, reused ch. 5.
- `team_match` — per (match_id, team) aggregate of `wc2022_shots`: `n_shots`,
  `total_xg`, `goals`, plus shares (`prop_under_pressure`, `prop_set_piece`).
  **127 rows** (one team-match has zero shots — mention it). Introduced ch. 5
  (weighted means), main stage in chs. 7 and 24.
- `team_profile` — per-team shot-mix shares from `wc2022_shots` (32 rows):
  `% headers, % first_time, % under_pressure, % from corners, % open play`,
  conversion, mean xG. Introduced ch. 1 (scatterplots), reused chs. 7, 22.

Canonical synthetic datasets (seed = `set.seed(100 * chapter_number + k)`;
regenerate verbatim when reused):

- `drill_trial` (ch. 1) — multi-academy RCT of a new high-intensity finishing
  program vs standard training; 30-day and season-end assessments; the
  program *hurts* season-end conversion (the stent surprise). Mirror stent30/
  stent365 arithmetic (45/224 vs 28/227 at season end).
- `dossier48` (ch. 11, flagship) — 48 Northbridge scouts, one identical
  prospect dossier each, only the player's listed nationality randomized
  (24 "domestic" / 24 "foreign"); 35 shortlist recommendations total: 21 vs
  14, diff = 0.292. Numbers mirror IMS `sex_discrimination` exactly.
- `budget150` (ch. 11) — 150 scouts, recommendation form with vs without the
  line "or keep the €15M for the winter window"; mirror `opportunity_cost`
  (diff 0.20; empirical permutation p = 0.008, 8/1000 with seed 1102 — IMS
  reports 0.006, but quote the seeded run's value).
- `audit_study` (ch. 9) — the scaled-up dossier audit: many synthetic
  profiles, several randomized cues (nationality label, video clip attached,
  agent-submitted flag), outcome = shortlisted. The book's `resume` data.
- `gps_pair25` (ch. 21) — 25 academy players wearing two GPS-vest vendors
  simultaneously; the book's tire-tread data.
- `template_ab` (ch. 20) / `template_abc` (ch. 22) — scout-report template
  randomizations; the book's exam-version data.
- `screening_trial` (ch. 17) — large-n video-analytics vs live-scouting
  screening RCT (mammogram analogue); `recovery_trial` (ch. 17) — rare-injury
  recovery-protocol RCT (fish-oil analogue).

### 1.3 Terminology mapping (IMS generic → this book)

| IMS | This book |
|---|---|
| observational unit / case | a shot; sometimes a team-match, match, player, or scout-evaluation — say which |
| population | all shots in a tournament; all prospects in a market; all evaluations the network could make |
| sample | the shots/matches a scout actually saw; a seeded `slice_sample()` |
| treatment / control | new drill / standard training; augmented report / standard report |
| placebo, blinding | sham drill with equal contact time; identically formatted reports of unknown source |
| success (binary outcome) | goal scored; prospect shortlisted; benchmark met |
| anecdotal evidence | "I watched him twice and he was electric" — the highlight-reel fallacy |
| convenience sample | agent-submitted clips; only matches near the scout's home |
| non-response bias | scouts who don't file reports; only enthusiastic raters reply |
| confounding variable | play pattern behind body-part effects; pressure behind distance effects |
| US court analogy | VAR review: H0 = on-field call stands; overturn only on clear evidence |
| Type I / Type II error | signing a dud / passing on a gem |
| data snooping | eyeballing all 32 squads, then testing the two extremes |

House vocabulary: "statistically discernible" / "discernibility level" (per
contract); "conversion" = proportion of shots scored; "chance quality" =
`statsbomb_xg`; "the club" = Northbridge United.

### 1.4 Notation ledger

A symbol is decomposed piece-by-piece ONLY in the chapter listed; afterwards
use it freely with at most a "recall @sec-...".

| First in ch. | Symbols introduced there |
|---|---|
| 1 | proportion as fraction/percent; explanatory → response arrow; association ≠ causation; $\approx$ |
| 5 | $\bar{x}$, $x_i$, $n$, $\mu$, $s^2$, $s$, $\sigma^2$, $\sigma$, $\Sigma$, $Q_1$, $Q_3$, IQR, 1.5×IQR rule, $\log_{10}$, $\pm$ |
| 7 | $b_0, b_1$, $\beta_0, \beta_1$, $e_i$, $\hat{y}$, $r$, $R^2$, SST, SSE, SSR, $b_1 = (s_y/s_x)r$, $|\cdot|$ (absolute value) |
| 8 | $x_1,\dots,x_k$, $k$, $R^2_{adj}$, $n-k-1$, level-indicator subscripts |
| 9 | $Y_i$, $p_i$, $\hat{p}_i$, $\text{logit}(p_i)=\log_e\frac{p_i}{1-p_i}$, $e^{\beta_0+\cdots}$ back-transform, AIC |
| 11 | $H_0$, $H_A$, $\hat{p}$ with group subscripts, p-value, $\alpha$ |
| 12 | $\hat{p}_{boot}$, bootstrap percentile interval |
| 13 | $N(\mu,\sigma)$, $Z$, $z^\star$ (1.96), SE, margin of error, point estimate ± 1.96×SE, $p_0$ (informal) |
| 14 | two-sided $\neq$ in $H_A$; $p_T, p_C$; power (named) |
| 16 | $p_0$ (formal), $SE(\hat{p})=\sqrt{p(1-p)/n}$, $\hat{p}_{sim}$, $z^\star$ at other levels (1.65, 2.58), $P(\cdot)$ probability-of notation |
| 17 | $p_1-p_2$, $\hat{p}_1-\hat{p}_2$, two-sample SE, $\hat{p}_{pool}$ (compounds like $\hat{p}_{T,boot}$ = recall-composition, no new decomposition) |
| 18 | $X^2$, expected counts formula, $df=(R-1)(C-1)$ |
| 19 | $T$, $t^\star_{df}$, $df=n-1$, $SE=s/\sqrt{n}$, $SE_{BS}$, $\bar{x}_{bs}$ |
| 20 | $\mu_1-\mu_2$, $\bar{x}_1-\bar{x}_2$, $\sqrt{s_1^2/n_1+s_2^2/n_2}$, $df=\min(n_1-1,n_2-1)$ |
| 21 | $\mu_{diff}$, $\bar{x}_{diff}$, $s_{diff}$, $n_{diff}$ |
| 22 | $F$, MSG, MSE, SSG, SSE/SST (ANOVA), $df_G=k-1$, $df_E=n-k$ |
| 24 | $SE_{b_i}$, $t^\star_{n-2}$, $b_i \pm t^\star SE_{b_i}$, LINE conditions, $\varepsilon$ population error term |
| 25 | conditional $H_0: \beta_i=0$ given others; $\hat{y}_{cv,i}$; CV SSE; $k$ folds; $E[\cdot]$ expectation operator |
| 26 | logistic residual $e_i = Y_i - \hat{p}_i$; Wald test (named), $Z = b_i/SE(b_i)$ (recall/specificity named in prose, not Terms) |

### 1.5 Verified data facts (recompute in-chapter before quoting)

**PENALTY CONVENTION (user-approved 2026-07-05).** Penalties (incl. period-5
shootout kicks) sit on one side of most headline splits and can manufacture or
mask effects. The book TEACHES this rather than hiding it: every affected
comparison is shown pens-in AND pens-out, with the contrast as the lesson.
Verified open-play checkpoints (wc2022 `shot_type == "Open Play"`):
- pressure conv 0.1008 (238) vs 0.1101 (1,144): diff −0.9pp, permutation
  p = 0.385 (seed 1107) — NOT discernible. The all-shots gap (0.1008 vs
  0.1361, seed-1103 permutation p = 0.084 — fails at α = 0.05 but would be
  declared discernible at α = 0.10) is penalty-driven; ch 11 teaches the pair
  (borderline pens-in vs nowhere-close pens-out). AS BUILT: ch 11
  §sec-chp11-pens-out; ex 7(e) reruns weuro open play (33/325 = 0.1015 vs
  62/526 = 0.1179, seed 1108, p ≈ 0.20 vs ≈ 0.02 all-shots).
- weuro open-play first_time 0.1234 vs 0.1050 — NO sign flip; the all-shots
  "reversal" (0.1234 vs 0.1405) is a penalty artifact. Ch 14's peeking-analyst
  anecdote uses the artifact itself ("he tested garbage"), not a real flip.
- open-play foot conv 0.1065 < headers 0.1111 — the all-shots header "deficit"
  (0.111 vs 0.133) is mostly the 64 all-footed pens at 0.672.
- Argentina: 15 goals in periods 1–4 (23 incl. shootout); tournament open-play
  totals differ from the 1,494/195 all-shots totals — flag whichever is used.
Chapters 15–27 writers: any spec bullet quoting an all-shots number affected
by penalties must either filter (and say so) or flag "includes penalties/
shootout kicks" — recompute both variants before choosing what to teach.

- wc2022: 1,494 shots, 195 goals, conversion 0.1305; mean xG 0.1259.
  **under_pressure: n=238, conv 0.1008 vs n=1,256, conv 0.1361** (flagship,
  diff −0.0353); mean xG 0.0961 vs 0.1315.
- wc2022 one_on_one: n=85, conv 0.200, mean xG 0.2455 (non-1v1 mean xG ≈ 0.119).
- wc2022 first_time: conv 0.1517 vs 0.1209 (first-time HIGHER).
  **weuro2025 first_time reverses: 0.1234 vs 0.1405** — never assume the sign
  transfers across competitions; this reversal is itself teachable.
- weuro2025: 913 shots, 123 goals (0.1347), mean xG 0.1350; under_pressure
  n=325 conv 0.1015 vs n=588 conv 0.1531; one_on_one n=29, conv 0.172, xG 0.356.
- Headers: wc conv 0.111 / xG 0.1055 (n=252) vs foot 0.133 / 0.127; weuro
  0.113 vs 0.140. Corner-pattern shots: wc 17/223 = 0.076; weuro 16/160 = 0.100.
- `shot_type` includes **Penalty** (wc 64, weuro 51) with xG ≈ 0.78 — a spike
  in the right tail of every xG histogram. Either keep it and teach it, or
  filter `shot_type == "Open Play"` and say so.
- `team_match` (wc): goals ≈ 0.190 + 0.909 × total_xg, r = 0.691, n = 127.
  Shots per team-match: mean 11.76, SD 5.55, range 2–31 (≈ normal enough for
  ch. 13 percentile work).
- r(xG, minute) among open-play shots ≈ +0.03 (wc) / −0.03 (weuro): a genuine
  near-zero relationship — reserved for "CI contains 0" lessons (chs. 24, 27).

## 2. PER-CHAPTER SPECS

Format per bullet: IMS case → translation | data | expected behavior |
continuity. "Exercises:" line gives translation guidance for the exercise set.

### Ch 1 — data-hello.qmd (20 ex.)

- Stent study → `drill_trial`: academies randomize players to a new
  high-intensity finishing program vs standard training; assessed at 30 days
  and season end | synthetic, seed 101 | mirror 45/224 vs 28/227: the program
  HARMS season-end conversion — same "intervention backfires" shock | dataset
  returns in chs. 13, 16.
- loan50 → `shots50` (50 seeded WC2022 shots): data-frame anatomy,
  variable-type walkthrough (`statsbomb_xg` continuous, `minute` discrete,
  `play_pattern` nominal, `outcome` ordinal-ish, logicals) with a
  variable-description table | real | reused ch. 5.
- county scatterplots → `team_profile`: % headers vs conversion (negative,
  r ≈ −0.29; % headers vs mean xG, r ≈ −0.32, also works), total xG vs goals
  (clearly positive, r ≈ 0.93); highlight Morocco the way IMS highlights
  Chattahoochee County | real | verify directions in code. Do NOT use
  % under pressure vs conversion here: the shot-level pressure effect washes
  out at team level (r ≈ −0.04, a flat cloud).
- Energy-drink illustration → caffeine gum before extra time, placebo gum,
  response = sprint distance | hypothetical prose only.
- Coin flips → striker with true 10% conversion takes 100 shots; rarely
  exactly 10 goals | synthetic `rbinom` | seeds intuition for chs. 11, 16.
- Exercises: swap each context 1:1 (marketing → fan-survey, medicine →
  injury-screening); keep every design classification question.

### Ch 2 — data-design.qmd (30 ex.)

- MLB salaries sampling → estimate mean xG/shot at WC2022 by SRS of 120 shots
  vs stratified by team (teams differ hugely in volume/quality) | real | no
  headline number; show both estimators in code.
- Malaria villages → Emil can only send scouts to 8 of 64 matches: cluster
  (all shots in sampled matches) vs multistage (subsample within) | real
  wc2022_shots + matches | travel-cost framing.
- Heart-disease drug trial → Jonas Beck's finishing-drill RCT with a **sham
  drill** (equal contact time) as placebo, graders blinded → double-blind |
  hypothetical prose | foreshadows ch. 1's `drill_trial` results.
- Stents-unblindable aside → GPS-vest load-management protocol: randomized but
  players know their arm; no placebo possible | prose.
- Nurses' Health Study → prospective matchday report logging vs retrospective
  video re-tagging of historical event data | prose + real data mention.
- Sunscreen confounding → headers convert less (0.111 vs 0.133 wc) but
  play_pattern confounds: headers come from crosses/corners at bad angles |
  real | verify proportions; this confounder returns in chs. 8, 27.
- Duke sampling bias → highlight-reel = convenience sample; agent-submitted
  clips = selection/non-response bias; contrast with random sample of all
  logged shots | real + prose.
- Exercises: keep all design-vocabulary items; population = "all shots in the
  tournament" or "all prospects in a market" consistently.

### Ch 3 — data-applications.qmd (case study, 0 ex.)

- paralympic_1500 EDA → first look at `wc2022_shots`: rows/columns, data
  dictionary, tricky `minute:second` time variable, bar plots of team and
  play_pattern counts, xG summaries by position and shot_type | real.
- Division comparison → WC2022 vs WEuro2025 as two "divisions": mean/min/max
  xG by competition × play_pattern | real | plant the two-tournament contrast
  used throughout.
- Simpson's paradox → synthetic scout-rating paradox: club-wide, ratings fall
  with prospect age, but rise within each scout's assigned age cohort (scout
  assignment is the lurking variable) | synthetic, seed 301 | do NOT promise a
  reversal in the real shot data unless you verify one.
- Scope-of-inference wrap-up → shots data is observational; contrast with a
  Northbridge randomizable design | prose.

### Ch 4 — explore-categorical.qmd (10 ex.)

- Homeownership × application_type → `body_part` (Right/Left/Head, drop
  `Other` n=13, say so) × `outcome` collapsed to goal/no-goal: contingency
  table, row vs column proportions | real wc2022 | head conv 0.111 < foot 0.133.
- All bar-plot variants (stacked/standardized/dodged/mosaic) → position group
  (FW/MF/DF, derive from `position` strings — define the mapping once here) ×
  `shot_type` | real weuro2025.
- Loan-grade pie lesson → `play_pattern` (9 levels) as pie vs sorted bar:
  too-many-slices | real wc2022.
- Spam × format → `under_pressure` × `goal`: which conditioning direction
  helps a scout predict? 0.1008 vs 0.1361 | real wc2022 | **explicitly
  foreshadow ch. 11's flagship test on this exact split**.
- County income across groups → `statsbomb_xg` by goal/no-goal: side-by-side
  box, ridge, faceted histograms; facet competition × position for the
  3-variable figure | real, both tournaments | xG right-skewed like income.
- Exercises: binary×binary and 3×2 tables from first_time, one_on_one,
  technique; keep conditional-proportion direction questions.

### Ch 5 — explore-numerical.qmd (26 ex.)

- loan50 rates → `shots50` xG: dot plot, histogram, mean vs median (right
  skew), SD; robustness by moving the single highest-xG shot (a penalty or
  1v1) — median/IQR stable, mean/SD not | real | recompute all summary stats.
- county weighted mean → tournament mean xG/shot via pooling all shots vs
  averaging `team_match` team means (unequal matches by stage) | real |
  introduces `team_match`.
- county log transform → per-player shot counts, heavily right-skewed, log10 |
  real weuro2025.
- Intensity map → replaced by a constructed pitch-zone heat grid (no x/y in
  CSVs): synthetic zone coordinates, framed as a constructed scenario | seed 501.
- Asthma trial → randomized report-template trial: 500 new-template vs 1,000
  standard evaluations; raw error counts (200 vs 300) mislead vs rates
  (0.4 vs 0.3) | synthetic seed 502.
- Emilio's truck → scout travel: 11,000 km / 625 hours = 17.6 km/h workload
  standardization | prose arithmetic.
- Fabricated distributions → simulated academy-open-day heights (players +
  coaches = bimodal); three sprint-speed shapes with equal mean/SD; 68/95
  rule | synthetic seed 503.
- Exercises: xG, minute, shots-per-match distributions; keep every
  "which is robust" and shape-identification item.

### Ch 6 — explore-applications.qmd (case study, 0 ex.)

- Pie vs bar → Argentina's shots by play_pattern: 3D pie vs sorted bar | real.
- Duke hires time series → shots per matchday across each tournament,
  annotated where knockouts begin | real, both tournaments.
- Brexit ordinal survey → synthetic Northbridge panel: 48 scouts rate a
  prospect (Excellent/Good/Average/Poor/Don't know) by scouting region;
  ordering, stacking, faceting, cividis | synthetic seed 601.
- Color-to-highlight → xG by body part with the club's target profile
  highlighted vs rainbow default | real wc2022.

### Ch 7 — model-slr.qmd (32 ex.)

- Target stock perfect line → tournament accreditation: total cost = flat
  admin fee + per-scout fee × n scouts; perfect fit | prose arithmetic.
- Possum head~length → `team_match`: goals ~ total_xg. Verified: ŷ = 0.190 +
  0.909·xG, r = 0.691, n = 127 | real | residual = finishing over/
  under-performance — a scouting concept in its own right; reused chs. 24, 27.
- Elmhurst aid~income → synthetic veteran market: asking price vs age for
  players 28+, negative slope, r ≈ −0.5 engineered; extrapolation absurdity of
  a negative fee at 40 | synthetic seed 701 | slope CI revisited ch. 24.
  AS BUILT (ch. 7, n=50, ages 28–35): r = −0.534, ŷ = 56.4 − 1.44·age,
  ŷ(40) = −1.2 €m — reuse these exact values in ch. 24.
- Crop-yield correlation ranking → six `team_profile` scatterplots of shot-mix
  shares ranked by r | real | compute the six r's; don't guess order.
  AS BUILT: team_profile has no set-piece share; the six panels pair the five
  canonical shares (headers, first_time, pressure, corner, open_play); r's:
  −0.17, 0.03, 0.31, −0.33, −0.11, 0.50.
- bdims unit invariance → the same shot clock in two units: r(xG,
  minute + second/60) = r(xG, 60·minute + second) = 0.238 exactly | real
  wc2022 | note r(xG, `minute` alone) = 0.2383 differs slightly — `second`
  adds information, so it is not a pure unit change.
- Mario Kart indicator → xG ~ one_on_one: intercept ≈ 0.119 (ordinary shots),
  slope ≈ +0.127 (1v1 premium) | real wc2022 | indicator inference in ch. 27.
- Simulated panels (outliers/leverage/nonlinearity) → seeded scouting
  scatters: "super-sub" influential point; curved age-value cloud | synthetic
  seed 702 | must stay constructed to control geometry.
- Exercises: keep interpretation-of-slope/intercept phrasing exactly; football
  units (xG, goals, € m, km).

### Ch 8 — model-mlr.qmd (16 ex.)

- Loans MLR → xG ~ body_part + technique + under_pressure + one_on_one +
  play_pattern + minute on wc2022; reference level = Right Foot, stated |
  real | interpret each coefficient "holding others constant".
- Bankruptcy-coefficient shrink → show one_on_one (or first_time) coefficient
  shrinking once play_pattern and body_part enter — the ch. 2 header
  confounder, now in model form | real | remember first_time's sign flips
  between competitions.
- Stepwise selection → backward + forward by $R^2_{adj}$ on combined
  tournaments; expect a weak predictor (e.g. `period`) to drop, mirroring
  issue_month | real | report actual adj-R² path from your run.
- Exercises: reuse the fitted wc2022 model; prediction + reference-level
  questions.

### Ch 9 — model-logistic.qmd (10 ex.)

- Resume callback audit → `audit_study`: Northbridge dossier audit at scale —
  synthetic profiles with randomized cues (nationality label, video attached,
  agent flag); outcome = shortlisted; multi-predictor logistic + AIC backward
  elimination; back-transform to probabilities | synthetic seed 901 |
  discrimination theme preserved; small-scale version is ch. 11's `dossier48`.
- Honors warm-up → one-predictor model inside the audit: `video_attached`
  first, then full model | synthetic.
- Observational counterpoint (flagged NOT causal) → goal ~ body_part +
  technique + under_pressure + one_on_one + first_time on wc2022 | real |
  full logistic inference deferred to ch. 26.
- Sex-imbalance thought experiment → 20% goalkeepers / 80% outfield academy;
  10% of coaches on each side undervalue the other role; minority absorbs
  8% vs 2% biased reviews; ratio $(1-p)/p$ | prose arithmetic.
- Exercises: audit-study variants; keep logit-interpretation items.

### Ch 10 — model-applications.qmd (case study, 0 ex.)

- Duke Forest houses → full workflow on wc2022: EDA per predictor → SLR
  (xG ~ one_on_one) → MLR → backward elimination by $R^2_{adj}$ → residual
  plots | real.
- California-house extrapolation → fit on weuro2025, predict a wc2022 shot
  (or vice versa): out-of-scope prediction, large residual; competitions
  differ | real, both | quantify the miss in code.

### Ch 11 — foundations-randomization.qmd (8 ex.) — FLAGSHIP

- Sex discrimination (opening randomized experiment) → `dossier48`: all 48
  Northbridge scouts receive an identical prospect dossier; only the listed
  nationality is randomized (24 domestic / 24 foreign); 21/24 vs 14/24
  shortlisted, diff = 0.292; card-shuffle narrative then 100 permutations,
  p ≈ 0.02 | synthetic seed 1101 | numbers mirror IMS exactly so the pedagogy
  transfers 1:1.
- Opportunity cost → `budget150`: 150 scouts, form with/without "keep the
  €15M for the winter window"; diff 0.20, 1,000 permutations, p = 0.008
  (8/1000 with seed 1102; IMS's run gave 0.006) | synthetic seed 1102 |
  revisited ch. 13 with the normal model.
- Observational randomization test (MANDATED) → wc2022 under-pressure split:
  conv **0.1008 (238 shots) vs 0.1361 (1,256)**, diff −0.0353; permute
  `under_pressure` labels; state clearly this tests association, not
  causation (defenders press good chances less, etc.) | real.
- Classroom left/right thought experiment → odd- vs even-minute shots'
  first_time proportion: null-true-by-construction chance variation | real
  weuro2025.
- Court analogy → VAR review (contract-mandated): H0 = on-field call stands;
  "check complete" ≠ call proven correct | prose.
- Exercises: permutation logic on club experiments; one exercise re-runs the
  under-pressure test at WEuro2025 (0.1015 vs 0.1531 — stronger).

### Ch 12 — foundations-bootstrapping.qmd (8 ex.)

- Medical consultant → a set-piece consultant claims his methods beat the
  tournament: bootstrap percentile CI for one team's conversion (choose a
  team with ~60 shots and ABOVE-average conversion so the claim's direction
  is coherent — England works: 13/63 = 0.2063 vs baseline 0.1305; verify in
  code); CI overlaps baseline; observational, so no causal claim either way |
  real wc2022 | returns chs. 13, 14, 16.
- Tappers and listeners → coaches vastly overrate corners: shots from
  From-Corner possessions score 17/223 = 0.076 at wc2022; bootstrap CI vs
  the inflated intuition | real | expectation-vs-reality framing preserved.
- Marble bag → seven trialists (3 "sign", 4 "pass"); resample with
  replacement; infinite-estimated-population diagrams redrawn with trialists |
  synthetic seed 1201.
- Exercises: single-proportion bootstraps on play_pattern/body_part subsets;
  keep the "what is the parameter?" drills.

### Ch 13 — foundations-mathematical.qmd (16 ex.)

- Opportunity cost, normal model → `budget150` revisited: Z = 0.20/SE ≈ 2.56,
  p ≈ 0.005, CI (0.047, 0.353); overlay normal on ch. 11's permutation null |
  synthetic (same seed/code).
- Medical consultant, normal fails → ch. 12's team-conversion case (England,
  13/63): success-failure fails (n·p0 = 63 × 0.1305 ≈ 8.2 < 10) and skew
  breaks the normal approximation; simulation disagrees with Z | real.
- Stents CI → `drill_trial` season-end harm: 95% CI for the risk difference
  excludes 0 — the program discernibly hurt | synthetic (ch. 1 seed/code).
- SAT/ACT Z-scores → which prospect stands out more: sprint time vs vertical
  jump on different scales | synthetic seed 1301; plus real variant using
  per-player shots-per-match across the two tournaments.
- Male heights → team shots-per-match ≈ N(11.76, 5.55) from `team_match`:
  percentile and qnorm-style questions | real | check normality visually first.
- 25 CIs simulation → wc2022 shots as the population (p = 0.1305); 25 seeded
  samples of n = 300, count misses (~1 expected) | real + seed 1302.
- Four-nulls recap → the book's own four: dossier48, budget150, team
  conversion, corner proportion; overlay normal curves; note the skewed one |
  mixed, reuse earlier code.
- Exercises: Z/percentile drills in football units; CI-interpretation items
  verbatim in structure.

### Ch 14 — foundations-errors.qmd (10 ex.)

- Court analogy → sign/pass decision table: Type I = signing a dud, Type II =
  passing on a gem; tightening one loosens the other | prose; one-line VAR
  callback to ch. 11.
- CPR trial → academy drill-program RCT sized to be inconclusive: diff 0.13,
  two-sided permutation p ≈ 0.26, fail to reject | synthetic seed 1401 |
  distinct from ch. 1's `drill_trial` (which rejected).
- Medical consultant revisited → ch. 12 team-conversion case (England,
  13/63), one-sided p in the claimed "beats the tournament" direction
  (≈ 0.06 by exact binomial; verify) doubled to two-sided | real.
- Type-I doubling → simulate an analyst choosing the test direction AFTER
  seeing each season's first_time split; 5% + 5% = 10% | synthetic seed 1402 |
  the real wc/weuro first_time sign flip (0.152>0.121 vs 0.123<0.141) is the
  perfect motivating anecdote.
- Callbacks → could `dossier48`'s rejection have been a Type I error? | prose.
- Exercises: error-type identification in scouting decisions; α trade-off items.

### Ch 15 — foundations-applications.qmd (case study, 0 ex.)

- Malaria vaccine (14/6) → 20 scouts: 14 randomized to xG-augmented reports,
  6 to standard; outcome = ranking matches expert panel; observed diff 0.643;
  ~2/100 permutations as extreme | synthetic seed 1501.
- Notecard simulation → 11 "hit" / 9 "miss" cards shuffled into 14/6 by hand,
  then `infer` with 100 permutations | same synthetic data.
- Vocabulary recap (data/population/sampling/randomization/bootstrap
  distributions) → illustrate each with wc2022 conversion | real.
- AS BUILT: dataset `report20`; card counts are 11 "miss" / 9 "hit" (the
  bullet above transposed them — IMS's malaria table is 11 infection /
  9 no-infection, and the diff 0.643 = 6/6 − 5/14 is in BAD-outcome rates:
  augmented 9 hit / 5 miss vs standard 0 hit / 6 miss). Seed 1501: hand
  shuffle = 8/6 vs 1/5 (diff 0.405, doubles as infer's first permutation);
  100 permutations give 1/100 ≥ 0.643 (IMS's seed-19 run gave 2/100) —
  chapter quotes the seeded 1/100, p = 0.01. Recap frames both conversions
  (all-shots 195/1494 = 0.1305 flagged, open-play 150/1382 = 0.1085);
  shots50 (seed 101) p̂ = 7/50 = 0.14; sampling dist seed 1502 (mean 0.131,
  SD 0.0487); bootstrap seed 1503 (mean 0.141, SD 0.0498); randomization =
  ch 11's open-play pressure test rerun, seed 1504, p = 0.42 (vs 0.385 on
  seed 1107 — Monte Carlo gap taught explicitly, same verdict). Tutorials/
  labs repurposed per ch 3: 4-lesson weuro walkthrough (seeds 1505–1508;
  open-play frame 95/851 = 0.1116; first_time open-play two-sided
  permutation p = 2 × 0.233 = 0.466; n = 100 bootstrap CI (0.04, 0.16)
  captures 0.1116) + corner-pattern lab (both frames). Ends with a Chapter
  review {#sec-chp15-review} per ch 10's nothing-new precedent (Summary +
  "Terms revisited" table {#tbl-terms-chp-15}): the book's applications
  convention outranks IMS's review-less ending (verifier adjudication).

### Ch 16 — inference-one-prop.qmd (30 ex.)

- Medical consultant, parametric bootstrap → an agent claims her striker
  finishes 1v1s above tournament level: test a small one_on_one sample
  against p0 = 0.20 (= 17/85 wc2022 1v1 conversion); success-failure fails
  (n·p0 < 10), so simulate with `rbinom` | real baseline + small subset |
  continuity with chs. 12–14 consultant thread.
- Payday survey → Northbridge network survey, n = 826 synthetic responses,
  TWO separate questions mirroring IMS's two items: (a) 70% support a
  mandatory xG field → 95% CI example; (b) a second question observes
  p̂ = 0.51, majority test vs p0 = 0.50 → Z = (0.51 − 0.50)/0.017 = 0.59,
  fail to reject | synthetic seed 1601 | mirror IMS numbers; do not apply the
  majority test to the 70% item.
- Marijuana-legalization voter poll (SE practice) → large-n real CI:
  proportion of wc2022 shots under pressure: 238/1494 = 0.159; CI, then test
  a pundit's "one in five" claim (p0 = 0.20) | real.
- Stents CI revisit → `drill_trial` risk difference at 90% and 99% | synthetic.
- 10,000-sim null → `rbinom(10000, 62, p0)` penalty-box conversion null,
  shade tail at an observed team's count | seed 1602, observed from real data.
- Exercises: keep every SE-formula substitution drill (p0 for tests, p̂ for
  CIs); football claims throughout.
- AS BUILT: the garbled `rbinom(10000, 62, p0)` bullet was MERGED into the
  flagship consultant case as `rbinom(10000, 6, 0.20)` (seed 1602; Morocco's
  real 3-of-6 open-play 1v1 record; no separate 62-shot example exists — 62
  was IMS's n). The "small one_on_one sample" is the TEAM's 6 shots, not an
  individual's (max 4 1v1s per player league-wide); the attribution gap is
  taught explicitly. Baselines shown both frames: 17/85 = 0.200 (6 pens all
  MISSED + 2 direct corners) vs open-play 17/77 = 0.221; taught frame p0 =
  0.20 (lenient bar, failure a fortiori; open-play p = 0.126 vs 0.099).
  drill_trial 99% CI (−0.0115, 0.1665) CROSSES zero (unlike IMS's stent
  analogue) — taught as the confidence-level trade-off; 90% (0.0206, 0.1344).
  Survey seed 1601: Z quoted rounded 0.59/0.278 (IMS mirror) then
  full-precision 0.56/0.289.

### Ch 17 — inference-two-props.qmd (22 ex.)

- CPR trial → ~90-player academy finishing intervention: randomization test
  (fail to reject at α = 0.05 mirror: p ≈ 0.24), bootstrap percentile + SE
  CIs, then Z-based 90% CI spanning 0 | synthetic seed 1701.
- Two-population marbles → 7 headers vs 9 foot shots, tiny two-sample
  bootstrap | synthetic seed 1702.
- 25 CIs coverage → wc2022 as population; true diff = first_time conversion
  gap 0.1517 − 0.1209 = 0.0309 (unrounded arithmetic; the 4-dp roundings
  subtract to 0.0308); 25 seeded resampled studies | real + seed 1703.
- Fish oil (rare outcome, big n) → `recovery_trial`: cryotherapy vs standard,
  soft-tissue injury rare; CI barely excludes 0 | synthetic seed 1704.
- Mammogram → `screening_trial`: video-analytics vs live-scouting screening
  of thousands of prospects; pro-contract-within-5-years diff ≈ 0, Z ≈ −0.17;
  policy discussion = cost and false flags, mirroring over-diagnosis |
  synthetic seed 1705.
- Exercises: pooled-vs-unpooled SE drills; at least one real-data exercise on
  under_pressure conversion gap per competition.
- AS BUILT: CPR analogue = `feedback90` (video-feedback finishing trial,
  45/45, 16 vs 10 met benchmark, diff 0.1333; distinct from ch 14's
  benchmark90 and says so). Seed-1701 100-rep randomization: 10/100 right
  tail → two-sided p = 0.20 (spec's ≈0.24 mirror; same fail-to-reject verdict;
  seeded run quoted). Seed-1701 1,000-rep bootstrap: percentile 90% CI
  (−0.022, 0.300), SE 0.0974, ±2·SE 95% CI (−0.061, 0.328); Z-based 90% CI
  (−0.023, 0.289), formula SE 0.0945. Marbles = `headers7` (3/7 on target) vs
  `foot9` (5/9), seed 1702, boot SE 0.250. 25 CIs: all-shots frame, flagged,
  with the open-play contrast (0.152 vs 0.086) recomputed in code; n = 500
  per study (n = 300 fails success-failure in some samples); seed 1703 →
  2 misses of 25, both entirely above the true 0.0309. `recovery_trial`
  145/12,933 vs 200/12,938, 95% CI (−0.0070, −0.0015); seed 1704 = rbinom SE
  cross-check (0.00144). `screening_trial` 500/44,925 vs 505/44,910, hand
  Z = −0.17 (exact −0.164), p 0.865 (exact 0.870); seed 1705 = rbinom null
  cross-check (SE 0.00069, p 0.86). Exercise seeds 1706–1713; ex 1/3 =
  under-pressure gap wc/weuro, open-play frame with all-shots flag (wc
  two-sided p ≈ 0.78; weuro 95% CIs straddle 0); ex 10/12 pair is the
  explicit unpooled-CI vs pooled-test SE drill.

### Ch 18 — inference-tables.qmd (16 ex.)

- iPod disclosure → 3 randomized question prompts to scouts holding a known
  injury concern ("Tell me about him" / "No weaknesses, right?" / "What are
  his weaknesses?"); disclose vs withhold; X² ≈ 40, df = 2, permutation +
  chi-squared | synthetic seed 1801 | mirror IMS table margins.
- Diabetes 3×2 → Jonas Beck's 3-arm academy intervention (standard drills /
  VR decision training / recovery program) × benchmark met/missed; expected
  counts by hand | synthetic seed 1802.
- Single null shuffle → real observational table: play_pattern collapsed to
  open play / set piece / counter × goal on wc2022; one seeded permutation
  shown, then the full test; association-only language | real.
- Exercises: 2×3 and 3×2 football tables; keep df and expected-count
  computation items.
- AS BUILT: `disclose219` mirrors IMS ask margins (73/73/73; 61/158), X² =
  40.13, df 2, perm p = 0/1000 (seed 1801); `benchmark699` mirrors diabetes2
  (232/233/234; 319/380; seed 1802 row shuffle only). Real test drops
  play_pattern "Other" (64 pens w/ 43 goals + 4 open-play-tagged, 0 goals):
  open play 96/862, set piece 46/508, counter 10/56; X² = 4.63, perm
  p = 0.107 (shuffle seed 1803, test seed 1804), pchisq p = 0.099 — FAILS to
  reject at α = 0.05; pens-in 4-row contrast X² = 162. Ex 3/5/7/9: wc2022
  open-play FW/MF/DF × body part, n = 1,369, X² = 65.28, df 4, p ≈ 0 (seeds
  1805–1807). Ex 4/6/8/10: weuro pattern3 × goal, n = 859 (excl. 54 = 51 pens
  + 3 tagged Other), X² = 3.43, p ≈ 0.17 — counters LOWEST, direction flips
  vs wc2022 (seeds 1808–1810).

### Ch 19 — inference-one-mean.qmd (22 ex.)

- Awesome Auto (n = 5) → a scout logs 5 shots by one target player (subset of
  a high-volume shooter, seeded pick); bootstrap percentile + SE CIs for mean
  xG; also bootstrap CI for the SD | real subset + seed 1901.
  AS BUILT: player = Messi (34 shots: 24 open play, 7 pens, 3 FKs — sampled
  from open play only, pens-out frame stated per convention); seed 1901 →
  5 shots, x̄ = 0.1305, s = 0.2004; bootstrap seed 1902 (1,000 reps):
  90% percentile CI (0.0361, 0.3051), 95% (0.0333, 0.3103), SE_BS = 0.0798,
  SE interval (−0.0291, 0.2901) — the negative bound is taught as the
  symmetric-formula failure; 90% CI for σ (0.0090, 0.2490). Full 24-shot
  open-play mean 0.0797 used as closing reality check.
- Risso's dolphins → one team's full-campaign mean xG/shot (n ≈ 20–30; pick
  and verify): t-CI; "is chance quality worryingly low?" | real wc2022.
  AS BUILT: Australia — n = 26, ALL open play (no pens/FKs, frame check
  shown), x̄ = 0.0607, s = 0.0578, SE = 0.0113, t*_25 = 2.06, 95% CI
  (0.0374, 0.0840): entirely below the open-play benchmark 0.0983 →
  "worryingly low" confirmed.
- FDA croaker → weuro2025 one_on_one shots: n = 29, mean xG 0.356; 90% t-CI
  from summary stats only | real.
  AS BUILT: n = 29, x̄ = 0.356, s = 0.300, min 0.029, max 0.784; SE = 0.0557,
  t*_28 = 1.70, 90% CI (0.261, 0.451). PENALTY FLAG taught: 8 of the 29
  logged 1v1s are penalties at 0.7835 (open-play 1v1s: n = 21, mean 0.193) —
  a spike the memo's min/max outlier check cannot reveal; the CI describes
  the blended frame, stated explicitly.
- Cherry Blossom → weuro2025 under-pressure shots' mean xG (0.0914, n = 325,
  s = 0.1018) tested against the wc2022 all-shot benchmark 0.1259: T ≈ −6.1,
  reject —
  pressured chances are discernibly worse than the benchmark | real, verify |
  sample-vs-known-benchmark design preserved; observational caveat.
  AS BUILT (penalty convention — the spec's "reject" does NOT survive the
  frame-consistent rerun): sample verified 0.0914 / 0.1018 / n = 325, all
  325 open play; pens-in benchmark 0.1259 gives T = −6.11, p ≈ 2.9e−9 (kept
  as the worked mirror), but that benchmark holds the 64 pens at 0.7835;
  open-play benchmark 0.0983 gives T = −1.22, p = 0.223 — not discernible.
  Ch 19 teaches the pair with the flip as the lesson (mirrors ch 11
  §sec-chp11-pens-out): ~4/5 of the headline "deficit" was the benchmark's
  penalties, not pressured shooting.
- Exercises: keep t vs z decision items and df drills; football sensor/combine
  metrics allowed for variety (synthetic, seeded).
- AS BUILT (exercise-file scout-review fixes, 2026-07-06 — regenerated numbers
  only): ex 15 "Working backwards, I" re-unitized — a stated 95% CI of
  (18.985, 21.015) km/h for a winger's average TOP sprint speed was a jog;
  now (33.4925, 34.5075) km/h, n = 36 / df = 35 / skill unchanged; back-solved
  answers x̄ = 34.0, ME = 0.5075, s = 1.5 km/h with t*₃₅ = 2.03 (exact
  qt(0.975, 35) = 2.0301 reproduces the stated endpoints to 4 dp); odd →
  solution 15 updated to match. Ex 22 creatine kinase rescaled to
  elite-footballer physiology — congested-winter sample now x̄ = 851.59 U/L,
  s = 258.52 U/L (n = 52, drawn the morning after a matchday) vs full-rest
  off-season benchmark 220 U/L (was 124.32 / 37.74 vs 35, IMS's blood-lead
  values quoted as U/L); T = 17.62, df = 51, one-sided p ≈ 1.2e-23 — same
  reject verdict, same skill; even-numbered, no solution entry exists.

### Ch 20 — inference-two-means.qmd (20 ex.)

- Exam A/B → `template_ab`: scout-report templates randomly assigned;
  mean accuracy diff ≈ 3 points, permutation p ≈ 0.2 > α = 0.01, fail to
  reject | synthetic seed 2001.
  AS BUILT: 113 randomized report assignments (58 A / 55 B, mirroring IMS
  classdata's group sizes), accuracy 0–100 vs a blinded expert panel;
  seed 2001 → A 76.34 (SD 12.08), B 73.11 (14.42), x̄_A − x̄_B = 3.24;
  9-report toy shuffle shown in code (73 vs 70.8 → shuffled 74.75 vs 69.4);
  1,000 permutations (seed 2001): 104/1000 in the right tail, p = 2 × 0.104
  = 0.208 — quoted as 0.21 > α = 0.01, fail to reject.
- Awesome Auto two franchises → two agencies each value 5 comparable wingers;
  toy two-sample bootstrap visualization | synthetic seed 2002.
  AS BUILT (regenerated 2026-07-06 per panel review — the original seed-2002
  run priced wingers at €15.0–25.7M, too rich for the €15M-budget world;
  design params halved to `rnorm(5, 10.5, 2)` / `rnorm(5, 8, 1.5)`): two
  partner agencies value 5 shortlist wingers each (seed 2002): means 12.84
  vs 7.52 €m, diff 5.32; 1,000 two-bag bootstrap differences (explicit
  `replicate()` resampling per group, per ch 17's marbles): SE 1.14, range
  1.3–8.4; figures/inference-two-means-4.png regenerated to match.
- ESC sheep → randomized finishing-drill program vs standard, change scores;
  bootstrap CI then t-CI (df = min rule) excluding 0 — causal improvement |
  synthetic seed 2003.
  AS BUILT: `drill18` (seed 2003) — 18 academy forwards, 9 drill / 9
  standard, change = after − before assessment points; drill +3.52 (4.95)
  vs standard −4.27 (2.56), diff 7.79 (mirrors stem_cell's 7.83); seed-2003
  infer bootstrap: SE_BS 1.74, 90% percentile CI (4.93, 10.60), 90% SE CI
  (4.93, 10.65), no bootstrapped diff ≤ 0; formula SE 1.86, df = min(8,8)
  = 8, t*_8 = 2.31, 95% t-CI (3.49, 12.09) — excludes 0, causal.
- births14 smoking → mean xG under pressure vs not at wc2022: 0.0961 vs
  0.1315, groups 238/1256 (imbalance mirrors smokers); T large, reject;
  observational — repeat the ch. 11 causality caveat | real.
  AS BUILT (penalty convention — the verdict FLIPS and the flip is the
  lesson, mirroring ch 19's Cherry-Blossom pair): all-shots 0.1315
  (n = 1,256, s = 0.1961) vs 0.0961 (n = 238, s = 0.0949), diff 0.0354,
  SE 0.0083, T = 4.27, df = 237, p = 2.8e-5 → reject (kept as the worked
  IMS mirror); but all 64 pens (0.7835) + 48 unpressured dead balls sit in
  the unpressured group and the pressured group is pure open play; open-play
  rerun: unpressured 0.0988 (n = 1,144, s = 0.1304; the spec's "≈ 0.096"
  verified as 0.0988) vs 0.0961 — diff 0.0027, T = 0.37, p = 0.71, fail to
  reject. Association-only caveat repeated in both frames; Agnes Whitmore
  1968 notebook quote fills IMS's tobacco-quote slot.
- Exercises: at least one weuro replication (0.0914 vs 0.1591); keep SE and
  df computation drills.
  AS BUILT: seeds 2004–2010. The weuro pressure pair is the recurring
  diamonds-slot dataset (ex 3/5/9/11), both frames per convention: all
  shots 0.1591 (588, s 0.2231) vs 0.0914 (325, s 0.1018), diff 0.0677 —
  perm 0/1000 (seed 2004), T = 6.27, df = 324, p ≈ 1e-9, 95% CI (0.046,
  0.089), boot SE 0.0111 (seed 2007); open play 0.1011 (526, s 0.1186) vs
  0.0914 — diff 0.0097, perm two-sided p = 0.222 (111/1000, seed 2005),
  T = 1.27, p = 0.205, CI (−0.005, 0.025): verdict flips, taught across
  ex 3/5/9/11 (weuro pens 51 @ 0.7835 + 11 FKs all unpressured). Lizards
  slot (ex 4/6) = wc2022 open-play first-time xG 0.1347 (468, s 0.1558) vs
  0.0797 (914, s 0.1009), diff 0.0549, perm 0/1000 (seed 2006), boot SE
  0.0081 (seed 2008), 90% CI (0.042, 0.068) — frame stated up front (pens
  cannot be first-time). chickwts slot (ex 15/17) = `intake71` six-arm
  finishing trial (seed 2009, 400-point assessment, arm sizes mirror
  chickwts): ex 15 pattern drills 220.08 (54.33, n 12) vs static repetition
  169.80 (35.43, n 10), T = 2.61, df = 9, p = 0.028 — rejects at 0.05 but
  not at 0.01 (IMS's α-flip in part (d) preserved); ex 17 constraint games
  314.33 (60.63, 12) vs small-sided 223.64 (46.80, 14), T = 4.22, df = 11,
  p = 0.0014, causal attribution. epa2021 slot (ex 16/18) = seed-2010
  samples of 25 matches per tournament (scores exclude shoot-outs; 172/106
  match-goal totals verified vs 169/103 shot-data goals, gap = own goals):
  goals/match 2.68 (1.91) vs 3.68 (1.99); margins 1.24 (1.23) vs 2.00
  (1.44). SE/df drills kept: ex 13 mirrors IMS's 15/20/50 vs 20/10/30
  (2.8284 / 1.8257 / 3.3665); ex 19 distraction mirror T = 2.24, df = 21,
  p = 0.036.

### Ch 21 — inference-paired-means.qmd (18 ex.)

- Tire tread → `gps_pair25`: 25 academy players wear both GPS-vest vendors in
  one session (pocket side randomized); paired diff in recorded sprint
  distance; within-pair permutation, reject | synthetic seed 2101.
- UCLA vs Amazon → per-team paired mean xG: under pressure vs not, paired by
  team (require ≥ 5 pressured shots per team, state the filter — it keeps
  22 of the 32 wc2022 teams, so ~22 pairs, df = 21); x̄_diff ≈ −0.032
  (verify; paired t ≈ −2.4, rejects); paired t + bootstrap CIs |
  real | note pairing removes between-team quality differences — say WHY
  pairing beats ch. 20's pooled comparison on the same variable.
- Exercises: paired-vs-independent identification drills in club settings;
  one weuro first-half/second-half per-match pairing (31 pairs).
- AS BUILT (GPS section REBUILT 2026-07-06, panel review — the original
  rnorm(25, 310, 3)/rnorm(25, 308, 3) build lacked the pairing structure the
  lesson preaches: vendor readings were independent draws and all 25 players
  "sprinted" 302–316 m): `gps_pair25` vendors = SprintTrack (ST) vs
  QuickPulse (QP), sprint distance in meters; seed 2101 now builds a
  per-player wide tibble `gps_sessions` — workload w_i ~ rnorm(25, 310, 50),
  then vendor columns in ALPHABETICAL order: QuickPulse = w + rnorm(25, 0, 3),
  SprintTrack = w + 2 + rnorm(25, 0, 3), each rounded 0.1 — then pivot_longer.
  Between-player SD (~34 realized; readings 287.8–417.1) dwarfs s_diff, so
  pairing-beats-pooling is now true IN THE DATA (two-sample SE 9.5 vs paired
  SE 0.94, both quoted in the pooling CYU). DRAW ORDER IS LOAD-BEARING:
  drawing ST's noise before QP's under the same seed yields x̄_diff = 1.31,
  sign-flip p = 0.17 — fail to reject, breaking the spec'd verdict; the
  alphabetical-column order (QP noise first) is the rule-5 fallback, recorded
  here. As built: x̄_ST 333.6, x̄_QP 330.9; x̄_diff 2.69, s_diff 4.72 (16
  pos / 1 zero / 8 neg; player 9's +4.1 feeds the new sign-flip CYU; player 3
  diff 0.0). Hand shuffles seeds 2102–2104 unchanged in pattern (13/12/11
  swaps; player 4 swaps, player 5 holds — IMS's 4th/5th-car narrative
  intact); simulated vendor gaps 0.6 / −0.2 / −0.2 m. Infer sign-flip seed
  2105: null range (−3.21, 3.49), 12/1000 two-sided, p = 0.012 — rejects at
  α = 0.05, no longer 0/1000; taught as the observed statistic sitting inside
  the null's range but deep in its tail. Figures inference-paired-means-1/2
  regenerated, same filenames/ggsave convention. Didactic additions (panel):
  sign-flip-universe CYU (±4.1, probability one-half each — the entire null
  universe for one pair) right after the paired-independence pipeline intro;
  predict-then-confirm CYU immediately before the team-paired open-play rerun
  (reader predicts the flip from the ch 19/20 precedents; answer confirms
  −0.0317 → −0.0028); recycled reveal phrasing ("Set the two runs side by
  side" / "State the frame, defend the filter…") varied in this chapter only.
  Team-paired test
  (`team_pressure`, diff = pressured − unpressured mean xG, ≥5 pressured
  filter): keeps 22/32 (drops incl. Australia, Spain); all-shots frame
  x̄_diff = −0.0317, s = 0.0612, T = −2.43, df 21, p = 0.024 (reject),
  95% CI (−0.0588, −0.0045); bootstrap seed 2106: 99% percentile
  (−0.0648, 0.0009), 99% SE (−0.0664, 0.0031) — unlike IMS's UCLA case BOTH
  99% intervals cross zero, taught as consistency with 0.01 < p < 0.05.
  PENALTY CONVENTION: the verdict FLIPS — all 238 pressured shots are open
  play, so the open-play rerun keeps the identical 22 teams and pressured
  sides while 57 pens @0.7835 leave the unpressured side of 15 pairs
  (Argentina 0.2080 → 0.1141): x̄_diff = −0.0028, T = −0.28, p = 0.78,
  95% CI (−0.0237, 0.0180); taught as the pens-in/pens-out pair per the
  ch 19/11 pattern. Pairing-beats-pooling taught at the power note (each
  team its own control; between-team quality and volume composition removed;
  pooled means 0.0961 vs 0.1315 recomputed in-chapter). Exercises: hsb2
  thread → wc2022 home/away-LABEL pairing at a neutral tournament (64
  matches, open-play frame, Spain 7-0 Costa Rica has 0 away open-play shots;
  x̄ = −0.19, s = 8.31; perm seed 2107 p = 0.856; boot seed 2108, 95% CIs
  (−2.17, 1.72) / (−2.22, 1.84); T = −0.18 fail to reject — mirrors hsb2's
  verdict, null ≈ true by construction). NOAA thread → the mandated weuro
  first/second-half pairing (31 pairs, open-play regulation-halves frame,
  815/913 shots kept; x̄ = 2.74, s = 5.51; perm seed 2109 p = 0.011; boot
  seed 2110, 90% CIs (1.06, 4.39) / (1.11, 4.38); T = 2.77, df 30,
  p = 0.0095 reject; 90% t-CI (1.06, 4.42)). friday traffic/accident →
  synthetic `turf10` (seed 2111; grass vs turf sprint output; T = 4.12,
  p = 0.0026) and `academies6` (seed 2112; injury flags per block;
  T = −5.40, df 5, p = 0.003, 95% CI (−3.94, −1.40); the critiqued memo's
  "as much as 40%" = ratio 9.33/6.67). forest → `jump50` (seed 2113; CMJ
  27.7 → 39.4 cm, diff 11.7 ± 6.3, 99% CI via t*₄₉ = 2.68). IMS ex 6's
  point-null bootstrap randomization replaced with the chapter-consistent
  paired-independence permute.

### Ch 22 — inference-many-means.qmd (14 ex.)

- Toy groups I–VI → six synthetic academy-intake grade distributions: three
  noisy, three tight-with-shifted-means | synthetic seed 2201.
- MLB OBP by position → mean xG by position group (FW/MF/DF; reuse ch. 4's
  mapping) at wc2022; ANOVA table from `lm()`; verify F and p in code |
  real | mirrors observational design.
- Exam A/B/C → `template_abc`: three report templates randomized across
  assignments; observed F vs 1,000 permuted F's, p ≈ 0.036 mirror | synthetic
  seed 2202.
- Classrooms snooping → eyeball xG/shot across all 32 wc2022 squads, then
  "test" only the two extremes: inflated Type I; 32 groups beats IMS's 20 |
  real + simulation seed 2203.
- Exercises: keep MSG/MSE hand-computation and df items; play_pattern ANOVA
  on weuro2025 as the marquee exercise.
- AS BUILT: case study runs the OPEN-PLAY frame (stated filter; no GK shots
  exist at wc2022 so nothing to drop; body part not involved): FW 678/0.1146,
  MF 443/0.0781, DF 261/0.0903, grand 0.0983; SSG 0.378, SSE 21.190,
  SST 21.568, MSG 0.189024, MSE 0.015366, F = 12.301 (df 2, 1379),
  p = 5.07e-06. Penalty convention pair shown at the ANOVA-table section:
  pens-in (n = 1,494) gives SSG 0.411, MSE 0.033708, F = 6.103, p = 0.0023 —
  the 64 pens (33 FW / 22 MF / 9 DF, all xG 0.7835) barely move SSG but
  DOUBLE MSE: penalties MASK the effect here (vs manufacturing one in ch 11);
  both frames reject, the halved F is the lesson, and the 0.7835 spike is the
  "extreme outliers" condition violation in the pens-in frame. Toy groups
  seed 2201 (`intake_toy`, 6 × 15 grades; I–III design means 62/66/64 SD 14,
  F = 2.66; IV–VI same means SD 1.8, F = 24.53; toy F's computed after F is
  defined). `template_abc` seed 2202 (n = 58/55/51 mirroring IMS classdata;
  design means 75/72/77 SD 13; realized 75.6/70.3/76.1), observed F = 3.4208
  vs IMS 3.48; shuffle-once seed 2204 (means 74.3/76.7/70.7, F = 2.89 — IMS's
  randANOVA image redrawn as full-data code); 1,000 perms seed 2205 → 33/1000,
  p = 0.033 (IMS 0.036 mirror), max permuted F 7.59. Snooping = real 32-squad
  open-play xG/shot table: Switzerland 0.1685 (36 shots) vs Australia 0.0607
  (26 — ch 19's team), t = −3.03, p = 0.0041; seed-2203 sim (shuffle team
  labels, t-test the eyeballed extremes, 1,000 reps) rejects in 77.8% of
  true-null worlds at α = 0.05. SST/SSE bridged to @sec-r-squared (SST = SSG
  + SSE vs SST = SSR + SSE, "same total, different knife"); CYU computes
  SSG/SST = 0.0175 as the ANOVA R² analogue. EXERCISES: IMS ch 22 has 14
  exercises, not the 9 this spec originally listed (header since corrected) —
  all 14 translated 1:1. Marquee
  ex 3/4 = weuro xG ~ play_pattern (8 levels; Other bucket = 54 shots
  (51 pens + 3 tagged) dropped with stated filter per ch 18 precedent,
  n = 859): F = 1.774, perm p = 0.091 (91/1000, seed 2207; shuffle-once seed
  2206) — fails to reject, consistent with ch 18's weuro verdict. Ex 5
  `drill71` seed 2208 (71 strikers, 6 programmes, chickwts sizes):
  F_{5,65} = 15.97, p = 3.1e-10. Ex 7/8 constructed tables mirror IMS numbers
  exactly (ex 7 reuses ch 18 ex 16's 50,739-player registry bands; outcome =
  weekly high-intensity match minutes). Ex 9 = weuro open-play pos-group
  ANOVA: F = 16.406 (df 2, 848), p = 1.0e-07, n = 851 — REJECTS where IMS's
  GPA analogue failed to reject (skill mirrored: read output, n from df:
  848 + 2 = 850 → 851). Ex 10 = wc xG ~ play_pattern (Other = 68 = 64 pens +
  4 tagged dropped, n = 1,426): F = 3.611, p = 0.0007 — counters top (0.159),
  verdict flips vs the Euro. Ex 13 seed 2209 `region_A`/`region_B` (SD 5 vs
  20): F_A = 11.01 (0/1000 beyond), F_B = 0.645 (560/1000 beyond). Ex 14 seed
  2210 `video_hours` (n = 905, 5 experience bands): F = 8.04, p = 2.3e-06.
  Chapter seeds 2201–2205, exercise seeds 2206–2210.

### Ch 23 — inference-applications.qmd (case study, 0 ex.)

- Single-mean bootstrap CI → mean statsbomb_xg at wc2022, percentile vs SE
  interval | real.
- Paired randomization test → each scout grades the same 10 prospects in
  video-first and data-first formats (order randomized within scout); permute
  within pair; small p | synthetic seed 2301.
- Two independent means, two parallel tests → (a) under pressure vs not
  (rejects, both tournaments), (b) wc2022 vs weuro2025 overall mean xG
  (0.1259 vs 0.1350 — expect NOT discernible; verify) | real | mirrors the
  4-item (sig) / 16-item (not sig) structure exactly.
- AS BUILT: case study = "the end-of-season review" (IMS anchors kept,
  incl. §sec-case-study-redundant-adjectives). Single-mean bootstrap runs
  BOTH frames per the convention: all-shots x̄ = 0.1259 (seed 2302,
  percentile (0.1172, 0.1357), SE_BS 0.0048, SE interval (0.1162, 0.1355))
  vs open play x̄ = 0.0983 (seed 2303, percentile (0.0919, 0.1047), SE
  interval (0.0918, 0.1049)) — the frames' intervals are DISJOINT (~6 SEs
  apart): pens INFLATE a single-mean benchmark (third verb after ch 11's
  manufacture and ch 22's mask). Paired test = `format_trial` (seed 2301):
  22 scouts × 10 full-backs, video-first vs data-first dossiers, crossover
  order randomized 11/11, response = % agreement with the expert panel;
  IMS's redundant-adjectives CSV is NOT in the repo, so the mirror is
  structural (n = 22, 10 items, percentage response, within-pair permute),
  not numeric: x̄_diff = 15.91, s_diff = 12.97, permutation 0/1000 (seed
  2304, p < 1/1000), t crosscheck T = 5.75 (df 21) — small p as spec'd,
  causal (randomized crossover). Two-means (a): the spec's "rejects, both
  tournaments" was the pens-in artifact and does NOT survive the honest
  frame — open-play runs FAIL in both: wc diff 0.0027, perm p = 0.743
  (seed 2305); weuro diff 0.0097, perm p = 0.213 (seed 2307; ch 20's
  seed-2005 p = 0.222 cited as the Monte Carlo gap). Ch 20's pens-in story
  (T = 4.27 wc; T = 6.27 weuro) recalled with citations, not rerun.
  (b) VERIFIED not discernible in both frames: all-shots 0.1259 vs 0.1350
  (diff 0.0092, perm p = 0.255 seed 2308; T = 1.15, df 912, p = 0.25) with
  the penalty-mix back-of-envelope (51/913 − 64/1494 shares × 0.6865 ≈
  0.0089) shown to explain ~all of the gap; open play 0.0983 vs 0.0974
  (perm p = 0.869 seed 2309; T = −0.18, p = 0.86) — closes ch 3's
  "0.098 vs 0.097" planted question. IMS's sig/not-sig contrast is thus
  carried by FRAMES (pens-in recalled sig, pens-out run not-sig) and by
  the paired trial (the afternoon's one rejection); the parallel-tests
  structure (can't pool tournaments → one test per competition, Simpson
  rationale) is mirrored exactly. Seed 2306 skipped (already used by
  data/ims/exercises/_05-ex-explore-numerical.qmd); chapter seeds
  2301–2305, 2307–2309. Tutorials/labs repurposed per ch 15: walkthrough
  = "seven questions, seven tools", one MATHEMATICAL-model lesson per
  chapter 16–22 (IMS lists 8 tutorial lessons; GOF was never taught and
  paired means needed a slot; no seeds — case study runs the engines, the
  walkthrough runs the shortcuts): L1 wc open-play first_time 468/1382 =
  0.3386, z-CI (0.3137, 0.3636) contains 1/3 (all 64 pens first_time =
  FALSE; all-shots 0.3133 flagged); L2 Euro finalists' open-play
  conversion 15/101 vs 18/142, pooled Z = 0.49, p = 0.63; L3 weuro
  open-play body_part × goal (4 "Other" dropped, expected < 1), X² = 0.62,
  df 2, p = 0.73 — the ch 4 header "deficit" gone in the honest frame;
  L4 Morocco open-play t-CI (n = 59; 4 shoot-out pens + 3 FKs excluded):
  (0.0611, 0.1225) STRADDLES 0.0983 — the anti-Australia verdict; L5 pays
  off ch 3's counter-attack question: 0.1592 (56) vs 0.0905 (41), T =
  2.58, df 40, p = 0.014 — REJECTS at 0.05 (not at 0.01; α-flip noted),
  penalty-free by construction; L6 16 KO teams, group vs knockout paired
  open-play xG: x̄_diff = −0.011, s 0.0415, T = −1.06, p = 0.30, 95% CI
  (−0.0331, 0.0111) — fail, Type II caveat; L7 weuro open-play xG ~ stage
  ANOVA: F(3, 847) = 0.13, p = 0.94. Lab = the Croatia file (both IMS labs
  merged: categorical + numerical arms): 8 pens ALL shoot-out kicks, 7
  scored → all-shots conv 0.1724 vs open-play 8/78 = 0.1026 (mean xG
  0.1512 vs 0.0884; field 142/1304 = 0.1089, 0.0989); Croatia's 8 open-play
  goals FAIL success-failure, routing task 2 to ch 16's parametric
  bootstrap. Ends with Chapter review {#sec-chp23-review} + "Terms
  revisited" table {#tbl-terms-chp-23} (15 terms from chs 16–22) per the
  ch 10/15 applications convention (overrides IMS's review-less ending).
  Nothing new introduced; no exercises.

### Ch 24 — inf-model-slr.qmd (9 ex.)

- Sandwich store → omniscient-federation illustration: synthetic population
  of 1,000 prospects with known true line (senior xG output ~ academy
  training hours); repeated samples of 20 fan out sample slopes | synthetic
  seed 2401.
- births weight~weeks randomization slope test → `team_match` goals ~
  total_xg: permute goals, observed slope 0.909 far outside null; reject |
  real | continuity with ch. 7's fitted line.
- births weight~mage bootstrap CI containing 0 → xG ~ minute (open-play
  shots): r ≈ ±0.03, bootstrap percentile + SE CIs straddle 0 | real |
  fatigue-drift story dies on inspection — teach that as the point.
- Midterms t-test (fail to reject) → match-level: goal margin ~ share of
  shots under pressure across 64 wc2022 matches; expect weak slope (verify;
  if discernible, switch predictor to kickoff-period share or use weuro's 31
  matches) | real | small-n + outlier/leverage discussion via blowout matches.
- Elmhurst t-CI → ch. 7's synthetic veteran-market model: 95% CI for the
  price-per-year-of-age slope, interpreted in € per year | synthetic (ch. 7
  seed/code).
- LINE panels → four synthetic violations (quadratic age-curve, mis-entered
  wonderkid, heteroskedastic fee~age, autocorrelated GPS load) + real bonus:
  residuals of goal ~ xG on shots exposing the binary-outcome violation →
  hooks ch. 26 | synthetic seed 2402 + real.
- Exercises: keep condition-checking items; slope-CI interpretation in
  football units.
- AS BUILT: sandwich analogue = "omniscient federation" registration cohort
  (seed 2401): `prospects`, hours ~ N(4, 1) thousands of academy training
  hours, xg3 = 12 + 4.7·hours + N(0, 8) three-season senior xG (IMS's exact
  generating geometry); population fit 11.27 + 4.85·hours; seed 2403 draws
  the two samples of 20 (slopes 8.38 / 5.28) and the 50 repeated samples
  (slope mean 4.85, SD 2.10, range −0.83 to 9.55 — one honest sample returns
  a NEGATIVE slope, taught). ε decomposed at first use (ch 7 used e only).
  Randomization test: canonical team_match (all-shots frame flagged per
  convention), goals ~ total_xg slope 0.9087 (SE 0.0849, T 10.70); 4-panel
  intro r's 0.40 / −0.16 / −0.27 / 0.69; perm scatter seed 2404, two perms
  seed 2405 (−0.025 / −0.060); seed-2406 1,000 permuted slopes span (−0.305,
  0.406), 0/1000 → reported p < 1/1000. Bootstrap: xG ~ minute (bare
  `minute`), open-play frame as mandated, n = 1,382, r = 0.0299, slope
  0.000131 (SE 0.000118, p = 0.2667); seed 2407 one resample (873 distinct
  shots, slope 0.0002), seed 2408 fifty lines (−0.00006 to 0.00038), seed
  2409 1,000 slopes: 95% percentile (−0.00007, 0.00034), SE_BS 0.00011,
  SE interval (−0.00009, 0.00035) — both straddle 0; fatigue drift ≤ 0.03 xG
  per 90 even at the CI edge. Midterms analogue VERIFIED weak, no fallback
  needed: margin ~ open-play pressure share, 64 matches, r = −0.073, slope
  −0.93 (SE 1.62), T = −0.57, p = 0.5688 — fail to reject; all-shots frame
  −0.77, p = 0.658 (same verdict, pair shown per convention). Blowout GP:
  Spain 7–0 (share 0.000) and Portugal 6–1 (0.391) sit at BOTH x-extremes;
  refit without them: slope −0.65, p = 0.62 (two-analyses practice).
  Elmhurst: seed-701 code verbatim; age −1.44 (SE 0.329), T −4.37,
  p 6.6e-5; df 48, t*_48 = 2.01; hand 95% CI (−2.10, −0.78), confint
  (−2.1029, −0.7783) — €0.78M–€2.10M per year of age. LINE (seed 2402):
  age hump (17–35, peak 26); mis-keyed wonderkid (fee 36.6 vs true ≈ 3.6,
  residual +32, slope 0.094 with vs 0.117 without); youth fees fan (16–22,
  SD ∝ age − 15.5); GPS random-walk load (lag-1 resid autocorrelation
  0.85). Real bonus: lm(goal01 ~ statsbomb_xg) on all 1,494 shots — slope
  0.951 (T 23.5); residual bands (goals +0.136..+0.982, misses
  −0.756..−0.011) → N and E impossible for binary outcomes → hooks
  @sec-inf-model-logistic. Chapter seeds 2401–2409 (2402 = LINE per
  reservation). EXERCISES: IMS ch 24 has 20 exercises, not the 9 in the
  header above — all 20 translated 1:1 (ch 22 precedent); seeds 2410–2417.
  Threads: bdims → `team_match_weuro` (62 rows, no shotless team-match;
  all-shots frame flagged): ex 1/5/7 goals ~ total_xg (slope 0.785, SE
  0.0777; perm seed 2410 range ±0.4, 0/1000; boot seed 2412: 98% pct CI
  (0.598, 1.087), SE_BS 0.107, 98% SE CI (0.536, 1.034)); ex 3/9 total_xg ~
  n_shots (slope 0.168, r 0.63, R² 39%) — the four largest residuals
  (+3.7 to +4.8) are the two shoot-outs' team-matches (7–8 kicks at 0.7835),
  taught in ex 9's solution as the penalty convention meeting the N check.
  births/fage → weuro open-play xG ~ minute, ex 2/4/6/8/10 (n = 851,
  r = −0.0326, slope −0.000125, p = 0.342; perm seed 2411 p = 0.363; boot
  seed 2413 95% pct (−0.00037, 0.00013), SE_BS 0.00013). murders →
  `matches20` (seed 2414: 20 of 64 matches; single-source frame = shots with
  period ≤ 4, in-game pens in both sides, own goals absent — stated): ex
  11–15, slope 1.10 (SE 0.330, p 0.0036), perm seed 2415 5/1000 = 0.005,
  95% t-CI (0.41, 1.80) via t*_18 = 2.10, boot seed 2416 90% pct (0.78,
  1.68), SE_BS 0.28; England 6–2 Iran (8 goals, 3.44 xG, resid +4.0) is ex
  15's outlier. cats → wc team_match total_xg ~ n_shots, ex 16/19 (slope
  0.154, SE 0.0140, 95% CI (0.126, 0.181) via t*_125 = 1.98; residual SD by
  volume third 0.41/0.77/1.24 — a REAL fan, E-violation discussion). bac →
  `drill16` (seed 2417): 16 forwards randomly assigned 1–9 extra sessions,
  gain = 1 + 2.2·s + N(0, 3); slope 2.19 (SE 0.279), r 0.90, R² 0.81,
  causal per design; ex 20 = small-n residual plot + generalization.
  urban_owner → ex 18 team_profile prop_headers ~ prop_pressure (r 0.50,
  R² 25%, fit 0.11 + 0.40x).

### Ch 25 — inf-model-mlr.qmd (12 ex.)

- Loans MLR p-values → xG ~ under_pressure + one_on_one + minute on wc2022;
  interpret each conditional p-value ("given the other variables") | real.
- Coin dish multicollinearity → synthetic team-threat data: predict total
  threat from total shots and n low-quality shots; slope sign flips between
  nested models | synthetic seed 2501 | fabricate ~26 rows like IMS's coins.
- Penguins CV → 4-fold CV on wc2022: small model (xG ~ one_on_one) vs large
  (+ under_pressure + body_part + technique + play_pattern); CV SSE drops
  sharply; then external validation on weuro2025 as holdout | real.
- Exercises: conditional-hypothesis phrasing drills; one CV-by-hand fold count.
- AS BUILT: frame = ch 8's `shots_wc` (1,365 open-play, `Other` body/pattern
  dropped), rebuilt verbatim; weuro frame same prep code → 844 shots. Loans
  mirror `m_shot_tags` (xG ~ under_pressure + one_on_one + minute): 0.0832 +
  0.00009·up + 0.1040·oo + 0.00012·min; conditional p-values 0.991 / 3.1e-13 /
  0.289 — unlike IMS's all-low loans p-values, the three verdicts span the
  range, taught as the richer lesson (formalizes ch 10's elimination of the
  pressure tag; ch-8 cross-model contrast −0.0052/p 0.577 vs 0.00009/p 0.991
  drills the "given the others" reading). Coin dish = `threat26` (seed 2501):
  trainee tally classes hopeful hit 0.01 / half-chance 0.05 / decent look
  0.10 / big chance 0.25 (the quarter); low-quality = shots − big chances;
  r(threat,shots) 0.681, r(threat,low) 0.251, r(shots,low) 0.867; slopes
  0.096 (p 1.3e-4), 0.040 (p 0.217), joint +0.263/−0.218 (both <1e-10) —
  sign flip and $0.41/$0.66/$0.17 swap examples mirror IMS as 0.41/0.66/0.17
  xG. CV seed 2502 (folds 342/341/341/341): CV SSE small 18.909 vs large
  18.557 — the spec's "drops sharply" FAILS empirically (≈2% drop; in-sample
  18.81/18.01); taught honestly as the tags-can't-see-the-pitch theme, with
  the in-sample-vs-CV gap as the overfit signature. External validation
  (added subsection "Validating on a second tournament", ch 10's promise):
  weuro holdout SSE small 10.123 vs large 10.537 — order REVERSES; per-shot
  MSE 0.0139→0.0120 (small), 0.0136→0.0125 (large); mechanism shown via lobs
  (wc 13 open-play lobs mean xG 0.251 → +0.137 coefficient; weuro's 13 lobs
  mean 0.053; large predicts 0.232 on them, small 0.090). k-collision
  (ch 8 predictors / ch 22 groups / ch 25 folds) flagged at the fold
  definition; $\hat{y}_{cv,i}$ and CV SSE decomposed at IMS's anchors.
  EXERCISES: IMS count verified = 12, all translated 1:1; seeds 2503
  (`trainee55`, all slopes non-discernible, CI for `live_mt2` (−1.51, 8.13)),
  2504 (`transfer540` ROI, academy-graduate tail breaks LINE), 2505/2506
  (`we100` weuro sample + 4 folds: CV SSE 7-pred 1.252 > 2-pred 1.180 —
  mirrors IMS's ex-11 overfit verdict; 8 vs 3 coefficients exact mirror),
  2507 (`match64` open-play match goals, 3-fold: 6-pred 143.2 > 2-pred
  128.4). Ex 3 real cherry-mirror (32 wc open-play teams): xg~shots and
  xg~matches each discernible alone; jointly matches flips sign (+1.35 →
  −0.12, p 0.518) — flips where IMS's cherry keeps both, same skill, taught
  in the solution. Ex 7 = ch 8's `m_full` verbatim + diagnostics (resid
  −0.236..+0.817, all 44 |resid|>0.3 positive); tests under_pressure given
  others, p 0.577 → fail to reject (IMS's habit rejects; skill mirrored,
  verdict flips). Ex 8 = canonical `team_match`: goals~shots 0.116
  (p 2.6e-6) alone dies jointly (−0.045, p 0.082) next to xg 1.05 — the
  coin dish on real data. Ex 6 constructed table mirrors IMS numbers
  exactly (ch 22 ex 7/8 precedent).

### Ch 26 — inf-model-logistic.qmd (8 ex.)

- Email spam (whole chapter) → goal ~ under_pressure + first_time +
  one_on_one + body_part + play_pattern on wc2022; goals ≈ 13% of shots
  mirrors spam imbalance; Wald p-values; classify at a LOW cutoff (0.10–0.15)
  and discuss recall/specificity trade-off for a shortlist | real.
- Calibration buckets → bucket weuro2025 shots by predicted probability,
  observed goal rate with CIs; bonus: calibration of `statsbomb_xg` itself —
  "is the xG model honest?" | real.
- CV model choice → 4-fold CV small vs large model; goal true-positive vs
  non-goal true-positive rates; train wc2022 → test weuro2025 external
  validation | real.
- Exercises: coefficient back-transformation drills; cutoff-choice reasoning.
- AS BUILT: taught frame = ch 8's open-play filter (`shot_type == "Open
  Play"`, `Other` body/pattern dropped; n = 1,365, 147 goals, conv 0.1077 —
  the spec's ≈10.9% is the 1,382-shot filter; pens-in 195/1,494 = 0.1305
  shown as companion, both recomputed in-chapter) per ch 9's coda. ONE
  chapter model serves diagnostics + Wald + CV-large: goal ~ under_pressure +
  first_time + one_on_one + body_part + play_pattern (13 coefs, refs Right
  Foot / Regular Play) — ch 9's promised centerpiece returns with technique
  swapped for play_pattern per this spec, and IMS's separate 4-predictor
  software-section model is folded into it (level-indicator hypotheses taught
  via ch 8's notation). Wald results: first_time +0.9832 (Z 4.70, p 2.6e-6),
  one_on_one +1.1256 (Z 3.49, p 4.8e-4), body_partHead +0.7566 (p 0.010,
  taught as ch 2's confounder adjusted); under_pressure −0.0695, p 0.79 —
  converges with chs 10/11/20. PENALTY CONVENTION delivered at the Wald
  table: pens-in refit (n = 1,494, Other levels kept) hands the biggest Z to
  play_patternOther (+3.02, Z 9.54 — the 64 pens live in that bucket) and
  FLIPS the one_on_one verdict (0.576, p 0.074; 6 pens carry the 1v1 tag).
  Diagnostics: in-sample 8-bucket calibration, 7/8 CIs cover y = x (bucket 4
  misses: obs 0.041 vs pred 0.085); logistic residual e_i = Y_i − p̂_i owned
  here (Kaye −0.184 / Ziyech +0.844; two-stripe contrast with ch 7's e_i,
  hooks ch 24 via @sec-tech-cond-linmod). CV: seed 2601, 4 folds
  (342/341/341/341), cutoff 0.10 (< base rate 0.108; 0.5 shown vacuous, max
  p̂ = 0.397); smaller model goal ~ one_on_one (−2.1818/+0.9114) is a KNIFE
  EDGE — its ordinary-shot price straddles the cutoff by fold
  (0.107/0.093/0.096/0.109), so folds 1/4 flag everything (goalTP = 1,
  nongoalTP = 0) and folds 2/3 flag only 1v1s (goalTP 0.068/0.119) — taught
  as the single-tag failure mode plus the accuracy trap (0.09 vs 0.84 for
  the same useless model); larger model goalTP 0.48–0.80, nongoalTP
  0.44–0.60; recall/specificity named in prose (italic, kept out of Terms);
  CYU reruns cutoff 0.15 (accuracy up, recall 0.16–0.57). External
  validation {#sec-chp26-external}: goal_fit → weuro open play (851 − 7 =
  844, 93 goals, 0.110); at 0.10: 342 flagged, goalTP 0.495, nongoalTP
  0.606 — inside the CV fold ranges. Weuro 5-bucket calibration of the
  exported p̂: obs nearly flat (0.065–0.137) vs preds 0.050–0.183, bucket-1
  CI (0.055, 0.146) excludes its 0.050 prediction → ranking transfers,
  probabilities don't. statsbomb_xg honesty check (chapter-level version of
  ch 9 ex 4: weuro, quantile buckets, CIs): all 5 CIs cover avg xG (obs
  0.018→0.315 vs priced 0.019→0.271) — honest on open play; penalty coda per
  convention: weuro 28/51 = 0.549, CI (0.412, 0.686) EXCLUDES 0.7835; wc
  43/64 = 0.672, CI (0.557, 0.787) covers — logged as a vendor query, not a
  conviction. Deviations: review anchor {#sec-chp26-review} (IMS's file
  carries a typo'd #sec-chp27-review that would collide with ch 27's
  book-convention review); summary cites @tbl-randsampValloc (a table in
  this book's ch 2, a figure in IMS). EXERCISES: 8, 1:1 (IMS count verified
  = 8); ex 3/4 gain back-transform part (b), ex 5 a cutoff-choice part (d),
  ex 6 a part (e), per this spec's drill mandate. Ex 3 = goal ~ first_time
  on the chapter frame (0.0855 vs 0.1509; Z 3.65, p 2.65e-4; back-transform
  reproduces the group rates). Ex 4 = `warmup_trial` seed 2602 (1,475
  players, 738/737, fit-all-season 0.852 vs 0.890; Z 2.16, p 0.031; causal).
  Ex 5/7 = competition classification (possum mirror; 2,209 combined
  open-play shots, 4 folds seed 2603, cutoff 0.5): minute model collapses to
  majority (1,365/2,209 = 0.618, never predicts weuro); under_pressure +
  statsbomb_xg model 1,449/2,209 = 0.656 (321/844 weuro recovered; the
  cross-competition pressure-tagging gap doing the work is flagged in the
  solution). Ex 6/8 = weuro goal CV (births14 mirror; 844 shots, 3 folds
  seed 2604, default 0.5 cutoff as the foil): 5-predictor model predicts
  goal for nobody (751/844 = 0.890); xG + 1v1 model flags 27 (16 right),
  756/844 = 0.896 — feeds the cutoff-reasoning parts. Chapter seeds 2600
  (plot jitter) + 2601; exercise seeds 2602–2604. (Ch 26 is wired into
  _quarto.yml and exercise-solutions.qmd as of 2026-07-06.)

### Ch 27 — inf-model-applications.qmd (case study, 0 ex.)

- Mario Kart case study → xG ~ one_on_one SLR (slope ≈ +0.127), then MLR
  adding under_pressure + first_time + play_pattern: watch the 1v1 premium
  shrink (confounding: 1v1s arise in open play) — the wheels/cond_new story |
  real wc2022.
- Permutation slope null → permute one_on_one labels 1,000×; observed slope
  far outside | real + seed 2701.
- Bootstrap slope CIs → 1,000 resamples; SE-method vs percentile 90% CIs for
  the 1v1 premium | real + seed 2702.
- CV wrap-up → 3-fold CV, 1-predictor vs 4-predictor CV SSE | real.
- Match-level coda → bootstrap CI for the knockout-stage indicator on goals
  across 64 matches: wider CIs from small n | real wc2022_matches.
- AS BUILT: working frame = ch 8's open-play filter rebuilt as `shots27`
  (1,365 shots; identical filters/recodes, keeps `first_time` as a fourth
  0/1 tag; body_part/technique not modeled). Case study opens on ch 7's
  all-shots fit (0.119/0.127, recomputed) and reuses ch 8's count table
  (6/64 pens tagged 1v1 at the fixed 0.784; 7% vs 4% group shares) to move
  to the open-play frame per the penalty convention: SLR 0.0896 + 0.1039
  (SE 0.0141). SPEC DEVIATION (rule 5): the spec'd "watch the premium
  shrink" FAILS empirically for the mandated 4-predictor MLR — the premium
  RISES 0.1039 → 0.1273, because 0 of 73 open-play 1v1s are first-time
  while first_time carries +0.0706; play_pattern alone shrinks it only to
  0.1014 (counters 9.6% vs 3.7%, goal kicks 13.7% vs 5.3%). Taught honestly
  as adjustment-is-direction-agnostic: the wheels/cond_new shrink is
  delivered by the FRAME move (0.127 → 0.104, the 6 pens as the bundled
  confounder — frame-vs-control taught explicitly), with ch 8's
  technique-equipped 0.0872 recalled as the third conditional answer
  (ch 25's language). Permutation seed 2701: 1,000 permuted slopes span
  (−0.0329, 0.0747), 0/1000 ≥ |0.1039| → p < 1/1000. Bootstrap seed 2702:
  SE_BS 0.0195 vs lm's 0.0141 — the gap taught as the E-violation (group
  SDs 0.166 vs 0.114; ch 20's unpooled SE reproduces the bootstrap,
  0.0197); 90% CIs: SE (0.0718, 0.1360), percentile (0.0724, 0.1367). CV
  seed 2703, 3 folds (455 × 3): CV SSE 1-pred 18.87 vs 4-pred 17.52 (≈7%
  better; in-sample 18.81/17.11 — the 0.05-vs-0.41 flattery gap per
  ch 25); IMS's factor-of-two GP answered honestly (spread comparison
  genuinely ambiguous: 85.6% vs 79.3% of errors within ±0.1; worst
  under-prediction obs 0.897 / pred 0.134, fold 3). Match coda = tutorials
  repurpose (ch 15 pattern), {#sec-inf-model-tutorials}: total_goals ~
  knockout on 64 matches (48/16; means 2.50/3.25; slope 0.75, SE 0.543,
  p 0.172, not discernible); bootstrap seed 2704: SE_BS 0.525, 90% pct
  (−0.104, 1.622), SE (−0.114, 1.614) — both straddle 0; relative widths
  0.62 vs 2.3 as the small-n lesson; data callout flags ET exposure,
  shoot-outs excluded, own goals included. Lab {#sec-inf-model-labs} =
  weuro rerun of the whole audit: agent's all-shots fit 0.128 + 0.228
  shown as materials (29 1v1s, 8 of them pens — ch 19's flag recalled as
  the hint; open-play answer 0.0950 + 0.0980, T 3.98, p 7.5e-5, verified
  in the build run but NOT printed in the chapter). IMS anchors kept:
  {#sec-inf-model-applications}, {#sec-case-study-mario-cart} (IMS's own
  spelling); review {#sec-chp27-review} per the ch 15/10 house convention:
  no-new-terms prose + "Terms revisited" table {#tbl-terms-chp-27}
  (12 terms) + the book-closing Northbridge passage inside the Summary; no
  exercises. Chapter seeds 2701–2704. (Ch 27 is wired into _quarto.yml as of
  2026-07-06; no solutions entry needed — case-study chapter.)

## 2.5 BOOK-ORIGINAL APPENDICES (no IMS counterpart; added 2026-07-06 from student-panel feedback)

- appendix-setup.qmd — R/RStudio install, packages, data access, first script.
- exercise-solutions.qmd — worked odd solutions (IMS convention).
- appendix-even-answers.qmd — bare final answers for evens (user-approved;
  includes exercises/_NN-ea-*.qmd files; keep reasoning OUT so evens remain
  assignable / usable as tutor mastery checks).
- appendix-reference.qmd — notation index (mirror of §1.4), football primer,
  method-chooser, penalty-convention at-a-glance.
- appendix-further.qmd — further reading ("where the proofs live"), estimand
  bridge, same-move-other-fields table.
- appendix-dependence.qmd — worked AR(1) demo (seeds 9001/9002): naive SE vs
  truth, effective n; mixed-models signposts. Appendix seeds use the 90xx block.
- Supplemental exercises marked "S1" in _12/_14/_19-ex sit OUTSIDE the IMS
  numbering (simulation workshops); their solutions live in the _NN-sa files.

## 3. HARD RULES (restated)

1. Study-design fidelity: IMS randomized experiments → Northbridge
   randomizable interventions (synthetic, seeded, visible code). IMS
   observational studies → real StatsBomb data with association-only language
   where a football-data analogue exists; observational/survey IMS cases with
   NO football-data analogue may become constructed synthetic scenarios
   (seeded, framed as constructed, never presented as real, design type
   preserved) — e.g. Elmhurst → veteran market (chs. 7/24, seed 701), payday
   survey → network survey (ch. 16, seed 1601), Brexit/YouGov → scout panel
   (ch. 6, seed 601), Simpson's paradox → scout ratings (ch. 3, seed 301).
   Constructed illustrations stay constructed.
2. Football scouting/recruitment exclusively; adjacent club operations
   (academy, medical, load management) sparingly; nothing outside the club.
3. Every real-data number must be recomputed from `data/derived/` inside the
   chapter's own code blocks. §1.5 values are checkpoints, not sources.
4. Chapter 11 flagship is fixed: `dossier48` (IMS sex-discrimination mirror,
   48 scouts, 21/24 vs 14/24) as the opening randomized experiment, and the
   wc2022 under-pressure conversion split (0.1008 vs 0.1361) as the
   observational randomization test — taught as a pens-in/pens-out PAIR per
   §1.5's penalty convention: the all-shots test comes within sight of the
   bar (p = 0.084; discernible at α = 0.10, not at 0.05), the open-play rerun
   is nowhere close (p = 0.385), and that contrast is the lesson.
5. Reuse the cast, datasets, and seeds defined here. If a spec'd example fails
   empirical verification (direction/discernibility), use the fallback noted
   in its bullet or the nearest synthetic variant — and update this file.
