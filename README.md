# VinFast ChargeAlign — hỗ trợ căn vị trí sạc bằng camera

**Học viên: 2A202602415 · Team 1 người · Track 4 Capstone**

Demo bàn: webcam tìm marker ArUco ID 0, báo vị trí mục tiêu bên trái/phải, căn giữa và ước lượng khoảng cách. Người dùng giả định là nhân viên thử nghiệm bố trí camera/marker tại trạm sạc VinFast. Dự án độc lập phục vụ khóa học, chưa tích hợp xe hoặc trạm sạc.

Chọn đề tài này vì chỉ cần laptop + một tờ marker, không train model, không GPU, không robot. Bài làm sử dụng **hình học, biểu diễn, bất định, thời gian, dữ liệu và bằng chứng**; không tuyên bố sử dụng trụ cột Học.

## Chạy nhanh

Đã kiểm tra trên Linux, Python 3.14.7. Khuyến nghị Python 3.11–3.14. Cần desktop để mở cửa sổ OpenCV; máy không có màn hình dùng `--headless`.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
# Windows PowerShell: .venv\Scripts\Activate.ps1

# Chạy ngay bằng video mô phỏng đã có trong repo
python app.py --source assets/simulation.avi --calibration assets/sim_camera.json

# Chạy webcam thật, ghi video dự phòng và log
python app.py --source 0 --record runs/webcam_backup.avi
```

Nhấn **Q** để thoát. Nếu webcam không mở, thử `--source 1`, đóng ứng dụng đang dùng camera hoặc dùng video. Không có model tải ngầm, không cần mạng sau khi cài thư viện. File đề bài gốc vẫn ở [index.html](index.html).

## Chuẩn bị marker và hiệu chuẩn

1. In [marker_id0.png](assets/marker_id0.png), giữ lề trắng. Đo cạnh **hình vuông đen ngoài cùng**, không đo cả lề. Có thể mở ảnh trên điện thoại thứ hai để thử, nhưng vẫn phải đo kích thước hiển thị thực tế.
2. Đặt marker gần song song mặt camera, đủ sáng và nhìn rõ bốn góc. Camera cố định, không bật mirror. Di chuyển marker qua trái/phải để thấy trạng thái tương ứng. `TARGET RIGHT` nghĩa là **mục tiêu nằm bên phải ảnh camera**, không phải lệnh đánh lái.
3. Ví dụ cạnh đen 10 cm, khoảng cách từ camera đến mặt marker 50 cm:

```bash
python app.py --source 0 --marker-m 0.10 --known-distance 0.50 --record runs/webcam_backup.avi
```

4. Khi marker chính diện và nhìn rõ, nhấn **C** để lưu `runs/camera.json`. Từ lúc này số đo dùng tiêu cự vừa đo. Khởi động lần sau:

```bash
python app.py --source 0 --marker-m 0.10 --calibration runs/camera.json --record runs/webcam_backup.avi
```

Chưa nhấn C thì khoảng cách được ghi **UNCALIBRATED**, chỉ có tính minh họa. Thay độ phân giải, zoom, camera hoặc kích thước marker thì hiệu chuẩn lại. `assets/sim_camera.json` **chỉ dành cho mô phỏng**, không dùng cho webcam.

Đây là hiệu chuẩn tiêu cự một điểm, không phải hiệu chuẩn nội tại đầy đủ. Không bù méo thấu kính, không đo góc xoay 3D. Sai kích thước marker, góc nghiêng hoặc méo ống kính có thể gây sai số ngay cả khi vẫn nhận diện được.

## Kiến thức nằm ở đâu?

| Trụ cột | Trong hệ thống | Lý do lựa chọn |
|---|---|---|
| Hình học | `docking.analyze`: Z = fL/s; X = (u − W/2)Z/f. C đo f = sZ/L | Đủ cho mô hình marker chính diện, dễ giải thích và kiểm chứng; solvePnP phù hợp bước mở rộng khi cần góc xoay |
| Biểu diễn | ID 0 + bốn góc → cạnh pixel → Z/X → trạng thái | Tránh nhầm marker khác và tách nhận diện khỏi quyết định |
| Bất định | Từ chối cạnh <24 px hoặc tỉ lệ cạnh dài/ngắn >1.25 | Chặn trường hợp quá nhỏ/méo rõ rệt; đây là heuristic, không phải xác suất tin cậy |
| Thời gian | `processing_ms`, median/p95 trong báo cáo | Đo thời gian đọc frame + nhận diện + quyết định; không gồm vẽ, ghi video, hiển thị hoặc độ trễ phần cứng camera |
| Dữ liệu | CSV từng frame; replay; ground truth mô phỏng | Có thể chạy lại cùng đầu vào để đối chiếu |
| Bằng chứng | `evidence/metrics.json`, bài test và ca che marker | Phân biệt số đo mô phỏng với chất lượng ngoài thực tế |

Ngưỡng căn giữa là ±2.5 cm trong mô hình đã hiệu chuẩn. Không giữ vị trí cũ khi mất marker. Không có điều khiển xe, phanh hoặc quyết định an toàn tự động.

## Tái tạo bằng chứng

```bash
python -m unittest discover -s tests
python prepare_demo.py
python app.py --source assets/simulation.avi --calibration assets/sim_camera.json --headless --log evidence/simulation.csv --record assets/backup_annotated.avi
python evaluate.py
```

[Video dự phòng có overlay](assets/backup_annotated.avi) và [video đầu vào](assets/simulation.avi) dài 12 giây, đều là **MÔ PHỎNG**, không phải video webcam thật. Có nhãn mô phỏng ngay trên hình. Có thể mở AVI bằng VLC hoặc replay ứng dụng. Script tạo ảnh marker, video và ground truth, không dùng dữ liệu của người khác.

Kết quả lần chạy đã lưu: **200/200 frame marker rõ được đo**, MAE khoảng cách **1.02 cm**, MAE lệch ngang **0.91 mm**. Cạnh marker được dựng từ 80/100/128 pixel với f=800 px, L=0.1 m; ground truth khoảng cách tính từ thông số dựng ảnh, còn kết quả đi qua video MJPEG và bộ nhận diện thật. Sai số có lượng tử hóa góc ảnh. Không suy rộng số này ra webcam hoặc xe thật. Thời gian xử lý tùy máy, xem JSON thay vì coi là cam kết FPS.

**Ca lỗi được tái hiện:** giây 8–10 (frame 160–199), một nửa marker bị che. Hệ thống không giải mã được ID dù mục tiêu vẫn ở đó: 40/40 frame `NO MARKER`, không xuất khoảng cách. Nguyên nhân là mất viền và ô mã cần nhận diện. Trạng thái cảnh báo tránh dùng số cũ nhưng nhiệm vụ định vị vẫn thất bại. Một giới hạn khác: marker nghiêng vừa phải có thể qua ngưỡng hình dạng mà khoảng cách vẫn sai.

Trước buổi thi cần đo thật ở 0.4, 0.6, 0.8 m bằng thước, mỗi mốc 10 lần, ghi khoảng cách thật/ước lượng rồi tính MAE = trung bình |ước lượng − thật|. Đánh dấu các lần không đo được riêng; không thay bằng 0. Chưa có kết quả đo thật trong repo này.

## Demo và nộp bài

Xem [kịch bản 10 phút, checklist, impact và Q&A](docs/DEMO.md). Đã kiểm tra replay headless và đọc webcam thật trong phiên triển khai (không lưu ảnh webcam). Cửa sổ GUI, định vị bằng marker in và video tự quay vẫn cần kiểm tra trên đúng máy mang đi thi.

Repo nộp: https://github.com/hongcuong26-debug/K4-Track4-ProjectCapstone

Học viên **2A202602415** phải tự đăng nhập VLearn và nộp link repo để được ghi nhận bài. Việc push GitHub không thay cho nộp VLearn.

Tham khảo API: [OpenCV ArUco detection](https://docs.opencv.org/4.13.0/d5/dae/tutorial_aruco_detection.html). Thiết kế và phạm vi: [docs/DESIGN.md](docs/DESIGN.md).
