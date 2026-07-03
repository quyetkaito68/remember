retrieval of the rsa public key is not enabled for insecure connections
- lỗi này hiện chưa rõ nguyên nhân
- gặp 1 lần ở production: khi stop mysqld đi và switch được sang con master2 thì khi start lại master1 thì dính lỗi luôn
- khắc phục: trong máy chủ mở dbforce ra close connection đi và open lại là được

===================
Ngoài lề

- Kiểm tra xem mysql server có dùng ssl ko:
SHOW VARIABLES LIKE 'have_ssl';

- Kiểm tra xem ssl_cert là gì
SHOW VARIABLES LIKE 'ssl_cert';

==========
ngày 06/05/2024 máy chủ vật lý bị restart nên lại gặp lỗi này
- sau khi tìm hiểu thì do mysql từ version 8.3 dùng caching_sha2_password, nó cache lại publicKey
- có thể khi restart lại máy chủ thì cache này bị mất đi và ko khởi tạo được cái mới => lỗi
- khi vào máy chủ close và open lại thì tạo được public key mới nên lại vào bình thường

SHOW STATUS LIKE 'Caching_sha2_password_rsa_public_key' => lệnh kiểm tra xem có cache ko => nếu trống là lỗi

https://baotri.misa.vn/browse/TSDR-197204

