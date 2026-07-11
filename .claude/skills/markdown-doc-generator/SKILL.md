---
name: markdown-doc-generator
description: Tạo tài liệu markdown tiếng Việt có dấu, hỗ trợ sơ đồ ASCII/unicode (kiến trúc, cây thư mục), tóm tắt code/project, sinh document nhanh chóng. Sử dụng skill này KHI user yêu cầu: viết document/readme, tóm tắt code/base code, vẽ sơ đồ kiến trúc/folder tree, tạo tài liệu kỹ thuật tiếng Việt. Skill này luôn ưu tiên tiếng Việt có dấu, định dạng markdown chuẩn, sơ đồ trực quan.
---

# Markdown Documentation Generator Skill

Skill tạo tài liệu markdown chuyên nghiệp bằng tiếng Việt có dấu, hỗ trợ:
- **Sơ đồ ASCII/Unicode**: Kiến trúc hệ thống, folder tree, sequence diagram, flow chart
- **Tóm tắt thông minh**: Phân tích codebase, trích xuất điểm chính, sinh summary
- **Template đa dạng**: README, API docs, Architecture, Changelog, Contributing, Technical Spec
- **Output**: File `.md` đơn lẻ, sẵn sàng commit

---

## Workflow chính

```
User Request → Phân tích context → Chọn mode → Thu thập dữ liệu → Sinh document → Ghi file .md
```

### Các Mode hoạt động

| Mode | Trigger keywords | Mô tả |
|------|------------------|-------|
| `doc-gen` | viết document, tạo readme, tạo docs, tài liệu | Sinh tài liệu hoàn chỉnh từ code/context |
| `summarize` | tóm tắt, summarize, summary, overview, tổng quan | Tóm tắt codebase/project |
| `diagram` | sơ đồ, diagram, architecture, tree, folder structure, kiến trúc | Vẽ sơ đồ ASCII/unicode |
| `template` | dùng template, mẫu, boilerplate | Áp dụng template có sẵn |
| `reformat` | trình bày lại, format lại, viết lại, tái cấu trúc, làm lại document | Đọc file .md có sẵn → viết lại đúng chuẩn markdown |

---

## Hướng dẫn chi tiết cho từng Mode

### 1. Mode: `doc-gen` - Tạo tài liệu hoàn chỉnh

**Input**: Path thư mục/project, hoặc mô tả yêu cầu
**Output**: File markdown hoàn chỉnh

**Quy trình**:
1. **Quét context**: Dùng `Glob`/`Grep`/`Read` để hiểu cấu trúc project
2. **Xác định loại doc**: README / API / Architecture / Technical Spec / Changelog
3. **Thu thập dữ liệu**:
   - Package.json, Cargo.toml, go.mod, requirements.txt → dependencies
   - Entry points (main, index, app) → flow chính
   - Config files → cấu hình
   - Tests → coverage, patterns
   - Git history (nếu có) → changelog
4. **Sinh nội dung** theo template phù hợp (xem section Templates)
5. **Ghi file** với tên mặc định hoặc do user chỉ định

### 2. Mode: `summarize` - Tóm tắt codebase

**Input**: Path thư mục/file cụ thể
**Output**: Section "Tóm tắt" có thể nhúng vào doc lớn hoặc file riêng

**Quy trình**:
1. Đọc các file quan trọng (entry points, core modules, config)
2. Trích xuất:
   - Mục đích project
   - Kiến trúc tổng quát (layers, modules)
   - Tech stack chính
   - Data flow quan trọng
   - API endpoints / Public interfaces
   - Dependencies ngoài
3. Viết tóm tắt bằng tiếng Việt có dấu, cấu trúc:
   - **Mục đích**: 1-2 câu
   - **Kiến trúc**: Bullet points + mini diagram
   - **Tech stack**: Table
   - **Điểm nổi bật**: 3-5 items

### 3. Mode: `diagram` - Vẽ sơ đồ ASCII/Unicode

**Input**: Loại sơ đồ + dữ liệu/context
**Output**: Sơ đồ markdown code block

**Các loại sơ đồ hỗ trợ**:

#### Folder Tree (Cây thư mục)
```
project-root/
├── src/
│   ├── components/
│   │   ├── Header.tsx
│   │   └── Footer.tsx
│   ├── hooks/
│   │   └── useAuth.ts
│   ├── pages/
│   │   ├── Home.tsx
│   │   └── Dashboard.tsx
│   └── main.tsx
├── public/
│   └── index.html
├── package.json
├── tsconfig.json
└── README.md
```

#### Architecture Diagram (Kiến trúc hệ thống)
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│  API Gateway│────▶│  Services   │
│  (React)    │     │  (Kong)     │     │  (Go/Node)  │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                    ┌─────────────┐            │
                    │  Database   │◀───────────┘
                    │ (PostgreSQL)│
                    └─────────────┘
```

#### Sequence Diagram (Luồng tương tác)
```
User → Frontend: Click "Đăng nhập"
Frontend → Auth Service: POST /login {email, pass}
Auth Service → DB: SELECT * FROM users WHERE email=?
DB → Auth Service: User record
Auth Service → Frontend: JWT Token
Frontend → User: Redirect Dashboard
```

#### Flow Chart (Luồng xử lý)
```
    ┌─────────────┐
    │   Start     │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐     Yes    ┌─────────────┐
    │ Valid Input?│───────────▶│  Process    │
    └──────┬──────┘            └──────┬──────┘
           │ No                       │
           ▼                          ▼
    ┌─────────────┐            ┌─────────────┐
    │  Return     │            │  Save/Return│
    │  Error      │            │  Result     │
    └─────────────┘            └─────────────┘
```

### 4. Mode: `template` - Áp dụng template

**Templates có sẵn** (xem `references/templates.md`):
- `readme` - README.md chuẩn GitHub
- `api-docs` - API Documentation
- `architecture` - Architecture Decision Record (ADR)
- `changelog` - Changelog (Keep a Changelog format)
- `contributing` - Contributing Guide
- `tech-spec` - Technical Specification
- `meeting-notes` - Meeting Notes / RFC

### 5. Mode: `reformat` - Viết lại document

**Input**: Path file `.md` có sẵn
**Output**: File markdown được viết lại đúng chuẩn cấu trúc

**Trigger keywords**: "trình bày lại", "format lại", "viết lại", "tái cấu trúc", "làm lại document"

**Quy trình**:
1. **Đọc file** hiện tại bằng `Read` tool
2. **Phân tích nội dung**:
   - Xác định loại document (hướng dẫn, reference, overview, v.v.)
   - Trích xuất thông tin quan trọng: steps, commands, notes, warnings
   - Nhận diện cấu trúc hiện tại: heading, code block, table, list
3. **Viết lại** theo chuẩn:
   - **Frontmatter**: đúng format (nếu là VitePress project)
   - **Heading hierarchy**: H1 → H2 → H3, không nhảy cấp
   - **Code block**: luôn có language hint (`bash`, `powershell`, `json`, ...)
   - **Table**: đúng định dạng markdown, header separator
   - **List**: nhất quán bullet/number, indent đúng
   - **Section "Lưu ý"**: tách riêng warnings/notes quan trọng
   - **Ngắn gọn**: loại bỏ redundant, giữ đủ ý
4. **Ghi đè file** hoặc tạo file mới theo yêu cầu

**Quy tắc format**:

| Element | Quy tắc |
|---------|---------|
| Heading | `# Title` → `## Section` → `### Subsection`, không skip level |
| Code | Fenced block với language: `` ```bash ``, `` ```powershell `` |
| Command | Luôn trong code block, có thể thêm mô tả trước |
| Table | Header + separator + rows, align đúng |
| List | Dùng `-` thống nhất, indentation 2 spaces |
| Note/Warning | Tách thành section riêng hoặc dùng blockquote `>` |
| Link | Internal: `[text](path)`, External: `[text](url)` |

**Ví dụ trước/sau**:

Trước (messy):
```
cài nodejs rồi chạy npm install
npm run dev để start
lưu ý: phải cài python trước
```

Sau (reformatted):
```markdown
## Cài đặt

1. Cài Node.js
2. Chạy `npm install`

## Khởi động

```bash
npm run dev
```

> **Lưu ý**: Phải cài Python trước khi chạy.
```

---

## Templates chi tiết

Xem file: `references/templates.md`

---

## Sơ đồ ASCII/Unicode - Quy tắc vẽ

### Ký tự Unicode khuyến nghị (hiển thị đẹp trên mọi terminal)

| Mục đích | Ký tự | Ví dụ |
|----------|-------|-------|
| Góc trên trái | `┌` | `┌─────────┐` |
| Góc trên phải | `┐` | |
| Góc dưới trái | `└` | `└─────────┘` |
| Góc dưới phải | `┘` | |
| Ngang | `─` | `─────────` |
| Dọc | `│` | `│ Content │` |
| Tраз trái | `├` | `├─────────┤` |
| Traz phải | `┤` | |
| Traz trên | `┬` | |
| Traz dưới | `┴` | |
| Chéo | `┼` | |
| Cây thư mục | `├──`, `└──`, `│   ` | `├── folder/` |

### Quy tắc:
1. **Luôn dùng Unicode box-drawing** cho diagram kiến trúc/sequence/flow
2. **Dùng ASCII tree** (`├──`, `└──`) cho folder tree
3. **Độ rộng tối đa**: 100 ký tự (fit terminal chuẩn)
4. **Label tiếng Việt có dấu** trong diagram
5. **Wrap trong code block markdown** với language hint: `text` hoặc `ascii`

---

## Tiếng Việt có dấu - Quy tắc

### Bắt buộc:
- ✅ Tiếng Việt có dấu đầy đủ: "Tóm tắt", "Kiến trúc", "Cài đặt", "Cấu hình"
- ✅ Dùng từ vựng kỹ thuật chuẩn: "dependency" (thư viện phụ thuộc), "endpoint" (điểm cuối), "middleware" (phần trung gian)
- ✅ Viết hoa chữ cái đầu câu, tên riêng, viết tắt (API, DB, UI, CI/CD)

### Tránh:
- ❌ Tiếng Việt không dấu: "Tom tat", "Kien truc", "Cai dat"
- ❌ Việt-glish lỏng lẻo: "Project này có architecture tốt" → "Dự án này có kiến trúc tốt"
- ❌ Dịch ý nghĩa sai: "commit" → "gửi" (nên dùng "commit" hoặc "ghi nhận thay đổi")

### Thuật ngữ chung (giữ nguyên hoặc dịch chuẩn):
| English | Việt Nam (có dấu) |
|---------|-------------------|
| Repository | Kho chứa / Repository |
| Branch | Nhánh |
| Commit | Commit / Ghi nhận |
| Merge | Gộp / Merge |
| Deploy | Triển khai |
| Pipeline | Quy trình / Pipeline |
| Middleware | Middleware / Phần trung gian |
| Endpoint | Endpoint / Điểm cuối API |

---

## Output Format

File markdown xuất ra TUÂN THỦ cấu trúc:

```markdown
# [Tiêu đề chính]

> **Tóm tắt**: [1-2 câu mô tả nhanh]

## Mục lục
- [Phần 1](#phần-1)
- [Phần 2](#phần-2)

---

## Phần 1: [Tên phần]

### Nội dung chi tiết

#### Sơ đồ (nếu có)
```text
[ASCII/Unicode diagram]
```

#### Code example (nếu có)
```language
[code]
```

#### Bảng thông tin (nếu có)
| Cột 1 | Cột 2 |
|-------|-------|
| Data  | Data  |

---

## Phần 2: [Tên phần]
...

---

*Tài liệu được tạo tự động bởi Markdown Doc Generator - [Ngày tạo]*
```

---

## Scripts hỗ trợ

Xem thư mục `scripts/`:
- `generate-tree.py` - Sinh folder tree từ đường dẫn
- `analyze-project.py` - Phân tích project, trích xuất metadata
- `diagram-generator.py` - Sinh các loại diagram từ spec đơn giản

**Usage**: Skill sẽ tự gọi script phù hợp thay vì viết diagram thủ công.

---

## Ví dụ thực tế

### User: "Tạo README cho project này"
```
→ Mode: doc-gen + template readme
→ Quét project → Sinh README.md
```

### User: "Tóm tắt codebase src/auth"
```
→ Mode: summarize
→ Đọc src/auth/ → Sinh SUMMARY.md
```

### User: "Vẽ sơ đồ kiến trúc hệ thống"
```
→ Mode: diagram (architecture)
→ Hỏi thêm chi tiết nếu cần → Sinh ARCHITECTURE.md
```

### User: "Tạo doc API cho REST endpoints"
```
→ Mode: doc-gen + template api-docs
→ Quét routes/controllers → Sinh API_DOCS.md
```

### User: "Trình bày lại tài liệu dotnet-run.md"
```
→ Mode: reformat
→ Đọc dotnet-run.md → Viết lại đúng chuẩn markdown → Ghi đè file
```

---

## Lưu ý quan trọng

1. **Luôn đọc context trước** - không đoán mò, dùng tools để hiểu project
2. **Ưu tiên script có sẵn** - sinh tree/diagram bằng script, không viết tay
3. **Tiếng Việt có dấu** - kiểm tra output trước khi ghi file
4. **File đơn lẻ** - gom mọi thứ vào 1 file .md trừ khi user yêu cầu tách
5. **Metadata cuối file** - luôn thêm dòng "Tài liệu được tạo tự động..."
6. **Idempotent** - chạy lại không bị duplicate content