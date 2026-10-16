"""Run: python app.py --source 0; use --help for replay/record/calibration."""
import argparse
import csv
import json
import math
from pathlib import Path
import time

import cv2
from docking import DICTIONARY, analyze, detect


def positive(value):
    number = float(value)
    if number <= 0 or not math.isfinite(number):
        raise argparse.ArgumentTypeError('must be finite and > 0')
    return number


def main():
    parser = argparse.ArgumentParser(description='VinFast ChargeAlign | 2A202602415 | tabletop prototype')
    parser.add_argument('--source', default='0', help='camera index or video path')
    parser.add_argument('--marker-m', type=positive, default=.1, help='measured BLACK square side, metres')
    parser.add_argument('--calibration', help='JSON saved by C key; required for calibrated real-camera distances')
    parser.add_argument('--known-distance', type=positive, default=.5, help='frontal reference distance for C key')
    parser.add_argument('--calibration-out', default='runs/camera.json')
    parser.add_argument('--log', default='runs/session.csv')
    parser.add_argument('--record', help='save annotated AVI backup video')
    parser.add_argument('--headless', action='store_true')
    parser.add_argument('--max-frames', type=int, default=0, help='stop after N frames; 0 means until EOF/Q')
    args = parser.parse_args()
    if args.max_frames < 0:
        parser.error('--max-frames must be >= 0')
    calibration = None
    if args.calibration:
        try:
            calibration = json.loads(Path(args.calibration).read_text())
            for name in ('focal_px', 'width', 'height'):
                value = calibration[name]
                if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
                    raise ValueError(f'{name} must be finite and positive')
        except (OSError, ValueError, KeyError, TypeError) as error:
            parser.error(f'Invalid calibration: {error}')
    source = int(args.source) if args.source.isdecimal() else args.source
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        parser.exit(1, 'Cannot open input. Try --source assets/simulation.avi, or check camera permissions.\n')
    detector = cv2.aruco.ArucoDetector(DICTIONARY)
    Path(args.log).parent.mkdir(parents=True, exist_ok=True)
    writer = None
    count = 0
    session_started = time.perf_counter()
    fps = cap.get(cv2.CAP_PROP_FPS)
    fps = fps if 0 < fps <= 120 else 30
    try:
        with open(args.log, 'w', newline='') as output:
            fields = ['frame', 'source_s', 'status', 'distance_m', 'offset_m', 'side_px', 'processing_ms', 'calibrated']
            log = csv.DictWriter(output, fieldnames=fields)
            log.writeheader()
            while True:
                started = time.perf_counter()
                ok, frame = cap.read()
                if not ok:
                    break
                h, w = frame.shape[:2]
                if calibration and (calibration['width'] != w or calibration['height'] != h):
                    raise ValueError('Calibration resolution differs from input. Recalibrate at this resolution.')
                focal = calibration['focal_px'] if calibration else float(w)
                corners = detect(frame, detector)
                result = analyze(corners, w, focal, args.marker_m)
                elapsed = (time.perf_counter() - started) * 1000
                log.writerow(dict(frame=count, source_s=count / fps if isinstance(source, str) else time.perf_counter() - session_started, processing_ms=round(elapsed, 3), calibrated=bool(calibration), **result))
                if corners is not None:
                    cv2.polylines(frame, [corners.astype('int32')], True, (0, 220, 220), 2)
                cv2.line(frame, (w//2, 0), (w//2, h), (120, 120, 120), 1)
                z, x = result['distance_m'], result['offset_m']
                lines = ['VinFast ChargeAlign | TABLETOP DEMO | 2A202602415', result['status'],
                         f'Z={z:.2f} m | target X={x:+.3f} m' if z is not None else 'No reliable measurement',
                         f'Processing: {elapsed:.1f} ms | frame {count}',
                         'CALIBRATED (frontal only)' if calibration else 'UNCALIBRATED: distance is illustrative',
                         'Q: quit | C: calibrate | target direction in camera image']
                cv2.rectangle(frame, (0, 0), (w, 155), (20, 25, 35), -1)
                for i, line in enumerate(lines):
                    cv2.putText(frame, line, (10, 23 + i*24), cv2.FONT_HERSHEY_SIMPLEX, .47, (240, 240, 240), 1, cv2.LINE_AA)
                if args.record:
                    if writer is None:
                        Path(args.record).parent.mkdir(parents=True, exist_ok=True)
                        writer = cv2.VideoWriter(args.record, cv2.VideoWriter_fourcc(*'MJPG'), fps, (w, h))
                        if not writer.isOpened():
                            raise RuntimeError('Cannot create recording')
                    writer.write(frame)
                count += 1
                if args.max_frames and count >= args.max_frames:
                    break
                if not args.headless:
                    cv2.imshow('ChargeAlign', frame)
                    key = cv2.waitKey(max(1, int(1000/fps - elapsed)) if isinstance(source, str) else 1) & 0xff
                    if key == ord('q'):
                        break
                    if key == ord('c') and z is not None:
                        calibration = dict(focal_px=result['side_px']*args.known_distance/args.marker_m, width=w, height=h)
                        Path(args.calibration_out).parent.mkdir(parents=True, exist_ok=True)
                        Path(args.calibration_out).write_text(json.dumps(calibration, indent=2))
                        print('Saved calibration:', args.calibration_out)
    finally:
        cap.release()
        if writer is not None:
            writer.release()
        if not args.headless:
            cv2.destroyAllWindows()
    print(f'Processed {count} frames. Log: {args.log}')


if __name__ == '__main__':
    main()
