---
title: Hiệu Năng Database
description: Ghi chú thiết kế index, đọc execution plan và tối ưu truy vấn MySQL.
tags: [database, mysql, performance]
category: developer
updated: 2026-10-17
order: 4
---

# Hiệu năng Database

> Ghi chú thực hành về index, execution plan, truy vấn MySQL và monitoring.

Nguồn: <a href="./database-performance-tips%20(1).pdf" target="_blank" rel="noopener">PDF đảm bảo hiệu năng tầng Database</a>.

## Flow điều tra truy vấn chậm

```text
Tái hiện truy vấn với dữ liệu gần production
    ↓
EXPLAIN / EXPLAIN ANALYZE
    ↓
Kiểm tra scan, index, số rows, sort, join và thời gian thực tế
    ↓
Thay đổi truy vấn hoặc index
    ↓
Đo lại và kiểm tra ảnh hưởng đến INSERT / UPDATE / DELETE
```

`EXPLAIN` cho biết kế hoạch và ước lượng của optimizer; `EXPLAIN ANALYZE` thực thi truy vấn để cung cấp số liệu thực tế. Dùng truy vấn đại diện và cân nhắc ảnh hưởng khi chạy phân tích trên production.

## Thiết kế index

- Xem các điều kiện `WHERE`, cột `JOIN`, `ORDER BY` và truy vấn thực tế trước khi thêm index.
- Index có thể giảm scan và I/O khi đọc, nhưng tiêu tốn dung lượng và làm tăng chi phí ghi, nhất là khi cập nhật cột được index.
- Composite index hữu ích khi các cột thường được truy vấn cùng nhau. Thứ tự cột quan trọng: MySQL tận dụng index theo tiền tố từ trái sang phải.
- Chọn thứ tự dựa trên workload: cột thường xuất hiện, điều kiện equality/`IN`, độ chọn lọc và thứ tự sắp xếp.
- Rà soát index dư thừa, gồm index trùng hoặc index đơn là tiền tố của index ghép.
- Không thêm index chỉ dựa vào phỏng đoán; xác nhận plan và đo lại sau thay đổi.

## Viết truy vấn có thể dùng index

- Tránh áp function lên cột được index trong `WHERE` nếu có thể viết lại điều kiện theo khoảng giá trị. Functional index là phương án khác khi được hỗ trợ và đã đo kiểm.
- Chỉ dùng `DISTINCT`/`UNION` khi ngữ nghĩa yêu cầu loại trùng; chúng có thể cần thêm bước xử lý.
- Trả đúng dữ liệu cần: tránh `SELECT *`, giới hạn số dòng với `LIMIT` hoặc paging phù hợp.
- Ưu tiên thao tác theo tập dữ liệu (set-based) thay vì lặp từng dòng bằng cursor khi có thể biểu diễn bằng một câu SQL.
- Tính trước giá trị không đổi trong truy vấn thay vì gọi hàm không xác định lặp theo từng dòng; kiểm tra plan để xác nhận optimizer có thể dùng index.

## Đọc nhanh execution plan

| Dấu hiệu | Cần kiểm tra |
|----------|--------------|
| `ALL` / full table scan | Có cần index phù hợp hoặc truy vấn đang đọc phần lớn bảng? |
| `index` / full index scan | Có thể giới hạn dữ liệu hoặc dùng index chọn lọc hơn không? |
| Nhiều rows bị đọc | Điều kiện lọc, thứ tự cột index và độ chọn lọc có phù hợp không? |
| Sort / filesort tốn kém | `ORDER BY` có khớp index và điều kiện lọc không? |
| `key` rỗng | Vì sao optimizer không chọn index; plan và thống kê dữ liệu nói gì? |

Không xem một loại scan là lỗi tuyệt đối: nếu truy vấn cần phần lớn bảng, scan có thể là lựa chọn hợp lý. So sánh số rows, chi phí và thời gian thực tế trong đúng ngữ cảnh.

## Monitoring và checklist

Theo dõi CPU, RAM, Disk I/O, Network I/O, truy vấn chậm hoặc gọi thường xuyên, table scan đáng chú ý và index dư thừa.

- [ ] Có thể tái hiện truy vấn và tham số gây chậm không?
- [ ] Đã xem plan và so sánh estimated rows với actual rows?
- [ ] Có thể giảm rows/columns đọc hoặc round trip không?
- [ ] Index mới có cải thiện read mà không gây write/storage overhead không?
- [ ] Đã đo lại dưới workload đại diện và kiểm tra hồi quy?

Các con số benchmark trong slide nguồn phụ thuộc dữ liệu, cấu hình và môi trường; không coi là mức cải thiện bảo đảm cho hệ thống khác.
