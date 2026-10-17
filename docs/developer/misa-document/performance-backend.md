---
title: Tối Ưu Hiệu Năng Backend
description: Ghi chú tối ưu xử lý, truy vấn, truyền tải dữ liệu và tác vụ nền.
tags: [performance, backend, database]
category: developer
updated: 2026-10-17
order: 3
---

# Tối ưu hiệu năng Backend

> Ghi chú thực hành về phân bổ công việc, xử lý ứng dụng, database và truyền tải dữ liệu.

Nguồn: <a href="./Đảm bảo%20hiệu%20năng%20tầng%20back-end.pdf" target="_blank" rel="noopener">PDF đảm bảo hiệu năng tầng backend</a>.

## Phân bổ công việc

```text
Client
  ├─ Tính toán / hiển thị phù hợp với dữ liệu đã có
  └─ Gửi đúng dữ liệu cần xử lý
       ↓
Backend
  ├─ Kiểm tra quyền và quy tắc nghiệp vụ
  ├─ Điều phối xử lý
  └─ Chỉ lấy dữ liệu cần dùng
       ↓
Database
  └─ Lưu trữ và thực hiện truy vấn đọc / ghi
```

Database thường là nút thắt khó mở rộng hơn backend. Đừng chuyển một khối lượng lớn dữ liệu lên backend chỉ để lọc/tính toán nếu database có thể truy vấn đúng tập dữ liệu cần thiết.

## Xử lý trong ứng dụng

- Đo trước khi tối ưu vi mô. Với tập dữ liệu nhỏ, `for` và `foreach` thường không phải nút thắt; ưu tiên code dễ đọc trừ khi profiler chỉ ra vấn đề.
- Tránh lặp công việc và truy vấn cùng một thông tin nhiều lần; lưu kết quả dùng lại khi phù hợp.
- Hạn chế reflection (`PropertyInfo`) trên đường xử lý nóng; dùng API/contract tường minh khi có thể.
- Dùng async cho I/O như HTTP, database, cache. Chỉ chạy song song những công việc độc lập và giới hạn concurrency khi tải có thể tăng cao.
- Không dùng fire-and-forget thay cho xử lý nền có đảm bảo: cần nghĩ đến lỗi, retry, logging, shutdown và scope DI.
- Dùng queue/worker cho tác vụ lâu hoặc tải ghi tăng đột biến; API nhận yêu cầu, worker xử lý, client theo dõi trạng thái.
- Giải phóng stream, connection và tài nguyên disposable đúng vòng đời (`using` / `await using` khi thích hợp).

## Cache và database

- Cache dữ liệu ít thay đổi để giảm truy vấn; xác định rõ expiry, invalidation và cách chấp nhận dữ liệu cũ.
- Chỉ chọn memory cache hay distributed cache sau khi hiểu yêu cầu về chia sẻ dữ liệu, dung lượng và số instance.
- Tránh `SELECT *`; lấy đúng cột và số dòng cần dùng.
- Đẩy lọc, join và phân trang xuống database khi phù hợp; tránh lấy toàn bộ dữ liệu rồi xử lý trên ứng dụng.
- Dùng batch cho thao tác hàng loạt thay vì một round trip cho từng dòng.
- Đánh giá query plan, index và thời gian thực tế trước khi quyết định giữa ORM, SQL tường minh, view hay stored procedure.

## API và thiết kế

- Giới hạn payload: chỉ trả các trường và bản ghi cần cho màn hình/ngữ cảnh hiện tại.
- Với danh sách lớn, dùng server-side paging; có thể tách truy vấn dữ liệu trang khỏi truy vấn tổng hợp nếu số liệu tổng hợp chậm.
- Tạo request/response DTO đúng nhu cầu thay vì truyền đối tượng lớn không liên quan.
- Tách lớp theo trách nhiệm nghiệp vụ để tránh một service phụ thuộc quá nhiều thành phần.
- Giữ dependency rõ ràng; tránh biến `IServiceProvider` thành service locator chung vì làm dependency khó thấy và khó kiểm thử. Nếu resolve lazy, phải bảo toàn scope, đặc biệt với tác vụ nền.

## Checklist khi điều tra chậm

- [ ] Xác định thời gian nằm ở client, backend, database hay truyền tải.
- [ ] Kiểm tra số lượng request, query và round trip.
- [ ] Kiểm tra query plan, index, số dòng/cột đọc và lượng dữ liệu trả về.
- [ ] Tìm vòng lặp gọi I/O hoặc lặp lại cùng phép tính.
- [ ] Kiểm tra cache có invalidation; tác vụ nền có retry và quan sát lỗi.
- [ ] Đo lại bằng dữ liệu và tải gần với production.
