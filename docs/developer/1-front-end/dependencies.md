---
title: NPM Dependencies
description: "Phân biệt dependencies, devDependencies, peerDependencies và chẩn đoán lỗi cài đặt, resolve thư viện bằng npm"
tags: [nodejs, npm, dependencies, peer-dependencies, troubleshooting]
category: developer
updated: 2026-10-23
order: 1
---

# NPM Dependencies

Chọn đúng loại dependency và lần theo nguyên nhân khi `npm install` hoặc build không resolve được thư viện.

## Chọn loại dependency

| Loại | Dùng khi | Ví dụ |
|------|----------|-------|
| `dependencies` | Ứng dụng cần package khi chạy production | `express`, thư viện xử lý dữ liệu |
| `devDependencies` | Chỉ cần khi phát triển, test hoặc build | `vite`, ESLint, test runner |
| `peerDependencies` | Package là plugin/thư viện cần ứng dụng dùng chung một package host tương thích | Plugin cho React hoặc Vite |

```text
Ứng dụng cài dependency
├── dependencies       → có trong môi trường chạy production
├── devDependencies    → công cụ phát triển/build
└── peerDependencies   → yêu cầu ứng dụng cung cấp package host tương thích
```

Thêm package:

```bash
npm install <package>            # dependencies
npm install -D <package>         # devDependencies
npm install -P <package>         # dependencies, tương đương mặc định
```

`peerDependencies` thường được khai báo trong `package.json` của package được phát hành, không phải loại dependency để tùy tiện chuyển mọi package của ứng dụng sang. Với npm 7+, npm tự cài peer dependency khi có thể; nếu phiên bản peer không tương thích, npm có thể dừng với `ERESOLVE`.

```json
{
  "peerDependencies": {
    "react": "^18"
  },
  "devDependencies": {
    "react": "^18"
  }
}
```

Trong ví dụ trên, `peerDependencies` khai báo host mà consumer phải cung cấp; `devDependencies` giúp chính package phát triển và test. Có thể khai báo peer tùy chọn bằng `peerDependenciesMeta`, nhưng chỉ khi package thật sự hoạt động mà không cần peer đó.

## `npm install` và `npm ci`

| Lệnh | Mục đích | Lưu ý |
|------|----------|-------|
| `npm install` | Cài/cập nhật dependency theo `package.json` và lockfile; khi thêm package, cập nhật manifest và lockfile | Phù hợp phát triển; có thể cập nhật lockfile |
| `npm ci` | Cài sạch, chính xác theo `package-lock.json` | Dùng CI; xóa `node_modules` trước khi cài và báo lỗi nếu manifest không khớp lockfile |

Commit `package-lock.json` cùng thay đổi dependency để máy khác và CI cài cùng cây phiên bản. Trước khi xóa lockfile hoặc `node_modules`, hãy lưu lại lỗi và kiểm tra nguyên nhân; xóa lockfile có thể làm đổi nhiều phiên bản đã resolve.

## Chọn cờ xử lý peer conflict

| Lệnh | Hành vi | Khi nào dùng |
|------|---------|--------------|
| `npm install` | Áp dụng kiểm tra dependency và peer dependency mặc định | Luôn thử trước; đọc gói và phiên bản trong lỗi |
| `npm install --legacy-peer-deps` | Bỏ qua peer dependency khi dựng cây cài đặt, gần với cách npm cũ xử lý | Workaround tạm thời cho cây dependency cũ; có thể cài tổ hợp package không tương thích |
| `npm install --force` | Tắt một số bảo vệ của npm và cho phép các thao tác mà npm thường từ chối | Chỉ dùng khi đã hiểu rõ cảnh báo cụ thể; phạm vi rộng hơn, không phải cách sửa peer conflict mặc định |

Hai cờ cuối không sửa điều kiện tương thích trong `package.json`. Ưu tiên tìm phiên bản package có peer range tương thích, nâng/hạ package liên quan, hoặc sửa khai báo dependency. Nếu dự án cần cờ để cài nhất quán trên CI, truyền cùng cấu hình cho `npm ci` và các máy phát triển; có thể đặt `legacy-peer-deps=true` trong `.npmrc` của dự án, nhưng chỉ sau khi chấp nhận tradeoff.

## Chẩn đoán cài chậm

Không mặc định nguyên nhân là npm: có thể là registry/proxy, DNS/kết nối, tải binary hoặc script `postinstall`.

```bash
node --version
npm --version
npm config get registry
npm config get proxy
npm config get https-proxy
npm ping
npm install --verbose
```

1. Kiểm tra registry và proxy đang được dùng; đối chiếu với cấu hình mạng của máy.
2. Nếu chỉ một package hoặc scope bị chậm, kiểm tra registry của scope đó và thử truy vấn package trên cùng registry.
3. Nếu tải package xong nhưng đứng lâu, xem log `--verbose` để xác định package/script đang chạy.
4. Dùng `npm cache verify` để kiểm tra cache. Không xóa cache hoặc chuyển sang `--force` như bước đầu tiên.

### Cấu hình registry trong `.npmrc`

Registry mặc định áp dụng cho package không thuộc scope khác. Registry riêng được gán theo **scope** (nhóm package có tên bắt đầu bằng `@scope/`), không cấu hình registry tùy ý cho từng package không scope.

```ini
registry=https://registry.npmjs.org/
@company:registry=https://npm.company.example/
```

Package `@company/ui` sẽ lấy từ registry riêng; package thông thường sẽ lấy từ registry mặc định. `.npmrc` có thể ở cấp dự án, user hoặc global; cấu hình gần dự án hơn có thể ghi đè giá trị mặc định. Không commit token hoặc thông tin xác thực vào `.npmrc` trong repository.

## Lỗi resolve thường gặp

| Dấu hiệu | Nguyên nhân thường gặp | Hướng xử lý |
|----------|------------------------|-------------|
| `ERESOLVE unable to resolve dependency tree` | Phiên bản dependency/peer dependency không giao nhau | Đọc phần `Found` và `Could not resolve dependency`; điều chỉnh phiên bản trước khi cân nhắc `--legacy-peer-deps` |
| `ETARGET` / `No matching version found` | Version hoặc version range không tồn tại trên registry đang truy vấn | Kiểm tra tên, version, tag và registry; dùng `npm view <package> versions` |
| `E404` | Package không tồn tại ở registry đó, sai tên, hoặc package private chưa được xác thực | Kiểm tra tên/scope, registry theo scope và quyền truy cập |
| `ECONNRESET`, `ETIMEDOUT`, `ENOTFOUND` | Kết nối, DNS, proxy hoặc registry | Kiểm tra `npm config get registry`, proxy, `npm ping` và kết nối mạng |
| `Cannot find module` / `ERR_MODULE_NOT_FOUND` | Package chưa cài, import sai tên/path, hoặc dependency chỉ được khai báo ở nơi không được cài | Kiểm tra import, `package.json`, lockfile và lệnh cài; cài package trực tiếp nếu code dùng nó |
| Build báo không resolve được import | Sai đường dẫn/hoa-thường, thiếu package, hoặc cấu hình alias chưa được hỗ trợ trong build | Xác nhận file tồn tại, phân biệt hoa-thường, kiểm tra khai báo package và cấu hình bundler |

## Flow xử lý

```text
Lỗi khi install?
├── ERESOLVE → kiểm tra peer range → chỉnh phiên bản → chỉ cân nhắc legacy-peer-deps nếu cần
├── ETARGET / E404 → kiểm tra tên + version + registry/scope
└── lỗi mạng → kiểm tra proxy + registry + kết nối

Lỗi khi build?
├── kiểm tra import và đường dẫn (kể cả hoa-thường)
├── xác nhận package nằm trong package.json và lockfile
├── cài theo lockfile bằng npm ci
└── nếu vẫn lỗi → kiểm tra phiên bản Node/npm và cấu hình build
```
