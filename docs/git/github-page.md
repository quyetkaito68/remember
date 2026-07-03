# Triển khai ứng dụng React + Vite lên GitHub Pages

## 1. Mục tiêu

Tài liệu này hướng dẫn triển khai ứng dụng React + TypeScript + Vite lên GitHub Pages theo hướng hiện đại, đơn giản và dễ bảo trì.

Công nghệ sử dụng:

* React
* TypeScript
* Vite
* React Router
* GitHub Pages
* GitHub Actions (CI/CD)

Mô hình triển khai:

* Static Hosting
* Không Backend
* Không Database
* Không Server riêng

---

## 2. Điều kiện cần

## Kiểm tra Node.js

Khuyến nghị sử dụng:

```bash
node -v
```

Phiên bản:

```text
>= 22.x
```

## Kiểm tra Git

```bash
git --version
```

## Tài khoản GitHub

Đăng ký hoặc đăng nhập:

https://github.com

---

## 3. Tạo Repository

Ví dụ:

```text
dev-toolbox
```

URL repository:

```text
https://github.com/<username>/dev-toolbox
```

Ví dụ:

```text
https://github.com/quyetkaito/dev-toolbox
```

---

## 4. Khởi tạo project

Tạo project React + TypeScript bằng Vite:

```bash
npm create vite@latest dev-toolbox -- --template react-ts
```

Di chuyển vào thư mục dự án:

```bash
cd dev-toolbox
```

Cài đặt package:

```bash
npm install
```

Khởi chạy môi trường phát triển:

```bash
npm run dev
```

Mặc định:

```text
http://localhost:5173
```

---

## 5. Cấu hình Vite cho GitHub Pages

Mở file:

```text
vite.config.ts
```

Cấu hình:

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/dev-toolbox/",
});
```

Lưu ý:

Giá trị `base` phải trùng với tên repository.

Ví dụ:

Repository:

```text
dev-toolbox
```

Thì:

```ts
base: "/dev-toolbox/"
```

Nếu sau này đổi tên repository thì phải cập nhật lại giá trị này.

---

## 6. Cấu hình React Router

GitHub Pages không hỗ trợ Server Side Routing.

Không sử dụng:

```tsx
createBrowserRouter()
```

Nên sử dụng:

```tsx
createHashRouter()
```

Ví dụ:

```tsx
import { createHashRouter } from "react-router-dom";

export const router = createHashRouter([
  {
    path: "/",
    element: <App />
  }
]);
```

Khi đó URL sẽ có dạng:

```text
https://username.github.io/dev-toolbox/#/json
```

Điều này giúp tránh lỗi 404 khi refresh trang.

---

## 7. Tạo file .gitignore

Tạo file:

```text
.gitignore
```

Nội dung:

```gitignore
node_modules
dist
.vscode
.idea
.env
.env.local
.DS_Store
```

---

## 8. Khởi tạo Git

Khởi tạo repository local:

```bash
git init
```

Thêm toàn bộ source:

```bash
git add .
```

Commit đầu tiên:

```bash
git commit -m "Initial commit"
```

Đặt branch chính:

```bash
git branch -M main
```

Kết nối GitHub:

```bash
git remote add origin https://github.com/<username>/dev-toolbox.git
```

Push source code:

```bash
git push -u origin main
```

---

## 9. Thiết lập GitHub Actions

Khuyến nghị sử dụng GitHub Actions thay vì package `gh-pages`.

Tạo thư mục:

```text
.github/workflows
```

Tạo file:

```text
.github/workflows/deploy.yml
```

Nội dung:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout source
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Build application
        run: npm run build

      - name: Upload build artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

  deploy:
    needs: build

    runs-on: ubuntu-latest

    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}

    permissions:
      pages: write
      id-token: write

    steps:
      - name: Deploy
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## 10. Bật GitHub Pages

Truy cập:

```text
Repository
→ Settings
→ Pages
```

Tại mục:

```text
Build and deployment
```

Chọn:

```text
Source: GitHub Actions
```

Lưu cấu hình.

---

## 11. Thực hiện triển khai

Mỗi khi có thay đổi:

```bash
git add .
git commit -m "Thêm tính năng mới"
git push
```

GitHub Actions sẽ tự động:

1. Build ứng dụng
2. Sinh thư mục dist
3. Triển khai lên GitHub Pages

Không cần chạy lệnh deploy thủ công.

---

## 12. Kiểm tra kết quả

Sau khi workflow hoàn thành:

```text
https://<username>.github.io/dev-toolbox/
```

Ví dụ:

```text
https://quyetkaito.github.io/dev-toolbox/
```

Lần deploy đầu tiên thường mất từ 1 đến 5 phút.

---

## 13. Kiểm tra build trước khi push

Khuyến nghị luôn kiểm tra local:

```bash
npm run build
```

Nếu build thành công sẽ sinh thư mục:

```text
dist/
```

Kiểm tra bản build:

```bash
npm run preview
```

---

## 14. Quy trình làm việc khuyến nghị

## Phát triển

```bash
npm run dev
```

## Kiểm tra build

```bash
npm run build
```

## Commit

```bash
git add .
git commit -m "Mô tả thay đổi"
```

## Push

```bash
git push
```

## Deploy

GitHub Actions tự động triển khai.

---

## 15. Các lỗi thường gặp

## Trang trắng sau khi deploy

Nguyên nhân:

```ts
base
```

không đúng.

Kiểm tra lại:

```ts
base: "/dev-toolbox/"
```

---

## Refresh bị lỗi 404

Nguyên nhân:

```tsx
createBrowserRouter()
```

Giải pháp:

```tsx
createHashRouter()
```

---

## CSS hoặc JS không tải được

Nguyên nhân:

```ts
base
```

không khớp tên repository.

---

## Deploy thành công nhưng website chưa cập nhật

Nguyên nhân:

Cache trình duyệt.

Thử:

```text
Ctrl + F5
```

hoặc mở tab ẩn danh.

---

## 16. Checklist trước khi phát hành

* Project sử dụng React + TypeScript
* Sử dụng Vite
* npm run build thành công
* Đã cấu hình base trong vite.config.ts
* Đã cấu hình Hash Router
* Đã bật GitHub Pages
* Đã tạo GitHub Actions workflow
* Website truy cập được từ GitHub Pages
* Không có lỗi Console
* Hoạt động tốt trên Mobile

---

## 17. Kiến trúc triển khai khuyến nghị

Đối với dự án Dev Toolbox:

```text
React
├── TypeScript
├── Vite
├── TailwindCSS
├── React Router (Hash Router)
├── GitHub Actions
└── GitHub Pages
```

Mô hình này phù hợp cho:

* Công cụ dành cho lập trình viên
* Utility tools
* Dashboard nội bộ
* SPA tĩnh
* Dự án cá nhân
* Dự án mã nguồn mở
* Triển khai miễn phí trên GitHub

```
```
