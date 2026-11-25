import unittest

import numpy as np

from rheomarine_transport import VelocityField, simulate_m0


def constant_field(u=0.0, v=0.0, valid=None):
    x = np.linspace(0.0, 10.0, 11)
    y = np.linspace(0.0, 10.0, 11)
    times = np.array([0.0, 10.0])
    velocity = np.zeros((2, 11, 11, 2))
    velocity[..., 0] = u
    velocity[..., 1] = v
    return VelocityField(x, y, times, velocity, valid)


class TestM0(unittest.TestCase):
    def test_uniform_advection_matches_analytic_solution(self):
        field = constant_field(u=1.0, v=-0.5)
        result = simulate_m0(field, np.array([[2.0, 5.0]]),
                             start_time=0, end_time=2, dt=0.1,
                             boundary="reflect")
        np.testing.assert_allclose(result.final_positions, [[4.0, 4.0]], atol=1e-12)
        self.assertEqual(result.number_balance_residual, 0)

    def test_zero_flow_zero_diffusion_is_stationary(self):
        field = constant_field()
        initial = np.array([[2.0, 3.0], [8.0, 7.0]])
        result = simulate_m0(field, initial, start_time=0, end_time=3, dt=0.25)
        np.testing.assert_allclose(result.final_positions, initial, atol=0)
        self.assertEqual(result.active_count, 2)

    def test_absorbing_boundary_accounts_for_exit(self):
        field = constant_field(u=2.0)
        result = simulate_m0(field, np.array([[9.0, 5.0]]),
                             start_time=0, end_time=1, dt=0.5,
                             boundary="absorb")
        self.assertEqual(result.exited_count, 1)
        self.assertEqual(result.active_count, 0)
        self.assertEqual(result.number_balance_residual, 0)

    def test_reflecting_boundary_keeps_particles_in_domain(self):
        field = constant_field(u=3.0)
        result = simulate_m0(field, np.array([[9.0, 5.0]]),
                             start_time=0, end_time=1, dt=0.5,
                             boundary="reflect")
        self.assertTrue(np.all(result.final_positions >= 0))
        self.assertTrue(np.all(result.final_positions <= 10))

    def test_qc_invalid_stencil_fails_loudly(self):
        mask = np.ones((2, 11, 11), dtype=bool)
        mask[:, 5, 5] = False
        field = constant_field(valid=mask)
        with self.assertRaisesRegex(ValueError, "QC-invalid"):
            field.sample(np.array([[5.0, 5.0]]), 1.0)

    def test_no_extrapolation_outside_hfr_time_coverage(self):
        field = constant_field()
        with self.assertRaisesRegex(ValueError, "outside forcing coverage"):
            field.sample(np.array([[5.0, 5.0]]), 11.0)


    def test_simulation_refuses_to_cross_large_observation_gap(self):
        x = np.linspace(0.0, 10.0, 11)
        y = np.linspace(0.0, 10.0, 11)
        times = np.array([0.0, 1.0, 10.0, 11.0])
        velocity = np.zeros((4, 11, 11, 2))
        field = VelocityField(x, y, times, velocity)
        with self.assertRaisesRegex(ValueError, "intersects an HFR forcing gap"):
            simulate_m0(field, np.array([[5.0, 5.0]]),
                        start_time=0.5, end_time=10.5, dt=1.0)

    def test_explicit_max_forcing_gap_can_be_configured(self):
        x = np.linspace(0.0, 10.0, 11)
        y = np.linspace(0.0, 10.0, 11)
        times = np.array([0.0, 1.0, 10.0, 11.0])
        velocity = np.zeros((4, 11, 11, 2))
        field = VelocityField(x, y, times, velocity)
        with self.assertRaisesRegex(ValueError, "intersects an HFR forcing gap"):
            simulate_m0(field, np.array([[5.0, 5.0]]),
                        start_time=1.0, end_time=10.0, dt=1.0,
                        max_forcing_gap=2.0)


    def test_direct_sampling_refuses_large_observation_gap(self):
        x = np.linspace(0.0, 10.0, 11)
        y = np.linspace(0.0, 10.0, 11)
        times = np.array([0.0, 1.0, 10.0, 11.0])
        velocity = np.zeros((4, 11, 11, 2))
        field = VelocityField(x, y, times, velocity)
        with self.assertRaisesRegex(ValueError, "lies in an HFR forcing gap"):
            field.sample(np.array([[5.0, 5.0]]), 5.0)

    def test_first_order_surface_loss_is_bookkept(self):
        field = constant_field()
        result = simulate_m0(field, np.repeat([[5.0, 5.0]], 1000, axis=0),
                             start_time=0, end_time=2, dt=0.1,
                             surface_loss_rate=100.0, seed=7)
        self.assertEqual(result.active_count, 0)
        self.assertEqual(result.surface_loss_count, 1000)
        self.assertEqual(result.number_balance_residual, 0)


if __name__ == "__main__":
    unittest.main()
