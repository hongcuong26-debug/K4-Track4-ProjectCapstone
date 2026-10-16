"""Evaluate app CSV against simulation labels, excluding occlusion from distance MAE."""
import csv
import json
from pathlib import Path
import statistics


def main():
    truth = list(csv.DictReader(open('assets/ground_truth.csv')))
    rows = list(csv.DictReader(open('evidence/simulation.csv')))
    if len(rows) != len(truth) or any(r['frame'] != t['frame'] for r, t in zip(rows, truth)):
        raise ValueError('Frame count/order mismatch')
    visible = [(r,t) for r,t in zip(rows,truth) if t['visible'] == '1']
    measured = [(r,t) for r,t in visible if r['distance_m']]
    hidden = [(r,t) for r,t in zip(rows,truth) if t['visible'] == '0']
    report = dict(dataset='SYNTHETIC frontal markers; not real-world accuracy', frames=len(rows),
        visible_frames=len(visible), measured_frames=len(measured),
        detection_rate=len(measured)/len(visible),
        distance_mae_m=statistics.mean(abs(float(r['distance_m'])-float(t['z_m'])) for r,t in measured),
        offset_mae_m=statistics.mean(abs(float(r['offset_m'])-float(t['x_m'])) for r,t in measured),
        occluded_frames=len(hidden), occluded_no_marker=sum(r['status']=='NO MARKER' for r,t in hidden),
        processing_median_ms=statistics.median(float(r['processing_ms']) for r in rows),
        processing_p95_ms=sorted(float(r['processing_ms']) for r in rows)[int(.95*(len(rows)-1))])
    Path('evidence/metrics.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    if report['detection_rate'] < .95 or report['distance_mae_m'] > .03 or report['occluded_no_marker'] != len(hidden):
        raise SystemExit('Simulation acceptance failed')


if __name__ == '__main__':
    main()
