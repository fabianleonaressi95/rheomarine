import unittest

import numpy as np

from rheomarine_hfr.trajectory import simulate_qc_aware
from rheomarine_transport import VelocityField


def field_with_mask(valid):
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([0.0, 1.0, 2.0])
    times = np.array([0.0, 1.0])
    velocity = np.zeros((2, 3, 3, 2))
    velocity[..., 0] = 1.0
    return VelocityField(x, y, times, velocity, valid)


class TestQCAwareTrajectory(unittest.TestCase):
    def test_invalid_endpoint_rejects_step_and_keeps_last_valid_position(self):
        valid = np.ones((2, 3, 3), dtype=bool)
        valid[1, 0, 2] = False
        field = field_with_mask(valid)
        initial = np.array([[0.5, 0.5]])
        final, alive, stopped = simulate_qc_aware(field, initial)
        np.testing.assert_allclose(final, initial)
        self.assertFalse(alive[0])
        self.assertTrue(stopped[0])

    def test_valid_endpoint_commits_advected_position(self):
        valid = np.ones((2, 3, 3), dtype=bool)
        field = field_with_mask(valid)
        initial = np.array([[0.5, 0.5]])
        final, alive, stopped = simulate_qc_aware(field, initial)
        np.testing.assert_allclose(final, [[1.5, 0.5]])
        self.assertTrue(alive[0])
        self.assertFalse(stopped[0])

    def test_invalid_start_stencil_stops_without_advancing(self):
        valid = np.ones((2, 3, 3), dtype=bool)
        valid[0, 0, 1] = False
        field = field_with_mask(valid)
        initial = np.array([[0.5, 0.5]])
        final, alive, stopped = simulate_qc_aware(field, initial)
        np.testing.assert_allclose(final, initial)
        self.assertFalse(alive[0])
        self.assertTrue(stopped[0])

    def test_empty_particle_cohort(self):
        valid = np.ones((2, 3, 3), dtype=bool)
        final, alive, stopped = simulate_qc_aware(
            field_with_mask(valid), np.empty((0, 2))
        )
        self.assertEqual(final.shape, (0, 2))
        self.assertEqual(alive.size, 0)
        self.assertEqual(stopped.size, 0)


if __name__ == "__main__":
    unittest.main()
