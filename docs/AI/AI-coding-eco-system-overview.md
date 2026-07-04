---
title: AI Coding Ecosystem Handbook
description: Tổng quan hệ sinh thái AI Coding từ Model, Runtime, API, Coding Agent đến IDE.
tags: [ai, coding, ecosystem, model, agent]
category: ai
order: 1
updated: 2026-07-05
---

# AI Coding Ecosystem Handbook

> Phiên bản: 2026
> Mục tiêu: Giúp Developer hiểu toàn bộ hệ sinh thái AI Coding từ Model → Runtime → API → Coding Agent → IDE.

---

# Mục lục

* [1. Kiến trúc tổng quan](#1-kiến-trúc-tổng-quan)
* [2. AI Model](#2-ai-model)
* [3. Runtime (Cloud & Local)](#3-runtime-cloud--local)
* [4. Ollama](#4-ollama)
* [5. OpenRouter](#5-openrouter)
* [6. AI Coding Agent](#6-ai-coding-agent)
* [7. IDE](#7-ide)
* [8. Quan hệ giữa các thành phần](#8-quan-hệ-giữa-các-thành-phần)
* [9. Ollama vs OpenRouter](#9-ollama-vs-openrouter)
* [10. Stack khuyến nghị & Lộ trình học](#10-stack-khuyến-nghị--lộ-trình-học)

---

# 1. Kiến trúc tổng quan

Toàn bộ hệ sinh thái AI Coding có thể chia thành 5 tầng.

```text
                ┌─────────────────────────────┐
                │         AI Model            │
                │ GPT / Claude / Qwen / ...   │
                └──────────────┬──────────────┘
                               │
                       Runtime / API
                               │
           ┌───────────────────┴────────────────────┐
           │                                        │
     Cloud Runtime                          Local Runtime
(OpenAI, Anthropic, OpenRouter)      (Ollama, LM Studio...)
           │                                        │
           └───────────────────┬────────────────────┘
                               │
                       AI Coding Agent
      Claude Code / Cursor / Cline / Roo Code / ...
                               │
                               ▼
                    IDE (VS Code / JetBrains)
```

---

## Vai trò từng tầng

| Thành phần   | Vai trò                  |
| ------------ | ------------------------ |
| AI Model     | Bộ não sinh nội dung     |
| Runtime/API  | Chạy hoặc cung cấp Model |
| Coding Agent | Điều khiển AI làm việc   |
| IDE          | Môi trường lập trình     |

---

# 2. AI Model

AI Model là thành phần thực hiện suy luận và sinh kết quả.

Ví dụ:

* GPT-5
* Claude Sonnet
* Qwen3-Coder
* DeepSeek R1
* Kimi K2
* GLM
* Mistral
* Llama

Model chỉ thực hiện:

```text
Input
   │
Reasoning
   │
Output
```

Model **không biết**:

* File đang mở
* Git
* VS Code
* Repository
* Docker
* Terminal

Những khả năng đó thuộc về Coding Agent.

---

## Phân loại Model

### General Chat Model

Ví dụ:

* GPT
* Claude
* Gemini

Dùng để:

* Chat
* Giải thích
* Viết tài liệu

---

### Coding Model

Ví dụ:

* Qwen3-Coder
* DeepSeek
* Kimi

Tối ưu cho:

* Generate code
* Refactor
* Debug
* Repository

---

### Reasoning Model

Ví dụ:

* DeepSeek R1

Đặc điểm:

* Suy nghĩ nhiều bước
* Giải bug khó
* Thiết kế kiến trúc

Đổi lại:

* Chậm hơn
* Tốn token hơn

---

# 3. Runtime (Cloud & Local)

Runtime là nơi thực sự chạy AI Model.

Có hai nhóm.

---

## Cloud Runtime

Model chạy trên server của nhà cung cấp.

```text
VS Code
   │
Cline
   │
OpenRouter
   │
DeepSeek R1
```

Ví dụ:

* OpenAI API
* Anthropic API
* Google AI Studio
* OpenRouter
* Together AI
* Groq

Ưu điểm

* Không cần GPU
* Model mới nhất
* Dễ sử dụng

Nhược điểm

* Mất phí theo token
* Cần Internet

---

## Local Runtime

Model chạy ngay trên máy người dùng.

```text
VS Code
   │
Cline
   │
localhost:11434
   │
Ollama
   │
Qwen3-Coder
```

Ví dụ:

* Ollama
* LM Studio
* llama.cpp
* vLLM
* SGLang
* TensorRT-LLM

Ưu điểm

* Không tốn API
* Offline
* Riêng tư

Nhược điểm

* Cần RAM/GPU mạnh
* Model thường nhỏ hơn Cloud

---

# 4. Ollama

Ollama **không phải AI Model**.

Ollama là Runtime dùng để chạy AI Model trên máy local.

Có thể xem như:

> Docker Desktop dành cho AI.

Ví dụ:

```bash
ollama run qwen3-coder
```

Sau khi chạy, Ollama sẽ tạo API:

```text
http://localhost:11434
```

Các Agent như:

* Cline
* Continue
* Roo Code

sẽ gọi API này.

---

## Chức năng

* Download Model
* Quản lý Model
* Load Model
* Expose REST API
* Quản lý Context

---

## Ví dụ kiến trúc

```text
VS Code
   │
Cline
   │
localhost:11434
   │
Ollama
   │
Qwen3-Coder
```

---

# 5. OpenRouter

OpenRouter không phải AI.

OpenRouter là API Gateway.

Có thể hình dung như:

> Booking.com của các AI Model.

Thay vì đăng ký API của từng hãng:

* OpenAI
* Anthropic
* Google
* Alibaba
* Moonshot
* Zhipu

Bạn chỉ cần:

* 1 API Key
* 1 Endpoint

Sau đó đổi Model rất dễ.

Ví dụ:

```json
{
  "model": "deepseek-r1"
}
```

Đổi thành:

```json
{
  "model": "kimi-k2"
}
```

Không cần sửa code khác.

---

## Kiến trúc

```text
Application
      │
 OpenRouter
      │
 ├── GPT
 ├── Claude
 ├── DeepSeek
 ├── Kimi
 ├── GLM
 └── Qwen
```

---

## Ưu điểm

* Một API
* Đổi Model nhanh
* Nhiều lựa chọn
* Giá linh hoạt

---

# 6. AI Coding Agent

Đây là thành phần quan trọng nhất trong AI Coding.

Agent sẽ:

* Đọc project
* Tìm file
* Search code
* Refactor
* Build
* Test
* Git
* Chạy Terminal
* Gọi AI

Ví dụ:

* Claude Code
* Cursor
* Cline
* Roo Code
* Continue
* GitHub Copilot
* Aider
* OpenHands

---

## Ví dụ

```text
User:
"Sửa bug Login"

↓

Agent

↓

Đọc project

↓

Tìm LoginService

↓

Đọc Database

↓

Đọc API

↓

Chỉnh nhiều file

↓

Build

↓

Test

↓

Commit
```

Model chỉ trả lời.

Agent mới là người làm việc.

---

# 7. IDE

IDE là nơi Developer lập trình.

Ví dụ:

* VS Code
* Visual Studio
* JetBrains
* Neovim

IDE kết hợp với Coding Agent để tạo thành trải nghiệm AI Coding.

Ví dụ:

```text
VS Code

↓

Cline

↓

OpenRouter

↓

DeepSeek
```

---

# 8. Quan hệ giữa các thành phần

```text
               AI MODEL
  GPT / Claude / Qwen / DeepSeek

                    │

         Runtime / API Layer

     ┌──────────────┴──────────────┐
     │                             │

 OpenRouter                    Ollama

     │                             │

     └──────────────┬──────────────┘

                    │

             Coding Agent

 Claude Code
 Cursor
 Cline
 Roo Code
 Continue
 Copilot

                    │

                   IDE

             VS Code
             Rider
             Visual Studio
```

---

## Mối quan hệ

Model

→ Sinh nội dung

Runtime

→ Chạy Model

Agent

→ Điều khiển Model

IDE

→ Nơi Developer làm việc

---

# 9. Ollama vs OpenRouter

| Tiêu chí    | Ollama                      | OpenRouter        |
| ----------- | --------------------------- | ----------------- |
| Loại        | Local Runtime               | Cloud API Gateway |
| Có Internet | Không cần sau khi tải Model | Luôn cần          |
| GPU         | Cần                         | Không cần         |
| API         | localhost                   | Cloud             |
| Chi phí     | Miễn phí                    | Theo Token        |
| Model       | Chạy Local                  | Chạy Cloud        |
| Tốc độ      | Phụ thuộc máy               | Phụ thuộc Server  |

---

## Khi nào dùng Ollama

* Muốn Offline
* Không muốn gửi dữ liệu lên Cloud
* Có GPU mạnh

---

## Khi nào dùng OpenRouter

* Muốn Model mạnh nhất
* Không có GPU
* Muốn đổi Model nhanh

---

# 10. Stack khuyến nghị & Lộ trình học

## Stack đề xuất

### IDE

* VS Code

---

### Coding Agent

* Cline
* Roo Code

---

### Cloud Model

* GPT-5
* Claude Sonnet
* Qwen3-Coder
* DeepSeek R1
* Kimi K2

---

### Local Model

* Ollama
* Qwen3-Coder

---

## Lộ trình học

### Giai đoạn 1

* AI Model
* Token
* Context Window

---

### Giai đoạn 2

* Runtime
* API
* Ollama
* OpenRouter

---

### Giai đoạn 3

* Claude Code
* Cursor
* Cline
* Roo Code

---

### Giai đoạn 4

* MCP
* Tool Calling
* RAG

---

### Giai đoạn 5

* AI Software Engineering
* Multi-Agent
* AI Architect
* AI DevOps

---

# Tổng kết

Một hệ thống AI Coding hiện đại có thể hình dung như sau:

```text
                AI Model
                    │
          Runtime / API Layer
          (Cloud hoặc Local)
                    │
            AI Coding Agent
                    │
                 IDE
                    │
               Developer
```

Hiểu đúng vai trò của từng thành phần sẽ giúp bạn:

* Chọn đúng Model.
* Chọn đúng Runtime.
* Chọn đúng Coding Agent.
* Dễ dàng thay đổi công nghệ mà không ảnh hưởng đến quy trình phát triển.
* Xây dựng môi trường AI Coding chuyên nghiệp và có khả năng mở rộng.
