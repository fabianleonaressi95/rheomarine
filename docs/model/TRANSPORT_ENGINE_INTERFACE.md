# RheoMarine transport engine: implementation and HFR interface

Status: M0 numerical core implemented, including wet-cell masks, per-step active (QC-barrier) masks and open-boundary exchange in the Eulerian solver. HFR ingestion exposes both a QC-aware Lagrangian handoff and a cell-centred Eulerian handoff. This is a computational baseline, not a calibrated or validated coastal forecast model.

## Module layout
- `src/rheomarine_transport/grid.py`: conservative finite-volume surface advection–diffusion step on a uniform Cartesian grid.
- `src/rheomarine_transport/m0.py`: Lagrangian surface advection–diffusion engine.
- `src/rheomarine_hfr/adapter.py`: ERDDAP NetCDF loading, QC, metric coordinates and temporal segmentation.
- `src/rheomarine_hfr/eulerian.py`: conversion of HFR node velocities to finite-volume cell-centred forcing.
- `tests/test_hfr_eulerian.py`: HFR-to-Eulerian conversion and end-to-end numerical handoff tests.

## HFR → Eulerian handoff

The public API is:

```python
from rheomarine_hfr import load_erddap_netcdf, to_velocity_fields, to_eulerian_forcing

dataset = load_erddap_netcdf("IZOL_subset.nc")
segments = to_velocity_fields(dataset, max_gap_s=7200.0)
forcing = to_eulerian_forcing(segments[0])

result = forcing.step(
    concentration, start_time_s=forcing.times[0],
    dt_s=1800.0, diffusivity=K_h,
)
concentration = result.concentration
```

The conversion has explicit semantics:

1. Input HFR coordinates are the local equirectangular metric node axes produced by the existing adapter. Both axes must be uniformly spaced; nonuniform axes are rejected rather than approximated by a single `dx,dy`.
2. Each finite-volume cell is the quadrilateral between four adjacent HFR nodes. Cell-centred eastward and northward velocities are the arithmetic means of the four corner-node values. On this local equirectangular grid, east/north remain aligned with x/y.
3. A cell is valid only if all four corner nodes pass the HFR QC mask. At an exact observation time only that observation's mask is required; at an intermediate time both bracketing masks must be valid.
4. Time sampling is restricted to the supplied contiguous `VelocityField` segment. There is no extrapolation and no crossing of a temporal gap.
5. Invalid cell velocities become NaN at sampling time. Two explicit policies exist via the `qc_holes` argument of `EulerianHFRForcing.step`:
   - `"fail"` (default): NaN forcing reaches the solver and is rejected on any active cell — the historical fail-closed behaviour requiring a fully QC-supported rectangular subdomain.
   - `"barrier"`: QC-invalid cells become zero-flux barriers for that step through the solver's `active` mask. Tracer mass inside a hole is retained unchanged and resumes when QC support returns; no interpolation or zero-fill is performed. A QC hole is treated as a temporary barrier, not as observed still water.
6. `wet` (static land mask) and `open_edges` may be forwarded to the solver; see "Masks and boundaries" below.

`EulerianHFRForcing.step` samples the velocity at the temporal midpoint of the requested step and delegates to `step_advection_diffusion`. The requested interval must lie entirely inside the segment. The solver's explicit stability check remains active by default.

## Solver inputs and units
| Input | Shape / units | Meaning |
|---|---|---|
| `u`, `v` | (ny,nx), m s-1 | eastward/northward surface velocity at cell centres |
| `concentration` | (ny,nx) | surface-layer concentration |
| `diffusivity` | scalar or (ny,nx), m2 s-1 | horizontal diffusivity |
| `dt` | seconds | time step |
| `Grid2D` | nx, ny, dx, dy | projected metric finite-volume grid |

## Masks and boundaries (`step_advection_diffusion`)

Optional keyword arguments, all off by default:

| Argument | Semantics |
|---|---|
| `wet` | Static (ny,nx) boolean water mask. `False` cells are land: they must carry exactly zero concentration, every face flux touching them is identically zero (no-flux coastline condition), and source/sink are not applied. Non-finite forcing is permitted on land cells only. |
| `active` | Per-step (ny,nx) boolean mask combined as `wet & active`. A wet-but-inactive cell is isolated for that step: all incident face fluxes are zero, so its tracer mass is retained unchanged and resumes when the mask lifts. This is the conservative QC-hole barrier used by `qc_holes="barrier"`. |
| `open_edges` | Subset of `{"west","east","south","north"}` replacing zero-normal-flux on those sides. The open face uses the boundary cell's velocity and concentration (zero-gradient, first-order upwind) for advection and carries **zero diffusive flux**. Mass is not closed; the net mass leaving the domain is reported as `TransportResult.boundary_loss_mass` (positive = loss). |

Rules that never change:

- Velocities, diffusivity, source and sink must be finite on every active cell; non-finite values are allowed only where `wet & active == False` and are treated as absent, never as zero.
- Concentration must be finite and non-negative everywhere; land cells must be exactly zero — a nonzero value on land raises instead of being silently discarded.
- Unknown `open_edges` names and wrongly shaped masks raise `ValueError`.
- With all defaults (`wet=None, active=None, open_edges=()`), behaviour is identical to the original closed-box solver.

The zero-gradient open boundary is a documented first-order closure, not a validated open-ocean condition: it assumes the exterior concentration equals the boundary-cell value and neglects diffusive exchange. It is appropriate for sensitivity experiments, not for claiming coastal retention or export skill.

## Numerical method and boundaries
- First-order upwind advective face fluxes; centred diffusive face fluxes.
- Finite-volume flux divergence; all outer boundaries have zero normal flux unless listed in `open_edges`.
- Explicit advection/diffusion stability bound via `stability_timestep` (masked to active cells when masks are used).
- Materially negative post-transport states raise an error rather than being silently clipped.
- Optional source (concentration s-1) and first-order sink (s-1); sink is integrated exponentially on participating cells only.
- Budget: `mass_after = mass_before + source_mass - sink_mass - boundary_loss_mass`, up to floating-point roundoff.

The grid is a uniform Cartesian metric grid (the local equirectangular projection from the HFR adapter). Spherical metric terms, nonuniform grids, wet/dry fronts and two-way nested boundaries are not implemented; coastline geometry must be supplied by the caller as a `wet` mask derived from an authoritative source, not inferred from QC holes.

## M1 particle properties
`ParticleClass` stores diameter, density, and optional signed settling velocity. `stokes_settling_velocity` is a spherical low-Reynolds-number reference estimate (positive downward, negative upward). It must not be applied blindly to irregular particles, aggregates, or regimes outside Stokes assumptions. Missing empirical properties remain missing.

This initial M1 layer does not implement aggregation kinetics, biofouling transitions, or a vertical water-column model. A surface-layer loss closure requires a declared layer thickness and justified vertical-mixing assumptions; it is not a measurement of seabed deposition.

## Tests
Run:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

The Eulerian adapter tests cover node-to-cell conversion, uniform metric spacing, time interpolation, exact-time QC handling, rejection of temporal extrapolation, fail-closed QC holes, and an end-to-end HFR-to-solver zero-flow benchmark. `tests/test_eulerian_boundaries.py` additionally covers wet-cell no-flux behaviour, land-concentration rejection, isolated-cell mass retention, the QC-barrier policy end-to-end through `EulerianHFRForcing.step`, open-boundary mass export with `boundary_loss_mass` accounting, the exact-translation manufactured check at Courant number 1, and rejection of invalid mask/edge configurations. Passing these tests verifies software behaviour on synthetic data; it does not validate the physical model against independent observations.

## Before coastal pilot use
1. Supply an authoritative coastline/wet-cell mask; do not infer land from QC holes.
2. Choose boundary conditions per edge (`open_edges`) from the pilot design and report `boundary_loss_mass`; reflect/absorb-style closures remain sensitivity experiments.
3. Decide the QC-hole policy explicitly per run (`fail` vs `barrier`) and report which was used.
4. Validate grid metrics and the equirectangular approximation for the selected domain.
5. Archive original vector NetCDFs, queries and hashes for IZOL/PIRA pilot reproducibility.
6. Compare against independent drifter/ADCP observations on held-out periods before claiming predictive skill.
