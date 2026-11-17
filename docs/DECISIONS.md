# DECISIONS
## NHẬT KÝ QUYẾT ĐỊNH THIẾT KẾ
### TRACK A — DR MAY DAY: RULE ENGINE SPRINT

| Thuộc tính | Thông tin |
| :--- | :--- |
| **Cuộc thi** | KTPMUD Hack Marathon 2026 |
| **Track** | Track A — Dr May Day: Rule Engine Sprint |
| **Nhóm** | Nhóm 26 |
| **Người phụ trách tài liệu** | Đặng Văn Duy |
| **Tài liệu gốc** | REQUIREMENTS - phiên bản v1.1 |
| **Phiên bản Decisions** | v1.1 — Bản hợp nhất sau đối chiếu; chờ peer review và xác nhận các mục OPEN |
| **Trạng thái triển khai** | Tài liệu quyết định thiết kế; không khẳng định code, test, CI hoặc benchmark đã hoàn thành |
| **Cảnh báo** | educational/synthetic — not for clinical use |

---

### Mục đích – Nguyên tắc – Quy ước sử dụng

Tài liệu này ghi lại các quyết định thiết kế phục vụ triển khai Rule Engine. REQUIREMENTS v1.1 là căn cứ trực tiếp để xác định contract, yêu cầu và tiêu chí nghiệm thu. DECISIONS không được dùng để sửa hoặc diễn giải lại Decision Table.

Thứ tự ưu tiên nguồn: (1) `docs/decision-table.md` tại tag `bkt-2026-v1` và clarification/erratum chính thức của TA; (2) yêu cầu đề bài được phản ánh trong REQUIREMENTS v1.1; (3) quyết định triển khai nội bộ của nhóm. Khi chưa có căn cứ chính thức, nội dung phải được đánh dấu là đề xuất hoặc OPEN.

Trạng thái “Đã chốt theo Requirements” chỉ có nghĩa là lựa chọn đã được REQUIREMENTS v1.1 quy định. Trạng thái “Quyết định triển khai” là lựa chọn kỹ thuật nội bộ, không phải quy tắc nghiệp vụ mới. Trạng thái “OPEN” cần được nhóm hoặc TA xác nhận trước khi coi là chốt.

---

## 1. Bối cảnh và ràng buộc

Sản phẩm là module Rule Engine Python độc lập, nhận dữ liệu synthetic qua `classify(patient)`, áp dụng Decision Table Track A V1, trả kết quả có giải thích và ghi audit tối thiểu. Ba mối quan tâm thiết kế là tính đúng đắn của suy luận, khả năng giải thích/truy vết và bảo vệ dữ liệu.

| Ràng buộc | Cách áp dụng trong thiết kế |
| :--- | :--- |
| **Contract đầu vào** | Giữ đúng 9 khóa được liệt kê trong REQUIREMENTS; không nhận khóa định danh hoặc khóa ngoài allowlist. |
| **Contract đầu ra** | Chỉ trả 3 khóa: `muc_do`, `rule_id`, `ly_do`. |
| **Nghiệp vụ** | Giữ nguyên R01-PV, R02-PV, R03-PV, R-SOC, biểu thức, dấu so sánh và các biên tuổi. |
| **Dữ liệu thiếu** | Phân biệt unavailable/missing/null với dữ liệu sai; dùng TRUE/FALSE/UNKNOWN theo REQUIREMENTS. |
| **Audit** | Mỗi lần gọi theo luồng quy định phải tạo một record đúng 4 trường; không ghi raw clinical input hoặc PII. |
| **Phạm vi an toàn** | Chỉ dùng synthetic; không chẩn đoán, tư vấn điều trị, production hoặc dữ liệu bệnh nhân thật. |
| **Bằng chứng nghiệm thu** | Unit test, clean checkout, CI trên Pull Request và benchmark phải có bằng chứng riêng; tài liệu này không tuyên bố đã đạt. |

---

## 2. Danh mục quyết định

| ID | Chủ đề | Trạng thái | Liên quan |
| :--- | :--- | :--- | :--- |
| **D01** | Bảo toàn contract và Decision Table | Đã chốt theo Requirements | FR-01–FR-08 |
| **D02** | Kiến trúc module tối giản, tách nghiệp vụ khỏi I/O | Quyết định triển khai | NFR-04 |
| **D03** | Ưu tiên rule khi nhiều rule Tầng 2 cùng TRUE | Theo REQUIREMENTS; cần xác nhận TA | FR-04; A-03 |
| **D04** | Xử lý missing/null và logic ba trạng thái | Theo REQUIREMENTS; cần xác nhận TA | FR-05; A-04 |
| **D05** | Validation nghiêm ngặt và exception | Đã chốt theo Requirements | FR-06; A-04 |
| **D06** | Sinh ly_do bằng template tất định | Quyết định triển khai trong giới hạn Requirements | FR-07; NFR-06; A-05 |
| **D07** | Audit writer, schema và UUID | Schema đã chốt; chi tiết triển khai một phần OPEN | FR-08; NFR-02 |
| **D08** | Fail-closed và xử lý lỗi audit | Đã chốt theo Requirements; lỗi nội bộ bất ngờ OPEN | NFR-03; A-06 |
| **D09** | Chiến lược kiểm thử theo hành vi và biên | Quyết định triển khai | NFR-05; A-01–A-09 |
| **D10** | Benchmark toàn luồng | Đã chốt theo Requirements; cách đo chi tiết triển khai | NFR-01; A-10 |

---

## 3. Kiến trúc tổng quan

`classify(patient)` là điểm vào công khai duy nhất. Hàm điều phối các bước theo thứ tự dưới đây; helper nghiệp vụ nên thuần, không tự đọc/ghi file. Audit writer là thành phần duy nhất thực hiện I/O.

| Bước / thành phần | Trách nhiệm | Nguyên tắc |
| :--- | :--- | :--- |
| **1. validate** | Kiểm tra cấu trúc, khóa, kiểu và miền của mọi trường có mặt. | Chạy trước suy luận; không bỏ qua trường invalid dù rule khác có thể TRUE. |
| **2. evaluate_rules** | Đánh giá R01-PV, R02-PV, R03-PV và điều kiện tụt HATT. | Dùng ba trạng thái TRUE/FALSE/UNKNOWN; không dùng truthiness để diễn giải UNKNOWN. |
| **3. select_result(...)** | Áp dụng thứ tự quyết định để chọn muc_do và rule_id. | Tuân thủ mục 4.4 của REQUIREMENTS; không tạo rule hoặc output mới. |
| **4. build_reason(...)** | Sinh ly_do theo template cố định. | Không chèn raw input, số đo, PII hoặc lời khuyên điều trị. |
| **5. audit.write(...)** | Ghi record JSONL theo schema audit. | Chỉ allowlist 4 trường; audit thành công trước khi trả kết quả. |
| **6. classify(patient)** | Điều phối luồng, xử lý lỗi và trả đúng output. | Không để helper nghiệp vụ phụ thuộc file hoặc trạng thái global. |

---

## 4. Các quyết định chi tiết (ADR)

### D01 — Bảo toàn contract và Decision Table

| Thuộc tính | Nội dung |
| :--- | :--- |
| **Trạng thái** | Đã chốt theo REQUIREMENTS v1.1. |
| **Bối cảnh** | Mọi thay đổi tên trường, kiểu dữ liệu, biểu thức rule, ngưỡng hoặc output có thể làm lệch đặc tả và khiến kết quả không còn đối chiếu được với Decision Table V1. |
| **Quyết định** | Giữ nguyên `classify(patient)`, đúng 9 khóa input, đúng 3 khóa output; giữ nguyên R01-PV, R02-PV, R03-PV và R-SOC. Không thêm rule, không đổi AND/OR, ngoặc, dấu so sánh hoặc ngưỡng. R03 tiếp tục dùng `co_di_nguyen_nghi_ngo` theo biểu thức được nêu trong REQUIREMENTS, dù tên mô tả rule là “dị nguyên đã biết”. |
| **Lý do** | Bảo đảm implementation và test có thể đối chiếu trực tiếp với REQUIREMENTS và decision-table.md. |
| **Đánh đổi / giới hạn** | Không có quyền tự mở rộng nghiệp vụ. Mọi thay đổi contract chỉ thực hiện khi có clarification/erratum chính thức và cập nhật REQUIREMENTS tương ứng. |
| **Phương án không chọn** | Không chọn cách “làm hợp lý hơn” bằng suy luận lâm sàng hoặc tự thêm trường/rule. |
| **Kiểm chứng** | Review chữ ký hàm, allowlist input, output keys, từng biểu thức và biên; test theo từng rule và ngưỡng. |
| **Truy vết** | REQUIREMENTS §2–§5; FR-01–FR-07; A-01–A-05. |

### D02 — Kiến trúc module tối giản

| Thuộc tính | Nội dung |
| :--- | :--- |
| **Trạng thái** | Quyết định triển khai của nhóm; cần peer review. |
| **Bối cảnh** | Validation, suy luận, tạo giải thích và ghi audit có trách nhiệm khác nhau. Trộn toàn bộ vào một khối code làm khó review biểu thức và khó cô lập lỗi. |
| **Quyết định** | Giữ `classify(patient)` làm public entry point. Tách helper theo trách nhiệm: validate, evaluate_rules, select_result, build_reason và audit writer. Helper xử lý rule/kết quả không thực hiện I/O; chỉ writer thao tác file. Chỉ tách module hoặc abstraction thêm khi có lợi ích rõ ràng. |
| **Lý do** | Phần logic thuần dễ unit test; luồng public vẫn được kiểm thử end-to-end; kiến trúc vừa đủ cho phạm vi ba rule. |
| **Đánh đổi / giới hạn** | Cần thống nhất kiểu dữ liệu nội bộ giữa helper; tránh tạo framework rule/plugin tổng quát không cần thiết. |
| **Phương án không chọn** | Không chọn một hàm lớn trộn nghiệp vụ/I/O hoặc hệ thống lớp/plugin quá mức. |
| **Kiểm chứng** | Test helper nghiệp vụ độc lập với file; test classify() trực tiếp để bảo đảm đầy đủ validation, audit và output. |
| **Truy vết** | REQUIREMENTS FR-01; NFR-04; A-01, A-02. |

### D03 — Ưu tiên rule khi nhiều rule Tầng 2 cùng TRUE

| Thuộc tính | Nội dung |
| :--- | :--- |
| **Trạng thái** | Quy ước hiện tại đã được ghi trong REQUIREMENTS v1.1; cần TA xác nhận vì Decision Table không quy định priority. |
| **Bối cảnh** | Output chỉ cho phép một rule_id, trong khi các điều kiện R01/R02/R03 có thể đồng thời TRUE. Decision Table không nêu cách chọn một rule đại diện. |
| **Quyết định** | Áp dụng thứ tự R01-PV > R02-PV > R03-PV để chọn rule_id đầu tiên có giá trị TRUE. Nếu điều kiện Tầng 1 cũng TRUE thì kết quả là SOC_PHAN_VE với rule_id = R-SOC. Không trả danh sách rule và không tự đánh giá rule nào “nặng hơn”. |
| **Lý do** | Thứ tự cố định, tất định, dễ kiểm thử và khớp FR-04 của REQUIREMENTS. |
| **Đánh đổi / giới hạn** | Priority là quy ước kỹ thuật để chọn một rule_id, không phải thứ tự mức độ nghiêm trọng lâm sàng. Cần hỏi TA; nếu clarification khác, cập nhật policy và test. |
| **Phương án không chọn** | Không chọn trả nhiều rule_id vì phá output schema; không tự chọn theo nhận định lâm sàng. |
| **Kiểm chứng** | Tạo test overlap từng cặp R01/R02, R01/R03, R02/R03 và cả ba; assert rule_id theo priority. |
| **Truy vết** | REQUIREMENTS §4.4, §12; FR-04; A-03, A-07. |

### D04 — Dữ liệu thiếu và logic ba trạng thái

| Thuộc tính | Nội dung |
| :--- | :--- |
| **Trạng thái** | Theo REQUIREMENTS v1.1; các quy ước được nêu tại §12 vẫn cần TA xác nhận. |
| **Bối cảnh** | Data Dictionary cho phép một số trường missing/null. Quy missing thành False hoặc True có thể làm thay đổi kết quả rule; coi tất cả missing là invalid cũng trái với contract hiện tại. |
| **Quyết định** | Missing và null được xem là unavailable đối với các trường mà Data Dictionary cho phép. Tuổi missing/null dẫn đến THEO_DOI, rule_id = null và ly_do nêu thiếu tuổi. HATT hiện tại hoặc HATT nền thiếu không tự động là invalid. Điều kiện tụt HATT là UNKNOWN khi thiếu dữ kiện cần thiết; nếu đã có rule Tầng 2 TRUE thì kết quả là PHAN_VE và ly_do nêu chưa xác nhận được sốc. Riêng người lớn có HATT < 90 mmHg vẫn đủ điều kiện R-SOC dù thiếu HATT nền. Một rule đã TRUE không bị hạ bởi rule khác UNKNOWN. |
| **Lý do** | Mỗi điều kiện nhận TRUE/FALSE/UNKNOWN. AND: có FALSE → FALSE; mọi vế TRUE → TRUE; còn lại UNKNOWN. OR: có TRUE → TRUE; mọi vế FALSE → FALSE; còn lại UNKNOWN. NOT UNKNOWN = UNKNOWN. Với R02, đặt T là số TRUE và U là số UNKNOWN trong bốn điều kiện: T ≥ 2 → TRUE; T + U < 2 → FALSE; trường hợp còn lại → UNKNOWN. UNKNOWN không xuất ra output. |
| **Đánh đổi / giới hạn** | Không suy đoán dữ liệu còn thiếu; giữ được khác biệt giữa “không khớp” và “chưa đủ dữ kiện”. Một số ca thiếu boolean có thể ra THEO_DOI thay vì PHAN_VE; cách xử lý này phải được xác nhận vì Decision Table không mô tả đầy đủ null của boolean. |
| **Phương án không chọn** | Không chọn None → False/True; không tự điền giá trị mặc định; không duyệt các cách điền giả định để chọn rule chưa thực sự được chứng minh. |
| **Kiểm chứng** | Test bảng chân trị AND/OR/NOT; các trường hợp R02 với T/U; R02 TRUE + R03 UNKNOWN; thiếu từng boolean; thiếu tuổi/HATT/nền; người lớn HATT 89/90 khi thiếu nền. |
| **Truy vết** | REQUIREMENTS §3.1, §4.3–§4.4, §12; FR-05; A-03, A-04, A-07. |

### D05 — Validation nghiêm ngặt

| Thuộc tính | Nội dung |
| :--- | :--- |
| **Trạng thái** | Đã chốt theo REQUIREMENTS v1.1. |
| **Bối cảnh** | Python có một số quan hệ kiểu dễ gây lỗi, ví dụ bool là lớp con của int. Type annotation không thay thế kiểm tra runtime. Input sai không được biến thành dữ kiện hợp lệ bằng ép kiểu. |
| **Quyết định** | Chỉ chấp nhận đúng 9 khóa. Khóa ngoài allowlist → ValueError. Với trường có mặt và khác null: sai kiểu → TypeError; sai miền số → ValueError. Tuổi nhận int/float hữu hạn ≥ 0, loại bool. HATT hiện tại nhận int ≥ 0, loại bool. HATT nền nhận int > 0, loại bool. Không ép kiểu, không tự đặt giới hạn trên. Missing/null xử lý theo Data Dictionary và D04. Validate mọi trường có mặt trước suy luận. |
| **Lý do** | Lỗi dữ liệu được phát hiện nhất quán; không để một rule TRUE che khuất lỗi ở trường khác. |
| **Đánh đổi / giới hạn** | Thông báo lỗi không chứa raw input hoặc dữ liệu nhạy cảm. Không chuyển invalid thành UNKNOWN hay THEO_DOI. |
| **Phương án không chọn** | Không chọn ép chuỗi số thành số; không mặc định bool là số; không bỏ qua trường không liên quan. |
| **Kiểm chứng** | Test chuỗi, bool, float ở trường HATT, số âm, NaN, vô cực, HATT nền bằng 0, khóa lạ và lỗi ở trường không liên quan khi rule khác TRUE. |
| **Truy vết** | REQUIREMENTS §3.1–§3.2; FR-06; A-04, A-07. |

### D06 — Giải thích bằng template tất định

| Thuộc tính | Nội dung |
| :--- | :--- |
| **Trạng thái** | Quyết định triển khai trong giới hạn REQUIREMENTS. |
| **Bối cảnh** | Output phải truy vết được rule/kết quả nhưng không được để lộ dữ liệu lâm sàng thô hoặc đưa ra lời khuyên điều trị. Văn bản sinh tự do có thể gây sai khác giữa các lần chạy. |
| **Quyết định** | Sinh ly_do bằng template cố định theo muc_do, rule_id và tình trạng dữ liệu thiếu. Có thể nêu mã rule, nhóm điều kiện và loại dữ kiện còn thiếu (tuổi/HATT/nền) ở mức khái quát. Không đưa giá trị triệu chứng, số đo hoặc raw patient vào ly_do. THEO_DOI phải được mô tả là chưa đủ dữ kiện kết luận, tuyệt đối không diễn đạt là “an toàn”. |
| **Lý do** | Câu giải thích tất định, dễ kiểm thử và reviewer có thể đối chiếu với rule_id. |
| **Đánh đổi / giới hạn** | Câu văn có thể ít linh hoạt; chỉ bổ sung template khi có nhánh output hoặc tình huống thiếu dữ kiện thực sự cần thiết. |
| **Phương án không chọn** | Không ghép raw input vào câu; không dùng LLM hoặc nội dung tư vấn điều trị. |
| **Kiểm chứng** | Assert template tương ứng với từng kết quả; chạy lặp cùng input; negative test kiểm tra không chứa số đo/raw input, lời khuyên điều trị hoặc từ ngữ khẳng định an toàn. |
| **Truy vết** | REQUIREMENTS §5; FR-07; NFR-06; A-05. |

### D07 — Audit writer, schema và UUID

| Thuộc tính | Nội dung |
| :--- | :--- |
| **Trạng thái** | Schema audit đã chốt theo REQUIREMENTS; JSONL/writer riêng là quyết định triển khai; đường dẫn mặc định và quản lý UUID cần peer review. |
| **Bối cảnh** | Mỗi lần gọi classify() cần audit tối thiểu nhưng không được lưu patient hoặc thông tin định danh. UUID audit không được thêm vào 9 khóa input. |
| **Quyết định** | Dùng writer riêng; mỗi record có đúng bốn trường: Timestamp (ISO 8601 UTC), User_UUID (UUID hợp lệ, synthetic, thuộc phiên thao tác), Action_Type = CLASSIFY và Status = SUCCESS hoặc INVALID_INPUT. Định dạng JSONL một record mỗi dòng là lựa chọn triển khai. UUID được cấp ngoài patient; có thể dùng ContextVar để chia sẻ UUID trong một phiên tường minh và tạo UUID tạm cho call độc lập. Mở/ghi/đóng record trước khi trả kết quả. File audit phải nằm ngoài patient, ngoài repository và không commit. |
| **Lý do** | Writer tập trung cho phép allowlist chính xác; JSONL đơn giản, dễ đọc lại và phù hợp phạm vi bài tập. |
| **Đánh đổi / giới hạn** | JSONL, ContextVar và vị trí mặc định là lựa chọn kỹ thuật chứ không phải yêu cầu nghiệp vụ. V1 chỉ cam kết ghi tuần tự nếu chưa có cơ chế đồng bộ; không mặc định bảo đảm an toàn đa tiến trình. |
| **Phương án không chọn** | Không ghi audit trong từng nhánh rule; không dùng global UUID dùng chung giữa các test; không ghi input, triệu chứng, tuổi, huyết áp, PII hoặc exception payload. |
| **Kiểm chứng** | Đọc lại record để xác nhận đúng bốn trường, Timestamp UTC hợp lệ, UUID hợp lệ; kiểm tra cùng phiên/call độc lập; kiểm tra file nằm ngoài repo và đổi working directory không làm sai đường dẫn cấu hình. |
| **Truy vết** | REQUIREMENTS §6; FR-08; NFR-02; A-06. |

### D08 — Status, fail-closed và thứ tự xử lý lỗi

| Thuộc tính | Nội dung |
| :--- | :--- |
| **Trạng thái** | Đã chốt theo REQUIREMENTS v1.1; hành vi với lỗi nội bộ bất ngờ chưa được quy định đầy đủ. |
| **Bối cảnh** | Nếu chỉ audit thành công, các lần gọi input invalid không được ghi nhận. Ngược lại, ghi lỗi hoặc raw input vào audit có thể làm lộ dữ liệu. Lỗi ghi audit không được phép trả kết quả phân loại thành công. |
| **Quyết định** | Phân loại hoàn tất, kể cả THEO_DOI do thiếu dữ liệu hợp lệ, ghi Status = SUCCESS. Validation lỗi ghi Status = INVALID_INPUT nếu audit ghi được, sau đó raise TypeError/ValueError tương ứng. Nếu audit lỗi (I/O, quyền ghi, đĩa đầy...), raise AuditError là lớp con RuntimeError; giữ lỗi hệ thống gốc trong `__cause__` và không trả kết quả. Nếu validation và audit cùng lỗi, ưu tiên AuditError. Message lỗi không chứa giá trị input. Không thêm Status mới. |
| **Lý do** | Fail-closed ngăn hệ thống trả kết quả thành công khi không tạo được audit record; phân biệt input invalid với lỗi hạ tầng audit. |
| **Đánh đổi / giới hạn** | REQUIREMENTS chưa xác định Status cho lỗi nội bộ bất ngờ xảy ra trước khi có thể hoàn tất validation/audit. Không tự gán SUCCESS hoặc INVALID_INPUT và không thêm status mới khi chưa được thống nhất. |
| **Phương án không chọn** | Không bỏ qua lỗi audit; không retry vô hạn; không ghi exception hoặc payload lâm sàng vào audit. |
| **Kiểm chứng** | Kiểm thử: validation lỗi + audit OK; input hợp lệ + audit lỗi; cả validation và audit cùng lỗi; lỗi mở/ghi/đóng file; xác nhận AuditError.__cause__ và message không lộ input. |
| **Truy vết** | REQUIREMENTS §3.2, §6; FR-08; NFR-03; A-06. |

### D09 — Chiến lược kiểm thử theo hành vi và biên

| Thuộc tính | Nội dung |
| :--- | :--- |
| **Trạng thái** | Quyết định triển khai; nghĩa vụ test/CI được REQUIREMENTS quy định. |
| **Bối cảnh** | Test stub chỉ xác nhận starter còn chạy được, không chứng minh rule đúng. Các điều kiện gần giống nhau có thể sai do ngoặc, AND/OR, dấu so sánh hoặc biên tuổi. |
| **Quyết định** | Tổ chức test theo nhóm: normal từng rule; boundary tuổi 1/11/18, HATT sát ngưỡng, giảm đúng 30% và lớn hơn 30%; missing/null; invalid/type/domain/extra key; overlap; tuổi lẻ; output/reason; audit/privacy; integration classify(). Mỗi test audit dùng đường dẫn tạm riêng (tmp_path) và fixture reset context kể cả khi exception. Kỳ vọng phải suy ra từ REQUIREMENTS/Decision Table, không sao chép logic từ implementation. Không phụ thuộc ID fixture công khai. |
| **Lý do** | Bắt lỗi sai ngoặc/dấu và bảo đảm test độc lập thứ tự chạy; tạo bằng chứng trực tiếp cho A-01 đến A-09. |
| **Đánh đổi / giới hạn** | Bộ test tốn công xây dựng và bảo trì; không dùng coverage dòng đơn lẻ làm bằng chứng duy nhất cho tính đúng đắn. |
| **Phương án không chọn** | Không chỉ test ca điển hình; không chỉ dựa vào public fixture hoặc line coverage. |
| **Kiểm chứng** | Chạy `pytest -q` từ clean checkout; CI chạy trên mọi Pull Request; lưu URL/lượt chạy và kết quả thực tế. Chỉ đánh dấu đạt khi có bằng chứng. |
| **Truy vết** | REQUIREMENTS NFR-05; A-01–A-09. |

### D10 — Benchmark toàn luồng

| Thuộc tính | Nội dung |
| :--- | :--- |
| **Trạng thái** | Yêu cầu đo đã chốt theo REQUIREMENTS; công thức và cách tổ chức đo là quyết định triển khai. |
| **Bối cảnh** | Đo riêng helper rule sẽ bỏ qua validation, tạo reason và audit I/O, do đó không đại diện cho public path mà người gọi thực sự sử dụng. |
| **Quyết định** | Dùng `time.perf_counter_ns()`. Thực hiện 100 lần warm-up không tính vào mẫu; đo tối thiểu 1.000 lần. Sắp xếp thời gian tăng dần và dùng nearest-rank: phần tử thứ $\lceil p \times N \rceil$, đánh số từ 1; báo p50 và p95. Phép đo chính là toàn bộ classify() với audit I/O thật, không mock writer. Có thể báo thêm thời gian logic thuần nhưng phải ghi rõ là số liệu phụ. Công bố CPU/máy, OS, Python, số warm-up, số mẫu, dữ liệu synthetic và cấu hình I/O. Mục tiêu p95 < 100 ms. |
| **Lý do** | Số liệu phản ánh đường gọi thực tế và có thể tái lập khi môi trường đo được công bố. |
| **Đánh đổi / giới hạn** | Kết quả phụ thuộc máy và I/O; nearest-rank có bước nhảy theo cỡ mẫu. Không tuyên bố đạt trước khi chạy benchmark thật. |
| **Phương án không chọn** | Không chỉ báo trung bình; không dùng số liệu logic thuần thay cho benchmark toàn luồng. |
| **Kiểm chứng** | Kiểm tra nearest-rank bằng tập mẫu nhỏ tính tay; chạy benchmark ở mốc phù hợp, lưu script, số liệu và thông tin môi trường để đối chiếu A-10. |
| **Truy vết** | REQUIREMENTS NFR-01; A-10. |

---

## 5. Các vấn đề cần xác nhận (OPEN)

Các nội dung dưới đây không được Decision Table quy định đầy đủ hoặc cần peer review về lựa chọn triển khai. Cho đến khi có xác nhận, nhóm phải giữ nguyên giả định hiện tại trong REQUIREMENTS v1.1 và không mô tả chúng như quy định chính thức của đề.

| ID | Nội dung cần xác nhận | Giả định/ứng xử hiện tại | Người xác nhận |
| :--- | :--- | :--- | :--- |
| **OPEN-01** | Khi nhiều rule Tầng 2 cùng TRUE, rule_id được chọn theo thứ tự nào? | R01-PV > R02-PV > R03-PV theo REQUIREMENTS §4.4; cần TA xác nhận. | TA/giảng viên |
| **OPEN-02** | Missing/null của sáu trường boolean được xử lý như thế nào? | UNKNOWN theo logic ba trạng thái; không tự quy về False/True; cần TA xác nhận. | TA/giảng viên |
| **OPEN-03** | Tuổi thiếu khi đã có rule Tầng 2 TRUE; HATT/nền thiếu được xử lý ra sao? | Tuổi thiếu → THEO_DOI; thiếu dữ kiện tụt HATT → PHAN_VE nếu đã có rule Tầng 2 TRUE; người lớn HATT < 90 vẫn có thể R-SOC. | TA/giảng viên |
| **OPEN-04** | Miền số có giới hạn trên không; HATT = 0 và HATT nền = 0? | HATT hiện tại ≥ 0; nền > 0; tuổi hữu hạn ≥ 0; không tự đặt trần trên theo REQUIREMENTS. | Nhóm; hỏi TA nếu cần |
| **OPEN-05** | Đường dẫn mặc định của file audit và cơ chế cấu hình/override? | File nằm ngoài patient và repository, không commit; chọn thư mục mặc định và cách override cần peer review. | Nhóm |
| **OPEN-06** | UUID được chia sẻ trong phiên thao tác như thế nào? | UUID synthetic ngoài patient; đề nghị ContextVar cho phiên tường minh và UUID tạm cho call độc lập. | Nhóm |
| **OPEN-07** | Lỗi nội bộ bất ngờ trước khi audit hoàn tất được xử lý thế nào? | Không tự gán SUCCESS/INVALID_INPUT và không thêm status; cần thống nhất policy không trái schema audit. | Nhóm; hỏi TA nếu ảnh hưởng yêu cầu |

---

## 6. Ma trận truy vết quyết định

| Quyết định | Yêu cầu liên quan | Acceptance criteria | Bằng chứng dự kiến |
| :--- | :--- | :--- | :--- |
| **D01** | FR-01–FR-07 | A-01–A-05 | Review contract; test từng rule và biên |
| **D02** | FR-01; NFR-04 | A-01, A-02 | Review cấu trúc; test helper và public function |
| **D03** | FR-04 | A-03, A-07 | Test overlap các cặp và cả ba rule |
| **D04** | FR-05 | A-03, A-04, A-07 | Truth table; test missing/null và R02 T/U |
| **D05** | FR-06 | A-04, A-07 | Test type/domain/extra key; kiểm tra message |
| **D06** | FR-07; NFR-06 | A-05 | Assert template, tính tất định, negative privacy test |
| **D07** | FR-08; NFR-02 | A-06 | Đọc record; schema 4 trường; UUID/UTC; kiểm tra file |
| **D08** | FR-08; NFR-03 | A-06 | Test ba nhánh lỗi và AuditError chaining |
| **D09** | NFR-05 | A-01–A-09 | pytest -q clean checkout; CI PR có URL |
| **D10** | NFR-01 | A-10 | Script benchmark; p50/p95; thông tin môi trường |

---

## 7. Rủi ro chính và biện pháp giảm thiểu

| Rủi ro | Biện pháp |
| :--- | :--- |
| **Giả định missing/null hoặc priority khác kỳ vọng TA** | Đặt policy tập trung; hỏi TA sớm; cập nhật ADR và test khi có clarification. |
| **Sai ngoặc, AND/OR hoặc dấu < / ≤ tại biên** | Đối chiếu Decision Table; test boundary cho từng nhóm tuổi, HATT và giảm đúng 30%. |
| **Validation bỏ qua trường invalid vì rule khác đã TRUE** | Validate toàn bộ input trước suy luận; test lỗi ở trường không liên quan. |
| **Audit hoặc ly_do làm lộ dữ liệu** | Allowlist đúng bốn trường audit; template cố định; negative test; chỉ dùng synthetic. |
| **Audit I/O làm p95 vượt 100 ms** | Đo toàn luồng sớm; công bố môi trường; chỉ tối ưu sau khi có số liệu. |
| **Nhầm hoàn thành tài liệu với nghiệm thu** | Giữ trạng thái AC là chưa đạt cho tới khi có test, CI và benchmark thật. |
| **Lựa chọn triển khai bị hiểu nhầm là yêu cầu đề** | Gắn trạng thái rõ ràng; mọi thay đổi nghiệp vụ phải có nguồn chính thức. |

---

## 8. Quy trình cập nhật quyết định

1. Mỗi quyết định mới hoặc thay đổi phải có ID, bối cảnh, lựa chọn, lý do, đánh đổi/rủi ro, cách kiểm chứng, trạng thái và liên kết tới FR/NFR/AC liên quan.
2. Chỉ chuyển OPEN thành DECIDED sau khi nhóm thống nhất; nếu liên quan nghiệp vụ chưa được đặc tả, cần clarification/erratum chính thức của TA.
3. Khi quyết định thay đổi, cập nhật đồng bộ DECISIONS, REQUIREMENTS (nếu contract thay đổi), test và bằng chứng liên quan.
4. Không ghi PASSED/Đạt cho test, CI hoặc benchmark nếu chưa có kết quả thực tế có thể kiểm tra.
5. Ghi ngày cập nhật, người thực hiện và người xác nhận trong lịch sử thay đổi của repository.

---

## 9. Nguồn tham chiếu và phạm vi căn cứ

- `REQUIREMENTS_fixed (1).docx`, phiên bản v1.1 — tài liệu yêu cầu chuẩn của Nhóm 26, dùng làm căn cứ đối chiếu trực tiếp cho bản Decisions này.
- `docs/decision-table.md` trong starter repository, tag `bkt-2026-v1` — nguồn đặc tả nghiệp vụ được REQUIREMENTS chỉ định.
- Đề kiểm tra Track A — dùng trong phạm vi các nội dung được phản ánh trong REQUIREMENTS và các clarification/erratum chính thức của TA.
- `DECISIONS_claude.docx` và `DECISIONS_Track_A_GPT.docx` — chỉ dùng làm nguồn tham khảo về cấu trúc ADR, phân tích lựa chọn và quản lý OPEN; không kế thừa metadata sai hoặc quyết định mâu thuẫn với REQUIREMENTS.

---

## 10. Lịch sử phiên bản

| Phiên bản | Nội dung thay đổi | Trạng thái |
| :--- | :--- | :--- |
| **v1.1** | Hợp nhất hai bản Decisions theo REQUIREMENTS v1.1; chuẩn hóa metadata Nhóm 26; thống nhất 10 ADR; tách yêu cầu bắt buộc, lựa chọn triển khai và nội dung OPEN; bổ sung truy vết, rủi ro và quy trình cập nhật. | Bản hợp nhất — chờ peer review/TA xác nhận các mục OPEN. |