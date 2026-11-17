# PROGRESS — Nhóm 26 — Track A

- Starter: ktpmud-bkt-ruleengine-starter · tag bkt-2026-v1 (hoặc v1.1)
- Fork: https://github.com/DangDuyarch/ktpmud-bkt-ruleengine-starter/tree/Track_A_Development

## PC-1 — 11/11/2026

### 1.1. Tiến độ theo acceptance criteria
| Mã | Trạng thái (Chưa / Đang / Xong) | Bằng chứng (commit / CI / file) | Ghi chú |
|---|---|---|---|
| A-01 | Đang | tests/test_classifier_qa.py; commit c19db18 | Đã có test contract nhưng chưa đối chiếu đầy đủ với yêu cầu classify(). Cần kiểm tra trực tiếp các input tổng quát, output và xác nhận không còn NotImplementedError. |
| A-02 | Đang | Mã nguồn cần review; commit c19db18 liên quan đến mở rộng test QA | Chưa có kết quả review xác nhận không hard-code ID của public fixture. Cần kiểm tra code và thử với fixture độc lập. |
| A-03 | Đang | tests/test_classifier_qa.py; kết quả python -m pytest -v: 79 passed | Đã có bộ test mở rộng nhưng chưa có bảng đối chiếu chứng minh bao phủ đầy đủ decision table, các tầng phân loại, trường hợp overlap và giá trị sát biên. |
| A-04 | Đang | tests/test_classifier_qa.py; kết quả python -m pytest -v: 79 passed | Cần đối chiếu từng test với các trường hợp missing/null/invalid, khóa lạ, dữ liệu ngoài miền và xử lý TypeError/ValueError theo policy. Chưa đánh dấu Xong khi chưa xác minh đủ. |
| A-05 | Đang | tests/test_classifier_qa.py; kết quả python -m pytest -v: 79 passed | Cần kiểm tra assertion của ly_do, khả năng truy vết rule, không chứa lời khuyên điều trị và kết quả nhất quán khi chạy lặp cùng input. |
| A-06 | Đang | rule_engine/classifier.py; đã thử cấu hình AUDIT_LOG_DIR để lưu log ngoài repo trong phiên Git Bash | Chưa có bằng chứng đầy đủ về nội dung audit đúng bốn trường, không ghi raw clinical input, xử lý lỗi ghi log và kiểm tra PII/secret trong repo. Cần kiểm tra cả hành vi khi không cấu hình biến môi trường. |
| A-07 | Đang | tests/test_classifier_qa.py; kết quả python -m pytest -v: 79 passed; commit c19db18 | Đã có bộ test QA mở rộng và chạy thành công. Cần đối chiếu, xác nhận đủ test normal, boundary, invalid và missing, đồng thời xác nhận bộ test đáp ứng yêu cầu thay thế test stub. |
| A-08 | Đang | Kết quả chạy python -m pytest -v: 79 passed trên máy hiện tại | Chưa có bằng chứng chạy pytest -q thành công từ clean checkout. Cần ghi lại lệnh và kết quả chạy thực tế từ môi trường sạch. |
| A-09 | Chưa | Chưa có URL lượt chạy CI thành công được xác nhận | Cần cung cấp link CI chạy test thành công trên Pull Request. |
| A-10 | Chưa | Chưa có script và kết quả benchmark được xác nhận | Cần benchmark ít nhất 1.000 lần, báo cáo p50/p95, xác nhận p95 dưới 100 ms, nêu cấu hình máy đo và tính cả thời gian audit. |
| A-11 | Chưa | Chưa có bằng chứng review README được xác nhận | Cần kiểm tra README có cảnh báo “educational/synthetic — not for clinical use” và hướng dẫn cài đặt, chạy chương trình, chạy test. |

### 1.2. Sửa đổi bắt buộc từ Checkpoint 1
Không có — nhóm không nhận được mục sửa đổi bắt buộc nào.

### 1.3. Timeline dự kiến đến khi hoàn thành
| Việc | Vai trò phụ trách | Mốc (CP2 15/11 · M3 · Freeze 19/11 · M4 20/11) | Ngày dự kiến |
|---|---|---|---|
| Hoàn thiện kiểm thử và đối chiếu AC | QA | CP2 | 15/11/2026 |
| Xác minh CI và README | Dev/QA | M3 | Theo kế hoạch nhóm |
| Hoàn tất benchmark và rà soát bảo mật | QA/Dev | Freeze | 19/11/2026 |
| Kiểm tra cuối và bàn giao | Cả nhóm | M4 | 20/11/2026 |

### 1.4. Rủi ro / đang vướng
- Chưa xác minh CI trên Pull Request.
- Chưa có bằng chứng benchmark đạt ngưỡng p95 dưới 100 ms.
- Cần rà soát lại audit log và các yêu cầu bảo mật liên quan.

### 1.5. Câu hỏi cho GV
- Q1: Những tiêu chí chưa có đủ bằng chứng ở PC-1 có bắt buộc hoàn tất trước CP2 không?
- Q2 (Thứ tự ưu tiên Rule Tầng 2): Khi có nhiều rule Tầng 2 cùng khớp, việc áp dụng thứ tự ưu tiên `R01 > R02 > R03` (D01) đã đúng với đáp án mẫu chưa?
- Q3 (Xử lý null/thiếu dữ liệu): Cơ chế xử lý trường hợp thiếu boolean, thiếu tuổi ở Tầng 2 hoặc thiếu HATT/bệnh nền theo mục 4.3, 4.4 (D02, D03) có cần điều chỉnh gì không?
- Q4 (Miền giá trị hợp lệ): Quy ước biên dữ liệu (`HATT = 0` hợp lệ, `nền = 0` không hợp lệ, không giới hạn trần) (D04) đã chuẩn xác chưa?
- Q5 (Format Audit Log): Định dạng `Action_Type`/`Status`, `Timestamp`/`User UUID` và đường dẫn file audit theo mục 6 (D07, D08) có cần bổ sung trường thông tin nào không?

### 1.6. Phân công (alias hoặc vai trò, KHÔNG ghi họ tên/MSSV)
| Alias / vai trò | Đầu việc chính | Commit/PR tiêu biểu |
|---|---|---|
| QA | Test, traceability, checklist bảo mật | `de522a4db2d8cdc1a30e7c8e38df5faf0ae076bb`<br>`a0afe66dbf60a41089e336beecc282cf41015013`<br>`ebbf20ff1eaf8f232ec7e88ffafd6fa04e148c6e`<br>`5f7387aff133f8a2f078a928672abb76a51a2d02`<br>`c19db187c3016dd092a1685c1505ee670a29096c` |
| Dev | Triển khai rule engine | `4f75a76d3188fbb9314b62527cb5033f0b345c4b`<br>`1e5afde48b462309d26b8376071dcf87bdd876c7`<br>`570f04a146e10206b025688ec3848c7be17fa9ba` |
| Spec | Requirements và Decision table | `d4f708477406ec90509be60ffe5e4709f703a498`<br>`d39f2b85695fc49158026d63f15214ff7cab1282` |

---

## 2. PC-2 — 18/11/2026

### 2.1. Đối chiếu timeline PC-1
| Việc theo kế hoạch | Kế hoạch | Thực tế | Lệch và lý do |
|---|---|---|---|
| Hoàn thiện kiểm thử và đối chiếu AC | Hoàn thành tại PC-2 | Bộ test QA đã được mở rộng; lần chạy mới nhất đạt 84 passed trong 0.48 giây | Đã có kết quả test cục bộ nhưng cần đối chiếu từng AC và xác minh clean checkout. |
| Xác minh CI và README | Hoàn thành tại mốc M3 | Chưa có URL CI xanh được xác nhận; README chưa có bằng chứng review cuối cùng | Chưa đủ bằng chứng để kết luận hoàn thành. |
| Hoàn tất benchmark và rà soát bảo mật | Hoàn thành trước Freeze 19/11 | Đã có thay đổi liên quan đến audit và test; chưa có báo cáo benchmark đạt ngưỡng | Cần chạy benchmark và kiểm tra lại audit log, fail-closed, quyền riêng tư. |
| Kiểm tra cuối và bàn giao | M4 ngày 20/11 | Chưa có bằng chứng hoàn tất bàn giao | Tiếp tục sau khi chốt các tiêu chí và deliverable bắt buộc. |

### 2.2. Tiến độ theo Acceptance Criteria
| Mã | Trạng thái tại PC-2 | Bằng chứng | Ghi chú / việc còn lại |
|---|---|---|---|
| A-01 | Cần đối chiếu bằng chứng cuối | docs/decision-table.md, rule_engine/classifier.py, tests/test_classifier.py | Xác nhận đầu vào, đầu ra và hành vi phân loại theo yêu cầu chính thức. |
| A-02 | Cần đối chiếu bằng chứng cuối | docs/decision-table.md, tests/test_classifier.py, tests/test_classifier_qa.py | Xác nhận các rule và điều kiện tương ứng với decision table. |
| A-03 | Cần đối chiếu bằng chứng cuối | docs/decision-table.md, tests/test_classifier.py, tests/test_classifier_qa.py | Xác nhận thứ tự ưu tiên R01 > R02 > R03 và các tình huống nhiều rule cùng khớp. |
| A-04 | Đã có test cho dữ liệu đầu vào; cần đối chiếu đầy đủ AC | tests/test_classifier_qa.py, tests/test_classifier.py | Xác nhận đầy đủ trường hợp missing/null, kiểu dữ liệu và miền giá trị. |
| A-05 | Đã có kiểm thử cấu trúc đầu ra; cần đối chiếu đầy đủ AC | tests/test_classifier.py, tests/test_classifier_qa.py | Xác nhận đầu ra chỉ có muc_do, rule_id, ly_do. |
| A-06 | Đã có kiểm thử lỗi và tính nhất quán; cần đối chiếu đầy đủ AC | tests/test_classifier_qa.py, tests/test_classifier.py | Kiểm tra lại mọi yêu cầu xử lý lỗi và các trường hợp biên trong đặc tả. |
| A-07 | Đã có bộ test QA mở rộng | tests/test_classifier_qa.py; commit c19db187c3016dd092a1685c1505ee670a29096c; 84 passed trong 0.48 giây | Cần xác nhận phạm vi test đáp ứng đầy đủ yêu cầu thay thế test stub. |
| A-08 | Test cục bộ đã chạy thành công; clean checkout chưa xác minh | python -m pytest -v: 84 passed trong 0.48 giây | Chạy lại test từ clean checkout bằng pytest -q hoặc python -m pytest -q. |
| A-09 | Chưa xác minh | .github/workflows/test.yml; chưa có URL CI xanh được xác nhận | Kiểm tra GitHub Actions trên PR và lưu URL lượt chạy thành công. |
| A-10 | Chưa xác minh | Chưa có báo cáo benchmark đầy đủ | Đo tối thiểu 100 warm-up và 1.000 lần; báo cáo p50/p95, cấu hình máy và thời gian audit. |
| A-11 | Chưa xác minh đầy đủ | Chưa có bằng chứng review README cuối cùng | Xác nhận cảnh báo sử dụng và hướng dẫn cài đặt/chạy/test. |

### 2.3. Sẵn sàng nộp bài — theo Mục 6 đề thi
| Deliverable | Có / Chưa / Trạng thái | Đường dẫn / bằng chứng |
|---|---|---|
| README.md — cài đặt / chạy / test | Có | Track_A_Development/ README.md |
| REQUIREMENTS.md | Có | Track_A_Development/docs/ REQUIREMENTS.md |
| DECISIONS.md / ADR | Có | Track_A_Development/docs/ DECISIONS.md |
| Test tự động + CI xanh | Có | tests/, .github/workflows/test.yml; kết quả local: 84 passed trong 0.48 giây. |
| TEST_REPORT.md | Có | Track_A_Development/docs/ TEST_REPORT.md |
| SECURITY_PRIVACY_CHECKLIST.md | Có | Track_A_Development/docs/SECURITY_PRIVACY_CHECKLIST.md |
| AI_USE.md | Có | Track_A_Development/docs/ AI_USE.md |
| CONTRIBUTIONS.md | Có | Track_A_Development/docs/ CONTRIBUTIONS.md |
| Slide / demo script không quá 7 phút | Chưa | Cần xác nhận với nhóm và kiểm tra nội dung demo. |
| Draft PR vào ktpmud-project, check validate xanh | Có | https://github.com/fossbk-spec/ktpmud-project/pull/33 |

### 2.4. Việc còn lại đến Freeze — 23:59 ngày 19/11/2026
| Việc | Vai trò phụ trách | Hạn |
|---|---|---|
| Rà soát 5 file đang thay đổi, kiểm tra diff và chạy lại test | QA/Dev | Trước khi commit |
| Chốt bảng AC và bảo đảm tài liệu thống nhất với hành vi thực tế | QA/Spec/Dev | Trước Freeze |
| Chạy pytest -q hoặc python -m pytest -q từ clean checkout và lưu kết quả | QA | Trước Freeze |
| Xác nhận GitHub Actions chạy thành công trên PR | Dev/QA | Trước Freeze |
| Benchmark 100 warm-up và 1.000 lần đo; báo cáo p50/p95 và cấu hình máy | Dev/QA | Trước Freeze |
| Rà soát audit log, quyền riêng tư, fail-closed và đường dẫn log | QA/Dev | Trước Freeze |
| Review README: cảnh báo sử dụng, cài đặt, chạy chương trình và test | QA/Dev | Trước Freeze |
| Kiểm tra các deliverable bắt buộc và cấu trúc thư mục theo đề | Cả nhóm | Trước Freeze |
| Tạo draft PR vào đúng repo/nhánh đích, xác nhận validate xanh | Dev/Leader | Trước Freeze |
| Kiểm tra tag, SHA và trạng thái cuối của từng AC | Cả nhóm | 23:59, 19/11/2026 |

### 2.5. Rủi ro / câu hỏi cho giảng viên
- Cần xác nhận các tiêu chí chưa đủ bằng chứng tại PC-2 có bắt buộc phải hoàn tất trước Freeze hay không.
- Cần xác nhận các quy ước dữ liệu biên và thứ tự ưu tiên rule với đáp án mẫu.
- Cần thống nhất yêu cầu audit log, cách chứng minh không lưu dữ liệu đầu vào nhạy cảm và hành vi khi ghi audit thất bại.
- Cần xác nhận đúng cấu trúc thư mục, tên deliverable, nhánh đích và điều kiện CI của draft PR.

---

## 3. Kết quả cuối — Freeze 19/11/2026
- Tag: bkt-2026-<mã nhóm>-rc1 · SHA: 
- Trạng thái cuối từng mã AC: (cập nhật bảng 2.2 hoặc ghi "như 2.2 trừ: …")
- Những việc trong timeline chưa hoàn thành và lý do:

