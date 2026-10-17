---
title: Tối Ưu Hiệu Năng Frontend
description: Checklist tối ưu tải trang, Vue, JavaScript và request API.
tags: [performance, frontend, vue]
category: developer
updated: 2026-10-17
order: 2
---

# Tối ưu hiệu năng Frontend

> Ghi chú thực hành về tải trang, Vue, JavaScript và dữ liệu API; ưu tiên đo trước khi thay đổi.

Nguồn: <a href="./BestPractice_Performance_FE.pptx.pdf" target="_blank" rel="noopener">PDF best practice hiệu năng frontend</a>.

## Flow tối ưu

```text
Đo hiện trạng
    ↓
Xác định bottleneck: tải trang | render | JavaScript | API
    ↓
Chọn thay đổi nhỏ nhất để xử lý bottleneck
    ↓
Đo lại bằng DevTools / profiler
    ↓
Kiểm tra UX và hồi quy
```

## Tải trang và component

- Tách bundle theo route/chức năng; lazy-load route hoặc component lớn, ít dùng.
- Phân tích kích thước bundle sau build; tránh gom không cần thiết vào bundle ban đầu.
- Tree-shake bằng ES modules và chỉ import phần thư viện cần dùng.
- `keep-alive` giữ state khi điều hướng nhưng dùng thêm bộ nhớ; chỉ cache màn hình cần giữ trạng thái và giới hạn bằng `include`, `exclude`, `max`.
- Tách component khi component đang đảm nhiệm nhiều việc hoặc có phần dùng chung.
- Chọn `v-if` khi nội dung ít đổi trạng thái hoặc tốn tài nguyên; chọn `v-show` khi cần bật/tắt thường xuyên.
- Không đặt `v-if` và `v-for` cùng một phần tử; lọc dữ liệu trước khi render.
- Watch đúng thuộc tính cần theo dõi; tránh deep watch nếu không cần.
- Giữ computed thuần, không dùng để tạo side effect.

## JavaScript và render

- Dùng debounce cho sự kiện cần đợi người dùng ngừng thao tác (ví dụ tìm kiếm); dùng throttle để giới hạn tần suất xử lý (ví dụ scroll).
- Tránh truy cập/thay đổi DOM lặp lại khi framework đã quản lý DOM; nếu buộc thao tác trực tiếp, quản lý vòng đời và cache reference phù hợp.
- Giảm công việc lặp không cần thiết; tính trước giá trị bất biến bên ngoài vòng lặp.
- Chỉ chạy tác vụ bất đồng bộ song song khi chúng độc lập; nếu phụ thuộc kết quả nhau thì giữ thứ tự.

```js
const [users, settings] = await Promise.all([
  loadUsers(),
  loadSettings(),
])
```

## Request và dữ liệu

- Cache dữ liệu ít thay đổi ở client khi có chiến lược hết hạn/làm mới phù hợp.
- Load on-demand cho tab chưa mở, combobox chưa tương tác và các vùng dashboard chưa hiển thị.
- Dùng server-side paging khi tập dữ liệu lớn; local paging chỉ phù hợp khi lượng dữ liệu tải về nhỏ và đã được đánh giá.
- Với combobox/danh sách lớn, cân nhắc paging hoặc virtual scroll để giới hạn dữ liệu và DOM đang hiển thị.
- Tránh duplicate request: kiểm tra đăng ký/hủy event listener và tab Network trong DevTools.
- Chỉ gửi tham số cần thiết; khi có thể, tải song song các API độc lập.
- Tác vụ lâu nên có trạng thái tiến trình rõ ràng; cân nhắc background job và kênh thông báo kết quả.

## Checklist kiểm tra

- [ ] Đã đo và xác định bottleneck trước khi tối ưu.
- [ ] Không có request trùng hoặc request chưa cần thiết.
- [ ] Bundle và component nặng chỉ tải khi cần.
- [ ] Dữ liệu trả về, tham số gửi lên và lượng DOM được giới hạn phù hợp.
- [ ] Đã so sánh trước/sau và kiểm tra UX.

Các ngưỡng số lượng bản ghi hoặc kích thước bundle trong tài liệu nguồn chỉ nên xem là gợi ý ban đầu, không phải giới hạn đúng cho mọi ứng dụng.
