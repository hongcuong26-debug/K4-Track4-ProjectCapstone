"""Frontal-marker pinhole geometry; no model training or vehicle control."""
import cv2
import numpy as np

DICTIONARY = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)


def detect(frame, detector):
    corners, ids, _ = detector.detectMarkers(frame)
    if ids is not None:
        for points, marker_id in zip(corners, ids.flatten()):
            if marker_id == 0:
                return points.reshape(4, 2)
    return None


def analyze(corners, width, focal_px, marker_m):
    result = dict(status='NO MARKER', distance_m=None, offset_m=None, side_px=None)
    if corners is None:
        return result
    points = np.asarray(corners, dtype=float).reshape(4, 2)
    sides = np.linalg.norm(points - np.roll(points, -1, axis=0), axis=1)
    side = float(np.mean(sides))
    result['side_px'] = side
    # Reject tiny or obviously foreshortened quadrilaterals; not a pose guarantee.
    if min(sides) < 24 or max(sides) / max(min(sides), 1) > 1.25:
        result['status'] = 'UNCERTAIN'
        return result
    z = focal_px * marker_m / side
    x = (float(points[:, 0].mean()) - width / 2) * z / focal_px
    result.update(distance_m=z, offset_m=x)
    result['status'] = 'ALIGNED' if abs(x) <= .025 else ('TARGET RIGHT' if x > 0 else 'TARGET LEFT')
    return result
