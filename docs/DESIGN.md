# Thiết kế: VinFast ChargeAlign — 2A202602415

Mục tiêu: một người hoàn thành demo webcam trong khoảng hai giờ. Người dùng giả định là nhân viên thử nghiệm vị trí camera/marker tại trạm sạc. Đây là mô hình bàn, không điều khiển xe, không tích hợp sản phẩm VinFast.

Chọn ArUco thay cho nhận diện buồn ngủ (cần model/mốc mắt) hoặc robot (cần mô phỏng và điều khiển). Không cần học máy: rubric cho phép chọn các trụ cột khác.

Luồng: webcam/video → ArUco DICT_4X4_50 ID 0 → bốn góc → kiểm tra kích thước/méo → hình học pinhole → trạng thái và CSV. Không giữ kết quả cũ khi marker mất. Khoảng cách chỉ đúng xấp xỉ khi mặt marker song song mặt camera, tiêu cự được đo cùng độ phân giải, bỏ qua méo thấu kính. Từ chối hình thang/méo lớn nhưng không đảm bảo loại mọi góc nghiêng.

Phạm vi: căn ngang, khoảng cách, hiệu chuẩn tiêu cự một điểm, record/replay, video mô phỏng ghi nhãn, đánh giá tự động và tài liệu demo. Không có backend, training, tự lái hoặc chẩn đoán an toàn.

Kế hoạch: (1) test hình học và trạng thái mất marker; (2) module nhận diện + CLI webcam/video, CSV/record; (3) marker in, video mô phỏng và ground truth; (4) đánh giá sai số/mất nhận diện; (5) hướng dẫn chạy, demo, giới hạn và commit/push main. Kiểm tra bằng unittest, chạy toàn video headless, kiểm tra file video và git diff. Webcam và video tự quay cần thực hiện tại máy demo nếu phiên làm việc không có camera.
