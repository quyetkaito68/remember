---
title: User, Group & Permission Trên Windows
description: 'Mô hình quản lý user, group, permission trên Windows và cách phân quyền thực tế cho một máy tính dùng chung trong gia đình.'
tags: [windows, user-account, group, permission, ntfs, family]
category: 'computer/windows'
updated: 2026-07-31
order: 3
---

# User, Group & Permission Trên Windows

> Mô hình phân quyền Windows: **User → Group → Permission**. Bài viết gồm khái niệm cốt lõi, thao tác GUI/CMD và recipe phân quyền cho một máy tính gia đình dùng chung.

---

## 1. Mô hình tổng quan

```text
User (tài khoản)
  │  thuộc
  ▼
Group (nhóm)
  │  nhận
  ▼
Permission (quyền)
  │  áp lên
  ▼
Object: File / Folder / Registry / Service / Printer / Share
```

Nguyên tắc: **user nằm trong group → group được cấp quyền → quyền áp lên object**. Gán quyền cho group thay vì từng user để dễ quản lý.

Phân biệt 3 tầng quyền khác nhau:

| Tầng | Tên | Phạm vi | Ví dụ |
|------|-----|---------|-------|
| **Privilege** | Quyền hệ thống | Cả máy | Cài phần mềm, đổi giờ, tắt máy |
| **Permission (NTFS)** | Quyền trên object | File / folder | Đọc / ghi thư mục |
| **UAC** | Cửa sổ xác thực | Nâng quyền tạm thời | Admin prompt khi cài app |

---

## 2. User Account — các loại tài khoản

### Local vs Microsoft

| Tiêu chí | Local Account | Microsoft Account |
|----------|---------------|-------------------|
| Dữ liệu | Chỉ tồn tại trên máy | Sync lên cloud (settings, OneDrive...) |
| Đăng nhập | Username + password | Email + password |
| Family Safety | ❌ | ✅ (giới hạn giờ, chặn web, báo cáo) |
| Khôi phục password | Câu hỏi bảo mật | Qua email / phone |
| Phù hợp | Máy offline, dùng 1 mình | Gia đình, cần sync |

### Mức quyền của account

| Loại | Đặc quyền | Khi nào dùng |
|------|-----------|--------------|
| **Administrator** | Toàn quyền: cài app, đổi settings, xem mọi dữ liệu | 1 người quản trị (bố/mẹ) |
| **Standard User** | Chạy app, dùng printer, chỉ truy cập file của mình | Các thành viên còn lại |
| Guest (tắt mặc định) | Hạn chế tối đa, không cần password | Cho người ngoài mượn máy (khuyên tắt) |

> **Nguyên tắc:** máy gia đình chỉ nên có **1 tài khoản Admin** + các Standard còn lại. Standard user khi cần cài app sẽ nhập password Admin qua UAC — vừa chặn được, vừa biết ai đang làm gì.

---

## 3. Group — nhóm tích hợp sẵn

```text
net localgroup                    → liệt kê các nhóm
net localgroup Users              → xem thành viên nhóm Users
net localgroup Administrators     → xem ai đang là admin
```

| Group | Quyền mặc định | Ghi chú |
|-------|----------------|---------|
| **Administrators** | Toàn quyền máy | Chỉ thêm người thực sự cần |
| **Users** | Quyền chuẩn: chạy app, in ấn, không đổi settings | Standard user mặc định nằm đây |
| Power Users | ⚠️ **Vô dụng từ Windows Vista** — giữ chỉ để tương thích app cũ | Đừng dùng |
| Backup Operators | Backup / restore bỏ qua NTFS | Hiếm dùng ở gia đình |
| Remote Desktop Users | Được RDP vào máy | Tắt nếu không cần |
| Guests | Hạn chế, không có password | Mặc định tắt |

---

## 4. Permission — phân quyền NTFS

NTFS là lớp quyền chính trên file/folder của Windows.

### Các mức quyền phổ biến

| Mức | Quyền làm được |
|-----|----------------|
| **Full control** | Mọi thứ (đổi permission, xóa, đổi chủ sở hữu...) |
| **Modify** | Đọc + ghi + xóa |
| **Read & Execute** | Đọc + chạy file |
| **Read** | Chỉ xem |
| **Write** | Tạo file mới, ghi đè — không xóa được file người khác |

### 3 quy tắc vàng

```text
1. Deny luôn thắng Allow
   └── 1 quyền Deny ở bất kỳ đâu → user bị chặn, dù Allow chồng chất

2. Allow được cộng dồn
   └── Allow từ user + Allow từ mọi group user thuộc → gộp lại

3. Kế thừa (Inheritance)
   └── Thư mục con tự kế thừa quyền của thư mục cha
   └── Muốn quyền khác → tắt kế thừa rồi set lại
```

> **Quyền hiệu dụng (Effective) = tổng Allow − Deny.** Xem tại: Properties → Security → Advanced → Effective Access.

### Share permission (khi chia sẻ folder qua mạng)

Quyền khi truy cập qua mạng = **giao của NTFS và Share** (lấy cái chặt hơn). Truy cập local chỉ tính NTFS.

---

## 5. Thao tác — User

### Tạo Local Account bằng GUI (Windows 10/11)

```text
Settings → Accounts → Family & other users → Add account
  → "I don't have this person's sign-in information"
  → "Add a user without a Microsoft account"
  → nhập Username / Password / Security questions
```

> Windows 10/11 cố tình ưu tiên form Microsoft Account — phải đi qua mục "không có sign-in info" mới tạo được local. Sau khi tạo, chọn tài khoản → **Change account type** → Standard User / Administrator.

### Bằng CMD

```bash
net user Bob 123456 /add                 # tạo user + password
net user Bob /active:no                  # vô hiệu hóa (không xóa dữ liệu)
net user Bob /delete                     # xóa user
net localgroup Administrators Bob /add   # nâng lên admin
net localgroup Administrators Bob /delete # hạ xuống standard
```

> **Lưu ý:** password gõ thẳng trên command line sẽ lưu trong history cmd. Tạo qua Settings bắt buộc password + security questions — không nên để local account trống password.

---

## 6. Password Policy — quy tắc đặt mật khẩu

Admin muốn ép toàn bộ user đặt mật khẩu mạnh (tối thiểu N ký tự + có ký tự đặc biệt) → dùng **Password Policy**. Chỉ có trên Windows **Pro/Enterprise** — bản Home không có.

### GUI (Pro)

```text
Win+R → secpol.msc
  → Security Settings → Account Policies → Password Policy
```

| Policy | Giá trị cho yêu cầu "≥ N ký tự + ký tự đặc biệt" |
|--------|-------------------------------------------------|
| **Password must meet complexity requirements** | `Enabled` — mật khẩu ≥ 8 ký tự và chứa **3 trong 4** nhóm: chữ hoa, chữ thường, số, ký tự đặc biệt |
| **Minimum password length** | `N` (ví dụ 12) — nâng cứng hơn nếu cần |
| **Maximum password age** | `30` (ngày) — ép user đổi mật khẩu định kỳ |
| **Minimum password age** | `1` (ngày) — chặn user đổi ngay về mật khẩu cũ |
| **Enforce password history** | `10` — không dùng lại 10 mật khẩu gần nhất |

> Windows **không có** ô riêng "bắt buộc ký tự đặc biệt" — tính năng này gộp vào cờ *complexity requirements* (≥ 8 ký tự + 3/4 nhóm ký tự).

### CLI (chạy trên mọi bản, nhưng không đầy đủ)

```bash
net accounts
net accounts /minpwlen:12     # độ dài tối thiểu
net accounts /maxpwage:30     # hết hạn sau 30 ngày
net accounts /uniqpw:10       # không trùng 10 mật khẩu gần nhất
```

> `net accounts` **không** bật được complexity (chữ hoa / ký tự đặc biệt) — chỉ `secpol.msc` / `gpedit.msc` (Pro) làm được.

### 2 điểm cần biết

1. Policy chỉ **ép từ lần đổi mật khẩu sau** — không ép user cũ đổi ngay. Muốn ép ngay: `lusrmgr.msc` → chuột phải user → **User must change password at next logon**, hoặc Admin reset mật khẩu user.
2. Máy **Home** không có `secpol.msc` → nâng cấp Pro, hoặc chấp nhận quy ước đặt mật khẩu bằng thỏa thuận giữa các thành viên.

---

## 7. Thao tác — phân quyền thư mục

### GUI

```text
Chuột phải folder → Properties → Security → Edit
  → Add → nhập username → check Allow / Deny → OK
```

| Tình huống | Làm |
|------------|-----|
| Cấp quyền cho user / group | Check Allow ở mức cần |
| Chặn quyền | Check Deny (dùng dè — dễ rối) |
| Không muốn kế thừa quyền cha | Advanced → Disable inheritance → Copy/Remove |
| Xem ai thực sự có quyền | Advanced → Effective Access |

### CLI (icacls)

```bash
icacls D:\Shared                                       # xem ACL hiện tại
icacls D:\Shared /grant "Users:(OI)(CI)R,W"            # Allow Users đọc + ghi
icacls D:\Private /inheritance:r /grant "Admin:(OI)(CI)F" # bỏ kế thừa, chỉ admin full
```

| Flag | Ý nghĩa |
|------|---------|
| `(OI)` | Object inherit — áp cho file con |
| `(CI)` | Container inherit — áp cho thư mục con |
| `/inheritance:r` | Xóa toàn bộ quyền thừa kế |
| `F` / `M` / `R` / `W` | Full / Modify / Read / Write |

---

## 8. Case study — phân quyền máy tính gia đình

### Mô hình đề xuất

| Account | Quyền | Làm được |
|---------|-------|----------|
| **Admin** (bố/mẹ) | Administrator | Cài app, đổi settings, xem toàn bộ, cấp quyền qua UAC |
| **Con** | Standard | Chạy app đã cài sẵn, không cài app, không đổi system settings |
| **Mẹ** | Standard | Như Con + được đọc thêm `D:\Family` |

### Các bước thực hiện

1. **Tạo 1 Admin duy nhất** cho người quản lý máy.
2. **Tạo Standard cho từng thành viên** (local hoặc Microsoft).
3. **Phân vùng dữ liệu theo mức nhạy cảm**:

```text
D:\Private  → chỉ Admin
D:\Family   → cha mẹ đọc/ghi, con chỉ đọc
D:\Shared   → mọi người đọc + ghi (phim, tài liệu chung)
```

4. **Set quyền**:

```bash
# Chia sẻ chung — mọi standard user đọc + ghi
icacls D:\Shared /grant "Users:(OI)(CI)R,W"

# Thư mục gia đình — mẹ full, con chỉ đọc
icacls D:\Family /grant "Mom:(OI)(CI)F" /grant "Child1:(OI)(CI)R"

# Riêng tư — chỉ admin, bỏ kế thừa
icacls D:\Private /inheritance:r /grant "AdminPC:(OI)(CI)F"
```

5. **Test với tài khoản Con**: đăng nhập → chạy app, mở `D:\Shared`, cố cài app → phải nhập password Admin. Thử mở `D:\Private` → bị chặn.
6. (User profile `C:\Users\<tên>\` mặc định Windows **đã tự chặn** người khác truy cập — không cần làm thêm.)

## 9. Account Unknown (S-1-5-21-...) — hiện tượng & cách xử lý

> ACL (Access Control List) của folder vẫn lưu SID của một tài khoản, nhưng Windows không tìm thấy tài khoản đó nữa → hiển thị **Account Unknown (S-1-5-21-...)**.

### Hiện tượng

Trong tab **Security** của Properties thấy dòng:

```text
Account Unknown (S-1-5-21-123456789-987654321-123456789-1003)
```

Chuỗi `S-1-5-21-...` chính là **SID** (Security Identifier).

### Nguyên nhân

| Nguyên nhân | Cơ chế |
|-------------|--------|
| **Đã xóa user** *(phổ biến nhất)* | User A được cấp quyền cho folder → sau đó A bị xóa → ACL vẫn giữ SID của A |
| **Cài lại Windows** | Cùng tên `Quyet` nhưng SID đổi hoàn toàn — `S-1-5-21-1111-2222-3333-1001` → `S-1-5-21-9999-8888-7777-1001` → ACL giữ SID cũ, Windows không nhận ra |
| **Từng join Domain** | Máy từng join AD (ví dụ `DOMAIN\Alice`) → rời Domain → không hỏi được Domain Controller → chỉ còn Account Unknown |
| **Restore dữ liệu từ máy khác** | Copy nguyên ổ cứng / restore backup → ACL mang theo SID của máy cũ |

**Tra cứu SID hiện tại:**

```powershell
Get-LocalUser
wmic useraccount get name,sid
whoami /user
(Get-Acl "D:\Videos").Access     # xem toàn bộ ACE trong ACL
```

Nếu SID trong ACL không khớp với bất kỳ user nào hiện có → chính là account đã mất.

### Có xóa được không?

**Có** — account không còn tồn tại thì hoàn toàn Remove được.

**GUI:**

```text
Properties → Security → Edit → chọn Account Unknown → Remove
```

**CLI:**

```bash
icacls "D:\Videos"               # xem ACL → thấy dòng Account Unknown:(OI)(CI)(RX)
icacls "D:\Videos" /reset /T     # reset toàn bộ quyền về mặc định
```
