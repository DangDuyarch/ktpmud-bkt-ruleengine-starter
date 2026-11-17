# BÁO CÁO KẾ HOẠCH KIỂM THỬ — TEST_REPORT

## 1. Thông tin chung

| Thuộc tính | Nội dung |
|---|---|
| Dự án | KTPMUD Hack Marathon 2026 |
| Track | Track A — Dr May Day: Rule Engine Sprint |
| Nhóm | 26 |
| Nguồn quy tắc nghiệp vụ | `docs/decision-table.md` |
| Tag quy tắc | `bkt-2026-v1` |
| Mã nguồn cần kiểm thử | Module triển khai hàm `classify()` |
| Bộ kiểm thử | `tests/test_classifier.py`, `tests/test_classifier_qa.py` |
| Công cụ | Python, pytest |
| Kết quả đã ghi nhận trước đó | 84 passed, 0 failed; chưa xác nhận lại sau mọi thay đổi mới nhất |
| Cảnh báo bắt buộc | `educational/synthetic — not for clinical use` |

## 2. Mục tiêu kiểm thử

Kế hoạch kiểm thử nhằm xác minh hệ thống Rule Engine có đáp ứng yêu cầu về logic phân loại, kiểm tra dữ liệu đầu vào, cấu trúc đầu ra, quyền riêng tư, audit và khả năng chạy tự động hay không.

Các mục tiêu chính:

- Kiểm tra kết quả phân loại theo bảng quyết định nghiệp vụ.
- Kiểm tra thứ tự ưu tiên giữa các quy tắc và các trường hợp biên.
- Kiểm tra dữ liệu thiếu, `None`, UNKNOWN, sai kiểu, sai miền giá trị và khóa không được phép.
- Kiểm tra cấu trúc kết quả và nội dung giải thích.
- Kiểm tra audit trail, xử lý lỗi audit và bảo vệ dữ liệu.
- Kiểm tra khả năng chạy bộ test và CI.
- Kiểm tra benchmark hiệu năng và nội dung README.

**Nguyên tắc:** Chỉ kết luận một tiêu chí đã đạt khi có bằng chứng phù hợp. Tổng số test PASS không đồng nghĩa tất cả yêu cầu nghiệm thu đã được xác minh.

## 3. Phạm vi kiểm thử

### 3.1. Trong phạm vi

1. Logic phân loại R01-PV, R02-PV, R03-PV và R-SOC.
2. Thứ tự ưu tiên quy tắc và các điều kiện biên.
3. Xử lý dữ liệu đầu vào thiếu hoặc không hợp lệ.
4. Kiểm tra kiểu dữ liệu, miền giá trị và danh sách khóa cho phép.
5. Cấu trúc đầu ra gồm đúng ba khóa `muc_do`, `rule_id`, `ly_do`.
6. Tính xác định của kết quả và kiểm tra một số giá trị đầu vào không xuất hiện trong `ly_do`.
7. Audit trail và các tình huống lỗi liên quan.
8. Kiểm tra quyền riêng tư, cấu hình lưu log và repository.
9. Chạy test tự động, CI, benchmark và kiểm tra README.

### 3.2. Ngoài phạm vi

- Sử dụng dữ liệu bệnh nhân thật.
- Đánh giá hiệu quả chẩn đoán hoặc điều trị ngoài đời thực.
- Đưa ra khuyến nghị điều trị cho người sử dụng.
- Khẳng định hệ thống đủ điều kiện sử dụng lâm sàng.

Hệ thống chỉ phục vụ mục đích giáo dục và thử nghiệm với dữ liệu tổng hợp.

## 4. Môi trường và cách chạy kiểm thử

### 4.1. Môi trường đã ghi nhận

| Thành phần | Thông tin |
|---|---|
| Hệ điều hành | Windows |
| Python | 3.15.1 — theo kết quả đã ghi nhận |
| pytest | 9.2.0 — theo kết quả đã ghi nhận |
| Kết quả kiểm thử mới nhất được ghi nhận trong lịch sử dự án | 84 passed |
| Trạng thái hiện tại | Chưa chạy xác nhận lại sau mọi thay đổi mới nhất |

Không ghi số test hoặc thời gian chạy là kết quả hiện tại nếu chưa có output của lần chạy tương ứng.

### 4.2. Lệnh kiểm thử

Chạy toàn bộ bộ test:

```bash
python -m pytest -v
```

Chạy riêng từng file:

```bash
python -m pytest -v tests/test_classifier.py
python -m pytest -v tests/test_classifier_qa.py
```

Kiểm tra định dạng thay đổi và trạng thái repository:

```bash
git diff --check
git status --short --untracked-files=all
git diff --cached --name-only
```

Không chạy `git add .` trước khi kiểm tra các file phát sinh, đặc biệt là log audit và dữ liệu ngoài phạm vi.

## 5. Các nhóm kiểm thử và tiêu chí

| Nhóm | Nội dung | Tiêu chí cần đạt | Bằng chứng hiện có |
|---|---|---|---|
| TC-01 | Phân loại R01-PV | Kết quả và `rule_id` đúng theo bảng quyết định | Có test QA liên quan |
| TC-02 | Phân loại R02-PV | Điều kiện và mức độ phân loại đúng | Có test QA liên quan |
| TC-03 | Phân loại R03-PV | Điều kiện và mức độ phân loại đúng | Có test QA liên quan |
| TC-04 | Quy tắc R-SOC | Chỉ áp dụng khi đủ điều kiện Tier 2 và tiêu chí huyết áp theo đặc tả | Có test ngưỡng huyết áp; cần đối chiếu toàn bộ điều kiện với bảng quyết định |
| TC-05 | Thứ tự ưu tiên | Khi nhiều quy tắc cùng khớp, chọn đúng quy tắc ưu tiên | Có test ưu tiên R02 so với R03 |
| TC-06 | Ngưỡng theo tuổi | Xử lý đúng các ngưỡng tuổi và trường hợp biên | Có test ngưỡng theo tuổi |
| TC-07 | Giảm huyết áp ở người lớn | Phân biệt đúng mức giảm 30% và trên 30% theo yêu cầu | Có test trường hợp đúng 30% và trên 30% |
| TC-08 | Dữ liệu thiếu | Xử lý đúng trường thiếu, `None` và UNKNOWN | Có test QA liên quan |
| TC-09 | Sai kiểu dữ liệu | Từ chối kiểu dữ liệu không hợp lệ, không ép kiểu ngầm | Có test QA liên quan |
| TC-10 | Sai miền giá trị | Từ chối giá trị không hợp lệ theo hợp đồng | Có test QA liên quan |
| TC-11 | Khóa ngoài allowlist | Từ chối khóa không nằm trong danh sách 9 khóa đầu vào | Có test khóa ngoài allowlist |
| TC-12 | Thứ tự xác thực | Kiểm tra các trường được cung cấp trước khi suy luận | Có test QA liên quan |
| TC-13 | Cấu trúc đầu ra | Chỉ có `muc_do`, `rule_id`, `ly_do` | Có test QA liên quan |
| TC-14 | Giải thích kết quả | `ly_do` xác định và không chứa các giá trị đầu vào mẫu được kiểm tra | Có test kiểm tra một số giá trị cụ thể |
| TC-15 | Audit thành công | Một lần gọi tạo đúng một bản ghi với đúng bốn trường | Có `test_audit_success_4_fields_and_no_pii` |
| TC-16 | Audit đầu vào lỗi | Ghi `INVALID_INPUT` khi xác thực thất bại và audit hoạt động | Có `test_audit_invalid_input_logs_before_raise` |
| TC-17 | Audit thất bại | Phát sinh `AuditError`, giữ lỗi gốc trong `__cause__` và không trả kết quả phân loại | Có `test_audit_fail_closed_raises_audit_error_with_cause` |
| TC-18 | Ưu tiên lỗi audit | `AuditError` được ưu tiên khi audit và xác thực cùng lỗi | Có `test_audit_error_takes_precedence_over_validation_error` |
| TC-19 | Vị trí audit | Thư mục audit mặc định nằm ngoài repository; kiểm tra đường dẫn thực tế | Có `test_default_audit_dir_is_outside_repo`; cần xác minh cấu hình thực tế |
| TC-20 | Git ignore | `.audit_logs/` được Git bỏ qua và không bị đưa vào commit ngoài ý muốn | Đã có ghi nhận `git check-ignore`, commit `d1f8774` và push |
| TC-21 | CI | Bộ test tự động chạy thành công trên Pull Request | Chưa có bằng chứng CI mới nhất trong lần đối chiếu này |
| TC-22 | Benchmark | Ít nhất 100 lượt warm-up, 1000 lượt đo, báo cáo p50/p95 và p95 dưới 100 ms | Chưa có báo cáo benchmark phù hợp trong bằng chứng hiện có |
| TC-23 | README | Có hướng dẫn cài đặt, chạy, kiểm thử và cảnh báo bắt buộc chính xác | Chưa xác minh nội dung README hiện tại |

Các test hiện có là bằng chứng cho những trường hợp cụ thể được kiểm tra. Không suy rộng thành kết luận rằng toàn bộ quy tắc nghiệp vụ hoặc yêu cầu bảo mật đã được bao phủ.

## 6. Kết quả kiểm thử đã ghi nhận

### 6.1. Kết quả tổng thể

Kết quả mới nhất được ghi nhận trong lịch sử dự án là **84 passed, 0 failed**. Chưa xác nhận lại sau mọi thay đổi mới nhất.

Để cập nhật kết quả chính thức cho phiên bản hiện tại, cần chạy:

```bash
python -m pytest -v
```

Sau đó ghi chính xác số test thu thập được, số test PASS/FAIL/SKIP và thời gian từ output thực tế. Không giữ số `79 passed in 0.27s` của bản PC1 làm kết quả hiện tại nếu đó không phải lần chạy đang báo cáo.

### 6.2. Các nội dung đã có bằng chứng kiểm thử

**Logic và xác thực đầu vào**

- Các trường hợp phân loại R01-PV, R02-PV và R03-PV.
- Thứ tự ưu tiên khi nhiều quy tắc cùng khớp.
- Ngưỡng sốc theo tuổi và một số điều kiện huyết áp ở người lớn.
- Dữ liệu thiếu, `None` và UNKNOWN.
- Sai kiểu dữ liệu, sai miền giá trị và các trường hợp giá trị không hợp lệ được test.
- Khóa ngoài allowlist.
- Xác thực đầu vào trước khi suy luận.
- Cấu trúc đầu ra, `rule_id` của `THEO_DOI` và tính xác định.
- Kiểm tra một số giá trị đầu vào không xuất hiện trong `ly_do`.

**Audit**

Trong `tests/test_classifier.py` đã xác định năm test:

1. `test_audit_success_4_fields_and_no_pii`
2. `test_audit_invalid_input_logs_before_raise`
3. `test_audit_fail_closed_raises_audit_error_with_cause`
4. `test_audit_error_takes_precedence_over_validation_error`
5. `test_default_audit_dir_is_outside_repo`

Các test này cung cấp bằng chứng cho cấu trúc audit bốn trường, một số kiểm tra không lộ dữ liệu mẫu, `INVALID_INPUT`, xử lý `AuditError`, ưu tiên lỗi audit và vị trí thư mục audit mặc định.

### 6.3. Các nội dung chưa thể kết luận

| Hạng mục | Bằng chứng còn thiếu |
|---|---|
| Timestamp UTC | Test hiện có kiểm tra timestamp có thông tin múi giờ, chưa trực tiếp xác nhận độ lệch UTC bằng 0 |
| Bao phủ trạng thái audit | Chưa có bằng chứng rằng tất cả nhánh nghiệp vụ, bao gồm `THEO_DOI`, đều được kiểm tra trạng thái `SUCCESS` |
| Quyền riêng tư toàn diện | Các test chỉ kiểm tra một số giá trị mẫu; chưa chứng minh mọi dữ liệu nhạy cảm đều không thể xuất hiện trong log |
| Đường dẫn audit thực tế | Test xác nhận thư mục mặc định nằm ngoài repository; cần kiểm tra biến môi trường `AUDIT_LOG_DIR` và cấu hình đang dùng |
| Repository và lịch sử Git | Chưa có kết quả rà soát toàn bộ PII, bí mật và lịch sử Git |
| CI | Chưa có bằng chứng kết quả workflow trên Pull Request trong lần đối chiếu này |
| Benchmark | Chưa có báo cáo p50/p95 phù hợp |
| README | Chưa xác minh nội dung hiện tại và cảnh báo bắt buộc |

## 7. Kiểm thử audit và quyền riêng tư

Các kiểm tra audit phải tuân theo REQUIREMENTS v1.1:

1. Mỗi lần gọi `classify()` tạo đúng một bản ghi.
2. Bản ghi chỉ chứa `Timestamp`, `User_UUID`, `Action_Type`, `Status`.
3. `Timestamp` sử dụng ISO 8601 UTC.
4. `User_UUID` là UUID tổng hợp hợp lệ, không phải mã định danh bệnh nhân.
5. `Action_Type` phải là `CLASSIFY`.
6. `Status` chỉ nhận `SUCCESS` hoặc `INVALID_INPUT`.
7. Khi đầu vào không hợp lệ và audit hoạt động, ghi `INVALID_INPUT` trước khi phát sinh lỗi xác thực tương ứng.
8. Khi audit thất bại, phát sinh `AuditError` kế thừa `RuntimeError`, giữ lỗi gốc trong `__cause__` và không trả kết quả phân loại.
9. Nếu audit và xác thực cùng thất bại, `AuditError` được ưu tiên.
10. Không ghi dữ liệu bệnh nhân thô, triệu chứng, chỉ số sức khỏe, PII hoặc bí mật vào log.
11. Tệp audit phải nằm ngoài repository và không được commit.

### 7.1. Bằng chứng đã có

- Đã xác định năm test audit trong `tests/test_classifier.py`.
- Có test kiểm tra cấu trúc bốn trường và một số giá trị không xuất hiện trong log.
- Có test kiểm tra `INVALID_INPUT`.
- Có test mô phỏng lỗi audit và kiểm tra `AuditError` cùng `__cause__`.
- Có test kiểm tra ưu tiên lỗi audit.
- Có test kiểm tra thư mục audit mặc định nằm ngoài repository.

### 7.2. Việc cần xác minh hoặc bổ sung

- [ ] Xác nhận timestamp có độ lệch UTC bằng 0.
- [ ] Xác nhận mỗi lần gọi chỉ tạo một bản ghi trong các trạng thái cần thiết, bao gồm `THEO_DOI`.
- [ ] Kiểm tra thêm các trường hợp sai kiểu và sai miền giá trị đều ghi `INVALID_INPUT` khi audit hoạt động.
- [ ] Mở rộng kiểm tra dữ liệu nhạy cảm không xuất hiện trong audit.
- [ ] Xác minh đường dẫn audit thực tế khi có hoặc không có `AUDIT_LOG_DIR`.
- [ ] Xác nhận trạng thái Git hiện tại không chứa log cần tránh commit.

### 7.3. Kiểm tra `.audit_logs/`

Đã có ghi nhận các bước sau:

- Đã thêm `.audit_logs/` vào `.gitignore`.
- Đã kiểm tra quy tắc bằng `git check-ignore`.
- Đã commit bằng `d1f8774 chore: ignore local audit logs`.
- Đã push lên `origin/test/quy-qa-security`.
- Đã có ghi nhận working tree sạch sau commit.

Những bằng chứng này xác nhận quy tắc ignore đã được thiết lập và đẩy lên remote. Chúng **không** chứng minh đường dẫn audit thực tế nằm ngoài repository, cũng không chứng minh lịch sử Git không từng chứa log.

Trước lần commit tiếp theo, kiểm tra:

```bash
git status --short --untracked-files=all
git check-ignore -v .audit_logs/
git diff --cached --name-only
```

Không cần lặp lại việc thêm quy tắc `.audit_logs/` nếu quy tắc hiện tại vẫn tồn tại và hoạt động đúng.

## 8. Kiểm thử hiệu năng

Benchmark cần đáp ứng các yêu cầu:

- Ít nhất 100 lượt warm-up.
- Ít nhất 1000 lượt đo.
- Báo cáo p50 và p95 theo phương pháp nearest-rank.
- Ghi rõ cấu hình máy và môi trường thực thi.
- Tính cả chi phí audit thực tế.
- Đáp ứng p95 dưới 100 ms.

**Trạng thái:** Chưa xác minh do chưa có báo cáo benchmark phù hợp trong bằng chứng hiện có.

Không dùng kết quả đo cũ chỉ tính thời gian suy luận, bỏ qua audit, để kết luận yêu cầu hiệu năng tổng thể đã đạt.

## 9. Điều kiện hoàn tất kiểm thử

Chỉ coi hoạt động kiểm thử đã hoàn tất khi có đủ bằng chứng phù hợp:

- [ ] Đối chiếu logic và expected result với `docs/decision-table.md`, tag `bkt-2026-v1`.
- [ ] Chạy lại toàn bộ bộ test trên phiên bản hiện tại và ghi output thực tế.
- [ ] Xác minh audit đáp ứng hợp đồng bốn trường và xử lý đúng các tình huống lỗi.
- [ ] Xác minh các yêu cầu bảo vệ dữ liệu trong log bằng test phù hợp.
- [ ] Xác nhận đường dẫn audit thực tế nằm ngoài repository.
- [ ] Xác nhận `.audit_logs/` được ignore và không bị đưa vào commit ngoài ý muốn.
- [ ] Rà soát PII, bí mật và lịch sử Git.
- [ ] Xác nhận CI chạy thành công trên Pull Request.
- [ ] Hoàn tất benchmark và có báo cáo p50/p95.
- [ ] Xác nhận README có hướng dẫn và cảnh báo bắt buộc.
- [ ] `git diff --check` không báo lỗi định dạng.
- [ ] Kiểm tra danh sách file chuẩn bị commit không chứa log audit hoặc dữ liệu ngoài phạm vi.

## 10. Kết luận

Kế hoạch kiểm thử đã được cập nhật từ bản PC1 để phản ánh bằng chứng mới về audit và `.gitignore`. Các test audit đã xác định được ghi nhận cụ thể; quy tắc bỏ qua `.audit_logs/` cũng đã được commit và push.

Kết quả **84 passed** là kết quả đã được ghi nhận trước đó, chưa được xác nhận lại sau mọi thay đổi mới nhất. Không sử dụng con số này để khẳng định phiên bản hiện tại đã chạy thành công nếu chưa chạy lại.

Audit, quyền riêng tư toàn hệ thống, vị trí lưu log thực tế, CI, benchmark và README chỉ được kết luận đạt khi có bằng chứng tương ứng. Không kết luận toàn bộ hệ thống đạt yêu cầu chỉ dựa trên tổng số test PASS.
