---
title: 'Tổng Quan Về PAM (Privileged Access Management)'
description: 'Kiến trúc, luồng hoạt động và các giải pháp PAM dùng trong doanh nghiệp để quản lý truy cập remote vào hệ thống máy chủ'
tags: [pam, privileged-access-management, security, remote-access, devops]
category: 'system-admin'
updated: 2026-07-06
order: 3
---

# Tổng Quan Về PAM — Privileged Access Management

> **PAM** là hệ thống quản lý truy cập đặc quyền, cho phép doanh nghiệp kiểm soát, giám sát và ghi lại toàn bộ phiên làm việc remote vào hạ tầng máy chủ. Bài viết này dành cho sysadmin, DevOps và security team muốn hiểu luồng hoạt động tổng thể.

---

## Tổng quan

Trong môi trường doanh nghiệp, việc quản lý tài khoản **root / admin** trên hàng trăm máy chủ là thách thức lớn:
- Mật khẩu chia sẻ qua email, chat — không kiểm soát được.
- Không biết ai đã làm gì trên server nào vào lúc nào.
- Audit log phân tán, khó truy vấn khi có sự cố.

**PAM giải quyết**:
- Tập trung mật khẩu / khóa SSH vào một **vault** bảo mật.
- Bắt buộc phiên làm việc đi qua một **cổng kiểm soát** (gateway / jumpbox / session proxy).
- Ghi hình / ghi log toàn bộ thao tác của người dùng.
- Tự động thay đổi mật khẩu sau mỗi lần check-out / sau phiên.

---

## Kiến trúc tổng thể

```text
┌─────────────────────────────────────────────────────────────┐
│                      NGƯỜI DÙNG                             │
│  (SSH / RDP / Web Console)                                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   PAM GATEWAY (Proxy)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐ │
│  │ Auth     │  │ Session  │  │ Vault    │  │ Audit      │ │
│  │ Service  │  │ Proxy    │  │ Manager  │  │ Recorder   │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────────┘ │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              HẠ TẦNG MÁY CHỦ (Target)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐ │
│  │ Linux    │  │ Windows  │  │ Network  │  │ Database   │ │
│  │ Server   │  │ Server   │  │ Devices  │  │ Servers    │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────────┘ │
└─────────────────────────────────────────────────────────────┘

                    ┌──────────────────┐
                    │   SIEM / SOC     │
                    │  (Log forward)   │
                    └──────────────────┘
```

---

## Luồng hoạt động chi tiết

```text
┌──────────┐          ┌──────────┐          ┌──────────┐          ┌──────────┐
│  User    │          │  PAM     │          │  Vault   │          │  Target  │
│(Client)  │          │ Gateway  │          │(Secrets) │          │  Server  │
└────┬─────┘          └────┬─────┘          └────┬─────┘          └────┬─────┘
     │                     │                     │                     │
     │  1. Request Access  │                     │                     │
     │────────────────────▶│                     │                     │
     │                     │                     │                     │
     │  2. Xác thực (MFA)  │                     │                     │
     │◀────────────────────│                     │                     │
     │                     │                     │                     │
     │  3. Check-out yêu   │                     │                     │
     │    cầu mật khẩu     │                     │                     │
     │────────────────────▶│────────────────────▶│                     │
     │                     │                     │                     │
     │                     │  4. Trả secrets     │                     │
     │                     │◀────────────────────│                     │
     │                     │   (tự động inject)  │                     │
     │                     │                     │                     │
     │  5. Kết nối proxy   │                     │                     │
     │◀────────────────────│──────────────────────────────────────────▶│
     │                     │  6. Tạo session     │                     │
     │                     │  (record all I/O)   │                     │
     │                     │◀────────────────────                     │
     │                     │                     │                     │
     │  7. Làm việc        │                     │                     │
     │────────────────────▶│──────────────────────────────────────────▶│
     │                     │                     │                     │
     │  8. Kết thúc        │                     │                     │
     │────────────────────▶│────────────────────▶│                     │
     │                     │  9. Rotate secret   │                     │
     │                     │────────────────────▶│                     │
     │                     │  10. Lưu session    │                     │
     │                     │  log + recording    │                     │
     │                     │  (→ SIEM / SOC)     │                     │
     │                     │                     │                     │

```

## Các chức năng cốt lõi

### 1. Vault — Kho lưu trữ bí mật

- Lưu mật khẩu, private key, certificate, API token **mã hóa**.
- Hỗ trợ **rotation** tự động — đổi mật khẩu ngay sau khi check-out / phiên kết thúc.
- Ví dụ: `vault.cyberark.com`, AWS Secrets Manager, HashiCorp Vault.

### 2. Session Manager — Quản lý phiên

- **Session Proxy / Gateway**: Proxy SSH, RDP, HTTPS — user không thể bypass.
- **Just-In-Time (JIT)**: Cấp quyền tạm thời, thu hồi sau phiên kết thúc.
- **Multi-factor authentication (MFA)**: Bắt buộc trước khi mở phiên.

### 3. Audit & Recording — Ghi lại & kiểm toán

- **Session Recording**: Ghi video toàn bộ màn hình / thao tác (keystroke, command).
- **Log Forward**: Gửi log về SIEM (Splunk, ELK, Sentinel).
- **Alert & Block**: Phát hiện hành vi nguy hiểm (`rm -rf /`, `DROP TABLE`) → chặn / cảnh báo.

### 4. Access Policy — Chính sách truy cập

- Ai được access server nào? Khi nào? Với tài khoản nào?
- Ví dụ:
  - Dev chỉ SSH vào staging, không vào production.
  - Production chỉ access được sau 09:00-18:00 + approval từ Leader.
  - Cần 2 người approve để checkout root password.

---

## So sánh các giải pháp PAM phổ biến

| Tiêu chí | CyberArk | BeyondTrust | Delinea (Thycotic) | ManageEngine PAM360 |
|----------|----------|-------------|--------------------|---------------------|
| **Loại** | On-prem / Cloud | On-prem / Cloud | On-prem / Cloud | On-prem / Cloud |
| **Giao thức** | SSH, RDP, DB, API | SSH, RDP, VNC, DB | SSH, RDP, DB, K8s | SSH, RDP, DB |
| **Session Recording** | Có | Có | Có | Có |
| **Password Rotation** | Có | Có | Có | Có |
| **MFA hỗ trợ** | RADIUS, SAML, OTP | RADIUS, SAML, OTP | RADIUS, SAML, OTP | RADIUS, SAML, OTP |
| **SIEM Integration** | Splunk, ArcSight, ELK | Splunk, QRadar, ELK | Splunk, ArcSight | Splunk, ELK, Azure |
| **Giá (ước lượng)** | Cao nhất thị trường | Cao | Trung bình | Thấp-Cao (theo user) |
| **Độ phức tạp** | Cao (cần team vận hành) | Trung bình | Trung bình | Thấp (dễ cài) |

### CyberArk — Phù hợp doanh nghiệp lớn, banking

- Leader thị trường, bảo mật cấp cao nhất.
- Yêu cầu infrastructure riêng (PVWA, CPM, PSM, AIM).
- Hỗ trợ **On-Demand Privilege** cho DevOps / CI/CD.

### BeyondTrust — Linh hoạt, tích hợp mạnh

- Hỗ trợ nhiều giao thức và platform.
- **BeyondTrust Password Safe** + **Privileged Remote Access**.
- Tích hợp sâu với SIEM, ITSM (ServiceNow, Jira).

### Delinea (Secret Server) — Giá hợp lý, dễ triển khai

- Web UI thân thiện, ít phụ thuộc agent.
- Hỗ trợ **SSH Key Manager** cho Linux fleet.
- Tích hợp **Distributed Engine** cho multi-region.

### ManageEngine PAM360 — Giá rẻ, đủ dùng cho SME

- Nếu đã dùng ManageEngine stack (ADManager, ServiceDesk) → tích hợp sẵn.
- Bản On-prem cài trên Windows Server.
- Hỗ trợ remote access qua **Remote Access Plus**.

---

## Mô hình triển khai thực tế

```text
Doanh nghiệp vừa (200-500 servers)
─────────────────────────────────────

DMZ Network
┌─────────────────────────────────────┐
│  PAM Gateway (Linux Hardened)       │
│  - Nginx reverse proxy (HTTPS)      │
│  - SSH Proxy (custom port)          │
│  - RDP Proxy (TLS / Gateway)        │
└──────────┬──────────────────────────┘
           │
Corporate Network
┌──────────┴──────────────────────────┐
│  PAM Server (Internal)              │
│  - Vault (e.g., CyberArk Vault)     │
│  - Web Portal (check-out web UI)    │
│  - Audit DB (PostgreSQL / MSSQL)    │
│  - Session Storage (NAS / S3)       │
└──────────┬──────────────────────────┘
           │
Target Network
┌──────────┴──────────────────────────┐
│  Linux Farm ─── SSH Agent           │
│  Windows Farm ── RDP Agent          │
│  Database ────── DB Account         │
└─────────────────────────────────────┘
```

---

## Lưu ý khi triển khai

- **Network Isolation**: PAM Gateway đặt trong DMZ, Vault trong internal network.
- **High Availability**: Gateway cluster (ít nhất 2 node), Vault replica.
- **Backup**: Backup Vault DB + Session Recording ra dung lượng lớn (NAS / S3).
- **Disaster Recovery**: Có PAM standby site nếu là hệ thống quan trọng.
- **User Training**: Ai cũng phải biết process — không được phép copy password ra ngoài.
- **Compliance**: Đáp ứng SOX, PCI-DSS, ISO 27001 — audit trail phải đầy đủ.

---

## Tổng kết

PAM là lớp bảo vệ bắt buộc trong hạ tầng doanh nghiệp để kiểm soát truy cập đặc quyền. Luồng cốt lõi: **User → Xác thực (MFA) → Check-out secret → Session proxy → Record → Rotate → Audit**. Tùy quy mô và ngân sách, doanh nghiệp có thể chọn CyberArk (enterprise lớn), BeyondTrust (linh hoạt), Delinea (dễ dùng) hoặc ManageEngine (giá rẻ). Mấu chốt thành công không chỉ là sản phẩm, mà là quy trình vận hành và ý thức người dùng.

---

*Tài liệu được tạo ngày 06-07-2026 — Tổng quan về PAM trong doanh nghiệp.*
