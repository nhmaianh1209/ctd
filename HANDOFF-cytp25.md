# Handoff: trang Hồ sơ Young Talent (CYTP 2025)

Cập nhật: 29/09/2026 · Người phụ trách: Nguyễn Hoàng Mai Anh (L&OD, Coteccons)

## 1. Trang này là gì

Trang HTML tĩnh hiển thị hồ sơ của 27 Young Talent CYTP 2025 (6 Super Star, 21 Rising Star). PD/PM dùng trang để xem hồ sơ trước khi chọn Young Talent cho dự án. Việc chọn được ghi vào file Excel trên SharePoint, qua nút "Lựa chọn Young Talent TẠI ĐÂY" ở header.

- Link chính: https://cytp25.vercel.app
- Tài liệu mật, chỉ lưu hành nội bộ. Trang có thẻ `noindex, nofollow` để Google không lập chỉ mục.

## 2. Tình trạng hiện tại

Đã launch. Mọi thay đổi đã merge vào `main` qua PR #1 đến #6 và đang chạy trên production.

| PR | Nội dung |
|---|---|
| #1 | Sửa ảnh: đổi tên thành `photos/ss01.png`…`rs21.png`, nén từ khoảng 25MB xuống 1.2MB |
| #2 | Brand refresh (xem mục 5) và bổ sung dữ liệu còn thiếu từ file Excel đối chiếu. Highlight mảng Xây dựng/Cơ điện, thêm ghi chú xem video bằng Edge, gộp "Mong muốn làm việc" vào "Định hướng nghề nghiệp" |
| #3 | Link video SharePoint cho 6 Super Star |
| #4 | Nút "Lựa chọn Young Talent TẠI ĐÂY" ở header, mở file Excel SharePoint |
| #5 | Favicon là logo rút gọn Coteccons (chữ C) |
| #6 | Chuyển "Kinh nghiệm làm việc" lên thẻ thông tin cá nhân |

## 3. Cấu trúc thư mục

```
cytp25/
├── index.html          # toàn bộ trang: CSS, dữ liệu và JS trong 1 file
├── photos/             # ss01.png … ss06.png, rs01.png … rs21.png (600px)
├── assets/
│   ├── logo-coteccons.svg   # wordmark trắng, chữ N màu teal (lấy từ file logo 2026)
│   ├── favicon.svg          # chữ C navy, tự chuyển trắng khi trình duyệt để dark mode
│   ├── favicon-32.png
│   └── apple-touch-icon.png # 180px, nền trắng
└── review/index.html   # trang cũ "Review: Planning vs. Thực tế", không liên quan, giữ nguyên
```

File handoff này nằm ở gốc repo, ngoài `cytp25/`, nên không bị Vercel publish lên web.

## 4. Dữ liệu

Toàn bộ dữ liệu nằm trong mảng `const C=[...]` của `index.html`, mỗi Young Talent là một object:

| Trường | Ý nghĩa |
|---|---|
| `id`, `grp`, `name` | Mã (SS01/RS01…), nhóm (SUPER STAR / RISING STAR), họ tên |
| `dob`, `sex`, `field` | Năm sinh, giới tính, mảng (Xây dựng / Cơ điện) |
| `school`, `fac`, `major`, `onboard` | Trường, khoa, ngành học, thời gian onboard |
| `video` | Link video SharePoint (chỉ có ở Super Star) |
| `nv1`, `nv2` | Nguyện vọng dự án `{p: dự án, r: vị trí}`; để trống nếu chưa đăng ký |
| `exp` | Mảng các dòng kinh nghiệm làm việc |
| `str`, `weak`, `career`, `wish`, `commit` | Điểm mạnh, điểm cần cải thiện, định hướng nghề nghiệp, mong muốn làm việc (gộp chung vào Định hướng), cam kết |
| `peer` | Peer assessment |
| `bgk` | Ghi chú V3.2 từ BGK, giữ nguyên văn |
| `gpa`, `eng` | Thành tích học tập (dạng "x/4.0"), tiếng Anh |
| `cog`, `v`, `l`, `n` | Điểm V2: Cognitive overall, Verbal, Logical, Numerical |
| `r31`, `r32` | Điểm V3.1 và V3.2 theo từng tiêu chí (thang 1–3) |

Nội dung 2 chuyên đề đào tạo nằm trong `const DAOTAO`, dùng chung cho mọi hồ sơ.

Nguồn dữ liệu: file `CYTP2025_Doi_chieu_du_lieu.xlsx`, sheet "Du lieu dang dung". 180 ô tô vàng là các ô trước đây còn trống, đã được bổ sung.

**Các điểm còn mở về dữ liệu:**
- 6 bạn chưa có điểm tiếng Anh nên trang hiển thị "—": RS03, RS04, RS08, RS12, RS18, RS21.
- RS03 có điểm V2 thấp bất thường (12 / 10 / 5 / 73). Nên đối chiếu lại với dữ liệu gốc.
- Lỗi chính tả trong nội dung ứng viên và BGK được giữ nguyên văn theo yêu cầu.

## 5. Bố cục và brand

- Header: logo Coteccons, eyebrow "Coteccons Young Talent Program · Batch 2025", tiêu đề "Hồ sơ Young Talent", nút CTA teal bên phải.
- Cột trái: danh sách chỉ hiện mã và tên, có ô tìm kiếm và bộ lọc nhóm/mảng.
- Thẻ cá nhân: ảnh, tên, mảng (chip navy), năm sinh/giới tính, 4 ô học vấn và onboard, kinh nghiệm làm việc, nút video (Super Star).
- Mục (1) Nguyện vọng: nguyện vọng dự án, điểm mạnh/cải thiện, định hướng nghề nghiệp, cam kết.
- Mục (2) Thông tin Đào tạo: peer assessment, nội dung đào tạo.
- Mục (3) Thông tin Tuyển dụng: ghi chú BGK, kết quả đánh giá.
- Footer: "Tài liệu mật — Chỉ lưu hành nội bộ · Confidential & Proprietary" và "Được xây dựng bởi Phòng Đào tạo và Phát triển Tổ chức — Coteccons © 2026".
- Chiều rộng tối đa 1180px, có responsive cho điện thoại (≤600px).

Màu:

| Biến | Mã | Dùng cho |
|---|---|---|
| navy | `#16315E` | màu chủ đạo |
| `--ss` / `--ss-d` | `#5FD1C1` / `#2E9E8D` | Super Star (teal) |
| `--rs` / `--rs-d` | `#1D50A3` / `#163F82` | Rising Star (PANTONE 2728C, theo file logo 2026) |

## 6. Deploy (Vercel)

- Project `ctd-cytp25`, team `nhmaianh`, Root Directory = `cytp25`.
- Merge vào `main` sẽ cập nhật production (cytp25.vercel.app) sau khoảng 1 phút.
- Mỗi lần push lên nhánh khác, Vercel tạo một bản preview. Link preview của nhánh hiện tại: https://ctd-cytp25-git-claude-epic-clarke-ekm1df-nhmaianh.vercel.app/
- Bảo vệ truy cập: Vercel Authentication ở chế độ "all except custom domains", không đặt mật khẩu. Nên mở link production bằng tab ẩn danh để kiểm tra người ngoài có vào được không. Nếu cần khoá chặt hơn, bật Password Protection hoặc chuyển hẳn lên SharePoint.

## 7. Cách sửa thường gặp

- **Sửa nội dung một hồ sơ:** tìm object theo `id` trong `const C` rồi sửa trường tương ứng. Nhớ escape dấu ngoặc kép.
- **Đổi link video:** sửa trường `video` của SS01–SS06.
- **Đổi ảnh:** thay file `photos/<id viết thường>.png`. Nên dùng ảnh khoảng 600px, dạng chân dung.
- **Đổi link Excel lựa chọn:** sửa `href` của thẻ `<a class="cta">` trong header.
- **Kiểm tra trước khi merge:** mở `index.html` trên máy (hoặc link preview), bấm qua vài hồ sơ và mở Console (F12) để xem có lỗi JS không.

## 8. Việc còn mở

- [ ] Kiểm tra quyền truy cập production bằng tab ẩn danh (mục 6).
- [ ] Bổ sung điểm tiếng Anh cho 6 bạn và xác minh điểm V2 của RS03 (mục 4).
- [ ] Cân nhắc đổi phụ đề mục (1) từ "chia sẻ của chính ứng viên" thành "chia sẻ của Young Talent" cho thống nhất cách gọi (chưa chốt).
- [ ] Form lựa chọn PD/PM là file riêng (Excel SharePoint), không nằm trong repo này.
