# REQUIREMENTS

## Yêu cầu và phạm vi hệ thống — Track A: Dr May Day Rule Engine Sprint

### 1. Thông tin tài liệu

| Thuộc tính | Giá trị |
| ----- | ----- |
| **Cuộc thi** | KTPMUD Hack Marathon 2026 |
| **Track** | Track A — Dr May Day: Rule Engine Sprint |
| **Nhóm** | Nhóm 26 |
| **Người phụ trách tài liệu** | Đặng Văn Duy |
| **Mốc bàn giao** | M1 — Understand (Checkpoint 1) |
| **Phiên bản / trạng thái** | v1.1 — Bản hiệu chỉnh sau rà soát, chờ peer review; chưa triển khai, chưa có bằng chứng test/CI/benchmark |
| **Nguồn nghiệp vụ duy nhất** | `docs/decision-table.md`, tag `bkt-2026-v1` (repo `fossbk-spec/ktpmud-bkt-ruleengine-starter`); không dùng tài liệu nghiệp vụ nào khác |
| **Cảnh báo bắt buộc** | educational/synthetic — not for clinical use |

---

### 2. Mục tiêu và phạm vi

#### 2.1. Mục tiêu
Xây dựng module Rule Engine bằng Python với hàm `classify(patient)`: nhận dữ liệu giả lập (synthetic) theo Data Dictionary, áp dụng đúng bảng quyết định Track A (V1) và trả kết quả có giải thích. Module ghi audit trail tối thiểu, không lưu dữ liệu lâm sàng thô hoặc thông tin định danh.

Đây là sản phẩm học tập, không phải công cụ chẩn đoán hay hỗ trợ quyết định điều trị. README phải có dòng cảnh báo: `educational/synthetic — not for clinical use`.

#### 2.2. Phạm vi

| Trong phạm vi | Ngoài phạm vi |
| ----- | ----- |
| Phân loại phản vệ và sốc phản vệ đúng Decision Table V1 | Giao diện bệnh viện hoàn chỉnh, hệ thống quản lý bệnh nhân |
| Validation input, output ba trường, giải thích kết quả, audit bốn trường | Dữ liệu bệnh nhân thật; kết nối production, Railway hoặc CSDL thật |
| Unit test, chạy từ clean checkout, CI trên Pull Request, benchmark | Chẩn đoán, khuyến nghị điều trị, tư vấn y tế |
| Tài liệu yêu cầu, quyết định thiết kế, bằng chứng kiểm thử | Machine/deep learning; tự thêm hoặc sửa rule, ngưỡng ngoài đặc tả |

---

### 3. Hợp đồng dữ liệu đầu vào

#### 3.1. Danh sách trường (chỉ chín khóa này)

| Trường | Kiểu | Miền hợp lệ | Thiếu / null | Ghi chú |
| ----- | ----- | ----- | ----- | ----- |
| `tuoi` | float (năm) | Hữu hạn, $\ge 0$; nhận int hoặc float, không nhận bool | Hợp lệ; kết quả THEO_DOI | Cho phép số lẻ (0.5 = 6 tháng) |
| `huyet_ap_tam_thu` | int \| null | Số nguyên $\ge 0$ (mmHg); không nhận bool, float, chuỗi | Hợp lệ; chưa xác nhận được sốc | HATT hiện tại |
| `huyet_ap_tam_thu_nen` | int \| null | Số nguyên $> 0$; chỉ dùng khi tuổi $\ge 18$ | Hợp lệ; không xét nhánh giảm $> 30\%$ | HATT nền cho nhánh giảm tương đối ở tuổi $\ge 18$ |
| `co_di_nguyen_nghi_ngo` | bool | True / False | Hợp lệ; coi là chưa biết | Có dị nguyên nghi ngờ; xuất hiện cả nhánh phủ định và khẳng định |
| `di_nguyen_qua_duong_hit` | bool | True / False | Như trên | Dị nguyên qua đường hít, ảnh hưởng nhánh hô hấp |
| `co_ton_thuong_da_niem_mac` | bool | True / False | Như trên | Tổn thương da/niêm mạc |
| `co_trieu_chung_ho_hap` | bool | True / False | Như trên | Triệu chứng hô hấp |
| `co_trieu_chung_tuan_hoan` | bool | True / False | Như trên | Triệu chứng tuần hoàn |
| `co_trieu_chung_tieu_hoa_nang` | bool | True / False | Như trên | Triệu chứng tiêu hóa nặng |

**Zero PII:** input chỉ gồm chín trường trên; không nhận thêm khóa nào (tên, CCCD, SĐT, địa chỉ, UUID…). UUID của audit được cấp ngoài patient.

#### 3.2. Quy tắc validation
Tuổi null không còn bị coi là input invalid; boolean null không còn bị coi là sai kiểu chỉ vì null. Thiếu/null HATT hiện tại và nền là unavailable hợp lệ. Không đồng nhất unavailable với invalid. 

Phần không bị thay thế: non-null sai kiểu raise TypeError; sai miền số hoặc khóa ngoài allowlist raise ValueError. Giữ tuổi hữu hạn $\ge 0$, HATT hiện tại int $\ge 0$ và nền int $> 0$ nếu có số; bool không thay số, không ép kiểu, không tự đặt giới hạn trên. 

Validate mọi trường có mặt trước suy luận. Một trường invalid không được bỏ qua vì rule khác đã TRUE. Không đổi invalid thành UNKNOWN hoặc trả THEO_DOI để che lỗi dữ liệu. 

Khi validation lỗi và ghi audit INVALID_INPUT thành công thì raise TypeError/ValueError.; lỗi kép ưu tiên AuditError. Không đưa raw input hoặc dữ liệu nhạy cảm vào message/chaining/log. 

---

### 4. Quy tắc phân loại

#### 4.1. Tầng 2 — Phản vệ (khớp một trong ba kịch bản)

| Rule | Điều kiện khớp |
| ----- | ----- |
| **R01-PV** — Không rõ dị nguyên | `co_di_nguyen_nghi_ngo = false AND co_ton_thuong_da_niem_mac = true AND (co_trieu_chung_ho_hap = true OR co_trieu_chung_tuan_hoan = true)` |
| **R02-PV** — Dị nguyên nghi ngờ, $\ge 2/4$ hệ cơ quan | `co_di_nguyen_nghi_ngo = true AND` có ít nhất 2 trong 4 trường (`co_ton_thuong_da_niem_mac`, `co_trieu_chung_ho_hap`, `co_trieu_chung_tuan_hoan`, `co_trieu_chung_tieu_hoa_nang`) bằng `true` |
| **R03-PV** — Dị nguyên đã biết | `co_di_nguyen_nghi_ngo = true AND ((di_nguyen_qua_duong_hit = false AND co_trieu_chung_ho_hap = true) OR co_trieu_chung_tuan_hoan = true)` |

Giữ nguyên tên trường, AND/OR và dấu ngoặc của đề. Biểu thức R03 dùng `co_di_nguyen_nghi_ngo` dù tên là “dị nguyên đã biết”; nhóm bám biểu thức, không suy thêm khóa.

#### 4.2. Tầng 1 — Sốc phản vệ (`R-SOC`)
Điều kiện: đã đạt một rule Tầng 2 VÀ huyết áp tâm thu (HATT) thấp hơn ngưỡng theo tuổi. Tụt huyết áp đơn độc không đủ để kết luận.

| Nhóm tuổi | Điều kiện HATT |
| ----- | ----- |
| $0 \le \text{tuổi} < 1$ | HATT $< 70$ mmHg |
| $1 \le \text{tuổi} < 11$ | HATT $< 70 + 2 \times \text{tuổi}$ (mmHg) |
| $11 \le \text{tuổi} < 18$ | HATT $< 90$ mmHg |
| $\text{tuổi} \ge 18$ | HATT $< 90$ mmHg HOẶC giảm $> 30\%$ so với HATT nền (tương đương $10 \times \text{HATT} < 7 \times \text{nền}$) |

Các dấu so sánh là nghiêm ngặt, không đổi $<$ thành $\le$. Ở người lớn, giảm đúng 30% không thỏa điều kiện giảm trên 30%.

#### 4.3. Dữ liệu thiếu và logic ba trạng thái
Mỗi điều kiện có giá trị TRUE, FALSE hoặc UNKNOWN (UNKNOWN chỉ là trạng thái nội bộ, không xuất ra ngoài). AND: có FALSE $\rightarrow$ FALSE; mọi vế TRUE $\rightarrow$ TRUE; còn lại UNKNOWN. OR: có TRUE $\rightarrow$ TRUE; mọi vế FALSE $\rightarrow$ FALSE; còn lại UNKNOWN. NOT UNKNOWN = UNKNOWN. Đếm của R02: T = số vế TRUE, U = số vế UNKNOWN; $T \ge 2 \rightarrow$ TRUE; $T + U < 2 \rightarrow$ FALSE; còn lại UNKNOWN.

Một rule đã TRUE không bị hủy vì rule khác UNKNOWN; không bao giờ coi UNKNOWN là False để kết luận mức.

HATT thiếu, hoặc người lớn có HATT $\ge 90$ mà thiếu nền $\rightarrow$ điều kiện tụt HATT là UNKNOWN $\rightarrow$ chỉ đạt PHAN_VE, ly_do nêu chưa xác nhận được sốc.

Người lớn có HATT $< 90$ đủ chứng minh sốc dù thiếu nền.

#### 4.4. Thứ tự quyết định
1. Validate toàn bộ input (mục 3.2). Lỗi $\rightarrow$ ghi audit INVALID_INPUT rồi raise.
2. Đánh giá R01, R02, R03 và điều kiện tụt HATT theo mục 4.3.
3. Sau khi toàn bộ input có mặt đã vượt qua bước validation (Không phát sinh TypeError/ValueError), nếu `tuoi` bị thiếu/null $\rightarrow$ chuyển sang kết quả THEO_DOI, `rule_id = null`, `ly_do` nêu thiếu tuổi. Nếu có rule Tầng 2 TRUE và điều kiện tụt HATT (Tầng 1) TRUE $\rightarrow$ SOC_PHAN_VE, `rule_id = R-SOC`.
4. Có rule Tầng 2 TRUE nhưng chưa xác nhận được sốc $\rightarrow$ PHAN_VE; `rule_id` là rule TRUE đầu tiên theo ưu tiên R01 > R02 > R03.
5. Còn lại $\rightarrow$ THEO_DOI / null; `ly_do` phân biệt không khớp với chưa đủ dữ kiện.

---

### 5. Kết quả đầu ra

| Trường | Kiểu | Giá trị |
| ----- | ----- | ----- |
| `muc_do` | chuỗi | `SOC_PHAN_VE` \| `PHAN_VE` \| `THEO_DOI` |
| `rule_id` | chuỗi \| null | `R-SOC` \| `R01-PV` \| `R02-PV` \| `R03-PV`; `THEO_DOI` luôn là null |
| `ly_do` | chuỗi | Giải thích ngắn, tất định, nêu rule đã kích hoạt; không chứa dữ liệu lâm sàng thô, không lời khuyên điều trị |

Chỉ đúng ba khóa trên. THEO_DOI là trạng thái “chưa đủ dữ kiện kết luận”, không phải mức nguy cơ và không được diễn đạt là “an toàn”. Ví dụ `ly_do`: “Khớp R02-PV (dị nguyên nghi ngờ, từ 2 hệ cơ quan trở lên).”; “Thiếu thông tin tuổi (tuoi), không đủ dữ kiện để phân loại.”

---

### 6. Yêu cầu audit

| Trường | Yêu cầu |
| ----- | ----- |
| **Timestamp** | ISO 8601, múi giờ UTC |
| **User_UUID** | UUID hợp lệ, synthetic, thuộc phiên thao tác; không phải định danh bệnh nhân |
| **Action_Type** | CLASSIFY |
| **Status** | SUCCESS (phân loại hoàn tất, kể cả THEO_DOI) hoặc INVALID_INPUT (validation lỗi) |

Mỗi lần gọi `classify()` ghi đúng một bản ghi, đúng bốn trường; không ghi triệu chứng, điểm sức khỏe, số đo hay dữ liệu định danh.

Dữ liệu thiếu hợp lệ không làm Status thành INVALID_INPUT.

Fail-closed: validation lỗi và ghi audit được $\rightarrow$ ghi INVALID_INPUT rồi raise TypeError/ValueError; ghi audit lỗi (lỗi I/O, thiếu quyền ghi, đĩa đầy…) $\rightarrow$ raise AuditError (lớp con của RuntimeError; lỗi hệ thống gốc giữ ở `__cause__`) và không trả kết quả phân loại; cả hai lỗi $\rightarrow$ ưu tiên AuditError. Message không chứa giá trị input.

File audit nằm ngoài patient, ngoài repository và không được commit.

---

### 7. Yêu cầu chức năng

| ID | Yêu cầu | AC |
| ----- | ----- | ----- |
| **FR-01** | Hiện thực `classify(patient)`: giữ chữ ký, không còn NotImplementedError, không phụ thuộc ID fixture; tự điều phối validation, đánh giá rule, giải thích và audit kể cả khi gọi trực tiếp. | A-01, A-02 |
| **FR-02** | Hiện thực đúng R01-PV, R02-PV, R03-PV theo mục 4.1. | A-01, A-03 |
| **FR-03** | Hiện thực R-SOC với bốn nhóm tuổi, dấu so sánh nghiêm ngặt và nhánh giảm $> 30\%$ cho người lớn theo mục 4.2. | A-01, A-03 |
| **FR-04** | Áp dụng thứ tự quyết định mục 4.4: tuổi thiếu $\rightarrow$ THEO_DOI; ưu tiên R01 > R02 > R03; sốc chỉ khi đã đạt Tầng 2. | A-03 |
| **FR-05** | Xử lý dữ liệu thiếu bằng logic ba trạng thái (mục 4.3); không ép UNKNOWN thành False; không âm thầm sửa dữ liệu. | A-04 |
| **FR-06** | Validation nghiêm ngặt: mọi trường kể cả trường không liên quan, không ép kiểu. | A-04 |
| **FR-07** | Trả đúng ba khóa output; `ly_do` truy vết được rule, nêu thiếu tuổi/HATT/nền khi liên quan; không raw input, không lời khuyên điều trị. | A-05 |
| **FR-08** | Ghi audit bốn trường cho mỗi lần gọi theo mục 6. | A-06 |

---

### 8. Yêu cầu phi chức năng

| ID | Yêu cầu | AC |
| ----- | ----- | ----- |
| **NFR-01** | Hiệu năng: benchmark $\ge 1.000$ lần chạy sau 100 lần warm-up; báo p50/p95 (nearest-rank); p95 $< 100$ ms trên máy đo được khai báo. Phép đo chính là toàn bộ `classify()` gồm ghi audit thật. | A-10 |
| **NFR-02** | Riêng tư: chỉ dùng dữ liệu synthetic; không PII, secret, token, tệp .env trong input, test, log, repo. | A-06 |
| **NFR-03** | Toàn vẹn audit: fail-closed — ghi audit lỗi thì không trả kết quả thành công; message lỗi không lộ input. | A-06 |
| **NFR-04** | Bảo trì: tách rule thuần khỏi I/O; helper theo trách nhiệm; không framework hay abstraction thừa. | A-01, A-02 |
| **NFR-05** | Kiểm thử: test normal, boundary, invalid, missing; pytest -q đạt từ clean checkout; CI chạy test trên mọi Pull Request. | A-07, A-08, A-09 |
| **NFR-06** | Tất định: cùng input cho cùng muc_do, rule_id, ly_do, không phụ thuộc thứ tự gọi. | A-05 |
| **NFR-07** | Tài liệu: README có lệnh cài đặt/chạy/test và dòng “educational/synthetic — not for clinical use”. | A-11 |

---

### 9. Tiêu chí nghiệm thu

Trạng thái phản ánh bằng chứng hiện có tại M1; chưa mục nào được xem là đạt.

| AC | Tiêu chí (theo đề) | Bằng chứng cần có | Yêu cầu | Trạng thái |
| ----- | ----- | ----- | ----- | ----- |
| **A-01** | `classify()` đúng contract, hết NotImplementedError | Test theo từng rule/ngưỡng; gọi trực tiếp với input tổng quát | FR-01–04, NFR-04 | Chưa làm |
| **A-02** | Không hard-code theo ID của public fixture | Review code; fixture độc lập | FR-01, NFR-04 | Chưa làm |
| **A-03** | Bao phủ đủ các mức phân loại theo decision-table | Test Tầng 1, Tầng 2, overlap, THEO_DOI, giá trị sát biên | FR-02–04 | Chưa làm |
| **A-04** | Xử lý input thiếu, sai kiểu, ngoài miền theo policy | Test missing/null/invalid, khóa lạ, TypeError/ValueError | FR-05, FR-06 | Chưa làm |
| **A-05** | `ly_do` truy vết được rule, không lời khuyên điều trị | Assert nội dung `ly_do`; chạy lặp cùng input cho cùng kết quả | FR-07, NFR-06 | Chưa làm |
| **A-06** | Audit đúng bốn trường, không log raw clinical input | Đọc lại file audit; test lỗi ghi; review repo không có PII/secret | FR-08, NFR-02, NFR-03 | Chưa làm |
| **A-07** | Có unit test cho normal, boundary, invalid, missing | Bộ test thay thế test stub | NFR-05 | Chưa làm |
| **A-08** | pytest -q đạt từ clean checkout | Lệnh và kết quả chạy thật | NFR-05 | Chưa làm |
| **A-09** | CI chạy test trên Pull Request | URL lượt chạy CI thành công | NFR-05 | Chưa làm |
| **A-10** | Benchmark $\ge 1.000$ lần; p50/p95; p95 $< 100$ ms | Script, số liệu thật, cấu hình máy đo | NFR-01 | Chưa làm |
| **A-11** | README ghi “educational/synthetic — not for clinical use” | Review README: lệnh cài/chạy/test và dòng cảnh báo | NFR-07 | Chưa làm |

---

### 10. Ma trận kiểm chứng mẫu (synthetic)

Kỳ vọng suy ra từ decision-table; chưa chạy engine. Test Plan sẽ chi tiết hóa.

| # | Tình huống | Kỳ vọng |
| ----- | ----- | ----- |
| **1** | Tuổi 30, không nghi dị nguyên, da/niêm mạc + hô hấp, HATT 120 | PHAN_VE / R01-PV |
| **2** | Như 1 nhưng HATT 85 | SOC_PHAN_VE / R-SOC |
| **3** | Nghi dị nguyên, da + tiêu hóa nặng, không hô hấp/tuần hoàn | PHAN_VE / R02-PV |
| **4** | Nghi dị nguyên, hít = false, chỉ hô hấp | PHAN_VE / R03-PV |
| **5** | Nghi dị nguyên, hít = true, chỉ hô hấp (R02 chỉ 1/4) | THEO_DOI / null |
| **6** | Tuổi 5, có phản vệ: HATT 79 / HATT 80 (ngưỡng 80) | SOC_PHAN_VE / PHAN_VE |
| **7** | Tuổi 0.5, có phản vệ: HATT 69 / HATT 70 | SOC_PHAN_VE / PHAN_VE |
| **8** | Tuổi 25, HATT 140, nền 200 (giảm đúng 30%), có phản vệ | PHAN_VE |
| **9** | Tuổi 25, HATT 139, nền 200 (giảm $> 30\%$), có phản vệ | SOC_PHAN_VE / R-SOC |
| **10** | Tuổi 25, HATT 89, thiếu nền, có phản vệ | SOC_PHAN_VE / R-SOC |
| **11** | Tuổi 15, có phản vệ, HATT null hoặc thiếu khóa | PHAN_VE; `ly_do` nêu chưa xác nhận sốc |
| **12** | Tuổi null hoặc thiếu, có phản vệ | THEO_DOI / null; `ly_do` nêu thiếu tuổi |
| **13** | Không khớp Tầng 2, HATT rất thấp | THEO_DOI / null (tụt HA đơn độc không đủ) |
| **14** | R02 đã TRUE, `di_nguyen_qua_duong_hit` thiếu | PHAN_VE / R02-PV (không bị hạ mức) |
| **15** | `co_di_nguyen_nghi_ngo` thiếu, các trường còn lại khớp R01/R02 | THEO_DOI / null; `ly_do` nêu chưa đủ dữ kiện |
| **16** | Tuổi là chuỗi "30", hoặc trường bool nhận số 1 | TypeError; audit INVALID_INPUT |
| **17** | Có khóa lạ (vd. `ten`), hoặc HATT âm | ValueError; audit INVALID_INPUT |
| **18** | `tuoi = null` và `co_di_nguyen_nghi_ngo = "true"` (chuỗi thay vì bool) | TypeError; audit INVALID_INPUT (validation chạy trước khi xét thiếu tuổi) |

---

### 11. Đối chiếu với decision-table

| Nội dung decision-table | Vị trí trong tài liệu | Kết quả |
| ----- | ----- | ----- |
| Data Dictionary — 9 trường, Zero PII | Mục 3.1, 3.2 | Khớp |
| Tầng 2 — R01, R02, R03 | Mục 4.1; FR-02 | Khớp |
| Tầng 1 — bốn nhóm tuổi, giảm $> 30\%$ ở người lớn | Mục 4.2; FR-03 | Khớp |
| Không khớp hoặc thiếu `tuoi` $\rightarrow$ THEO_DOI | Mục 4.4; FR-04 | Khớp |
| Output `muc_do`, `rule_id`, `ly_do` | Mục 5; FR-07 | Khớp |
| Không đổi ngưỡng, không thêm rule | Mục 2.2; FR-02, FR-03 | Khớp |
| Nội dung decision-table không quy định (ưu tiên khi nhiều rule, dữ liệu thiếu, miền số, giá trị audit) | Mục 3.2, 4.3, 4.4, 6; DECISIONS.md | Cần xác nhận (mục 12) |

---

### 12. Giả định và điểm cần xác nhận

Đề không quy định chi tiết các nội dung sau. Nhóm dùng quy ước tạm trong tài liệu này, lý do ghi ở `DECISIONS.md`; cần hỏi TA/giảng viên trước M2.

* Rule được báo khi nhiều rule Tầng 2 cùng khớp: R01 > R02 > R03 (DECISIONS D01, Q1).
* Xử lý boolean thiếu/null; tuổi thiếu khi đã đạt Tầng 2; HATT hoặc nền thiếu: theo mục 4.3, 4.4 (D02, D03; Q2, Q3).
* Miền số: HATT = 0 hợp lệ, nền = 0 không hợp lệ, không có giới hạn trên (D04, Q4).
* Giá trị Action_Type/Status, định dạng Timestamp/User_UUID, đường dẫn file audit và xử lý lỗi ghi: theo mục 6 (D07, D08; Q5, Q6).

*Nếu câu trả lời chính thức khác quy ước trên, chỉ sửa mục 3.2, 4.3, 4.4, 6 và các test tương ứng.*