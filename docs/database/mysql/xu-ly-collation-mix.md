---
title: Xử lý collation hỗn hợp trong MySQL
description: Nguyên nhân, chẩn đoán và cách xử lý khi gặp tình trạng mix collation (connection/session, biến user-defined, TEXT vs VARCHAR).
tags: [mysql, collation, connection, text, varchar]
category: database
order: 11
updated: 2026-07-04
---

# Xử lý mix collation trong MySQL

Trang này ghi lại kinh nghiệm xử lý các vấn đề liên quan đến collation khi:
- Tạo data bằng stored procedure (procedure) lần đầu gặp lỗi, nhưng chạy lại thì lỗi biến mất.
- Có sự khác nhau giữa `collation_connection` / `character_set_connection` và collation của bảng hoặc cột.

## Triệu chứng

- Procedure tạo dữ liệu lần đầu báo lỗi liên quan tới so sánh/ép kiểu chuỗi.
- Chạy lại cùng procedure trong cùng database thì không còn lỗi.
- Một số cột hoặc biến (user-defined variable) có collation không khớp với bảng.

## Nguyên nhân chính

- `collation_connection` và `character_set_connection` phụ thuộc vào client/connection, không nhất thiết theo cấu hình server hoặc database mặc định.
- Biến user-defined (`@var`) không có collation cố định; khi gán chuỗi, MySQL gán collation dựa trên `character_set_connection` hiện tại.
- Kiểu dữ liệu `TEXT` không tự động kế thừa collation của bảng như `VARCHAR`; nếu không chỉ định `COLLATE`, `TEXT` sẽ dùng `character_set_connection` tại thời điểm gán.

## Chẩn đoán nhanh

1. Kiểm tra giá trị kết nối hiện tại:

```sql
SELECT @@character_set_connection, @@collation_connection;
```

2. Tìm các bảng/cột không dùng collation chuẩn (tham khảo trang "Kiểm tra Collation MySQL"):

```sql
-- ví dụ: tìm bảng và cột không dùng utf8mb4_0900_as_ci
-- (sử dụng truy vấn từ trang kiểm tra collation)
```

3. Kiểm tra trong script/procedure có lệnh `SET character_set_connection` hoặc thiết lập từ connection string không.

## Vấn đề với biến user-defined

- Ví dụ:

```sql
SET @v_ReportID = 'InInventoryItem';
```

Khi gán như trên, `@v_ReportID` sẽ nhận collation dựa trên `character_set_connection` đang hoạt động. Nếu cột `ReportID` trong bảng `report_list` có collation khác, thao tác so sánh/insert có thể gây lỗi hoặc implicit coercion.

Giải pháp:

- Thiết lập rõ `character_set_connection` và `collation_connection` trước khi chạy script/procedure:

```sql
SET character_set_connection = 'utf8mb4',
		collation_connection = 'utf8mb4_0900_as_ci';
```

- Hoặc chỉ định COLLATE khi so sánh/gán:

```sql
-- ép COLLATE cho biến hoặc chuỗi tạm
SET @v_ReportID = CONVERT('InInventoryItem' USING utf8mb4) COLLATE utf8mb4_0900_as_ci;
```

## TEXT vs VARCHAR

- `VARCHAR` thường kế thừa collation của cột/bảng khi tạo.
- `TEXT` nếu không chỉ định `COLLATE` sẽ lấy `character_set_connection` tại thời điểm gán giá trị.
- Do đó, khi hệ thống dùng nhiều nguồn/connection khác nhau, `TEXT` dễ bị mismatch hơn.

## Các bước xử lý thực tế

1. Trước khi chạy migration/procedure: đặt session charset/collation rõ ràng.

```sql
SET character_set_connection = 'utf8mb4',
		collation_connection = 'utf8mb4_0900_as_ci';
```

2. Nếu cần chuẩn hóa toàn bộ bảng về collation chuẩn:

```sql
ALTER TABLE table_name CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
```

3. Đổi từng cột (khi cần giữ một vài cột riêng biệt):

```sql
ALTER TABLE table_name MODIFY column_name VARCHAR(255)
	CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
```

4. Với `TEXT` nếu muốn an toàn, thêm `COLLATE` trong định nghĩa hoặc dùng `CONVERT` khi gán.

5. Luôn sao lưu trước khi thay đổi collation/index.

## Lưu ý

- Việc đổi collation có thể ảnh hưởng đến index và sắp xếp, nên kiểm tra performance sau khi chuyển.
- Đối với ứng dụng, đảm bảo connection string/ORM cấu hình charset/collation nhất quán.

## biến tự định nghĩa trong procedure
set @v_ReportID = 'InInventoryItem'; => ko ăn theo collation_connection được set mà ăn theo collation_connection mặc định của bộ mã character_set_client => ví dụ utf8mb4 là utf8mb4_0900_ai_ci;

Biến user-defined (@v_ReportID) không có collation cố định ngay từ đầu.
Khi gán giá trị 'InInventoryItem' cho @v_ReportID, MySQL sẽ gán cho nó một collation mặc định dựa trên character_set_connection hiện tại.
Nếu ReportID trong bảng report_list có collation khác với @v_ReportID, MySQL có thể tự động ép kiểu hoặc gây lỗi (trong một số chế độ strict).

## set characterset mà không set kèm collation => nguyên nhân chính gây lỗi

 để ý trong các script có script nào set character_set_connection về utf8mb4 hay không, nếu chỉ set character_set_connection về utf8mb4 thì khi đó collation_connection sẽ ăn theo mặc định của utf8mb4 => tức là về utf8mb4_0900_ai_ci chứ ko phải as_ci => do đó khi gán thì phải gán theo cặp. Gán cả utf8mb4 và collation_connection về utf8mb4_0900_as_ci luôn.

```
SET character_set_connection = 'utf8mb4';
SELECT @@collation_connection; => trả ra kết quả là 0900_ai_ci

SET character_set_connection = 'utf8mb4', collation_connection = 'utf8mb4_0900_as_ci';
SELECT @@collation_connection; => trả ra kết quả là 0900_as_ci
```

- việc set character set trong connectionString cũng sẽ xảy ra tình trạng đổi collation_connection về mặc định của character_set đó => cần xử lý sau khi tạo connection => có thể chạy lệnh set lại collation_connection luôn.

## Dữ liệu kiểu TEXT
- không kế thừa collation của bảng, trong khi VARCHAR thì có.
- kế thừa collation của session khi có lệnh thay đổi collation trước đó
- khi bạn không chỉ định COLLATE cho cột TEXT, MySQL sẽ sử dụng collation mặc định của character_set_connection, có thể khác với VARCHAR.


