# DS2 v2 — notes on interpretation decisions (25 Nov 2026)

Response to `POST_MERGE_AUDIT_2026-11-25.md`. Script:
`scripts/analyze_ds2_stratified.py` (rewritten).

## 1. Set → fluid mapping: still not in the dataset

The Water Research paper (Mrokowska et al. 2025, 10.1016/j.watres.2025.123487)
is paywalled; no OA full text found (Unpaywall, Semantic Scholar, PW
repository behind Cloudflare). What IS documented:

- Mendeley dataset description: **6 experiments "XG-containing layer
  overlaid by the AS layer"** (AS on top, XG bottom) and **3 "AS layer
  overlaid by XG-containing layer"** (XG on top, AS bottom).
- The set3 series shows the inverted velocity signature (particles slow
  above the interface, fast below), matching the 3-experiment minority
  configuration. We therefore assign `set1*, set2* → AS_over_XG` and
  `set3* → XG_over_AS` with `confidence = inferred_not_paper_verified`.
- Exact recipes (AS salinity 35 vs 42, XG g/L) remain open. Density
  suggests set1 top ≈ AS35 (~1024), set3 top ≈ AS42 (~1030); set2 is
  intermediate (~1025). **Anomaly:** set3 bottom densities reach
  ~1037–1038 kg/m³ — far above AS42 (~1029) and not explainable by
  XG ≤ 1.5 g/L. Either a different/bottom recipe or a measurement
  artefact; must be checked against the paper.

## 2. IW1 vs IW2 — resolved

Splitting the two interrogation windows changed the picture completely:

- **IW1** tracks cross the interface: velocity decays (sets 1–2) or
  grows (set3) across the boundary. Zone analysis applies here.
- **IW2** tracks are ~uniform in speed and their median speed matches
  the IW1 *below-interface* speed within ~±25% for 8/9 sets
  (`iw_consistency` in the JSON). Interpretation: the second window
  samples only the lower layer; its z origin does not share the
  interface reference, so zone splitting is NOT applied (flag
  `lower_layer_window_no_zone_split`).
- The earlier "set3_3 n=7" problem was an artefact: edge-trimming of
  the smoothing window ate the short below-interface segment, and
  jittered/duplicated timestamps produced gradient spikes. Fixed by
  resampling z(t) onto a uniform grid (median dt) + edge-padded
  smoothing. All 6 IW1 set3_3 trajectories now have below-zone
  coverage (n_below 18–44).

## 3. Predeclared coverage rule

A below/above ratio is reported only when n_above ≥ 10 and n_below ≥ 10
samples survive trimming; otherwise the row is kept with
`insufficient_zone_coverage`. This removed a few IW1 tracks whose
windows start inside/below the upper boundary (e.g. set1_3 R_a/R_b) —
reported, not hidden.

## 4. Headline numbers (IW1, R = w_below / w_above)

| set | inferred config | Δρ (meas.) | R_below median |
|-----|-----------------|------------|----------------|
| set1_1 | AS/XG | +1.1 | 0.66 |
| set1_2 | AS/XG | +1.5 | 0.36 |
| set1_3 | AS/XG | +2.3 | 0.14 |
| set2_1 | AS/XG | +3.6 | 0.67 |
| set2_2 | AS/XG | +4.2 | 0.33 |
| set2_3 | AS/XG | +5.9 | 0.20 |
| set3_1 | XG/AS | +8.4 | 1.37 |
| set3_2 | XG/AS | +7.3 | 2.57 |
| set3_3 | XG/AS | +7.4 | 5.41 |

Within sets 1–2, retardation grows with Δρ and is stronger for rods
(R) than spheres (S) — consistent with the paper's claim that
rheology, not just density, drives the effect. Set3 shows the inverse
ordering (acceleration below), as expected if the viscous layer sits on
top. Per-particle table: `data/ds2_stratified/ds2_set_iw_particle_summary.csv`.

## 5. Still open

- Paper-verified set → recipe mapping (paywalled; ask authors or
  library access).
- Absolute z calibration ds1 (units look like metres, README says
  pixels).
- Rheological_data files exist for 6 solutions but cannot be assigned
  to sets without the mapping; viscosities should be joined once the
  paper table is available.
