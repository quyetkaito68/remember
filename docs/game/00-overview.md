---
title: Tổng quan Game Development
description: Tổng quan ngành phát triển game từ ý tưởng đến sản phẩm hoàn chỉnh
tags: [game-dev, overview]
category: game
updated: 2025-07-20
order: 0
---

# Game Development Overview

> Tổng quan ngành phát triển game — từ ý tưởng đến sản phẩm hoàn chỉnh.

---

## Game Development là gì?

Quá trình xây dựng một trò chơi, kết hợp nhiều chuyên ngành:

```text
┌──────────────────────────────────────────────────────┐
│                  Game Development                    │
│                                                      │
│  Programming    Art            Animation             │
│  Audio          Story          UI/UX                 │
│  Networking     AI             Physics               │
│  Deployment     Testing        Optimization          │
└──────────────────────────────────────────────────────┘
```

---

## Kiến trúc tổng quan

Mọi game đều dựa trên các tầng từ phần cứng đến gameplay:

```text
┌─────────────────────────────┐
│          Gameplay           │
├─────────────────────────────┤
│         Game Engine         │
├─────────────────────────────┤
│        Graphics API         │
├─────────────────────────────┤
│       Operating System      │
├─────────────────────────────┤
│          GPU / CPU          │
└─────────────────────────────┘
```

---

## Quy trình phát triển

Từ ý tưởng đến sản phẩm:

```text
┌──────┐   ┌────────┐   ┌───────────┐   ┌────────┐   ┌────────┐   ┌──────┐
│ Idea │──>| Design |──>| Prototype │──>| Build  │──>|  Test  │──>| Ship │
└──────┘   └────────┘   └───────────┘   └────────┘   └────────┘   └──────┘
```

---

## Game Loop

"Trái tim" của mọi game — chạy liên tục cho đến khi game đóng:

```text
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  Input  │──>| Update  │──>| Physics │──>| Render  │
└─────────┘   └─────────┘   └─────────┘   └────┬────┘
                                                |
                                                v
                                            (repeat)
```

---

## Cách làm game

Từ tự viết mọi thứ đến dùng engine hoàn chỉnh:

```text
┌─────────────────────────────┐
│     Write from Scratch      │
├─────────────────────────────┤
│       Graphics API          │
├─────────────────────────────┤
│         Framework           │
├─────────────────────────────┤
│           Engine            │
└─────────────────────────────┘
```

| Level | Approach | Bạn viết | Ví dụ |
|-------|----------|----------|-------|
| 4 | Write from Scratch | Mọi thứ | C++ + OS API |
| 3 | Graphics API | Game logic | OpenGL, Vulkan, DirectX |
| 2 | Framework | Game logic | SDL, SFML, Raylib |
| 1 | Engine | Gameplay | Unity, Unreal, Godot |

---

## Stack công nghệ

| Nhóm | Ngôn ngữ / Công cụ |
|------|---------------------|
| Native | C, C++, Rust |
| Engine Script | C# (Unity), Blueprint (Unreal), GDScript (Godot), Lua |
| Mobile | Java, Kotlin, Swift |
| Browser | JavaScript, TypeScript, WebGL, WebGPU |

---

## Mức độ phức tạp

```text
Text Game
    │
ASCII Game
    │
2D
    │
2D Physics
    │
Platformer
    │
Top Down RPG
    │
Tower Defense
    │
Multiplayer
    │
Open World
    │
MMORPG
```

---

## Tìm hiểu thêm

| Chủ đề | Mô tả |
|--------|-------|
| [Lịch sử](01-history.md) | Tiến hóa công nghệ từ Assembly đến AI |
| [Phân loại game](02-game-types.md) | Theo đồ họa (2D/3D/VR) và gameplay (FPS/RPG/MOBA) |
| [Nền tảng](03-platforms.md) | PC, Console, Mobile, Browser, Cloud, VR/AR |
| [Game Engine](04-game-engines.md) | Cấu trúc engine và chuẩn chung |
| [Graphics API](05-graphics-api.md) | OpenGL, Vulkan, DirectX, Metal |
| [Game Loop](07-game-loop.md) | Chi tiết chu trình Input → Update → Render |
| [Kiến trúc game](17-architecture.md) | ECS, Component Based, Actor Model |
| [Lộ trình học](roadmap.md) | Từ cơ bản đến AAA Architecture |


# Game Development

> Tổng quan ngành phát triển game

---

## Tài liệu hiện có

| # | File | Chủ đề |
|---|------|--------|
| 00 | [Tổng quan](00-overview.md) | Tổng quan ngành Game Development |
| 01 | [Lịch sử](01-history.md) | Tiến hóa công nghệ từ Assembly đến AI |
| 02 | [Phân loại game](02-game-types.md) | Theo đồ họa và gameplay |
| 03 | [Nền tảng](03-platforms.md) | PC, Console, Mobile, Browser, Cloud, VR/AR |
| 04 | [Game Engine](04-game-engines.md) | Cấu trúc engine và chuẩn chung |
| 05 | [Graphics API](05-graphics-api.md) | OpenGL, Vulkan, DirectX, Metal |
| 07 | [Game Loop](07-game-loop.md) | Chu trình Input → Update → Render |
| 17 | [Kiến trúc](17-architecture.md) | ECS, Component Based, Actor Model |
| — | [Lộ trình học](roadmap.md) | Từ cơ bản đến AAA Architecture |

---

## Đang phát triển

| # | File | Chủ đề |
|---|------|--------|
| 06 | Rendering Pipeline | Quy trình渲染 từ scene đến pixel |
| 08 | Physics | Hệ thống vật lý trong game |
| 09 | Game AI | FSM, Behavior Tree, Navigation |
| 10 | Networking | Multiplayer, Client-Server |
| 11 | Audio | Hệ thống âm thanh trong game |
| 12 | Animation | Skeletal, Blend Tree, State Machine |
| 13 | Shaders | Vertex, Fragment, GLSL/HLSL |
| 14 | Mathematics | Vector, Matrix, Quaternion |
| 15 | Optimization | Profiling, LOD, Culling |
| 16 | Asset Pipeline | Quy trình quản lý asset |
| 18 | Design Patterns | Singleton, Observer, State... |
| 19 | Project Structure | Cấu trúc thư mục dự án |
