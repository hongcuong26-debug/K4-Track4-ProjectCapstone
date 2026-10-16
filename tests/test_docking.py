import unittest
import numpy as np
from docking import analyze

class DockingTests(unittest.TestCase):
    def test_frontal_marker_at_known_distance(self):
        result = analyze(np.array([[280,200],[360,200],[360,280],[280,280]]), 640, 800, .1)
        self.assertAlmostEqual(result['distance_m'], 1.)
        self.assertEqual(result['status'], 'ALIGNED')

    def test_marker_right_means_target_right(self):
        result = analyze(np.array([[360,200],[440,200],[440,280],[360,280]]), 640, 800, .1)
        self.assertEqual(result['status'], 'TARGET RIGHT')
        self.assertAlmostEqual(result['offset_m'], .1)

    def test_missing_marker_never_keeps_old_guidance(self):
        self.assertEqual(analyze(None, 640, 800, .1)['status'], 'NO MARKER')

    def test_foreshortened_marker_has_no_distance(self):
        result = analyze(np.array([[300,160],[340,160],[340,280],[300,280]]), 640, 800, .1)
        self.assertEqual(result['status'], 'UNCERTAIN')
        self.assertIsNone(result['distance_m'])

    def test_small_marker_rejected(self):
        self.assertEqual(analyze(np.array([[300,200],[310,200],[310,210],[300,210]]), 640, 800, .1)['status'], 'UNCERTAIN')

if __name__ == '__main__':
    unittest.main()
