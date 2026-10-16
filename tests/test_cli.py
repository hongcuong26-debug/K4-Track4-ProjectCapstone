import csv
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

class CliTests(unittest.TestCase):
    def test_negative_calibration_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            calibration = Path(tmp) / 'camera.json'
            calibration.write_text('{"focal_px": -800, "width": 800, "height": 600}')
            result = subprocess.run([sys.executable, 'app.py', '--source', 'assets/simulation.avi', '--headless', '--max-frames', '1', '--calibration', str(calibration), '--log', str(Path(tmp) / 'out.csv')], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Invalid calibration', result.stderr)

    def test_replay_can_stop_after_three_frames(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / 'session.csv'
            result = subprocess.run([sys.executable, 'app.py', '--source', 'assets/simulation.avi', '--headless', '--max-frames', '3', '--log', str(log)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            with log.open() as file:
                rows = list(csv.DictReader(file))
            self.assertEqual(len(rows), 3)
            self.assertEqual(rows[0]['status'], 'TARGET LEFT')
            self.assertEqual(rows[0]['calibrated'], 'False')

if __name__ == '__main__':
    unittest.main()
