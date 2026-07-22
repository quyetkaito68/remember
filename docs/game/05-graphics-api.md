---
title: Graphics API
description: Lớp giao tiếp trực tiếp giữa Game/Engine và GPU - OpenGL, Vulkan, DirectX, Metal
tags: [game-dev, graphics, api]
category: game
updated: 2025-07-20
order: 5
---

# Graphics API

> Lớp giao tiếp trực tiếp giữa Game/Engine và GPU

---

## Vị trí trong pipeline

```text
Game

↓

Engine

↓

Graphics API

↓

GPU

↓

Monitor
```

---

## Các API phổ biến

| API | Nền tảng | Ghi chú |
|-----|----------|---------|
| OpenGL | Cross-platform | Deprecated, nhiều legacy |
| Vulkan | Cross-platform | Low-level, hiệu năng cao |
| DirectX | Windows / Xbox | Microsoft only |
| Metal | Apple | iOS / macOS only |
| WebGL | Browser | Dựa trên OpenGL ES |
| WebGPU | Browser | Thế hệ mới, thay WebGL |
