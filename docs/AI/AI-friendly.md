---
title: AI Friendly Technology
description: "Hướng dẫn chọn công nghệ và kiến trúc phù hợp cho sản phẩm AI-friendly"
tags: [ai, coding, architecture, agent]
category: ai
order: 2
updated: 2026-08-04
---

# AI-friendly: cách chọn công nghệ theo sản phẩm

Đây là tài liệu mô tả cách chọn công nghệ, kiến trúc và xu hướng coding với agent sao cho thân thiện với AI nhất, đồng thời tối ưu khả năng xử lý của AI.

Không nên bắt đầu bằng việc chọn ngôn ngữ trước rồi mới suy nghĩ về sản phẩm cần làm. Thay vào đó, hãy bắt đầu từ các yếu tố sau:

- Loại sản phẩm (Product Type)
- Domain / lĩnh vực nghiệp vụ
- Ecosystem hỗ trợ
- Khả năng AI hỗ trợ
- Hiệu năng

Loại sản phẩm => Hệ điều hành mục tiêu => Khả năng AI hỗ trợ => Ecosystem => Hiệu năng (nếu cần)

## Bảng lựa chọn công nghệ theo từng loại sản phẩm

| Loại sản phẩm | Công nghệ khuyến nghị | AI Support | Tốc độ phát triển | Hiệu năng | Ghi chú |
|--------------|----------------------|-----------|-------------------|-----------|---------|
| Website doanh nghiệp | TypeScript + Next.js | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Lựa chọn mặc định hiện nay |
| Dashboard/Admin | TypeScript + React + Vite | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | AI sinh UI rất tốt |
| SPA Web | React / Vue | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | React có ecosystem lớn hơn, Vue đơn giản hơn |
| Backend REST API | NestJS hoặc ASP.NET Core | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | NestJS nhanh phát triển, ASP.NET mạnh enterprise |
| GraphQL API | NestJS | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | AI hỗ trợ tốt |
| Realtime API | NestJS + Socket.IO | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Websocket rất phổ biến |
| SaaS | Next.js + NestJS | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Stack phổ biến nhất hiện nay |
| Internal Tool | React + NestJS | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | AI sinh CRUD cực nhanh |
| CMS | Next.js + PostgreSQL | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | |
| ERP/MES | ASP.NET Core | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Domain enterprise vẫn rất mạnh |
| Microservice | ASP.NET Core / NestJS / Go | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Go khi cần scale lớn |
| API Gateway | Go / ASP.NET | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Ưu tiên hiệu năng |
| Chrome Extension | TypeScript | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Manifest V3 |
| Firefox Extension | TypeScript | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Gần giống Chrome |
| Edge Extension | TypeScript | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | |
| VSCode Extension | TypeScript | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Official SDK dùng TS |
| Desktop App | Tauri + React | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Thay thế Electron trong đa số trường hợp |
| Desktop Enterprise | C# + WPF | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Khi chỉ chạy Windows |
| Cross-platform Desktop | Tauri | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Nhẹ hơn Electron |
| Mobile App | Flutter | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Cross-platform tốt |
| Mobile Native | Kotlin / Swift | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Khi cần native hoàn toàn |
| CLI Tool | Go | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | File binary nhỏ |
| DevOps CLI | Go | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Docker, kubectl đều viết bằng Go |
| Automation Script | Python | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | AI sinh script rất tốt |
| OCR | Python | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | OpenCV, Tesseract |
| AI Application | Python | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Hầu hết framework AI đều ưu tiên Python |
| Machine Learning | Python | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Chuẩn ngành |
| Deep Learning | Python | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | PyTorch, TensorFlow |
| Data Science | Python | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Pandas, NumPy |
| ETL/Data Pipeline | Python | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | |
| Web Scraping | Python | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | BeautifulSoup, Playwright |
| Test Automation | Playwright (TS) / Python | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | |
| Game 2D | Unity (C#) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | |
| Game 3D | Unity / Unreal | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | |
| Browser Game | TypeScript + Phaser | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | |
| IoT | C/C++ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | |
| Embedded | C/C++ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | |
| Blockchain | Solidity + TypeScript | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | |

## Khi nào nên chọn từng công nghệ làm main

| Công nghệ | Nên dùng khi |
|-----------|--------------|
| TypeScript | Web, API, SaaS, Dashboard, Extension, Tool |
| C# | ERP, MES, Backend lớn, Enterprise, Windows |
| Python | AI, ML, OCR, Automation, Data Processing |
| Go | CLI, DevOps, API Gateway, Cloud Native |
| Java | Enterprise lớn, Banking, Legacy |
| Kotlin | Android |
| Swift | iOS |
| Flutter | Mobile Cross-platform |
| Rust | Hiệu năng cực cao, System, Tauri |
| C/C++ | Driver, Embedded, Game Engine |

## AI hỗ trợ ngôn ngữ nào tốt nhất

| Công nghệ | AI hiểu code | AI sửa lỗi | AI refactor | AI generate |
|-----------|-------------|------------|--------------|-------------|
| TypeScript | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Python | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| C# | ⭐⭐⭐⭐☆ | ⭐⭐⭐⭐☆ | ⭐⭐⭐⭐☆ | ⭐⭐⭐⭐☆ |
| Go | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Java | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Rust | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| C++ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

## Đề xuất công nghệ chính (Main Stack)

Nếu mục tiêu là một lập trình viên có thể làm hầu hết các loại sản phẩm hiện đại, thì 4 công nghệ cốt lõi dưới đây là lựa chọn đáng cân nhắc nhất:

| Mục tiêu | Công nghệ |
|----------|-----------|
| Web + API + SaaS + Extension + Tool | TypeScript |
| Enterprise + Windows + Backend lớn | C# |
| AI + Automation + OCR + Data | Python |
| Cloud + DevOps + CLI + High Performance | Go |

