---
title: Collation & Character Set trong MySQL
description: Tổng quan về character set và collation trong MySQL, cách kiểm tra và xử lý lỗi khi so sánh.
tags: [mysql, collation, charset, database]
updated: 2026-07-05
---

## COLLATION

Ví dụ về collation:

```sql
CREATE TABLE example_table (
    column1 VARCHAR(255) COLLATE utf8mb4_0900_as_ci,
    column2 VARCHAR(255) -- This column will use the collation specified at the database or server level.
);
```

- Nếu cột không được định nghĩa `COLLATE` thì sẽ lấy `collation_database`.
- Nếu `collation_database` không được định nghĩa thì sẽ lấy `collation_server`.
- Nếu 2 cột ở 2 bảng khác nhau có `COLLATE` khác nhau thì khi so sánh sẽ **báo lỗi**.

### Kiểm tra collation database/server

```sql
SHOW VARIABLES LIKE 'collation_database';
SHOW VARIABLES LIKE 'collation_server';

-- Kiểm tra default collation của database
SELECT
    SCHEMA_NAME,
    DEFAULT_CHARACTER_SET_NAME,
    DEFAULT_COLLATION_NAME
FROM
    information_schema.SCHEMATA
WHERE
    SCHEMA_NAME = 'your_database_name';
```

### Table & Column collation

- Table không có default collation riêng, nó lấy collation của database.
- Khi tạo table mà không định nghĩa gì cho cột thì cột sẽ kế thừa collation của database.
- Lỗi hay gặp nhất là so sánh giữa column và column.

Kiểm tra collation của column:

```sql
SELECT
    COLUMN_NAME,
    COLLATION_NAME
FROM
    information_schema.COLUMNS
WHERE
    TABLE_SCHEMA = 'your_database_name'
    AND TABLE_NAME = 'your_table_name'
    AND COLUMN_NAME = 'your_column_name';
```

### JSON_TABLE & temp table

Nếu là table dạng temp hoặc table tạo từ `JSON_TABLE` thì sẽ không có default collation.

```sql
CREATE TABLE your_table AS
SELECT
    j.*,
    column1 COLLATE utf8mb4_0900_as_ci AS new_column
FROM
    json_table(your_json_column, '$[*]'
        COLUMNS (
            column1 VARCHAR(255) PATH '$.column1'
        )
    ) AS j;
```

Trong trường hợp này collation của column được định nghĩa ở trên, nếu không có thì sẽ lấy từ `JSON_TABLE` config.

**Tốt nhất là khi compare thì set collation**, chứ set ở column nhiều lúc không ăn.

Ví dụ:

```sql
INSERT INTO pr_purchase_order_detail_plan(ID, PlanID, PlanDetailID, PurchaseOrderDetailID, Quantity)
    SELECT
        uuid(),
        t.PlanID,
        t.PlanDetailID,
        ppod.PurchaseOrderDetailID,
        t.Quantity
    FROM pr_purchase_order_detail ppod,
         JSON_TABLE (ppod.PlanListID, '$[*]' COLUMNS (
             PlanID char(36) PATH '$.PlanID',
             PlanDetailID char(36) PATH '$.PlanDetailID',
             Quantity decimal(24,10) PATH '$.Quantity'
         )) AS t
    WHERE (SELECT 1 FROM pr_purchase_order_detail_plan
           WHERE PlanID COLLATE utf8mb4_0900_as_ci = t.PlanID COLLATE utf8mb4_0900_as_ci
             AND PlanDetailID COLLATE utf8mb4_0900_as_ci = t.PlanDetailID COLLATE utf8mb4_0900_as_ci
             AND PurchaseOrderDetailID COLLATE utf8mb4_0900_as_ci = ppod.PurchaseOrderDetailID COLLATE utf8mb4_0900_as_ci
          ) IS NULL;
```

## CHARACTER SET

Tương tự như collation:

- Nếu không chỉ định cho column thì column sẽ lấy của database.
- Nếu database không chỉ định thì sẽ lấy của server.
- Mặc định `utf8mb4` và `utf8mb4_0900_ai_ci` sẽ là character set và collation mặc định của server, nhưng ta có thể set khi server startup.

```sql
SHOW VARIABLES LIKE 'character_set_server';
SHOW VARIABLES LIKE 'collation_server';
SHOW VARIABLES LIKE 'character_set_database';
SHOW VARIABLES LIKE 'collation_database';
```

## Các thuộc tính cấu hình trong my.cnf

Tham khảo: <https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_collation_server>

| Variable | Mô tả |
|----------|-------|
| `default_collation_for_utf8mb4` | Chỉ nhận 2 giá trị: `utf8mb4_0900_ai_ci`, `utf8mb4_general_ci` |
| `character_set_client` | Mặc định là `utf8mb4` |
| `character_set_server` | Mặc định `utf8mb4` |
| `collation_connection` | Quan trọng đối với việc so sánh chuỗi ký tự |
| `collation_database` | Mặc định `utf8mb4_0900_ai_ci` — chỉ nên set trong config server, không nên set bằng command line |
| `collation_server` | Mặc định `utf8mb4_0900_ai_ci` — từ 8.33 nếu tự định nghĩa sẽ có cảnh báo |

> **Note:** `character_set_database` và `collation_database` đã bị deprecate, dự kiến sẽ bị xoá trong phiên bản MySQL tương lai.
