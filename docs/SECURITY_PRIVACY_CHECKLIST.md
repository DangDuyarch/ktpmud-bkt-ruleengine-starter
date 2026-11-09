# DANH SÁCH KIỂM TRA BẢO MẬT VÀ QUYỀN RIÊNG TƯ

## 1. Mục đích

Tài liệu này ghi nhận việc rà soát bảo mật và quyền riêng tư cho dự án Rule Engine WAO/EAACI trong khuôn khổ bài tập học phần KTPMUD.

Việc kiểm tra tập trung vào dữ liệu đầu vào, đầu ra, xử lý dữ liệu thiếu, tính nhất quán của quy tắc, bảo vệ thông tin nhạy cảm và các yêu cầu liên quan đến ghi nhận hoạt động.

Đây là checklist phục vụ đánh giá học tập, không thay thế quy trình kiểm thử an toàn lâm sàng hoặc đánh giá bảo mật chuyên nghiệp.

## 2. Danh sách kiểm tra

| Mã | Nội dung kiểm tra | Phương pháp xác minh | Trạng thái |
|---|---|---|---|
| BM-01 | Đầu vào không yêu cầu thông tin định danh không cần thiết | Đối chiếu Data Dictionary trong `docs/decision-table.md` | Đạt theo đặc tả |
| BM-02 | Test không sử dụng dữ liệu bệnh nhân thật có thể định danh | Rà soát dữ liệu trong các file test đã kiểm tra | Đạt theo dữ liệu test đã kiểm tra |
| BM-03 | Không ghi dữ liệu lâm sàng nhạy cảm vào log hoặc thông báo lỗi không cần thiết | Rà soát code, cơ chế log và xử lý lỗi | Chưa xác minh đầy đủ |
| BM-04 | Xử lý dữ liệu thiếu, sai kiểu hoặc ngoài phạm vi một cách nhất quán | Kiểm thử các trường hợp đầu vào không hợp lệ | Đang kiểm thử |
| BM-05 | Không tự bổ sung quy tắc hoặc ngưỡng lâm sàng ngoài đặc tả | Đối chiếu `classifier.py` với `docs/decision-table.md` | Đạt theo code đã rà soát |
| BM-06 | Cấu trúc đầu ra đúng đặc tả | Kiểm tra các trường và giá trị trả về của `classify()` | Đạt theo bộ test hiện tại |
| BM-07 | Trường `ly_do` không đưa dữ liệu lâm sàng thô vào thông báo | Rà soát các nhánh trả kết quả trong `classifier.py` | Đạt theo code đã rà soát |
| BM-08 | Không đưa mật khẩu, token, khóa bí mật hoặc thông tin xác thực vào mã nguồn | Rà soát file được Git quản lý, cấu hình và lịch sử Git | Chưa xác minh đầy đủ |
| BM-09 | Các thư viện phụ thuộc được khai báo và có thể cài đặt | Kiểm tra `requirements.txt` và thử cài đặt trong môi trường sạch | Đã khai báo; chưa xác minh cài đặt sạch |
| BM-10 | Tài liệu nêu rõ mục đích học tập và giới hạn sử dụng | Rà soát README và `docs/decision-table.md` | Đang hoàn thiện xác minh |
| BM-11 | Có cơ chế audit trail theo yêu cầu dự án | Tìm kiếm và rà soát cơ chế ghi nhận `Timestamp`, `User_UUID`, `Action_Type`, `Status` | Chưa thấy triển khai trong các file đã kiểm tra |

## 3. Quy ước trạng thái

- **Chưa xác minh:** Chưa thực hiện kiểm tra hoặc chưa có đủ minh chứng.
- **Đang kiểm thử:** Đã kiểm tra một phần nhưng chưa đủ căn cứ để kết luận.
- **Đạt:** Có minh chứng cho thấy tiêu chí được đáp ứng trong phạm vi kiểm tra.
- **Không đạt:** Phát hiện vấn đề không đáp ứng tiêu chí.
- **Không áp dụng:** Tiêu chí không thuộc phạm vi dự án và đã được nhóm thống nhất loại trừ.

Các trạng thái như “Đạt theo code đã rà soát” và “Đạt theo bộ test hiện tại” chỉ áp dụng trong phạm vi minh chứng tương ứng.

## 4. Kết quả kiểm thử liên quan

Lệnh kiểm thử:

```bash
python -m pytest -q
```

Kết quả gần nhất:

```text
24 passed in 0.03s
```

Bộ test hiện tại đã chạy thành công với 24 test đạt.

Phép đo sơ bộ thời gian thực thi hàm `classify()`:

```text
Trung binh: 0.0013 ms/lan
```

Phép đo được thực hiện bằng `timeit` với 10.000 lần gọi hàm trên một đầu vào cụ thể. Kết quả thấp hơn ngưỡng 100 ms/lần nêu trong README, nhưng chưa đại diện cho độ trễ toàn hệ thống.

Các giới hạn của kết quả kiểm tra:

- Bộ test hiện tại không chứng minh hệ thống không có lỗ hổng bảo mật.
- Thời gian chạy toàn bộ pytest không phải thời gian xử lý của riêng `classify()`.
- Chưa xác minh cài đặt phụ thuộc trong môi trường sạch.
- Chưa tìm thấy triển khai audit trail trong các file đã rà soát.
- Chưa hoàn tất kiểm tra đầu vào sai kiểu, cấu hình và lịch sử Git.

## 5. Nguyên tắc bảo mật và quyền riêng tư

1. Chỉ sử dụng các trường dữ liệu cần thiết cho chức năng phân loại.
2. Không đưa dữ liệu bệnh nhân có thể định danh vào test, log hoặc minh chứng.
3. Không tự bổ sung quy tắc lâm sàng ngoài đặc tả đã thống nhất.
4. Không coi việc toàn bộ test đạt là bằng chứng đầy đủ về an toàn hoặc bảo mật.
5. Không đưa thông tin xác thực hoặc dữ liệu nhạy cảm lên Git.
6. Ghi nhận phát hiện, minh chứng và trạng thái xử lý rõ ràng.
7. Với yêu cầu chưa được đặc tả rõ, trao đổi với nhóm trước khi tự thay đổi hành vi hệ thống.
8. Không ghi dữ liệu lâm sàng thô vào audit log nếu không cần thiết; cần thống nhất phạm vi và quyền truy cập log với nhóm.

## 6. Minh chứng cần lưu

- Kết quả chạy `python -m pytest -q`.
- Kết quả đo thời gian thực thi `classify()`.
- Các test case liên quan đến dữ liệu thiếu và các nhánh phân loại.
- Kết quả rà soát code, log và thông báo lỗi.
- Kết quả rà soát cấu hình, thư viện phụ thuộc và lịch sử Git.
- Kết quả kiểm tra README và các tài liệu dự án.
- Minh chứng triển khai audit trail nếu chức năng này được bổ sung.
