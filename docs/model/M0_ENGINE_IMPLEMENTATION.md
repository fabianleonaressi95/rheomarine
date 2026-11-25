# M0 transport engine — implementation note

**Status:** first executable implementation; numerical verification tests are
provided but must be run in a Python environment before this branch is merged.
**Scope:** independent Lagrangian surface advection–diffusion engine. No HFR
ingestion, download, decoding, calibration or mutation is performed here.

## Interface contract

The transport package consumes a `VelocityField` constructed by the upstream
HFR adapter:

- `x`, `y`: strictly increasing 1-D coordinate arrays;
- `times`: strictly increasing numeric timestamps;
- `velocity`: finite array of shape `(nt, ny, nx, 2)`, components ordered
  `(u, v)`;
- `valid`: optional boolean QC mask of shape `(nt, ny, nx)`.

The adapter is responsible for converting coordinates, timestamps and velocity
to a single documented unit system. The transport engine performs no implicit
unit conversion, temporal gap filling, extrapolation or QC repair. A sample whose
bilinear stencil touches an invalid cell raises an error. Temporal interpolation
is rejected when bracketing observations are separated by more than 1.5 median
sampling intervals by default; callers may provide an explicitly justified
`max_forcing_gap`. Integration steps intersecting a larger gap fail rather than
bridging it.

## Numerical method

Particles are advanced with Euler–Maruyama:

```text
X(t+dt) = X(t) + u(X,t) dt + sqrt(2 dt) L ξ,
L Lᵀ = K,  ξ ~ N(0,I).
```

The diffusivity `K` may be an isotropic scalar or symmetric positive
semidefinite 2×2 tensor. Velocity is bilinearly interpolated in space and
linearly in time. The time step is shortened for the final interval so that
the requested end time is reached exactly.

Two explicit horizontal boundary policies are implemented: reflection and
absorption/domain exit. An optional first-order surface-layer loss hazard
`lambda` removes particles with probability `1-exp(-lambda dt)` per step.
This is a modelled loss from the defined surface layer, not a claim of
measured seabed deposition. M0 defaults to zero loss unless the caller supplies
a documented parameter.

## Outputs and invariants

The result includes initial/final positions, active and exited masks, a
position history, time vector and counts for initial, active, exited and
surface-loss particles. The invariant is

```text
N_initial = N_active + N_exited + N_surface_loss.
```

The invariant is checked by `number_balance_residual == 0`. Absorbed particles
remain at their last in-domain position in the history; inactive history
entries are not interpreted as continued trajectories.

## Verification tests

Run from the repository root:

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

The tests cover constant-velocity analytic advection, zero-flow stationarity,
absorbing and reflecting boundaries, strict QC-mask behaviour, no temporal
extrapolation, rejection of direct sampling and integration across large HFR
gaps, and first-order loss bookkeeping. These are code-verification tests, not
observational validation of coastal transport. The expanded suite has not yet
been executed in this editing session; passing status must be established by a
real Python test run before merge.

## HFR handoff

The upstream HFR integration should call the public constructor and pass the
resulting `VelocityField` to `simulate_m0`. The engine is not coupled to
Devin's filenames, data structures or ingestion code. The adapter mapping
should be added only after its actual output schema is inspected and agreed.
