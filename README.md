# BKT Rule Engine — Nhóm 26

**Track A — Dr May Day: Rule Engine Sprint**

---

##  Tóm tắt sản phẩm

Hệ thống xây dựng **Rule Engine** bằng **Python** cung cấp hàm `classify(patient)` để tiếp nhận dữ liệu synthetic, kiểm tra tính hợp lệ của đầu vào, áp dụng các quy tắc `R01-PV`, `R02-PV`, `R03-PV` và `R-SOC` theo **Decision Table V1**, sau đó trả về kết quả phân loại gồm `muc_do`, `rule_id` và `ly_do`. Hệ thống hỗ trợ xử lý dữ liệu thiếu, logic ba trạng thái và ghi audit trail theo đúng yêu cầu.

>  **Cảnh báo bắt buộc:** `educational/synthetic — not for clinical use`.

---

## Hướng dẫn cài đặt, chạy và kiểm thử từ clean checkout

### Yêu cầu hệ thống
* **Git**, **Python** (gọi được bằng lệnh `python`), **pip**.
* *(Đã kiểm thử thành công trên Windows, Python 3.15.1, pytest 9.2.0).*

### Các bước thực hiện:

```bash
# 1. Clone repository
git clone [https://github.com/DangDuyarch/ktpmud-bkt-ruleengine-starter.git](https://github.com/DangDuyarch/ktpmud-bkt-ruleengine-starter.git) 
cd ktpmud-bkt-ruleengine-starter 

# 2. Cài đặt các gói phụ thuộc
python -m pip install -e .

# 3. Chạy bộ kiểm thử (pytest)
python -m pytest -q
