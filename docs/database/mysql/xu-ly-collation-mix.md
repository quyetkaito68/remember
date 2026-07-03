- kinh nghiệm xử lý collation
- trường hợp procedure chạy lần đầu khi tạo dữ liệu mới thì bị lỗi mix collation nhưng khi cầm chính procedure đó chạy lại vào database thì lại hết lỗi
- nghi ngờ: nguyên nhân do collation_connection, character_set_connection: vì hai thằng này không ăn theo config mặc định của server mà ăn theo client kết nối, khi create database và khi chạy lại bằng tay thì lúc này đã khác nhau về character_set_collation rồi
- biến tự định nghĩa và kiểu dữ liệu text
+ biến tự định nghĩa trong procedure
set @v_ReportID = 'InInventoryItem'; => ko ăn theo collation_connection được set mà ăn theo collation_connection mặc định của bộ mã character_set_client => ví dụ utf8mb4 là utf8mb4_0900_ai_ci;

Biến user-defined (@v_ReportID) không có collation cố định ngay từ đầu.
Khi gán giá trị 'InInventoryItem' cho @v_ReportID, MySQL sẽ gán cho nó một collation mặc định dựa trên character_set_connection hiện tại.
Nếu ReportID trong bảng report_list có collation khác với @v_ReportID, MySQL có thể tự động ép kiểu hoặc gây lỗi (trong một số chế độ strict).

-- để ý trong các script có script nào set character_set_connection về utf8mb4 hay không, nếu chỉ set character_set_connection về utf8mb4 thì khi đó collation_connection sẽ ăn theo mặc định của utf8mb4 => tức là về utf8mb4_0900_ai_ci chứ ko phải as_ci => do đó khi gán thì phải gán theo cặp. Gán cả utf8mb4 và collation_connection về utf8mb4_0900_as_ci luôn.

SET character_set_connection = 'utf8mb4';
SELECT @@collation_connection; => trả ra kết quả là 0900_ai_ci

SET character_set_connection = 'utf8mb4', collation_connection = 'utf8mb4_0900_as_ci';
SELECT @@collation_connection; => trả ra kết quả là 0900_as_ci

- việc set character set trong connectionString cũng sẽ xảy ra tình trạng đổi collation_connection về mặc định của character_set đó => cần xử lý sau khi tạo connection => có thể chạy lệnh set lại collation_connection luôn.

*** dữ liệu kiểu TEXT
- không kế thừa collation của bảng, trong khi VARCHAR thì có.
- kế thừa collation của session khi có lệnh thay đổi collation trước đó
- khi bạn không chỉ định COLLATE cho cột TEXT, MySQL sẽ sử dụng collation mặc định của character_set_connection, có thể khác với VARCHAR.


