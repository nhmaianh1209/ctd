### APPROACH — 9-Box "A & C Focus" view (v1.9) · ĐÃ BUILD (preview, chưa merge)

Nhánh: `claude/9box-ac-focus` (tách từ `main` @ `ed40572`, dashboard v1.8.2, SEP 2026).

#### 1. Yêu cầu từ business
Chỉ tập trung vào **nhóm A và C** ở **level 4 trở lên**. Mỗi ô A1, A2, A3, C1, C2, C3 có một biểu đồ tròn (pie) riêng:
- Các lát cắt là **L4, L5, L6, L7, L8**, mỗi level một màu nổi bật. **L1–L3 gộp thành 1 lát màu xám**, không nổi bật.
- Mỗi lát hiển thị **số lượng và tỉ lệ**.
- **Kích thước pie tỉ lệ với số người** trong ô.
- Mỗi ô có ghi chú action:

| Ô | Action (giao diện tiếng Anh) |
|---|---|
| A1 | **Ready now** — promotable at any point within 12 months |
| A2, A3 | **Ready later** — next role in 2–3 years |
| C1, C2 | **Improvement plan required** |
| C3 | **PIP or manage out** |

#### 2. Số liệu hiện tại (SEP 2026, 3.411 người đã đánh giá)
| Ô | Tổng | L1–L3 | L4 | L5 | L6 | L7 | L8 | Tỉ lệ L4+ |
|---|---|---|---|---|---|---|---|---|
| A1 | 168 | 43 | 66 | 37 | 19 | 3 | 0 | 74% |
| A2 | 280 | 138 | 85 | 30 | 23 | 4 | 0 | 51% |
| A3 | 353 | 89 | 135 | 87 | 38 | 3 | 1 | 75% |
| C1 | 202 | 159 | 29 | 9 | 5 | 0 | 0 | 21% |
| C2 | 39 | 30 | 4 | 2 | 1 | 1 | 1 | 23% |
| C3 | 21 | 16 | 3 | 0 | 1 | 1 | 0 | 24% |

Tổng người đã đánh giá theo level: L1 371 · L2 949 · L3 919 · L4 698 · L5 281 · L6 162 · L7 28 · L8 3.

Nhận xét:
- Nhóm A tập trung ở level cao: 74–75% của A1 và A3 nằm ở L4+.
- Nhóm C chủ yếu là level thấp: chỉ khoảng 1/5 ở L4+ (C1 có 43 người, C2 có 9, C3 có 5).
- Ô lớn nhất (A3, 353 người) gấp khoảng 17 lần ô nhỏ nhất (C3, 21 người). Nếu diện tích pie tỉ lệ với số người, bán kính pie C3 chỉ bằng khoảng 1/4 pie A3.
- Lát L7/L8 thường chỉ 0–4 người, quá nhỏ để ghi nhãn trực tiếp trên pie.

#### 3. Approach đề xuất
1. **Vị trí:** thêm **tab thứ 6 "A & C Focus"** vào `index.html`, không làm trang riêng. Tab này dùng chung dữ liệu `BU_LEVEL` và `EMPLOYEE_DATA`, nên mỗi lần cập nhật số liệu thì tab tự đúng theo, không phải nhập 2 nơi. Trang `apr-2026.html` giữ nguyên (đóng băng).
2. **Bố cục:** 2 hàng.
   - Hàng A: A1 · A2 · A3, kèm băng action màu xanh lá.
   - Hàng C: C1 · C2 · C3, kèm băng action màu đỏ.
   - Mỗi thẻ gồm: mã ô + tên, tổng số người và số người L4+, pie, bảng chú giải theo level (count · % của ô), và dòng action.
3. **Pie:**
   - Vẽ bằng SVG inline, không dùng thư viện ngoài, để file vẫn chạy offline.
   - **Diện tích tỉ lệ với số người**, dùng một thang chung cho cả 6 pie (bán kính ∝ √n), để so sánh giữa các ô là trung thực.
   - L4→L8 dùng một dải màu đậm dần theo level. L1–L3 dùng màu xám nhạt.
   - Nhãn % chỉ hiện trên lát đủ lớn. Lát nhỏ (L7/L8) xem qua bảng chú giải và tooltip khi rê chuột.
   - Tooltip có thêm "% của toàn bộ level đó". Ví dụ: A1-L5 có 37/281 người, tức 13% số người L5.
4. **Bộ lọc BU (tùy chọn):** Overall / BU1…Back Office, giống tab By BU.
5. **Danh sách người:**
   - Ô C đã có danh sách tên, nên có thể thêm nút "View L4+ employees".
   - Ô A hiện **chưa có tên** trong dữ liệu. Muốn có danh sách promote cho A1 L4+ thì phải nhập thêm tên (cân nhắc bảo mật).
6. **Kiểm tra:** `node --check`, chụp ảnh headless Chromium, đối chiếu tổng từng pie với số ô ở tab Overview.

#### 4. Câu hỏi cần user chốt
1. Làm thành tab trong dashboard hiện tại (đề xuất), hay trang riêng?
2. Kích thước pie: một thang chung cho cả 6 (đề xuất, trung thực), hay thang riêng cho nhóm A và nhóm C (pie C to hơn, dễ đọc hơn nhưng không so được với A)?
3. Có cần bộ lọc theo BU không?
4. Có nhập danh sách tên cho A1/A2/A3 ở L4+ (khoảng 531 người) để làm danh sách promote không?
5. % hiển thị chính là % trong ô (đề xuất), hay % trên tổng số người của level?

#### 5. Quyết định của user (08/10/2026) và cách đã build
- **Trang riêng** `9box/focus.html`, không làm tab. Dashboard chính có nút **"A & C Focus →"** trên thanh tab; trang Focus có nút **"← Full 9-Box dashboard"** để quay lại.
- **Thang pie chung** cho cả 6 ô (bán kính ∝ √n theo ô lớn nhất trong view đang xem).
- **Có bộ lọc BU**, mặc định là **Company-wide**.
- **Chưa làm danh sách tên nhóm A.** Trang Focus không chứa tên người nào.
- % chính là **% trong ô**. Tooltip khi rê chuột có thêm % trên tổng số người cùng level.
- Màu level L4→L8 là ramp xanh dương ordinal `#86b6ef → #5598e7 → #2a78d6 → #1c5cab → #104281`, đã qua validator dataviz (`--ordinal`, light). L1–L3 dùng xám `#D9DFE8`.
- **Dữ liệu:** `focus.html` nhúng một bản sao `BU_LEVEL` và `BU_META` lấy từ `index.html`. Sau mỗi lần cập nhật số liệu `index.html`, **chạy lại** `python3 9box/tools/build_focus.py` để sinh lại `focus.html`.
- Test: `node --check` sạch, Chromium headless không lỗi JS; tổng từng ô khớp tab Overview; không tràn ngang ở 390px.
