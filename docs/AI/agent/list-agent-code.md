---
title: Danh sách AI Coding Agent
description: Danh sách các AI Coding Agent phổ biến, sắp xếp theo thời gian ra mắt, kèm rating, giá và tính năng chính.
tags: [ai, coding, agent, list]
category: ai
order: 2
updated: 2026-07-05
---

# Danh sách AI Coding Agent

> Cập nhật: 2026-07-05

## Bảng tổng hợp

| #  | Agent             | Nhà cung cấp          | Ra mắt        | Rating / Đánh giá           | Free Tier                   | Giá Pro               | Tính năng chính |
| -- | ----------------- | --------------------- | ------------- | --------------------------- | --------------------------- | --------------------- | --------------- |
| 1  | **GitHub Copilot** | Microsoft / GitHub    | 06/2021       | 4.5/5 G2 (147 reviews)      | 2000 completions, 50 chat/mo | $10/mo (Pro)          | Autocomplete mạnh nhất, hỗ trợ 10+ IDE, native GitHub integration (Issue→PR), Agent mode, IP indemnity, JetBrains native |
| 2  | **Tabnine**       | Tabnine (Codota)      | 2018          | 4.2/5 G2                    | Không                       | $39/mo               | Privacy-first, enterprise, air-gapped, on-prem, multi-model |
| 3  | **Replit Agent**  | Replit                | 2023          | 4.3/5 G2                    | Free (limited)              | $25/mo               | Cloud IDE + agent, full-stack app generation, Ghostwriter autocomplete, deploy built-in |
| 4  | **Amazon Q Developer** | Amazon Web Services | 2023 (CodeWhisperer→Q) | 4.0/5 G2         | Generous free               | $19/mo               | AWS deep integration, Java refactoring chuyên sâu, enterprise |
| 5  | **Cursor**        | Anysphere             | 03/2023       | 9.0/10 (tooltester), 78% sat. | 2000 completions, 50 slow req | $20/mo               | VS Code fork AI-native, Composer (multi-file agent), 200K context, background agents, MCP support, parallel sub-agents |
| 6  | **Gemini Code Assist** | Google             | 2024          | 4.4/5 G2 (39 reviews)       | Free (limited)              | $19.99/mo (AI Pro)   | Google Cloud integration, BigQuery/Vertex AI, multi-IDE |
| 7  | **Sourcegraph Cody** | Sourcegraph         | 2023          | 4.5/5 G2 (68 reviews)       | Free (limited)              | $9/mo                | Codebase indexing mạnh nhất, Slack/Teams integration, context-aware |
| 8  | **Continue**      | Continue Dev (OSS)    | 2024          | Open source                 | Free (BYOM)                 | Free + API cost      | Open-source IDE plugin, BYOLLM, Mission Control UI, cloud agent |
| 9  | **Devin**         | Cognition Labs        | 03/2024       | N/A                         | Không                       | $500+/mo (ACUs)      | Autonomous cloud SWE, ticket→PR, multi-day tasks, cloud sandbox |
| 10 | **Windsurf**      | Codeium (→OpenAI 04/2025) | 09/2024   | 8.2/10, 78% sat.           | Unlimited autocomplete, 25 credits | $15/mo (500 credits) | Cascade agent, Riptide indexing, SWE-1.5 model, parallel multi-session, terminal turbo mode |
| 11 | **Aider**         | Paul Gauthier (OSS)    | 2024          | Open source popular          | Free + API cost             | Free (BYOM)          | Terminal CLI, git-native (auto commit), voice input, BYOLLM, surgical edits |
| 12 | **Cline**         | Cline (OSS)            | 08/2024       | 5M+ VS Code installs        | Free + API cost             | Free (BYOM)          | VS Code extension, transparent token usage, BYOLLM, terminal access, MCP |
| 13 | **Claude Code**   | Anthropic              | 02/2025       | 9.3/10, 84% sat., 4.3/5 G2 | Không                       | $20/mo               | CLI agent, SWE-bench 80.8% (cao nhất), 1M context, plan mode, MCP, Agent Teams, hooks |
| 14 | **Roo Code**      | Roo (OSS)              | 2025          | Open source                 | Free + API cost             | Free (BYOM)          | VS Code extension, cloud agents, fork of Cline |
| 15 | **OpenAI Codex CLI** | OpenAI             | 04/2025       | N/A                         | MIT License (code) + API    | Included ChatGPT Pro | CLI agent, MIT license, async cloud agent, PR automation, Agents SDK |
| 16 | **OpenHands**     | All Hands AI (OSS)     | 2024          | SWE-bench 53.0% (v0.38)    | Free (OSS) + API cost       | Free (BYOM)          | Self-hosted cloud agent, model-agnostic, Docker sandbox |
| 17 | **Antigravity**   | Google                | 2026          | N/A (free preview)          | Free                        | Free (hiện tại)      | Google AI IDE, Gemini-powered, multi-agent orchestration, CLI + VS Code ext |
| 18 | **JetBrains Junie** | JetBrains           | 2025          | 73% sat.                    | Limited                     | $10/mo               | Deep JetBrains IDE integration, code analysis native |
| 19 | **v0 by Vercel**  | Vercel                | 2024          | 4.3/5 G2                    | Free (limited)              | Pay-as-you-go        | React component generation, shadcn/ui native, web UI |
| 20 | **Bolt.new**      | StackBlitz            | 2024          | N/A                         | Free (limited)              | Pay-as-you-go        | WebContainer browser full-stack, Node.js in browser, no setup |
| 21 | **OpenCode**      | opencode.ai (cộng đồng) | 2025          | N/A                         | Free (full)                 | Free (full)          | TUI native, ACP (Agent Control Protocol), plugins, open-source, BYOM |


## Ghi chú

- **BYOM** = Bring Your Own Model (tự mang API key model)
- **Rating**: dựa trên G2 (star/5), tooltester24 (điểm/10), fungies.io (satisfaction %), hoặc dữ liệu từ báo cáo người dùng
- **Ra mắt**: thời điểm phiên bản đầu tiên ra công chúng (có thể beta/preview)
- **Free model**: hầu hết các agent đều dùng chung model từ OpenAI, Anthropic, Google — không có "free model" riêng; agent chỉ là lớp điều khiển

## Agent + Model Free mà agent đó có thể dùng

Hầu hết agent không cung cấp model miễn phí. Người dùng tự cung cấp API key hoặc dùng:

- **Local**: Ollama + Qwen3-Coder, DeepSeek, Llama (free, chạy local)
- **Cloud free**: Gemini API (free tier), OpenRouter (có model free)
- **Agent free + BYOM**: Cline, Roo Code, Continue, Aider, OpenHands
- **Agent free tier tích hợp sẵn**: Windsurf (25 credits/mo), Cursor (2000 completions), GitHub Copilot (50 chat/mo)
