# Hướng Dẫn Kết Nối Claude Code Với Miễn Phí Qua OpenRouter

## Tổng Quan

Hướng dẫn này giúp bạn cấu hình **Claude Code** để sử dụng các **model AI miễn phí** thông qua **OpenRouter** thay vì dùng API key chính thức của Anthropic (có phí).

---

## Bước 1: Tạo Tài Khoản OpenRouter

1. Truy cập: https://openrouter.ai
2. Đăng ký tài khoản (có thể dùng GitHub/Google)
3. Vào **Settings** → **Keys** → **Create Key**
4. Copy **API Key** (dạng `sk-or-v1-xxxxx...`)

---

## Bước 2: Chọn Model Miễn Phí

Vào trang **Models** tại: https://openrouter.ai/models

Lọc **"Free"** hoặc tìm các model phổ biến:
| Model | Context | Đặc điểm |
|-------|---------|----------|
| `qwen/qwen3-coder:free` | 32K | Tốt cho coding |
| `meta-llama/llama-3.1-8b-instruct:free` | 8K | Cân bằng tốt |
| `google/gemma-2-9b-it:free` | 8K | Nhanh, nhẹ |
| `microsoft/phi-3-mini-128k-instruct:free` | 128K | Context dài |
| `nvidia/nemotron-3-ultra-550b-a55b:free` | 4K | Mạnh reasoning |

> **Lưu ý**: Model có đuôi `:free` là hoàn toàn miễn phí. Không có đuôi `:free` có thể tốn credit.

---

## Bước 3: Cấu Hình Claude Code

### Cách 1: Biến Môi Trường (Khuyên Dùng)

**Windows (PowerShell - vĩnh viễn):**
```powershell
[Environment]::SetEnvironmentVariable("ANTHROPIC_BASE_URL", "https://openrouter.ai/api", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_AUTH_TOKEN", "sk-or-v1-VOTRE_KEY_ICI", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "", "User")
```

**Windows (CMD - session hiện tại):**
```cmd
set ANTHROPIC_BASE_URL=https://openrouter.ai/api
set ANTHROPIC_AUTH_TOKEN=sk-or-v1-VOTRE_KEY_ICI
set ANTHROPIC_API_KEY=
```

**Linux/macOS (~/.bashrc hoặc ~/.zshrc):**
```bash
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="sk-or-v1-VOTRE_KEY_ICI"
export ANTHROPIC_API_KEY=""
```

### Cách 2: File Cấu Hình Claude Code

Tạo/sửa file `~/.claude/settings.json` (hoặc `%USERPROFILE%\.claude\settings.json` trên Windows):

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://openrouter.ai/api",
    "ANTHROPIC_AUTH_TOKEN": "sk-or-v1-VOTRE_KEY_ICI",
    "ANTHROPIC_API_KEY": ""
  }
}
```

### Cách 3: Chỉ Định Model Khi Chạy

```bash
# Chạy một lần với model cụ thể
claude --model qwen/qwen3-coder:free

# Hoặc set model mặc định
claude config set model qwen/qwen3-coder:free
```

---

## Bước 4: Kiểm Tra Kết Nối

```bash
# Kiểm tra version
claude --version

# Test chat đơn giản
claude -p "Xin chào, bạn là model nào?"

# Kiểm tra model đang dùng
claude config get model
```

---

## Bước 5: Cấu Hình Nâng Cao (Tùy Chọn)

### Thêm Header Referer (Khuyên Dùng Cho Production)

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://openrouter.ai/api",
    "ANTHROPIC_AUTH_TOKEN": "sk-or-v1-VOTRE_KEY_ICI",
    "ANTHROPIC_API_KEY": "",
    "HTTP_REFERER": "https://github.com/yourusername/yourproject",
    "X_TITLE": "Your Project Name"
  }
}
```

### Quản Lý Nhiều Model (Model Router)

Tạo file `~/.claude/model-aliases.json`:
```json
{
  "aliases": {
    "coder": "qwen/qwen3-coder:free",
    "chat": "meta-llama/llama-3.1-8b-instruct:free",
    "long": "microsoft/phi-3-mini-1-128k-instruct:free"
  }
}
```

Sử dụng:
```bash
claude --model @coder
claude --model @chat
```

---

## Khắc Phục Sự Cố Thường Gặp

| Lỗi | Nguyên Nhân | Giải Pháp |
|-----|-------------|-----------|
| `401 Unauthorized` | Sai API key | Kiểm tra key tại OpenRouter Settings |
| `429 Rate Limited` | Quá nhiều request | Đợi 1-2 phút, hoặc dùng model khác |
| `404 Model Not Found` | Sai tên model | Copy chính xác tên từ OpenRouter (có `:free`) |
| `Connection Refused` | Sai BASE_URL | Đảm bảo `https://openrouter.ai/api` |
| Model không phản hồi | Model down | Thử model free khác |

---

## So Sánh Chi Phí

| Cách | Chi Phí | Ưu Điểm | Nhược Điểm |
|------|---------|---------|------------|
| Anthropic Official | $5/1M tokens (Sonnet) | Ưu tiên cao, ổn định | Tốn tiền |
| OpenRouter Free | **$0** | Miễn phí hoàn toàn | Rate limit, đôi khi chậm |
| OpenRouter Paid | Theo model | Nhiều model, fallback | Cần nạp tiền |

---

## Mẹo Hay

1. **Xoay vòng model**: Khi bị rate limit, chuyển model khác:
   ```bash
   claude --model meta-llama/llama-3.1-8b-instruct:free
   ```

2. **Dry-run trước khi chạy code**:
   ```bash
   claude -p "Review code này cho bugs" --dry-run
   ```

3. **Lưu lịch sử chat** (mặc định đã lưu tại `~/.claude/history/`)

4. **Tắt telemetry** (nếu cần):
   ```bash
   export ANTHROPIC_TELEMETRY_DISABLED=1
   ```

---

## Tài Liệu Tham Khảo

- [OpenRouter Docs](https://openrouter.ai/docs)
- [Claude Code Reference](https://github.com/anthropics/claude-code)
- [Free Models List](https://openrouter.ai/models?max_price=0)
- [Claude Code Settings](https://github.com/anthropics/claude-code/blob/main/docs/settings.md)

---

## Cập Nhật

- **Ngày tạo**: 2026-06-30
- **Phiên bản**: 1.0
- **Tác giả**: Automation Script Project

> **Lưu ý quan trọng**: Các model miễn phí có giới hạn rate limit (thường 20-50 requests/phút). Nếu cần ổn định cao cho production, hãy cân nhắc nạp ít nhất $5-10 vào OpenRouter để dùng model paid với quota cao hơn.