---
title: Game Loop
description: Chu trình lặp Input → Update → Render - "trái tim" của mọi game
tags: [game-dev, game-loop]
category: game
updated: 2025-07-20
order: 7
---

# Game Loop

> Chu trình lặp của mọi game — "trái tim" của game

---

## Cơ bản

Đây là chuẩn chung của gần như mọi game.

```text
while (running)

    Read Input

    Update Logic

    Physics

    AI

    Animation

    Render

repeat
```

---

## Chi tiết hơn

```text
Input

↓

Update

↓

Physics

↓

Collision

↓

Animation

↓

Render

↓

Repeat (60 FPS)
```
