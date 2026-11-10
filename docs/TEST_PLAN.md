# TEST_PLAN.md — Kế hoạch kiểm thử Rule Engine

## 1. Thông tin chung

- **Dự án:** Rule Engine WAO/EAACI — bài tập KTPMUD, Track A.
- **Phạm vi phụ trách:** QA, kiểm thử và rà soát bảo mật/quyền riêng tư.
- **Hàm trọng tâm:** `classify()`.
- **Đặc tả đối chiếu:** `docs/decision-table.md`.
- **Mã kiểm thử QA:** `tests/test_classifier_qa.py`.
- **Mã kiểm thử sẵn có của dự án:** `tests/test_classifier.py`.
- **Tài liệu liên quan:** `docs/AC_TRACEABILITY.md`, `docs/SECURITY_PRIVACY_CHECKLIST.md`.

Tài liệu này mô tả phạm vi, phương pháp, tiêu chí và cách ghi nhận kiểm thử. Kết quả trong tài liệu chỉ phản ánh những lần chạy đã ghi nhận; không mặc định rằng mọi yêu cầu đều đã được xác minh.

## 2. Mục tiêu

1. Kiểm tra kết quả của `classify()` theo các quy tắc và thứ tự ưu tiên được mô tả trong đặc tả.
2. Kiểm tra những trường hợp biên có thể làm thay đổi kết quả, đặc biệt là dữ liệu tuổi và điều kiện huyết áp.
3. Kiểm tra cách xử lý đầu vào thiếu, `None`, sai kiểu hoặc ngoài miền hợp lệ theo hợp đồng đầu vào.
4. Kiểm tra tính ổn định của cấu trúc đầu ra và tránh làm thay đổi dữ liệu đầu vào của bên gọi, trong phạm vi có test tương ứng.
5. Ghi nhận riêng các yêu cầu về audit, log, quyền riêng tư và hiệu năng để không kết luận đạt khi chưa có bằng chứng phù hợp.

## 3. Phạm vi kiểm thử

### 3.1. Trong phạm vi

- Kết quả phân loại theo các nhánh quy tắc trong `docs/decision-table.md`.
- Thứ tự ưu tiên khi nhiều quy tắc cùng có thể khớp.
- Các trường hợp thiếu dữ liệu tuổi và thứ tự xử lý xác thực dữ liệu.
- Điều kiện huyết áp, bao gồm ranh giới giảm huyết áp tương đối 30% đã được nhóm kiểm tra.
- Một số đầu vào sai kiểu, giá trị âm hoặc giá trị không hợp lệ được đưa vào bộ test.
- Kiểm tra hồi quy bằng cách chạy toàn bộ test tự động.
- Rà soát mã và tài liệu liên quan đến an toàn dữ liệu, audit và quyền riêng tư; các nội dung này được đánh dấu theo bằng chứng thực tế.

### 3.2. Ngoài phạm vi hoặc chưa đủ bằng chứng

- Chưa khẳng định toàn bộ hệ thống đáp ứng mọi yêu cầu chỉ từ kết quả test của hàm `classify()`.
- Chưa coi việc test hàm đơn lẻ là bằng chứng audit trail được ghi đầy đủ trong luồng chạy thực tế.
- Chưa xác nhận đầy đủ việc loại bỏ dữ liệu nhạy cảm khỏi log ở mọi đường đi xử lý.
- Chưa có benchmark toàn hệ thống có I/O thực tế được xác nhận trong phạm vi kết quả đang ghi nhận.
- Chưa khẳng định kiểm thử CI từ clean checkout đạt nếu chưa có kết quả chạy tương ứng.

## 4. Môi trường và cách chạy

- **Ngôn ngữ:** Python.
- **Framework:** `pytest`.
- **Lệnh chạy toàn bộ test:**

```bash
python -m pytest -q
```

Chạy lệnh từ thư mục gốc repository. Khi kiểm thử trên máy mới hoặc môi trường CI, cần cài các phụ thuộc theo hướng dẫn của repository trước khi chạy.

### Quy trình chạy

1. Đồng bộ nhánh với phiên bản code cần kiểm thử.
2. Kiểm tra `git status` để xác định các thay đổi đang có.
3. Chạy `python -m pytest -q`.
4. Ghi lại lệnh, kết quả, commit/phiên bản được kiểm thử và lỗi nếu có.
5. Nếu test thất bại, lưu thông tin lỗi, phân loại nguyên nhân và chạy lại sau khi sửa.
6. Chỉ cập nhật trạng thái tài liệu theo kết quả mới nhất đã quan sát được.

## 5. Ma trận nhóm kiểm thử

| Mã nhóm | Nhóm kiểm thử         | Nội dung                                                                                 | Kết quả mong đợi                                                                                    | Bằng chứng                                                                          |
| ------- | --------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| TP-01   | Quy tắc phân loại     | Các đầu vào đại diện cho những nhánh được mô tả trong decision table                     | Nhãn phân loại và mã quy tắc khớp đặc tả                                                            | `tests/test_classifier.py`, `tests/test_classifier_qa.py`, `docs/decision-table.md` |
| TP-02   | Thứ tự ưu tiên        | Đầu vào có nhiều điều kiện/quy tắc cùng khớp                                             | Chọn kết quả theo thứ tự ưu tiên đã quy định; không tự thêm quy tắc                                 | Test tương ứng và decision table                                                    |
| TP-03   | Thiếu dữ liệu tuổi    | Tuổi bị thiếu hoặc không có giá trị trong những trường hợp được kiểm tra                 | Xử lý đúng theo đặc tả và đúng thứ tự xác thực; không đưa ra kết luận vượt quá dữ liệu              | Test QA liên quan và kết quả chạy                                                   |
| TP-04   | Ranh giới huyết áp    | Giá trị ở dưới, đúng bằng và ở trên ngưỡng; trường hợp giảm tương đối 30%                | Kết quả ở mỗi phía ngưỡng khớp quy ước của đặc tả                                                   | Test biên trong bộ test                                                             |
| TP-05   | Kiểu dữ liệu          | Dữ liệu số/boolean/chuỗi không đúng kiểu theo hợp đồng đầu vào                           | Được chấp nhận hoặc từ chối đúng như đặc tả; không âm thầm diễn giải sai kiểu                       | Test đầu vào không hợp lệ                                                           |
| TP-06   | Miền giá trị          | Giá trị âm hoặc giá trị ngoài miền hợp lệ đã được quy định                               | Phản hồi đúng theo hợp đồng; không phát sinh kết quả phân loại sai                                  | Test xác thực dữ liệu                                                               |
| TP-07   | Cấu trúc đầu ra       | Các trường hợp đầu ra có nhãn, mã quy tắc và lý do                                       | Cấu trúc và giá trị đầu ra đúng hợp đồng đã được đặc tả                                             | Assertion trong test và rà soát code                                                |
| TP-08   | Tính toàn vẹn đầu vào | Kiểm tra dữ liệu đầu vào có bị hàm sửa ngoài ý muốn hay không, nếu có test tương ứng     | Dữ liệu của bên gọi không bị thay đổi ngoài hợp đồng                                                | Test tương ứng hoặc kiểm tra mã                                                     |
| TP-09   | Hồi quy               | Chạy lại toàn bộ test sau khi cập nhật code hoặc test                                    | Test hiện có tiếp tục đạt; lỗi đã sửa không xuất hiện lại                                           | Kết quả `pytest` mới nhất                                                           |
| TP-10   | Audit trail           | Kiểm tra việc ghi nhận hành động, thời điểm, định danh và trạng thái trong luồng thực tế | Chỉ đánh dấu đạt khi có test/bằng chứng audit thực tế; test hàm phân loại đơn lẻ không đủ           | Mã triển khai, test audit và log thử nghiệm nếu có                                  |
| TP-11   | Log và quyền riêng tư | Rà soát việc không ghi dữ liệu nhạy cảm không cần thiết và cách xử lý lỗi                | Chỉ đánh dấu đạt với bằng chứng phù hợp; nếu mới đọc một phần mã thì ghi rõ phạm vi                 | `docs/SECURITY_PRIVACY_CHECKLIST.md`, mã và test liên quan                          |
| TP-12   | Hiệu năng             | Đo thời gian xử lý theo phương pháp có thể lặp lại                                       | Phân biệt benchmark hàm đơn lẻ với hiệu năng toàn hệ thống; không kết luận khi chưa đo đúng phạm vi | Script, cấu hình và kết quả benchmark nếu có                                        |
| TP-13   | Môi trường sạch/CI    | Cài đặt phụ thuộc và chạy test từ checkout sạch hoặc CI                                  | Quy trình tái lập được và test đạt trên môi trường mục tiêu                                         | Workflow CI và log chạy thực tế                                                     |

**Lưu ý:** Ma trận là kế hoạch kiểm thử. Việc liệt kê một nhóm không có nghĩa nhóm đó đã được thực thi hoặc đã đạt. Với các mục không có test/bằng chứng tương ứng, trạng thái phải là **Chưa xác minh**.

## 6. Một số tình huống kiểm thử tiêu biểu

| Mã    | Tình huống                                | Cách kiểm tra                                                     | Kỳ vọng                                                             |
| ----- | ----------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| TC-01 | Đầu vào đủ dữ liệu cho một nhánh quy tắc  | Gọi `classify()` với fixture hợp lệ đã được xác định trong đặc tả | Nhãn và mã quy tắc đúng với decision table                          |
| TC-02 | Nhiều nhánh quy tắc cùng khớp             | Dùng fixture thể hiện điều kiện chồng lấn                         | Kết quả tuân theo thứ tự ưu tiên                                    |
| TC-03 | Thiếu tuổi                                | Thử trường hợp thiếu tuổi theo test đã định nghĩa                 | Xử lý đúng theo đặc tả; không bỏ qua quy tắc xác thực tuổi          |
| TC-04 | Huyết áp nằm ngay dưới ngưỡng             | Dùng dữ liệu biên trong bộ test                                   | Kết quả phù hợp với quy tắc ngưỡng                                  |
| TC-05 | Huyết áp đúng bằng ngưỡng                 | Dùng dữ liệu đúng tại ranh giới                                   | Kết quả khớp quy ước so sánh trong đặc tả                           |
| TC-06 | Huyết áp ngay trên ngưỡng                 | Dùng dữ liệu biên trong bộ test                                   | Kết quả phù hợp với quy tắc ngưỡng                                  |
| TC-07 | Giảm huyết áp tương đối tại ranh giới 30% | Đối chiếu các trường hợp hai phía ranh giới đã có trong test      | Không lệch do phép so sánh `<`, `<=` hoặc tính toán ngưỡng          |
| TC-08 | Đầu vào sai kiểu                          | Dùng giá trị sai kiểu đã được định nghĩa trong test               | Xử lý theo hợp đồng; không tự chuyển kiểu nếu đặc tả không cho phép |
| TC-09 | Đầu vào có giá trị không hợp lệ           | Dùng giá trị ngoài miền đã được định nghĩa trong test             | Từ chối hoặc xử lý theo hợp đồng đầu vào                            |
| TC-10 | Chạy hồi quy toàn bộ                      | Chạy `python -m pytest -q`                                        | Ghi lại tổng số test pass/fail và lỗi chi tiết nếu có               |

Các tình huống trên là mô tả mức kế hoạch, không thay thế input/expected cụ thể trong mã test. Trước khi bàn giao, cần đối chiếu từng tình huống với assertion thực tế để tránh ghi nhận một test chưa tồn tại.

## 7. Tiêu chí đạt/không đạt

- **Đạt:** test đã thực thi và kết quả thực tế khớp expected; có thể chỉ ra bằng chứng tương ứng.
- **Không đạt:** test đã thực thi nhưng kết quả khác expected, hoặc phát hiện lỗi.
- **Chưa xác minh:** chưa có test, chưa chạy test, hoặc bằng chứng chưa đủ để kết luận.
- **Không áp dụng:** yêu cầu không thuộc phạm vi phiên bản đang kiểm thử; cần nêu rõ lý do.

Không chuyển một mục sang “Đạt” chỉ vì toàn bộ pytest thành công. Ví dụ, test của `classify()` không tự chứng minh audit trail, bảo mật log, quyền riêng tư toàn hệ thống hoặc hiệu năng có I/O.

## 8. Kết quả thực thi đã ghi nhận

Trong lần chạy trước được ghi nhận trong quá trình làm việc, lệnh:

```bash
python -m pytest -q
```

cho kết quả:

```text
24 passed
```

Đây là kết quả của lần chạy tại thời điểm đó, không phải cam kết rằng phiên bản hiện tại vẫn đạt. Cần chạy lại trên commit sẽ bàn giao và cập nhật kết quả chính xác, bao gồm số test thất bại nếu có.

| Hạng mục                                           | Trạng thái ghi nhận                      | Ghi chú                                       |
| -------------------------------------------------- | ---------------------------------------- | --------------------------------------------- |
| Bộ test tự động trong lần chạy đã ghi nhận         | 24 passed                                | Cần chạy lại trước khi bàn giao               |
| Quy tắc phân loại và các trường hợp biên được test | Được kiểm tra trong phạm vi test hiện có | Đối chiếu lại với decision table              |
| Audit trail thực tế                                | Chưa xác minh đầy đủ                     | Cần bằng chứng từ triển khai và test audit    |
| Log và quyền riêng tư toàn hệ thống                | Chưa xác minh đầy đủ                     | Không suy ra từ pytest pass                   |
| Benchmark toàn hệ thống có I/O                     | Chưa xác minh                            | Không dùng microbenchmark hàm đơn lẻ thay thế |
| Clean checkout/CI trên commit bàn giao             | Chưa xác minh trong tài liệu này         | Ghi nhận sau khi chạy thực tế                 |

## 9. Liên kết với tài liệu QA khác

- `docs/decision-table.md`: nguồn đối chiếu quy tắc và expected.
- `docs/AC_TRACEABILITY.md`: liên kết tiêu chí nghiệm thu với test/bằng chứng và trạng thái.
- `docs/SECURITY_PRIVACY_CHECKLIST.md`: danh sách kiểm tra bảo mật và quyền riêng tư.
- `tests/test_classifier.py`: bộ test sẵn có của dự án.
- `tests/test_classifier_qa.py`: bộ test QA bổ sung.

Nếu trạng thái trong Test Plan khác với kết quả chạy mới nhất hoặc bảng truy vết, cần cập nhật các tài liệu để thống nhất.

