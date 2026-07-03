# 📘 Network & Internet Cơ Bản

## 1. Internet là gì?

Internet là mạng lưới kết nối hàng tỷ thiết bị trên toàn thế giới để trao đổi dữ liệu.

**Ví dụ:** 
Khi bạn mở Facebook, dữ liệu từ điện thoại của bạn đi qua nhiều thiết bị mạng và đến máy chủ Facebook trước khi trả về cho bạn. Quá trình này diễn ra trong vài chục mili giây.

## 2. ISP (Nhà cung cấp Internet)

ISP là công ty xây dựng và vận hành hệ thống mạng.

**Ví dụ:**
Trong Việt Nam, có các nhà cung cấp như Viettel, VNPT, và FPT Telecom. Nếu bạn đăng ký gói 300 Mbps của Viettel, họ sẽ kéo cáp quang tới nhà, cung cấp modem, cấp địa chỉ IP, và cho phép bạn kết nối Internet.

**Ví dụ khác:**
Giống như EVN bán điện, ISP bán kết nối Internet.

## 3. Luồng truy cập Internet

**Sơ đồ luồng truy cập:**
```text
PC/Điện thoại
      │
 Wi-Fi / LAN
      │
    Router
      │
 Cổng WAN
      │
      ISP
      │
 Internet
      │
 DNS -> Máy chủ
```

## 4. Modem, Router, Switch

-   📡 **Modem:** Nhận tín hiệu từ ISP và chuyển sang dạng dữ liệu cho thiết bị.
-   📶 **Router:** Chia mạng, phát Wi-Fi, và thực hiện NAT (Network Address Translation).
-   🔀 **Switch:** Mở rộng số cổng mạng LAN.

## 5. WAN và LAN

-   **WAN (Wide Area Network):** Kết nối ra ISP.
-   **LAN (Local Area Network):** Mạng nội bộ trong nhà.

## 6. Wi-Fi ≠ Internet

Wi-Fi chỉ là phương thức truyền không dây. Có Wi-Fi nhưng chưa chắc có Internet.

## 7. Địa chỉ IP

-   **Private IP:** 192.168.x.x, 10.x.x.x...
-   **Public IP:** Được ISP cấp để giao tiếp với Internet.

**Ví dụ:**
- Private IP: 192.168.1.100
- Public IP: Cung cấp bởi ISP

## 8. Default Gateway

Là địa chỉ IP của Router trong mạng nội bộ.

**Ví dụ:** 
- PC: 192.168.1.100 - Gateway: 192.168.1.1

## 9. DNS

DNS chuyển tên miền thành địa chỉ IP.

```text
google.com
     │
     ▼
142.x.x.x
```

**Ví dụ:**
Để truy cập google.com, bạn cần convert tên miền thành địa chỉ IP để thiết bị có thể truyền dữ liệu tới đúng máy chủ.

## 10. Mbps và MB/s

-   **8 bit = 1 Byte**
-   **Mbps (Megabit/s):** Tốc độ truyền data trong đơn vị Mega-bit mỗi giây.
-   **MB/s (Megabyte/s):** Tốc độ truyền data trong đơn vị Mega-byte mỗi giây.

**Ví dụ:**
- 100 Mbps ≈ 12.5 MB/s
- 300 Mbps ≈ 37.5 MB/s
- 1 Gbps ≈ 125 MB/s

## 11. Băng thông

Băng thông là khả năng truyền dữ liệu tối đa của đường truyền.

**Ví dụ:**
Để mạng hoạt động ổn định, băng thông cần phải đủ lớn để xử lý lượng dữ liệu được gửi đi và nhận lại.

## 12. Ping

Ping đo thời gian gói tin đi và về từ thiết bị đến đích.

-   **\<20ms:** Rất tốt
-   **20--50ms:** Good
-   **\>100ms:** Easier to notice latency

**Ví dụ:**
- Nếu ping gateway của bạn trả về 20 ms, đó là thời gian rất tốt.

## 13. Download / Upload

-   **Download:** Internet → Thiết bị
-   **Upload:** Thiết bị → Internet

**Ví dụ:**
Khi tải file từ Internet về thiết bị của bạn (download) hoặc gửi file từ thiết bị lên Internet (upload).

## 14. Vì sao mạng chậm?

Có nhiều nguyên nhân khiến mạng chậm:

- Wi-Fi yếu
- Dây mạng lỗi
- Router quá tải
- ISP gặp sự cố
- DNS lỗi
- Server đích chậm
- Nhiều thiết bị dùng cùng lúc

**Ví dụ:**
Nếu bạn đang chơi game và thấy mạng chậm, có thể do nhiều người dùng khác cũng đang chơi cùng lúc hoặc ISP gặp vấn đề.

## 15. Quy trình kiểm tra mạng

```text
Có IP?
 │
 ├─ Không → Kiểm tra Wi-Fi/LAN
 │
 ▼
Ping Gateway?
 │
 ├─ Không → Router hoặc kết nối nội bộ
 │
 ▼
Ping 8.8.8.8?
 │
 ├─ Không → ISP/WAN
 │
 ▼
Ping google.com?
 │
 ├─ Không → DNS
 │
 ▼
Internet hoạt động bình thường
```

Lệnh kiểm tra:

```cmd
ipconfig
ping <Default Gateway>
ping 8.8.8.8
ping google.com
```

## 16. Link Speed

Link Speed là tốc độ giữa PC và Router, không phải gói Internet.

**Ví dụ:**
- 10 Mbps ❌
- 100 Mbps ✅
- 1.0 Gbps ✅

**Ví dụ khác:**
Nếu bạn có link speed 100 Mbps, đó là tốc độ ổn định và đủ để sử dụng Internet.

## 17. QoS

QoS (Quality of Service) ưu tiên băng thông cho thiết bị quan trọng khi mạng bị nghẽn.

## 18. Thuật ngữ cần nhớ

| Thuật ngữ | Ý nghĩa |
|-----------|---------|
| Internet | Mạng toàn cầu |
| ISP | Nhà cung cấp Internet |
| Router | Điều hướng mạng |
| Modem | Kết nối ISP |
| Switch | Chia cổng LAN |
| WAN | Mạng bên ngoài |
| LAN | Mạng nội bộ |
| IP | Địa chỉ thiết bị |
| Gateway | Router của mạng |
| DNS | Phân giải tên miền |
| Ping | Độ trễ |
| Bandwidth | Băng thông |
| QoS | Ưu tiên lưu lượng |
| NAT | Chuyển IP nội bộ ra Internet |
