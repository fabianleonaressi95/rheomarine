# HFR–M0 integration audit and execution boundary

**Branch:** `integration/hfr-m0-audit-morandotti`
**Scope:** inspect the existing HFR adapter and both transport implementations without changing the HFR download/ingestion pipeline.

## Findings from the current `main`

1. The HFR ingestion/audit package is already present under `src/rheomarine_hfr/`; it must not be duplicated.
2. `src/rheomarine_hfr/adapter.py` already reads ERDDAP NetCDF subsets, converts lon/lat to a local metric equirectangular grid, applies the strict default `QCflag == 1` mask, rejects fill/non-finite/out-of-envelope velocities, and splits time into contiguous segments.
3. Its output is `rheomarine_transport.VelocityField`, consumed by `simulate_m0` in `src/rheomarine_transport/m0.py`. This is the **Lagrangian particle engine**.
4. The repository also contains a distinct Eulerian finite-volume solver in `src/rheomarine_transport/grid.py` (`Grid2D`, `step_advection_diffusion`). That solver accepts instantaneous arrays `u,v` but currently has no HFR adapter, no QC mask argument, and no temporal forcing/provenance object. It must not be described as HFR-integrated.
5. The HFR adapter's existing tests cover metric coordinate conversion, QC policy, time segmentation, masks, and crop behaviour. The HFR trajectory pilots documented in `docs/hfr/M0_HFR_PILOT_2026-11-25.md` are K=0 Lagrangian path simulations, not runs of the Eulerian finite-volume advection–diffusion solver.

## Defect found and corrected on this branch

The NetCDF loader sorted the time coordinate but did not apply the same permutation to EWCT, NSCT and QCflag. If a file contained unsorted timestamps, the velocity/QC slices could silently be associated with the wrong times. The loader now sorts all four arrays together, retains the first occurrence of duplicate timestamps, and validates the expected singleton surface-depth and matching array shapes. A regression test constructs a synthetic NetCDF file with deliberately unsorted timestamps and checks that both velocity components and QC flags remain aligned.

## Remaining integration gates

- **Lagrangian M0:** adapter-to-`VelocityField` code path exists. This branch adds a loader-order regression test; a clean full-suite run is still required before marking it tested.
- **Eulerian finite-volume M0:** not integrated. A safe interface must define the target cell-centred grid, time interpolation, valid-cell policy, provenance and behaviour at QC holes. The current finite-volume solver has no wet/QC mask; silently replacing missing currents with zero or treating QC holes as impermeable coast would be scientifically unjustified.
- **Pilot:** raw NetCDF inputs are git-ignored and were not available in the repository tree through this audit. No new IZOL/PIRA pilot was regenerated on this branch.
- **Independent validation:** HFR QC fractions and numerical tests do not establish current-field accuracy or particle-transport skill. Independent ADCP/buoy/drifter comparison remains required.

## Safe next step for the Eulerian solver

Design a separate forcing contract (e.g. `HFRGridForcing`) that carries `Grid2D`, strictly increasing UTC/epoch times, `u(t,y,x)`, `v(t,y,x)`, a QC-valid mask, source/node identifiers, source units, projection metadata, and segment boundaries. Before implementing it, choose and test one explicit policy for cells invalid at a time slice. The default must be fail-closed; no zero fill, temporal gap bridging, or unlabelled impermeable-mask interpretation. Only after that contract is agreed should the finite-volume step accept masked forcing.

## Test status

The new regression test is committed in this branch but has **not** been executed in a Python environment in this session. No claim of passing tests or regenerated pilots is made. Required command:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```
