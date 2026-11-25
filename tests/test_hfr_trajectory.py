import unittest

import numpy as np

from rheomarine_hfr.trajectory import _cells_on_segment, simulate_qc_aware
from rheomarine_transport import VelocityField


def field_with_mask(valid, u=1.0, times=None):
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([0.0, 1.0, 2.0])
    if times is None:
        times = np.array([0.0, 1.0])
    velocity = np.zeros((len(times), 3, 3, 2))
    velocity[..., 0] = u
    return VelocityField(x, y, times, velocity, valid)


class TestQCAwareTrajectory(unittest.TestCase):
    def test_invalid_endpoint_rejects_step_and_keeps_last_valid_position(self):
        valid = np.ones((2, 3, 3), dtype=bool)
        valid[1, 0, 2] = False
        field = field_with_mask(valid)
        initial = np.array([[0.5, 0.5]])
        final, alive, stopped, exited = simulate_qc_aware(field, initial)
        np.testing.assert_allclose(final, initial)
        self.assertFalse(alive[0])
        self.assertTrue(stopped[0])
        self.assertFalse(exited[0])

    def test_valid_endpoint_commits_advected_position(self):
        valid = np.ones((2, 3, 3), dtype=bool)
        field = field_with_mask(valid)
        initial = np.array([[0.5, 0.5]])
        final, alive, stopped, exited = simulate_qc_aware(field, initial)
        np.testing.assert_allclose(final, [[1.5, 0.5]])
        self.assertTrue(alive[0])
        self.assertFalse(stopped[0])
        self.assertFalse(exited[0])

    def test_invalid_start_stencil_stops_without_advancing(self):
        valid = np.ones((2, 3, 3), dtype=bool)
        valid[0, 0, 1] = False
        field = field_with_mask(valid)
        initial = np.array([[0.5, 0.5]])
        final, alive, stopped, exited = simulate_qc_aware(field, initial)
        np.testing.assert_allclose(final, initial)
        self.assertFalse(alive[0])
        self.assertTrue(stopped[0])
        self.assertFalse(exited[0])

    def test_path_crossing_invalid_cell_rejected_despite_valid_endpoints(self):
        # 5x3 node grid; node (iy=1, ix=2) invalid at both times.
        # Particle at (0.5,0.5) advects +3 in x to (3.5,0.5): start and
        # endpoint stencils exclude node ix=2, but the straight path
        # crosses its zone x in (1,3) where it is a stencil corner.
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
        y = np.array([0.0, 1.0, 2.0])
        times = np.array([0.0, 1.0])
        velocity = np.zeros((2, 3, 5, 2))
        velocity[..., 0] = 3.0
        valid = np.ones((2, 3, 5), dtype=bool)
        valid[:, 1, 2] = False
        field = VelocityField(x, y, times, velocity, valid)
        final, alive, stopped, exited = simulate_qc_aware(
            field, np.array([[0.5, 0.5]]))
        np.testing.assert_allclose(final, [[0.5, 0.5]])
        self.assertFalse(alive[0])
        self.assertTrue(stopped[0])
        self.assertFalse(exited[0])

    def test_grazing_corner_crossing_rejected_by_exact_traversal(self):
        # Adversarial case for a *sampled* pathwise check: node (2,2) is
        # invalid at both times; its stencil zone is the square
        # x,y in (1,3). The path from (0.95,1.1) to (1.1,0.95) clips only
        # the corner of that zone near (1,1) -- a sub-cell excursion that
        # a fixed sampling density could miss between samples. Both
        # endpoint stencils exclude node (2,2), so only the pathwise
        # check can reject the step.
        x = y = np.array([0.0, 1.0, 2.0, 3.0])
        times = np.array([0.0, 1.0])
        velocity = np.zeros((2, 4, 4, 2))
        velocity[..., 0] = 0.15   # dx = +0.15 over dt = 1
        velocity[..., 1] = -0.15  # dy = -0.15 over dt = 1
        valid = np.ones((2, 4, 4), dtype=bool)
        valid[:, 2, 2] = False
        field = VelocityField(x, y, times, velocity, valid)

        # sanity: traversal must report the corner cell (iy=1, ix=1)
        cells = _cells_on_segment(field, np.array([0.95, 1.1]),
                                  np.array([1.1, 0.95]))
        self.assertIn((1, 1), cells)

        final, alive, stopped, exited = simulate_qc_aware(
            field, np.array([[0.95, 1.1]]))
        np.testing.assert_allclose(final, [[0.95, 1.1]])
        self.assertFalse(alive[0])
        self.assertTrue(stopped[0])
        self.assertFalse(exited[0])

    def test_path_along_grid_edge_adjacent_to_invalid_node_rejected(self):
        # Conservative edge handling: a path running exactly along the
        # grid line y=1 touches cells on BOTH sides (iy=0 and iy=1).
        # Node (0,1) is invalid at both times; it is a corner of cell
        # (iy=0, ix=0) on the "below" side of the edge, while both
        # endpoint stencils (rows iy={1,2}) stay clear of row 0 -- so
        # only the conservative traversal can reject this step.
        x = y = np.array([0.0, 1.0, 2.0, 3.0])
        times = np.array([0.0, 1.0])
        velocity = np.zeros((2, 4, 4, 2))
        velocity[..., 0] = 0.5   # dx = +0.5 over dt = 1, dy = 0
        valid = np.ones((2, 4, 4), dtype=bool)
        valid[:, 0, 1] = False
        field = VelocityField(x, y, times, velocity, valid)

        cells = _cells_on_segment(field, np.array([0.5, 1.0]),
                                  np.array([1.0, 1.0]))
        self.assertIn((0, 0), cells)
        self.assertIn((1, 0), cells)

        final, alive, stopped, exited = simulate_qc_aware(
            field, np.array([[0.5, 1.0]]))
        np.testing.assert_allclose(final, [[0.5, 1.0]])
        self.assertFalse(alive[0])
        self.assertTrue(stopped[0])
        self.assertFalse(exited[0])

    def test_absorb_boundary_marks_exited_not_qc_stopped(self):
        valid = np.ones((2, 3, 3), dtype=bool)
        field = field_with_mask(valid, u=5.0)
        # x domain [0,2]; start near right edge, u=5 -> exits in one step
        final, alive, stopped, exited = simulate_qc_aware(
            field, np.array([[1.9, 0.5]]), boundary="absorb")
        self.assertFalse(alive[0])
        self.assertFalse(stopped[0])
        self.assertTrue(exited[0])

    def test_empty_particle_cohort(self):
        valid = np.ones((2, 3, 3), dtype=bool)
        final, alive, stopped, exited = simulate_qc_aware(
            field_with_mask(valid), np.empty((0, 2))
        )
        self.assertEqual(final.shape, (0, 2))
        self.assertEqual(alive.size, 0)
        self.assertEqual(stopped.size, 0)
        self.assertEqual(exited.size, 0)


if __name__ == "__main__":
    unittest.main()
