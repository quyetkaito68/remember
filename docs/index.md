---
title: "REMEMBER — Personal Knowledge Base"
description: "Bảng mục lục toàn bộ kiến thức"
---

# MỤC LỤC
---

## About

- [About](/about) -- Kiến trúc tổng thể và luồng hoạt động của website REMEMBER

---

## 🤖 AI

- [AI Coding Ecosystem Handbook](/AI/AI-coding-eco-system-overview) -- Tổng quan hệ sinh thái AI Coding từ Model, Runtime, API, Coding Agent đến IDE.
- **Agent**
  - [Hướng Dẫn Kết Nối Claude Code Với Miễn Phí Qua OpenRouter](/AI/agent/claude-code-free) -- Hướng dẫn cấu hình Claude Code sử dụng model AI miễn phí thông qua OpenRouter thay vì dùng API key chính thức của Anthropic.
  - [Danh sách AI Coding Agent](/AI/agent/list-agent-code) -- Danh sách các AI Coding Agent phổ biến, sắp xếp theo thời gian ra mắt, kèm rating, giá và tính năng chính.
  - [OpenCode — AI Coding Agent](/AI/agent/opencode) -- OpenCode là AI coding agent mã nguồn mở chạy trong terminal, hỗ trợ đa model (Claude, GPT, Gemini,...) cho lập trình viên.
  - [Tối Ưu Token Cho AI Coding Agent](/AI/agent/token-optimization) -- Hướng dẫn agent-agnostic về tiết kiệm token, quản lý context window và kỹ thuật prompting cho mọi AI coding agent (opencode, Claude Code, Cline, Continue...).
  - [Token — Claude Code CLI Specific](/AI/agent/token-claude-code) -- Các kỹ thuật tiết kiệm token đặc thù cho Claude Code CLI — slash commands, CLAUDE.md, Plan Mode, Sub-agents.

---

## 💻 Computer

- **File**
  - [Markdown — Cú Pháp Cơ Bản & Nâng Cao](/computer/file/markdown) -- Tổng hợp cú pháp Markdown - text formatting, lists, code blocks, tables, images, links, task lists, và extended syntax.
  - [Mermaid — Biểu Đồ Từ Markdown](/computer/file/mermaid) -- Hướng dẫn sử dụng Mermaid - Flowchart, Sequence, Class, Gantt, Pie — render diagram trực tiếp từ Markdown.
- **Linux**
  - [Vim — Các lệnh cơ bản để chỉnh sửa file](/computer/linux/vim-command) -- 'Các thao tác Vim cơ bản nhất: mở file, edit, save, delete, select, exit, và các mode.'
  - [Nano — Các lệnh cơ bản để chỉnh sửa file](/computer/linux/nano-command) -- 'Các thao tác Nano cơ bản nhất: mở file, edit, save, search, cut, exit.'
- **Network Internet**
  - [Network & Internet Cơ Bản](/computer/network-internet/network-internet-co-ban) -- Kiến thức cơ bản về mạng máy tính và internet, bao gồm ISP, DNS, địa chỉ IP và các giao thức mạng.
- **System Admin**
  - [Tổng Quan Về PAM (Privileged Access Management)](/computer/system-admin/pam) -- 'Kiến trúc, luồng hoạt động và các giải pháp PAM dùng trong doanh nghiệp để quản lý truy cập remote vào hệ thống máy chủ'
  - [Vdi](/computer/system-admin/vdi)
- **Windows**
  - [Mklink — Symbolic Link Trên Windows](/computer/windows/mklink) -- 'Cách tạo symbolic link (symlink) trên Windows bằng lệnh mklink — trỏ folder/file ảo đến vị trí thật'
  - [Tạo Scheduled Task Trên Windows](/computer/windows/create-task) -- 'Hướng dẫn tạo task chạy định kỳ bằng Task Scheduler — ví dụ với script clean-temp.bat dọn dẹp temp hàng ngày'
  - [RAM trên Windows](/computer/windows/RAM) -- 'Hiểu toàn diện về RAM trên Windows: physical memory, virtual memory, commit, pagefile, working set, cache, memory leak, cách đọc Task Manager và các công cụ chẩn đoán.'
  - [Dọn dẹp AppData trên Windows (An toàn & Hiệu quả)](/computer/windows/don-dep-appdata-windows) -- Hướng dẫn dọn dẹp thư mục AppData trên Windows an toàn, bao gồm cache ứng dụng, file tạm và dữ liệu còn sót lại sau khi uninstall.

---

## 🗄️ Database

- **Mysql**
  - [Collation & Character Set trong MySQL](/database/mysql/collation-charset) -- Tổng quan về character set và collation trong MySQL, cách kiểm tra và xử lý lỗi khi so sánh.
  - [Get database size](/database/mysql/get-size-database) -- Truy vấn lấy kích thước dữ liệu, index và tổng dung lượng của từng bảng trong database MySQL.
  - [Kiểm tra Collation MySQL](/database/mysql/kiem-tra-collation) -- Hướng dẫn xác định các bảng và cột trong MySQL không dùng collation utf8mb4_0900_as_ci.
  - [Xử lý collation hỗn hợp trong MySQL](/database/mysql/xu-ly-collation-mix) -- Nguyên nhân, chẩn đoán và cách xử lý khi gặp tình trạng mix collation (connection/session, biến user-defined, TEXT vs VARCHAR).
  - [Backup MySQL Database với mysqldump](/database/mysql/0-backup/dump-database) -- Script dump database MySQL tự động backup cấu trúc, procedures và triggers.
  - [Restore MySQL Database](/database/mysql/1-restore/restore-database) -- Khôi phục database MySQL từ file dump .sql bằng command mysql.
  - [Lỗi retrieval of the rsa public key is not enabled for insecure connections](/database/mysql/loi-retrieval-of-the-rsa-public-key-is-not-enabled-for-insecure-connections) -- Nguyên nhân và cách khắc phục lỗi RSA public key trong MySQL khi kết nối không an toàn.

---

## 🛠️ Developer

- **Jmetter**
  - [JMeter — Chạy Test Plan Với jmeter-run.bat](/developer/jmetter/jmeter-run) -- 'Sử dụng file jmeter-run.bat để chạy JMeter non-GUI với test plan có sẵn, tự động sinh HTML report'
  - [JMeter — Tạo Test Plan Cơ Bản](/developer/jmetter/jmeter-plan) -- 'Hướng dẫn tạo test plan JMeter từ A-Z: record request, xử lý dữ liệu, trích xuất kết quả và sinh data'
  - [Performance Test — Kiến thức nền tảng & Các loại kiểm thử](/developer/jmetter/performance-test-beginner) -- 'Tổng hợp khái niệm CCU, Tenant, User, Request; công thức tính toán; mối liên hệ CCU-Thread trong JMeter; các kiểu kiểm thử performance và những điểm quan trọng thường bị bỏ sót'
  - [Bài toán Performance Test — AMIS Kiểm toán SaaS](/developer/jmetter/performance-test-example) -- 'Bài toán thực tế: xác định quy mô user/tenant, tính CCU, thiết kế kịch bản kiểm thử hiệu năng cho phần mềm kiểm toán SaaS với bzm - Concurrency Thread Group, cấu hình JMeter và thời gian chạy cụ thể'
- **Nodejs And Npm**
  - [Node.js, npm và quản lý version](/developer/nodejs-and-npm/nodejs-and-npm) -- Cài đặt Node.js, npm, quản lý nhiều version với nvm/Volta/fnm, và xử lý lỗi thường gặp
- **Performance**
  - [Performance Backend C Sharp](/developer/performance/performance-backend-c-sharp)
  - [Performance Front End](/developer/performance/performance-front-end)
- **Tool**
  - [Developer Tools](/developer/tool/dev-tool-list) -- 'Danh sách công cụ developer — dạng bảng tối giản.'

---

## 🔀 DevOps

- **Builder**
  - [Build C# Backend Solution — 3 Lệnh Dotnet Cốt Lõi](/devops/builder/build-dotnet-command) -- 'Ba lệnh dotnet clean, restore, build dùng để build project/solution C# backend trong CI/CD hoặc local'
  - [Run ASP.NET Core — Chạy Project Sau Khi Build](/devops/builder/dotnet-run) -- 'Hướng dẫn chạy file .dll của ASP.NET Core bằng CLI, thiết lập môi trường Development/Production'
- **Docker**
  - [Docker Desktop](/devops/docker/docker-desktop-config) -- 'Hướng dẫn cài đặt, cấu hình Docker Desktop để làm việc với registry nội bộ (Harbor) trong mạng local'
- **Jenkins**
  - [Jenkins](/devops/jenkins/jenkins)
- **Kafka**
  - [Apache Kafka — Thao Tác Trên Linux Server](/devops/kafka/kafka) -- 'Cài đặt, cấu hình, vận hành Kafka trên Linux — các lệnh cơ bản, xem log, xử lý sự cố'

---

## 🌿 Git

- [Git Commands — Các lệnh Git hay dùng nhất](/git/git-command) -- 'Danh sách các lệnh Git thông dụng nhất: branch, commit, reset, restore, conflict, credential — kèm giải thích ngắn gọn.'
- [Hướng dẫn sử dụng Git](/git/git-guide) -- Hướng dẫn cơ bản về Git, từ khởi tạo repository, cấu hình người dùng đến đẩy mã nguồn lên GitHub.
- [Triển khai ứng dụng React + Vite lên GitHub Pages](/git/github-page) -- Hướng dẫn triển khai ứng dụng React TypeScript với Vite lên GitHub Pages sử dụng GitHub Actions CI/CD.

---

## 📂 Organization File

- [Organization File Tool](/organization-file/README) -- Công cụ tự động phân loại và di chuyển file theo loại vào các thư mục đích trên Windows.

---

## 📐 Software Engineering

- [Bản Đồ Thế Giới Phần Mềm](/software/software-overview) -- Tổng quan toàn cảnh thế giới phần mềm — từ nhu cầu người dùng đến cách phần mềm đến tay người dùng.
- [Các Loại Phần Mềm](/software/software-types) -- Hệ thống phân loại phần mềm — System, Application, Embedded, và mối quan hệ giữa chúng.
- [Kiến Trúc Phần Mềm](/software/software-architecture) -- Cách một phần mềm được tổ chức bên trong — từ mô hình-layered đến microservices.
- [Chu Kỳ Sống Phần Mềm](/software/software-lifecycle) -- Phần mềm đi qua các giai đoạn — từ ý tưởng đến bảo trì, retirement. Quy trình SDLC và DevOps.

---

## ⚡ Utilities Script

- [Clean Temp Windows](/utilities-script/clean-temp) -- Hướng dẫn cách clear temp với 1 click giải phóng disk windows
