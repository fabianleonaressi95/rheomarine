"""QC-aware Lagrangian stepping for HFR-forced particles.

A step is accepted only when the bilinear interpolation stencil is valid
at both the observed start and the advected endpoint of the interval.
Rejected steps leave the particle at its last accepted position.
"""
from __future__ import annotations

import numpy as np

from rheomarine_transport import VelocityField, simulate_m0


def _stencil_valid(field: VelocityField, positions: np.ndarray, time_index: int) -> np.ndarray:
    """Return per-particle validity of the bilinear stencil at one time index."""
    p = np.asarray(positions, dtype=float)
    if p.size == 0:
        return np.zeros(0, dtype=bool)
    inside = ((p[:, 0] >= field.x[0]) & (p[:, 0] <= field.x[-1])
              & (p[:, 1] >= field.y[0]) & (p[:, 1] <= field.y[-1]))
    ok = inside.copy()
    if field.valid is None:
        return ok
    ix1 = np.clip(np.searchsorted(field.x, p[:, 0], side="right"), 1, len(field.x) - 1)
    iy1 = np.clip(np.searchsorted(field.y, p[:, 1], side="right"), 1, len(field.y) - 1)
    ix0, iy0 = ix1 - 1, iy1 - 1
    for dx in (0, 1):
        for dy in (0, 1):
            ok &= field.valid[time_index, iy0 + dy, ix0 + dx]
    return ok


def simulate_qc_aware(
    field: VelocityField,
    initial_positions: np.ndarray,
    *,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Advance on observed intervals without accepting QC-unsupported endpoints.

    Returns (final_positions, alive, qc_stopped). A particle is stopped
    before an interval if its current stencil is invalid, or after a trial
    step if the endpoint stencil at the next observation is invalid. In
    either case its stored position remains the last accepted position.
    The integration is deterministic forward Euler (K=0), one observed
    forcing interval per step; no interpolation crosses time gaps because
    callers pass a single contiguous VelocityField segment.
    """
    pos = np.asarray(initial_positions, dtype=float).copy()
    if pos.ndim != 2 or pos.shape[1] != 2 or not np.all(np.isfinite(pos)):
        raise ValueError("initial_positions must be a finite (n, 2) array")
    n = len(pos)
    alive = np.ones(n, dtype=bool)
    qc_stopped = np.zeros(n, dtype=bool)

    for i in range(len(field.times) - 1):
        ids = np.flatnonzero(alive)
        if ids.size == 0:
            break
        t_i = float(field.times[i])
        t_j = float(field.times[i + 1])

        start_ok = _stencil_valid(field, pos[ids], i)
        rejected = ids[~start_ok]
        alive[rejected] = False
        qc_stopped[rejected] = True
        ids = ids[start_ok]
        if ids.size == 0:
            continue

        trial = simulate_m0(
            field, pos[ids], start_time=t_i, end_time=t_j,
            dt=t_j - t_i, diffusivity=0.0, boundary="reflect", seed=seed,
        ).final_positions

        # Do not commit a step whose advected endpoint touches a bad cell.
        endpoint_ok = _stencil_valid(field, trial, i + 1)
        rejected = ids[~endpoint_ok]
        alive[rejected] = False
        qc_stopped[rejected] = True
        accepted = ids[endpoint_ok]
        pos[accepted] = trial[endpoint_ok]

    return pos, alive, qc_stopped
