"""QC-aware Lagrangian stepping for HFR-forced particles.

A step is accepted only when the bilinear interpolation stencil is valid
at the observed start, at every grid cell touched by the advected path,
and at the advected endpoint of the interval. Cell traversal is exact
(conservative DDA over the rectilinear grid), not a fixed sampling
density. Rejected steps leave the particle at its last accepted
position.
"""
from __future__ import annotations

import numpy as np

from rheomarine_transport import VelocityField, simulate_m0

_EPS = 1e-9


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


def _cell_index(coord: float, axis: np.ndarray) -> int:
    """Cell index containing ``coord`` on a node axis (clamped to edges)."""
    i = int(np.searchsorted(axis, coord, side="right")) - 1
    return min(max(i, 0), axis.size - 2)


def _cells_on_segment(field: VelocityField, p0, p1) -> set[tuple[int, int]]:
    """All grid cells (iy, ix) touched by the closed segment p0->p1.

    Conservative traversal: the segment is split at every crossing of an
    interior grid line; each open sub-interval contributes its containing
    cell, and every event point (grid-line/vertex touch, including exact
    grazes) contributes ALL cells adjacent to that point, so a path
    running exactly along an edge or corner cannot slip through.
    """
    x, y = field.x, field.y
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    cells: set[tuple[int, int]] = set()

    # event parameters t in [0,1] where the path crosses a grid line
    ts = {0.0, 1.0}
    for k in range(1, x.size - 1):
        if abs(dx) > _EPS:
            t = (x[k] - p0[0]) / dx
            if -_EPS <= t <= 1 + _EPS:
                ts.add(min(max(t, 0.0), 1.0))
    for l in range(1, y.size - 1):
        if abs(dy) > _EPS:
            t = (y[l] - p0[1]) / dy
            if -_EPS <= t <= 1 + _EPS:
                ts.add(min(max(t, 0.0), 1.0))
    ts = sorted(ts)

    # midpoint of each open sub-interval -> its unique cell
    for a, b in zip(ts[:-1], ts[1:]):
        if b - a <= _EPS:
            continue
        tm = 0.5 * (a + b)
        px, py = p0[0] + tm * dx, p0[1] + tm * dy
        cells.add((_cell_index(py, y), _cell_index(px, x)))

    # each event point: all cells adjacent to the touched grid feature
    for t in ts:
        px, py = p0[0] + t * dx, p0[1] + t * dy
        ix_cands = {_cell_index(px, x)}
        iy_cands = {_cell_index(py, y)}
        for k in range(1, x.size - 1):
            if abs(px - x[k]) <= _EPS * max(1.0, abs(x[k])):
                ix_cands |= {_cell_index(px - _EPS, x),
                             _cell_index(px + _EPS, x)}
        for l in range(1, y.size - 1):
            if abs(py - y[l]) <= _EPS * max(1.0, abs(y[l])):
                iy_cands |= {_cell_index(py - _EPS, y),
                             _cell_index(py + _EPS, y)}
        for iy in iy_cands:
            for ix in ix_cands:
                if 0 <= iy < y.size - 1 and 0 <= ix < x.size - 1:
                    cells.add((iy, ix))
    return cells


def _path_clear(
    field: VelocityField,
    start: np.ndarray,
    end: np.ndarray,
    it0: int,
    it1: int,
) -> np.ndarray:
    """Exact pathwise QC check via grid-cell traversal.

    Forward Euler produces a straight path per interval. Every cell the
    segment touches must have all four corner nodes QC-valid at BOTH
    bracketing observation times (conservative: the field is only defined
    at observations). Returns one bool per particle; True = path fully
    supported. No sampling density is involved, so grazing corner
    crossings cannot evade the check.
    """
    p0 = np.asarray(start, dtype=float)
    p1 = np.asarray(end, dtype=float)
    if p0.size == 0:
        return np.zeros(0, dtype=bool)
    ok = np.ones(len(p0), dtype=bool)
    for n in range(len(p0)):
        for iy, ix in _cells_on_segment(field, p0[n], p1[n]):
            corners = (field.valid[it0, iy, ix] & field.valid[it0, iy, ix + 1]
                       & field.valid[it0, iy + 1, ix] & field.valid[it0, iy + 1, ix + 1]
                       & field.valid[it1, iy, ix] & field.valid[it1, iy, ix + 1]
                       & field.valid[it1, iy + 1, ix] & field.valid[it1, iy + 1, ix + 1])
            if not corners:
                ok[n] = False
                break
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
