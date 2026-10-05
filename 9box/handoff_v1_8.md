### HANDOFF — 9-Box Talent Dashboard (Coteccons) · v1.8

Thay thế bản _handoff v1.7.3_. Tài liệu mô tả trạng thái hiện tại của `9box/index.html` sau khi **nhập số liệu SEP 2026** (v1.8), cùng các thay đổi v1.7.2 / v1.7.3 trước đó.
File hiện hành: `9box/index.html` · **Không còn mật khẩu** (gỡ ở v1.7.3) · Kỳ dữ liệu: **SEP 2026** (biến `DATA_PERIOD`).
Nguồn số liệu: `FY26 - 9Box - Masterfile HRBP 28.08 update.xlsx`, sheet **Masterfile** (cột BU, Cấp bậc, Performance, Potential 26, 9Box).

#### 0. TL;DR cho phiên chat kế tiếp
- **v1.8 (29/09/2026): nhập số liệu SEP 2026, phạm vi mở rộng từ khối kỹ sư ra toàn công ty.**
  - 3.437 người trong phạm vi / **3.365 đã đánh giá (97,9%)**, trên **7 khối**: BU1–BU6 + **Back Office** (khối mới). Bản APR 2026 là 1.999 kỹ sư / 1.906 đã đánh giá, 6 BU.
  - Phân bổ: A 23,7% · B 68,9% · C 7,4% (so với ideal 20 / 65 / 15). Khớp sheet `Summary 9Box`.
  - **Danh sách nhân viên C1/C2/C3 đã nhập** (192 / 38 / 20 = 250 người): Họ tên, Chức danh, Dự án/Phòng ban, BU, Level. Bấm "View N employees in Cx" ở Box detail.
  - Giao diện: "engineer(s)" → "employee(s)"; bỏ badge "⚠ Possible rating inflation signal"; card-sub đổi thành "Line manager evaluation — HRBP calibrated"; nguồn headcount "(HRBP masterfile, 28 Aug)"; ô chia theo BU trong Box detail chuyển sang 7 cột.
  - Có **11 người lệch** giữa cột 9Box và tổ hợp Performance × Potential 26. Dashboard dùng **cột 9Box** theo chỉ đạo user; danh sách ở mục 3 để HRBP rà lại.
- **v1.8.2 (05/10/2026): cập nhật BU1** từ file `FY26 - 9Box - Masterfile HRBP - Triều last update.xlsx` (sheet Masterfile). Các khối khác giữ nguyên theo file 28.08.
  - BU1: 390 → **436/437** đã đánh giá (thêm 47 người, gỡ 1 người là Trần Anh Hòa EE26002786, vì Performance trống). BU1: A 20,2% · B 72,2% · C 7,6%.
  - Toàn công ty: 3.365 → **3.411/3.437** (99,2%); A 23,5% · B 68,8% · C 7,7%. Danh sách ô C: 202 / 39 / 21 = 262 người.
  - Cả 10 trường hợp lệch ở BU1 đã được HRBP sửa. **Chỉ còn 1 trường hợp lệch**: Phạm Thanh Sang (EE25001670, Back Office, L6), High × High nhưng file ghi A2.
  - Cách ghép: lấy toàn bộ dòng BU1 từ file Triều, các dòng còn lại lấy từ file 28.08. Nhãn nguồn headcount: "HRBP masterfile 28 Aug; BU1 updated". Nhãn nút Period SEP: n=3,411 (sửa ở cả `index.html` và `apr-2026.html`).
- **v1.8.1 (30/09/2026): so sánh 2 kỳ.** Khôi phục bản APR 2026 thành `9box/apr-2026.html` (lấy từ commit `bb4ac76`, tức bản v1.7.3 đã gỡ mật khẩu và vẫn giữ số liệu APR). Cả 2 trang có nút **Period** ở góc phải topbar: kỳ đang xem tô teal, bấm kỳ còn lại sẽ mở ở **tab mới** để đặt cạnh nhau. Tiêu đề tab trình duyệt ghi rõ kỳ (`9-Box · APR 2026` / `9-Box · SEP 2026`).
  - ⚠️ Hai kỳ **khác phạm vi**: APR là 1.906 kỹ sư / 6 BU, SEP là 3.365 nhân sự toàn công ty / 7 khối. So sánh tỷ lệ % theo zone thì được, còn so số tuyệt đối thì không tương đương. Nhãn nút Period có ghi phạm vi và n.
  - `apr-2026.html` là **bản đóng băng**, không sửa tiếp. Kỳ sau: copy `index.html` hiện tại thành `sep-2026.html`, nhập dữ liệu mới vào `index.html`, rồi thêm nút kỳ mới vào `.period-switch` của cả 3 file.
- **v1.7.3:** nút ⓘ Rating Definitions ở mọi tab + nút Back; dọn CSS legend cũ; chốt `.page-narrow` 960px; `<title>` mới; **gỡ mật khẩu**.
- **v1.7.2:** định nghĩa Potential mới (Aspiration / Engagement / Ability, không bù trừ).
- Test: `node --check` sạch, div cân bằng (332/332), Chromium headless không lỗi JS; đã kiểm tra 5 tab, 7 khối, modal danh sách nhân viên.

#### 1. Phạm vi của file này
Dashboard phục vụ **DATA** — đi từ tổng quan xuống chi tiết, insight nhẹ ở mô tả từng ô. Thông điệp/khuyến nghị/độ tin cậy dữ liệu thuộc **slide trình BLĐ**, không đưa vào HTML.
Người xem chính: Ban lãnh đạo (Chủ tịch là người nước ngoài) → **toàn bộ giao diện tiếng Anh**.
Từ v1.8, phạm vi là **toàn bộ nhân sự** (không riêng kỹ sư).

⚠️ **Bảo mật:** trang không còn mật khẩu nhưng đã chứa **họ tên 250 nhân viên vùng C**. Ai có link đều xem được. Nên bật Vercel Deployment Protection cho project `ctd-9box`, hoặc bật lại mật khẩu, trước khi chia sẻ link rộng.

#### 2. Cách map dữ liệu (v1.8)
| Khối trên dashboard | Giá trị cột `BU` trong Masterfile |
|---|---|
| BU1, BU2, BU4, BU5, BU6 | `BUSINESS UNIT n|…` |
| BU3 | `UNICONS|…` (622 người) |
| Back Office | `BACK OFFICE`, `FINANCE`, `SUPPLY CHAIN`, `CHAIRMAN OF EXCOM`, `CHAIRMAN OFFICE`, `BOARD OF DIRECTORS` (185 người) |

- **Total** = mọi dòng có mã NV; **Completed** = dòng có giá trị ở cột 9Box (giống định nghĩa sheet Summary).
- **Level** lấy từ cột "Cấp bậc" (L1–L8).
- **Dự án/Phòng ban** = cột "Bộ phận", đã bỏ phần "(tên quản lý)" ở cuối. Chữ "(On Leave)" trong họ tên được giữ nguyên như trong file.
- Script dùng để sinh dữ liệu không lưu trong repo. Kỳ sau chỉ cần làm lại theo đúng mapping này và thay 3 khối `BU_META`, `BU_LEVEL`, `EMPLOYEE_DATA`.

#### 3. 11 trường hợp cột 9Box lệch với Performance × Potential 26 — CẦN HRBP RÀ
Dashboard đang tính theo cột **9Box trong file**.

| # | MSNV | Họ tên | Khối | Level | Performance | Potential 26 | 9Box trong file | Theo công thức |
|---|---|---|---|---|---|---|---|---|
| 1 | EE25001920 | Lê Minh Đức | BU1 | L1 | Medium | Low | **C3** | C1 |
| 2 | EE25002237 | Kha Thành Đạt | BU1 | L1 | Medium | Low | **C3** | C1 |
| 3 | EE23001234 | Nguyễn Văn Khoa | BU1 | L4 | High | Medium | **B2** | A3 |
| 4 | EE26003269 | Nguyễn Quốc Anh | BU1 | L2 | Medium | Low | **C3** | C1 |
| 5 | EE26003274 | Đặng Tuấn Cường | BU1 | L2 | Medium | Low | **C3** | C1 |
| 6 | EE26003647 | Phạm Quang Sáng | BU1 | L2 | Low | Medium | **B2** | C2 |
| 7 | EE26003650 | Đặng Văn Lượng | BU1 | L2 | Low | Medium | **B2** | C2 |
| 8 | EE26003645 | Phan Đại Dương | BU1 | L2 | Low | Medium | **B2** | C2 |
| 9 | EE26003648 | Nguyễn Minh Tâm | BU1 | L4 | Low | Medium | **B2** | C2 |
| 10 | EE25001670 | Phạm Thanh Sang | Back Office | L6 | High | High | **A2** | A1 |
| 11 | EE25001854 | Lý Ngọc Nghĩa | BU1 | L4 | High | Medium | **B2** | A3 |

Nếu HRBP sửa lại, chỉ cần gửi lại file và nhập lại dữ liệu; code không cần đổi.

#### 4. Bảng điều khiển hiển thị (sửa ở đây, không sửa chỗ khác)
```
const DATA_PERIOD='SEP 2026';   // đổi mỗi kỳ; topbar tự đọc
const SMALL_N=30;               // nhóm nhỏ hơn số này hiện count thay vì %
const DEFAULT_BOX='A1';         // ô mở sẵn trong Box detail
```
| Hằng số | Ý nghĩa |
|---|---|
| `CA/CB/CC, TA/TB/TC` | Màu fill / màu chữ theo zone A/B/C |
| `BOX_DEF` | Map mỗi box (A1…C3) → zone, mô tả, action |
| `BU_META` | Total / Completed từng khối (7 khối) |
| `BU_LEVEL` | Số liệu gốc Khối × Level × Box |
| `EMPLOYEE_DATA` | Danh sách nhân viên C1/C2/C3 |
| `EMP_FIELDS` | Cột hiển thị trong modal (chỉ hiện field có dữ liệu) |
| `TARGET` | Model ideal — 20% A / 65% B / 15% C |

Text cứng liên quan đến kỳ dữ liệu: nguồn headcount `'headcount in scope (HRBP masterfile, 28 Aug)'` trong `renderKPIs()`; card-sub `"Line manager evaluation — HRBP calibrated"` ở Overview.

#### 5. Ghi chú kỹ thuật
- Logo SVG là vector path thật trích từ `2026-Logo_Coteccons.pdf` (bản trắng + N teal); đổi màu N bằng thuộc tính `fill` của path cuối trong SVG.
- Nút ⓘ: `openDefs()` / `closeDefs()` + biến `defReturn`; `showTab()` ẩn nút Back khi rời tab legend.
- Font Lexend Deca + palette Coteccons: navy `#16315E`, teal `#5FD1C1`, xanh `#0047BA`, đỏ `#B86054`, xanh lá `#51AC70`.
- File 1 trang, không phụ thuộc, chạy offline, deploy thẳng SharePoint / GitHub Pages / Vercel (project `ctd-9box`).
- Chữ "Target" ở tab Gap Analysis (mô hình 20/65/15) khác nghĩa với "Total" ở bảng Completion — giữ nguyên.
- Định nghĩa Potential (v1.7.2): High = cả 3 tiêu chí High; Medium = cả 3 có ít nhất mức cơ bản; Low = ít nhất 1 tiêu chí vắng rõ.

#### 6. Còn tồn
| Việc | Ghi chú |
|---|---|
| HRBP rà 11 trường hợp lệch ở mục 3 | Nhập lại dữ liệu sau khi có file sửa |
| Bảo vệ truy cập (Vercel Protection hoặc mật khẩu) | Vì trang đã có tên nhân viên vùng C |

Phần in (`@media print`, nút Print) đã **loại khỏi phạm vi** theo yêu cầu user (29/09/2026).

#### 7. Checklist
- [x] v1.7.2: Định nghĩa Potential mới
- [x] v1.7.3: Nút ⓘ + Back, dọn CSS, chốt 960px, `<title>` mới, gỡ mật khẩu
- [x] v1.8: Nhập số liệu SEP 2026 — 7 khối, 3.437 / 3.365
- [x] v1.8: Nhập danh sách nhân viên C1/C2/C3 (250 người)
- [x] v1.8: engineer → employee, bỏ badge inflation, sửa card-sub + nguồn headcount
- [x] Test: `node --check` sạch, div 332/332, Chromium headless không lỗi JS
- [x] v1.8.1: Trang APR 2026 riêng + nút Period mở tab mới để so sánh
- [x] v1.8.2: Cập nhật BU1 (file Triều last update); 10/11 trường hợp lệch đã được sửa
- [ ] HRBP rà trường hợp lệch còn lại (Phạm Thanh Sang, Back Office) và Trần Anh Hòa (BU1, thiếu Performance)

_Cập nhật: 29/09/2026 · Coteccons Academy (L&OD / CTA) · v1.7.3 → v1.8 (đã build)_
