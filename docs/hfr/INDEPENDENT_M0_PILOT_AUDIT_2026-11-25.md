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
