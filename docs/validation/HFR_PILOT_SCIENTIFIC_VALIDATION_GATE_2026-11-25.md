# HFR pilot — scientific validation gate assessment

**Date:** 25 November 2026
**Branch basis:** `main` at `6da85c2` (post PR #5 merge)
**Scope:** the IZOL/PIRA 7-day Lagrangian pilot (`results/hfr_pilot_audit*`,
`results/hfr_pilot_sensitivity/`). This document decides what the pilot may
scientifically claim and what remains unvalidated, following
`docs/validation/INDEPENDENT_VALIDATION_PROTOCOL.md`,
`docs/science/RESEARCH_QUESTION_AND_HYPOTHESES.md` and
`docs/model/M0_M1_M2_MODEL_SPECIFICATION.md`.

**Executive decision: CONDITIONAL — the pilot is a verified numerical
exercise and a sensitivity study, not an independently validated transport
model.** It may be reported in the dossier as *software-verified,
QC-controlled advection bookkeeping on real HFR subsets*, with sensitivity
ranges. It may **not** be reported as validated transport, as M0
advection–diffusion skill, or as evidence about microplastic
concentrations. A defensible path to Tier-A validation exists (OBS-01/02/06
below) but requires data requests that have not yet been answered.

---

## 1. What the present pilot actually establishes

Audit of `scripts/run_hfr_m0_pilot.py` + `src/rheomarine_hfr/`:

| Element | What it actually is | What it is NOT |
|---|---|---|
| Release | deterministic 8×8 (or 16×16) lattice inside the selected block, kept where the t0 stencil is QC-valid | not observed particles, not a measured initial distribution |
| Domain | best `block×block` cell window by mean temporal validity (4×4 → ~30 km²; 8×8 → ~120 km²) | not a chosen, representative pilot polygon; no coastline logic |
| Window | fixed 2026-11-18T14:02Z → 2026-11-25T14:02Z acquisition subset | one week only; not a seasonal or climatological sample |
| QC | `QCflag==1` (provider "good_data") + finite + \|v\|≤10 m/s + no fill; missing never zero-filled | provider flag is necessary-not-sufficient; no independent accuracy estimate |
| Gaps | segments split at gaps >3 h; all-invalid timestamps are barriers; per-step pathwise exact cell traversal | no trajectory crosses unobserved intervals — verified in code and tests |
| Boundary | `reflect`/`absorb` on the artificial crop edge | not a coastline, not an open boundary; both are sensitivity closures |
| Dynamics | K=0 forward-Euler advection on observed intervals, bilinear interpolation | not the finite-volume advection–diffusion `rheomarine_transport` engine; no diffusion, no settling, no vertical transport |
| Metrics | alive / qc_stopped / exited counts; active-only and all-initial-cohort displacement medians | displacement of a synthetic cohort under artificial closure — a bookkeeping diagnostic, not a transport statistic |

**Separation of evidence classes:**

- **Software verification (done):** 33 unit tests OK; exact pathwise QC
  traversal with adversarial grazing tests; SHA-256-verified inputs;
  reproducible commands. This validates the *code*, not the ocean.
- **Forcing-data QC (done, bounded):** flag semantics verified against the
  NetCDF `flag_values`/`flag_meanings` attributes (0=none, 1=good,
  2=probably_good, 3=correctable_bad, 4=bad, …). ~49–51 % of cells carry
  flag 1 in the 7-day subsets; flag 4 carries real (non-fill) velocities
  and is provider-flagged *bad_data* — correctly excluded by default.
- **Process/sensitivity results (done):** §5 matrix below.
- **Independent validation (NOT done):** no independent contemporaneous
  observation of currents *or* particles exists in-hand for this window.

## 2. Independent hydrodynamic validation — feasibility

HFR-vs-ADCP/drifter comparison can validate the **current field only**;
it cannot validate microplastic trajectories (protocol §3.2). Full
candidate inventory: `docs/validation/hfr_pilot_candidate_observations.csv`.

| Candidate | Status | Tier (current field) |
|---|---|---|
| OBS-01 OGS/Arpa FVG CODE+Stokes drifters, Gulf of Trieste (NEREIDES) | campaigns Dec-2024 → ~bimonthly through 2025–26; a Nov-2026 release is plausible but **unverified**; data not public — request to OGS/Arpa FVG | **A if a window-overlapping deployment exists and tracks are shared** |
| OBS-02 CMEMS `INSITU_MED_PHYBGCWAV_DISCRETE_MYNRT_013_035` | NRT product covering the window (metadata verified); actual drifter/mooring coverage inside the bbox **unverified — requires free CMEMS account query** | B until queried |
| OBS-03 CMEMS `INSITU_GLO_PHY_UV_DISCRETE_NRT_013_048` | global drifter+HFR NRT product; ~15 m drogue vs HFR ~1–2 m effective depth — shear caveat | B |
| OBS-05 NIB "Vida" buoy AWAC (off Piran, ~22 m) | operational for years, data on request; **subsurface profile, not surface** | B/C for surface currents |
| OBS-06 ADCP offshore Piran 45.55N 13.55E (inside pilot area) | referenced as available in Giordano et al. 2024; status/continuity **unknown — request from NIB** | B if shared |
| OBS-04 OGS MedSVP drifter archive (SEANOE 10.17882/90537) | open access but ends 2021–2022 | C — no window overlap |
| OBS-07/08 DIGOT 1984-85, NIB buoy 2003-06 | historical | C |
| OBS-09 HFR-NAdr TRI1/AURI | same network/processing — **not independent** | D |

**Conclusion:** no compatible contemporaneous independent current
observation is currently in hand. The correct statement is *"current-field
validation is feasible but pending data requests (OBS-01, OBS-02, OBS-06)"*.
A bounded regional benchmark (HFR vs long-term drifter climatology,
MedSVP archive, Tier C) can be produced without new downloads but must be
labelled regional, not pilot validation.

## 3. Independent particle-observation audit — Gajšt et al. (2016)

- Publication verified: Gajšt, Bizjak, Palatinus, Liubartseva, Kržan,
  *Mar. Pollut. Bull.* 113:392–399, DOI 10.1016/j.marpolbul.2016.10.031.
  17 epi-neuston trawls (300 µm) over 20 months in the **Slovenian part of
  Trieste Bay**; mean 406×10³ particles km⁻².
- **Data recoverability: NO public repository found.** Searches across
  Mendeley Data, PANGAEA, SEANOE and the journal page returned no dataset.
  The DeFishGear protocols document (Palatinus et al. 2015) describes the
  method but is not the data.
- **Classification: Tier C** (protocol §3.1) until the authors
  (University of Nova Gorica / NIB) provide sample-level coordinates,
  dates, tow tracks, counts, size fractions and filtering volume/area.
  The published regional mean must **not** be converted into a spatial
  validation field — the paper itself links variability to surface
  currents via a Markov-chain model, i.e. it is a *benchmark for
  plausibility*, not ground truth for our window.
- **Marchetto et al. 2022** (Venice Lagoon inlet, 2 campaigns 2015) is
  geographically distinct — kept as Tier C regional context only.
- **Action item:** formal data request to Gajšt/Palatinus/Kržan for the
  17 trawl records; also ask whether the Markov-model forcing fields are
  archived (could provide a published-model comparison, still Tier C).

## 4. Pilot-domain decision

**What the automatic selection produced** (from run metadata):

- IZOL block: lat 45.5539–45.5943, lon 13.5295–13.5874 (~30 km²)
- PIRA block: lat 45.5539–45.5943, lon 13.5681–13.6261 (~30 km²)
- Both lie in the **central Gulf of Trieste, ~3.6–7.7 km off the nearest
  Slovenian coast points** (Piran/Portorož/Strunjan), i.e. inside the
  nearshore Gulf, plausibly within the Slovenian coastal sector.

**Is it representative?** Partially. It is the highest-QC-coverage window
*by construction*, which biases it toward the best-observed (not
necessarily most-typical) waters. Precise assignment to Slovenian
territorial sea vs the Italy–Slovenia maritime delimitation in the Gulf
requires the official boundary line (e.g. Marineregions territorial-sea
layer or national gazette coordinates) — **unresolved, flagged**.

**Recommended objective selection rule (proposal, not yet applied):**

1. Fix the candidate domain *a priori*: intersection of (a) common
   IZOL∩PIRA QC-valid coverage mask, (b) a defensible geographic polygon —
   e.g. "Slovenian territorial sea ∩ Gulf of Trieste nearshore band",
   or the polygon used by Gajšt et al. for the Slovenian Trieste Bay —
   and (c) a maximum alongshore extent.
2. Within that polygon, select the sub-window by a *predeclared* rule
   (e.g. maximum mean validity, as now — but reported as such).
3. Run the pilot on the polygon-level domain with an **open or
   weakly-reflecting boundary**, not a 4×4 reflective box.

Until then the 4×4/8×8 results stand as **computational sensitivity
experiments**, preserved unchanged in `results/hfr_pilot_audit*/`.

## 5. Minimum sensitivity matrix — executed on existing subsets

All runs on the same two SHA-256-verified 7-day `.nc` subsets; K=0,
seed 42, exact pathwise QC. "Longest segment" = the single longest
contiguous segment per site. Active-only vs all-initial displacement
reported separately per protocol.

| # | Variant | Site | nseg | longest nt | alive/qc/ex | disp_active_med | disp_all_med |
|---|---------|------|------|-----------|-------------|-----------------|--------------|
| S0 | block4 reflect (baseline) | IZOL | 6 | 142 | 64/0/0 | 3.34 km | 3.34 km |
| S0 | block4 reflect | PIRA | 5 | 136 | 64/0/0 | 2.56 km | 2.56 km |
| S0 | block4 absorb | IZOL | 6 | 142 | 0/0/64 | — | 1.71 km |
| S0 | block4 absorb | PIRA | 5 | 136 | 0/0/64 | — | 1.16 km |
| S1 | block8 absorb | IZOL | 6 | 142 | 0/0/64 | — | 3.47 km |
| S1 | block8 absorb | PIRA | 5 | 136 | 0/16/11 | — | 2.50 km |
| S2 | gap ≤1 h, block4 reflect | IZOL | 6 | 142 | 64/0/0 | 3.34 km | 3.34 km |
| S2 | gap ≤1 h | PIRA | 7 | 102 | 17/47/0 | 3.47 km | 3.01 km |
| S3 | gap ≤6 h | both | = S0 | = S0 | = S0 | = S0 | = S0 |
| S4 | QC {1,4} incl. bad_data | IZOL | 1 | 337 | 64/0/0 | 3.60 km | 3.60 km |
| S4 | QC {1,4} | PIRA | 1 | 325 | 0/64/0 | — | 1.90 km |
| S5 | release 16×16, block4 reflect | IZOL | 6 | 142 | 256/0/0 | 3.39 km | 3.39 km |
| S5 | release 16×16 | PIRA | 5 | 136 | 256/0/0 | 2.54 km | 2.54 km |
| S0 | block8 reflect (existing) | IZOL | 6 | 142 | 64/0/0 | 7.03 km | 7.03 km |
| S0 | block8 reflect | PIRA | 5 | 136 | 0/27/0 | — | 4.00 km |

**Reading:**

- **Boundary is the dominant sensitivity**: `absorb` empties the cohort
  within days on every configuration; `reflect` retains everything in
  the longest segment. Neither is a physical coastal condition — both
  are artificial crop closures bounding the answer.
- **Domain size matters**: 8×8 roughly doubles IZOL displacements and
  drives PIRA's longest segment to total QC attrition — the same ocean,
  different bookkeeping.
- **Gap threshold**: 1 h splits PIRA into more, shorter segments
  (longest 102 ts vs 136) with visible QC attrition inside the longest;
  6 h changes nothing → no gaps in (3 h, 6 h] in these subsets.
- **QC policy is first-order**: including provider-flagged `bad_data`
  (flag 4) merges all-invalid timestamps into continuous segments
  (337/325 ts) yet degrades PIRA to 64/64 QC-stopped — bad vectors
  poison stencils. Confirms flag-1-only is the defensible default.
- **Release density** (8×8→16×16): medians stable within ~2 % —
  displacement statistics are not an artefact of lattice spacing.
- **Time window**: only the acquired 7-day subset exists; window
  sensitivity is bounded by segment-level variability shown above.
  Alternate windows require new downloads (not launched).

Reproduce: `PYTHONPATH=src python3 scripts/run_hfr_m0_pilot.py
--inputs 'data/hfr/raw/*_7d.nc' --out results/hfr_pilot_sensitivity/<name>
[--block N] [--boundary reflect|absorb] [--max-gap-s S] [--qc-flags 1,4]
[--n-side N]` — outputs committed under `results/hfr_pilot_sensitivity/`.

## 6. Numerical/model verification boundary

The pilot is **K=0 surface forward-Euler advection** driven by observed
intervals with exact pathwise QC gating. It is **not** the
`rheomarine_transport` finite-volume advection–diffusion engine, and it
does **not** exercise:

- M0 advection–diffusion (no K_h, no Eulerian solve) — *unverified here*;
- M1 particle classes, settling, aggregation, biofouling — untouched;
- M2 rheology — gated separately (M4);
- vertical transport, settling velocity, seabed deposition — out of scope
  of surface HFR by definition.

**Minimum benchmarks required before any stronger claim** (from
`docs/model/M0_M1_M2_MODEL_SPECIFICATION.md` §6 and standard practice):

1. uniform-flow translation test (particle displacement = ∫u dt);
2. solid-body rotation / manufactured-solution test for the Eulerian
   solver where applicable;
3. mass/number budget closure for the advection–diffusion engine;
4. grid and time-step convergence study;
5. open-boundary treatment test (inflow/outflow) replacing reflect/absorb
   sensitivity closures;
6. only then: comparison against OBS-01/02/06 current fields (Tier A/B),
   and separately against Tier-A particle observations if ever obtained.

## 7. Permitted wording for the RISTANC dossier

**Allowed:**

- "A QC-controlled Lagrangian advection pilot was executed on real
  HFR-NAdr IZOL and PIRA subsets (Nov 2026), with exact pathwise QC
  gating, SHA-256-verified inputs and 33 passing unit tests."
- "Results are reported as sensitivity ranges across domain size,
  boundary closure, gap threshold and QC policy; they are computational
  experiments, not validated transport predictions."
- "Independent validation of the current field is feasible via OGS/Arpa
  FVG drifters and CMEMS in-situ products; data requests are pending."
- "Gajšt et al. (2016) provides a Tier-C regional benchmark pending
  recovery of sample-level data."

**Forbidden:**

- "validated", "verified against observations", "predictive skill" for
  the pilot outputs;
- any claim of M0 advection–diffusion, settling, vertical transport or
  seabed deposition from this pilot;
- treating the release lattice as observed particles or reflect/absorb
  as coastline physics;
- converting the Gajšt regional mean into a spatial validation field.

## 8. Unresolved items / data requests

| # | Item | Request to |
|---|------|-----------|
| 1 | Drifter tracks overlapping 2026-11-18→25 (NEREIDES campaigns) | OGS / Arpa FVG |
| 2 | CMEMS INSITU_MED query for drifters/moorings in pilot bbox | project (free account) |
| 3 | ADCP offshore Piran continuity + data access | NIB (Malačič) |
| 4 | NIB "Vida" buoy AWAC profile data | NIB MBP Piran |
| 5 | Gajšt et al. 2016 sample-level data | UNOVA / NIB authors |
| 6 | Official Slovenia maritime-boundary polygon for domain assignment | national gazette / marineregions |
| 7 | HFR longer-window subsets (90 d / 12 mo) per download plan | project decision (not launched) |

## 9. Reproducibility

- Code: `src/rheomarine_hfr/` (adapter + `simulate_qc_aware`),
  `scripts/run_hfr_m0_pilot.py` (`--qc-flags` added for S4).
- Inputs: `data/hfr/raw/*_7d.nc` (git-ignored; sha256 in each summary).
- Outputs: `results/hfr_pilot_audit*/` (baselines),
  `results/hfr_pilot_sensitivity/` (S1–S5).
- Tests: `PYTHONPATH=src python3 -m unittest discover -s tests -v`
  → 33 tests, OK (Python 3.10.12, numpy 2.2.6, scipy 1.15.3).
- Observation inventory: `docs/validation/hfr_pilot_candidate_observations.csv`
  (each row carries source URL, retrieval date 2026-11-25, access status
  and tier; rows marked UNVERIFIED have metadata verified but data not
  inspected).
