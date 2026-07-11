---
name: ascii-diagram
description: >
  Quy tắc vẽ ASCII diagram trong code block `text` — đếm ký tự chính xác, box template, flow arrows,
  cấm ký tự Unicode lệch width, kích thước tối đa, verification script.
  TRIGGER khi user yêu cầu vẽ sơ đồ, diagram, flow, architecture bằng ASCII.
---

# ascii-diagram — Quy tắc vẽ ASCII Diagram

**Bắt buộc tuân thủ khi vẽ sơ đồ trong code block `text`.**

---

## Nguyên tắc 1: Đếm ký tự chính xác

Mỗi dòng trong box phải có **đúng cùng số ký tự** từ `│` trái đến `│` phải.

```text
┌──────────────────┐     ← 20 inner chars (góc + 18 dash + góc)
│    Tiêu đề       │     ← 20 inner chars (│ + 18 content + │)
└──────────────────┘     ← 20 inner chars
```

**Cách đếm:** Đếm TẤT CẢ ký tự trên 1 dòng, kể cả spaces. Mỗi dòng trong cùng 1 box PHẢI bằng nhau.

---

## Nguyên tắc 2: Template cơ bản

### Box đơn giản

```text
┌─────────────────────┐
│     TIÊU ĐỀ         │
│                     │
│   Nội dung ở đây    │
└─────────────────────┘
```

### Box với sub-box

```text
┌───────────────────────────────────┐
│           TITLE                   │
│                                   │
│   ┌──────────┐  ┌──────────┐      │
│   │  Item A  │  │  Item B  │      │
│   └──────────┘  └──────────┘      │
└───────────────────────────────────┘
```

### Flow arrows

```text
┌──────────┐     ┌──────────┐
│  Step 1  │────>│  Step 2  │
└──────────┘     └──────────┘
```

---

## Nguyên tắc 3: Cấm ký tự có độ rộng khác chuẩn

Không dùng các ký tự Unicode có độ rộng khác với monospace chuẩn. Chỉ dùng `─`, `│`, `┌`, `┐`, `└`, `┘`, `├`, `┤`, `┬`, `┴`, `┼` cho border và `>`, `v`, `<`, `^` làm mũi tên.

| Sai | Đúng |
|-----|------|
| `───▶` | `───>` |
| `───▼` | `───v` |
| `───●` | `───o` |
| `───◆` | `───*` |
| `───■` | `───#` |

**Không dùng:** ▶, ▼, ●, ◆, ■, ➤, ➡, ▸, →, ↑, ←, ↓, ▲, △, ▽ (có thể lệch width trong terminal).
**Dùng thay thế:** `>`, `v`, `^`, `<`, `o`, `*`, `#`.

---

## Nguyên tắc 4: Verification

Sau khi sinh diagram, CHẠY script kiểm tra:

```bash
powershell -File scripts/verify-diagram.ps1 -File <path-to-md>
```

Script sẽ check:
- Mỗi dòng trong code block `text` có equal-length border chars
- Không có dòng nào bị lệch

---

## Nguyên tắc 5: Kích thước tối đa

- **Rộng tối đa:** 80 ký tự (fit terminal chuẩn)
- **Cao tối đa:** 30 dòng / diagram
- Nếu lớn hơn → tách thành nhiều diagram nhỏ
