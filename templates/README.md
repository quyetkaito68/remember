# Templates — Viết Markdown Chuẩn Cho REMEMBER

Bộ template này giúp **human** và **AI agent** viết markdown đồng nhất cấu trúc, đúng frontmatter, đúng quy ước của project.

## Cách dùng

1. Copy template phù hợp vào thư mục `docs/<category>/`
2. Đổi tên file `.template.md` → `<tên-bài>.md`
3. Điền nội dung theo hướng dẫn trong `<!-- AI: … -->`
4. Xoá các comment hướng dẫn sau khi hoàn thành

## Danh sách template

| Template | Dùng cho | Ví dụ trong project |
|----------|----------|---------------------|
| `tutorial-guide.template.md` | Hướng dẫn từng bước | Git guide, Windows maintenance, Network basics |
| `topic-overview.template.md` | Tổng quan chủ đề, kiến trúc | AI Coding Ecosystem Handbook |
| `technical-reference.template.md` | Vấn đề kỹ thuật, chẩn đoán, fix lỗi | MySQL collation, error troubleshooting |
| `script-documentation.template.md` | Script, công cụ, file config | Backup/restore database, clean-temp, organize-file |

## Quy tắc chung

### Frontmatter — tất cả file markdown

```yaml
---
title: Tiêu đề                  # BẮT BUỘC — hiển thị sidebar & trình duyệt
description: Mô tả 1-2 câu       # BẮT BUỘC — SEO & search
tags: [tag1, tag2]                  # BẮT BUỘC — YAML array, lowercase
category: 'tên-thư-mục'            # KHUYẾN NGHỊ — tên folder chứa file
updated: YYYY-MM-DD                # BẮT BUỘC — ngày viết/sửa
order: 1                           # TÙY CHỌN — vị trí sidebar (mặc định 999)
---
```

### Nội dung

- Viết tiếng Việt **có dấu**
- Code block **luôn** có language identifier: ` ```bash`, ` ```sql`, ` ```powershell`
- Heading hierarchy: `#` → `##` → `###` (không nhảy cấp, không skip)
- Dùng `---` giữa các section lớn
- Dùng `<!-- comment -->` để chứa hướng dẫn cho AI agent (xoá khi hoàn thành)
- ASCII diagram dùng ```text
- Table format: `| header | header |` + `|--------|--------|`

### Đặt tên file

- `kebab-case.md` (viết thường, gạch ngang)
- Dùng tiếng Anh hoặc tiếng Việt không dấu
- Ví dụ: `collation-charset.md`, `xu-ly-collation-mix.md`, `github-page.md`
