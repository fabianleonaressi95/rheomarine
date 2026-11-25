# Independent audit of the first HFR–M0 pilot

**Audit date:** 25 November 2026  
**Audited baseline:** 9b1e79fc73171c2d389e88e034fa1dc3bd7a3e40  
**Scope:** trajectory QC stopping, reported displacement statistics, runtime dependency, and interpretation of the pilot window.

## Findings

### 1. Endpoint QC was not enforced in the original particle step

The original simulate_qc_aware checked the current particle stencil at the two bracketing time indices, but it did not check the advected endpoint position at the next timestamp. Thus a step could be committed even when the new position's interpolation stencil was QC-invalid. That contradicted the claim that every stored endpoint was fully QC-supported.

The audited implementation moves this logic into rheomarine_hfr.trajectory.simulate_qc_aware. It checks the start stencil, computes a trial forward-Euler step, checks the endpoint stencil at the next observed timestamp, and commits the step only if both checks pass. Otherwise it marks the particle qc_stopped and retains its last accepted position.

Four synthetic regression tests cover invalid endpoints, valid endpoints, invalid starts, and empty cohorts. This is an endpoint guard, not yet a continuous pathwise barrier test: a sufficiently long step could in principle cross an invalid cell and end in a valid stencil. A follow-up should substep or sample the path at a spatial resolution tied to grid spacing.

### 2. Displacement must be stratified by QC status

In the baseline driver, the median and maximum displacement were computed over the entire initial cohort, including particles stopped by QC and held at their last accepted position. These are useful cohort-level truncated-displacement summaries, but they are not the displacement distribution of trajectories that remain active.

The revised output therefore reports separately:
- displacement_active_median_m and displacement_active_max_m: active trajectories only; null when none remain;
- displacement_all_initial_median_m and displacement_all_initial_max_m: all initially released particles, including QC-stopped trajectories.

Existing JSON summaries on the baseline are historical outputs from the pre-audit algorithm. They must not be described as endpoint-QC-audited or as active-only displacement statistics. Regenerate them from the original NetCDF subsets after this branch is merged.

### 3. The reflecting boundary is a modelling assumption, not a coastline

The pilot crop is an automatically selected 4×4 grid-cell window. Reflecting particles at its perimeter imposes a closed-box boundary on an artificial computational window. It is not a physical shoreline condition and can retain particles that would otherwise leave the selected window. This must be treated as a sensitivity assumption; it is not evidence of retention in the sea.

### 4. SciPy is a runtime dependency of the HFR adapter

rheomarine_hfr.adapter imports scipy.io.netcdf_file at module import time. The package metadata previously declared NumPy only. The branch adds SciPy explicitly so a clean installation can import and use the adapter.

### 5. Reproducibility is not validation

The highest-coverage 4×4 block is a deterministic computational selection, not a geographically justified pilot polygon. The two sites' windows differ geographically. Results are conditional on this selection, the accepted QC flag policy, the 3-hour temporal segmentation threshold, the 8×8 release lattice, K=0, and the reflecting crop boundary.

The pilot demonstrates an executable processing chain on archived surface-current subsets. It does not establish predictive skill, particle concentration, vertical transport, settling, seabed deposition, or representativeness of the whole coastal region.

## Verification status

- Four new synthetic endpoint-QC regression tests are added.
- The baseline reported 25 passing tests, but this audit branch has not yet run the suite in a clean environment.
- The original raw NetCDF subsets are git-ignored and were not available in the repository tree for an independent rerun. The pilot JSON and hashes were inspected; the raw-input hashes cannot be recomputed without the source files.
- Do not treat the new pilot summaries as regenerated until the script is run against the exact archived inputs and the output hashes are checked.

## Next validation gate

1. Install the project from pyproject.toml in a clean environment.
2. Run the full unit suite.
3. Re-run IZOL and PIRA from the exact NetCDF files matching the recorded SHA-256 values.
4. Compare endpoint-QC attrition and active-only displacement with the baseline summaries.
5. Repeat with an open/absorbing crop boundary or a larger domain to quantify boundary sensitivity.
6. Add a pathwise QC barrier test (not only endpoint tests), with substeps bounded by grid spacing.
7. Only then use the pilot as a preliminary computational result in the project dossier.

## Resolution of the validation gate (same day, second pass)

All gate items were executed on this branch:

1. **Test suite run for real** — Python 3.10.12, numpy 2.2.6, scipy
   1.15.3. `PYTHONPATH=src python -m unittest discover -s tests -v`
   → **33 tests, OK** (25 baseline + 4 endpoint-QC + 2 pathwise/
   boundary + 2 exact-traversal adversarial). No test was declared
   passed without this log.
2. **Inputs verified** — `sha256sum data/hfr/raw/*_7d.nc` reproduces
   the baseline hashes exactly: IZOL
   `d37844f5f0f6c9844e3a585fd75d0b6e4ed0c3625d79f3cd492b5ad9c1adef5d`,
   PIRA `908ee53dc53ec65d272f89596a6a91ac75f8c1bd434dd6126d68a15e4aafc353`.
3. **Pathwise QC barrier implemented, then hardened** — `simulate_qc_aware` first substeps each accepted interval at ≤ half the smallest grid spacing (cap 32) and requires a fully valid stencil at every interior path point at both bracketing times. Post-merge review correctly noted this is a *sampled* check, not a continuous guarantee. The follow-up PR replaces it with exact segment→grid-cell traversal (`_cells_on_segment`): every cell the straight path touches — including all cells adjacent to exact edge/vertex grazes — must have all four corner nodes QC-valid at both bracketing times. Adversarial tests cover a sub-cell corner grazing that a fixed sampling density could miss, and a path running exactly along a grid edge. The start stencil is checked at both bracketing times (the engine interpolates velocity between them). `exited` (boundary removal) is now tracked separately from `qc_stopped`.
4. **Pilots regenerated** — outputs in `results/hfr_pilot_audit/`
   (block 4, reflect), `results/hfr_pilot_audit_block8/` (block 8,
   reflect), `results/hfr_pilot_audit_absorb/` (block 4, absorb).
   Baseline `results/hfr_pilot/` preserved untouched.
5. **Boundary sensitivity quantified** — under `absorb` essentially the
   entire cohort exits the 4×4 crop within days (IZOL 64/64 and PIRA
   64/64 exited in the longest segment); under the wider 8×8 window
   PIRA's longest segment loses all 27 released particles to QC.
   Reflecting-boundary results are closed-box sensitivity experiments,
   not coastal retention estimates.
6. **Active vs cohort displacement separated** — JSON now reports
   `displacement_active_*` (null when no particle remains) alongside
   `displacement_all_initial_*`.

### Regenerated headline numbers (longest segment, 70.5 h)

| Site | block/boundary | alive / qc_stopped / exited | active-only median displacement |
|------|----------------|------------------------------|----------------------------------|
| IZOL | 4, reflect | 64 / 0 / 0 | 3.34 km |
| IZOL | 8, reflect | 64 / 0 / 0 | 7.03 km |
| IZOL | 4, absorb  | 0 / 0 / 64 | — |
| PIRA | 4, reflect | 64 / 0 / 0 | 2.56 km |
| PIRA | 8, reflect | 0 / 27 / 0 | — |
| PIRA | 4, absorb  | 0 / 0 / 64 | — |

Remaining limitations: the pathwise check is now an *exact*
segment→cell traversal, but it certifies only the straight-line
Euler path per interval — it assumes the velocity is constant within
an interval (true for the K=0 forward-Euler step); under `reflect` a
path that would bounce off the artificial boundary is checked as a
straight line to the reflected endpoint — documented, not exact. The
4×4/8×8 windows remain computational selections, not validated pilot
polygons. Pilot outputs were regenerated once more after the
exact-traversal upgrade; longest-segment headline numbers are
unchanged, intermediate PIRA segments show slightly higher QC
attrition (e.g. seg 1: 26/13 vs 30/9 alive/stopped).
