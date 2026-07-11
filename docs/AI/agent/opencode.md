---
title: OpenCode — AI Coding Agent
description: OpenCode là AI coding agent mã nguồn mở chạy trong terminal, hỗ trợ đa model (Claude, GPT, Gemini,...) cho lập trình viên.
tags: [opencode, ai, coding-agent, terminal, opensource]
category: ai
order: 3
updated: 2026-07-11
---

# OpenCode — AI Coding Agent

[OpenCode](https://opencode.ai/) là AI coding agent mã nguồn mở, chạy trực tiếp trong terminal. Hỗ trợ đa dạng model AI (Claude, GPT, Gemini,...), có khả năng đọc/ghi file, chạy lệnh, tìm kiếm code và quản lý Git.

## Tính năng chính

- Miễn phí, mã nguồn mở
- Chạy trong terminal, không cần GUI
- Hỗ trợ 75+ LLM providers (Anthropic, OpenAI, Google, Groq, DeepSeek, Ollama,...)
- Tích hợp sâu với codebase (đọc/ghi file, chạy lệnh, Git)
- Hệ thống plugin, skill, MCP servers, custom tools

## Model & Provider

OpenCode dùng [AI SDK](https://ai-sdk.dev/) và [Models.dev](https://models.dev) để hỗ trợ đa dạng model:

**Providers built-in sẵn:** Anthropic (Claude), OpenAI (GPT), Google (Gemini), Groq, DeepSeek, GitHub Copilot, GitLab Duo, OpenRouter, Ollama (local), LM Studio, Together AI, và nhiều provider khác.

**OpenCode Zen:** Danh sách model đã được đội ngũ OpenCode kiểm thử và tối ưu cho coding agent. Gồm các dòng model chính:
- **OpenAI:** GPT-5.x, GPT-5.6 Sol/Terra/Luna, GPT-5.x Codex
- **Anthropic:** Claude Opus 4.x, Claude Sonnet 4.x/5, Claude Haiku 4.5, Claude Fable 5
- **Google:** Gemini 3.x Pro/Flash
- **Others:** Qwen 3.x, DeepSeek V4, Kimi K2.x, MiniMax M3, GLM 5.x, Grok 4.5
- **Free models:** Big Pickle, DeepSeek V4 Flash Free, MiMo-V2.5 Free, Nemotron 3 Ultra Free

Các provider phổ biến được nạp sẵn, chỉ cần thêm API key qua lệnh `/connect`.

## Cài đặt nhanh

```bash
npm i -g opencode-ai
```

Sau đó chạy `opencode` trong terminal, dùng `/connect` để thêm API key provider, `/models` để chọn model.

## Tài liệu & Hướng dẫn

- Trang chủ: [opencode.ai](https://opencode.ai/)
- Tài liệu: [opencode.ai/docs](https://opencode.ai/docs/)
- Model Zen: [opencode.ai/zen](https://opencode.ai/zen/)
