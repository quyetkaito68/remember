---
title: NPM Version Ranges
description: "Cách đọc Semantic Versioning, hiểu version range trong package.json và kiểm soát phiên bản npm thực sự cài"
tags: [nodejs, npm, semver, package-json, package-lock]
category: developer
updated: 2026-10-23
order: 2
---

# NPM Version Ranges

`package.json` thường khai báo một **khoảng phiên bản được chấp nhận**; `package-lock.json` ghi lại phiên bản cụ thể đã được resolve cho cây dependency.

## Đọc phiên bản

```text
1.2.6
│ │ └── PATCH: sửa lỗi tương thích
│ └──── MINOR: thêm tính năng tương thích ngược
└────── MAJOR: thay đổi có thể phá vỡ tương thích
```

Đây là quy ước Semantic Versioning (SemVer), không phải bảo đảm rằng mọi package luôn tuân thủ đúng. Kiểm tra release notes và peer dependency trước khi nâng phiên bản có rủi ro.

## Các range thường gặp

| Khai báo | Range được chấp nhận | Ý nghĩa |
|----------|----------------------|---------|
| `1.2.6` | Chỉ `1.2.6` | Exact version |
| `^1.2.6` | `>=1.2.6 <2.0.0` | Cho phép thay đổi tương thích theo SemVer |
| `~1.2.6` | `>=1.2.6 <1.3.0` | Cho phép cập nhật patch, giữ nguyên minor |
| `>=1.2.6 <2.0.0` | Từ `1.2.6` đến trước `2.0.0` | Range viết tường minh |
| `1.2.x` | `>=1.2.0 <1.3.0` | Bất kỳ patch nào trong minor `1.2` |
| `*` | Mọi phiên bản phù hợp | Thường không nên dùng cho dependency ứng dụng |

Với phiên bản bắt đầu bằng `0`, dấu `^` có phạm vi hẹp hơn vì major `0` chưa cam kết ổn định:

| Range | Tương đương |
|-------|-------------|
| `^0.2.6` | `>=0.2.6 <0.3.0` |
| `^0.0.6` | `>=0.0.6 <0.0.7` |

```text
^1.2.6  → có thể lên 1.9.0, không lên 2.0.0
~1.2.6  → có thể lên 1.2.99, không lên 1.3.0
1.2.6   → không tự nhận phiên bản mới hơn
```

## npm cài phiên bản nào?

```text
package.json: range được chấp nhận
        │
        ├── package-lock.json có bản resolve phù hợp?
        │       └── npm install dùng lockfile để giữ cây phiên bản đã khóa
        │
        └── chưa có lockfile / cần resolve lại
                └── npm chọn phiên bản phù hợp với range và dependency tree
```

- Range trong `package.json` **không nhất thiết là** phiên bản nằm trong `node_modules`.
- `package-lock.json` ghi phiên bản cụ thể của dependency trực tiếp và bắc cầu để các lần cài nhất quán hơn.
- `npm install` dùng lockfile hiện có nếu phù hợp với manifest; thay đổi manifest hoặc resolve lại có thể cập nhật lockfile.
- `npm update` tìm phiên bản mới hơn nhưng vẫn nằm trong range khai báo, rồi cập nhật lockfile.
- Lockfile giúp tái lập cây dependency, nhưng không thay thế việc kiểm tra tương thích của package, Node.js hoặc môi trường hệ thống.

## Exact version và dấu `^` mặc định

```bash
npm install lodash@1.2.6
```

Lệnh chỉ định phiên bản để cài, nhưng npm mặc định thường ghi range có prefix `^` vào `package.json` (`save-prefix`). Để ghi phiên bản exact:

```bash
npm install lodash@1.2.6 --save-exact
```

Hoặc đặt cấu hình cho dự án trong `.npmrc`:

```ini
save-exact=true
```

`--save-exact` khóa trực tiếp dependency trong manifest, nhưng để tái lập toàn bộ cây cài đặt vẫn cần commit `package-lock.json`; dependency bắc cầu cũng có thể thay đổi nếu không được khóa.

## Kiểm tra phiên bản

```bash
npm ls <package>             # Phiên bản đang có trong cây cài đặt
npm view <package> versions  # Các phiên bản có trên registry
npm outdated                 # Phiên bản hiện tại, được yêu cầu, mới nhất
npm config get save-prefix   # Prefix npm dùng khi ghi version mới
```

## Quy trình nâng dependency

1. Xem `npm outdated` và xác định package nào cần nâng.
2. Kiểm tra range hiện tại, release notes, `engines` và `peerDependencies`.
3. Nâng từng nhóm có liên quan; tránh cập nhật hàng loạt khi đang xử lý lỗi.
4. Chạy `npm install` để cập nhật manifest/lockfile theo chủ đích.
5. Kiểm tra diff của cả `package.json` và `package-lock.json`.
6. Chạy test/build, sau đó xác nhận phiên bản thực tế bằng `npm ls <package>`.

Xem thêm [NPM Dependencies](./dependencies.md) để phân biệt loại dependency và xử lý lỗi resolve khi cài đặt.
