import unittest

import numpy as np

from rheomarine_hfr import to_eulerian_forcing
from rheomarine_transport import VelocityField


def make_field(*, invalid_node=None, nonuniform=False):
    x = np.array([0.0, 100.0, 200.0, 300.0])
    y = np.array([0.0, 100.0, 200.0, 300.0])
    if nonuniform:
        x[2] = 215.0
    times = np.array([0.0, 10.0, 20.0])
    velocity = np.zeros((3, 4, 4, 2), dtype=float)
    velocity[..., 0] = np.array([0.1, 0.2, 0.3])[:, None, None]
    velocity[..., 1] = -0.05
    valid = np.ones((3, 4, 4), dtype=bool)
    if invalid_node is not None:
        ti, iy, ix = invalid_node
        valid[ti, iy, ix] = False
    return VelocityField(x, y, times, velocity, valid)


class TestHFRToEulerian(unittest.TestCase):
    def test_node_to_cell_conversion_and_metric_grid(self):
        forcing = to_eulerian_forcing(make_field())
        self.assertEqual((forcing.grid.nx, forcing.grid.ny), (3, 3))
        self.assertEqual(forcing.u.shape, (3, 3, 3))
        self.assertEqual(forcing.v.shape, (3, 3, 3))
        self.assertAlmostEqual(forcing.grid.dx, 100.0)
        self.assertAlmostEqual(forcing.grid.dy, 100.0)
        np.testing.assert_allclose(forcing.u[:, 1, 1], [0.1, 0.2, 0.3])
        np.testing.assert_allclose(forcing.v, -0.05)

    def test_time_interpolation_and_exact_observation_qc(self):
        forcing = to_eulerian_forcing(make_field(invalid_node=(1, 1, 1)))
        u0, v0, valid0 = forcing.sample(0.0)
        self.assertTrue(valid0.all())
        np.testing.assert_allclose(u0, 0.1)
        np.testing.assert_allclose(v0, -0.05)

        um, _, valid_mid = forcing.sample(5.0)
        self.assertAlmostEqual(um[0, 0], 0.15)
        self.assertFalse(valid_mid[0, 0])
        self.assertTrue(np.isnan(um[0, 0]))

    def test_no_temporal_extrapolation(self):
        forcing = to_eulerian_forcing(make_field())
        with self.assertRaises(ValueError):
            forcing.sample(-1.0)
        with self.assertRaises(ValueError):
            forcing.sample(21.0)
        with self.assertRaises(ValueError):
            forcing.step(np.ones((3, 3)), start_time_s=15.0, dt_s=10.0,
                         diffusivity=0.0)

    def test_qc_hole_fails_loudly_in_solver(self):
        forcing = to_eulerian_forcing(make_field(invalid_node=(1, 1, 1)))
        with self.assertRaisesRegex(ValueError, "must be finite"):
            forcing.step(np.ones((3, 3)), start_time_s=0.0, dt_s=10.0,
                         diffusivity=0.0)

    def test_end_to_end_hfr_to_eulerian_solver(self):
        field = make_field()
        field = VelocityField(field.x, field.y, field.times,
                              np.zeros_like(field.velocity), field.valid)
        forcing = to_eulerian_forcing(field)
        concentration = np.arange(9, dtype=float).reshape(3, 3) + 1.0
        result = forcing.step(concentration, start_time_s=0.0, dt_s=10.0,
                              diffusivity=0.0)
        np.testing.assert_allclose(result.concentration, concentration)
        self.assertAlmostEqual(result.mass_after, result.mass_before, places=10)

    def test_nonuniform_hfr_grid_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "uniformly spaced"):
            to_eulerian_forcing(make_field(nonuniform=True))


if __name__ == "__main__":
    unittest.main()
