# BẢNG TRUY VẾT YÊU CẦU VÀ TIÊU CHÍ NGHIỆM THU

## 1. Mục đích

Tài liệu này liên kết các yêu cầu trong đặc tả với phương pháp kiểm thử, kết quả mong đợi và trạng thái xác minh của dự án Rule Engine WAO/EAACI.

Các tiêu chí kiểm thử phải tuân thủ `docs/decision-table.md`. Không tự bổ sung ngưỡng huyết áp hoặc quy tắc phân loại ngoài đặc tả.

## 2. Bảng truy vết yêu cầu

| Mã yêu cầu | Nội dung cần xác minh | Phương pháp kiểm thử | Kết quả mong đợi | Trạng thái |
|---|---|---|---|---|
| YC-01 | Cấu trúc kết quả của hàm `classify()` | Kiểm tra các trường trong kết quả trả về | Có đủ `muc_do`, `rule_id`, `ly_do` theo đặc tả | Đạt theo bộ test hiện tại |
| YC-02 | Quy tắc R01 | Kiểm thử trường hợp thỏa và không thỏa điều kiện R01 | Kết quả phân loại và mã `R01-PV` đúng đặc tả | Đạt theo bộ test hiện tại |
| YC-03 | Quy tắc R02 | Kiểm thử điều kiện dị nguyên nghi ngờ và số hệ cơ quan có triệu chứng | Kết quả phân loại và mã `R02-PV` đúng đặc tả | Đạt theo bộ test hiện tại |
| YC-04 | Quy tắc R03 | Kiểm thử điều kiện dị nguyên, đường hít, hô hấp và tuần hoàn | Kết quả phân loại và mã `R03-PV` đúng đặc tả | Đạt theo bộ test hiện tại |
| YC-05 | Quy tắc sốc phản vệ | Kiểm thử ngưỡng huyết áp theo tuổi và mức giảm huyết áp so với nền | Chỉ phân loại sốc khi thỏa điều kiện theo đặc tả | Đạt theo bộ test hiện tại |
| YC-06 | Trường hợp không thỏa quy tắc phân loại | Kiểm thử đầu vào không thỏa điều kiện phân loại | Trả `THEO_DOI`, `rule_id` là `None` | Đạt theo bộ test hiện tại |
| YC-07 | Mã quy tắc trả về | Đối chiếu mã quy tắc ở các nhánh phân loại | Chỉ sử dụng các mã quy tắc được quy định trong đặc tả | Đạt theo code đã rà soát |
| YC-08 | Dữ liệu thiếu, sai kiểu hoặc ngoài phạm vi | Kiểm thử thiếu tuổi và các trường hợp đầu vào không hợp lệ | Xử lý nhất quán theo đặc tả và chính sách đầu vào đã thống nhất | Đang kiểm thử |
| YC-09 | Nội dung trường `ly_do` | Kiểm tra kiểu dữ liệu và nội dung lý do trả về | Lý do ngắn gọn, phù hợp kết quả và không đưa dữ liệu lâm sàng thô vào thông báo | Đạt theo code đã rà soát |
| YC-10 | Khả năng chạy bộ test tự động | Chạy `python -m pytest -q` | Bộ test chạy hoàn tất, các test hiện có đều đạt | Đạt — 24/24 |
| YC-11 | Giới hạn sử dụng của hệ thống | Rà soát README và `docs/decision-table.md` | Nêu rõ mục đích học tập, phạm vi và giới hạn sử dụng của hệ thống | Đang hoàn thiện xác minh |
| YC-12 | Audit trail cho mỗi lần phân loại | Rà soát mã nguồn và kiểm thử cơ chế ghi nhận hoạt động | Có ghi nhận `Timestamp`, `User_UUID`, `Action_Type`, `Status` theo yêu cầu dự án | Chưa thấy triển khai trong các file đã kiểm tra |
| YC-13 | Thời gian thực thi chức năng phân loại | Đo thời gian gọi `classify()` và lưu kết quả benchmark | Thời gian thực thi nhỏ hơn 100 ms/lần | Đạt trong phép đo sơ bộ |

## 3. Kết quả kiểm thử

Lệnh kiểm thử:

```bash
python -m pytest -q
```

Kết quả gần nhất:

```text
24 passed in 0.03s
```

Bộ test hiện tại đã chạy thành công với 24 test đạt và không có test thất bại.

Phép đo sơ bộ thời gian thực thi:

```text
Trung binh: 0.0013 ms/lan
```

Phép đo sử dụng 10.000 lần gọi `classify()` với một đầu vào cụ thể. Kết quả đáp ứng ngưỡng 100 ms/lần trong phép đo này, nhưng chưa xác minh độ trễ của toàn hệ thống hoặc các điều kiện tải khác.

Các lỗi được ghi nhận ở lần kiểm thử trước gồm:

- Trường hợp thiếu `tuoi` trả về mức phân loại không đúng yêu cầu.
- Test biên giảm huyết áp 30% chưa tách biệt được điều kiện HATT dưới 90 mmHg.

Sau khi lấy code mới nhất về, bộ test đã chạy lại thành công. Kết quả này chỉ phản ánh các trường hợp đang được kiểm thử.

## 4. Quy ước trạng thái

- **Chưa xác minh:** Chưa có đủ minh chứng để kết luận.
- **Đang kiểm thử:** Đã thực hiện một phần kiểm tra nhưng chưa đủ căn cứ để kết luận toàn bộ yêu cầu.
- **Đạt:** Kết quả thực tế đáp ứng tiêu chí nghiệm thu và có minh chứng phù hợp.
- **Không đạt:** Có kết quả kiểm thử cho thấy yêu cầu chưa được đáp ứng.

Trạng thái “Đạt theo bộ test hiện tại” chỉ áp dụng trong phạm vi các trường hợp đã được kiểm thử, không thay thế việc xác minh toàn diện.

## 5. Nguyên tắc xác minh

1. Đối chiếu yêu cầu với `docs/decision-table.md`.
2. Chỉ đánh dấu Đạt khi có minh chứng thực tế.
3. Phân biệt lỗi triển khai với lỗi thiết kế test.
4. Không tự đặt thêm quy tắc hoặc ngưỡng lâm sàng.
5. Không sử dụng dữ liệu bệnh nhân có thể định danh trong test hoặc minh chứng.
6. Ghi nhận lệnh kiểm thử, kết quả và các lỗi phát hiện được.
7. Với yêu cầu chưa được đặc tả rõ, cần thống nhất với nhóm trước khi kết luận.
8. Với benchmark, ghi rõ phương pháp đo, đầu vào, số lần lặp và phạm vi đo.
9. Với audit trail, xác minh cả nội dung bản ghi và việc ghi nhận đúng theo yêu cầu.

## 6. Minh chứng

- Kết quả chạy `python -m pytest -q`.
- Các test case trong thư mục `tests/`.
- Đặc tả `docs/decision-table.md`.
- Kết quả rà soát đầu vào, đầu ra và các nhánh phân loại.
- Kết quả benchmark riêng hàm `classify()`.
- Kết quả kiểm tra README và checklist bảo mật, quyền riêng tư.
- Minh chứng triển khai và kiểm thử audit trail nếu chức năng này được bổ sung.
