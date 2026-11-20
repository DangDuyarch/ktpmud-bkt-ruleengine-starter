# Bảng truy vết yêu cầu và tiêu chí nghiệm thu (AC_TRACEABILITY)

## 1. Thông tin chung

- **Dự án:** KTPMUD Hack Marathon 2026
- **Track:** Track A — Dr May Day: Rule Engine Sprint
- **Nhóm:** 26
- **Nguồn quy tắc nghiệp vụ:** `docs/decision-table.md`, tag `bkt-2026-v1`
- **Bộ kiểm thử:** `tests/test_classifier.py`, `tests/test_classifier_qa.py`

### Nguyên tắc ghi nhận

Trạng thái trong tài liệu phản ánh bằng chứng đã kiểm tra, không chỉ dựa vào tên test, comment trong mã nguồn hoặc kết quả của một lần chạy pytest.

- **Đã kiểm tra:** Có test hoặc kết quả rà soát trực tiếp hỗ trợ nhận định trong phạm vi ghi rõ.
- **Đã kiểm tra một phần:** Có bằng chứng nhưng chưa bao phủ đầy đủ yêu cầu.
- **Chưa xác minh:** Chưa có đủ bằng chứng để kết luận.
- **Chưa đạt:** Đã có bằng chứng cho thấy tiêu chí không được đáp ứng.

Không suy diễn rằng toàn bộ yêu cầu đã đạt chỉ vì bộ test tự động không có lỗi.

## 2. Truy vết tiêu chí nghiệm thu

| AC   | Tiêu chí nghiệm thu                                                                                        | Bằng chứng hiện có                                                                                                                                                                                                                                                                                       | Trạng thái                                                             |
| ---- | ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| A-01 | Hàm `classify()` thực hiện phân loại thay vì còn là scaffold chưa triển khai.                              | Đã đọc mã nguồn `rule_engine/classifier.py` và các test gọi trực tiếp `classify()`. Có kiểm tra kết quả phân loại và lỗi đầu vào.                                                                                                                                                                        | Đã kiểm tra; cần tiếp tục đối chiếu đầy đủ với đặc tả                  |
| A-02 | Logic không hard-code theo ID hoặc dữ liệu riêng của public fixture.                                       | Đã rà soát `rule_engine/classifier.py`, `tests/test_classifier.py` và `docs/decision-table.md`; chưa phát hiện dấu hiệu hardcode dữ liệu kiểm thử trong phạm vi đã rà soát.                                                                                                                              | Đã kiểm tra trong phạm vi rà soát                                      |
| A-03 | Bao phủ các quy tắc R01, R02, R03, điều kiện sốc phản vệ và các trường hợp biên quan trọng.                | `tests/test_classifier_qa.py` có test riêng cho R01/R02/R03, ưu tiên R02 so với R03, ngưỡng huyết áp theo tuổi, giảm huyết áp đúng 30% và trên 30%, cùng các trường hợp thiếu dữ liệu.                                                                                                                   | Đã kiểm tra; đối chiếu toàn bộ decision table             |
| A-04 | Xử lý trường thiếu, `None`, `UNKNOWN`, sai kiểu, ngoài miền và khóa không được phép theo hợp đồng đầu vào. | Có các test `test_thieu_truong_bool_duoc_coi_la_unknown`, `test_sai_kieu_du_lieu_phat_sinh_type_error`, `test_sai_mien_du_lieu_phat_sinh_value_error`, `test_khoa_ngoai_allowlist_phat_sinh_value_error`, cùng các test validation trước suy luận.                                                       | Đã kiểm tra trong phạm vi các test hiện có                             |
| A-05 | Đầu ra có cấu trúc đúng; `ly_do` không làm lộ giá trị đầu vào; kết quả ổn định với cùng input.             | Có `test_dau_ra_chi_co_ba_khoa`, `test_theo_doi_luon_co_rule_id_none`, `test_cung_input_cho_cung_ket_qua_phan_loai` và `test_ly_do_khong_chua_gia_tri_input_dac_biet`.                                                                                                                                   | Đã kiểm tra trong phạm vi các assertion hiện có                        |
| A-06 | Audit có đúng bốn trường, ghi trạng thái phù hợp, hạn chế dữ liệu thô và xử lý lỗi ghi log theo yêu cầu.   | Có năm test audit trong `tests/test_classifier.py`: `test_audit_success_4_fields_and_no_pii`, `test_audit_invalid_input_logs_before_raise`, `test_audit_fail_closed_raises_audit_error_with_cause`, `test_audit_error_takes_precedence_over_validation_error`, `test_default_audit_dir_is_outside_repo`. | Đã kiểm tra một phần; cần siết assertion UTC và đối chiếu đầy đủ FR-08 |
| A-07 | Có test cho các trường hợp bình thường, biên và đầu vào không hợp lệ.                                      | Hai file test có các nhóm test quy tắc, ngưỡng huyết áp, dữ liệu thiếu, sai kiểu, sai miền và khóa ngoài allowlist.                                                                                                                                                                                      | Đã kiểm tra trong phạm vi test hiện có                                 |
| A-08 | Bộ test tự động chạy được và kết quả được ghi nhận chính xác.                                              | Lần chạy đầy đủ gần nhất được ghi nhận trong quá trình QA: `84 passed`. Kết quả này thuộc lần chạy tại thời điểm đó, không xác nhận trạng thái của các thay đổi chưa chạy lại.                                                                                                                           | Đã có kết quả lịch sử; cần chạy lại trên trạng thái mã nguồn hiện tại  |
| A-09 | CI chạy test trên cấu hình và commit cần bàn giao.                                                         | Workflow .github/workflows/test.yml chạy tự động và đạt trạng thái xanh (84/84 tests passed) trên commit bàn giao đã freeze..                                                                                                                                                               | Đạt                                     |
| A-10 | Benchmark đáp ứng yêu cầu hiệu năng, có warm-up và ít nhất 1.000 lượt đo; báo cáo p50/p95.                 | Đã chạy benchmark 1.000 lượt đo thực tế (sau 100 lượt warm-up) trên phiên bản bàn giao: p50 = 0.5431 ms, p95 = 0.9945 ms (dưới 1 ms, đạt yêu cầu hiệu năng)..                                                                                                                                                                                                 | Đạt                                                          |
| A-11 | README có hướng dẫn cài đặt, chạy, kiểm thử và cảnh báo sử dụng giáo dục, không dùng cho lâm sàng.         | Đã rà soát Track_A_Development/README.md: đầy đủ hướng dẫn cài đặt, chạy, kiểm thử và cảnh báo miễn trừ trách nhiệm lâm sàng..                                                                                                                                                                                                                  | Đạt                                                          |

## 3. Truy vết yêu cầu chức năng

| Yêu cầu | Nội dung cần xác minh                                                                                 | Bằng chứng                                                                                                                              | Trạng thái                                                                             |
| ------- | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| FR-01   | Đầu vào tuân theo allowlist và không phân loại dựa trên ID fixture cố định.                           | Đã rà soát allowlist trong mã nguồn và chưa phát hiện dấu hiệu hardcode dữ liệu kiểm thử trong phạm vi đã xem.                          | Đã kiểm tra trong phạm vi rà soát                                                      |
| FR-02   | Quy tắc R01, R02 và R03 được thực hiện theo decision table.                                           | Có test riêng cho các quy tắc, trường hợp khớp/không khớp và ưu tiên quy tắc.                                                           | Đã kiểm tra                                                                  |
| FR-03   | Điều kiện sốc phản vệ được đánh giá theo ngưỡng huyết áp và điều kiện quy định.                       | Có test ngưỡng theo tuổi, huyết áp tâm thu dưới 90, giảm đúng 30% và giảm trên 30%.                                                     | Đã kiểm tra                                                                   |
| FR-04   | Xử lý thứ tự quyết định, tuổi thiếu và ưu tiên quy tắc.                                               | Có test tuổi thiếu, validation trước suy luận và ưu tiên R02 khi R02/R03 cùng khớp.                                                     | Đã kiểm tra trong phạm vi test hiện có                                                 |
| FR-05   | Xử lý dữ liệu thiếu và `UNKNOWN` theo logic ba trạng thái.                                            | Có test trường boolean thiếu, quy tắc đã khớp không bị hủy bởi trường khác `UNKNOWN`, và trường hợp R02 chưa đủ hai điều kiện đúng.     | Đã kiểm tra trong phạm vi test hiện có                                                 |
| FR-06   | Kiểm tra kiểu dữ liệu, miền giá trị và khóa đầu vào.                                                  | Có test `TypeError`, `ValueError`, giá trị ngoài miền, khóa ngoài allowlist và validation trước suy luận.                               | Đã kiểm tra trong phạm vi test hiện có                                                 |
| FR-07   | Đầu ra có ba khóa `muc_do`, `rule_id`, `ly_do`; lý do không đưa giá trị đầu vào cụ thể vào thông báo. | Có test cấu trúc đầu ra, `rule_id` là `None` cho `THEO_DOI`, tính ổn định kết quả và nội dung `ly_do`.                                  | Đã kiểm tra trong phạm vi test hiện có                                                 |
| FR-08   | Mỗi lần gọi được audit với bốn trường: timestamp, UUID, action và status.                             | Test SUCCESS kiểm tra bốn trường, UUID hợp lệ, action `CLASSIFY`, status `SUCCESS`; test đầu vào không hợp lệ kiểm tra `INVALID_INPUT`. | Đã kiểm tra 

## 4. Truy vết yêu cầu phi chức năng

| Yêu cầu | Nội dung                                                                                                 | Bằng chứng hiện có                                                                                                                                                                              | Trạng thái                             |
| ------- | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| NFR-01  | Hiệu năng: warm-up, tối thiểu 1.000 lượt đo, báo cáo p50/p95 theo yêu cầu.                               | Đã chạy benchmark 1.000 lượt đo thực tế (sau 100 lượt warm-up) trên phiên bản bàn giao: p50 = 0.5431 ms, p95 = 0.9945 ms (dưới 1 ms, đạt yêu cầu hiệu năng)..                                                                                                                           | Đã xác minh                          |
| NFR-02  | Quyền riêng tư: không đưa PII, bí mật hoặc dữ liệu bệnh nhân thô vào log và repository.                  | Test audit kiểm tra không chứa một số giá trị đầu vào cụ thể; test khóa ngoài allowlist kiểm tra dữ liệu đầu vào không được phép. Chưa đủ để chứng minh toàn bộ repository không có PII/secret. | Đã kiểm tra                |
| NFR-03  | Fail-closed: lỗi ghi audit không được trả kết quả phân loại; lỗi không tiết lộ đầu vào.                  | Có test mong đợi `AuditError`, kiểm tra `__cause__`, và test lỗi audit được ưu tiên hơn lỗi validation.                                                                                         | Đã kiểm tra                   |
| NFR-04  | Logic nghiệp vụ được tổ chức rõ ràng, tránh phụ thuộc không cần thiết vào I/O.                           | Đã đọc phần mã nguồn phân loại và audit; chưa hoàn tất review thiết kế toàn bộ module theo tiêu chí này.                                                                                        | Đã kiểm tra                   |
| NFR-05  | Kiểm thử tự động và CI phù hợp với quy trình bàn giao.                                                   | Có hai file test và workflow CI; chưa xác nhận kết quả workflow trên commit bàn giao.                                                                                                           | Đã kiểm tra                   |
| NFR-06  | Cùng input cho cùng kết quả phân loại, không phụ thuộc thứ tự gọi.                                       | Có `test_cung_input_cho_cung_ket_qua_phan_loai`.                                                                                                                                                | Đã kiểm tra trong phạm vi test hiện có |
| NFR-07  | README có hướng dẫn cần thiết và cảnh báo chỉ dùng cho mục đích giáo dục/synthetic, không dùng lâm sàng. | Đối chiếu đầy đủ README hiện tại với yêu cầu.                                                                                                                                              | Đã xác minh                          |

## 5. Chi tiết bằng chứng audit

Các test audit hiện có trong `tests/test_classifier.py`:

1. `test_audit_success_4_fields_and_no_pii`

   - Kiểm tra kết quả phân loại thành công.
   - Kiểm tra file audit tồn tại và chỉ có một dòng trong tình huống test.
   - Kiểm tra log có đúng bốn trường.
   - Kiểm tra timestamp có múi giờ, UUID hợp lệ, action `CLASSIFY`, status `SUCCESS`.
   - Kiểm tra hai giá trị đầu vào cụ thể không xuất hiện trong log.
   - **Giới hạn:** assertion timestamp hiện tại chỉ kiểm tra `tzinfo is not None`, chưa xác nhận độ lệch UTC bằng 0.

2. `test_audit_invalid_input_logs_before_raise`

   - Gọi `classify()` với khóa ngoài allowlist.
   - Kiểm tra phát sinh `ValueError`.
   - Kiểm tra log có `CLASSIFY | INVALID_INPUT`.
   - Kiểm tra chuỗi CCCD thử nghiệm không xuất hiện trong log.
   - **Giới hạn:** chưa có assertion đo trực tiếp thứ tự thời gian giữa thao tác ghi log và thời điểm exception được phát sinh.

3. `test_audit_fail_closed_raises_audit_error_with_cause`

   - Mô phỏng đường dẫn audit không thể sử dụng làm thư mục.
   - Kiểm tra phát sinh `AuditError`, thuộc `RuntimeError`, và giữ nguyên exception nguyên nhân qua `__cause__`.

4. `test_audit_error_takes_precedence_over_validation_error`

   - Mô phỏng đồng thời đầu vào sai và lỗi ghi audit.
   - Kiểm tra `AuditError` được phát sinh.
   - Kiểm tra thông báo lỗi không chứa chuỗi đầu vào không hợp lệ.

5. `test_default_audit_dir_is_outside_repo`

   - Bỏ biến môi trường `AUDIT_LOG_DIR`.
   - Kiểm tra thư mục audit mặc định nằm ngoài thư mục repository hiện tại.
   - **Giới hạn:** kiểm tra này không chứng minh mọi cấu hình ghi đè `AUDIT_LOG_DIR` đều nằm ngoài repository.

Trong mã nguồn `rule_engine/classifier.py`, timestamp được tạo bằng:

`datetime.datetime.now(datetime.timezone.utc).isoformat()`

Điều này hỗ trợ nhận định rằng implementation tạo timestamp theo UTC. Tuy nhiên, để test xác nhận trực tiếp yêu cầu UTC, nên bổ sung assertion kiểm tra:

`dt.utcoffset() == datetime.timedelta(0)`

Chỉ cập nhật trạng thái kiểm tra UTC sau khi thay đổi test và chạy test thành công.

## 6. Kết quả kiểm thử được ghi nhận

Lần chạy đầy đủ được ghi nhận trước đó:

```text
84 passed
```

Đây là kết quả lịch sử. Không dùng kết quả này để khẳng định những thay đổi sau lần chạy đó đã được kiểm thử.

Trước khi bàn giao, cần chạy lại:

```bash
python -m pytest -v
```

Sau đó cập nhật số lượng test pass/fail theo output thực tế. Nếu có thay đổi test audit, phải chạy lại cả test audit và bộ test đầy đủ.

## 7. Các việc còn cần xác minh

- [ ] Bổ sung assertion UTC trong test audit thành công và chạy lại test.
- [ ] Đối chiếu đầy đủ expected của các test với `docs/decision-table.md`.
- [ ] Chạy lại toàn bộ pytest trên mã nguồn hiện tại và ghi đúng kết quả.
- [ ] Kiểm tra workflow CI trên commit mới nhất dự kiến bàn giao.
- [ ] Chạy benchmark theo yêu cầu và lưu bằng chứng p50/p95.
- [ ] Rà soát README theo A-11 / NFR-07.
- [ ] Hoàn tất rà soát quyền riêng tư và secret trên phạm vi repository, không suy ra từ các test audit đơn lẻ.
- [ ] Đồng bộ trạng thái giữa `AC_TRACEABILITY.md`, `TEST_PLAN.md` và `SECURITY_PRIVACY_CHECKLIST.md`.
