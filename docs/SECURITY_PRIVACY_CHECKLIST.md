# CHECKLIST BẢO MẬT VÀ QUYỀN RIÊNG TƯ

## 1. Thông tin chung

- **Dự án:** KTPMUD Hack Marathon 2026
- **Track:** Track A — Dr May Day: Rule Engine Sprint
- **Nhóm:** 26
- **Nguồn quy tắc nghiệp vụ:** `docs/decision-table.md`, tag `bkt-2026-v1`
- **Bộ kiểm thử:** `tests/test_classifier.py`, `tests/test_classifier_qa.py`
- **Kết quả kiểm thử đã ghi nhận:** 84 passed, 0 failed.&#x20;
- **Cảnh báo sử dụng yêu cầu:** `educational/synthetic — not for clinical use`

## 2. Quy ước trạng thái

| Trạng thái                    | Ý nghĩa                                                                            |
| ----------------------------- | ---------------------------------------------------------------------------------- |
| Đạt trong phạm vi đã kiểm tra | Có bằng chứng cụ thể xác nhận hạng mục đáp ứng trong phạm vi đã kiểm tra.          |
| Đã có bằng chứng kiểm thử     | Có test tương ứng đã được xác định, nhưng chưa đủ để kết luận toàn bộ yêu cầu đạt. |
| Chưa xác minh                 | Chưa có đủ bằng chứng từ mã nguồn, test, log hoặc cấu hình.                        |
| Cần xử lý và xác minh         | Cần bổ sung hoặc kiểm tra lại trước khi kết luận đạt.                              |

## 3. Checklist bảo mật và quyền riêng tư

| ID     | Hạng mục                             | Yêu cầu kiểm tra                                                                                                    | Bằng chứng hiện có                                                                                                                                                                                                                                                                   | Trạng thái                                                                          |
| ------ | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| SEC-01 | Dữ liệu tổng hợp                     | Chỉ sử dụng dữ liệu giả lập; không sử dụng dữ liệu bệnh nhân thật.                                                  | Đã rà soát dữ liệu giả lập theo xác nhận của nhóm. Chưa có bằng chứng rà soát toàn bộ repository và lịch sử Git.                                                                                                                                                                     | Đã xác nhận dữ liệu giả lập trong phạm vi đã rà soát; toàn repository chưa xác minh |
| SEC-02 | Zero PII / allowlist                 | Chỉ chấp nhận 9 khóa đầu vào được quy định; từ chối khóa ngoài allowlist, bao gồm khóa chứa PII.                    | Có `test_invalid_value_extra_key_pii` và `test_khoa_ngoai_allowlist_phat_sinh_value_error`.                                                                                                                                                                                          | Đã có bằng chứng kiểm thử                                                           |
| SEC-03 | Kiểm tra đầu vào                     | Kiểm tra các trường được cung cấp trước khi suy luận; từ chối kiểu dữ liệu và miền giá trị không hợp lệ.            | Có test sai kiểu, sai miền giá trị, khóa ngoài allowlist và lỗi ở trường khác không bị che bởi tuổi thiếu.                                                                                                                                                                           | Đã có bằng chứng kiểm thử                                                           |
| SEC-04 | Không để lộ dữ liệu trong `ly_do`    | Lời giải thích không chứa dữ liệu đầu vào cụ thể hoặc lời khuyên điều trị ngoài phạm vi.                            | Có `test_ly_do_khong_chua_gia_tri_input_dac_biet`; test kiểm tra một số giá trị cụ thể.                                                                                                                                                                                              | Đã có bằng chứng kiểm thử một phần                                                  |
| SEC-05 | Cấu trúc audit                       | Mỗi lần gọi `classify()` tạo đúng một bản ghi gồm đúng bốn trường.                                                  | `test_audit_success_4_fields_and_no_pii` kiểm tra một bản ghi thành công có đúng bốn trường; `test_audit_invalid_input_logs_before_raise` kiểm tra một bản ghi khi đầu vào không hợp lệ. Chưa có kết quả chạy test nhiều lần gọi liên tiếp để xác nhận mỗi lần chỉ thêm một bản ghi. | Đã có bằng chứng kiểm thử một phần                                                  |
| SEC-06 | Giá trị audit                        | Timestamp ISO 8601 UTC; UUID hợp lệ; `Action_Type=CLASSIFY`; `Status` phù hợp.                                      | Test hiện tại kiểm tra timestamp phân tích được và có `tzinfo`, UUID hợp lệ, `CLASSIFY`, `SUCCESS`; test đầu vào sai kiểm tra `INVALID_INPUT`. Chưa xác nhận assertion UTC bằng `dt.utcoffset() == datetime.timedelta(0)`.                                                           | Cần xử lý và xác minh                                                               |
| SEC-07 | Không ghi dữ liệu nhạy cảm vào audit | Không ghi dữ liệu đầu vào thô, triệu chứng, chỉ số sức khỏe, PII hoặc bí mật vào log.                               | Test kiểm tra các giá trị mẫu `42.5`, `115` và chuỗi CCCD giả lập không xuất hiện trong log. Chưa rà soát toàn diện mọi trường nhạy cảm.                                                                                                                                             | Đã có bằng chứng kiểm thử một phần                                                  |
| SEC-08 | Audit cho đầu vào không hợp lệ       | Khi xác thực thất bại và audit hoạt động, ghi `INVALID_INPUT` rồi phát sinh lỗi xác thực phù hợp.                   | `test_audit_invalid_input_logs_before_raise` kiểm tra khóa ngoài allowlist gây `ValueError`, ghi `INVALID_INPUT` và không ghi chuỗi CCCD mẫu vào log. Chưa xác nhận tất cả trường hợp sai kiểu và sai miền giá trị đều được ghi đúng trạng thái.                                     | Đã có bằng chứng kiểm thử một phần                                                  |
| SEC-09 | Audit fail-closed                    | Khi audit không ghi được, phát sinh `AuditError`, giữ lỗi gốc và không trả kết quả phân loại.                       | `test_audit_fail_closed_raises_audit_error_with_cause` mô phỏng đường dẫn audit không thể sử dụng làm thư mục; kiểm tra `AuditError`, quan hệ kế thừa `RuntimeError` và `__cause__`.                                                                                                 | Đã có bằng chứng kiểm thử                                                           |
| SEC-10 | Ưu tiên lỗi audit                    | Khi audit và xác thực cùng lỗi, lỗi audit được ưu tiên; thông báo không tiết lộ dữ liệu đầu vào.                    | `test_audit_error_takes_precedence_over_validation_error` kiểm tra lỗi audit được ưu tiên và thông báo không chứa chuỗi đầu vào mẫu.                                                                                                                                                 | Đã có bằng chứng kiểm thử                                                           |
| SEC-11 | Vị trí lưu audit và tránh commit log | Audit phải nằm ngoài repository và không được commit.                                                               | Đã thêm `.audit_logs/` vào `.gitignore`, xác nhận bằng `git check-ignore`, commit `d1f8774 chore: ignore local audit logs` và push lên `origin/test/quy-qa-security`. Có ghi nhận working tree sạch sau commit. Chưa xác minh đường dẫn audit thực tế của môi trường hiện tại.       | Đã xác minh quy tắc ignore; vị trí audit thực tế cần xác minh                       |
| SEC-12 | Bí mật và cấu hình                   | Không đưa token, mật khẩu, khóa API, `.env` hoặc thông tin kết nối môi trường thật vào mã nguồn, test, log hay Git. | Chưa có kết quả rà soát toàn bộ repository và lịch sử Git được cung cấp.                                                                                                                                                                                                             | Chưa xác minh                                                                       |
| SEC-13 | Cảnh báo sử dụng                     | README có chính xác dòng `educational/synthetic — not for clinical use`.                                            | Đã xác định câu cảnh báo cần có; chưa có bằng chứng kiểm tra nội dung README hiện tại.                                                                                                                                                                                               | Chưa xác minh                                                                       |
| SEC-14 | Kiểm thử bảo mật                     | Bộ test của phiên bản đang kiểm tra chạy thành công.                                                                | Có kết quả lịch sử 84 passed, 0 failed. Chưa chạy lại sau mọi thay đổi mới nhất.                                                                                                                                                                                                     | Đạt trong phạm vi lần chạy đã ghi nhận; cần chạy lại                                |

## 4. Yêu cầu bắt buộc đối với audit

Audit trail phải tuân thủ các yêu cầu sau:

1. Mỗi lần gọi `classify()` tạo đúng một bản ghi audit.
2. Bản ghi chỉ chứa bốn trường:
   - `Timestamp`
   - `User_UUID`
   - `Action_Type`
   - `Status`
3. `SUCCESS` áp dụng khi phân loại hoàn tất, kể cả kết quả `THEO_DOI`.
4. `INVALID_INPUT` áp dụng khi xác thực đầu vào thất bại và việc ghi audit thành công.
5. Khi audit thất bại, hệ thống phải fail-closed và không trả kết quả phân loại.
6. Khi audit và xác thực cùng thất bại, lỗi audit được ưu tiên.
7. Không ghi dữ liệu bệnh nhân thô, triệu chứng, huyết áp, PII hoặc bí mật vào audit.
8. Thông báo lỗi và chuỗi exception không được làm lộ dữ liệu đầu vào.
9. Tệp audit phải nằm ngoài repository và không được đưa vào commit.

Đây là các tiêu chí nghiệm thu, không phải bằng chứng rằng toàn bộ tiêu chí đã được đáp ứng. Trạng thái từng mục phải dựa trên test, mã nguồn, log hoặc cấu hình thực tế.

## 5. Bằng chứng kiểm thử hiện có

### 5.1. Kết quả bộ test

Kết quả đã ghi nhận:

```text
84 passed
0 failed
```

Đây là kết quả được ghi nhận trước đó, chưa xác nhận lại sau mọi thay đổi mới nhất. Để dùng làm bằng chứng cho phiên bản hiện tại, chạy lại:

```bash
python -m pytest -v
```

### 5.2. Các test audit đã xác định

Trong `tests/test_classifier.py` có năm test audit sau:

1. `test_audit_success_4_fields_and_no_pii`
2. `test_audit_invalid_input_logs_before_raise`
3. `test_audit_fail_closed_raises_audit_error_with_cause`
4. `test_audit_error_takes_precedence_over_validation_error`
5. `test_default_audit_dir_is_outside_repo`

Các test này cung cấp bằng chứng cho:

- Cấu trúc bản ghi audit gồm bốn trường.
- Một số kiểm tra dữ liệu đầu vào mẫu không xuất hiện trong log.
- Trạng thái `INVALID_INPUT` cho một trường hợp đầu vào không hợp lệ.
- Xử lý lỗi audit và lưu lỗi gốc trong `__cause__`.
- Ưu tiên lỗi audit khi xác thực đầu vào cũng thất bại.
- Vị trí thư mục audit mặc định nằm ngoài repository.

**Chưa xác nhận:** Test bổ sung cho SEC-05 kiểm tra nhiều lần gọi liên tiếp mới chỉ được đề xuất trong cuộc trò chuyện; chưa có kết quả chạy test xác nhận đã được thêm vào file và chạy thành công.

### 5.3. Bằng chứng về `.gitignore`

- Quy tắc `.audit_logs/` đã được thêm vào `.gitignore`.
- `git check-ignore` đã xác nhận quy tắc ignore.
- Commit `d1f8774 chore: ignore local audit logs` đã được push lên nhánh `test/quy-qa-security`.
- Đã có ghi nhận working tree sạch sau commit.

Những bằng chứng này xác nhận việc cấu hình Git ignore đã được thực hiện. Chúng không thay thế việc xác minh đường dẫn audit thực tế và việc rà soát lịch sử Git.

### 5.4. Giới hạn của bằng chứng

- Test timestamp hiện kiểm tra timestamp có thông tin múi giờ, chưa trực tiếp xác nhận độ lệch UTC bằng 0.
- Test không lộ dữ liệu chỉ kiểm tra một số giá trị mẫu, chưa chứng minh mọi loại dữ liệu nhạy cảm đều không thể xuất hiện trong log.
- Test thư mục mặc định nằm ngoài repository không tự chứng minh mọi cấu hình môi trường đều sử dụng đường dẫn đó.
- `.gitignore` không chứng minh log thực tế nằm ngoài repository và không loại bỏ tệp đã được theo dõi trước đó.
- Chưa có kết quả rà soát toàn bộ bí mật trong repository và lịch sử Git.
- Chưa có bằng chứng kiểm tra nội dung README hiện tại trong lần đối chiếu này.
- Chưa xác nhận lại tổng số test sau mọi thay đổi mới nhất.
- Chưa có kết quả xác nhận test mới cho nhiều lần gọi `classify()` đã được thêm và chạy thành công.

##
