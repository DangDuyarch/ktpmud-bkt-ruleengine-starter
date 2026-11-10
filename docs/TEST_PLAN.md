# KẾ HOẠCH KIỂM THỬ — TEST_PLAN

## 1. Thông tin chung

| Thuộc tính              | Nội dung                                                  |

| Dự án                   | KTPMUD Hack Marathon 2026                                 |
| Track                   | Track A — Dr May Day: Rule Engine Sprint                  |
| Nhóm                    | 26                                                        |
|                         |                                                           |
| Nguồn quy tắc nghiệp vụ | `docs/decision-table.md`                                  |
| Tag quy tắc             | `bkt-2026-v1`                                             |
| Mã nguồn cần kiểm thử   | Module triển khai hàm `classify()`                        |
| Bộ kiểm thử             | `tests/test_classifier.py`, `tests/test_classifier_qa.py` |
| Công cụ                 | Python, pytest                                            |
| Kết quả gần nhất        | 79 passed, 0 failed, 0.27 giây                            |
| Cảnh báo bắt buộc       | `educational/synthetic — not for clinical use`            |

## 2. Mục tiêu kiểm thử

Kế hoạch kiểm thử nhằm xác minh hệ thống Rule Engine có đáp ứng yêu cầu về logic phân loại, kiểm tra dữ liệu đầu vào, cấu trúc đầu ra, quyền riêng tư, audit và khả năng chạy tự động hay không.

Các mục tiêu chính:

- Kiểm tra kết quả phân loại theo đúng bảng quyết định nghiệp vụ.
- Kiểm tra thứ tự ưu tiên giữa các quy tắc và những trường hợp biên.
- Kiểm tra dữ liệu thiếu, UNKNOWN, sai kiểu, sai miền giá trị và khóa không được phép.
- Kiểm tra cấu trúc kết quả và nội dung giải thích.
- Kiểm tra audit trail, khả năng xử lý lỗi audit và việc bảo vệ dữ liệu.
- Kiểm tra khả năng chạy bộ test trong môi trường sạch và trên CI.
- Kiểm tra benchmark hiệu năng và nội dung hướng dẫn trong README.

**Nguyên tắc:** Chỉ kết luận một tiêu chí đã đạt khi có bằng chứng phù hợp. Việc pytest chạy thành công không đồng nghĩa tất cả yêu cầu nghiệm thu đều đã được xác minh.

## 3. Phạm vi kiểm thử

### 3.1. Trong phạm vi

1. Logic phân loại R01-PV, R02-PV, R03-PV và R-SOC.
2. Thứ tự ưu tiên của quy tắc và các điều kiện biên.
3. Xử lý dữ liệu đầu vào thiếu hoặc không hợp lệ.
4. Kiểm tra kiểu dữ liệu, miền giá trị và danh sách khóa cho phép.
5. Cấu trúc đầu ra gồm đúng ba khóa `muc_do`, `rule_id`, `ly_do`.
6. Tính xác định của kết quả và việc không đưa dữ liệu đầu vào cụ thể vào `ly_do`.
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

| Thành phần   | Thông tin |
| ------------ | --------- |
| Hệ điều hành | Windows   |
| Python       | 3.15.1    |
| pytest       | 9.2.0     |
| Tổng số test | 79        |
| Kết quả      | 79 passed |
| Thời gian    | 0.27 giây |

Thông tin trên được lấy từ output kiểm thử đã ghi nhận. Cần cập nhật nếu môi trường hoặc phiên bản mã nguồn thay đổi.

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

Kiểm tra định dạng thay đổi trước khi commit:

```bash
git diff --check
git status
```

Không chạy `git add .` khi chưa kiểm tra các file phát sinh, đặc biệt là thư mục audit.

## 5. Các nhóm kiểm thử và tiêu chí

| Nhóm  | Nội dung                  | Tiêu chí cần đạt                                                                      |
| ----- | ------------------------- | ------------------------------------------------------------------------------------- |
| TC-01 | Phân loại R01-PV          | Kết quả và `rule_id` đúng theo bảng quyết định                                        |
| TC-02 | Phân loại R02-PV          | Điều kiện và mức độ phân loại đúng                                                    |
| TC-03 | Phân loại R03-PV          | Điều kiện và mức độ phân loại đúng                                                    |
| TC-04 | Quy tắc R-SOC             | Chỉ áp dụng khi đủ điều kiện Tier 2 và tiêu chí huyết áp                              |
| TC-05 | Thứ tự ưu tiên            | Khi nhiều quy tắc cùng khớp, chọn đúng quy tắc ưu tiên                                |
| TC-06 | Ngưỡng theo tuổi          | Xử lý đúng các ngưỡng tuổi và trường hợp biên                                         |
| TC-07 | Giảm huyết áp ở người lớn | Phân biệt đúng mức giảm 30% và trên 30% theo yêu cầu                                  |
| TC-08 | Dữ liệu thiếu             | Xử lý đúng trường thiếu, `None` và UNKNOWN                                            |
| TC-09 | Sai kiểu dữ liệu          | Từ chối kiểu dữ liệu không hợp lệ, không ép kiểu ngầm                                 |
| TC-10 | Sai miền giá trị          | Từ chối giá trị không hợp lệ theo hợp đồng                                            |
| TC-11 | Khóa ngoài allowlist      | Từ chối khóa không nằm trong danh sách 9 khóa đầu vào                                 |
| TC-12 | Thứ tự xác thực           | Kiểm tra toàn bộ trường được cung cấp trước khi suy luận                              |
| TC-13 | Cấu trúc đầu ra           | Chỉ có `muc_do`, `rule_id`, `ly_do`                                                   |
| TC-14 | Giải thích kết quả        | `ly_do` xác định, không chứa dữ liệu đầu vào cụ thể hoặc lời khuyên điều trị          |
| TC-15 | Audit thành công          | Mỗi lần gọi có đúng một bản ghi với đúng bốn trường                                   |
| TC-16 | Audit đầu vào lỗi         | Ghi `INVALID_INPUT` khi xác thực thất bại và audit hoạt động                          |
| TC-17 | Audit thất bại            | Phát sinh `AuditError`, giữ lỗi gốc trong `__cause__` và không trả kết quả phân loại  |
| TC-18 | Quyền riêng tư            | Không ghi dữ liệu bệnh nhân thô, PII hoặc bí mật vào audit                            |
| TC-19 | CI                        | Bộ test tự động chạy thành công trên Pull Request                                     |
| TC-20 | Benchmark                 | Có ít nhất 100 lượt warm-up, 1000 lượt đo, báo cáo p50/p95 và đáp ứng p95 dưới 100 ms |
| TC-21 | README                    | Có hướng dẫn cài đặt, chạy, kiểm thử và cảnh báo bắt buộc chính xác                   |

Các nhóm TC-01 đến TC-14 có bằng chứng kiểm thử trong output 79 test đã cung cấp, nhưng cần đối chiếu nội dung test với bảng quyết định để xác nhận phạm vi chính xác. Các nhóm TC-15 đến TC-21 cần bằng chứng riêng trước khi kết luận đạt.

## 6. Kết quả kiểm thử đã ghi nhận

Lần chạy gần nhất:

```text
python -m pytest -v

collected 79 items
79 passed in 0.27s
```

### 6.1. Các nội dung đã có bằng chứng kiểm thử

- Các trường hợp phân loại R01-PV, R02-PV và R03-PV.
- Thứ tự ưu tiên khi nhiều quy tắc cùng khớp.
- Ngưỡng sốc theo tuổi.
- Trường hợp huyết áp thấp và điều kiện giảm huyết áp ở người lớn.
- Dữ liệu thiếu, `None` và UNKNOWN.
- Sai kiểu dữ liệu, sai miền giá trị và giá trị NaN/vô hạn.
- Khóa ngoài allowlist.
- Xác thực đầu vào trước khi suy luận.
- Cấu trúc đầu ra, `rule_id` của `THEO_DOI` và tính xác định.
- Một số kiểm tra nhằm phát hiện giá trị đầu vào xuất hiện trong `ly_do`.

### 6.2. Các nội dung chưa thể kết luận

| Hạng mục                       | Bằng chứng còn thiếu                           |
| ------------------------------ | ---------------------------------------------- |
| Audit                          | Kiểm tra bản ghi thực tế và đúng bốn trường    |
| Audit khi đầu vào không hợp lệ | Xác nhận bản ghi `INVALID_INPUT`               |
| Audit fail-closed              | Mô phỏng lỗi I/O và xác nhận `AuditError`      |
| Ưu tiên lỗi audit              | Kiểm tra tình huống audit và xác thực cùng lỗi |
| Lưu audit an toàn              | Xác nhận tệp audit nằm ngoài repository        |
| Quyền riêng tư toàn hệ thống   | Rà soát mã nguồn, log, test và lịch sử Git     |
| CI                             | Kết quả chạy trên Pull Request                 |
| Benchmark                      | Báo cáo p50/p95 và môi trường đo               |
| README                         | Kiểm tra nội dung và dòng cảnh báo bắt buộc    |

Lưu ý: Một test kiểm tra vài giá trị cụ thể không đủ chứng minh `ly_do` không thể làm lộ bất kỳ dữ liệu đầu vào nào. Tương tự, 79 test PASS không tự chứng minh audit an toàn hoặc mọi nhánh nghiệp vụ đã được bao phủ.

## 7. Kiểm thử audit và quyền riêng tư

Các kiểm tra audit phải tuân theo REQUIREMENTS v1.1:

1. Mỗi lần gọi tạo đúng một bản ghi.
2. Bản ghi chỉ chứa `Timestamp`, `User_UUID`, `Action_Type`, `Status`.
3. `Timestamp` sử dụng ISO 8601 UTC.
4. `User_UUID` là UUID phiên tổng hợp.
5. `Action_Type` phải là `CLASSIFY`.
6. `Status` chỉ nhận `SUCCESS` hoặc `INVALID_INPUT`.
7. Khi đầu vào không hợp lệ và audit hoạt động, ghi `INVALID_INPUT` trước khi phát sinh lỗi xác thực tương ứng.
8. Khi audit thất bại, phát sinh `AuditError` kế thừa `RuntimeError`, giữ lỗi gốc trong `__cause__` và không trả kết quả phân loại.
9. Nếu cả audit và xác thực đều lỗi, `AuditError` được ưu tiên.
10. Không ghi dữ liệu bệnh nhân thô, triệu chứng, chỉ số sức khỏe, PII hoặc bí mật vào log.
11. Tệp audit phải nằm ngoài repository và không được commit.

Trước khi commit, phải xác minh thư mục `.audit_logs/` đã xuất hiện trong `git status` trước đó. Không được coi việc thêm thư mục này vào `.gitignore` là đủ nếu vị trí lưu audit thực tế vẫn nằm trong repository.

## 8. Kiểm thử hiệu năng

Benchmark phải đáp ứng các yêu cầu:

- Chạy ít nhất 100 lượt warm-up.
- Đo ít nhất 1000 lượt chạy.
- Báo cáo percentile p50 và p95 theo phương pháp nearest-rank.
- Ghi rõ cấu hình máy và môi trường thực thi.
- Tính cả chi phí audit thực tế.
- Đáp ứng p95 dưới 100 ms.

**Trạng thái:** Chưa xác minh do chưa có báo cáo benchmark phù hợp trong bằng chứng hiện có.

## 9. Điều kiện hoàn tất kiểm thử

Chỉ coi hoạt động kiểm thử đã hoàn tất khi có đủ các bằng chứng sau:

- [ ] Đối chiếu logic và expected result với `docs/decision-table.md`, tag `bkt-2026-v1`.
- [ ] Bộ test hiện có chạy thành công.
- [ ] Audit đáp ứng hợp đồng bốn trường và xử lý đúng các tình huống lỗi.
- [ ] Xác nhận không có dữ liệu nhạy cảm trong log hoặc repository.
- [ ] Xác nhận audit nằm ngoài repository.
- [ ] CI chạy thành công trên Pull Request.
- [ ] Benchmark đáp ứng yêu cầu và có báo cáo p50/p95.
- [ ] README có đầy đủ hướng dẫn và cảnh báo bắt buộc.
- [ ] `git diff --check` không báo lỗi định dạng.
- [ ] Danh sách file chuẩn bị commit không chứa log audit hoặc dữ liệu ngoài phạm vi.

## 10. Kết luận

Tại thời điểm lập tài liệu, bộ kiểm thử đã ghi nhận **79/79 test PASS trong 0.27 giây** trên môi trường Windows với Python 3.15.1 và pytest 9.2.0.

Kết quả này cung cấp bằng chứng tích cực cho các nhóm kiểm thử logic phân loại, xác thực đầu vào và cấu trúc đầu ra. Tuy nhiên, audit, quyền riêng tư toàn hệ thống, CI, benchmark và README vẫn cần được xác minh bằng bằng chứng riêng.

Tài liệu này cần được cập nhật khi có kết quả kiểm thử mới. Không đánh dấu toàn bộ hệ thống đạt yêu cầu chỉ dựa trên số lượng test PASS.
