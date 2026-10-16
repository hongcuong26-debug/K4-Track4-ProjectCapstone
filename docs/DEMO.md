# Kịch bản demo — 2A202602415

## 1 phút: bài toán

“Em chọn VinFast ChargeAlign, mô hình hỗ trợ quan sát vị trí tương đối giữa camera và marker đặt tại vị trí sạc. Người dùng giả định là nhân viên thử nghiệm bố trí trạm sạc. Em làm một mình nên chọn ArUco, chỉ cần webcam và giấy in; không cần huấn luyện model. Đây là thử nghiệm trên bàn, chưa chứng minh khả năng căn xe thật.”

## 4 phút: chạy trực tiếp

- Mở app trên webcam, chỉ marker in và kích thước cạnh đen đã đo.
- Đặt chính diện ở khoảng cách đã đo, nhấn C. Giải thích bước đo tiêu cự.
- Di chuyển marker trái → giữa → phải. Chỉ rõ hướng mục tiêu trong ảnh, không phải hướng đánh lái.
- Đưa gần/xa để xem Z. Nhờ giám khảo tự cầm marker thay đổi vị trí.
- Che một nửa marker: NO MARKER, không dùng lại khoảng cách cũ. Nghiêng mạnh: UNCERTAIN nếu hình dạng bị méo đủ lớn.
- Nếu webcam hỏng: nói rõ chuyển sang video mô phỏng; chạy `python app.py --source assets/simulation.avi --calibration assets/sim_camera.json`. Không nói đây là video tự quay.

## 2 phút: bằng chứng, kiến thức, tác động

Mở `evidence/metrics.json`: 200 frame rõ và 40 frame che. Khoảng cách MAE trên mô phỏng khoảng 1.02 cm; chỉ chứng minh pipeline hoạt động trong điều kiện tổng hợp chính diện. Thời gian xử lý không phải độ trễ hiển thị đầu cuối.

Chỉ công thức Z=fL/s và biểu diễn bốn góc trong `docking.py`, log theo frame ở `app.py`. Giải thích vì sao không train model trong hai giờ và vì sao ngưỡng từ chối cần thiết.

**Impact giả định, không phải số liệu VinFast:** nếu một địa điểm có 100 lượt/ngày và phương án sau khi thử nghiệm thực tế giúp giảm 5 giây căn vị trí mỗi lượt thì tiết kiệm 500 giây, khoảng 8.3 phút/ngày, hay 4.2 giờ/30 ngày. Cần đo baseline và thời gian có hỗ trợ để kiểm chứng cả giả định 5 giây. Chưa chứng minh tiết kiệm hoặc giảm tai nạn.

Mở rộng: hiệu chuẩn camera đầy đủ, solvePnP để đo pose, nhiều marker tăng khả năng nhìn thấy, đánh giá nắng/chói/bẩn/ban đêm và gắn camera thực tế. Rủi ro gồm che khuất, góc nhìn, phản chiếu, kích thước marker sai và vị trí camera không trùng tâm xe.

## 3 phút: hỏi đáp

- Có dùng AI không? Không train/call model; chọn các trụ cột hình học, biểu diễn, bất định, thời gian, dữ liệu và bằng chứng. ArUco giải mã mẫu xác định.
- Vì sao khoảng cách sai khi nghiêng? Kích thước chiếu bị co; công thức đang giả định chính diện. Kiểm tra tỉ lệ cạnh chỉ chặn một số trường hợp.
- Ngưỡng 2.5 cm từ đâu? Ngưỡng demo do người làm chọn, chưa phải dung sai kỹ thuật của trạm sạc.
- 100% có đáng tin không? Chỉ 200 frame tổng hợp rất đơn giản, không phải kiểm thử độc lập trên xe thật; không kết luận tổng quát.
- Vì sao che marker là ca lỗi? Mục tiêu còn trong ảnh nhưng hệ thống không định vị được; cảnh báo mất dữ liệu là cách xử lý, không khắc phục được nhiệm vụ.

## Checklist trước thi

- [ ] Cài môi trường và thử webcam/GUI tại phòng demo.
- [ ] In marker, đo cạnh đen và mang thước.
- [ ] Hiệu chuẩn cùng độ phân giải, đo thật ít nhất ba khoảng cách.
- [ ] Tự quay video webcam bằng `--record runs/webcam_backup.avi`, kiểm tra phát lại.
- [x] Có video mô phỏng dự phòng với nhãn nguồn rõ ràng.
- [x] Có ground truth, CSV, MAE mô phỏng và ca che khuất.
- [x] Chỉ được ít nhất hai trụ cột và giới hạn mô hình.
- [x] Dữ liệu có sẵn hoàn toàn tổng hợp, không có bệnh nhân/sinh viên.
- [x] Có người dùng giả định, tác động định lượng với giả định rõ.
- [ ] Đăng nhập VLearn cá nhân và nộp link repo.

Không quay người xung quanh khi demo. Nếu ghi webcam, chỉ quay marker/bàn của bản thân; không commit video chứa người ngoài vào repo.
