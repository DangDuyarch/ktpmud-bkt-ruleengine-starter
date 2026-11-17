# BÁO CÁO NHÓM 26 — CHÍNH SÁCH SỬ DỤNG AI (AI_USE.MD)
**Môn:** Kỹ thuật Phần mềm ứng dụng (Track A — Dr May Day: Rule Engine Sprint)

---

## 1. Đặng Văn Duy

| Trường thông tin | Nội dung chi tiết |
| :--- | :--- |
| **Người chịu trách nhiệm** | Đặng Văn Duy |
| **Công cụ/model** | ChatGPT (GPT-4o) / Claude 3.5 Sonnet |
| **Mục đích** | • Hỗ trợ cấu trúc hóa tài liệu yêu cầu (REQUIREMENTS) và hệ thống hóa các quyết định thiết kế (DECISIONS) theo chuẩn ADR.<br>• Giải thích các vấn đề kỹ thuật liên quan đến Python Rule Engine, validation, xử lý dữ liệu thiếu và audit.<br>• Rà soát tính nhất quán giữa yêu cầu chức năng, yêu cầu phi chức năng, tiêu chí nghiệm thu và quyết định thiết kế.<br>• Đề xuất các trường hợp kiểm thử, tình huống biên và phương pháp kiểm chứng. |
| **Phạm vi** | • Thư mục tài liệu (`docs/`) gồm `DECISIONS.md` và `REQUIREMENTS.md`.<br>• Đề chính thức KTPMUD Hack Marathon 2026 — Track A.<br>• Các commit phát triển trên nhánh `feat/duy-requirements`.<br>• Các file trong repo `ktpmud-project` được fork về của nhóm. |
| **Kiểm chứng** | • Review thủ công: Đọc và so sánh nội dung AI gợi ý để đối chiếu trực tiếp với `docs/decision-table.md` (tag `bkt-2026-v1`).<br>• Đối chiếu Data Dictionary, 9 trường đầu vào và 3 trường đầu ra.<br>• Kiểm tra sự phân biệt giữa dữ liệu thiếu hợp lệ, sai kiểu và sai miền giá trị… |
| **Quyết định của nhóm** | • **Giữ:** Cấu trúc REQUIREMENTS gồm FR, NFR, AC và Traceability, Các đề xuất xử lý missing/null.<br>• **Sửa:** Các đề xuất validation và exception, Các đề xuất về audit.<br>• **Loại bỏ:** Các đề xuất không có nguồn xác minh hoặc làm thay đổi nghiệp vụ. |

---

## 2. Nguyễn Hoàng Sơn

| Trường thông tin | Nội dung chi tiết |
| :--- | :--- |
| **Người chịu trách nhiệm** | Nguyễn Hoàng Sơn |
| **Công cụ/model** | ChatGPT (GPT-4o) / Claude 3.5 Sonnet (phiên bản 2026) |
| **Mục đích** | • Hỗ trợ triển khai logic phân loại 2 tầng, logic ba trạng thái và cơ chế ghi audit fail-closed trong `rule_engine/classifier.py`.<br>• Hỗ trợ thiết kế và xây dựng bộ Unit Test (`tests/test_classifier.py`) nhằm bao phủ các tiêu chí nghiệm thu từ A-01 đến A-08 và danh mục bảo mật SEC-02 đến SEC-11. |
| **Phạm vi** | • File `rule_engine/classifier.py` và `tests/test_classifier.py`.<br>• Các commit phát triển trên nhánh `feat/son-classifier`. |
| **Kiểm chứng** | • Chạy thực thi trực tiếp toàn bộ test suite bằng lệnh `pytest -q` từ clean checkout để xác thực tất cả các test case đều pass thành công.<br>• Kiểm tra chéo (peer review) để đảm bảo các test case phản ánh chính xác quy tắc ba trạng thái và các ràng buộc Zero PII. |
| **Quyết định của nhóm** | • **Giữ:** Cấu trúc tổ chức test thành các nhóm rõ ràng (Test ma trận lâm sàng, Test validation lỗi, Test audit trail & fail-closed) vì giúp dễ kiểm soát độ bao phủ (code coverage).<br>• **Sửa:** Tinh chỉnh lại cơ chế cô lập thư mục log sử dụng `tmp_path` và `monkeypatch` để các bài test kiểm tra I/O lỗi hoạt động ổn định trên mọi hệ điều hành (Windows/Linux). |

---

## 3. Đoàn Bá Quý

| Trường thông tin | Nội dung chi tiết |
| :--- | :--- |
| **Người chịu trách nhiệm** | Đoàn Bá Quý |
| **Công cụ/model** | ChatGPT (GPT-4o) |
| **Mục đích** | • Hỗ trợ xây dựng và mở rộng bộ kiểm thử QA độc lập tại `tests/test_classifier_qa.py` nhằm kiểm tra logic phân loại trong `rule_engine/classifier.py` theo đặc tả REQUIREMENTS v1.1 và bảng quyết định `docs/decision-table.md`.<br>• Thiết kế các trường hợp kiểm thử biên và bảo mật, bao gồm ngưỡng huyết áp theo nhóm tuổi, mức giảm huyết áp đúng 30% và trên 30%, logic ba trạng thái TRUE/FALSE/UNKNOWN, từ chối khóa ngoài allowlist và kiểm tra nội dung `ly_do` không làm lộ dữ liệu đầu vào thô.<br>• Hỗ trợ xây dựng, rà soát và cập nhật các tài liệu QA: `docs/TEST_PLAN.md`, `docs/AC_TRACEABILITY.md` và `docs/SECURITY_PRIVACY_CHECKLIST.md`. |
| **Phạm vi** | • `tests/test_classifier_qa.py`.<br>• `docs/TEST_PLAN.md`, `docs/AC_TRACEABILITY.md`, `docs/SECURITY_PRIVACY_CHECKLIST.md`.<br>• Nhánh phát triển `test/quy-qa-security`. |
| **Kiểm chứng** | • Chạy `python -m pytest -v` trên môi trường cục bộ. Kết quả kiểm thử mới nhất đã ghi nhận: 84 passed, 0 failed trong 0.41 giây, gồm 67 test trong `tests/test_classifier_qa.py` và 17 test trong `tests/test_classifier.py`. Kết quả này phản ánh lần chạy đã được báo cáo, không thay thế việc chạy lại trên commit cuối cùng trước khi nộp.<br>• Rà soát mã nguồn `rule_engine/classifier.py` và đối chiếu các điều kiện R01, R02, R03, R-SOC với `docs/decision-table.md`. Việc xác minh toàn bộ trường hợp biên và tất cả expected output cần dựa trên kết quả rà soát, không chỉ dựa vào việc pytest thành công.<br>• Sử dụng `git status --short` và `git diff --check` để kiểm tra thay đổi trong working tree và các lỗi khoảng trắng. Việc xác nhận trạng thái commit/push, các tệp audit log và CI cần kiểm tra riêng trên trạng thái repository tương ứng. |
| **Quyết định của nhóm** | • **Giữ:** Cách tổ chức bộ kiểm thử theo nhóm chức năng, nghiệp vụ và bảo mật để hỗ trợ kiểm tra chéo với unit test của phần phát triển.<br>• **Sửa:** Cập nhật trạng thái trong `AC_TRACEABILITY.md` và `SECURITY_PRIVACY_CHECKLIST.md` theo bằng chứng thực tế. Phân biệt rõ các mục đã có kết quả kiểm thử với các mục còn cần xác minh, chẳng hạn CI, benchmark p50/p95 có tính thời gian ghi audit và vị trí lưu audit log. Không đánh dấu hoàn tất chỉ dựa trên suy đoán hoặc kết quả của một lần chạy test. |
