---
name: markdown-doc-generator
description: Tạo tài liệu markdown tiếng Việt có dấu, hỗ trợ sơ đồ ASCII/unicode (kiến trúc, cây thư mục), tóm tắt code/project, sinh document nhanh chóng. Sử dụng skill này KHI user yêu cầu: viết document/readme, tóm tắt code/base code, vẽ sơ đồ kiến trúc/folder tree, tạo tài liệu kỹ thuật tiếng Việt. Skill này luôn ưu tiên tiếng Việt có dấu, định dạng markdown chuẩn, sơ đồ trực quan.
---

# Markdown Documentation Generator Skill

Tạo tài liệu markdown tiếng Việt có dấu. Hỗ trợ: tóm tắt codebase, reformat doc, templates (README, API, ADR, Changelog...), sơ đồ ASCII/Mermaid.

---

## Workflow

```
User Request → Phân tích context → Chọn mode → Thu thập dữ liệu → Sinh document → Ghi file .md
```

### Modes

| Mode | Trigger keywords | Mô tả |
|------|------------------|-------|
| `doc-gen` | viết document, tạo readme, tạo docs, tài liệu | Sinh tài liệu hoàn chỉnh từ code/context |
| `summarize` | tóm tắt, summarize, summary, overview, tổng quan | Tóm tắt codebase/project |
| `diagram` | sơ đồ, diagram, architecture, tree, folder structure, kiến trúc | Vẽ sơ đồ (Mermaid hoặc ASCII) |
| `template` | dùng template, mẫu, boilerplate | Áp dụng template có sẵn, fill placeholders |
| `reformat` | trình bày lại, format lại, viết lại, tái cấu trúc, làm lại document | Đọc file .md có sẵn → viết lại đúng chuẩn |

---

## 1. Mode: `doc-gen`

**Input**: Path thư mục/project, hoặc mô tả yêu cầu
**Output**: File markdown hoàn chỉnh

**Quy trình**:
1. **Quét context**: Dùng `Glob`/`Grep`/`Read` để hiểu cấu trúc project
2. **Xác định loại doc**: README / API / ADR / Technical Spec / Changelog
3. **Thu thập dữ liệu**:
   - Package files → dependencies
   - Entry points (main, index, app) → flow chính
   - Config files → cấu hình
   - Tests → patterns
   - Git history → changelog
4. **Sinh nội dung** theo template tương ứng (xem `references/templates.md`)
5. **Ghi file**

---

## 2. Mode: `summarize`

**Input**: Path thư mục/file cụ thể
**Output**: Tóm tắt bằng tiếng Việt có dấu

**Cấu trúc**:
- **Mục đích**: 1-2 câu
- **Kiến trúc**: Bullet points + diagram ngắn
- **Tech stack**: Table
- **Điểm nổi bật**: 3-5 items

---

## 3. Mode: `diagram` — Mermaid vs ASCII

**Chọn loại diagram theo độ phức tạp:**

| Loại diagram | Nên dùng | Lý do |
|---|---|---|
| Folder tree, kiến trúc nhỏ (< 10 node) | **ASCII** (`text` block) | Đơn giản, không cần render, luôn hiển thị |
| Sequence diagram, flow chart phức tạp | **Mermaid** (``` ```mermaid````) | Dễ đọc, dễ bảo trì, VitePress render đẹp |
| Gantt, timeline, pie chart | **Mermaid** | ASCII không làm được |
| ER diagram, class diagram | **Mermaid** | Quan hệ phức tạp |
| Cây thư mục | **ASCII** (`├──`, `└──`) | Không có Mermaid equivalent |
| Architecture > 10 node | **Mermaid** | Tránh lộn xộn khi vẽ tay |

**Quy tắc vẽ ASCII**: Load skill `ascii-diagram` để biết rules (đếm ký tự, equal-width borders, cấm Unicode lệch width, max 80 ký tự, max 30 dòng).

**Language hint**: Luôn dùng `text` cho ASCII diagrams, `mermaid` cho Mermaid diagrams.

---

## 4. Mode: `template`

Có 2 kho template riêng biệt — chọn theo mục đích:

### 4A. Tạo file xuất — `references/templates.md`

Dùng khi sinh file output (README, API docs, ADR...) từ code/context.

**Cách dùng**: Chọn template name → xem cấu trúc trong `references/templates.md` → dùng `Glob`/`Read`/`Grep` lấy dữ liệu thực tế từ project → thay thế `{placeholder}` → ghi file `.md`.

| Template | Mục đích |
|----------|----------|
| `readme` | README.md GitHub |
| `api-docs` | API Documentation |
| `architecture` | Architecture Decision Record |
| `changelog` | Changelog (Keep a Changelog) |
| `contributing` | Contributing Guide |
| `tech-spec` | Technical Specification |
| `meeting-notes` | Meeting Notes / RFC |

### 4B. Khung viết content — `templates/` (project root)

Dùng khi user muốn viết bài mới cho REMEMBER knowledge base (trigger: "viết bài mới", "tạo guide", "thêm tài liệu").

**Cách dùng**: Copy `.template.md` từ `templates/` → thư mục `docs/<category>/` → đổi tên `<slug>.md` → điền nội dung theo hướng dẫn `<!-- AI: … -->` → xoá comment.

| Template | Dùng cho |
|----------|----------|
| `tutorial-guide.template.md` | Hướng dẫn từng bước (Git, Windows, Network) |
| `topic-overview.template.md` | Tổng quan chủ đề, kiến trúc |
| `technical-reference.template.md` | Vấn đề kỹ thuật, chẩn đoán, fix lỗi |
| `script-documentation.template.md` | Script, tool, file config |

---

## 5. Mode: `reformat`

**Input**: Path file `.md` có sẵn → đọc → phân tích → viết lại đúng chuẩn:
- Frontmatter đúng format (nếu VitePress project)
- Heading hierarchy: H1 → H2 → H3, không skip level
- Code block luôn có language hint
- Table đúng header separator
- List dùng `-` nhất quán, indent 2 spaces
- Note/Warning tách riêng
- Loại bỏ redundant, giữ đủ ý

**Ghi đè file gốc hoặc tạo file mới.**

---

## Tiếng Việt có dấu

- ✅ Dùng đầy đủ dấu: "Tóm tắt", "Kiến trúc", "Cài đặt"
- ✅ Viết hoa đầu câu, tên riêng, viết tắt (API, DB, CI/CD)
- ❌ Không dùng không dấu: "Tom tat", "Kien truc"
- ❌ Không Việt-glish lỏng lẻo

Thuật ngữ chuẩn: Repository (kho chứa), Branch (nhánh), Commit (ghi nhận), Deploy (triển khai), Middleware (phần trung gian), Endpoint (điểm cuối).

---

## Scripts hỗ trợ

Thư mục `scripts/`:
- `generate-tree.py` — Sinh folder tree ASCII từ đường dẫn
- `analyze-project.py` — Phân tích project, trích xuất metadata

Gọi script khi cần thay vì tự implement.

---

## Lưu ý

1. **Luôn đọc context trước** — không đoán mò, dùng tools để hiểu project
2. **Ưu tiên script có sẵn** — `generate-tree.py` / `analyze-project.py`
3. **Tiếng Việt có dấu** — kiểm tra output trước khi ghi file
4. **File đơn lẻ** — gom vào 1 file .md trừ khi user yêu cầu tách
5. **Metadata cuối file** — thêm dòng "*Tài liệu được tạo bởi <git-username> - [Ngày tạo]*"
