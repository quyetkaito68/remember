# 🧹 Dọn dẹp AppData trên Windows (An toàn & Hiệu quả)

## 📌 Tổng quan
Thư mục AppData có thể tăng dung lượng theo thời gian do:
- Cache ứng dụng
- File tạm (temp)
- Dữ liệu còn sót lại sau khi uninstall

---

## 📁 Cấu trúc AppData

C:\Users\<user>\AppData

| Thư mục   | Mô tả                     | Nên xóa |
|----------|--------------------------|--------|
| Local    | Cache, temp              | ✅ Có thể |
| LocalLow | Dữ liệu nhẹ              | ⚠️ Cẩn thận |
| Roaming  | Config ứng dụng          | ❌ Không xóa bừa |

---

## 🔍 Bước 1: Thống kê dung lượng

### ✔ Cách 1: Tool
- Dùng phần mềm phân tích ổ đĩa (khuyến nghị)

### ✔ Cách 2: PowerShell
```powershell
Get-ChildItem "$env:LOCALAPPDATA" -Directory |
Sort-Object {
    (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
} -Descending |
Select-Object Name,
@{Name="Size(GB)";Expression={[math]::Round((
(Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum / 1GB),2)}} |
Select-Object -First 20
```

---

## 🧹 Bước 2: Phân loại dữ liệu

### ✅ Có thể xóa an toàn

#### 1. Temp
%LOCALAPPDATA%\Temp

#### 2. Cache trình duyệt
- Chrome / Edge → thư mục Cache

#### 3. App đã uninstall
AppData\Local\<AppName>  
AppData\Roaming\<AppName>

#### 4. Cache dev tools
- npm-cache
- Docker
- VSCode Cache

---

### ⚠️ Không nên xóa bừa

| Thư mục | Lý do |
|--------|------|
| Roaming\Microsoft | Config hệ thống |
| Local\Packages | App Windows |
| Roaming\Code\User | Config VSCode |

---

## 🧠 Quy tắc an toàn

- Không chắc → KHÔNG xóa
- Ưu tiên:
  - Cache
  - Temp
- App không dùng → xóa folder

---

## 🔄 Bước 3: Xóa an toàn

### ✔ Best practice
Rename → dùng thử → nếu ổn → xóa

Ví dụ:
Docker → Docker_old

---

## ⚙️ Bước 4: Tự động hóa

### Xóa temp:
```powershell
Remove-Item "$env:LOCALAPPDATA\Temp\*" -Recurse -Force
```

### Xóa file cũ hơn 7 ngày:
```powershell
Get-ChildItem "$env:LOCALAPPDATA\Temp" -Recurse |
Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) } |
Remove-Item -Force
```

---

## 🚀 Chiến lược tối ưu

1. Scan dung lượng
2. Xác định folder lớn
3. Kiểm tra thuộc app nào
4. Quyết định:
   - Còn dùng → xóa cache
   - Không dùng → xóa toàn bộ

---

## ⚡ Gợi ý (Dev)

Nên kiểm tra kỹ:
- Docker
- npm / node cache
- Chrome cache
- Temp

---

## 🎯 Kết luận

Không nên xóa toàn bộ AppData.

👉 Quy trình đúng:
Scan → Phân tích → Xóa có chọn lọc
