# CHECKLIST BẢO MẬT VÀ QUYỀN RIÊNG TƯ

## 1. Thông tin chung

- **Dự án:** KTPMUD Hack Marathon 2026
- **Track:** Track A — Dr May Day: Rule Engine Sprint
- **Nhóm:** 26
- **Nguồn quy tắc nghiệp vụ:** `docs/decision-table.md`, tag `bkt-2026-v1`
- **Bộ kiểm thử:** `tests/test_classifier.py`, `tests/test_classifier_qa.py`
- **Kết quả kiểm thử đã ghi nhận:** 84 passed, 0 failed. Chưa xác nhận lại sau mọi thay đổi mới nhất.
- **Cảnh báo sử dụng:** `educational/synthetic — not for clinical use`

## 2. Quy ước trạng thái

| Trạng thái | Ý nghĩa |
|---|---|
| Đạt trong phạm vi đã kiểm tra | Có bằng chứng cụ thể xác nhận hạng mục đáp ứng trong phạm vi đã kiểm tra. |
| Đã có bằng chứng kiểm thử | Có test tương ứng đã chạy thành công, nhưng chưa đủ để kết luận toàn bộ yêu cầu đạt. |
| Chưa xác minh | Chưa có đủ bằng chứng từ mã nguồn, test, log hoặc cấu hình. |
| Cần xử lý và xác minh | Có vấn đề hoặc điều kiện còn phải kiểm tra trước khi kết luận đạt. |

## 3. Checklist bảo mật và quyền riêng tư

| ID | Hạng mục | Yêu cầu kiểm tra | Bằng chứng hiện có | Trạng thái |
|---|---|---|---|---|
| SEC-01 | Dữ liệu tổng hợp | Chỉ sử dụng dữ liệu giả lập; không sử dụng dữ liệu bệnh nhân thật. | Các test đã xem sử dụng dữ liệu mẫu. Chưa có bằng chứng rà soát toàn bộ repository, lịch sử Git và các tệp liên quan. | Chưa xác minh đầy đủ |
| SEC-02 | Zero PII / allowlist | Chỉ chấp nhận 9 khóa đầu vào được quy định; từ chối khóa ngoài allowlist, bao gồm khóa chứa PII. | Có `test_invalid_value_extra_key_pii` và `test_khoa_ngoai_allowlist_phat_sinh_value_error`. Các test hỗ trợ xác nhận việc từ chối khóa ngoài allowlist, không chứng minh toàn bộ repository không chứa PII. | Đã có bằng chứng kiểm thử |
| SEC-03 | Kiểm tra đầu vào | Kiểm tra các trường được cung cấp trước khi suy luận; từ chối kiểu dữ liệu và miền giá trị không hợp lệ. | Bộ QA có test sai kiểu, sai miền giá trị, khóa ngoài allowlist và các trường hợp lỗi ở trường khác không bị che bởi tuổi thiếu. | Đã có bằng chứng kiểm thử |
| SEC-04 | Không để lộ dữ liệu trong `ly_do` | Lời giải thích không chứa dữ liệu đầu vào cụ thể hoặc lời khuyên điều trị ngoài phạm vi. | Có `test_ly_do_khong_chua_gia_tri_input_dac_biet`. Test kiểm tra một số giá trị cụ thể, không bao phủ mọi dữ liệu có thể có. | Đã có bằng chứng kiểm thử một phần |
| SEC-05 | Cấu trúc audit | Mỗi lần gọi `classify()` tạo đúng một bản ghi gồm đúng bốn trường. | `test_audit_success_4_fields_and_no_pii` kiểm tra một dòng log có đúng bốn trường. `test_audit_invalid_input_logs_before_raise` kiểm tra một dòng log trong trường hợp đầu vào không hợp lệ. | Đã có bằng chứng kiểm thử |
| SEC-06 | Giá trị audit | Timestamp ISO 8601 UTC; UUID hợp lệ; `Action_Type=CLASSIFY`; `Status` phù hợp. | `test_audit_success_4_fields_and_no_pii` kiểm tra timestamp phân tích được và có thông tin múi giờ, UUID hợp lệ, `CLASSIFY`, `SUCCESS`. Test chưa kiểm tra trực tiếp độ lệch UTC bằng 0. Test đầu vào không hợp lệ kiểm tra `CLASSIFY | INVALID_INPUT`. | Đã có bằng chứng kiểm thử một phần |
| SEC-07 | Không ghi dữ liệu nhạy cảm vào audit | Không ghi dữ liệu đầu vào thô, triệu chứng, chỉ số sức khỏe, PII hoặc bí mật vào log. | Test audit thành công kiểm tra các giá trị mẫu `42.5` và `115` không xuất hiện trong log. Test audit đầu vào không hợp lệ kiểm tra chuỗi CCCD mẫu không xuất hiện trong log. Chưa có rà soát toàn diện mọi trường nhạy cảm. | Đã có bằng chứng kiểm thử một phần |
| SEC-08 | Audit cho đầu vào không hợp lệ | Khi xác thực thất bại và audit hoạt động, ghi `INVALID_INPUT` rồi phát sinh lỗi xác thực phù hợp. | `test_audit_invalid_input_logs_before_raise` kiểm tra trường hợp khóa ngoài allowlist gây `ValueError` và log chứa `CLASSIFY | INVALID_INPUT`. Chưa chứng minh mọi loại lỗi xác thực đều được bao phủ. | Đã có bằng chứng kiểm thử |
| SEC-09 | Audit fail-closed | Khi audit không ghi được, phát sinh `AuditError`, giữ lỗi gốc và không trả kết quả phân loại. | `test_audit_fail_closed_raises_audit_error_with_cause` mô phỏng đường dẫn audit không thể dùng làm thư mục; xác nhận `AuditError` là `RuntimeError` và có `__cause__`. | Đã có bằng chứng kiểm thử |
| SEC-10 | Ưu tiên lỗi audit | Khi audit và xác thực cùng lỗi, lỗi audit được ưu tiên; thông báo không tiết lộ dữ liệu đầu vào. | `test_audit_error_takes_precedence_over_validation_error` xác nhận `AuditError` được phát sinh khi đầu vào sai kiểu đồng thời audit không ghi được; thông báo không chứa chuỗi đầu vào mẫu. | Đã có bằng chứng kiểm thử |
| SEC-11 | Vị trí lưu audit và tránh commit log | Audit phải nằm ngoài repository và không được commit. | Đã thêm `.audit_logs/` vào `.gitignore`; `git check-ignore` đã xác nhận quy tắc bỏ qua. Commit `d1f8774 chore: ignore local audit logs` đã được push. Đã có ghi nhận working tree sạch sau commit. Tuy nhiên, `.gitignore` không chứng minh đường dẫn log thực tế nằm ngoài repository. | Đã xác minh việc ignore; vị trí log thực tế cần xác minh riêng |
| SEC-12 | Bí mật và cấu hình | Không đưa token, mật khẩu, khóa API, `.env` hoặc thông tin kết nối môi trường thật vào mã nguồn, test, log hay Git. | Chưa có kết quả rà soát toàn bộ repository và lịch sử Git được cung cấp. | Chưa xác minh |
| SEC-13 | Cảnh báo sử dụng | README có chính xác dòng `educational/synthetic — not for clinical use`. | Chưa có bằng chứng kiểm tra nội dung README hiện tại trong lần đối chiếu này. | Chưa xác minh |
| SEC-14 | Kiểm thử bảo mật | Bộ test của phiên bản đang kiểm tra chạy thành công. | Kết quả đã ghi nhận: 84 passed, 0 failed. Chưa xác nhận lại sau mọi thay đổi mới nhất. Kết quả tổng thể không tự chứng minh mọi yêu cầu bảo mật đều đạt. | Đạt trong phạm vi lần chạy đã ghi nhận |

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

Các yêu cầu trên là tiêu chí nghiệm thu, không phải bằng chứng rằng toàn bộ tiêu chí đã được đáp ứng. Trạng thái từng mục phải dựa trên test, mã nguồn, log hoặc cấu hình thực tế.

## 5. Xử lý `.audit_logs/` trước khi commit

### 5.1. Những việc đã thực hiện

- [x] Thêm `.audit_logs/` vào `.gitignore`.
- [x] Kiểm tra quy tắc ignore bằng `git check-ignore`.
- [x] Commit thay đổi với commit `d1f8774 chore: ignore local audit logs`.
- [x] Push commit lên `origin/test/quy-qa-security`.
- [x] Đã có ghi nhận working tree sạch sau commit.

### 5.2. Những việc cần phân biệt và xác minh thêm

- [ ] Kiểm tra `git status --short --untracked-files=all` để xác nhận trạng thái hiện tại.
- [ ] Kiểm tra cấu hình `AUDIT_LOG_DIR` và đường dẫn audit thực tế trong môi trường đang chạy.
- [ ] Xác nhận log thực tế nằm ngoài repository theo yêu cầu.
- [ ] Kiểm tra danh sách file đã stage bằng `git diff --cached --name-only` trước lần commit tiếp theo.
- [ ] Rà soát log để bảo đảm không có PII hoặc dữ liệu nhạy cảm ngoài ý muốn.
- [ ] Nếu có dấu hiệu log hoặc dữ liệu nhạy cảm từng được commit, kiểm tra lịch sử Git.

**Lưu ý:** `.gitignore` ngăn Git tự động hiển thị các tệp chưa được theo dõi phù hợp với quy tắc ignore; nó không di chuyển log ra ngoài repository, không tự loại bỏ tệp đã được theo dõi và không xóa dữ liệu đã có trong lịch sử Git.

Không cần làm lại bước thêm `.audit_logs/` vào `.gitignore` nếu quy tắc hiện tại vẫn còn và hoạt động đúng. Phần còn lại là xác minh đường dẫn log thực tế và trạng thái Git hiện tại.

## 6. Các kiểm tra cần bổ sung

### 6.1. Kiểm tra audit thành công

- [x] Kiểm tra một bản ghi được tạo trong trường hợp phân loại thành công.
- [x] Kiểm tra bản ghi có đúng bốn trường.
- [x] Kiểm tra UUID hợp lệ, action là `CLASSIFY` và status là `SUCCESS`.
- [ ] Bổ sung assertion xác nhận timestamp thực sự ở UTC, ví dụ `dt.utcoffset() == datetime.timedelta(0)`.
- [ ] Kiểm tra trường hợp kết quả `THEO_DOI` vẫn tạo `SUCCESS`.
- [ ] Kiểm tra nhiều lần gọi liên tiếp để xác nhận mỗi lần chỉ tạo một bản ghi mới.
- [x] Kiểm tra một số giá trị đầu vào mẫu không xuất hiện trong audit.
- [ ] Mở rộng kiểm tra để bao phủ các trường nhạy cảm khác theo hợp đồng dữ liệu.

### 6.2. Kiểm tra đầu vào không hợp lệ

- [x] Kiểm tra trường hợp khóa ngoài allowlist gây `ValueError` và ghi `INVALID_INPUT`.
- [x] Kiểm tra chuỗi CCCD mẫu không xuất hiện trong bản ghi audit.
- [ ] Xác nhận riêng các trường hợp sai kiểu và sai miền giá trị đều ghi `INVALID_INPUT` khi audit hoạt động bình thường.
- [ ] Xác nhận loại exception phù hợp cho các trường hợp đầu vào không hợp lệ còn lại.
- [ ] Mở rộng kiểm tra thông báo lỗi để bảo đảm không làm lộ dữ liệu đầu vào.

### 6.3. Kiểm tra lỗi audit

- [x] Mô phỏng tình huống không thể ghi audit.
- [x] Xác nhận phát sinh `AuditError` kế thừa `RuntimeError`.
- [x] Xác nhận lỗi gốc được lưu trong `__cause__`.
- [x] Kiểm tra lỗi audit được ưu tiên khi đầu vào cũng không hợp lệ.
- [x] Kiểm tra thông báo lỗi không chứa chuỗi đầu vào mẫu trong tình huống ưu tiên lỗi.
- [ ] Kiểm tra bổ sung các trường hợp lỗi I/O hoặc quyền ghi khác nếu cần mở rộng độ bao phủ.

### 6.4. Kiểm tra repository

- [ ] Rà soát mã nguồn, test, log và tài liệu để tìm PII hoặc bí mật ngoài ý muốn.
- [ ] Kiểm tra `.env`, token, khóa API và thông tin kết nối môi trường thật.
- [x] Đã thêm `.audit_logs/` vào `.gitignore` và xác nhận quy tắc ignore.
- [ ] Xác minh vị trí audit thực tế đang được sử dụng.
- [ ] Kiểm tra trạng thái Git và danh sách file đã stage mới nhất.
- [ ] Kiểm tra lịch sử Git nếu có dấu hiệu dữ liệu nhạy cảm từng được commit.
- [ ] Xác minh README có cảnh báo bắt buộc.

## 7. Bằng chứng kiểm thử hiện có

### 7.1. Kết quả bộ test

Kết quả đã ghi nhận:

```text
84 passed
0 failed
```

Đây là kết quả được ghi nhận trước đó, chưa xác nhận lại sau mọi thay đổi mới nhất. Để dùng làm bằng chứng cho phiên bản hiện tại, chạy lại:

```bash
python -m pytest -v
```

### 7.2. Các test audit đã xác định

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

### 7.3. Bằng chứng về `.gitignore`

- Quy tắc `.audit_logs/` đã được thêm vào `.gitignore`.
- `git check-ignore` đã xác nhận quy tắc ignore.
- Commit `d1f8774 chore: ignore local audit logs` đã được push lên nhánh `test/quy-qa-security`.
- Đã có ghi nhận working tree sạch sau commit.

Những bằng chứng này xác nhận việc cấu hình Git ignore đã được thực hiện. Chúng không thay thế việc xác minh đường dẫn audit thực tế và việc rà soát lịch sử Git.

### 7.4. Giới hạn của bằng chứng

- Test timestamp hiện kiểm tra timestamp có thông tin múi giờ, chưa trực tiếp xác nhận độ lệch UTC bằng 0.
- Test không lộ dữ liệu chỉ kiểm tra một số giá trị mẫu, chưa chứng minh mọi loại dữ liệu nhạy cảm đều không thể xuất hiện trong log.
- Test thư mục mặc định nằm ngoài repository không tự chứng minh mọi cấu hình môi trường đều sử dụng đường dẫn đó.
- `.gitignore` không chứng minh log thực tế nằm ngoài repository và không loại bỏ tệp đã được theo dõi trước đó.
- Chưa có kết quả rà soát toàn bộ bí mật trong repository và lịch sử Git.
- Chưa có bằng chứng kiểm tra nội dung README hiện tại trong lần đối chiếu này.
- Chưa xác nhận lại tổng số test sau mọi thay đổi mới nhất.

## 8. Kết luận và điều kiện hoàn tất

Checklist đã được cập nhật từ bản PC1. Các test audit hiện có đã được đưa vào làm bằng chứng; việc thêm `.audit_logs/` vào `.gitignore`, kiểm tra bằng `git check-ignore`, commit và push cũng đã được ghi nhận.

Không tiếp tục coi việc xử lý `.audit_logs/` là chưa thực hiện. Tuy nhiên, cần phân biệt việc Git bỏ qua thư mục này với yêu cầu audit thực tế phải nằm ngoài repository.

Trước khi kết luận checklist bảo mật đã hoàn tất, cần:

1. Bổ sung hoặc xác nhận kiểm tra timestamp UTC.
2. Xác minh `SUCCESS` cho kết quả `THEO_DOI` và số bản ghi qua nhiều lần gọi.
3. Mở rộng kiểm tra dữ liệu nhạy cảm không xuất hiện trong audit.
4. Xác minh đường dẫn audit thực tế và trạng thái Git hiện tại.
5. Rà soát PII, bí mật và lịch sử Git.
6. Kiểm tra README có cảnh báo bắt buộc.
7. Chạy lại bộ test sau các thay đổi mới nhất và ghi đúng kết quả thực tế.

**Kết luận:** Đã có bằng chứng kiểm thử cho nhiều hành vi audit và đã xử lý quy tắc Git ignore cho `.audit_logs/`. Chưa đủ bằng chứng để tuyên bố toàn bộ checklist bảo mật và quyền riêng tư đã hoàn tất.