"""Generate reproducible SIMULATION assets and ground truth, never camera footage."""
import csv
import json
from pathlib import Path
import cv2
import numpy as np
from docking import DICTIONARY


def main():
    Path('assets').mkdir(exist_ok=True)
    marker = cv2.aruco.generateImageMarker(DICTIONARY, 0, 600)
    cv2.imwrite('assets/marker_id0.png', cv2.copyMakeBorder(marker, 100, 100, 100, 100, cv2.BORDER_CONSTANT, value=255))
    Path('assets/sim_camera.json').write_text(json.dumps(dict(focal_px=800., width=800, height=600), indent=2))
    video = cv2.VideoWriter('assets/simulation.avi', cv2.VideoWriter_fourcc(*'MJPG'), 20, (800, 600))
    if not video.isOpened():
        raise RuntimeError('Video writer unavailable')
    try:
        with open('assets/ground_truth.csv', 'w', newline='') as file:
            log = csv.writer(file)
            log.writerow(['frame', 'case', 'z_m', 'x_m', 'visible'])
            for i in range(240):
                stage = i // 40
                x = [-.12, 0, .12, 0, 0, 0][stage]
                size = [80, 80, 80, 128, 100, 100][stage]
                case = ['left', 'aligned', 'right', 'closer', 'occluded', 'recovered'][stage]
                frame = np.full((600, 800, 3), 235, dtype=np.uint8)
                cx = round(400 + x*size/.1)
                left, top = cx - size//2, 320-size//2
                tile = cv2.resize(marker, (size, size), interpolation=cv2.INTER_NEAREST)
                frame[top:top+size, left:left+size] = cv2.cvtColor(tile, cv2.COLOR_GRAY2BGR)
                if stage == 4:
                    frame[top:top+size, left:left+size//2+5] = 235
                cv2.putText(frame, 'SIMULATION - NOT REAL CAMERA FOOTAGE', (50, 530), cv2.FONT_HERSHEY_SIMPLEX, .65, (20,20,170), 2)
                cv2.putText(frame, f'Case: {case}', (50, 560), cv2.FONT_HERSHEY_SIMPLEX, .6, (30,30,30), 1)
                video.write(frame)
                log.writerow([i, case, .1*800/size, x, int(stage != 4)])
    finally:
        video.release()
    print('Generated marker, 12-second simulated video, camera parameters, ground truth.')


if __name__ == '__main__':
    main()
