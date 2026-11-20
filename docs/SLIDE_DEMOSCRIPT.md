# NHÓM 26: SLIDE
- https://docs.google.com/presentation/d/11_dHq-RzoCugc5NalHWmvilyhEb8pLO12zfARVi3lt0/edit?slide=id.p4#slide=id.p4
# KỊCH BẢN DEMO & THUYẾT TRÌNH (DEMO SCRIPT) — NHÓM 26
- **Đề tài:** Track A — Dr May Day Rule Engine Sprint
- **Thành viên Nhóm 26:** Nguyễn Hoàng Sơn, Đặng Văn Duy, Đoàn Bá Quý
- **Thời lượng tối đa:** 07 phút (420 giây)
- **Mục tiêu:** Chứng minh tính đúng đắn của kiến trúc Rule Engine, độ phủ kiểm thử tự động, quy trình CI/CD và tuân thủ an toàn dữ liệu/AI-use.

---

## 1. Phân bổ thời gian & Vai trò (Timeline 7 phút)

| Mốc thời gian | Thời lượng | Nội dung trình bày | Người phụ trách | Tài liệu / Màn hình hiển thị |
| :--- | :---: | :--- | :--- | :--- |
| **00:00 – 01:00** | 1.0 phút | Giới thiệu bài toán Dr May Day, phạm vi Track A & phân công nhóm | **Nguyễn Hoàng Sơn** | `README.md`, `CONTRIBUTIONS.md` |
| **01:00 – 02:30** | 1.5 phút | Kiến trúc hệ thống, luồng xử lý luật (Rule Engine) & các quyết định thiết kế (ADR) | **Đặng Văn Duy** | `REQUIREMENTS.md`, `DECISIONS.md` (C4 / Class Diagram) |
| **02:30 – 05:00** | 2.5 phút | **Live Demo:** Chạy bộ phân loại ca bệnh với dữ liệu giả lập (biên, ngoại lệ, ca khẩn cấp) | **Nguyễn Hoàng Sơn** | Terminal / CLI hoặc giao diện chạy thực tế |
| **05:00 – 06:15** | 1.25 phút | Kiểm thử tự động (84 test cases pass trong 0.48s) & GitHub Actions CI xanh | **Đoàn Bá Quý** | `TEST_REPORT.md`, Tab Actions trên GitHub |
| **06:15 – 07:00** | 0.75 phút | Bảo mật dữ liệu y tế (synthetic data), minh bạch sử dụng AI & Kết luận | **Đoàn Bá Quý** | `SECURITY_PRIVACY_CHECKLIST.md`, `AI_USE.md` |

---

## 2. Kịch bản chi tiết từng phần

### Phần 1: Mở đầu & Tổng quan bài toán (00:00 – 01:00) — *Nguyễn Hoàng Sơn*
* **Lời dẫn:** *"Xin chào thầy và các bạn. Chúng em là Nhóm 26 gồm Hoàng Sơn, Văn Duy và Bá Quý. Nhóm thực hiện Track A — Dr May Day Rule Engine Sprint, xây dựng bộ máy suy diễn luật nhằm phân loại mức độ ưu tiên ca bệnh một cách nhất quán, minh bạch và dễ mở rộng."*
* **Thao tác:** Mở nhanh `Track_A_Development/README.md` và `CONTRIBUTIONS.md` để chốt phạm vi triển khai và trách nhiệm từng thành viên.

### Phần 2: Kiến trúc & Quyết định thiết kế (01:00 – 02:30) — *Đặng Văn Duy*
* **Lời dẫn:** *"Để tránh việc hard-code các điều kiện if-else lồng nhau khó bảo trì, nhóm tách biệt hoàn toàn dữ liệu đầu vào, tập luật và bộ thực thi (Rule Engine)."*
* **Nội dung nhấn mạnh (trên `REQUIREMENTS.md` & `DECISIONS.md`):**
  1. **Luồng xử lý:** Input dữ liệu bệnh nhân $\rightarrow$ Chuẩn hóa & Validate dữ liệu $\rightarrow$ Đánh giá qua chuỗi luật ưu tiên (Red-flag / khẩn cấp trước, các mức nhẹ sau) $\rightarrow$ Trả về kết quả phân loại kèm lý do kích hoạt luật (explainability).
  2. **Lý do chọn thiết kế (ADR):** Dễ dàng thêm/sửa ngưỡng lâm sàng mà không làm thay đổi lõi thực thi; đảm bảo tính tất định (deterministic) — cùng một đầu vào luôn cho một kết quả duy nhất.

### Phần 3: Live Demo thực tế (02:30 – 05:00) — *Nguyễn Hoàng Sơn*
* **Thao tác trên Terminal / Môi trường chạy:**
  * **Kịch bản 1 (Ca khẩn cấp / Red-flag):** Chạy dữ liệu giả lập có dấu hiệu sinh tồn nguy kịch $\rightarrow$ Hệ thống lập tức gắn nhãn mức ưu tiên cao nhất và chỉ rõ luật nào đã kích hoạt.
  * **Kịch bản 2 (Ca thông thường / Theo dõi):** Chạy dữ liệu mức độ nhẹ/trung bình $\rightarrow$ Hệ thống phân loại đúng nhóm và không kích hoạt nhầm cảnh báo khẩn cấp.
  * **Kịch bản 3 (Dữ liệu biên / Thiếu trường thông tin):** Chạy input giá trị biên hoặc thiếu dữ liệu $\rightarrow$ Hệ thống xử lý an toàn (graceful handling), không crash.

### Phần 4: Kiểm thử tự động & CI/CD (05:00 – 06:15) — *Đoàn Bá Quý*
* **Thao tác:**
  1. Chạy trực tiếp lệnh `pytest` trên terminal: show kết quả **84 passed trong 0.48 giây** (bao phủ toàn bộ luồng chính, giá trị biên và ngoại lệ).
  2. Mở tab **GitHub Actions** trên repository để chứng minh workflow `.github/workflows/test.yml` chạy tự động và đạt trạng thái **xanh (Pass)** trên từng commit.
  3. Đối chiếu nhanh với `TEST_REPORT.md`.

### Phần 5: An toàn dữ liệu, AI-Use & Chốt (06:15 – 07:00) — *Đoàn Bá Quý*
* **Nội dung nhấn mạnh:**
  * **Privacy & Security (`SECURITY_PRIVACY_CHECKLIST.md`):** 100% dữ liệu kiểm thử là dữ liệu tổng hợp/giả lập (synthetic data), tuyệt đối không chứa thông tin định danh bệnh nhân thật (PII/PHI).
  * **AI Use (`AI_USE.md`):** Công khai minh bạch các bước dùng AI hỗ trợ sinh test case biên, rà soát tài liệu; toàn bộ logic luật và mã nguồn đều được nhóm kiểm chứng và viết lại.
* **Kết thúc:** *"Phần trình bày của Nhóm 26 xin kết thúc tại đây. Nhóm rất mong nhận được câu hỏi và góp ý từ thầy ạ."*

---

## 3. Checklist chuẩn bị trước giờ Viva (Thứ Bảy 21/11/2026)
- [ ] Mở sẵn VS Code tại thư mục `Track_A_Development`, kích hoạt sẵn virtual environment (`venv`).
- [ ] Mở sẵn trình duyệt với 2 tab: GitHub Repo (tab Actions xanh) và tài liệu thiết kế (`DECISIONS.md`).
- [ ] Mỗi thành viên nắm chắc phần giải thích code của module mình phụ trách để sẵn sàng trả lời chất vấn ngẫu nhiên.
