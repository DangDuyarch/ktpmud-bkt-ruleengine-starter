# Phân công và Đóng góp Thành viên (`CONTRIBUTIONS.md`)

## 1. Thông tin chung

* **Dự án:** KTPMUD Hack Marathon 2026
* **Track:** Track A — Dr May Day: Rule Engine Sprint
* **Nhóm:** Nhóm 26
* **Repository phát triển:** `https://github.com/DangDuyarch/ktpmud-bkt-ruleengine-starter`
* **Cảnh báo bắt buộc:** `educational/synthetic — not for clinical use`

---

## 2. Bảng tổng hợp phân công và đóng góp

| STT | Thành viên | Mã sinh viên | Vai trò chính | Nhiệm vụ & Sản phẩm bàn giao | Bằng chứng đối chiếu (Nhánh / File / PR) |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | **Đặng Văn Duy** | `202414085` | **Trưởng nhóm** (Spec, Architecture & PR Lead) | • Phân tích đặc tả nghiệp vụ từ `docs/decision-table.md` (`bkt-2026-v1`), biên soạn và hiệu chỉnh `REQUIREMENTS.md` (v1.1).<br>• Quản lý cấu trúc repository, nhánh phát triển (`Track_A_Development`, `main`), thực hiện code review và hợp nhất các Pull Request của thành viên.<br>• Tổng hợp tài liệu `README.md`, `AI_USE.md`, kịch bản thuyết trình (`DEMO_SCRIPT.md`) và thực hiện mở Draft PR nộp bài vào `ktpmud-project`. | • Nhánh `main`, `Track_A_Development`<br>• `REQUIREMENTS.md`<br>• `README.md`<br>• `AI_USE.md`<br>• `docs/DEMO_SCRIPT.md` |
| 2 | **Nguyễn Hoàng Sơn** | `202414349` | **Core Logic & Architecture Lead** | • Thiết kế kiến trúc phân loại 2 tầng và ghi nhận quyết định thiết kế trong `docs/adr/001-rule-engine-architecture.md`.<br>• Hiện thực toàn bộ module phân loại `rule_engine/classifier.py` (logic Tầng 2: `R01-PV`, `R02-PV`, `R03-PV`; Tầng 1: `R-SOC`; logic ba trạng thái `TRUE/FALSE/UNKNOWN`).<br>• Xây dựng bộ kiểm tra đầu vào nghiêm ngặt (Zero PII) và cơ chế ghi audit trail 4 trường fail-closed (`AuditError`) nằm ngoài repository.<br>• Viết bộ unit test cốt lõi (`tests/test_classifier.py`) và xử lý cấu hình `sys.path` giúp CI runner vượt qua kiểm thử tự động. | • Nhánh `feat/son-classifier`<br>• `rule_engine/classifier.py`<br>• `tests/test_classifier.py`<br>• `docs/adr/001-rule-engine-architecture.md` |
| 3 | **Đoàn Bá Quý** | `202414338` | **QA & Security Lead** | • Xây dựng bộ kiểm thử QA độc lập mở rộng (`tests/test_classifier_qa.py`), nâng tổng số test case vượt qua lên 79/79 test cases.<br>• Kiểm thử chuyên sâu các trường hợp biên huyết áp theo 4 nhóm tuổi, giảm huyết áp đúng 30% vs trên 30%, và chống rò rỉ dữ liệu trong `ly_do`.<br>• Soạn thảo Kế hoạch kiểm thử (`docs/TEST_PLAN.md`), Bảng truy vết tiêu chí nghiệm thu (`docs/AC_TRACEABILITY.md`) và Checklist bảo mật & quyền riêng tư (`docs/SECURITY_PRIVACY_CHECKLIST.md`). | • Nhánh `test/quy-qa-security`<br>• `tests/test_classifier_qa.py`<br>• `docs/TEST_PLAN.md`<br>• `docs/AC_TRACEABILITY.md`<br>• `docs/SECURITY_PRIVACY_CHECKLIST.md` |

---

## 3. Quy trình phối hợp & Kiểm soát chất lượng

1. **Phân nhánh độc lập (Feature Branch Workflow):** Mỗi thành viên phát triển trên nhánh riêng (`feat/son-classifier`, `test/quy-qa-security`) và không push trực tiếp vào nhánh chính.
2. **Kiểm tra chéo (Peer Review):** Mọi thay đổi về mã nguồn và tài liệu đều được đối chiếu chéo giữa Dev (Sơn), QA (Quý) và Trưởng nhóm (Duy) trước khi hợp nhất.
3. **Xác thực tự động (CI):** Tất cả các commit và Pull Request đều bắt buộc chạy qua bộ kiểm thử tự động `pytest` trên GitHub Actions và kiểm tra trạng thái sạch bằng `git status` / `git diff --check` để đảm bảo không lọt log `.audit_logs/` hoặc dữ liệu nhạy cảm vào repository.
