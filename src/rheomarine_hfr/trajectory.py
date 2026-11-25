"""QC-aware Lagrangian stepping for HFR-forced particles.

A step is accepted only when the bilinear interpolation stencil is valid
at the observed start, at every interior point of the advected path, and
at the advected endpoint of the interval. Rejected steps leave the
particle at its last accepted position.
"""
from __future__ import annotations

import numpy as np

from rheomarine_transport import VelocityField, simulate_m0

# pathwise QC check resolves the straight-line step at sub-cell spacing;
# steps whose required subdivision exceeds this cap are unverifiable and
# the particle is stopped rather than trusted blindly
MAX_PATH_SUBSTEPS = 32
PATH_EDGE_FRACTION = 0.5  # substep target <= half the smallest grid spacing


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


def _path_clear(
    field: VelocityField,
    start: np.ndarray,
    end: np.ndarray,
    it0: int,
    it1: int,
) -> np.ndarray:
    """True where the straight advected path stays inside valid stencils.

    Forward Euler produces a straight path per interval, so the check
    samples interior points at a spacing tied to the grid: each interior
    point must have a fully valid bilinear stencil at BOTH bracketing
    observation times (conservative: the field is only defined at
    observations). Steps needing more than MAX_PATH_SUBSTEPS are treated
    as unverifiable and rejected.
    """
    p0 = np.asarray(start, dtype=float)
    p1 = np.asarray(end, dtype=float)
    if p0.size == 0:
        return np.zeros(0, dtype=bool)
    dx_min = float(np.min(np.diff(field.x)))
    dy_min = float(np.min(np.diff(field.y)))
    spacing = min(dx_min, dy_min)
    dist = np.linalg.norm(p1 - p0, axis=1)
    need = np.ceil(dist / (PATH_EDGE_FRACTION * spacing)).astype(int)
    ok = need <= MAX_PATH_SUBSTEPS
    n_sub = int(need[ok].max()) if np.any(ok) else 1
    n_sub = max(n_sub, 1)
    for k in range(1, n_sub):
        frac = k / n_sub
        mid = p0 + frac * (p1 - p0)
        ok &= _stencil_valid(field, mid, it0) & _stencil_valid(field, mid, it1)
    return ok


def simulate_qc_aware(
    field: VelocityField,
    initial_positions: np.ndarray,
    *,
    seed: int = 42,
    boundary: str = "reflect",
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Advance on observed intervals without accepting QC-unsupported steps.

    Returns (final_positions, alive, qc_stopped, exited). A particle is
    ``qc_stopped`` when a step is rejected for missing QC support, and
    ``exited`` when the boundary policy removes it from the domain;
    the two causes are never conflated. In all cases the stored position
    remains the last accepted in-domain position. The integration is
    deterministic forward Euler (K=0), one observed forcing interval per
    step; no interpolation crosses time
    gaps because callers pass a single contiguous VelocityField segment.

    ``boundary`` is forwarded to the engine ("reflect" or "absorb"); it
    is a computational closure on the cropped window, not a coastline.
    """
    pos = np.asarray(initial_positions, dtype=float).copy()
    if pos.ndim != 2 or pos.shape[1] != 2 or not np.all(np.isfinite(pos)):
        raise ValueError("initial_positions must be a finite (n, 2) array")
    n = len(pos)
    alive = np.ones(n, dtype=bool)
    qc_stopped = np.zeros(n, dtype=bool)
    exited = np.zeros(n, dtype=bool)

    for i in range(len(field.times) - 1):
        ids = np.flatnonzero(alive)
        if ids.size == 0:
            break
        t_i = float(field.times[i])
        t_j = float(field.times[i + 1])

        # the engine samples velocity interpolated between the two
        # bracketing times, so the start stencil must be valid at both
        start_ok = (_stencil_valid(field, pos[ids], i)
                    & _stencil_valid(field, pos[ids], i + 1))
        rejected = ids[~start_ok]
        alive[rejected] = False
        qc_stopped[rejected] = True
        ids = ids[start_ok]
        if ids.size == 0:
            continue

        step = simulate_m0(
            field, pos[ids], start_time=t_i, end_time=t_j,
            dt=t_j - t_i, diffusivity=0.0, boundary=boundary, seed=seed,
        )
        trial = step.final_positions
        # domain exit under the boundary policy is tracked separately
        # from QC rejection and takes precedence over it
        gone = step.exited
        exited_ids = ids[gone]
        exited[exited_ids] = True
        alive[exited_ids] = False

        # Do not commit a step whose advected endpoint touches a bad cell.
        endpoint_ok = _stencil_valid(field, trial, i + 1)
        # ...nor one whose straight path crosses a QC-invalid stencil,
        # even when both endpoints are valid.
        path_ok = _path_clear(field, pos[ids], trial, i, i + 1)
        commit_local = endpoint_ok & path_ok & ~gone
        rejected_local = ~(endpoint_ok & path_ok) & ~gone
        rejected = ids[rejected_local]
        alive[rejected] = False
        qc_stopped[rejected] = True
        accepted_local = np.flatnonzero(commit_local)
        pos[ids[accepted_local]] = trial[accepted_local]

    return pos, alive, qc_stopped, exited
