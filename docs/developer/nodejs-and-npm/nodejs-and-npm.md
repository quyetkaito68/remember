---
title: Node.js, npm và quản lý version
description: Cài đặt Node.js, npm, quản lý nhiều version với nvm/Volta/fnm, và xử lý lỗi thường gặp
tags: [nodejs, npm, nvm, volta, fnm, cai-dat, powershell]
category: developer/nodejs-and-npm
updated: 2026-07-11
order: 1
---

# Node.js, npm và quản lý version

## Cài đặt Node.js và npm

1. Truy cập [nodejs.org](https://nodejs.org) và tải bản LTS.
2. Chạy file installer, giữ nguyên các tùy chọn mặc định.
3. Sau khi cài xong, **đóng terminal cũ** và mở lại.
4. Kiểm tra:

```bash
node -v
npm -v
```

Nếu lệnh không được nhận, nghĩa là `node` và `npm` chưa có trong **PATH** — chạy lại installer và chọn tùy chọn thêm vào PATH.

---

## Lỗi thường gặp: `UnauthorizedAccess` khi chạy npm

**Triệu chứng:**

```text
C:\Program Files\nodejs\npm.ps1 cannot be loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170
```

**Nguyên nhân:** PowerShell đang chặn chạy file `.ps1` do chính sách ExecutionPolicy ở chế độ `Restricted`.

**Giải pháp:** Mở PowerShell với quyền thông thường, chạy lệnh sau:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Sau đó thử lại `npm`.

---

## Quản lý nhiều version Node.js

Mỗi project có thể cần version Node khác nhau. Các công cụ bên dưới giúp cài nhiều version và chuyển đổi giữa chúng.

### nvm, Volta, fnm — dùng cái nào?

Đây là **3 công cụ thay thế nhau**, cùng tác dụng: cài nhiều version Node.js trên một máy. **Bạn chỉ cần chọn 1 trong 3**, không cần kết hợp.

| | nvm | fnm | Volta |
|--|-----|-----|-------|
| **Tác dụng** | Cài + chuyển version Node | Cài + chuyển version Node | Cài + chuyển version Node |
| **Auto-switch khi cd vào project** | Không (cần script hook) | Có | Có |
| **Nơi lưu version project** | `.nvmrc` | `.nvmrc` / `.node-version` | `package.json` |
| **Quản lý npm/yarn** | Không | Không | Có |
| **Tốc độ** | Chậm (shell script) | Nhanh (Rust) | Nhanh (Rust) |
| **Windows** | Cần nvm-windows | Native | Native |
| **Phù hợp** | Đã quen nvm, chủ yếu Linux/Mac | Muốn nvm nhưng nhanh + auto-switch | Team, muốn commit version vào git |

**Tóm lại:**
- Đang dùng nvm, muốn auto-switch → chuyển sang **fnm** (cú pháp giống nvm, bỏ nvm đi)
- Muốn team cùng version, version nằm trong `package.json` → cài **Volta**
- **Volta không cần nvm** — Volta thay thế hoàn toàn nvm

---

### Cách 1: nvm (cũ nhất, nhiều người dùng nhất)

[nvm](https://github.com/coreybutler/nvm-windows) (Node Version Manager) — shell script, cần chạy `nvm use` thủ công mỗi lần chuyển.

**Cài đặt nvm-windows:**

1. **Gỡ Node.js đã cài trực tiếp** (nếu có): Settings → Apps → Uninstall "Node.js", xóa folder `C:\Program Files\nodejs` nếu còn sót
2. Download `nvm-setup.exe` từ [GitHub releases](https://github.com/coreybutler/nvm-windows/releases)
3. Chạy installer, chọn NVM_HOME (`C:\Users\<user>\AppData\Roaming\nvm`) và NVM_SYMLINK (`C:\Program Files\nodejs`)
4. Mở terminal mới, kiểm tra: `nvm -v`

**Các lệnh thường dùng:**

| Lệnh | Mô tả |
|------|-------|
| `nvm install lts` | Cài bản LTS mới nhất |
| `nvm install 20.11.1` | Cài version cụ thể |
| `nvm install 22` | Cài latest trong dòng 22 |
| `nvm ls` | Liệt kê các version đã cài |
| `nvm use <version>` | Chuyển sang version đó |
| `nvm uninstall <version>` | Xóa version |

> **Lưu ý:** `nvm use` cần chạy CMD/PowerShell **với quyền Administrator** vì tạo symlink.

**Tải Node.js thủ công và thêm vào nvm:**

Nếu muốn thêm version mà không dùng `nvm install`, có thể tải zip về và đặt thủ công:

1. Vào https://nodejs.org → tải bản **`.zip`** (không phải `.msi`) cho Windows 64-bit
2. Giải nén zip vào thư mục `NVM_HOME\<version>`:

```text
C:\Users\<user>\AppData\Roaming\nvm\
├── v18.20.0\        ← giải nén zip vào đây
│   ├── node.exe
│   ├── npm
│   ├── npx
│   └── ...
├── v20.11.1\
├── v22.14.0\
└── v24.13.1\
```

3. Kiểm tra và sử dụng:

```bash
nvm ls              # sẽ thấy version vừa thêm
nvm use 18.20.0     # chuyển sang version đó
node -v             # xác nhận
```

> Tên folder phải đúng format `v<version>` (ví dụ `v18.20.0`). Nếu sai tên, nvm sẽ không nhận.

**Lỗi thường gặp với nvm:**

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-------------|-----------|
| `nvm use` không chuyển version | Còn Node.js cài sẵn ở `C:\Program Files\nodejs` | Xóa folder đó, chạy lại `nvm use` |
| Permission denied khi `nvm use` | Tạo symlink cần quyền Admin | Mở CMD/PowerShell với quyền **Administrator** |
| `nvm` command not found | PATH chưa update | Restart terminal hoặc restart Windows |
| Global npm packages mất sau khi chuyển | Packages theo từng version Node | Cài lại global packages cho version mới |

**Hạn chế:** Phải chạy `nvm use` thủ công mỗi lần chuyển project. Muốn tự động → dùng fnm hoặc Volta (bên dưới).

---

### Cách 2: fnm (nvm nhưng nhanh và auto-switch)

[fnm](https://fnm.vercel.app) (Fast Node Manager) — viết bằng Rust, nhanh hơn nvm 10-40x. Cú pháp giống nvm, hỗ trợ `.nvmrc`, và **tự chuyển khi `cd`** vào project.

**Cài đặt:**

```powershell
winget install Schniz.fnm
```

**Bật auto-switch** — thêm dòng sau vào PowerShell profile (`notepad $profile`):

```powershell
fnm env --use-on-cd | Out-String | Invoke-Expression
```

**Sử dụng:**

```bash
fnm install 20          # cài Node 20
fnm use 20              # chuyển version
echo "20" > .nvmrc     # tạo file version cho project
```

Khi `cd` vào project có `.nvmrc`, fnm tự chuyển version — không cần chạy lệnh gì thêm.

---

### Cách 3: Volta (khuyến nghị cho team)

[Volta](https://volta.sh) tự động chuyển version khi bạn `cd` vào project — **không cần `.nvmrc`, không cần shell hook**. Volta đọc version trực tiếp từ `package.json`.

> **Volta không cần nvm.** Volta là công cụ quản lý version độc lập, thay thế hoàn toàn nvm. Nếu dùng Volta thì gỡ nvm đi.

**Cài đặt:**

```powershell
winget install Volta.Volta
```

Hoặc tải từ https://volta.sh → chạy installer.

**Sử dụng:**

```bash
volta install node@20        # cài Node 20
volta pin node@20            # "gắn" version 20 vào project này
```

Lệnh `volta pin` sẽ thêm đoạn sau vào `package.json`:

```json
{
  "volta": {
    "node": "20.11.1",
    "npm": "10.2.0"
  }
}
```

Commit `package.json` lên git → mọi người trong team đều dùng chung version.

**Các lệnh Volta thường dùng:**

| Lệnh | Mô tả |
|------|-------|
| `volta install node@20` | Cài Node 20 |
| `volta install npm@10` | Cài npm 10 |
| `volta pin node@20` | Gắn version vào project |
| `volta pin npm@10` | Gắn npm version vào project |
| `volta list all` | Xem tất cả version đã cài |

**Ưu điểm Volta:**
- Tự động chuyển khi `cd` vào project — không cần `.nvmrc`, không cần shell hook
- Quản lý cả Node, npm, yarn, và global packages
- Viết bằng Rust — rất nhanh
- Cross-platform (Windows, Mac, Linux)
- Version nằm trong `package.json` → commit git được → team đồng nhất

---

## Chuyển từ nvm sang Volta / fnm

Nếu đang dùng nvm và muốn chuyển:

1. Gỡ Node.js do nvm quản lý (nvm uninstall tất cả)
2. Gỡ nvm-windows: Settings → Apps → Uninstall
3. Cài Volta hoặc fnm (chọn 1)
4. Cài lại các version Node cần dùng bằng lệnh mới
5. Nếu dùng Volta, thêm `volta pin node@<version>` vào từng project