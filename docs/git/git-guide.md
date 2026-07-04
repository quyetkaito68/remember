---
title: Hướng dẫn sử dụng Git
description: Hướng dẫn cơ bản về Git, từ khởi tạo repository, cấu hình người dùng đến đẩy mã nguồn lên GitHub.
tags: [git, github, version-control]
category: git
updated: 2026-07-05
---

# Hướng dẫn sử dụng Git: Khởi tạo và đẩy mã nguồn lên GitHub

## 1. Khởi tạo Git trong thư mục dự án

Mở terminal/cmd tại thư mục dự án (đã có sẵn file, thư mục):

```sh
git init
```

## 2. Cấu hình thông tin người dùng (chỉ cần làm 1 lần trên máy)

Bước này có thể không cần làm, khi gõ lệnh git push thì sẽ yêu cầu đăng nhập => chuyển hướng qua xác thực với trình duyệt là xong.

```sh
git config --global user.name "Tên của bạn"
git config --global user.email "email@example.com"
```

## 3. Thêm tất cả file vào vùng staging

```sh
git add .
```

## 4. Commit lần đầu

```sh
git commit -m "Initial commit"
```

## 5. Tạo repository mới trên GitHub
- Truy cập https://github.com
- Đăng nhập và nhấn nút "New" để tạo repository mới
- Đặt tên repo, chọn Public/Private, nhấn "Create repository"

## 6. Kết nối repo local với GitHub

Thay `your-username` và `your-repo.git` bằng repo bạn vừa tạo:

```sh
git remote add origin https://github.com/your-username/your-repo.git
```

## 7. Đẩy mã nguồn lên GitHub

```sh
git branch -M main
git push -u origin main
```

---

### Lưu ý:
- Nếu repo GitHub đã có sẵn file (ví dụ: README.md), hãy pull về trước khi push:
  ```sh
  git pull origin main --allow-unrelated-histories
  ```
- Sau này chỉ cần:
  ```sh
  git add .
  git commit -m "Nội dung thay đổi"
  git push
  ```
