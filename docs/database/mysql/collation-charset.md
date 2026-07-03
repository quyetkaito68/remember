Một chút về character set và collation

==============
COLLATION
==============
 Ví dụ về collation
CREATE TABLE example_table (
    column1 VARCHAR(255) COLLATE utf8mb4_0900_as_ci,
    column2 VARCHAR(255) -- This column will use the collation specified at the database or server level.
);

-- nếu cột ko được định nghĩa collate thì sẽ lấy collation_database
-- nếu collation_database ko được định nghĩa thì sẽ lấy collation_server
-- nếu 2 cột ở 2 bảng khác nhau có collate khác nhau thì khi so sánh sẽ BÁO LỖI


SHOW VARIABLES LIKE 'collation_database';
SHOW VARIABLES LIKE 'collation_server';

-- câu lệnh kiểm tra xem database này có chứa default_collation không
SELECT 
    SCHEMA_NAME,
    DEFAULT_CHARACTER_SET_NAME,
    DEFAULT_COLLATION_NAME
FROM 
    information_schema.SCHEMATA
WHERE 
    SCHEMA_NAME = 'your_database_name'; -- tên schema
	
===============
-- table thì ko có default collation, nó lấy colation của database
-- khi tạo table mà ko định nghĩa gì cho cột thì nó sẽ kế thừa của database
==============
-- Quay về 1 mối là column vì ta hay gặp lỗi so sánh giữa column và column
-- Dưới đây là câu lệnh query collation của column 

SELECT 
    COLUMN_NAME,
    COLLATION_NAME
FROM 
    information_schema.COLUMNS
WHERE 
    TABLE_SCHEMA = 'your_database_name' 
    AND TABLE_NAME = 'your_table_name' 
    AND COLUMN_NAME = 'your_column_name';

======
-- Nếu là table dạng temp hoặc table create từ json_table thì sẽ ko có default collation

CREATE TABLE your_table AS
SELECT
    j.*,
    -- Explicitly specifying collation for the column
    column1 COLLATE utf8mb4_0900_as_ci AS new_column
FROM
    json_table(your_json_column, '$[*]'
        COLUMNS (
            column1 VARCHAR(255) PATH '$.column1'
        )
    ) AS j;

-- trong trường hợp này collation của column1 được định nghĩa ở trên và nếu ko có thì sẽ lấy từ json_table config
-- tốt nhất là khi compare thì set collation chứ set ở column nhiều lúc ko ăn
-- Ví dụ: 
INSERT INTO pr_purchase_order_detail_plan(ID, PlanID, PlanDetailID, PurchaseOrderDetailID, Quantity)
	select
   	  uuid(),
   	  t.PlanID,
   	  t.PlanDetailID,
   	  ppod.PurchaseOrderDetailID ,
   	  t.Quantity
    FROM pr_purchase_order_detail ppod,
         JSON_TABLE (ppod.PlanListID, '$[*]' COLUMNS (
         PlanID char(36)  PATH '$.PlanID',
         PlanDetailID char(36) PATH '$.PlanDetailID',
         Quantity decimal(24,10)  PATH '$.Quantity'
   )) AS t  
   where (SELECT 1 FROM pr_purchase_order_detail_plan WHERE PlanID COLLATE utf8mb4_0900_as_ci = t.PlanID COLLATE utf8mb4_0900_as_ci and PlanDetailID COLLATE utf8mb4_0900_as_ci = t.PlanDetailID COLLATE utf8mb4_0900_as_ci 
   and PurchaseOrderDetailID COLLATE utf8mb4_0900_as_ci = ppod.PurchaseOrderDetailID COLLATE utf8mb4_0900_as_ci) is null;
=============
CHARACTER SET
- tương tự như collation 
- nếu không chỉ định cho column thì column sẽ lấy của database
- nếu database ko chỉ định thì sẽ lấy của server
- mặc định utf8mb4 và utf8mb4_0900_ai_ci sẽ là character set và collation mặc định của server, nhưng ta có thể set khi server startup hoặc

SHOW VARIABLES LIKE 'character_set_server';
SHOW VARIABLES LIKE 'collation_server';
SHOW VARIABLES LIKE 'character_set_database';
SHOW VARIABLES LIKE 'collation_database';
================
các thuộc tính cấu hình trong mysql config : my.cnf
thông tin từ trang chủ mysql
https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_collation_server
default_collation_for_utf8mb4: chỉ nhận dc 2 giá trị: utf8mb4_0900_ai_ci, utf8mb4_general_ci
character_set_client: mặc định là utf8mb4
character_set_server: mặc định utf8mb4
collation_connection: quan trọng đối với việc so sánh chuỗi ký tự
collation_database: mặc định utf8mb4_ai_ci: chỉ nên set trong config server, ko nên set bằng commandline
The global character_set_database and collation_database system variables are deprecated; expect them to be removed in a future version of MySQL.
collation_server: mặc định utf8mb4_ai_ci, từ 8.33 nếu tự định nghĩa sẽ có cảnh báo





