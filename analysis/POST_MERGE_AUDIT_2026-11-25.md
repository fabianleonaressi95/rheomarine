# Post-merge audit — 25 November 2026

## Scope
Audit of `scripts/analyze_ds1_settling.py`, `scripts/analyze_ds2_stratified.py`, their JSON/CSV outputs, and the corresponding README claims. This is an interpretation audit, not a re-run against the original raw files.

## DS1 — correction required in the headline
The implemented ratio is
`R_vs_AS = mean(w_solution) / mean(w_AS)`.
Therefore R < 1 means settling is slower than the AS baseline; R > 1 means faster.

For AS_XG1 the material-level means in `ds1_analysis_summary.json` are:
- POM: R = 0.2437
- PA: R = 0.0715
- PET: R = 0.0723
- PS: R = 0.0475

Thus POM is **less retarded** than PS/PET/PA, but it is not faster than its own AS baseline. Replace any wording such as “POM sinks 4–6× faster” with “POM retains about 24% of its AS-baseline settling speed and is less retarded than the other reported materials.” The exact factor relative to baseline is about 1/0.2437 = 4.1 times slower, not faster.

At AS_XG0.5, POM R = 0.5975 and PS R = 0.2407, again indicating weaker retardation for POM.

### DS1 qualifications
- The summary averages species/specification-level ratios with equal weight; it is not a particle-count-weighted population estimate.
- Only 14/15 specifications have dimensions available for AS_XG1; the C_* specifications lack dimension records.
- `S_PS` is sourced from the manufacturer specification in the dataset README, not camera measurement. The script currently labels it `measured`; change the provenance label to `manufacturer`.
- The z-unit calibration remains unresolved. Ratios within matched runs may cancel a common scale factor, but absolute settling velocities cannot be reported physically until calibration is established.
- The per-run ratio spread is a Cartesian pairing of all solution runs with all AS runs for a spec; it is descriptive, not a paired experimental uncertainty estimate.

## DS2 — interpretation and robustness
The current summary reports 108 trajectory records. Median below/above ratios by set are:
- set1_1 0.903; set1_2 0.754; set1_3 0.218
- set2_1 0.899; set2_2 0.710; set2_3 0.318
- set3_1 1.087; set3_2 1.369; set3_3 4.375

These values support a descriptive contrast between sets 1–2 and set 3 in the analyzed records. They do **not** establish that density contrast alone causes acceleration or retardation.

Open limitations:
1. The dataset README supplies interface bounds but not the set-to-fluid-composition mapping. The mapping must be checked against Mrokowska et al. (2025), Water Research 280, 123487, before assigning layer identities or interpreting an inverted configuration.
2. set3_3 has only 7 valid below/above ratios (the other sets generally have 11–12). Report this denominator wherever set3_3 is discussed.
3. The per-set aggregates pool particle types and both interrogation windows. They are not independent replicate counts and may hide particle-specific or IW-specific effects.
4. The density contrast is estimated from the first and last quartiles of rows in each fitted profile. Confirm that rows are ordered consistently by vertical coordinate; preferably sort explicitly by z and define top/bottom using z, not row position.
5. The script computes smoothed derivatives from averaged centroid trajectories. It should be described as a kinematic analysis of ensemble-averaged tracks, not single-particle instantaneous dynamics.
6. The current finite-value helper and missing-zone handling should be tested on all output rows; empty strings, NaNs, and zero/negative slopes can affect ratios.

## Recommended next analysis
1. Fix DS1 provenance for S_PS and correct the README headline.
2. Recompute DS2 density top/bottom after explicit sorting by z; verify coordinate orientation from the source metadata.
3. Produce DS2 tables stratified by set × IW × particle type, retaining n_above/n_below and excluding inadequate zone coverage under a predeclared rule.
4. Retrieve the set-to-fluid mapping and layer composition from the 2025 paper before attributing set3 behavior to a specific stratification.
5. Compare each set's density contrast, rheological measurements, interface thickness, and settling ratios jointly. Treat the result as a candidate empirical relationship, not a universal constitutive law.

## Safe claim for the RISTANC dossier
Published laboratory datasets indicate that polymer-rich fluids and stratified rheological interfaces can substantially alter microplastic settling, with effects that vary by polymer material, particle geometry, and layer configuration. The current re-analysis identifies candidate material- and configuration-dependent patterns; absolute velocity calibration, source-paper mapping, and independent validation remain necessary before quantitative transfer to the North Adriatic.
