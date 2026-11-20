# BKT Rule Engine — Nhóm 26
**Track A — Dr May Day: Rule Engine Sprint**

> ⚠️ **Cảnh báo bắt buộc:** `educational/synthetic — not for clinical use.`  
> Dự án phục vụ mục đích học tập và kiểm thử với dữ liệu tổng hợp, không dùng dữ liệu bệnh nhân thật và không cung cấp lời khuyên chẩn đoán hoặc điều trị.

---

## Tóm tắt sản phẩm

Dự án thuộc Track A — Dr May Day: Rule Engine Sprint, xây dựng mô-đun Python thực hiện phân loại theo các quy tắc được quy định trong Decision Table.

Hệ thống nhận dữ liệu đầu vào tổng hợp (synthetic data), kiểm tra tính hợp lệ của dữ liệu, áp dụng các quy tắc theo thứ tự ưu tiên và trả về kết quả phân loại cùng mã quy tắc và lý do tương ứng. Hệ thống cũng ghi audit log để hỗ trợ kiểm tra hoạt động và xử lý lỗi.

* **Dự án:** KTPMUD Hack Marathon 2026
* **Track:** Track A — Dr May Day Rule Engine Sprint
* **Nguồn quy tắc nghiệp vụ:** `docs/decision-table.md`
* **Phiên bản starter:** `bkt-2026-v1`
* **Repository mã nguồn:** [`ktpmud-bkt-ruleengine-starter`](https://github.com/DangDuyarch/ktpmud-bkt-ruleengine-starter)

---

## Hướng dẫn cài đặt, chạy và kiểm thử từ clean checkout

### 2.1. Yêu cầu
* Python tương thích với dự án.
* Git.
* Các thư viện được khai báo trong `requirements.txt`.

### 2.2. Clone mã nguồn từ nhánh Track A
Mở terminal và chạy:

```bash
git clone --branch Track_A_Development [https://github.com/DangDuyarch/ktpmud-bkt-ruleengine-starter.git](https://github.com/DangDuyarch/ktpmud-bkt-ruleengine-starter.git)
cd ktpmud-bkt-ruleengine-starter
```

Lệnh trên tải mã nguồn trực tiếp từ nhánh Track_A_Development của repository nhóm.

### 2.3. Cài đặt môi trường
Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Git Bash/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2.4. Chạy kiểm thử
Từ thư mục gốc của repository:

```bash
python -m pytest -q
```

Để xem chi tiết từng test:

```bash
python -m pytest -v
```

> Kết quả được ghi nhận trong một lần chạy trước đó là 84 passed, 0 failed. Đây là kết quả lịch sử; cần chạy lại trên commit nộp bài để xác nhận trạng thái của phiên bản cuối cùng.

---

> Lưu ý: README này mô tả cách sử dụng và các tài liệu của dự án. Việc hoàn thành README không thay thế cho việc kiểm tra mã nguồn, chạy test, xác minh CI hoặc nghiệm thu của giảng viên/trợ giảng.

`educational/synthetic — not for clinical use`  
Slide/demo: https://docs.google.com/presentation/d/11_dHq-RzoCugc5NalHWmvilyhEb8pLO12zfARVi3lt0/edit?usp=sharing
