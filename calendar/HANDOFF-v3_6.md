# 📘 HANDOFF — CTD Training Calendar v3.6

**Tài liệu bàn giao chính thức** cho hệ thống Lịch đào tạo Coteccons Academy. Phiên bản này tổng hợp toàn bộ kiến thức, schema, cấu hình và hướng dẫn vận hành — **sử dụng độc lập, không cần tham chiếu HANDOFF cũ**.

| | |
|---|---|
| **Phiên bản** | v3.6 |
| **Ngày bàn giao** | 07/07/2026 |
| **Chủ sở hữu** | Phòng L&OD · Coteccons Academy |
| **Liên hệ** | cta@coteccons.vn |
| **Repo** | GitHub Pages (`ctd-training-calendar`) |
| **Backend** | Firebase project `ctd-training-calendar` (Singapore region) |

---

## 📑 Mục lục

1. [Tổng quan hệ thống](#1-tổng-quan-hệ-thống)
2. [Kiến trúc & Deploy](#2-kiến-trúc--deploy)
3. [Schema dữ liệu (Firestore)](#3-schema-dữ-liệu-firestore)
4. [Mã khoá học — Logic auto-gen](#4-mã-khoá-học--logic-auto-gen)
4b. [Người phụ trách (PIC)](#4b-người-phụ-trách-pic)
5. [UI/UX principles](#5-uiux-principles)
6. [Trang User (index)](#6-trang-user-index)
7. [Trang Admin](#7-trang-admin)
8. [Tab "Các định nghĩa"](#8-tab-các-định-nghĩa)
9. [Excel Export](#9-excel-export)
9b. [Export Email Hỗ trợ Tổ chức](#9b-export-email-hỗ-trợ-tổ-chức)
10. [Migration & Backend Adapter](#10-migration--backend-adapter)
11. [Firebase config & Security Rules](#11-firebase-config--security-rules)
12. [Deploy workflow](#12-deploy-workflow)
13. [Vận hành & bảo trì](#13-vận-hành--bảo-trì)
14. [Xử lý sự cố thường gặp](#14-xử-lý-sự-cố-thường-gặp)
15. [Lịch sử phiên bản](#15-lịch-sử-phiên-bản)
16. [Nguyên tắc thiết kế](#16-nguyên-tắc-thiết-kế)
17. [File deliverables](#17-file-deliverables)
18. [Liên hệ](#18-liên-hệ)

---

## 1. Tổng quan hệ thống

Hệ thống nội bộ giúp Phòng L&OD Coteccons Academy:

- **Quản lý** lịch các khoá đào tạo hàng tháng (admin nhập trực tiếp qua form, không cần Excel upload)
- **Truyền thông** lịch đào tạo công khai đến toàn bộ nhân viên qua trang user
- **Phân quyền hiển thị** linh hoạt giữa khoá Nội bộ và khoá Công khai
- **Xuất Excel** báo cáo theo nhu cầu (tháng / khoảng tháng / tất cả) với cấu trúc đồng bộ 12 trường form

### Đối tượng dùng

| Vai trò | Trang | Auth |
|---|---|---|
| Toàn bộ nhân viên Coteccons | `index.html` | Không cần login |
| Phòng L&OD | `admin.html` | Email/password whitelist |

### Approach nhập liệu

**Admin nhập trực tiếp qua form → ghi thẳng vào Firestore real-time → user xem ngay.** Không dùng Excel upload/import.

---

## 2. Kiến trúc & Deploy

```
┌─────────────────────┐         ┌─────────────────────┐
│  ADMIN              │         │  USER (public)      │
│  admin.html         │         │  index.html         │
│  (cần login)        │         │  (không cần login)  │
└──────────┬──────────┘         └──────────┬──────────┘
           │ CRUD                          │ READ (public only)
           ▼                               ▼
    ┌──────────────────────────────────────────┐
    │  Firebase Authentication                 │
    │  + Firestore Database (Singapore region) │
    │  Project: ctd-training-calendar          │
    │  Plan: Spark (Free tier)                 │
    └──────────────────────────────────────────┘
Hosting: GitHub Pages (static HTML files)
```

### Stack

- **Frontend:** 2 file HTML tĩnh (~24 KB user + ~67 KB admin), không cần build step
- **Backend:** Firebase Firestore + Auth
- **Hosting:** GitHub Pages
- **CDN Dependencies:**
  - Firebase SDK modular v10.13.2
  - SheetJS xlsx.full.min.js (admin only, cho Excel export)
  - Google Fonts — Lexend Deca (weights 300–700)

### Backend Adapter Layer

Cả 2 file HTML tách riêng block `api_*` functions ở đầu script để cách ly business logic khỏi backend calls. Nếu tương lai đổi backend (Supabase, custom API, SharePoint...), chỉ cần sửa các function này (~30 dòng), không phải viết lại UI/UX. Effort migration ước tính 1–2 ngày.

---

## 3. Schema dữ liệu (Firestore)

### Collection: `courses`

**12 trường thông tin khoá học + 4 trường audit tự động:**

| # | Field | Type | Required | Mô tả |
|---|---|---|---|---|
| 1 | `course_name` | string | ✅ | Tên khoá học đầy đủ (max 200 ký tự) |
| 2 | `course_short_name` | string | ⬜ | Tên ngắn để hiện trong ô lịch (~30 ký tự) |
| 3 | `category` | enum | ✅ | `technical` \| `mandatory` \| `language` \| `soft-skills` |
| 4 | `course_code` | string | ✅ **UNIQUE** | Mã định danh, vd `T001` (xem mục 4) |
| 5 | `formats` | string[] | ✅ | Online, Trực tiếp HCM, Trực tiếp HN, Trực tiếp ĐN, Trực tiếp PQ, E-learning |
| 6a | `audience_type` | enum | ✅ | `internal` \| `external` |
| 6b | `audience_detail` | string | ✅ | Chi tiết đối tượng (bắt buộc non-empty) |
| 7a | `instructor_type` | enum | ✅ | `internal` \| `external` |
| 7b | `instructor_detail` | string | ✅ | Chi tiết giảng viên (bắt buộc non-empty) |
| 8 | `duration_hours` | number | ✅ | Tính bằng giờ, step 0.5 |
| 9a | `dates` | string[] | ✅ | ISO YYYY-MM-DD, vd `["2026-06-29","2026-07-05"]` |
| 9b | `months` | string[] | ✅ auto | YYYY-MM unique — auto-compute từ `dates` để query `array-contains` |
| 10a | `registration_type` | enum | ✅ | `link` \| `email` \| `assigned` \| `other` |
| 10b | `registration_link` | string | conditional | URL nếu `registration_type === 'link'` |
| 10c | `registration_other` | string | conditional | Text nếu `registration_type === 'other'` |
| 11 | `requirements` | string | ⬜ | Điều kiện tham gia |
| 12 | `visibility` | enum | ✅ | `public` (user thấy) \| `internal` (chỉ admin) |
| 13a | `pic` | string | ✅ | Người phụ trách (PIC) — 1 trong 6 tên cố định, hoặc text tự do nếu chọn "Khác" (xem mục 4b) |
| — | `created_by` | string | auto | Email người tạo |
| — | `created_at` | timestamp | auto | Server timestamp tạo |
| — | `updated_by` | string | auto | Email người sửa cuối |
| — | `updated_at` | timestamp | auto | Server timestamp sửa cuối |

### Field cũ (deprecated, đọc qua adapter fallback — xem mục 10)

| Field cũ | Field mới |
|---|---|
| `name` | → `course_name` |
| `short_name` | → `course_short_name` |
| `target` | → `audience_detail` (audience_type default `internal`) |
| `trainer_type` | → `instructor_type` |
| `trainer_name` | → `instructor_detail` |

⚠️ **Không được ghi các field cũ khi save nữa.** Record mới chỉ ghi schema hiện hành (v3.5).

### Vì sao có cả `dates[]` và `months[]`?

- `dates[]` — Lưu chi tiết từng ngày diễn ra (ISO để sort/parse dễ)
- `months[]` — Query Firestore nhanh bằng `array-contains`. Hỗ trợ khoá multi-month (vd tiếng Anh 29/6 → 5/7 → 12/7 hiện ở cả tháng 6 và tháng 7)

### Query patterns

```js
// Admin — load tất cả khoá của 1 tháng (mọi visibility)
query(collection(db,'courses'), where('months','array-contains', '2026-07'))

// User — chỉ load khoá Công khai
query(collection(db,'courses'),
  where('months','array-contains', '2026-07'),
  where('visibility','==','public'))
```

---

## 4. Mã khoá học — Logic auto-gen

### Prefix mapping

| Phân loại | Prefix |
|---|---|
| Technical | **T** |
| Mandatory | **M** |
| Language | **L** |
| Soft-skills | **S** |

### Format

`{Prefix}{3-digit sequential}` — vd:
- `T001` = Technical khóa đầu tiên
- `M042` = Mandatory khóa thứ 42
- `L015`, `S008`, ...

Admin có thể sửa tay thành mã custom (vd `T-SPECIAL-01`) — miễn là unique.

### Auto-gen behavior

Khi admin **chọn Phân loại** trong form (nếu ô "Mã khoá học" đang trống):

1. Query `api_loadAllCourses()` → lấy tất cả courses
2. Filter courses có `course_code` bắt đầu bằng prefix tương ứng
3. Extract số phía sau prefix → tìm max → +1
4. Điền vào ô với format `{Prefix}{padStart(3,'0')}`

### Nút "🔄 Tạo lại"

- Cạnh ô nhập mã
- Click để **force re-gen** mã dựa trên Phân loại đang chọn (ghi đè giá trị hiện tại)
- Yêu cầu: đã chọn Phân loại trước; nếu chưa → toast error

### Validation khi save

1. `course_code` bắt buộc non-empty
2. Uppercase normalize: `code.trim().toUpperCase()`
3. **Unique check** trên toàn collection (loại trừ document đang edit)
4. Nếu trùng → toast error `Mã khoá học "XXX" đã tồn tại. Vui lòng chọn mã khác.` và block save

### Nguyên tắc hiển thị

| Nơi | Hiển thị mã KH? |
|---|---|
| Trang user (index) — card | ❌ |
| Trang user — detail modal | ❌ |
| Admin — form input | ✅ (text input + nút regen) |
| Admin — day-course card | ✅ (navy badge nhỏ cạnh tên) |
| Excel export | ✅ (cột "4. Mã khoá học") |

### Đánh số liên tục vĩnh viễn

- **KHÔNG reset theo năm** → mã `T001` chỉ tồn tại 1 lần trong lifetime của hệ thống
- Ưu điểm: mã ngắn gọn, dễ trace lịch sử

---

## 4b. Người phụ trách (PIC)

### Schema

Field `pic` (string, required) — lưu **1 giá trị cuối cùng** đã resolve, không tách `_type`/`_detail` như Đối tượng/Giảng viên (vì danh sách PIC là cố định + fallback tự do, không cần filter theo type).

### Danh sách 6 thành viên L&OD (cố định trong code)

- Mai Anh
- Tuấn Minh
- Mỹ Dung
- Hoàng Trần
- Kim Ngân
- Thanh Sang

### UI trong form admin

- Radio 7 lựa chọn: 6 tên cố định + **"Khác"**
- Chọn "Khác" → hiện ô text nhập tự do (bắt buộc nhập nếu chọn nhánh này)
- Validate: bắt buộc chọn 1 trong 7; nếu chọn "Khác" thì text không được rỗng

### Nguyên tắc hiển thị

| Nơi | Hiển thị PIC? |
|---|---|
| Trang user (index) — card/modal | ❌ (chỉ nội bộ Admin) |
| Admin — form input | ✅ (radio + nút "Khác") |
| Admin — day-course card | ✅ (dòng `PIC: ...` trong metadata) |
| Excel export | ✅ (cột "13. Người phụ trách (PIC)") |
| Tab "Các định nghĩa" | ✅ (section 6 — mô tả danh sách + cách dùng "Khác") |

### Backend adapter

Record cũ (trước v3.5) chưa có field `pic` → `normalizeCourse()` fallback về chuỗi rỗng `''`, hiển thị `—` ở admin card cho đến khi admin mở edit và chọn PIC.

---

## 5. UI/UX principles

### Visual design

- ✅ **Navy + Teal palette** đồng bộ brand Coteccons
- ✅ **Lexend Deca** font — sạch, hỗ trợ tiếng Việt tốt
- ✅ **Calendar Monday-first** (T2 → CN)
- ✅ **Pill màu theo phân loại** — scan nhanh
- ✅ **Today** highlight bằng teal circle
- ✅ **Weekend downplayed**: T7, CN header + số ngày → gray-400 (`#94A3B8`)
- ✅ **Weekday emphasized**: T2–T6 header → navy

### Chrome palette

**Từ v3.5:** mã màu chính thức lấy từ file brand gốc `2026-Logo_Coteccons.pdf` (Pantone), thay cho mã tự đặt ở các bản trước.

| Tên | Hex | Pantone | Dùng cho |
|---|---|---|---|
| Navy | `#121f47` | 2768C | Header background, main text, weekday emphasis |
| Navy-2 | `#1b51a4` | 2728C | Gradient end (góc header) |
| Teal | `#00b0ac` | 3262C | Primary CTA, today highlight, selected day |
| Teal-dark | `#008f8c` | — (derived, không phải Pantone) | Button hover |
| Teal-light | `#e0f7f6` | — (derived, tint nhạt của Teal) | Badge background |
| Gray-400 | `#94A3B8` | — (Tailwind slate, không phải brand) | Weekend downplay / UI chrome trung tính |

Các mã "derived" (Teal-dark, Teal-light) không có trong Pantone gốc — được tính toán từ Teal chính để phục vụ hover state / nền nhạt cho badge; không phải màu brand chính thức.

### Logo

Từ v3.5, thay icon chữ "C" giả bằng **logo vector thật** (trích xuất từ `2026-Logo_Coteccons.pdf`, dạng SVG path — sắc nét ở mọi kích thước, không phải ảnh raster):

| Vị trí | Biến thể dùng | Lý do |
|---|---|---|
| Trang User — header (nền navy gradient) | Icon màu trắng | Tương phản trên nền tối |
| Admin — topbar (nền navy) | Icon màu trắng | Tương phản trên nền tối |
| Admin — màn login (nền trắng) | Icon màu teal | Đúng màu brand trên nền sáng |

Icon được nhúng trực tiếp dạng `<svg>` inline trong HTML (không phải file ảnh rời) — giữ nguyên nguyên tắc "1 file HTML độc lập, không cần asset ngoài".

### Category palette

| Phân loại | Background | Text | Dot/Header strip |
|---|---|---|---|
| 🟦 **Technical** | `#DBEAFE` | `#1E40AF` | `#3B82F6` |
| 🟧 **Mandatory** | `#FED7AA` | `#9A3412` | `#EA580C` |
| 🟩 **Language** | `#D1FAE5` | `#065F46` | `#10B981` |
| 🟨 **Soft-skills** | `#CFFAFE` | `#155E75` | `#06B6D4` |

### Sort order (card grid & day modal)

1. 🟧 Mandatory
2. 🟦 Technical
3. 🟩 Language
4. 🟨 Soft-skills

Trong cùng phân loại → sort theo `dates[0]` ascending.

### Format ngày

Mọi ngày hiển thị dạng `dd/mm`, **chỉ ngày cuối cùng** có suffix `/yyyy`:

| Input | Output |
|---|---|
| `["2026-06-29"]` | `29/06/2026` |
| `["2026-06-30","2026-07-01","2026-08-01"]` | `30/06, 01/07, 01/08/2026` |
| `["2026-07-05","2026-07-12","2026-07-19","2026-07-26"]` | `05/07, 12/07, 19/07, 26/07/2026` |

Áp dụng đồng nhất ở: user card, user detail modal, admin day modal, Excel export.

### Information hierarchy

- ✅ **Lean & focused** — card chỉ show thông tin scan-friendly; chi tiết đầy đủ ở modal
- ✅ **Course card user KHÔNG có giảng viên** — giảng viên chỉ hiện ở modal chi tiết để card gọn
- ✅ **Course card user KHÔNG có mã khoá học** — mã chỉ hiện ở admin
- ✅ **Audit info** (created_by/updated_by) chỉ hiện ở admin

### Interaction

- Click ngày → mở **Day Modal** (list khoá trong ngày, sorted theo phân loại)
- Click khoá → mở **Detail Modal** (đầy đủ thông tin)
- Modal đóng bằng **backdrop click** hoặc **X button**
- **Mini calendar** trong form admin: compact (~28px/cell), multi-month picker
- **Toast feedback** cho mọi action (success/error)

### Responsiveness

| Breakpoint | Layout |
|---|---|
| Desktop ≥1024px | Card grid 4 cột |
| Tablet 640-1024px | 2 cột |
| Mobile <640px | 1 cột, calendar cell thu nhỏ |

---

## 6. Trang User (index)

**File:** `ctd-index-v3_5.html` (rename `index.html` khi deploy)

### Cấu trúc

- **Hero header** navy gradient với badge `Coteccons Academy · L&OD`
- **Toolbar** month nav (prev/next)
- **Calendar** hiển thị courses có `visibility === 'public'`
- **Legend row** 4 chip màu category
- **Card grid** "Các khoá học trong tháng" — sorted theo phân loại
- **Day modal** khi click ngày có khoá học
- **Detail modal** khi click card hoặc course item trong day modal

### Card user hiển thị

| Field | Có hiện? |
|---|---|
| Tên khoá học | ✅ |
| Header phân loại (màu) | ✅ |
| Hình thức | ✅ (📍 icon) |
| Đối tượng | ✅ (👥 icon, format `Nội bộ/Bên ngoài: {detail}`) |
| Thời lượng | ✅ (⏱️ icon) |
| Ngày diễn ra | ✅ (📅 icon) |
| Cách đăng ký | ✅ (🔗 icon) |
| Giảng viên | ❌ (chỉ ở detail modal) |
| Mã khoá học | ❌ |

### Detail modal user hiển thị

Phân loại • Hình thức • Đối tượng • Giảng viên • Thời lượng • Ngày diễn ra • Cách đăng ký • Điều kiện (nếu có)

---

## 7. Trang Admin

**File:** `ctd-admin-v3_5.html` (rename `admin.html` khi deploy)

### Cấu trúc

- **Login screen** (email + password)
- **Topbar** (brand + user email + logout)
- **Tab bar:** `📅 Lịch đào tạo` | `📖 Các định nghĩa`

### Tab Lịch đào tạo

- **Toolbar left:** month nav + filter pills (`Tất cả` / `🌐 Công khai` / `🔒 Nội bộ`)
- **Toolbar right:** `📊 Export Excel` button
- **Calendar** full CRUD với lock icon 🔒 trên pill nội bộ
- **Day modal:** list khoá trong ngày sorted theo phân loại, có nút Edit/Delete
- **Form modal:** 12 trường (xem dưới)
- **Export Excel modal:** 3 mode (tháng / khoảng / tất cả)

### Form modal — 13 trường

| # | Field | UI | Required |
|---|---|---|---|
| 1 | Tên khoá học | text input | ✅ |
| 2 | Tên ngắn | text input | ⬜ |
| 3 | Phân loại | radio 4 lựa chọn (có swatch màu) | ✅ |
| 4 | Mã khoá học | text input + nút 🔄 Tạo lại | ✅ (auto-gen + editable + unique) |
| 5 | Hình thức | multi-checkbox 6 options | ✅ |
| 6 | Đối tượng | radio (Nội bộ/Bên ngoài) + text detail | ✅ (cả 2) |
| 7 | Giảng viên | radio (Nội bộ/Bên ngoài) + text detail | ✅ (cả 2) |
| 8 | Thời lượng (giờ) | number step 0.5 | ✅ |
| 9 | Thời gian | mini calendar multi-day picker | ✅ (≥1 ngày) |
| 10 | Cách đăng ký | radio 4 options + conditional text | ✅ |
| 11 | Điều kiện tham gia | text input | ⬜ |
| 12 | Phân quyền hiển thị | radio (Công khai/Nội bộ) | ✅ |
| 13 | Người phụ trách (PIC) | radio 6 tên + "Khác" + conditional text | ✅ (xem mục 4b) |

### Day-course card admin hiển thị

Tên khoá + badge Mã KH + badge Phân loại + badge Visibility (Công khai/Nội bộ) + full metadata (Hình thức, Đối tượng, Giảng viên, Thời lượng, Ngày, Cách đăng ký, Điều kiện, **PIC**) + audit info + nút Edit/Delete.

---

## 8. Tab "Các định nghĩa"

### Layout

- **Mỗi item = 1 card riêng** (border + shadow + hover effect)
- Grid **2 cột desktop**, **1 cột mobile**
- Section heading có teal accent bar

### 6 sections

1. **Phân loại khoá học** (4 cards có swatch màu: Technical / Mandatory / Language / Soft-skills)
2. **Mã khoá học** (1 card full-width — logic tạo mã)
3. **Hình thức** (3 cards: Online / Trực tiếp HCM-HN-ĐN-PQ / E-learning)
4. **Cách đăng ký** (4 cards: Link / Email / Danh sách chỉ định / Khác)
5. **Phân quyền hiển thị** (2 cards: 🌐 Công khai / 🔒 Nội bộ)
6. **Người phụ trách (PIC)** *(mới từ v3.5)* — 1 card full-width, liệt kê 6 thành viên L&OD + cách dùng "Khác"

### Nội dung mẫu (đã fill)

- **Technical:** Các khoá đào tạo kỹ năng chuyên môn phục vụ trực tiếp cho công việc (vd chuyên môn xây dựng, cơ điện, quản lý dự án, chuyên môn phòng ban chức năng…).
- **Mandatory:** Các khoá đào tạo bắt buộc theo quy định pháp luật hoặc chính sách nội bộ Coteccons, tất cả nhân viên trong đối tượng chỉ định phải tham gia đầy đủ (vd ATLĐ, Hội nhập).
- **Online:** Học qua nền tảng họp trực tuyến (MS Teams).
- **Đăng ký tại link:** Đối tượng tham gia là 1 nhóm đông, được chọn đăng ký/không. Công khai link để tăng tỉ lệ đăng ký.
- **PIC:** Chọn 1 người phụ trách chính trong 6 thành viên L&OD; chọn "Khác" nếu người phụ trách không thuộc danh sách.
- ...

### Cách update Definition

Nội dung **hardcode trong HTML** (không dùng Firestore) — L&OD tự edit khi cần:

1. Mở `admin.html` (file đang deploy) bằng editor (VSCode / Notepad++)
2. Ctrl+F tìm heading section muốn sửa, vd `<h3>3. Hình thức</h3>`
3. Sửa nội dung trong `<div class="card-text">...</div>`
4. Save → commit lên GitHub → GitHub Pages tự deploy (~2 phút)

### Vì sao hardcode HTML thay vì Firestore?

- ✅ Không phụ thuộc Firestore reads (tiết kiệm quota)
- ✅ Không cần build UI CRUD cho admin
- ✅ Version control chặt qua Git
- ✅ Nội dung ít thay đổi (định nghĩa Technical không đổi mỗi tuần)

Nếu tần suất thay đổi cao → cân nhắc migrate sang Firestore `definitions` collection (Phase 3).

---

## 9. Excel Export

### 3 modes

- **Xuất tháng hiện tại** — chỉ tháng đang xem
- **Xuất khoảng tháng tuỳ chọn** — from-to (input type=month)
- **Xuất tất cả** — toàn bộ collection

### Cấu trúc 13 cột + 4 cột audit

Đồng bộ **đúng thứ tự và tên trường** với form nhập → dùng làm base cho các tác vụ downstream.

| Cột | Nguồn | Format |
|---|---|---|
| 1. Tên khoá học | `course_name` | text |
| 2. Tên ngắn | `course_short_name` | text |
| 3. Phân loại | `category` label | Technical/Mandatory/Language/Soft-skills |
| 4. Mã khoá học | `course_code` | vd T001 |
| 5. Hình thức | `formats` | join `, ` |
| 6. Đối tượng | `audience_type` + `audience_detail` | `Nội bộ/Bên ngoài: {detail}` |
| 7. Giảng viên | `instructor_type` + `instructor_detail` | `Nội bộ/Bên ngoài: {detail}` |
| 8. Thời lượng (giờ) | `duration_hours` | number |
| 9. Thời gian | `dates` | format `30/06, 01/07/2026` |
| 10. Cách đăng ký | `registration_type` + detail | `Label \| detail` khi có link/other |
| 11. Điều kiện tham gia | `requirements` | text |
| 12. Phân quyền hiển thị | `visibility` | Công khai/Nội bộ |
| 13. Người phụ trách (PIC) | `pic` | text (tên thành viên hoặc tên tự nhập) |
| Tạo bởi | `created_by` | email |
| Ngày tạo | `created_at` | locale VN |
| Sửa cuối bởi | `updated_by` | email |
| Ngày sửa cuối | `updated_at` | locale VN |

### Filename convention

- `ctd-training-calendar_{YYYY-MM}_export.xlsx` (tháng)
- `ctd-training-calendar_{from}_to_{to}_export.xlsx` (khoảng)
- `ctd-training-calendar_all_export.xlsx` (tất cả)

### Sort order trong Excel

Theo `dates[0]` ascending (ngày sớm nhất trước).

---

## 9b. Export Email Hỗ trợ Tổ chức

### Bối cảnh & mục đích

Mỗi tháng, sau khi chốt lịch đào tạo, L&OD cần gửi email cho các phòng ban tại HCM (Hành chính, Ban Quản lý toà nhà/Ban An ninh, CNTT) để báo lịch các khoá **Online** và **Trực tiếp HCM**, kèm yêu cầu hỗ trợ set up. Lịch có thể đổi giữa tháng → cần gửi lại email cập nhật.

**v3.6 là bản đơn giản (v1):** hệ thống chỉ **tạo sẵn nội dung email** (điền các trường đã có sẵn trong database, để trống các trường cần nhập tay) — người dùng copy dán vào Outlook rồi **tự điền/sửa trực tiếp trên Outlook**. Chưa lưu lại các trường tự điền vào Firestore (xem "Hướng phát triển tiếp" cuối mục).

### Vị trí

Nút **📧 Email hỗ trợ** — cạnh nút **📊 Export Excel**, trong tab "Lịch đào tạo".

### Logic lọc dữ liệu

- Chỉ lấy khoá học có `formats` chứa **"Online"** hoặc **"Trực tiếp HCM"** (khoá chỉ có HN/ĐN/PQ sẽ không xuất hiện)
- Mỗi **ngày học** trong `dates[]` (thuộc tháng được chọn) tách thành **1 dòng riêng** trong bảng — vì 1 khoá có thể học nhiều ngày với yêu cầu hỗ trợ khác nhau từng ngày
- Sort theo ngày tăng dần

### Cấu trúc bảng — 8 cột

| # | Cột | Nguồn | Có sẵn hay tự nhập? |
|---|---|---|---|
| 1 | Ngày | `dates[]` → format `Thứ X \| dd/mm` | ✅ Có sẵn |
| 2 | Giờ | — | ⬜ Để trống `______` |
| 3 | Tên khoá học | `course_short_name` (fallback `course_name`) | ✅ Có sẵn |
| 4 | Địa điểm | — | ⬜ Để trống — **trừ** khoá chỉ có format `Online` (không có `Trực tiếp HCM`) → tự gợi ý sẵn chữ `Online` |
| 5 | PIC | `pic` | ✅ Có sẵn |
| 6 | P.Hành Chính/B.QLTN | — | ⬜ Để trống |
| 7 | P.CNTT | — | ⬜ Để trống |
| 8 | BAN | — | ⬜ Để trống |

### Nội dung email (cố định, hardcode)

Phần đầu (Kính gửi, đoạn giới thiệu, 2 dòng nhờ hỗ trợ) và phần cuối (lời cảm ơn) là text cố định, chỉ thay `{tháng}/{năm}` — hardcode trong JS, giữ nguyên văn phong theo email mẫu L&OD đã dùng trước đó.

Subject/To/Cc hiển thị sẵn trong modal (dạng text, không phải input) để người dùng copy tay vào Outlook — hiện tại hardcode vì danh sách người nhận ít đổi:

- **Subject:** `Hỗ trợ tổ chức các khóa đào tạo - Tháng {MM} năm {YYYY}`
- **To:** Hanh Chinh; BQLTN Coteccons; Ban An Ninh; CTD IT Department
- **Cc:** Coteccons Academy

### Copy vào Outlook — kỹ thuật

Bảng được render bằng HTML `<table>` thật (không phải `<div>` giả bảng) với **inline style** trên từng `<td>`/`<th>` (border, padding, background) — bắt buộc phải inline vì Outlook không đọc CSS class ngoài khi paste.

Nút **📋 Copy nội dung email** dùng Clipboard API (`navigator.clipboard.write` với `ClipboardItem` chứa cả `text/html` và `text/plain`), fallback bằng `document.execCommand('copy')` cho browser cũ. Khi dán vào Outlook (Ctrl+V) sẽ ra đúng bảng có viền, giữ layout.

### Font

Preview trên web và bảng copy ra đều khai báo **Lexend Deca, weight 300 (Light), size 12px**.

⚠️ **Hạn chế đã biết:** Lexend Deca là Google Font, không nhúng được vào email. Khi dán vào Outlook (đặc biệt Outlook Desktop, dùng engine Word), font sẽ tự fallback về font mặc định máy người nhận (thường Calibri/Aptos) — đây là hạn chế của Outlook, không sửa được từ phía web app. Size 12px và cấu trúc bảng/viền vẫn giữ đúng khi dán.

### Vì sao chưa lưu dữ liệu tự nhập vào Firestore (v1)?

- Theo yêu cầu ban đầu: build bản đơn giản trước, các trường tự điền (Giờ, Địa điểm, 3 cột yêu cầu phòng ban) sẽ do người trong email **tự điền trực tiếp trên Outlook**, không cần quay lại app để điền
- Tránh phải mở rộng schema Firestore ngay ở bản đầu — không có rủi ro cho dữ liệu `courses` hiện tại
- **Hướng phát triển tiếp (chưa làm):** nếu cần giữ lại lịch sử các trường đã điền (vd để tái sử dụng khi gửi email cập nhật giữa tháng), có thể lưu thêm object `support_details` theo từng (course, date) vào Firestore — xem mục 16 "Nguyên tắc thiết kế" để biết pattern field split tương tự đã áp dụng cho Đối tượng/Giảng viên

---

## 10. Migration & Backend Adapter

### Approach: Adapter fallback (không cần bulk migration script)

Cả `index.html` và `admin.html` đều có helper `normalizeCourse(d)` trong Backend Adapter Layer:

```js
function normalizeCourse(d){
  return {
    ...d,
    course_name: d.course_name || d.name || '',
    course_short_name: d.course_short_name || d.short_name || '',
    course_code: d.course_code || '',
    audience_type: d.audience_type || 'internal',
    audience_detail: d.audience_detail || d.target || '',
    instructor_type: d.instructor_type || d.trainer_type || 'internal',
    instructor_detail: d.instructor_detail || d.trainer_name || '',
    pic: d.pic || ''
  };
}
```

Áp dụng ở mọi function LOAD:
- `api_loadCoursesByMonth`
- `api_loadAllCourses`
- `api_loadCoursesByMonthRange`
- `api_loadPublicCoursesByMonth` (user site)

### Fallback mapping

| Field mới | Fallback từ | Default nếu không có |
|---|---|---|
| `course_name` | `name` | `''` |
| `course_short_name` | `short_name` | `''` |
| `course_code` | — | `''` (blank cho đến khi admin edit) |
| `audience_type` | — | `'internal'` |
| `audience_detail` | `target` | `''` |
| `instructor_type` | `trainer_type` | `'internal'` |
| `instructor_detail` | `trainer_name` | `''` |
| `pic` *(mới v3.5)* | — | `''` (hiển thị `—`, admin cần điền khi edit lần đầu) |

### Behavior khi save

- Record được lưu bởi phiên bản hiện tại → **chỉ chứa field mới** (không kèm field cũ)
- Record cũ chưa được edit → **giữ nguyên field cũ**, hiển thị đúng qua adapter
- Sau khi admin mở form edit 1 record cũ → save → chuyển sang schema mới nhất hoàn toàn (bao gồm bắt buộc chọn PIC)

### Điểm cần chú ý

- ⚠️ Record v3.1 có `course_code = ''` — khi admin edit lần đầu **phải điền mã** (validate required)
- ⚠️ Record v3.1 có `target = "Trưởng phòng"` → adapter map thành `audience_type = "internal"` + `audience_detail = "Trưởng phòng"`. Nếu đối tượng thực tế là external → admin cần chỉnh lại khi edit.

### Reset backend (nếu cần)

Xoá toàn bộ collection courses trong Firebase Console:

1. Firebase Console → Firestore Database → tab Data
2. Click collection `courses` → 3-dot menu → **Delete collection**
3. Gõ tên xác nhận → Delete
4. Reload admin — calendar trống, nhập lại từ đầu

Sau khi reset, mọi record mới đều được ghi bằng schema hiện hành sạch, mã KH auto-gen từ T001/M001/L001/S001.

---

## 11. Firebase config & Security Rules

### Project info

| Thuộc tính | Giá trị |
|---|---|
| Project ID | `ctd-training-calendar` |
| Location | `asia-southeast1` (Singapore) — không đổi được sau khi tạo |
| Plan | Spark (Free tier) |
| Console | https://console.firebase.google.com/project/ctd-training-calendar |

### Firebase config (embed trong cả 2 file HTML)

```js
const firebaseConfig = {
  apiKey: "AIzaSyCl0izQatfWqRqQ4PjeJv242Q2obuaSyXw",
  authDomain: "ctd-training-calendar.firebaseapp.com",
  projectId: "ctd-training-calendar",
  storageBucket: "ctd-training-calendar.firebasestorage.app",
  messagingSenderId: "12986365110",
  appId: "1:12986365110:web:61083721f3c60525b7a217"
};
```

⚠️ Config này lộ ra public **không sao** — Firebase được thiết kế cho phép public. Bảo mật được enforce bằng Security Rules.

### Whitelist admin (2 emails)

- `anhnhm@coteccons.vn` (Admin chính)
- `minhvt01@coteccons.vn` (Admin phụ)

Mức phân quyền: **Mức A — Quyền ngang nhau** (tất cả có quyền create/edit/delete như nhau).

### Security Rules

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    function isAdmin() {
      return request.auth != null && request.auth.token.email in [
        'anhnhm@coteccons.vn',
        'minhvt01@coteccons.vn'
      ];
    }
    match /courses/{courseId} {
      allow read: if resource.data.visibility == 'public' || isAdmin();
      allow create: if isAdmin()
                    && request.resource.data.created_by == request.auth.token.email;
      allow update: if isAdmin()
                    && request.resource.data.created_by == resource.data.created_by;
      allow delete: if isAdmin();
    }
  }
}
```

### Đảm bảo gì?

- ✅ User chưa login chỉ thấy khoá `visibility = 'public'`
- ✅ Admin (trong whitelist) full quyền
- ✅ Người khác login (kể cả tự đăng ký) — không có quyền nào
- ✅ `created_by` không thể bị giả mạo

### Khi cần update whitelist

Sửa list email trong Rules → **Publish** → hiệu lực ngay.

---

## 12. Deploy workflow

### Setup lần đầu

**Bước 1 — GitHub repo:**
- Repository name: `ctd-training-calendar`
- Visibility: **Public** (bắt buộc cho GitHub Pages free)

**Bước 2 — Upload files:**
- Tải `ctd-index-v3_5.html` và `ctd-admin-v3_5.html`
- **Rename trước khi upload:**
  - `ctd-index-v3_5.html` → `index.html`
  - `ctd-admin-v3_5.html` → `admin.html`
- Drag & drop vào GitHub repo → Commit

**Bước 3 — Bật GitHub Pages:**
- Settings → Pages → Source: Deploy from branch
- Branch: `main` → `/ (root)` → Save
- Đợi 1-2 phút → URL: `https://<username>.github.io/ctd-training-calendar/`

**Bước 4 — ⚠️ Authorized Domain trong Firebase (bắt buộc):**
- Firebase Console → Authentication → Settings → Authorized domains
- Add domain: `<username>.github.io` → Save

### URLs production

| Trang | URL |
|---|---|
| User (public) | `https://<username>.github.io/ctd-training-calendar/` |
| Admin (login) | `https://<username>.github.io/ctd-training-calendar/admin.html` |

### Update workflow sau này

1. Sửa file `.html` local
2. Commit & push lên GitHub
3. Đợi 1-2 phút GitHub Pages rebuild
4. Hard refresh browser (**Ctrl+Shift+R**) để bypass cache

---

## 13. Vận hành & bảo trì

### Thêm thành viên team mới

1. Firebase Console → Authentication → Users → **Add user** → email + password tạm → Save
2. Firestore Database → Rules → thêm email vào `isAdmin()` array → **Publish**
3. Gửi email tạm + URL admin cho member, yêu cầu đổi password lần đầu

### Xoá thành viên (nghỉ việc)

1. Authentication → Users → tìm email → 3-dot → **Disable account**
2. Firestore → Rules → xoá email khỏi `isAdmin()` array → **Publish**

### Reset password cho member

**Cách 1 (khuyến nghị):** Authentication → Users → 3-dot → **Reset password** → Firebase tự gửi email reset link
**Cách 2 (thủ công):** Authentication → Users → 3-dot → **Edit password**

### Backup data định kỳ

**Khuyến nghị mỗi tháng 1 lần:**
1. Login admin.html
2. Click **📊 Export Excel** → **Xuất tất cả** → Tải file
3. Lưu vào OneDrive/SharePoint nội bộ

### Cập nhật nội dung Tab "Các định nghĩa"

Edit trực tiếp file HTML (xem mục 8).

### Monitoring usage

Free tier limits: **50K reads/ngày · 20K writes/ngày · 1 GB storage**.
Check tại: Firebase Console → Usage tab. Scale L&OD nhỏ → khó vượt 1%.

---

## 14. Xử lý sự cố thường gặp

### ❌ Login fail "Email hoặc mật khẩu không đúng"

**Nguyên nhân:** Email/password sai · Account bị disable · Account chưa tồn tại
**Giải pháp:** Firebase Console → Authentication → Users xem account có active · Reset password nếu cần

### ❌ Login OK nhưng calendar trống

**Nguyên nhân:** Chưa có data hoặc Security Rules block
**Giải pháp:**
- F12 → Console xem error
- Kiểm tra Firestore Console có document trong collection `courses` không
- Kiểm tra Security Rules đã publish đúng

### ❌ Lỗi "auth/unauthorized-domain"

**Nguyên nhân:** Domain hiện tại không nằm trong Authorized Domains của Firebase Auth
**Giải pháp:** Firebase Console → Authentication → Settings → Authorized domains → Add domain

### ❌ Khoá cũ (v1/v2) không hiển thị

**Nguyên nhân:** Schema cũ dùng `{year, month, days[]}` — từ v3 đã chuyển sang `{dates[], months[]}`
**Giải pháp:**
- Nếu là data test → xoá và tạo lại
- Nếu là data thật → liên hệ tech support viết script migration

### ❌ Mã khoá học trùng khi save

**Nguyên nhân:** Đã có course khác dùng mã đó (unique constraint)
**Giải pháp:**
- Sửa mã thủ công
- Hoặc click nút **🔄 Tạo lại** để sinh mã mới

### ❌ Mini calendar trong form không hiện

**Giải pháp:** F12 → Console check error · Reload page (Ctrl+Shift+R)

### ❌ Export Excel không tải xuống

**Nguyên nhân:** Browser block popup · SheetJS CDN load lỗi
**Giải pháp:** Allow popup cho domain GitHub Pages · Reload chờ CDN load xong

### ❌ Weekend hiện màu sai (còn teal thay vì gray)

**Nguyên nhân:** Cache browser cũ
**Giải pháp:** Hard refresh **Ctrl+Shift+R**

---

## 15. Lịch sử phiên bản

### v3.6 (CURRENT — 07/07/2026)

- ✅ Thêm tính năng **Export Email Hỗ trợ Tổ chức** — nút `📧 Email hỗ trợ` cạnh Export Excel (xem mục 9b)
- ✅ Tự lọc khoá học format `Online`/`Trực tiếp HCM`, tách mỗi ngày học thành 1 dòng, điền sẵn Ngày/Tên khoá/PIC từ database, để trống Giờ/Địa điểm/3 cột yêu cầu phòng ban
- ✅ Bảng render bằng HTML `<table>` + inline style — copy 1-click (Clipboard API `text/html`) dán thẳng vào Outlook giữ khung bảng
- ✅ Font preview & bảng copy: Lexend Deca Light 12px (có ghi chú hạn chế font khi dán vào Outlook)
- ✅ Không đổi schema Firestore — chỉ sửa `admin.html`, `index.html` giữ nguyên, không có rủi ro dữ liệu

### v3.5 (07/07/2026)

- ✅ Thêm field **`pic`** (Người phụ trách) — trường 13 trong form, radio 6 thành viên L&OD + "Khác", bắt buộc, chỉ hiện ở Admin (form/card/Excel), không hiện ở trang User
- ✅ Thêm section 6 "Người phụ trách (PIC)" vào Tab "Các định nghĩa"
- ✅ Excel export mở rộng thành **13 cột** (thêm cột `13. Người phụ trách (PIC)`)
- ✅ Cập nhật màu brand sang đúng mã Pantone chính thức (Navy `#121f47`, Navy-2 `#1b51a4`, Teal `#00b0ac`) — lấy từ file gốc `2026-Logo_Coteccons.pdf`, thay cho mã hex tự đặt ở các bản trước
- ✅ Thay icon chữ "C" giả bằng **logo vector thật** (SVG inline, trích từ file gốc) ở: trang User (header), Admin (topbar + màn login)

### v3.4 (07/07/2026)

- ✅ Tab **"Các định nghĩa"** (rename từ "Definition") với layout mỗi item 1 khung riêng
- ✅ Bỏ 2 sections Đối tượng, Giảng viên khỏi Tab định nghĩa (đã rõ ràng từ form)
- ✅ Nội dung Tab đã fill sẵn 5 sections (Phân loại / Mã khoá học / Hình thức / Cách đăng ký / Phân quyền)
- ✅ Grid layout 2 cột desktop, responsive 1 cột mobile

### v3.3 (07/07/2026)

- ✅ Excel export đồng bộ đầy đủ **12 trường form** (đánh số 1-12) + 4 cột audit
- ✅ Thêm cột `4. Mã khoá học` vào Excel (đảo quyết định trước là loại khỏi Excel)
- ✅ Gộp cột "Cách đăng ký" + "Link/Ghi chú" → 1 cột `10. Cách đăng ký` format `Label | detail`
- ✅ Đổi "Các ngày" → `9. Thời gian`, "Phân quyền" → `12. Phân quyền hiển thị` để đồng bộ label form

### v3.2 (07/07/2026)

- ✅ Thêm field **`course_code`** với auto-gen (T/M/L/S prefix + 3-digit sequential, unique, editable)
- ✅ Rename schema: `name` → `course_name`, `short_name` → `course_short_name`
- ✅ Restructure Đối tượng: single text → radio (Nội bộ/Bên ngoài) + detail text, REQUIRED
- ✅ Rename Giảng viên: `trainer_type`/`trainer_name` → `instructor_type`/`instructor_detail`
- ✅ Weekend calendar colors: teal → gray-400 (T7/CN downplayed); weekday emphasized navy
- ✅ Add tab "Definition" (skeleton, placeholder) — sau này rename thành "Các định nghĩa"
- ✅ Backend adapter `normalizeCourse()` fallback cho v3.1 data — không cần bulk migration script

### v3.1 (30/06/2026)

- Mini calendar compact ~40% (height 28px, font 11px)
- Bỏ trainer khỏi course card user (giữ ở modal chi tiết)
- Format ngày mới: `30/06, 01/07, 01/08/2026`

### v3 (deprecated)

- Schema breaking: `{dates[], months[]}` hỗ trợ khoá multi-month
- Mini calendar đa tháng trong form
- Thêm Phân loại (4 categories với màu)
- Thêm Giảng viên (internal/external + name)
- Course cards ở trang user
- Export Excel (3 modes)
- Backend Adapter Layer

### v2 (deprecated)

- Đổi sang Firebase backend
- Schema: `{year, month, days[]}`

### v1 (deprecated)

- Excel template → JSON → push GitHub

---

## 16. Nguyên tắc thiết kế

Tích luỹ qua quá trình co-design v3.1 → v3.5 — hữu ích cho các dự án/tính năng sau.

### Style ưa thích

- **Navy + Teal palette** đồng bộ brand Coteccons
- **Lexend Deca** font
- **Lean information** — bỏ thông tin thừa, gom vào modal chi tiết
- **Vietnamese-first** trong UI; English chỉ cho technical terms/field names backend

### Naming convention

- **Prefix `course_`** cho fields của entity Course (`course_name`, `course_short_name`, `course_code`) để tránh conflict trong document
- **English snake_case** cho field name (backend); **Vietnamese** cho UI label

### Field split pattern

Các thông tin có "loại + chi tiết" → tách 2 field:

| Ví dụ | `_type` | `_detail` |
|---|---|---|
| Đối tượng | `audience_type: internal/external` | `audience_detail: "Trưởng phòng"` |
| Giảng viên | `instructor_type: internal/external` | `instructor_detail: "Anh Nguyễn Văn A"` |

**Lợi ích:** Filter/thống kê theo `_type` dễ; text tự do ở `_detail` cho flexibility.

### Backend adapter fallback

Khi rename field: giữ mapping cũ→mới trong `normalizeCourse()`. Ưu điểm:
- Không cần bulk migration script
- Zero downtime
- Gradual migration (chỉ record được edit mới update schema)

### Definition tab hardcode

Nội dung ít thay đổi → hardcode HTML là đủ. Nếu thay đổi thường xuyên → migrate sang Firestore.

### Excel export sync với form

Export phải đồng bộ **đúng thứ tự + tên trường** với form nhập → làm base cho tác vụ downstream (báo cáo, analytics, migration).

### Weekend visual downplay

Weekday (T2–T6) emphasize navy · Weekend (T7, CN) downplay gray → giúp scan lịch làm việc nhanh hơn.

### Copy nội dung ra ứng dụng ngoài (Outlook, Word...)

Khi cần tạo nội dung để copy-paste sang app khác (email client, Word...):
- Dùng **HTML table thật** (`<table><tr><td>`) với **inline style** trên từng cell — không dùng CSS class ngoài, vì app đích (Outlook) không đọc file CSS khi paste
- Web font tuỳ chỉnh (Google Fonts...) **sẽ không giữ được** khi dán vào Outlook — app đích tự fallback về font mặc định máy người nhận. Nếu cần đúng font 100% → phải xuất ảnh (screenshot), nhưng đánh đổi là mất khả năng chỉnh sửa trực tiếp trên Outlook
- Copy bằng `navigator.clipboard.write()` + `ClipboardItem` chứa cả `text/html` và `text/plain` → paste vào Outlook giữ đúng bảng có viền; fallback `document.execCommand('copy')` cho browser cũ

### Cách làm việc

- ✅ **Debrief trước khi build** cho thay đổi lớn (schema, auth, layout)
- ✅ **Confirm từng điểm rõ ràng** (A/B/C choices) trước khi triển khai
- ✅ **Ready-to-use files** thay vì code snippets phải copy-paste
- ✅ **Audit changes globally** — đổi 1 nguyên tắc thì apply consistent ở mọi nơi
- ✅ **Rapid iteration** — build → test → feedback → fix nhanh

### Nguyên tắc nội dung L&OD (general)

- **Initiative/KPI** nên bắt đầu bằng **động từ**
- Khi setup KPI từ file CTD Strategic Priorities FY2027: lấy initiatives từ cột C của sheet "2. SP"; cột D chỉ là proposal KPI tham khảo

### Bảo mật

- Ưu tiên **email + password riêng cho từng người** thay vì shared password
- Sẵn sàng giải thích trade-off bảo mật để user quyết định

---

## 17. File deliverables

| File | Rename khi deploy | Kích thước | Ghi chú |
|---|---|---|---|
| `ctd-index-v3_5.html` | `index.html` | ~25 KB | User site (public) — **không đổi ở v3.6** |
| `ctd-admin-v3_6.html` | `admin.html` | ~80 KB | Admin site (login required) — **đã update ở v3.6** |
| `HANDOFF-v3_6.md` | — | ~34 KB | Tài liệu này |

### CDN & Dependencies (không có dependency npm)

- **Firebase SDK modular v10.13.2**: `https://www.gstatic.com/firebasejs/10.13.2/`
- **SheetJS**: `https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js`
- **Google Fonts — Lexend Deca**: weights 300–700

Không cần: npm install · build step · bundler. Mở file HTML trực tiếp là chạy được (cần Internet để load CDN).

---

## 18. Liên hệ

| Vai trò | Liên hệ |
|---|---|
| Owner dự án | Phòng L&OD · Coteccons Academy |
| Email chung | cta@coteccons.vn |
| Admin chính | anhnhm@coteccons.vn |
| Admin phụ | minhvt01@coteccons.vn |
| Firebase Console | https://console.firebase.google.com/project/ctd-training-calendar |

### Khi cần hỗ trợ kỹ thuật

1. Đọc mục **[Xử lý sự cố](#14-xử-lý-sự-cố-thường-gặp)** trước
2. Check Browser DevTools Console (F12) để xem error
3. Check Firebase Console: Auth users, Firestore data, Security Rules
4. Nếu vẫn không giải quyết được → liên hệ Copilot với screenshot error

---

**Cuối tài liệu.** Phiên bản v3.6 — Ngày 07/07/2026.

*Tài liệu này nên được cập nhật mỗi khi có thay đổi schema, security rules, hoặc bổ sung tính năng mới.*
