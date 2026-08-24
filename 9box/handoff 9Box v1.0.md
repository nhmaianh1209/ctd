# HANDOFF — 9-Box Talent Dashboard (Coteccons)

> Tài liệu này mô tả **cách bạn gửi file Excel**, **cách Copilot convert → cập nhật `index - 9box.html`**, và **các trường dữ liệu** cần có. Mỗi lần có data mới, chỉ cần gửi Excel đúng format bên dưới là toàn bộ dashboard tự tính lại.

---

## 0. Tóm tắt nhanh (TL;DR)

| Việc | Bạn làm | Copilot làm |
|---|---|---|
| Cập nhật số liệu | Gửi 1 file Excel 3 sheet (mẫu bên dưới) | Đọc, đối chiếu tính toàn vẹn, ghi vào `BU_LEVEL`, `BU_META`, `EMPLOYEE_DATA` |
| Kiểm tra | — | Báo nếu tổng số người lệch giữa các sheet |
| Xuất bản | — | Trả lại file `index - 9box.html` đã cập nhật |

**Câu thần chú khi gửi:** *"Update dashboard 9box với file Excel đính kèm."*

---

## 1. Cấu trúc file Excel cần gửi

Gửi **1 file `.xlsx`** gồm **3 sheet**. Tên sheet đặt đúng như dưới (hoặc gần đúng — Copilot sẽ tự nhận diện, nhưng đặt đúng thì chắc chắn nhất).

### 📄 Sheet 1 — `BU_LEVEL` (ma trận số người theo BU × Level × Box)
> Đây là **nguồn dữ liệu gốc**. Mọi con số khác (tổng, zone %, KPI, heatmap, gap) đều cộng dồn từ sheet này.

| BU | Level | A1 | A2 | A3 | B1 | B2 | B3 | C1 | C2 | C3 |
|----|-------|----|----|----|----|----|----|----|----|----|
| BU1 | L1 | 0 | 1 | 1 | 0 | 11 | 0 | 1 | 1 | 0 |
| BU1 | L2 | 15 | 37 | 7 | 0 | 88 | 0 | 9 | 0 | 0 |
| ... | ... | | | | | | | | | |
| BU6 | L8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**Quy tắc:**
- Mỗi dòng = 1 tổ hợp (BU × Level). Đủ **6 BU × 8 Level = 48 dòng** (nếu số nào = 0 vẫn ghi `0`, đừng bỏ trống).
- 9 cột box: `A1 A2 A3 B1 B2 B3 C1 C2 C3` — là **số người**, không phải %.
- Nếu số BU hoặc số Level thay đổi (vd thêm BU7, hoặc chỉ còn 6 level), cứ báo — Copilot sẽ điều chỉnh `BU_NAMES` / `LEVEL_NAMES` tương ứng.

**Ý nghĩa box** (Performance × Potential):
`A1` = High/High (Star) · `A2` = Med/High · `A3` = High/Med · `B1` = High/Low · `B2` = Med/Med (Core) · `B3` = Low/High · `C1` = Med/Low · `C2` = Low/Med · `C3` = Low/Low.

---

### 📄 Sheet 2 — `BU_META` (chỉ tiêu & đã đánh giá theo BU)

| BU | Target | Completed |
|----|--------|-----------|
| BU1 | 606 | 578 |
| BU2 | 879 | 843 |
| ... | ... | ... |

**Quy tắc:**
- `Target` = tổng số CBNV cần đánh giá của BU (dùng để tính completion rate).
- `Completed` = số đã đánh giá. **Phải khớp** với tổng số người của BU đó trong Sheet 1.
  - 👉 Nếu bạn không chắc, **bỏ trống cột Completed** — Copilot sẽ tự lấy = tổng Sheet 1.
- Copilot sẽ **tự đối chiếu** và cảnh báo nếu lệch (vd: "BU2 sheet1=843 nhưng Completed=840 → lệch 3").

---

### 📄 Sheet 3 — `EMPLOYEE_C` (danh sách nhân viên trong các ô C1, C2, C3)
> Chỉ cần dữ liệu cho **3 ô C** (C1, C2, C3) — vì đây là nhóm cần review/hành động, click vào ô sẽ hiện bảng này. Không cần liệt kê nhân viên A/B.

| Box | Code | Name | BU | Level | Position | FY25 | FY26 | Potential | Manager | Note |
|-----|------|------|----|----|----------|------|------|-----------|---------|------|
| C1 | E00123 | Nguyễn Văn A | BU2 | L2 | Site Engineer | E | NI | Low | Trần B | PIP Q3 |
| C3 | E00456 | Lê Thị C | BU1 | L1 | QS | NI | NI | Low | Phạm D | Exit risk |
| ... | | | | | | | | | | |

**Quy tắc:**
- Cột **`Box`** (bắt buộc): giá trị `C1`, `C2` hoặc `C3` — dùng để phân nhân viên vào đúng ô.
- Các cột còn lại (**đề xuất**, linh hoạt — có cột nào hiện cột đó):
  | Cột | Ý nghĩa | Bắt buộc? |
  |---|---|---|
  | `Code` | Mã nhân viên | Nên có |
  | `Name` | Họ tên | Nên có |
  | `BU` | Đơn vị (khớp tên BU ở Sheet 1) | Nên có — để lọc theo BU |
  | `Level` | Cấp bậc (L1–L8) | Nên có — để lọc theo Level |
  | `Position` | Chức danh | Tuỳ |
  | `FY25` | Rating FY25 (`O`/`HE`/`E`/`NI`, để trống nếu Group 2) | Tuỳ |
  | `FY26` | Rating FY26 (`O`/`HE`/`E`/`NI`) | Tuỳ |
  | `Potential` | High/Med/Low | Tuỳ |
  | `Manager` | Line manager | Tuỳ |
  | `Note` | Ghi chú / hành động (PIP, exit…) | Tuỳ |
- **`BU` và `Level` nên khớp** với giá trị ở Sheet 1 để bộ lọc trong modal hoạt động (khi bạn click ô C ở tab By BU hoặc By Level, danh sách sẽ tự lọc đúng phạm vi).
- Muốn thêm/bớt cột? Cứ báo — Copilot chỉnh `EMP_FIELDS` trong code (thứ tự cột + nhãn hiển thị).

---

## 2. Cách hiển thị nhân viên trong ô C (đề xuất — đã build sẵn)

Khi bạn **click vào ô C1 / C2 / C3** ở panel "Box detail" (tab Overview, By BU, hoặc By Level), sẽ xuất hiện nút **"👤 View N employees in Cx →"**. Bấm nút → mở **modal (cửa sổ popup)** gồm:

- **Header:** mã ô + mô tả (vd "C3 · Low performance · Low potential") + phạm vi đang xem (Overall / BU / Level).
- **Ô search:** gõ để lọc nhanh theo tên / mã / manager.
- **Bảng nhân viên:** mỗi dòng 1 người, các cột đúng như Sheet 3. Rating (O/HE/E/NI) hiển thị dạng **chip màu** (O xanh lá, HE xanh dương, E xám, NI đỏ) để dễ đọc.
- **Footer:** nhắc "⚠ Confidential — Talent review" + phạm vi lọc.
- Đóng bằng nút ×, phím **Esc**, hoặc click ra ngoài.

**Vì sao chọn modal (thay vì bung thẳng trong trang):**
1. Danh sách C có thể dài → modal cuộn riêng, không phá layout dashboard.
2. Dữ liệu nhân viên là **nhạy cảm** → tách riêng, có nhãn "Confidential", đóng nhanh bằng Esc.
3. Tự **lọc theo ngữ cảnh**: click ô C ở tab By BU → chỉ hiện nhân viên BU đó; ở tab By Level → chỉ level đó.

> Nếu bạn thích cách khác (vd: bung inline trong panel, hoặc mở sang trang riêng), báo Copilot đổi.

**Trạng thái khi chưa có data:** nút hiện *"Employee list — data not loaded yet"* (mờ, không bấm được). Sau khi fill Sheet 3, nút tự kích hoạt.

---

## 3. Định nghĩa Performance đã cập nhật (tab "Rating Definitions")

Tab Definitions hiện phân **2 nhóm** để người đọc hiểu rõ:

**Nhóm 1 — Nhân viên có đủ 2 năm data (FY25 + FY26):**
- **High:** chỉ toàn HE hoặc O ở cả 2 năm (không có rating thấp hơn ở bất kỳ năm nào).
- **Low:** có ít nhất 1 lần NI ở FY25 **hoặc** FY26.
- **Medium:** các tổ hợp còn lại (không thuần HE/O cả 2 năm, cũng không có NI).

**Nhóm 2 — Nhân viên chỉ có 1 năm data (FY26):**
- **High:** O ở FY26.
- **Low:** NI ở FY26.
- **Medium:** HE hoặc E ở FY26.

> ⚠️ **Lưu ý phân loại:** phần logic xếp Performance này **bạn đã xử lý sẵn** khi chuẩn bị data (mỗi người đã nằm đúng ô trong Sheet 1). Copilot **không** tự tính lại phân loại — chỉ hiển thị định nghĩa để người đọc hiểu. Nếu quy tắc đổi, báo Copilot sửa text tab Definitions.

---

## 4. Những gì Copilot tự tính (bạn KHÔNG cần đưa)

Sau khi có Sheet 1 + 2 + 3, các số sau **tự động** cập nhật — không còn hardcode:

- Tổng số kỹ sư đã đánh giá (`GRAND_TOTAL`) → tiêu đề "Overall 9-Box Distribution (n = …)" và header Gap.
- Tổng target (`TOTAL_TARGET`) → KPI "Total engineers" + completion rate.
- Zone A/B/C %, ô Star A1 %, bảng completion theo BU.
- Thang màu heatmap (`HM_MAX` = ô đông nhất, tự dò).
- Toàn bộ Gap Analysis (actual vs ideal), so sánh BU/Level vs Overall.

**Model ideal** hiện = 20% A / 65% B / 15% C (chi tiết box: A1 5%, A2 7%, A3 8%, B1 15%, B2 40%, B3 10%, C1 8%, C2 5%, C3 2%). Đổi model → báo Copilot sửa const `TARGET`.

---

## 5. Checklist mỗi lần update (cho Copilot)

- [ ] Đọc Sheet 1 → ghi vào `BU_LEVEL` (số nguyên, đủ 6×8, thiếu điền 0).
- [ ] Đọc Sheet 2 → ghi vào `BU_META` (id, target, completed).
- [ ] **Đối chiếu:** tổng Sheet 1 theo BU == `completed` Sheet 2 → báo nếu lệch.
- [ ] Đọc Sheet 3 → ghi vào `EMPLOYEE_DATA` (nhóm theo cột `Box`).
- [ ] Cập nhật `EMP_FIELDS` nếu Sheet 3 đổi cột.
- [ ] Đổi `BU_NAMES` / `LEVEL_NAMES` / `TARGET` nếu có thay đổi tương ứng.
- [ ] Chạy test: tổng khớp, syntax OK, modal chạy.
- [ ] Xuất `index - 9box.html`.

---

## 6. Ghi chú kỹ thuật

- **Password truy cập:** hiện `236/6` (lưu plaintext trong JS + sessionStorage). Đây là khóa hình thức, **không phải bảo mật thật** — ai mở DevTools đều thấy. Nếu cần bảo mật thật cho data nhân sự, cân nhắc đặt sau đăng nhập SharePoint/host có auth.
- **Font & màu:** Lexend Deca + palette Coteccons (navy #16315E, teal #5FD1C1, xanh #0047BA, đỏ #B86054, xanh lá #51AC70). Giữ nguyên khi update.
- **File 1 trang, không phụ thuộc:** toàn bộ HTML/CSS/JS trong 1 file, chạy offline, deploy thẳng lên SharePoint/GitHub Pages được.

---
*Cập nhật: 24/08/2026 · Coteccons Academy (L&OD / CTA)*
