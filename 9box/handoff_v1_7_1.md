### HANDOFF — 9-Box Talent Dashboard (Coteccons) · v1.7.1

Thay thế bản _handoff 9Box v1.7_. Tài liệu mô tả trạng thái hiện tại của file `index-9box-v1_7_1.html`, **những gì đã đổi ở v1.7 → v1.7.1**, và việc còn tồn.
File hiện hành: `index-9box-v1_7_1.html` · Mật khẩu: `236/6` · Kỳ dữ liệu: **APR 2026** (biến `DATA_PERIOD`) — không đổi.

#### 0. TL;DR cho phiên chat kế tiếp
v1.7.1 sửa 5 small details theo feedback sau khi xem v1.7: (1) bỏ badge `n=14` khỏi tên BU4 trong bảng heatmap; (2) hero "Assessment Coverage" đổi field name `Total engineers`→`Total`, `Assessed`→`Completed`; (3) đồng bộ tên field sang bảng "Completion Rate by BU" (`Target`→`Total`); (4) header topbar bỏ đoạn "ENGINEER WORKFORCE", chỉ còn `9-BOX TALENT DASHBOARD · APR 2026`, chữ subtitle in đậm (Lexend Deca Bold) cho nổi bật; (5) footer đổi từ nền navy sang nền xám nhạt `#F0F4FA` + viền trên 1px, chữ về 1 tone navy/xám (bỏ màu teal nhấn) cho nhẹ nhàng hơn. Node `--check` sạch, div cân bằng (330/330).

##### v1.7 (trước đó — giữ nguyên, chưa đổi lại)
(1) thay logo giả bằng **logo thật Coteccons** (full lockup — mark + wordmark + tagline, bản trắng/N-teal, lấy từ file gốc `2026-Logo_Coteccons.pdf`, nhúng dạng SVG vector trực tiếp trong HTML — không phụ thuộc file ngoài); (2) thu hẹp bố cục 2 tab **Gap Analysis** và **Rating Definitions** (`.page-narrow`, max-width 960px); (3) thêm **footer** cố định cuối trang.

#### 1. Phạm vi của file này (không đổi)
Dashboard phục vụ **DATA** — đi từ tổng quan xuống chi tiết, insight nhẹ ở mô tả từng ô. Thông điệp/khuyến nghị/độ tin cậy dữ liệu thuộc **slide trình BLĐ**, không đưa vào HTML.
Người xem chính: Ban lãnh đạo (Chủ tịch là người nước ngoài) → **toàn bộ giao diện tiếng Anh**.

#### 2. Những gì đã build ở v1.7 (đã xong, đã test)

##### 2.1 — Logo thật (topbar)
- Trước: `<div class="logo">C</div>` — ô vuông teal tự chế + text "COTECCONS" rời.
- Nay: SVG vector inline (trích từ trang có nền tối trong file gốc `2026-Logo_Coteccons.pdf`, đã bỏ nền xám demo, crop sát viewBox) — gồm mark hành tinh-C trắng + wordmark "COTECCONS" trắng + chữ "N" cách điệu màu teal + tagline "BUILDING FUTURES". Class `.topbar-logo{height:26px}`, tỉ lệ gốc giữ nguyên qua `viewBox` nên không méo hình.
- Thêm `.topbar-divider` (vạch dọc mờ) ngăn logo và subtitle "9-BOX TALENT DASHBOARD".
- Đã xoá CSS `.logo` và `.brand` (không còn dùng).

##### 2.2 — Thu gọn layout Gap Analysis & Rating Definitions
- CSS mới: `.page-narrow{max-width:960px}` — áp cho `#tab-gap` và `#tab-legend` (thêm class, giữ nguyên `.page`).
- Overview / By BU / By Level giữ nguyên `max-width:1440px` (cần rộng cho chart/grid nhiều cột).
- **Chưa tinh chỉnh sâu** — build theo đúng brief "build thử rồi xem & chỉnh sau". Nếu 960px chưa vừa mắt, đổi 1 số trong `.page-narrow` là xong, không ảnh hưởng logic khác.

##### 2.3 — Footer
- Thêm `<div class="site-footer">` cố định cuối trang (1 lần, dùng chung mọi tab — nằm ngoài các `.page` nên luôn hiển thị).
- Nội dung: **Coteccons** · **Internal / Confidential** (màu teal nhấn) · **By Human Capital**.
- Style: nền navy `#16315E`, viền trên teal 2.5px (đồng bộ topbar), chữ nhỏ 11px, letter-spacing nhẹ.

#### 2.4 — Small details v1.7.1 (đã xong, đã test)
| # | Việc | Vị trí trong code |
|---|---|---|
| 1 | Bỏ badge `n=14` (small-sample) khỏi label BU4 trong bảng heatmap | hàm `renderHeatmap()` — bỏ đoạn `${bd.n<SMALL_N?...}` khi render `<td>` tên BU |
| 2 | Hero "Assessment Coverage": `Total engineers`→`Total`, `Assessed`→`Completed` | hàm `renderKPIs()`, group `Assessment coverage` |
| 3 | Bảng "Completion Rate by BU": cột `Target`→`Total` | `<thead>` của `#completion-tbody`, id `tab-overview` |
| 4 | Header: bỏ "ENGINEER WORKFORCE", subtitle in đậm | dòng gán `topbar-subtitle`.textContent + CSS `.subtitle{font-weight:700;font-size:12px}` |
| 5 | Footer: nền `#F0F4FA`, viền trên `1px solid #D5DFEF`, chữ về tone navy/xám (`#16315E` / `#6B7A8D`), bỏ teal accent | CSS `.site-footer`, `.site-footer strong`, `.site-footer .ftr-dot`, `.site-footer .ftr-warn` |

**Lưu ý phạm vi:** chữ "Target" ở tab Gap Analysis (mô hình lý tưởng 20/65/15%) **không đổi** — khác nghĩa với "Target" ở bảng Completion (vốn là headcount trong phạm vi), nên giữ nguyên để không gây nhầm ý nghĩa. Các cảnh báo "small sample" ở màn hình chi tiết BU/Level (banner `smalln-note`) cũng **không đổi** — chỉ bỏ badge `n=X` ở bảng heatmap tổng quan theo đúng yêu cầu.

#### 3. Approach đã chốt cho v1.8 — CHƯA BUILD
_(Trống — chưa có feedback mới. Có thể cần: tinh chỉnh lại max-width của `.page-narrow` sau khi xem thực tế; các hạng mục tồn đọng ở mục 6 dưới.)_

#### 4. Bảng điều khiển hiển thị (sửa ở đây, không sửa chỗ khác) — không đổi
```
const DATA_PERIOD='APR 2026';   // đổi mỗi kỳ; topbar tự đọc
const SMALL_N=30;               // nhóm nhỏ hơn số này hiện count thay vì %
const DEFAULT_BOX='A1';         // ô mở sẵn trong Box detail
```
| Hằng số | Ý nghĩa |
|---|---|
| `PASSWORD` | Mật khẩu truy cập, hiện `236/6` |
| `CA/CB/CC, TA/TB/TC` | Màu fill / màu chữ theo zone A/B/C |
| `BOX_DEF` | Map mỗi box (A1…C3) → zone |
| `BU_META` | Target / Completed từng BU |
| `TARGET` | Model ideal — 20% A / 65% B / 15% C |

#### 5. Ghi chú kỹ thuật mới (v1.7)
- Logo SVG là **vector path thật** (trích xuất từ PDF gốc bằng `pdftocairo`, không phải ảnh raster/base64) → sắc nét ở mọi độ phân giải, file nhẹ (~25KB), không cần font ngoài vì chữ đã là path.
- Nguồn gốc file logo: `2026-Logo_Coteccons.pdf` (18 trang, có đủ biến thể màu N — teal/blue/orange/green/gray — và bản đảo màu cho nền sáng/tối). Đã chọn bản **trắng + N teal** vì khớp nền navy của topbar và bảng màu dashboard hiện có.
- Nếu cần đổi màu N sau này (vd sang xanh dương `#0047BA` cho khớp CTA khác), có thể sửa trực tiếp thuộc tính `fill` của path chữ N trong SVG (path cuối cùng, `fill="rgb(0%, 73.725891%, 71.372986%)"`).
- Mật khẩu `236/6` plaintext trong JS + sessionStorage — khóa hình thức (không đổi).
- Font Lexend Deca + palette Coteccons: navy `#16315E`, teal `#5FD1C1`, xanh `#0047BA`, đỏ `#B86054`, xanh lá `#51AC70`.
- File 1 trang, không phụ thuộc, chạy offline, deploy thẳng SharePoint / GitHub Pages.

#### 6. Còn tồn — chưa làm (kế thừa từ v1.6, chưa đụng tới)
| Việc | Ghi chú |
|---|---|
| `@media print` — in không mất màu nền zone, không cắt biểu đồ | Sau khi bố cục ổn định |
| Nút "Print / Save as PDF" ở topbar | BLĐ hay mang bản in vào họp |
| Nút ⓘ mở Rating Definitions ở mọi tab | Người đọc cần hiểu định nghĩa trước khi nhìn số |
| Dọn CSS legend cũ (`.legend-grid`, `.legend-col*`, `.nb-ref*`) | Tùy chọn |
| Tinh chỉnh lại max-width `.page-narrow` (hiện 960px, mang tính build-thử) | Sau khi user xem thực tế |

#### 7. Checklist v1.7 → v1.7.1 — ĐÃ HOÀN THÀNH
- [x] v1.7: Thay logo giả bằng logo thật Coteccons (SVG vector, mark + wordmark + tagline)
- [x] v1.7: Thu gọn layout tab Gap Analysis & Rating Definitions (`.page-narrow`, 960px)
- [x] v1.7: Thêm footer
- [x] v1.7.1: Bỏ badge `n=14` khỏi heatmap BU4
- [x] v1.7.1: Đồng bộ field name Total/Completed (hero + bảng Completion Rate by BU)
- [x] v1.7.1: Header bỏ "ENGINEER WORKFORCE", subtitle bold
- [x] v1.7.1: Footer đổi tone xám, bỏ nền navy
- [x] Test: `node --check` sạch, div cân bằng (330/330)
- [x] Xuất `index-9box-v1_7_1.html`

_Cập nhật: 25/08/2026 · Coteccons Academy (L&OD / CTA) · v1.7 → v1.7.1 (đã build)_
