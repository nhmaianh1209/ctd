### HANDOFF — 9-Box Talent Dashboard (Coteccons) · v1.6

Thay thế bản _handoff 9Box v1.5_. Tài liệu mô tả trạng thái hiện tại của file `index-9box-v1_6.html`, **những gì đã đổi ở v1.6**, và việc còn tồn — để mang cả 2 file sang chat khác build tiếp v1.7 khi có feedback.
File hiện hành: `index-9box-v1_6.html` · Mật khẩu: `236/6` · Kỳ dữ liệu: **APR 2026** (biến `DATA_PERIOD`) — không đổi.

#### 0. TL;DR cho phiên chat kế tiếp
v1.6 **rebuild mục 1 "Where the gap is" của tab Gap Analysis** theo **Phương án A — 3 thẻ = 3 zone song song (A / B / C)**. Trước đây 3 thẻ là *Largest over target · Largest under target · People off target* (thẻ 1 & 3 cùng hiện 615 → gây rối, nhãn mơ hồ). Nay mỗi thẻ = một zone, hiện % actual + actual vs ideal + gap. Chỉ đụng hàm `renderVerdict()`. Node `--check` sạch, số liệu verify khớp. **Không có hạng mục nào đang chờ build.**

#### 1. Phạm vi của file này (không đổi)
Dashboard phục vụ **DATA** — đi từ tổng quan xuống chi tiết, insight nhẹ ở mô tả từng ô. Thông điệp/khuyến nghị/độ tin cậy dữ liệu thuộc **slide trình BLĐ**, không đưa vào HTML.
Người xem chính: Ban lãnh đạo (Chủ tịch là người nước ngoài) → **toàn bộ giao diện tiếng Anh**.

#### 2. Những gì đã build ở v1.6 (đã xong, đã test)
Rebuild **mục 1 tab Gap Analysis** (`id="gap-verdict"`, hàm `renderVerdict()`).

##### 2.1 — Vì sao đổi
3 thẻ cũ đọc theo **số tuyệt đối từng zone rời rạc**:
- *Largest over target ↑615* (A-zone thừa) và *People off target 615* (= Σ phần dôi dương) **trùng số 615** vì chỉ A-zone lệch dương → người đọc tưởng lỗi lặp.
- *People off target* nhãn mơ hồ, dễ hiểu nhầm "615 người bị đánh giá sai".
- Chưa chạm insight lãnh đạo quan tâm: **tháp nhân tài lộn ngược / lạm phát rating** (A = 52% ≈ 2,6× chuẩn, lõi B rỗng 42% vs 65%).

##### 2.2 — 3 thẻ mới (Phương án A): 3 zone song song, tính động từ dữ liệu
| Thẻ (nhãn) | Value | Sub (data APR 2026) |
|---|---|---|
| **A-ZONE · Top talent** | **52.3%** | actual 996 vs ideal 20% (↑615) |
| **B-ZONE · Core** | **42.0%** | actual 800 vs ideal 65% (↓439) |
| **C-ZONE · Needs attention** | **5.8%** | actual 110 vs ideal 15% (↓176) |

- Mỗi thẻ = **một zone**, thứ tự A → B → C (nhất quán với grid + legend toàn dashboard). Không còn nhãn trừu tượng, BLĐ đọc thẳng hình dạng tháp nhân tài.
- Nhãn + value tô **màu chữ theo zone** (`textC`); gap hiện mũi tên `↑`/`↓` + số tuyệt đối.
- Toàn bộ derive từ `zoneGroups` (`renderVerdict` chỉ `zoneGroups.map(card)`) → **không hardcode**, tự cập nhật khi refresh data.
- Nhãn section 1 giữ nguyên **"Where the gap is"**.

#### 3. Approach đã chốt cho v1.7 — CHƯA BUILD
_(Trống — chưa có feedback mới.)_

#### 4. Bảng điều khiển hiển thị (sửa ở đây, không sửa chỗ khác) — không đổi
```
const DATA_PERIOD='APR 2026';   // đổi mỗi kỳ; topbar tự đọc
const SMALL_N=30;               // nhóm nhỏ hơn số này hiện count thay vì %
const DEFAULT_BOX='A1';         // ô mở sẵn trong Box detail
```
| Hằng số | Ý nghĩa |
|---|---|
| `PASSWORD` | Mật khẩu truy cập, hiện `236/6` |
| `CA/CB/CC, TA/TB/TC` | Màu fill / màu chữ theo zone A/B/C — dùng chung, gồm 3 thẻ verdict mới (v1.6) |
| `BOX_DEF` | Map mỗi box (A1…C3) → zone |
| `BU_META` | Target / Completed từng BU |
| `TARGET` | Model ideal — 20% A / 65% B / 15% C (nguồn cho `idealPct` của 3 thẻ) |

#### 5. Những gì tự tính (không cần đưa, không đổi)
- `GRAND_TOTAL`, `TOTAL_TARGET`, zone A/B/C %, ô Star A1 %, completion theo BU
- **3 thẻ verdict** (`renderVerdict`): tỉ lệ bội, gap zone, tổng dôi — tất cả derive từ `zoneGroups` trong `renderGapCharts()`
- Chip "small sample" + chuyển %/count theo `SMALL_N`

#### 6. Định nghĩa Performance & Potential — không đổi (v1.5)
Tab Rating Definitions vẫn 3 mục: 1 Performance · 2 Potential · 3 9-Box (HTML tĩnh).

#### 7. Checklist v1.6 — ĐÃ HOÀN THÀNH
- [x] Rebuild mục 1 Gap tab theo Phương án A (3 thẻ = 3 zone song song A / B / C)
- [x] Bỏ trùng số 615 giữa thẻ 1 & 3 của bản cũ
- [x] Mỗi thẻ: % actual + actual vs ideal + gap arrow; màu chữ theo zone
- [x] Giữ nhãn section 1 = "Where the gap is"
- [x] Toàn bộ tiếng Anh
- [x] Test: `node --check` sạch, số liệu verify (52.3% ↑615 / 42.0% ↓439 / 5.8% ↓176)
- [x] Xuất `index-9box-v1_6.html`

#### 8. Ghi chú kỹ thuật — không đổi
- Mật khẩu `236/6` plaintext trong JS + sessionStorage — khóa hình thức.
- Font Lexend Deca + palette Coteccons: navy `#16315E`, teal `#5FD1C1`, xanh `#0047BA`, đỏ `#B86054`, xanh lá `#51AC70`.
- File 1 trang, không phụ thuộc, chạy offline, deploy thẳng SharePoint / GitHub Pages.
- Biến runtime: `curBU, curLevel, selBox, hmMode, hmNum, cmpOpen, gapBoxOpen`; `resetView()` đưa về mặc định.

#### 9. Còn tồn — chưa làm
| Việc | Ghi chú |
|---|---|
| `@media print` — in không mất màu nền zone, không cắt biểu đồ | Sau khi bố cục ổn định |
| Nút "Print / Save as PDF" ở topbar | BLĐ hay mang bản in vào họp |
| Nút ⓘ mở Rating Definitions ở mọi tab | Người đọc cần hiểu định nghĩa trước khi nhìn số |
| Dọn CSS legend cũ (`.legend-grid`, `.legend-col*`, `.nb-ref*`) | Tùy chọn |

_Cập nhật: 24/08/2026 · Coteccons Academy (L&OD / CTA) · v1.5 → v1.6 (đã build)_
