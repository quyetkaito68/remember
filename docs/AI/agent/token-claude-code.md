---
# ─── BẮT BUỘC ───────────────────────────────────────────
title: Token — Claude Code CLI Specific
description: Các kỹ thuật tiết kiệm token đặc thù cho Claude Code CLI — slash commands, CLAUDE.md, Plan Mode, Sub-agents.
tags: [claude, token, claude-code, optimization]
category: ai
updated: 2026-07-11

# ─── TÙY CHỌN ───────────────────────────────────────────
order: 6
---

# Token — Claude Code CLI Specific

> Các kỹ thuật và công cụ tiết kiệm token đặc thù cho Claude Code CLI. Đọc [Tối Ưu Token Cho AI Coding Agent](./token-optimization) trước để nắm các nguyên lý agent-agnostic.

---

## Slash Commands Kiểm Soát Bộ Nhớ

### /clear — Reset hoàn toàn session

Xóa sạch lịch sử trò chuyện, đưa Claude về trạng thái khởi động mới (giữ CLAUDE.md).

**Khi nào dùng:**
- Hoàn thành 1 task, chuẩn bị chuyển sang task mới
- Claude bắt đầu lặp lỗi hoặc quên convention

**So sánh chi phí sau 10 turns:**

| Cách làm | Token/turn | Tổng 10 turns | Tiết kiệm |
|----------|-----------|--------------|-----------|
| Không /clear | ~15.000 | ~150.000 | — |
| /clear mỗi task | ~2.000 | ~20.000 | **~87%** |

### /compact — Nén lịch sử hội thoại

Yêu cầu Claude tóm tắt lịch sử dài thành bản ghi nhớ siêu ngắn, giữ lại quyết định kỹ thuật quan trọng.

- Trước: 80.000 tokens → Sau: 8.000 tokens → **Tiết kiệm ~90%**

### /context — Giám sát tài nguyên

In ra chi tiết phân rã tài nguyên trong context window:

```text
Total Tokens Used: 45,200 / 200,000
- System Prompt:         4,500 tokens (10%)
- Conversation History: 25,000 tokens (55%)
- Read Files (3 files): 12,500 tokens (28%)
- Tool Output:           3,200 tokens (7%)
```

### /mcp & /skills — Tắt bớt schema không dùng

| Command | Tác dụng | Tiết kiệm |
|---------|----------|-----------|
| `/mcp` | Mỗi MCP active nhét JSON Schema vào context. 5 MCP = 2–5k token/turn overhead | Tùy số lượng MCP |
| `/skills` | Tắt skill không liên quan đến vai trò hiện tại | ~60% token overhead skill |

---

## Thiết Lập Môi Trường

### CLAUDE.md

CLAUDE.md được nạp ngay khi khởi động và nằm trong context suốt session. Template tối ưu:

```markdown
# Project: MISA ERP Module X

## Stack
Node.js 20, TypeScript, Postgres, Redis

## Coding Conventions
- Name: camelCase, prefix (getUserById)
- Error: Always use custom AppError class
- Test: Jest, file test đặt cạnh source

## Commands
- Test: npm test -- --testPathPattern=<file>
- Lint: npm run lint:fix

## KHÔNG LÀM
- Không sửa file migration cũ
```

### .claudeignore

```gitignore
# Dependencies & Builds
node_modules/
dist/ build/ .next/

# Logs & coverage
*.log logs/ coverage/

# Large database assets
*.sql migrations/old/

# IDE config
.vscode/ .DS_Store
```

### Skills folder

Tách hướng dẫn chạy test, build, deploy thành file skill riêng trong `.claude/skills/`. Claude chỉ đọc mô tả ngắn khi khởi động, nạp nội dung chi tiết khi thực sự dùng. **Tiết kiệm ~700–1.000 token mỗi turn.**

---

## Plan Mode & Sub-agents

**Plan Mode:** Bật (Tab) → Claude lên kế hoạch trước khi code → duyệt → tránh backtrack tốn token.

**Sub-agents:** Chia task lớn thành task con, xử lý trên session riêng, kết thúc mỗi task bằng `/clear`.

---

## Claude-Specific Checklist

### Trước khi bắt đầu task

- [ ] Chạy `/clear` để làm sạch session cũ
- [ ] Kiểm tra project đã có `.claudeignore` chưa
- [ ] Xác định chính xác file và dòng code cần sửa
- [ ] Nạp wiki rules liên quan đến nghiệp vụ

### Trong khi làm việc

- [ ] Viết prompt chi tiết (file path, line, expected)
- [ ] Dùng `rtk` prefix khi chạy lệnh terminal
- [ ] Chủ động gõ `/compact` nếu session kéo dài

### Sau khi hoàn thành task

- [ ] Gõ `/clear` chuẩn bị cho task sau
- [ ] Cập nhật LLM Wiki nếu phát hiện pattern/gotcha mới
- [ ] Cập nhật CLAUDE.md nếu có convention mới (giữ tinh gọn)

---

## Yêu cầu

- Claude Code CLI đã cài đặt
- Đã đọc [Tối Ưu Token Cho AI Coding Agent](./token-optimization) — các nguyên lý chung

---

## Tham khảo

- [Tối Ưu Token Cho AI Coding Agent](./token-optimization) — bản agent-agnostic
- [Claude Code CLI Overview](https://docs.anthropic.com/en/docs/claude-code/overview)
- [Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)

---

<!--
======================================================================
  METADATA CHO AGENT
  - Loại: technical-reference (Claude Code CLI-specific)
  - Bổ sung cho token-optimization.md — chỉ chứa Claude-specific knowledge
======================================================================
-->
