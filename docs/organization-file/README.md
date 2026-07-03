# Organization File Tool

Tự động phân loại và di chuyển file theo loại vào các thư mục đích.

## Cách dùng

**Chạy nhanh (có GUI chọn folder):**
```
organize_run.bat
```
Double-click → chọn folder → chọn chế độ (dry-run / thật) → chọn phạm vi quét (root / subfolder).

**Chạy bằng PowerShell:**
```powershell
# Mặc định dùng thư mục Downloads
.\organize.ps1

# Chỉ định folder cụ thể
.\organize.ps1 -source "C:\Users\Name\Desktop"

# Xem trước mà không di chuyển file
.\organize.ps1 -source "C:\Users\Name\Desktop" -dryRun

# Quét sâu toàn bộ subfolder
.\organize.ps1 -source "C:\Users\Name\Desktop" -recurse

# Kết hợp: xem trước + quét sâu
.\organize.ps1 -source "C:\Users\Name\Desktop" -dryRun -recurse

# Dùng config tùy chỉnh
.\organize.ps1 -source "D:\Folder" -config "D:\my-config.json"
```

## Tham số

| Tham số | Mô tả | Mặc định |
|---------|-------|---------|
| `-source` | Folder cần dọn | `%USERPROFILE%\Downloads` |
| `-config` | Đường dẫn file config | `config.json` cùng thư mục script |
| `-dryRun` | Xem trước, không di chuyển file | tắt |
| `-recurse` | Quét sâu vào subfolder | tắt |

## Cấu hình (`config.json`)

Toàn bộ quy tắc phân loại nằm trong `config.json` — chỉnh sửa ở đây để thêm loại file hoặc đổi thư mục đích, không cần chạm vào script.

```json
{
  "rules": [
    {
      "name": "Hinh anh",
      "extensions": [".jpg", ".png"],
      "destination": "F:\\Pictures"
    }
  ]
}
```

## Phân loại mặc định

| Loại | Đuôi file | Thư mục đích |
|------|-----------|--------------|
| Hình ảnh | `.jpg` `.jpeg` `.png` `.gif` `.webp` `.bmp` `.tiff` `.svg` `.heic` `.raw` | `F:\Pictures` |
| Video | `.mp4` `.mkv` `.avi` `.mov` `.wmv` `.flv` `.mpeg` `.webm` `.vob` | `F:\Videos` |
| Tài liệu | `.pdf` `.doc` `.docx` `.xls` `.xlsx` `.xlsm` `.ppt` `.pptx` `.txt` `.csv` `.odt` `.ods` `.odp` | `F:\Documents` |
| Âm thanh | `.mp3` `.wav` `.flac` `.aac` `.ogg` `.wma` `.m4a` `.alac` `.aiff` `.opus` | `F:\Audio-Music` |

File không khớp loại nào → bỏ qua, không di chuyển.

## Kết quả mẫu

```
===== KET QUA =====
  Hinh anh : 4 file
  Video    : 1 file
  Tai lieu : 3 file
  Bo qua (khong khop loai) : 4 file
  Tong da di chuyen        : 8 / 12 file
  Thoi gian xu ly          : 2 giay
```

## Ghi chú

- File trùng tên ở đích → tự động thêm timestamp: `photo_20260528143022.jpg`
- Thư mục đích tự động tạo nếu chưa tồn tại
- `-recurse` nên dùng kèm `-dryRun` để xem trước trước khi chạy thật trên folder lớn
