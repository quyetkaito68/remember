---
# ─── BẮT BUỘC ───────────────────────────────────────────
title: Tối Ưu Token Cho AI Coding Agent
description: Hướng dẫn agent-agnostic về tiết kiệm token, quản lý context window và kỹ thuật prompting cho mọi AI coding agent (opencode, Claude Code, Cline, Continue...).
tags: [token, optimization, prompt, context-window, caching, agent]
category: ai
updated: 2026-07-11

# ─── TÙY CHỌN ───────────────────────────────────────────
order: 5
---

# Tối Ưu Token Cho AI Coding Agent

> Các kỹ thuật tối ưu token, kiểm soát context window và duy trì hiệu suất cho mọi AI coding agent — áp dụng được cho opencode, Claude Code CLI, Cline, Continue và các agent khác.

---

## Tổng quan

Token là đơn vị tính phí và tài nguyên của mọi LLM. Mỗi session coding agent không được kiểm soát có thể tiêu hao hàng trăm nghìn token do context bị phình to bởi lịch sử hội thoại dài, file rác và tool output dư thừa.

Tài liệu này tổng hợp các kỹ thuật tiết kiệm token agent-agnostic, giúp developer:
- Hiểu bản chất token và cơ chế context window
- Quản lý bộ nhớ session chủ động
- Thiết lập môi trường tối ưu ngay từ đầu
- Viết prompt tiết kiệm mà vẫn đủ ngữ cảnh
- Áp dụng công cụ hỗ trợ bên ngoài

---

## Mục lục

- [1. Bản chất Token & Context Window](#1-bản-chất-token--context-window)
- [2. Quản Lý Session](#2-quản-lý-session)
- [3. Thiết Lập Môi Trường Tối Ưu](#3-thiết-lập-môi-trường-tối-ưu)
- [4. Kỹ Thuật Prompting Tiết Kiệm](#4-kỹ-thuật-prompting-tiết-kiệm)
- [5. Công Cụ & Plugin Hỗ Trợ](#5-công-cụ--plugin-hỗ-trợ)
- [6. Checklist Thói Quen Hàng Ngày](#6-checklist-thói-quen-hàng-ngày)

---

## 1. Bản chất Token & Context Window

### Token là gì & Quy tắc ước lượng nhanh

**Định nghĩa:** Token là đơn vị nhỏ nhất mà LLM xử lý — không phải từ, không phải ký tự, mà là mảnh văn bản (sub-words) do mô hình phân tách.

**Đặc thù tiếng Việt:** Do sử dụng mã UTF-8 nhiều byte hơn và cách phân tách từ ghép, token tiếng Việt tốn gấp 2–3 lần so với tiếng Anh cho cùng độ dài nội dung.

> **Quy tắc quy đổi nhanh:**
> - 1 từ tiếng Anh ≈ 1–1.5 token
> - 1 từ tiếng Việt ≈ 2–3 token
> - 1 dòng code ≈ 5–15 token

| Nội dung | Token ước tính |
|----------|---------------|
| "Fix bug in login function" | ~6 token |
| "Bạn có thể giúp tôi sửa lỗi..." | ~18 token |
| 1 file package.json (50 dòng) | ~400–600 token |
| 1 file log server (500 dòng) | ~3.000–5.000 token |

### Context Window & "Context Rot"

**Hiện tượng "Context Rot":** Qua nhiều turn, agent bắt đầu lặp lại lỗi cũ, quên rule, phản hồi mơ hồ.

**Nguyên nhân:** Quá nhiều dữ liệu rác (logs dài, file cũ đã đọc) làm loãng bộ nhớ đệm.

**Công thức Context:**

```text
Context Window = System Prompt + Instructions + History
               + Read Files + Tool Outputs + Current Query
```

**Cách load context trong 1 session:**

| Thời điểm | Thành phần | Chi phí |
|-----------|-----------|---------|
| Session start | Instructions, memory files | Full content, mọi request |
| Khi dùng | Tool schemas, module definitions | On demand |
| Cô lập | Sub-agents, hooks | Riêng biệt, zero cost |

### Prompt Caching

Prompt Caching cho phép lưu trữ các đoạn prompt cố định (system prompt, instructions, file code, lịch sử dài) trên server để tái sử dụng.

- **Tiết kiệm chi phí:** Giá đọc cache rẻ hơn nhiều lần (có thể đến 90%)
- **Tăng tốc độ:** Giảm độ trễ đáng kể cho session dài
- **Tự động kích hoạt:** Khi prefix prompt đạt ngưỡng nhất định (thường ≥ 1.024 tokens)

**Cơ chế Prefix Cache:**

| Turn | Mô tả | Cache |
|------|-------|-------|
| 1 | System + Context + Message | Chưa có cache, ghi mới |
| 2 | Cả turn 1 + Message mới | Đọc cache từ turn 1 |
| 3 | Cả turn 2 + Message mới | Đọc cache từ turn 2 |
| 4 (nếu system prompt thay đổi) | Toàn bộ reprocess | Cache miss |

---

## 2. Quản Lý Session

### Reset session theo task

Xóa sạch lịch sử hội thoại khi chuyển task — đưa agent về trạng thái khởi động mới (giữ instructions/system prompt).

**Khi nào dùng:**
- Hoàn thành 1 task, chuẩn bị chuyển sang task mới
- Agent bắt đầu lặp lỗi hoặc quên convention

**So sánh chi phí sau 10 turns:**

| Cách làm | Token/turn | Tổng 10 turns | Tiết kiệm |
|----------|-----------|--------------|-----------|
| Không reset | ~15.000 | ~150.000 | — |
| Reset mỗi task | ~2.000 | ~20.000 | **~87%** |

### Nén lịch sử hội thoại

Yêu cầu agent tóm tắt lịch sử dài thành bản ghi nhớ siêu ngắn, giữ lại quyết định kỹ thuật quan trọng. Trước: 80.000 tokens → Sau: 8.000 tokens → **Tiết kiệm ~90%.**

### Giám sát tài nguyên

Kiểm tra phân rã tài nguyên trong context window:

```text
Total Tokens Used: 45,200 / 200,000
- System Prompt:         4,500 tokens (10%)
- Conversation History: 25,000 tokens (55%)
- Read Files (3 files): 12,500 tokens (28%)
- Tool Output:           3,200 tokens (7%)
```

---

## 3. Thiết Lập Môi Trường Tối Ưu

### Instructions file — System prompt tinh gọn (< 500 tokens)

File instructions (CLAUDE.md, AGENTS.md, .cursorrules, .windsurfrules...) được nạp ngay khi khởi động và nằm trong context suốt session. Mỗi dòng thừa nhân lên qua mỗi turn.

**So sánh chi phí (10 turns):**
- Dài dòng (2.000 tokens) → 20.000 tokens
- Tinh gọn (400 tokens) → 4.000 tokens → **Tiết kiệm ~80%**

**Template instructions tối ưu:**

```markdown
# Project: <Tên Project>

## Stack
<tech1>, <tech2>, <tech3>

## Coding Conventions
- Name: <convention>, prefix (getXById)
- Error: <error handling pattern>
- Test: <framework>, <convention>

## Commands
- Test: <command>
- Lint: <command>

## KHÔNG LÀM
- <rule 1>
- <rule 2>
```

### Ignore file — Chặn đọc file rác

Dùng ignore file (.claudeignore, .cursorignore, .gitignore-enhanced...) để loại bỏ folder build, logs, dependencies khỏi phạm vi đọc file tự động. **Giảm đến 85% token reads.**

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

### Skills / Modules — Tải theo nhu cầu

Tách hướng dẫn chạy test, build, deploy thành file riêng. Agent chỉ đọc mô tả ngắn khi khởi động, nạp nội dung chi tiết khi thực sự dùng. **Tiết kiệm ~700–1.000 token mỗi turn.**

### Knowledge Base / Wiki — "Bộ não ngoài"

Duy trì Wiki cấu trúc bằng Markdown thay vì để LLM tìm kiếm hoặc đoán mò.

**Cấu trúc thư mục gợi ý:**

```text
<project>-knowledge/wiki/
├── index.md           # Bản đồ Wiki dẫn đường
├── rules/
│   ├── backend-rules.md
│   └── frontend-rules.md
└── patterns/
    └── create-entity.md
```

**Quy tắc:** Mỗi file dưới 200 dòng. Nếu quá dài, tách file và liên kết qua Wiki Link.

**3 bước hàng ngày:**
1. **Ingest** — Nạp rule/pattern/domain knowledge vào folder tương ứng
2. **Update** — Review và cập nhật trang liên quan sau khi dev xong
3. **Query** — Đọc index.md và trang liên quan trước khi code

---

## 4. Kỹ Thuật Prompting Tiết Kiệm

### Specific beats verbose

❌ **Prompt mơ hồ** — Tốn ~8k–15k tokens
```text
"Bạn có thể giúp tôi với authentication không? Tôi đang gặp vấn đề với login."
```

✅ **Prompt tối ưu** — Chỉ tốn ~1.5k–2k tokens
```text
File: src/auth/controllers/login.controller.ts, dòng 47
Lỗi: 'Cannot read property userId of undefined'
Khi: User login với Google OAuth
Mong muốn: Fix lỗi này, giữ nguyên structure hiện tại.
```

### Chỉ đọc file cần thiết & thắt chặt output

**Giới hạn file đọc:**
- ❌ "Xem cả project và refactor code auth" → 30k+ tokens
- ✅ "Refactor auth.service.ts theo service pattern của user.service.ts" → ~2k tokens

**Ép agent trả lời ngắn gọn:**
- "Chỉ trả code, không giải thích"
- "Show diff only, not full file"
- "Tóm tắt trong 3 bullet points"

| Yêu cầu | Ràng buộc | Token output | Tiết kiệm |
|---------|-----------|-------------|-----------|
| Giải thích JWT | Không | ~800 token | — |
| Giải thích JWT | 5 dòng | ~150 token | ~81% |
| Viết fn validate | Không | ~400 token | — |
| Viết fn validate | Code only | ~150 token | ~63% |

### Chia nhỏ task

Chia task lớn thành task con, xử lý trên từng session riêng, reset session giữa các task — tránh context bị phình và giảm chi phí.

---

## 5. Công Cụ & Plugin Hỗ Trợ

### Nhóm A: Giảm output

| Công cụ | Cơ chế | Hiệu quả |
|---------|--------|----------|
| **Ponytail** | Inject YAGNI, tránh over-engineering | LOC -54%, Token -22% |
| **Caveman** | Loại bỏ văn phong hoa mỹ, trả lời tối giản | Token output -65% |

### Nhóm B: Giảm input noise

**RTK** — Wrap CLI commands, nén logs, loại bỏ dòng lặp:

| Câu lệnh | Tiết kiệm |
|----------|-----------|
| `rtk ls -la` | -81% tokens |
| `rtk git diff` | -76% tokens |
| `rtk npm run test` | -68% tokens |

**Context-Mode:** Chạy build/test trong sandbox riêng biệt, chỉ gửi tóm tắt 3KB → tiết kiệm >99%.

**Repomix:** Đóng gói toàn bộ codebase thành 1 file text sạch, loại bỏ file rác.

### Đồ thị tri thức (Knowledge Graph)

| Công cụ | Loại | Đặc điểm |
|---------|------|----------|
| **GitNexus** | MCP Server | Cung cấp tools/skills trên đồ thị tri thức, on-demand |
| **Graphify** | Hook | PreToolUse hook, intercept tool calls, bơm surgical context |
| **CodeGraph** | Local DB | Quét source → SQLite, file watcher tự động cập nhật |

### Bảng tra cứu nhanh

| Vấn đề | Triệu chứng | Công cụ / Giải pháp |
|--------|------------|---------------------|
| Code quá dài, phức tạp | Over-engineering | Ponytail |
| Giải thích quá nhiều | Token output cao | Caveman |
| Logs chiếm bộ nhớ | Context phình to | RTK |
| Build/test quá lớn | Vượt giới hạn token | Context-Mode |
| Onboarding dự án | Mất thời gian chỉ file | Repomix |
| Phân tích kiến trúc | AI phán đoán mò mẫm | Graphify, CodeGraph |
| Quên convention | Giải thích lại liên tục | Knowledge Base / Wiki |

---

## 6. Checklist Thói Quen Hàng Ngày

### Trước khi bắt đầu task

- [ ] Reset session để làm sạch lịch sử cũ
- [ ] Kiểm tra project đã có ignore file chưa
- [ ] Xác định chính xác file và dòng code cần sửa
- [ ] Nạp wiki rules liên quan đến nghiệp vụ

### Trong khi làm việc

- [ ] Viết prompt chi tiết (file path, line, expected)
- [ ] Dùng `rtk` prefix khi chạy lệnh terminal
- [ ] Chủ động nén lịch sử nếu session kéo dài

### Sau khi hoàn thành task

- [ ] Reset session chuẩn bị cho task sau
- [ ] Cập nhật Knowledge Base nếu phát hiện pattern/gotcha mới
- [ ] Cập nhật instructions file nếu có convention mới (giữ tinh gọn)

---

## Yêu cầu

- Một AI coding agent đã cài đặt (opencode, Claude Code CLI, Cline, Continue...)
- Hiểu biết cơ bản về terminal và CLI
- Quyền truy cập vào project (đọc/ghi file, chạy lệnh)

---

## Tham khảo

- [Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) — Anthropic prompt caching docs (khái niệm chung)
- [Ponytail](https://github.com/McKay42/ponytail) — YAGNI tool cho AI coding
- [Repomix](https://github.com/yamadashy/repomix) — Đóng gói codebase thành 1 file
- [RTK](https://github.com/nicoverbruggen/rtk) — CLI output compression

---

<!--
======================================================================
  METADATA CHO AGENT
  - Loại: topic-overview (agent-agnostic)
  - Agent-agnostic — không dùng thuật ngữ riêng của bất kỳ agent nào
  - Nếu cần thông tin agent-specific, xem file tương ứng (token-claude-code.md, opencode.md...)
======================================================================
-->
