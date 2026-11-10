# CHECKLIST BẢO MẬT VÀ QUYỀN RIÊNG TƯ

## 1. Thông tin chung

- **Dự án:** KTPMUD Hack Marathon 2026
- **Track:** Track A — Dr May Day: Rule Engine Sprint
- **Nhóm:** 26
- **Nguồn quy tắc nghiệp vụ duy nhất:** `docs/decision-table.md`, tag `bkt-2026-v1`
- **Bộ kiểm thử:** `tests/test_classifier.py`, `tests/test_classifier_qa.py`
- **Kết quả kiểm thử gần nhất được ghi nhận:** 79 passed, 0 failed, 0.27 giây
- **Cảnh báo bắt buộc:** `educational/synthetic — not for clinical use`

## 2. Quy ước trạng thái

| Trạng thái                    | Ý nghĩa                                                                   |
| ----------------------------- | ------------------------------------------------------------------------- |
| Đạt trong phạm vi đã kiểm tra | Có bằng chứng cụ thể xác nhận hạng mục đã đáp ứng.                        |
| Đã có bằng chứng kiểm thử     | Có test tương ứng đã PASS, nhưng chưa đủ để kết luận toàn bộ yêu cầu đạt. |
| Chưa xác minh                 | Chưa có đủ bằng chứng từ mã nguồn, test, log hoặc cấu hình.               |
| Không đạt                     | Có bằng chứng cho thấy hạng mục vi phạm yêu cầu.                          |

## 3. Checklist bảo mật và quyền riêng tư

| ID     | Hạng mục                             | Yêu cầu kiểm tra                                                                                                                                                                 | Bằng chứng hiện có                                                                                                                            | Trạng thái                         |
| ------ | ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| SEC-01 | Dữ liệu tổng hợp                     | Chỉ sử dụng dữ liệu giả lập; không sử dụng dữ liệu bệnh nhân thật.                                                                                                               | Các test thể hiện dữ liệu mẫu, nhưng chưa có rà soát toàn bộ repository.                                                                      | Chưa xác minh đầy đủ               |
| SEC-02 | Zero PII                             | Chỉ chấp nhận 9 khóa đầu vào được quy định; từ chối khóa ngoài allowlist như `ten`, số định danh, số điện thoại hoặc địa chỉ.                                                    | Có test `test_invalid_value_extra_key_pii` và `test_khoa_ngoai_allowlist_phat_sinh_value_error`.                                              | Đã có bằng chứng kiểm thử          |
| SEC-03 | Kiểm tra đầu vào                     | Kiểm tra tất cả trường được cung cấp trước khi suy luận; không chuyển đổi ngầm kiểu dữ liệu.                                                                                     | Có các test sai kiểu, sai miền giá trị và lỗi dữ liệu không bị che bởi tuổi thiếu.                                                            | Đã có bằng chứng kiểm thử          |
| SEC-04 | Không để lộ dữ liệu trong `ly_do`    | Lời giải thích không chứa dữ liệu đầu vào cụ thể hoặc lời khuyên điều trị.                                                                                                       | Có `test_ly_do_khong_chua_gia_tri_input_dac_biet`; test này chỉ kiểm tra một số giá trị cụ thể.                                               | Đã có bằng chứng kiểm thử một phần |
| SEC-05 | Cấu trúc audit                       | Mỗi lần gọi ghi đúng bốn trường: `Timestamp`, `User_UUID`, `Action_Type`, `Status`.                                                                                              | Chưa có output kiểm tra bản ghi audit trong bằng chứng được cung cấp.                                                                         | Chưa xác minh                      |
| SEC-06 | Giá trị audit                        | `Timestamp` theo ISO 8601 UTC; `User_UUID` là UUID phiên tổng hợp hợp lệ, không phải mã định danh bệnh nhân; `Action_Type=CLASSIFY`; `Status` là `SUCCESS` hoặc `INVALID_INPUT`. | Chưa có bằng chứng kiểm tra trực tiếp nội dung audit.                                                                                         | Chưa xác minh                      |
| SEC-07 | Không ghi dữ liệu nhạy cảm vào audit | Không ghi triệu chứng, chỉ số sức khỏe, dữ liệu đầu vào thô, PII hoặc bí mật vào audit.                                                                                          | Chưa có bằng chứng rà soát nội dung log thực tế.                                                                                              | Chưa xác minh                      |
| SEC-08 | Audit cho đầu vào không hợp lệ       | Khi xác thực thất bại và audit hoạt động, ghi `INVALID_INPUT` rồi phát sinh `TypeError` hoặc `ValueError` phù hợp.                                                               | Bộ test hiện có kiểm tra lỗi đầu vào; chưa thấy bằng chứng riêng xác nhận bản ghi audit tương ứng.                                            | Chưa xác minh                      |
| SEC-09 | Audit fail-closed                    | Nếu audit lỗi I/O, quyền truy cập hoặc ghi đĩa, phát sinh `AuditError` kế thừa `RuntimeError`, giữ lỗi gốc trong `__cause__` và không trả kết quả phân loại.                     | Chưa có bằng chứng từ test mô phỏng lỗi audit.                                                                                                | Chưa xác minh                      |
| SEC-10 | Ưu tiên lỗi audit                    | Nếu cả xác thực đầu vào và audit cùng lỗi, `AuditError` phải được ưu tiên; thông báo lỗi không tiết lộ dữ liệu đầu vào.                                                          | Chưa có bằng chứng kiểm thử tình huống hai lỗi đồng thời.                                                                                     | Chưa xác minh                      |
| SEC-11 | Vị trí lưu audit                     | Tệp audit phải nằm ngoài thư mục repository, không được commit.                                                                                                                  | Trước đó đã ghi nhận `.audit_logs/` xuất hiện trong `git status` dưới dạng chưa được theo dõi. Chưa xác minh vị trí cấu hình ghi log thực tế. | Cần xử lý và xác minh              |
| SEC-12 | Bí mật và cấu hình                   | Không đưa token, mật khẩu, khóa API, `.env` hoặc thông tin kết nối môi trường thật vào mã nguồn, test, log hay Git.                                                              | Chưa có kết quả rà soát toàn bộ repository và lịch sử Git.                                                                                    | Chưa xác minh                      |
| SEC-13 | Cảnh báo sử dụng                     | README phải có chính xác dòng `educational/synthetic — not for clinical use`.                                                                                                    | Chưa có bằng chứng kiểm tra README trong lần đối chiếu này.                                                                                   | Chưa xác minh                      |
| SEC-14 | Kiểm thử bảo mật                     | Các test liên quan phải chạy thành công trên phiên bản đang kiểm tra.                                                                                                            | `python -m pytest -v`: 79 passed, 0 failed. Kết quả không tự chứng minh mọi yêu cầu bảo mật đều đạt.                                          | Đạt trong phạm vi bộ test đã chạy  |

## 4. Yêu cầu bắt buộc đối với audit

Audit trail phải tuân thủ các quy định sau:

1. Mỗi lần gọi `classify()` tạo đúng một bản ghi audit.
2. Bản ghi chỉ chứa bốn trường:
   - `Timestamp`
   - `User_UUID`
   - `Action_Type`
   - `Status`
3. `SUCCESS` áp dụng khi phân loại hoàn tất, kể cả kết quả `THEO_DOI`.
4. `INVALID_INPUT` áp dụng khi xác thực đầu vào thất bại và việc ghi audit thành công.
5. Khi audit thất bại, hệ thống phải fail-closed; không trả kết quả phân loại.
6. Khi cả audit và xác thực đều thất bại, lỗi audit có mức ưu tiên cao hơn.
7. Không ghi dữ liệu bệnh nhân thô, triệu chứng, huyết áp, PII hoặc bí mật vào audit.
8. Thông báo lỗi và chuỗi exception không được làm lộ dữ liệu đầu vào.
9. Tệp audit phải nằm ngoài repository và tuyệt đối không được đưa vào commit.

## 5. Xử lý `.audit_logs/` trước khi commit

Tình trạng đã ghi nhận trước đó:

```text
?? .audit_logs/
```

Điều này cho biết Git đang nhìn thấy thư mục `.audit_logs/` là nội dung chưa được theo dõi tại thời điểm kiểm tra. Nó **không tự chứng minh** rằng tệp audit đã nằm ngoài repository hoặc không chứa dữ liệu nhạy cảm.

Các việc cần thực hiện:

- [ ] Kiểm tra cấu hình và vị trí thực tế mà mã nguồn sử dụng để ghi audit.
- [ ] Xác nhận thư mục audit nằm ngoài repository theo REQUIREMENTS v1.1.
- [ ] Không chạy `git add .` khi `.audit_logs/` còn nằm trong thư mục làm việc.
- [ ] Không đưa nội dung log vào tài liệu, ảnh chụp màn hình hoặc commit.
- [ ] Nếu log đang được tạo bên trong repository, điều chỉnh cấu hình lưu trữ ra ngoài repository.
- [ ] Chỉ cân nhắc xóa log sau khi đã xác định nội dung, mục đích và cách xử lý phù hợp; không xóa mù quáng.
- [ ] Kiểm tra lại `git status` và danh sách file đã stage trước khi commit.

Thêm `.audit_logs/` vào `.gitignore` có thể giúp ngăn vô tình thêm log, nhưng **không thay thế yêu cầu lưu audit bên ngoài repository**.

## 6. Các kiểm tra cần bổ sung

### 6.1. Kiểm tra audit thành công

- [ ] Gọi `classify()` với đầu vào hợp lệ.
- [ ] Xác nhận có đúng một bản ghi mới.
- [ ] Xác nhận đủ và chỉ có bốn trường quy định.
- [ ] Xác nhận định dạng timestamp, UUID và các giá trị action/status.
- [ ] Xác nhận không có dữ liệu bệnh nhân thô hoặc PII trong bản ghi.

### 6.2. Kiểm tra đầu vào không hợp lệ

- [ ] Gọi `classify()` với dữ liệu sai kiểu.
- [ ] Gọi `classify()` với giá trị ngoài miền hợp lệ.
- [ ] Gọi `classify()` với khóa ngoài allowlist.
- [ ] Xác nhận ghi `INVALID_INPUT` nếu audit hoạt động bình thường.
- [ ] Xác nhận lỗi phát sinh đúng loại và không tiết lộ dữ liệu đầu vào.

### 6.3. Kiểm tra lỗi audit

- [ ] Mô phỏng lỗi I/O hoặc lỗi quyền ghi.
- [ ] Xác nhận phát sinh `AuditError`.
- [ ] Xác nhận lỗi gốc nằm trong `__cause__`.
- [ ] Xác nhận không có kết quả phân loại được trả về khi audit thất bại.
- [ ] Kiểm tra tình huống đồng thời có lỗi xác thực và lỗi audit.
- [ ] Xác nhận thông báo lỗi không chứa dữ liệu đầu vào.

### 6.4. Kiểm tra repository

- [ ] Rà soát mã nguồn, test, log và tài liệu để tìm PII hoặc bí mật ngoài ý muốn.
- [ ] Kiểm tra `.env`, token, khóa API và thông tin kết nối môi trường thật.
- [ ] Xác nhận audit không nằm trong repository.
- [ ] Xác nhận không stage hoặc commit `.audit_logs/`.
- [ ] Kiểm tra lịch sử Git nếu có dấu hiệu dữ liệu nhạy cảm từng được commit.

## 7. Bằng chứng kiểm thử hiện có

Lần chạy gần nhất được cung cấp:

```text
python -m pytest -v

collected 79 items
79 passed in 0.27s
```

Các nhóm test có liên quan đến bảo mật và tính đúng đắn:

- Từ chối khóa ngoài allowlist.
- Từ chối kiểu dữ liệu không hợp lệ.
- Từ chối giá trị ngoài miền hợp lệ.
- Kiểm tra xác thực trước khi suy luận.
- Kiểm tra cấu trúc đầu ra.
- Kiểm tra tính xác định.
- Kiểm tra một số giá trị đầu vào không xuất hiện trong `ly_do`.

Giới hạn: output trên chưa chứng minh được audit fail-closed, tính an toàn của log, việc lưu audit ngoài repository, tình trạng CI hoặc việc repository không chứa bí mật.

## 8. Kết luận và điều kiện hoàn tất

Checklist hiện ghi nhận bộ test đã chạy thành công, đồng thời xác định các hạng mục còn cần xác minh.

Trước khi coi checklist bảo mật hoàn tất, cần có bằng chứng cụ thể cho:

1. Audit đủ bốn trường, đúng trạng thái và đúng một bản ghi mỗi lần gọi.
2. Audit fail-closed, xử lý đúng `AuditError` và không làm lộ dữ liệu đầu vào.
3. Tệp audit nằm ngoài repository và không được commit.
4. Repository, test, log và tài liệu không chứa PII hoặc bí mật ngoài ý muốn.
5. README có cảnh báo bắt buộc.
6. Các kết quả kiểm tra được ghi nhận và liên kết với tiêu chí nghiệm thu tương ứng.
