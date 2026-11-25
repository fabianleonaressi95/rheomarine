import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "check_observation_file.py"

HEADER = ("obs_id,dataset_id,instrument_id,obs_type,time_utc,time_original,"
          "tz_original,longitude,latitude,depth_m,depth_reference,u_east,"
          "v_north,speed,direction,direction_convention,qc_flag,qc_meaning,"
          "uncertainty,avg_interval_s,sample_interval_s,missing_reason,"
          "source_dataset,source_file,retrieved_utc,licence,raw_value")

VALID_ROW = ("NIB-01-t0,DS1,M1,eulerian_point,2026-11-20T06:00:00Z,"
             "2026-11-20 06:00,UTC,13.55,45.55,10.0,below_surface,"
             "0.10,-0.05,0.11,333,nautical_from_north_cw,1,good_data,"
             "0.05,600,600,,NIB-ADCP,file.nc,2026-11-25T00:00:00Z,"
             "institutional,")


def run_checker(lines):
    with tempfile.NamedTemporaryFile(
            "w", suffix=".csv", delete=False, newline="") as fh:
        fh.write("\n".join(lines) + "\n")
        path = fh.name
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), path],
        capture_output=True, text=True)
    Path(path).unlink()
    return proc


class TestObservationChecker(unittest.TestCase):
    def test_template_header_passes_structure_but_has_no_rows(self):
        proc = run_checker([HEADER])
        self.assertEqual(proc.returncode, 2)  # no data rows -> violation
        self.assertIn("no data rows", proc.stdout)

    def test_valid_row_passes(self):
        proc = run_checker([HEADER, VALID_ROW])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("PASS", proc.stdout)

    def test_bad_obs_type_fails(self):
        bad = VALID_ROW.replace("eulerian_point", "magic_beacon")
        proc = run_checker([HEADER, bad])
        self.assertEqual(proc.returncode, 2)
        self.assertIn("obs_type", proc.stdout)

    def test_missing_required_column_fails(self):
        short = HEADER.replace(",qc_flag", "")
        proc = run_checker([short, VALID_ROW.replace(",1,good_data", "")])
        self.assertEqual(proc.returncode, 2)
        self.assertIn("missing required columns", proc.stdout)

    def test_depth_without_reference_fails(self):
        bad = VALID_ROW.replace(",10.0,below_surface", ",10.0,")
        proc = run_checker([HEADER, bad])
        self.assertEqual(proc.returncode, 2)
        self.assertIn("depth_reference", proc.stdout)


if __name__ == "__main__":
    unittest.main()
