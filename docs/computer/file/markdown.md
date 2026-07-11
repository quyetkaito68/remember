---
title: Markdown — Cú Pháp Cơ Bản & Nâng Cao
description: Tổng hợp cú pháp Markdown - text formatting, lists, code blocks, tables, images, links, task lists, và extended syntax.
tags: [markdown, syntax, formatting]
category: computer/file
updated: 2026-07-11
order: 1
---

# Markdown — Cú Pháp Cơ Bản & Nâng Cao

> Markdown là ngôn ngữ đánh dấu lightweight, chuyển đổi thành HTML. Được dùng rộng rãi trong documentation, blog, GitHub README, và nhiều nền tảng khác.

---

## Tổng quan

**Tại sao dùng Markdown?**
- Đơn giản — viết text thuần, không tag HTML
- Portable — hoạt động trên mọi nền tảng, mọi tool
- Version control-friendly — diff rõ ràng
- Hỗ trợ rộng rãi — GitHub, GitLab, Notion, VS Code, VitePress, Jekyll...

**Flavor phổ biến:**
- **GitHub Flavored Markdown (GFM)** — GitHub, GitLab
- **CommonMark** — chuẩn chung
- **Pandoc Markdown** — nâng cao, conversion

---

## Text Formatting — Định dạng văn bản

### In nghiêng, đậm, gạch ngang

```text
    *In nghiêng* hoặc _In nghiêng_
    **Đậm** hoặc __Đậm__
    ***Đậm + nghiêng***
    ~~Gạch ngang~~
```

| Cú pháp | Kết quả |
|---------|---------|
| `*text*` | *In nghiêng* |
| `**text**` | **Đậm** |
| `***text***` | ***Đậm + nghiêng*** |
| `~~text~~` | ~~Gạch ngang~~ |
| `` `code` `` | `Inline code` |

---

## Headings — Tiêu đề

```text
    # Heading 1
    ## Heading 2
    ### Heading 3
    #### Heading 4
    ##### Heading 5
    ###### Heading 6
```

> **Mẹo:** Dùng `##` cho phần chính, `###` cho mục con. Tránh nhảy cấp (ví dụ từ `#` sang `###`).

---

## Links — Liên kết

```text
    [Text hiển thị](https://example.com)
    [Text với title](https://example.com "Tooltip")
    [Relative link](./relative-path.md)
    [Anchor link](#heading-name)
```

| Loại | Ví dụ |
|------|-------|
| URL đầy đủ | `[Google](https://google.com)` |
| Relative | `[Readme](./README.md)` |
| Anchor | `[Section](#section-name)` |

---

## Images — Hình ảnh

```text
    ![Alt text](path/to/image.png)
    ![Alt text](path/to/image.png "Title")
    <img src="path/to/image.png" width="200">
```

| Cú pháp | Ghi chú |
|---------|---------|
| `![Alt](url)` | Markdown image |
| `![Alt](url "title")` | Có tooltip |
| `<img>` tag | Kiểm soát width/height |

---

## Lists — Danh sách

### Unordered list

```text
    - Item 1
    - Item 2
      - Sub-item 2a
      - Sub-item 2b
    - Item 3
```

Kết quả:
- Item 1
- Item 2
  - Sub-item 2a
  - Sub-item 2b
- Item 3

### Ordered list

```text
    1. First
    2. Second
    3. Third
```

Kết quả:
1. First
2. Second
3. Third

> **Lưu ý:** Số thứ tự không quan trọng — Markdown tự render đúng số. Viết `1. 1. 1.` cũng ra `1. 2. 3.`

### Task list

```text
    - [x] Hoàn thành
    - [ ] Chưa làm
    - [ ] Cần làm tiếp
```

Kết quả:
- [x] Hoàn thành
- [ ] Chưa làm
- [ ] Cần làm tiếp

---

## Code — Mã nguồn

### Inline code

```text
    Use `console.log()` to debug.
```

Kết quả: Use `console.log()` to debug.

### Fenced code block

```text
    ```language
    code here
    ```
```

Ví dụ:

```javascript
function greet(name) {
  return `Hello, ${name}!`
}
```

### Code block với title

Một số flavor hỗ trợ title cho code block:

```text
    ```javascript title="greet.js"
    function greet(name) {
      return `Hello, ${name}!`
    }
    ```
```

### Indented code block

Cũng dùng được — indent 4 space hoặc 1 tab:

```text
        code here (indented 4 spaces)
```

---

## Tables — Bảng

```text
    | Cột 1 | Cột 2 | Cột 3 |
    |-------|-------|-------|
    | A     | B     | C     |
    | D     | E     | F     |
```

| Cột 1 | Cột 2 | Cột 3 |
|-------|-------|-------|
| A     | B     | C     |
| D     | E     | F     |

### Alignment

```text
    | Left | Center | Right |
    |:-----|:------:|------:|
    | a    | b      | c     |
    | d    | e      | f     |
```

| Left | Center | Right |
|:-----|:------:|------:|
| a    | b      | c     |
| d    | e      | f     |

| Ký hiệu | Vị trí |
|---------|--------|
| `:---` | Left align |
| `:---:` | Center align |
| `---:` | Right align |

---

## Blockquote — Trích dẫn

```text
    > This is a blockquote.
    > 
    > Multiple paragraphs.
```

> This is a blockquote.
>
> Multiple paragraphs.

### Nested blockquote

```text
    > Level 1
    > > Level 2
    > > > Level 3
```

> Level 1
> > Level 2
> > > Level 3

---

## Horizontal Rule — Đường kẻ ngang

```text
    ---
    ***
    ___
```

Ba cách trên đều tạo đường kẻ ngang:

---

## Line Breaks — Ngắt dòng

```text
    Dòng 1
    Dòng 2         ← cách nhau 2 space → xuống dòng trong HTML

    Dòng 3

    Dòng 4         ← cách nhau 1 dòng trống → paragraph mới
```

> **Mẹo:** Trong Markdown renderer, một dòng trống = paragraph mới. Muốn `<br/>` thì thêm 2 space ở cuối dòng.

---

## HTML trong Markdown

Markdown cho phép nhúng HTML trực tiếp:

```text
    <details>
    <summary>Click để mở</summary>
    
    Nội dung ẩn bên trong.
    
    </details>
```

Kết quả:

<details>
<summary>Click để mở</summary>

Nội dung ẩn bên trong.

</details>

### Các tag thường dùng

| Tag | Công dụng |
|-----|-----------|
| `<details>/<summary>` | Foldable section |
| `<br>` | Xuống dòng |
| `<img>` | Hình ảnh với width/height |
| `<kbd>` | Keyboard shortcut |
| `<sup>/<sub>` | Superscript/subscript |

### Ký hiệu đặc biệt

```text
    &amp;   → &
    &lt;    → <
    &gt;    → >
    &copy;   → ©
    &nbsp;   → khoảng trắng
```

---

## Escape Characters — Ký tự thoát

```text
    \*not italic\*
    \# not heading
    \[not a link\]
```

Dùng `\` trước ký tự đặc biệt để hiển thị thô.

---

## Extended Syntax — Nâng cao

### Strikethrough (GFM)

```text
    ~~deleted text~~
```

### Table of Contents

Một số tool tự tạo TOC:

```text
    ## Table of Contents
    - [Section 1](#section-1)
    - [Section 2](#section-2)
```

### Footnotes

```text
    This has a footnote[^1].

    [^1]: This is the footnote content.
```

### Definition List

```text
    Term
    :   Definition here
```

---

## Markdown trong IDE

### VS Code

| Extension | Mô tả |
|-----------|-------|
| **Markdown All in One** | Preview, TOC, formatting shortcuts |
| **Markdown Preview Mermaid Support** | Xem Mermaid diagrams |
| **markdownlint** | Lint & format |

### Shortcuts trong VS Code

| Phím | Action |
|------|--------|
| `Ctrl+Shift+V` | Mở preview |
| `Ctrl+K V` | Preview bên cạnh |
| `Ctrl+B` | Bold |
| `Ctrl+I` | Italic |

---

## Tham Khảo

- [Markdown Guide](https://www.markdownguide.org/) — Hướng dẫn đầy đủ
- [CommonMark Spec](https://commonmark.org/) — Chuẩn chung
- [GitHub Flavored Markdown](https://docs.github.com/en/get-started/writing-on-github) — GFM
- [Markdown Live Preview](https://markdownlivepreview.com/) — Preview trực tuyến

---

*Tài liệu được tạo ngày 11-07-2026 — Markdown.*
