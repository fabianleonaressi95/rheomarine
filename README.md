# rheomarine

Mathematical and computational modelling of microplastic transport,
biological aggregation and rheological effects in the North Adriatic
Sea — experimental data + analysis.

## Data sources (Mendeley Data, CC BY 4.0, IG PAS)

| Dir | Dataset | Content |
|-----|---------|---------|
| `data/ds1_rheology_settling/` | Mrokowska et al. 2024 — settling of MPs in mucus-rich water column | 722 PTV trajectories (`*_run_*.csv`: x,z,t,angle), 7 solutions (AS, XG, CR, XG+CR @ 0.5/1 g/L) × 15 particle types (S/D/R/B/C/I × PS/POM/PET/PA6); particle dimension CSVs; rheology files |
| `data/ds2_stratified/` | Mrokowska et al. 2025 — MPs sinking through rheologically stratified seawater | `MPs_sinking_dynamics` (9 experiments, two-layer AS↔XG), `Density_and_refractive_index_profiles`, `Rheological_data` (flow/amplitude/gelling), transition-interface positions in README |

## Analysis so far

`scripts/extract_settling_velocities.py` — terminal settling velocity `w_s`
(linear fit on last 40% of each trajectory) for all 722 runs:

- `data/ds1_rheology_settling/settling_velocities.csv` — one row per run
- `data/ds1_rheology_settling/settling_summary.json` — mean/std per
  solution × particle type × material × size

Headline: XG reduces `w_s` strongly and concentration-dependently
(AS 0.059 → XG1 0.013, −78%); carrageenan much weaker (−16% at 1 g/L);
XG+CR intermediate. Units of z are as-recorded (README claims pixels;
absolute calibration not in dataset — open item).

## Second-pass analyses

`scripts/analyze_ds1_settling.py` — joins velocities with measured
particle dimensions (14 dim files + S_PS from README; `C_*` specs have
no dimension data in the dataset) and computes the retardation factor
`R = w_fluid / w_AS` per solution × particle spec, aggregated by
solution/material/shape, plus orientation statistics (circular spread
of the projection angle, correlation with smoothed sinking speed) for
non-spherical particles:

- `data/ds1_rheology_settling/ds1_particle_dimensions.csv`
- `data/ds1_rheology_settling/ds1_retardation.csv`
- `data/ds1_rheology_settling/ds1_analysis_summary.json`

Findings: retardation is strongly **material-dependent** — at XG 1 g/L,
POM retains about 24% of its AS-baseline settling speed (R ≈ 0.24),
whereas PS/PET/PA retain roughly 5–7% (R ≈ 0.05–0.07). POM is therefore
less retarded than the other reported materials, but it is still slower
than its own AS baseline. At XG 0.5 g/L the ordering persists (POM
R≈0.60 vs PS R≈0.24). CR alone is weaker and shows the same broad
material ordering. These are equal-weight averages over available
particle specifications, not particle-count-weighted estimates.

`scripts/analyze_ds2_stratified.py` (v2) — resamples each ensemble-averaged
centroid track onto a uniform time grid (source timestamps are jittered),
splits IW1 tracks at the visible interface bounds into above / interface /
below zones, and reports IW2 as a lower-layer reference window. Density
profiles are explicitly sorted by z before computing layer densities:

- `data/ds2_stratified/ds2_interface_transit.csv` (108 trajectories,
  zone-coverage flags)
- `data/ds2_stratified/ds2_set_iw_particle_summary.csv` (set × IW ×
  particle-type medians)
- `data/ds2_stratified/ds2_interface_summary.json`
- `analysis/DS2_V2_NOTES.md` — interpretation decisions and caveats

Findings (IW1, `R = w_below/w_above`): sets 1–2 (inferred AS-over-XG)
show strong retardation growing with Δρ — set1_3 R≈0.14, set2_3
R≈0.20 — while set3 (inferred inverted XG-over-AS) shows acceleration
below the interface (R up to ≈5.4 in set3_3). IW2 speeds match the IW1
below-interface values within ~±25% for 8/9 sets, confirming IW2 samples
only the lower layer. Rods (R) are more affected than spheres (S) in
both regimes. Layer-order assignment is inferred from the Mendeley
dataset description (6× AS-over-XG, 3× XG-over-AS) plus the set3
velocity signature — **not** verified against the paywalled paper;
exact fluid recipes remain an open item, as does the anomalous set3
bottom density (~1038 kg/m³).

## Literature (`papers/`)

Reference papers on MP transport, aggregation and North Adriatic
rheology (see `papers/RheoMarine_Dossier_Unico.pdf`).
