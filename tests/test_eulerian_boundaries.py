import unittest

import numpy as np

from rheomarine_transport import Grid2D, step_advection_diffusion
from rheomarine_hfr import to_eulerian_forcing
from rheomarine_transport import VelocityField


def small_grid():
    return Grid2D(nx=6, ny=4, dx=100.0, dy=100.0)


def blob(shape=(4, 6)):
    c = np.zeros(shape)
    c[1:3, 2:4] = 1.0
    return c


class TestWetMask(unittest.TestCase):
    def setUp(self):
        self.grid = small_grid()
        self.c = blob()
        self.u = np.full((4, 6), 0.05)
        self.v = np.zeros((4, 6))
        self.wet = np.ones((4, 6), dtype=bool)
        self.wet[:, 4:] = False  # land on the east side

    def test_no_flux_into_land_and_mass_conserved(self):
        k = np.zeros((4, 6))
        r1 = step_advection_diffusion(self.c, self.u, self.v, k, 100.0,
                                      self.grid, wet=self.wet)
        # land cells stay exactly zero
        self.assertTrue(np.all(r1.concentration[:, 4:] == 0.0))
        # mass cannot cross the coastline: identical to a narrowed domain
        # where the last wet column is a closed boundary
        r2 = step_advection_diffusion(self.c[:, :4], self.u[:, :4],
                                      self.v[:, :4], k[:, :4], 100.0,
                                      Grid2D(nx=4, ny=4, dx=100.0, dy=100.0))
        np.testing.assert_allclose(r1.concentration[:, :4], r2.concentration,
                                   atol=1e-12)
        self.assertAlmostEqual(r1.mass_after, r1.mass_before, places=10)
        self.assertEqual(r1.boundary_loss_mass, 0.0)

    def test_concentration_on_land_rejected(self):
        bad = self.c.copy()
        bad[0, 5] = 1.0
        with self.assertRaisesRegex(ValueError, "wet == False"):
            step_advection_diffusion(bad, self.u, self.v, 0.0, 100.0,
                                     self.grid, wet=self.wet)

    def test_nan_forcing_allowed_only_off_land(self):
        u = self.u.copy()
        u[:, 4:] = np.nan
        r = step_advection_diffusion(self.c, u, self.v, 0.0, 100.0,
                                     self.grid, wet=self.wet)
        self.assertTrue(np.all(np.isfinite(r.concentration)))
        # NaN forcing on a wet cell must still fail loudly
        u2 = self.u.copy()
        u2[0, 0] = np.nan
        with self.assertRaisesRegex(ValueError, "finite on active"):
            step_advection_diffusion(self.c, u2, self.v, 0.0, 100.0,
                                     self.grid, wet=self.wet)

    def test_isolated_wet_enclave_keeps_mass(self):
        # single wet cell surrounded by land: tracer inside is retained
        wet = np.zeros((4, 6), dtype=bool)
        wet[1, 2] = True
        c = np.zeros((4, 6))
        c[1, 2] = 2.0
        r = step_advection_diffusion(c, self.u, self.v, 0.0, 100.0,
                                     self.grid, wet=wet)
        self.assertAlmostEqual(r.concentration[1, 2], 2.0)
        self.assertAlmostEqual(r.mass_after, r.mass_before, places=12)


class TestActiveMask(unittest.TestCase):
    """QC-hole barrier semantics: wet-but-inactive cells are isolated."""

    def setUp(self):
        self.grid = small_grid()
        self.c = blob()
        self.u = np.full((4, 6), 0.05)
        self.v = np.zeros((4, 6))
        self.active = np.ones((4, 6), dtype=bool)
        self.active[1:3, 2:4] = False  # hole over the blob

    def test_barrier_retains_mass_and_blocks_exchange(self):
        r = step_advection_diffusion(self.c, self.u, self.v, 0.0, 100.0,
                                     self.grid, active=self.active)
        # blob sits inside the hole: nothing may leave or enter
        np.testing.assert_allclose(r.concentration, self.c, atol=1e-12)
        self.assertAlmostEqual(r.mass_after, r.mass_before, places=12)

    def test_partial_hole_only_isolates_boundary_faces(self):
        c = np.zeros((4, 6))
        c[1, :3] = [0.0, 0.5, 1.0]
        active = np.ones((4, 6), dtype=bool)
        active[:, 3] = False  # vertical barrier column
        r = step_advection_diffusion(c, self.u, self.v, 0.0, 100.0,
                                     self.grid, active=active)
        # mass left of the barrier cannot cross it
        left_mass = r.concentration[:, :3].sum() * self.grid.cell_area
        before_left = c[:, :3].sum() * self.grid.cell_area
        self.assertAlmostEqual(left_mass, before_left, places=10)
        # advection still happened inside the active region
        self.assertLess(r.concentration[1, 1], 0.5)
        # the isolated column keeps its tracer untouched
        np.testing.assert_allclose(r.concentration[:, 3], c[:, 3])

    def test_nan_forcing_on_inactive_cell_accepted(self):
        u = self.u.copy()
        u[1:3, 2:4] = np.nan
        r = step_advection_diffusion(self.c, u, self.v, 0.0, 100.0,
                                     self.grid, active=self.active)
        np.testing.assert_allclose(r.concentration, self.c, atol=1e-12)

    def test_nan_forcing_on_active_cell_rejected(self):
        u = self.u.copy()
        u[0, 0] = np.nan
        with self.assertRaisesRegex(ValueError, "finite on active"):
            step_advection_diffusion(self.c, u, self.v, 0.0, 100.0,
                                     self.grid, active=self.active)

    def test_wet_and_active_combine(self):
        wet = np.ones((4, 6), dtype=bool)
        wet[:, 5] = False
        active = self.active.copy()
        active[:, 0] = False
        r = step_advection_diffusion(self.c, self.u, self.v, 0.0, 100.0,
                                     self.grid, wet=wet, active=active)
        self.assertTrue(np.all(r.concentration[:, 5] == 0.0))
        self.assertAlmostEqual(r.mass_after, r.mass_before, places=10)


class TestOpenBoundaries(unittest.TestCase):
    def setUp(self):
        self.grid = small_grid()
        self.c = blob()
        self.u = np.full((4, 6), 0.05)
        self.v = np.zeros((4, 6))

    def test_east_open_exports_mass_and_reports_loss(self):
        # tracer adjacent to the east edge so one step produces outflow
        c = np.zeros((4, 6))
        c[:, 4:] = 1.0
        dt = 400.0
        r = step_advection_diffusion(c, self.u, self.v, 0.0, dt,
                                     self.grid, open_edges=("east",))
        # closed run for comparison
        r_closed = step_advection_diffusion(c, self.u, self.v, 0.0, dt,
                                            self.grid)
        self.assertAlmostEqual(r_closed.mass_after, r_closed.mass_before,
                               places=10)
        self.assertGreater(r.boundary_loss_mass, 0.0)
        self.assertAlmostEqual(
            r.mass_after,
            r.mass_before + r.source_mass - r.sink_mass - r.boundary_loss_mass,
            places=8)

    def test_open_boundary_zero_gradient_inflow(self):
        # uniform concentration + uniform eastward flow: steady state,
        # flux in at west must equal flux out at east
        c = np.ones((4, 6))
        r = step_advection_diffusion(c, self.u, self.v, 0.0, 100.0,
                                     self.grid, open_edges=("west", "east"))
        np.testing.assert_allclose(r.concentration, c, atol=1e-10)
        self.assertAlmostEqual(r.boundary_loss_mass, 0.0, places=10)

    def test_closed_by_default_and_bad_edge_rejected(self):
        r = step_advection_diffusion(self.c, self.u, self.v, 0.0, 100.0,
                                     self.grid)
        self.assertEqual(r.boundary_loss_mass, 0.0)
        with self.assertRaisesRegex(ValueError, "unknown open_edges"):
            step_advection_diffusion(self.c, self.u, self.v, 0.0, 100.0,
                                     self.grid, open_edges=("north_up",))

    def test_exact_translation_at_courant_one(self):
        # manufactured solution: with u*dt/dx == 1 first-order upwind
        # translates the profile by exactly one cell per step
        c = np.zeros((4, 6))
        c[1, 2] = 1.0
        u = np.full((4, 6), 1.0)  # u*dt/dx = 1 at dt=100, dx=100
        r = step_advection_diffusion(c, u, self.v, 0.0, 100.0, self.grid,
                                     enforce_stability=False)
        expected = np.zeros((4, 6))
        expected[1, 3] = 1.0
        np.testing.assert_allclose(r.concentration, expected, atol=1e-12)

    def test_open_edge_respects_land_mask(self):
        wet = np.ones((4, 6), dtype=bool)
        wet[:, -1] = False  # entire east column is land
        c = np.zeros((4, 6))
        c[:, -2] = 1.0     # tracer pressed against the coastline
        r = step_advection_diffusion(c, self.u, self.v, 0.0, 400.0,
                                     self.grid, wet=wet, open_edges=("east",))
        # land column stays exactly zero and seals the east face
        self.assertTrue(np.all(r.concentration[:, -1] == 0.0))
        self.assertAlmostEqual(r.mass_after, r.mass_before, places=10)
        self.assertEqual(r.boundary_loss_mass, 0.0)


class TestEulerianHFRBoundaries(unittest.TestCase):
    def make_field(self, invalid=None):
        x = np.arange(0.0, 500.0, 100.0)
        y = np.arange(0.0, 400.0, 100.0)
        times = np.array([0.0, 10.0, 20.0])
        velocity = np.zeros((3, 4, 5, 2))
        velocity[..., 0] = 0.05
        valid = np.ones((3, 4, 5), dtype=bool)
        if invalid is not None:
            for ti, iy, ix in invalid:
                valid[ti, iy, ix] = False
        return VelocityField(x, y, times, velocity, valid)

    def test_cell_centers(self):
        forcing = to_eulerian_forcing(self.make_field())
        np.testing.assert_allclose(forcing.cell_center_x,
                                   [50.0, 150.0, 250.0, 350.0])
        np.testing.assert_allclose(forcing.cell_center_y,
                                   [50.0, 150.0, 250.0])

    def test_qc_barrier_mode_preserves_mass(self):
        # node (t=1, iy=1, ix=1) invalid -> the 4 cells around it invalid
        forcing = to_eulerian_forcing(
            self.make_field(invalid=[(1, 1, 1)]))
        c = np.ones((3, 4))
        # fail-closed default still raises at the midpoint t=5
        with self.assertRaises(ValueError):
            forcing.step(c, start_time_s=0.0, dt_s=10.0, diffusivity=0.0)
        # barrier mode steps through with mass conserved
        r = forcing.step(c, start_time_s=0.0, dt_s=10.0, diffusivity=0.0,
                         qc_holes="barrier")
        self.assertAlmostEqual(r.mass_after, r.mass_before, places=10)
        self.assertGreater(r.boundary_loss_mass, -1e-9)

    def test_qc_barrier_resumes_when_mask_lifts(self):
        forcing = to_eulerian_forcing(self.make_field())
        c = np.ones((3, 4))
        r1 = forcing.step(c, start_time_s=0.0, dt_s=10.0, diffusivity=0.0,
                          qc_holes="barrier", open_edges=("east",))
        self.assertGreater(r1.boundary_loss_mass, 0.0)
        # second step uses t in (10,20): all cells valid again
        r2 = forcing.step(r1.concentration, start_time_s=10.0, dt_s=10.0,
                          diffusivity=0.0, qc_holes="barrier",
                          open_edges=("east",))
        self.assertGreater(r2.boundary_loss_mass, 0.0)

    def test_invalid_qc_holes_policy_rejected(self):
        forcing = to_eulerian_forcing(self.make_field())
        with self.assertRaisesRegex(ValueError, "qc_holes"):
            forcing.step(np.ones((3, 4)), start_time_s=0.0, dt_s=10.0,
                         diffusivity=0.0, qc_holes="interpolate")

    def test_wet_mask_through_hfr_step(self):
        forcing = to_eulerian_forcing(self.make_field())
        wet = np.ones((3, 4), dtype=bool)
        wet[:, -1] = False
        c = np.ones((3, 4)) * 0.5
        c[:, -1] = 0.0
        r = forcing.step(c, start_time_s=0.0, dt_s=10.0, diffusivity=0.0,
                         wet=wet, open_edges=("west", "east", "south", "north"))
        # open faces exist only on the wet boundary; land column sealed
        self.assertTrue(np.all(r.concentration[:, -1] == 0.0))
        self.assertAlmostEqual(r.mass_after, r.mass_before
                               + r.source_mass - r.sink_mass
                               - r.boundary_loss_mass, places=10)


if __name__ == "__main__":
    unittest.main()
