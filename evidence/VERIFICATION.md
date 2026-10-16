# Kiểm tra triển khai — 2026-10-17

Môi trường: Linux, Python 3.14.7, OpenCV 4.13.0, NumPy 2.5.4.

- `python -m unittest discover -s tests`: 7 tests đạt, gồm hình học frontal, lệch ngang, mất marker, quá nhỏ, méo lớn và giới hạn replay CLI và từ chối tiêu cự âm trong file hiệu chuẩn.
- `python app.py --source 0 --headless --max-frames 30 --log runs/webcam_smoke.csv`: đọc/xử lý 30 frame webcam thành công. Không lưu ảnh/video webcam; CSV cục bộ nằm trong thư mục runs bị gitignore. Chưa thử với marker in trước camera.
- Replay mô phỏng headless: 240 frame; log `simulation.csv`, báo cáo `metrics.json`. Mỗi lần chạy thời gian xử lý có thể khác.
- Video `assets/backup_annotated.avi`: đọc được, 240 frame, 800×600; kiểm tra trực quan frame đầu có hộp marker, hướng, khoảng cách và nhãn SIMULATION.
- `python -m pip check`: không lỗi phụ thuộc.
- `git diff --check`: không lỗi khoảng trắng.

Chưa kiểm tra: cửa sổ GUI trên màn hình trình bày; định vị và MAE trên marker/thước thật; video webcam dự phòng tự quay. Video mô phỏng không thay thế các phép thử này.
