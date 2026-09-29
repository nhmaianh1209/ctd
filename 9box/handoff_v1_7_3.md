### HANDOFF — 9-Box Talent Dashboard (Coteccons) · v1.7.3

Thay thế bản _handoff v1.7.1_. Tài liệu mô tả trạng thái hiện tại của `9box/index.html`, **những gì đã đổi ở v1.7.2 và v1.7.3**, và việc chuẩn bị cho **v1.8 (dữ liệu SEP 2026)**.
File hiện hành: `9box/index.html` · **Không còn mật khẩu** (đã gỡ ở v1.7.3) · Kỳ dữ liệu đang hiển thị: **APR 2026** (biến `DATA_PERIOD`) — sẽ đổi sang **SEP 2026** ở v1.8.

#### 0. TL;DR cho phiên chat kế tiếp
- **v1.7.2 (26/08/2026):** viết lại định nghĩa **Potential** ở tab Rating Definitions — 3 tiêu chí **Aspiration / Engagement / Ability** (có dòng mô tả thành phần), ngang quyền và **không bù trừ**; bỏ cách tính theo số tiêu chí đạt (3/3, 1–2/3, 0/3).
- **v1.7.3 (29/09/2026):** dọn hết backlog còn tồn (trừ phần in — user **không cần**, đã gạch khỏi backlog):
  1. Nút **ⓘ How ratings are defined** ở 4 tab dữ liệu → mở Rating Definitions, có nút **← Back to <tab>** để quay lại đúng tab đang xem.
  2. Dọn CSS legend cũ không còn dùng (10 dòng: `.legend-grid`, `.legend-col*`, `.legend-row/dot/key/desc`, `.nb-ref*`).
  3. `.page-narrow` **chốt giữ 960px** sau khi xem ảnh chụp ở 1440px và 1920px (cân, dễ đọc); cột "Case B" trong bảng Performance được cố định `width:200px` để tiêu đề không bị xuống 3 dòng.
  4. `<title>` bỏ "Engineer Workforce" → `9-Box Talent Dashboard — Coteccons` (đồng bộ với header từ v1.7.1).
  5. **Gỡ mật khẩu đầu vào** — xoá toàn bộ khối `<script>` prompt mật khẩu ở đầu `<body>`; trang mở thẳng vào dashboard.
- Test: `node --check` sạch, div cân bằng (333/333), chạy Chromium headless không lỗi JS; đã test luồng ⓘ → Back.
- **Bước kế tiếp:** user sẽ gửi số liệu 9-box **tháng 9/2026** → build v1.8 theo checklist mục 3.

#### 1. Phạm vi của file này (không đổi)
Dashboard phục vụ **DATA** — đi từ tổng quan xuống chi tiết, insight nhẹ ở mô tả từng ô. Thông điệp/khuyến nghị/độ tin cậy dữ liệu thuộc **slide trình BLĐ**, không đưa vào HTML.
Người xem chính: Ban lãnh đạo (Chủ tịch là người nước ngoài) → **toàn bộ giao diện tiếng Anh**.

Cấu trúc 5 tab: **Overview · By Business Unit · By Level · Gap Analysis · Rating Definitions**. Overview/BU/Level rộng 1440px; Gap & Definitions dùng `.page-narrow` 960px.

#### 2. Chi tiết thay đổi

##### 2.1 — v1.7.2 · Định nghĩa Potential
| Level | Điều kiện |
|---|---|
| High | Aspiration, Engagement và Ability đều High, ổn định |
| Medium | Cả 3 đều có ít nhất ở mức cơ bản (không tiêu chí nào vắng rõ), nhưng không đồng thời High, hoặc dao động giữa các kỳ |
| Low | Ít nhất 1 tiêu chí vắng rõ, bất kể 2 tiêu chí kia mạnh thế nào |

Thành phần: Aspiration = Advancement · Learning agility & resilience; Engagement = Commitment & effort · Intent to stay; Ability = Business competence · Domain expertise · Communication · Leadership · Innovation & effort. CSS mới `.def-item-sub`.

##### 2.2 — v1.7.3 · Nút ⓘ Rating Definitions
- Link `<a class="def-link">` nằm cuối dòng `.page-sub` của 4 tab dữ liệu (overview, bu, level, gap).
- JS: `openDefs(e)` ghi nhớ tab + vị trí cuộn hiện tại vào `defReturn`, chuyển sang tab legend, hiện `#def-back` với nhãn "← Back to <tên tab>". `closeDefs(e)` quay lại đúng tab (state BU/Level đang chọn giữ nguyên vì là biến toàn cục).
- Trong `showTab()`: khi chuyển sang tab khác legend, `defReturn` được xoá và nút Back ẩn đi → bấm tab "Rating Definitions" trực tiếp thì không hiện Back.
- CSS: `.def-link`, `.def-back` (màu xanh `#0047BA`, gạch chân khi hover).

##### 2.3 — v1.7.3 · Việc nhỏ khác
| Việc | Vị trí |
|---|---|
| Xoá CSS legend cũ | khối CSS sau `.cmp-table` |
| Cột Case B `width:200px` | `<thead>` bảng Performance, tab-legend |
| `<title>` mới | dòng 6 |

#### 3. v1.8 — Cập nhật dữ liệu SEP 2026 (CHỜ SỐ LIỆU)
Khi user gửi file số liệu tháng 9/2026, cần sửa **chỉ ở các chỗ sau**:

| # | Chỗ sửa | Nội dung |
|---|---|---|
| 1 | `const DATA_PERIOD` | `'APR 2026'` → `'SEP 2026'` (topbar tự đọc) |
| 2 | `const BU_META` | `target` (headcount trong phạm vi) + `completed` từng BU1–BU6 |
| 3 | `const BU_LEVEL` | số người theo BU × Level (L1–L8) × box (A1…C3) — mọi con số khác (BUDATA, GRAND_TOTAL, TOTAL_TARGET, heatmap, gap) tự tính từ đây |
| 4 | `const EMPLOYEE_DATA` | danh sách nhân viên C1/C2/C3 (hiện đang trống) nếu file có sheet chi tiết; field theo `EMP_FIELDS` (code, name, bu, level, position, fy25, fy26, potential, manager, note) |
| 5 | Text cứng cần rà | `'headcount in scope (DS FY25)'` trong `renderKPIs()` (nguồn headcount có đổi không?); card-sub `"Line manager evaluation — First deployment"` + badge `"⚠ Possible rating inflation signal"` ở Overview (còn đúng cho kỳ 2 không?) |
| 6 | Nếu có BU/Level mới | cập nhật `BU_META` / `LEVEL_NAMES` |

Sau khi nhập: **kiểm tra tổng `BU_LEVEL` từng BU = `completed` trong `BU_META`** (kỳ APR 2026 đã khớp: 578/843/397/14/30/44 = 1.906 / 1.999). `TARGET` (20/65/15) giữ nguyên trừ khi có chỉ đạo mới.

#### 4. Bảng điều khiển hiển thị (sửa ở đây, không sửa chỗ khác) — không đổi
```
const DATA_PERIOD='APR 2026';   // đổi mỗi kỳ; topbar tự đọc
const SMALL_N=30;               // nhóm nhỏ hơn số này hiện count thay vì %
const DEFAULT_BOX='A1';         // ô mở sẵn trong Box detail
```
| Hằng số | Ý nghĩa |
|---|---|
| `CA/CB/CC, TA/TB/TC` | Màu fill / màu chữ theo zone A/B/C |
| `BOX_DEF` | Map mỗi box (A1…C3) → zone, mô tả, action |
| `BU_META` | Target / Completed từng BU |
| `BU_LEVEL` | Số liệu gốc BU × Level × Box |
| `TARGET` | Model ideal — 20% A / 65% B / 15% C |

#### 5. Ghi chú kỹ thuật (kế thừa v1.7)
- Logo SVG là vector path thật trích từ `2026-Logo_Coteccons.pdf` (bản trắng + N teal); đổi màu N bằng thuộc tính `fill` của path cuối trong SVG.
- Đã gỡ màn hình mật khẩu (`236/6`, prompt + sessionStorage `unlock_9box`) ở v1.7.3 theo yêu cầu user — trang mở thẳng vào dashboard.
- Font Lexend Deca + palette Coteccons: navy `#16315E`, teal `#5FD1C1`, xanh `#0047BA`, đỏ `#B86054`, xanh lá `#51AC70`.
- File 1 trang, không phụ thuộc, chạy offline, deploy thẳng SharePoint / GitHub Pages.
- Chữ "Target" ở tab Gap Analysis (mô hình 20/65/15) khác nghĩa với "Total" ở bảng Completion — giữ nguyên.

#### 6. Còn tồn
_Không còn hạng mục nào._ Phần in (`@media print`, nút Print / Save as PDF) đã **loại khỏi phạm vi** theo yêu cầu user (29/09/2026).

#### 7. Checklist
- [x] v1.7.2: Định nghĩa Potential mới (Aspiration / Engagement / Ability, không bù trừ)
- [x] v1.7.3: Nút ⓘ Rating Definitions ở mọi tab + nút Back
- [x] v1.7.3: Dọn CSS legend cũ
- [x] v1.7.3: Chốt `.page-narrow` 960px, sửa cột Case B
- [x] v1.7.3: `<title>` bỏ "Engineer Workforce"
- [x] v1.7.3: Gỡ mật khẩu đầu vào
- [x] Test: `node --check` sạch, div 333/333, Chromium headless không lỗi JS
- [ ] v1.8: Nhập số liệu SEP 2026 (chờ user gửi)

_Cập nhật: 29/09/2026 · Coteccons Academy (L&OD / CTA) · v1.7.1 → v1.7.3 (đã build)_
