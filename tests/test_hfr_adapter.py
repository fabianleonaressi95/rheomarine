import unittest

import numpy as np

from rheomarine_hfr import (
    build_segments,
    crop_field,
    equirectangular_grid,
    hfr_valid_mask,
    to_velocity_fields,
)
from rheomarine_hfr.adapter import HFRDataset
from rheomarine_transport import simulate_m0


def make_dataset(times, u_fill_frac=0.0, gap_after=None):
    """Tiny synthetic dataset: 3x3 lat/lon grid, constant fields."""
    nt = len(times)
    lat = np.linspace(45.5, 45.7, 3)
    lon = np.linspace(13.3, 13.5, 3)
    u = np.full((nt, 3, 3), 0.2)
    v = np.full((nt, 3, 3), -0.1)
    q = np.ones((nt, 3, 3), dtype=np.int16)
    if u_fill_frac:
        u[:, 0, 0] = -32.767
        v[:, 0, 0] = -32.767
        q[:, 0, 0] = -127
    if gap_after is not None:
        times = np.array(times, dtype=float)
        times[gap_after:] += 1e6
    return HFRDataset(times_s=np.asarray(times, float), latitude=lat,
                      longitude=lon, u=u, v=v, qcflag=q)


class TestCoordinates(unittest.TestCase):
    def test_equirectangular_origin_and_scale(self):
        x, y = equirectangular_grid(np.array([13.4]), np.array([45.6]))
        # centre of the single-point range is the point itself -> (0, 0)
        self.assertAlmostEqual(x[0], 0.0)
        self.assertAlmostEqual(y[0], 0.0)

    def test_equirectangular_spacing_is_metric(self):
        lon = np.array([13.3, 13.4, 13.5])
        lat = np.array([45.5, 45.6])
        x, y = equirectangular_grid(lon, lat)
        # ~0.1 deg lon at lat~45.55 -> ~7.8 km
        self.assertAlmostEqual(x[1] - x[0], 7787.0, delta=60.0)
        # ~0.1 deg lat -> ~11.1 km
        self.assertAlmostEqual(y[1] - y[0], 11120.0, delta=30.0)


class TestQC(unittest.TestCase):
    def test_mask_requires_flag1_and_finite_velocity(self):
        q = np.array([[[1, 4, -127], [2, 1, 4], [1, 1, 1]]], dtype=np.int16)
        u = np.array([[[0.1, 0.1, -32.767], [0.1, np.nan, 0.1],
                       [50.0, 0.1, 0.1]]])
        v = np.zeros((1, 3, 3))
        m = hfr_valid_mask(q, u, v)
        self.assertTrue(m[0, 0, 0])
        self.assertFalse(m[0, 0, 1])   # flag 4
        self.assertFalse(m[0, 0, 2])   # fill / flag -127
        self.assertFalse(m[0, 1, 1])   # flag 2 not accepted by default + NaN
        self.assertFalse(m[0, 2, 0])   # |u| > 10 m/s envelope

    def test_flags_2_and_8_can_be_opted_in(self):
        q = np.array([[[1, 2, 8]]], dtype=np.int16)
        u = np.full((1, 1, 3), 0.1)
        v = np.zeros((1, 1, 3))
        m = hfr_valid_mask(q, u, v, accepted_qc_flags=(1, 2, 8))
        self.assertTrue(m.all())


class TestSegments(unittest.TestCase):
    def test_gap_splits_segments(self):
        times = np.array([0.0, 1800.0, 3600.0, 3600.0 + 86400.0,
                          3600.0 + 86400.0 + 1800.0])
        segs = build_segments(times, max_gap_s=7200.0)
        self.assertEqual(len(segs), 2)
        self.assertEqual(segs[0], slice(0, 3))
        self.assertEqual(segs[1], slice(3, 5))

    def test_no_split_below_threshold(self):
        times = np.arange(0.0, 5 * 1800.0, 1800.0)
        segs = build_segments(times, max_gap_s=7200.0)
        self.assertEqual(len(segs), 1)

    def test_single_point_segment_dropped(self):
        times = np.array([0.0, 86400.0])
        self.assertEqual(build_segments(times, 7200.0), [])

    def test_unobserved_timestamp_is_a_barrier(self):
        times = np.arange(0.0, 6 * 1800.0, 1800.0)
        observed = np.array([True, True, False, True, True, True])
        segs = build_segments(times, max_gap_s=7200.0,
                              observed=observed)
        # no segment may contain or interpolate across index 2
        for s in segs:
            self.assertFalse(s.start <= 2 < s.stop)
        self.assertEqual([s.stop - s.start for s in segs], [2, 3])

    def test_all_unobserved_gives_no_segments(self):
        times = np.arange(0.0, 4 * 1800.0, 1800.0)
        self.assertEqual(build_segments(times, 7200.0,
                                        observed=np.zeros(4, bool)), [])


class TestVelocityFields(unittest.TestCase):
    def test_field_shapes_units_and_mask(self):
        ds = make_dataset([0.0, 1800.0, 3600.0], u_fill_frac=0.5)
        fields = to_velocity_fields(ds, max_gap_s=7200.0)
        self.assertEqual(len(fields), 1)
        f = fields[0]
        self.assertEqual(f.velocity.shape, (3, 3, 3, 2))
        self.assertEqual(f.valid.shape, (3, 3, 3))
        self.assertFalse(f.valid[:, 0, 0].any())   # fill cell masked
        self.assertTrue(f.valid[:, 1, 1].all())    # good cell kept
        np.testing.assert_allclose(f.velocity[0, 1, 1], [0.2, -0.1])
        # masked cell carries placeholder, never an observed value
        self.assertEqual(f.velocity[0, 0, 0].tolist(), [0.0, 0.0])
        # metric coordinates in metres, not degrees
        self.assertGreater(f.x[-1] - f.x[0], 10000.0)
        self.assertGreater(f.y[-1] - f.y[0], 20000.0)

    def test_gap_produces_independent_fields(self):
        ds = make_dataset([0.0, 1800.0, 3600.0, 90000.0, 91800.0],
                          gap_after=3)
        fields = to_velocity_fields(ds, max_gap_s=7200.0)
        self.assertEqual(len(fields), 2)
        self.assertEqual(fields[0].times[-1], 3600.0)
        self.assertEqual(fields[1].times[0], 1090000.0)
        # engine cannot reach across the unobserved interval
        with self.assertRaises(ValueError):
            simulate_m0(fields[0], np.array([[fields[0].x[1], fields[0].y[1]]]),
                        start_time=0.0, end_time=90000.0, dt=1800.0)

    def test_crop_field_restricts_domain(self):
        ds = make_dataset([0.0, 1800.0], u_fill_frac=0.0)
        field = to_velocity_fields(ds, max_gap_s=7200.0)[0]
        cropped = crop_field(field, slice(1, 3), slice(0, 2))
        self.assertEqual(cropped.velocity.shape, (2, 2, 2, 2))
        self.assertEqual(cropped.x.size, 2)
        self.assertTrue(np.all(np.diff(cropped.x) > 0))
        self.assertTrue(np.all(np.diff(cropped.y) > 0))
        # coordinates stay metric and consistent with parent grid
        np.testing.assert_allclose(cropped.x, field.x[0:2])
        np.testing.assert_allclose(cropped.y, field.y[1:3])


if __name__ == "__main__":
    unittest.main()
