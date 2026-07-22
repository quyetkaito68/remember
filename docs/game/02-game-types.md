---
title: Phân loại Game
description: Phân loại game theo đồ họa (2D/3D/VR) và gameplay (FPS/RPG/MOBA)
tags: [game-dev, game-types]
category: game
updated: 2025-07-20
order: 2
---

# Phân loại Game

> Phân loại game theo đồ họa và gameplay

---

## Theo đồ họa

```text
Text ──> ASCII ──> 2D ──> 2.5D ──> Isometric ──> 3D ──> VR
```

### Text Game

Không có hình ảnh, chỉ có chữ. Người chơi đọc mô tả và đưa ra lựa chọn. Đây là thể loại cổ nhất, thường thấy trong các game phiêu lưu thập niên 80.

```text
You are in a cave.

Choose:

1. Go Left

2. Go Right
```

**Ví dụ:** Zork, Colossal Cave Adventure

---

### ASCII Game

Sử dụng ký tự ASCII để tạo hình ảnh đơn giản. Thường là roguelike — thể loại game với bản đồ ngẫu nhiên và cái chết vĩnh viễn.

```text
#######
# @   #
#  M  #
#######
```

**Ví dụ:** Rogue, NetHack

---

### 2D

Đồ họa phẳng, chỉ có hai trục X và Y. Đây là thể loại phổ biến nhất trong thập niên 80-90, và vẫn được yêu thích đến ngày nay nhờ lối chơi đơn giản và nghệ thuật pixel.

```text
██████
Player → →
Enemy
```

**Ví dụ:** Mario, Stardew Valley, Hollow Knight

---

### 2.5D

Đồ họa 3D nhưng gameplay vẫn 2D. Góc nhìn thường là từ trên xuống hoặc side-scrolling. Kết hợp ưu điểm của cả hai thế giới.

**Ví dụ:** Diablo II, Sonic Adventures

---

### Isometric

Góc nhìn chéo 45 độ, tạo cảm giác 3D nhưng vẫn là 2D. Phổ biến trong game strategy và RPG vì cho phép quan sát chiến trường tốt.

**Ví dụ:** Age of Empires, Diablo, StarCraft

---

### 3D

Thế giới ba chiều với ba trục X, Y, Z. Đòi hỏi phần cứng mạnh hơn và graphics API chuyên dụng. Đây là tiêu chuẩn hiện nay cho AAA game.

**Ví dụ:** GTA, Elden Ring, Minecraft

---

### VR

Thế giới 3D nhập vai, người chơi đeo kính VR và tương tác trực tiếp. Mở ra trải nghiệm hoàn toàn mới nhưng đòi hỏi phần cứng chuyên dụng.

**Ví dụ:** Beat Saber, Half-Life: Alyx

---

## Theo Gameplay

| Thể loại | Mô tả | Ví dụ |
|----------|-------|-------|
| FPS | Bắn súng góc nhìn thứ nhất | Doom, Counter Strike |
| TPS | Bắn súng góc nhìn thứ ba | PUBG, Fortnite |
| Platform | Nhảy và di chuyển trên nền tảng | Mario, Celeste |
| RTS | Chiến thuật thời gian thực | StarCraft, Age of Empires |
| MOBA | Đội nhóm, bản đồ nhỏ | Dota 2, League of Legends |
| Turn Based | Lượt lượt | Civilization, Heroes |
| RPG | Phát triển nhân vật | Skyrim, Witcher |
| MMORPG | RPG trực tuyến nhiều người | World of Warcraft |
| Puzzle | Giải đố | Tetris, Candy Crush |
| Card | Bài bài | Hearthstone |
| Sandbox | Tự do sáng tạo | Minecraft |
| Simulation | Mô phỏng | The Sims, Euro Truck |
| Survival | Sinh tồn | Rust, Don't Starve |
| Idle | Tự chạy | Cookie Clicker |
| Rhythm | Nhịp điệu | Osu! |

---

## Nhóm thể loại chính

```text
┌─────────────────────────────────────────────────────────────────┐
│                      NHÓM THỂ LOẠI                              │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────┤
│   Action    │  Strategy   │     RPG     │   Puzzle    │  Other  │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────┤
│  FPS, TPS   │ RTS, MOBA   │ RPG         │ Puzzle      │ Sandbox │
│  Platform   │ Turn Based  │ MMORPG      │ Card        │ Sim     │
│             │             │             │             │ Survive │
│             │             │             │             │ Idle    │
│             │             │             │             │ Rhythm  │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────┘
```
