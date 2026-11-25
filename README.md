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
PS/PET/PA particles are nearly arrested (R ≈ 0.04–0.20) while POM
sinks ~4–6× faster relative to its AS baseline (R ≈ 0.24–0.29);
irregular (I) particles are the least affected shape. At XG 0.5 g/L
the ordering persists (POM R≈0.60 vs PS R≈0.24). CR alone is much
weaker and shows the same material ordering.

`scripts/analyze_ds2_stratified.py` — splits each averaged centroid
trajectory at the visible interface bounds (from
`README_MPs_sinking_dynamics.txt`) into above / interface / below zones
and computes median sinking speed per zone, plus the density contrast
Δρ across the interface from the tanh-fitted density profiles:

- `data/ds2_stratified/ds2_interface_transit.csv` (108 trajectories)
- `data/ds2_stratified/ds2_interface_summary.json`

Findings: particles crossing into the lower layer are retarded by a
factor that grows with Δρ — set1_3 (Δρ≈+2.3 kg/m³) R_below≈0.22,
set2_3 (Δρ≈+5.9) R_below≈0.32 — while the set3 series (largest Δρ,
≈+7–8 kg/m³) shows R_below > 1 (up to ~4), i.e. particles accelerate
below the interface, consistent with an inverted (AS-over-XG)
configuration where the viscous layer sits on top. The exact
set → fluid-pair mapping is only in the source paper
(Mrokowska et al. 2025, Water Res. 280:123487), not in the dataset
files — open item.

## Literature (root PDFs)

Reference papers on MP transport, aggregation and North Adriatic
rheology uploaded alongside this analysis (see `RheoMarine_Dossier_Unico.pdf`).
