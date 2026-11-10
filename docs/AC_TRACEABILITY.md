# Bảng truy vết yêu cầu và tiêu chí nghiệm thu (AC_TRACEABILITY)

## 1. Thông tin chung

- **Dự án:** KTPMUD Hack Marathon 2026
- **Track:** Track A — Dr May Day: Rule Engine Sprint
- **Nhóm:** 26
- **Nguồn quy tắc nghiệp vụ:** `docs/decision-table.md`, tag `bkt-2026-v1`
- **Bộ kiểm thử:** `tests/test_classifier.py`, `tests/test_classifier_qa.py`
- **Kết quả kiểm thử ghi nhận:** 79 passed, 0 failed, thời gian 0.27 giây

Tài liệu này liên kết yêu cầu chức năng, yêu cầu phi chức năng, tiêu chí nghiệm thu và bằng chứng kiểm thử hiện có. Trạng thái chỉ phản ánh bằng chứng đã ghi nhận, không mặc định rằng toàn bộ hệ thống đã đáp ứng yêu cầu.

## 2. Quy ước trạng thái

| Trạng thái                    | Ý nghĩa                                                                     |
| ----------------------------- | --------------------------------------------------------------------------- |
| Đã có bằng chứng kiểm thử     | Có test tương ứng và test đã PASS; chưa mặc nhiên xác nhận toàn bộ yêu cầu. |
| Đạt trong phạm vi đã kiểm tra | Có bằng chứng phù hợp với phạm vi tiêu chí đang xét.                        |
| Chưa xác minh                 | Chưa có đủ bằng chứng để kết luận.                                          |
| Không đạt                     | Có bằng chứng cho thấy tiêu chí không được đáp ứng.                         |

## 3. Bảng truy vết tiêu chí nghiệm thu

| AC ID | Tiêu chí nghiệm thu                                                                                                                          | Bằng chứng hiện có                                                                                                       | Trạng thái                        |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | --------------------------------- |
| A-01  | Hàm `classify(patient)` thực hiện phân loại và trả về kết quả theo hợp đồng.                                                                 | Bộ test phân loại, kiểm tra cấu trúc đầu ra và các trường hợp dữ liệu đầu vào.                                           | Đã có bằng chứng kiểm thử         |
| A-02  | Kết quả không phụ thuộc vào việc hardcode ID hoặc dữ liệu của bộ test công khai.                                                             | Output pytest chưa cho thấy bằng chứng riêng xác nhận tính tổng quát của mã nguồn.                                       | Chưa xác minh                     |
| A-03  | Phân loại đúng theo R01, R02, R03, R-SOC; xử lý ngưỡng huyết áp, thứ tự ưu tiên và trường hợp biên.                                          | Các test R01/R02/R03, ưu tiên R02-R03, ngưỡng theo tuổi, giảm huyết áp đúng/trên 30% và huyết áp thấp đơn độc.           | Đã có bằng chứng kiểm thử         |
| A-04  | Xử lý dữ liệu thiếu, `None`, UNKNOWN, sai kiểu, sai miền giá trị và khóa ngoài danh sách cho phép đúng hợp đồng.                             | Các test dữ liệu thiếu, UNKNOWN, `TypeError`, `ValueError`, khóa dư và kiểm tra dữ liệu trước khi suy luận.              | Đã có bằng chứng kiểm thử         |
| A-05  | Kết quả có đúng ba khóa; `rule_id` phù hợp; `ly_do` ổn định và không đưa các giá trị đầu vào cụ thể vào lời giải thích.                      | Các test cấu trúc đầu ra, `THEO_DOI` có `rule_id=None`, tính xác định và `test_ly_do_khong_chua_gia_tri_input_dac_biet`. | Đã có bằng chứng kiểm thử         |
| A-06  | Mỗi lần gọi ghi audit đúng bốn trường; không lộ dữ liệu bệnh nhân; xử lý lỗi audit theo cơ chế fail-closed.                                  | Output pytest được cung cấp chưa thể hiện test audit, kiểm tra nội dung log hoặc mô phỏng lỗi I/O.                       | Chưa xác minh                     |
| A-07  | Có bộ test cho trường hợp thông thường, biên, dữ liệu thiếu và dữ liệu không hợp lệ.                                                         | Hai bộ test thu thập tổng cộng 79 test và đều PASS trong lần chạy đã ghi nhận.                                           | Đạt trong phạm vi bộ test đã chạy |
| A-08  | Lệnh pytest chạy thành công trên phiên bản mã nguồn đang kiểm thử.                                                                           | `python -m pytest -v`: 79 passed, 0 failed, 0.27 giây.                                                                   | Đạt trong lần chạy đã ghi nhận    |
| A-09  | CI tự động chạy và đạt trên Pull Request theo yêu cầu dự án.                                                                                 | Output pytest cục bộ không chứng minh CI trên Pull Request đã chạy thành công.                                           | Chưa xác minh                     |
| A-10  | Benchmark có tối thiểu 1000 lượt đo sau 100 lượt làm nóng; báo cáo p50/p95 và p95 dưới 100 ms trên máy được khai báo, tính cả audit thực tế. | Chưa có output benchmark phù hợp trong bằng chứng được cung cấp.                                                         | Chưa xác minh                     |
| A-11  | README có hướng dẫn cài đặt, chạy, kiểm thử và dòng cảnh báo bắt buộc chính xác.                                                             | Chưa có bằng chứng kiểm tra nội dung README trong lần đối chiếu này.                                                     | Chưa xác minh                     |

## 4. Truy vết yêu cầu chức năng

| Yêu cầu | Nội dung                                                                                      | AC liên quan | Bằng chứng kiểm thử đã thấy                                                                                                                                      |
| ------- | --------------------------------------------------------------------------------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FR-01   | Triển khai `classify()` theo hợp đồng đầu vào và đầu ra.                                      | A-01, A-02   | Các test phân loại và kiểm tra cấu trúc đầu ra                                                                                                                   |
| FR-02   | Thực hiện chính xác R01, R02, R03.                                                            | A-01, A-03   | `test_r01_*`, `test_r02_*`, `test_r03_*`                                                                                                                         |
| FR-03   | Áp dụng ngưỡng R-SOC theo tuổi và điều kiện giảm huyết áp ở người lớn.                        | A-03         | `test_nguong_soc_theo_tuoi`, `test_nguoi_lon_giam_*`, `test_nguoi_lon_hatt_duoi_90_khong_can_hatt_nen`                                                           |
| FR-04   | Xử lý thứ tự quyết định, tuổi thiếu và độ ưu tiên của quy tắc.                                | A-03, A-04   | `test_tc12_missing_tuoi`, `test_tc18_validation_before_missing_tuoi`, `test_r02_duoc_uu_tien_hon_r03_khi_cung_khop`                                              |
| FR-05   | Xử lý dữ liệu thiếu và UNKNOWN theo logic ba trạng thái.                                      | A-04         | `test_thieu_truong_bool_duoc_coi_la_unknown`, `test_rule_da_true_khong_bi_huy_vi_truong_khac_unknown`, `test_r02_unknown_khi_chua_du_hai_true_nhung_con_unknown` |
| FR-06   | Kiểm tra nghiêm ngặt kiểu, miền giá trị và khóa đầu vào.                                      | A-04         | Các test `test_sai_kieu_du_lieu_*`, `test_sai_mien_du_lieu_*`, `test_khoa_ngoai_allowlist_phat_sinh_value_error`                                                 |
| FR-07   | Trả đúng cấu trúc kết quả, giải thích xác định, không đưa dữ liệu đầu vào cụ thể vào `ly_do`. | A-05         | `test_dau_ra_chi_co_ba_khoa`, `test_theo_doi_luon_co_rule_id_none`, `test_cung_input_cho_cung_ket_qua_phan_loai`, `test_ly_do_khong_chua_gia_tri_input_dac_biet` |
| FR-08   | Ghi audit đúng bốn trường cho mỗi lần gọi.                                                    | A-06         | Chưa có bằng chứng audit trong output pytest được cung cấp                                                                                                       |

## 5. Truy vết yêu cầu phi chức năng

| Yêu cầu | Nội dung cần xác minh                                                                               | AC liên quan     | Trạng thái                                                          |
| ------- | --------------------------------------------------------------------------------------------------- | ---------------- | ------------------------------------------------------------------- |
| NFR-01  | Hiệu năng: benchmark đầy đủ, p50/p95, tối thiểu 1000 lượt đo sau warm-up.                           | A-10             | Chưa xác minh                                                       |
| NFR-02  | Quyền riêng tư: không đưa PII, bí mật hoặc dữ liệu bệnh nhân vào input, test, log hay repository.   | A-06             | Chưa xác minh đầy đủ                                                |
| NFR-03  | Audit fail-closed; lỗi audit không được trả kết quả phân loại; thông báo lỗi không tiết lộ đầu vào. | A-06             | Chưa xác minh                                                       |
| NFR-04  | Tách logic quy tắc khỏi I/O, tránh trừu tượng hóa không cần thiết.                                  | A-01, A-02       | Chưa xác minh bằng rà soát mã nguồn                                 |
| NFR-05  | Có test thông thường, biên, thiếu dữ liệu và dữ liệu lỗi; pytest và CI đáp ứng yêu cầu.             | A-07, A-08, A-09 | Pytest đã PASS; CI chưa xác minh                                    |
| NFR-06  | Cùng đầu vào tạo cùng kết quả, không phụ thuộc thứ tự gọi.                                          | A-05             | Đã có test tính xác định; cần xem nội dung test để xác nhận phạm vi |
| NFR-07  | README có hướng dẫn cài đặt, chạy, kiểm thử và cảnh báo bắt buộc.                                   | A-11             | Chưa xác minh                                                       |

## 6. Bằng chứng kiểm thử đã ghi nhận

Lần chạy gần nhất được cung cấp:

```text
python -m pytest -v

collected 79 items
79 passed in 0.27s
```

Các nhóm kiểm thử thể hiện trong output:

- Quy tắc phân loại R01, R02, R03 và các trường hợp nhiều quy tắc cùng khớp.
- Ngưỡng sốc theo tuổi, bao gồm các giá trị ở hai phía của ngưỡng.
- Điều kiện giảm huyết áp đúng 30% và trên 30%.
- Dữ liệu thiếu, `None`, khóa bị bỏ trống và UNKNOWN.
- Sai kiểu dữ liệu, sai miền giá trị, giá trị vô hạn/NaN và khóa ngoài allowlist.
- Kiểm tra dữ liệu lỗi không bị che giấu bởi trường tuổi thiếu.
- Cấu trúc đầu ra, `rule_id` của `THEO_DOI`, tính xác định và một số trường hợp kiểm tra `ly_do`.

**Giới hạn của bằng chứng:** pytest PASS chỉ chứng minh các test hiện có vượt qua trong môi trường đã chạy. Nó không tự chứng minh rằng mọi nhánh nghiệp vụ đều đã được bao phủ, audit an toàn, CI đạt, benchmark đáp ứng ngưỡng hay README đầy đủ.

## 7. Các hạng mục cần xác minh tiếp

1. **A-02:** Rà soát mã nguồn để kiểm tra không hardcode ID hoặc dữ liệu của bộ test công khai.
2. **A-06:** Kiểm tra triển khai audit, đúng bốn trường, mỗi lần gọi đúng một bản ghi, `INVALID_INPUT`, `SUCCESS`, `AuditError`, lỗi I/O và việc không ghi dữ liệu nhạy cảm.
3. **A-09:** Kiểm tra kết quả CI trên Pull Request.
4. **A-10:** Kiểm tra script, cấu hình, số lượt benchmark, p50/p95, máy đo và việc benchmark bao gồm audit.
5. **A-11:** Đối chiếu README với hướng dẫn cài đặt, chạy, kiểm thử và dòng cảnh báo chính xác.
6. **A-01, A-03, A-04, A-05, A-07:** Đối chiếu nội dung test và expected với `docs/decision-table.md`, không chỉ dựa vào tên test.
7. Kiểm tra `.audit_logs/` và các tệp phát sinh để bảo đảm không đưa log nhạy cảm hoặc dữ liệu ngoài phạm vi vào commit.

## 8. Kết luận

Bộ kiểm thử hiện có đã chạy thành công **79/79 test**. Bằng chứng thể hiện phạm vi kiểm thử đáng kể cho logic phân loại, ngưỡng sốc, dữ liệu thiếu, xác thực đầu vào và cấu trúc đầu ra.

Tuy nhiên, chưa đủ căn cứ để kết luận toàn bộ tiêu chí nghiệm thu đã đạt. Các mục về audit, quyền riêng tư toàn hệ thống, CI, benchmark và README cần được xác minh riêng trước khi bàn giao.

Tài liệu này phải được cập nhật khi có bằng chứng mới; trạng thái nghiệm thu cuối cùng cần thống nhất với mã nguồn, bộ test và REQUIREMENTS v1.1.
