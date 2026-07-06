---
title: 'Docker Desktop — Cấu Hình Cho Mạng Local & Registry Nội Bộ'
description: 'Hướng dẫn cài đặt, cấu hình Docker Desktop để làm việc với registry nội bộ (Harbor) trong mạng local'
tags: [docker, docker-desktop, registry, harbor, local-network]
category: 'devops/docker'
updated: 2026-07-06
order: 1
---

# Docker Desktop — Cấu Hình Cho Mạng Local & Registry Nội Bộ

> Hướng dẫn cấu hình Docker Desktop để pull/push image từ registry nội bộ (Harbor) qua HTTP, xử lý lỗi SSL tự chứng chỉ, và các lệnh thao tác thường dùng.

---

## 1. Cấu hình Docker Engine — Insecure Registries

Registry nội bộ dùng HTTP hoặc tự chứng chỉ → cần thêm vào danh sách **insecure-registries**.

Vào **Docker Desktop → Settings → Docker Engine**, thay daemon config:

```json
{
  "debug": true,
  "experimental": false,
  "insecure-registries": [
    "192.168.11.236",
    "192.168.41.44:5000",
    "192.168.101.50",
    "192.168.101.51",
    "192.168.41.109",
    "registry-harbor.misa.local"
  ],
  "registry-mirrors": []
}
```

Sau đó **Apply & Restart** để Docker reload config.

---

## 2. Đăng nhập Registry Nội Bộ

### 2.1. File cấu hình credentials (`config.json`)

```json
{
  "auths": {
    "192.168.41.109": {},
    "registry-harbor.misa.local": {
      "auth": "YWRtaW46MTIzNDU2NzhAQWJj"
    }
  }
}
```

Vị trí: `%USERPROFILE%\.docker\config.json`

### 2.2. Login bằng lệnh

```bash
docker login -u=robot@viewer -p=12345678@Abc 192.168.41.109
```

Lưu ý: Nếu gặp lỗi **access denied**, đổi từ hostname `registry-harbor.misa.local` sang IP `192.168.41.109`.

---

## 3. Build & Push Image

### Build image

```bash
# Với -f chỉ định Dockerfile
docker build -t 192.168.41.109/amisams/ui:20.0.0.0 -f Dockerfile-UI .

# Không chỉ định Dockerfile (mặc định Dockerfile ở thư mục hiện tại)
docker build --quiet -t 192.168.41.109/qtsx/syncdataworker:0.0.0.1 .
```

### Push image lên registry

```bash
docker push 192.168.41.109/amisams/ui:20.0.0.0
docker push --quiet 192.168.41.109/qtsx/asynctaskworker:0.0.0.1
```

### Xoá image local

```bash
docker rmi 192.168.41.109/qtsx/asynctaskworker:0.0.0.1
```

---

## 4. Pull & Save Image

### Pull từ registry

```bash
docker pull registry-harbor.misa.local/nginx/nginx:1.19.0-alpine
```

### Export image ra file .tar (dùng để copy sang máy khác)

```bash
docker save -o nginx_1_19_0.tar registry-harbor.misa.local/nginx/nginx:1.19.0-alpine
```

---

## 5. Lỗi Thường Gặp

### 5.1. Push timeout

```
The push refers to repository [192.168.41.109/mau/onlyoffice/documentserver]
Get "https://192.168.41.109/v2/": net/http: request canceled while waiting for connection
(Client.Timeout exceeded while awaiting headers)
```

**Nguyên nhân:** Registry chưa được thêm vào `insecure-registries`, Docker cố gắng kết nối HTTPS và timeout.

**Xử lý:** Thêm IP `192.168.41.109` vào `insecure-registries` trong Docker Engine config (xem bước 1).

### 5.2. Unauthorized

```
docker push 192.168.41.109/mau/onlyoffice/documentserver:9.0.4.1
...
unauthorized: unauthorized to access repository: mau/onlyoffice/documentserver,
action: push
```

**Nguyên nhân:** Chưa đăng nhập registry.

**Xử lý:**

```bash
docker login -u=robot@viewer -p=12345678@Abc 192.168.41.109
docker push 192.168.41.109/mau/onlyoffice/documentserver:9.0.4.1
```

---

*Tài liệu được tạo ngày 06-07-2026 — Docker Desktop với registry nội bộ.*
