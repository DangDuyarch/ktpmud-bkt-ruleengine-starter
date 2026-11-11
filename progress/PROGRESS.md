# PROGRESS — Nhóm 26 — Track A

- Starter: ktpmud-bkt-ruleengine-starter · tag bkt-2026-v1 (hoặc v1.1)
- Fork: https://github.com/DangDuyarch/ktpmud-bkt-ruleengine-starter/tree/Track_A_Development

## PC-1 — 11/11/2026

### 1.1. Tiến độ theo acceptance criteria
<!-- Track A: A-01…A-11 · Track B: B-01…B-10 (đề thi Mục 7.3 / 8.3). Đủ mọi mã. -->
| Mã | Trạng thái (Chưa / Đang / Xong) | Bằng chứng (commit / CI / file) | Ghi chú |
|---|---|---|---|
| A-01 | Đang | tests/test_classifier_qa.py | Đã test contract, cần đối chiếu đầy đủ |
| A-02 | Đang | Review code | Chưa xác minh đầy đủ |
| A-03 | Đang | 79 test PASS | Đã test nhiều rule và ngưỡng biên |
| A-04 | Xong | tests/test_classifier_qa.py | Có test missing, invalid, sai kiểu |
| A-05 | Đang | tests/test_classifier_qa.py | Cần rà soát toàn bộ nội dung lý do |
| A-06 | Đang | rule_engine/classifier.py | Đã chuyển log ra ngoài repo, cần kiểm tra thêm |
| A-07 | Xong | 79 test PASS | Đã có bộ test mở rộng |
| A-08 | Đang | python -m pytest -v | Chưa xác minh clean checkout |
| A-09 | Chưa | Chưa có bằng chứng CI | Cần kiểm tra CI trên Pull Request |
| A-10 | Chưa | Chưa có benchmark | Cần đo ít nhất 1.000 lần |
| A-11 | Chưa | Chưa rà README | Cần kiểm tra cảnh báo và hướng dẫn |

### 1.2. Sửa đổi bắt buộc từ Checkpoint 1
<!-- Các mục ❗ trong nhận xét Checkpoint 1 của nhóm. Nếu không có, ghi "Không có". -->
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

## PC-2 — 18/11/2026

### 2.1. Đối chiếu timeline PC-1
| Việc (theo bảng 1.3) | Kế hoạch | Thực tế | Lệch & lý do |
|---|---|---|---|

### 2.2. Tiến độ theo acceptance criteria (cập nhật toàn bộ bảng 1.1)
| Mã | Trạng thái | Bằng chứng | Ghi chú |
|---|---|---|---|

### 2.3. Sẵn sàng nộp bài (đề thi Mục 6)
| Deliverable | Có / Chưa | Đường dẫn |
|---|---|---|
| README.md (cài đặt / chạy / test) | | |
| REQUIREMENTS.md | | |
| DECISIONS.md / ADR | | |
| Test tự động + CI xanh | | |
| TEST_REPORT.md | | |
| SECURITY_PRIVACY_CHECKLIST.md | | |
| AI_USE.md | | |
| CONTRIBUTIONS.md | | |
| Slide / demo script ≤ 7 phút | | |
| Draft PR vào `ktpmud-project`, check `validate` xanh | | |

### 2.4. Việc còn lại đến Freeze (23:59 19/11)
| Việc | Vai trò phụ trách | Hạn |
|---|---|---|

### 2.5. Rủi ro / câu hỏi cho GV
- 

## Kết quả cuối — Freeze 19/11/2026
- Tag: bkt-2026-<mã nhóm>-rc1 · SHA: 
- Trạng thái cuối từng mã AC: (cập nhật bảng 2.2 hoặc ghi "như 2.2 trừ: …")
- Những việc trong timeline chưa hoàn thành và lý do: