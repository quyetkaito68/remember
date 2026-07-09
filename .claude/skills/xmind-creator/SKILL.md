---
name: xmind-creator
description: >
  Tạo file XMind (.xmind) sơ đồ tư duy từ BẤT KỲ đầu vào nào: freetext mô tả chủ đề,
  nội dung PBI trên TFS, file markdown, hay ý tưởng tự do. Không theo cấu trúc cố định —
  tự phân tích và tổ chức thành cây tư duy từ tổng quan đến chi tiết, mỗi node cha tối đa 5 con.
  Output là file .xmind với theme Professional xanh, tiếng Việt có dấu.
  TRIGGER khi user nói: "tạo mind map", "vẽ sơ đồ tư duy", "xmind cho...", "tóm tắt thành mind map",
  "mindmap từ...", "xuất xmind", hoặc muốn trực quan hóa bất kỳ chủ đề/vấn đề/tài liệu nào.
  LUÔN dùng skill này thay vì tự viết code khi user cần tạo file .xmind.
---

# xmind-creator — Tạo sơ đồ tư duy XMind từ mọi đầu vào

Skill này nhận đầu vào dạng tự do (freetext, PBI TFS, markdown, ý tưởng) và tạo file `.xmind`
với cấu trúc cây tư duy trực quan — từ tổng quan đến chi tiết, không theo template cố định.

---

## Nguyên tắc sơ đồ tư duy tốt

Trước khi làm, nắm rõ 3 nguyên tắc này:

1. **Từ trung tâm ra ngoài**: Node gốc = chủ đề lớn nhất → các nhánh = khía cạnh chính → lá = chi tiết cụ thể.
2. **Tối đa 5 con mỗi node**: Nếu có nhiều hơn, nhóm gộp thành một node cha mới thay vì liệt kê thẳng.
3. **Ngắn gọn**: Mỗi node ≤ 60 ký tự. Nếu dài hơn → tách thành 2 node hoặc rút gọn ý chính.

---

## Bước 1 — Đọc và hiểu đầu vào

Đầu vào có thể là:

| Loại | Cách xử lý |
|---|---|
| **Freetext** | Phân tích ý chính, xác định chủ đề trung tâm và các khía cạnh |
| **TFS PBI ID** | Dùng MCP `tfs_get_workitem` lấy nội dung, trích xuất mục đích + giải pháp + ảnh hưởng |
| **File markdown** | Đọc file, dùng heading làm nhánh chính, bullet làm nhánh con |
| **Ý tưởng ngắn** | Hỏi thêm nếu cần, hoặc tự suy luận và mở rộng hợp lý |

Nếu đầu vào mơ hồ hoặc quá ngắn → hỏi: "Bạn muốn mind map này trình bày điều gì? Đối tượng xem là ai?"

---

## Bước 2 — Xây dựng cây tư duy

### Quy tắc phân tích

- **Node gốc**: Tiêu đề chủ đề ngắn gọn, súc tích (≤ 40 ký tự)
- **Nhánh cấp 1** (3–5 nhánh): Các khía cạnh/góc nhìn lớn của chủ đề
- **Nhánh cấp 2** (2–5 mục/nhánh): Chi tiết cụ thể của từng khía cạnh
- **Nhánh cấp 3+** (tùy): Chỉ thêm khi thực sự cần đi sâu; tránh cây quá nhiều tầng

### Cách nhóm khi có nhiều ý

Thay vì:
```
Giải pháp
├── Thêm API A
├── Thêm API B
├── Thêm API C
├── Thêm API D
├── Thêm API E
├── Thêm API F   ← vượt quá 5
```

Nhóm lại:
```
Giải pháp
├── Backend API (6 endpoints)
│   ├── API A, B, C
│   └── API D, E, F
```

### Các pattern phổ biến theo loại đầu vào

**Cho PBI / Feature:**
```
Tên tính năng
├── Mục đích
├── Đối tượng & bối cảnh
├── Giải pháp
│   ├── Tổng thể
│   └── Chi tiết (BE / FE / DB)
├── Ảnh hưởng
└── Rủi ro & lưu ý
```

**Cho vấn đề / phân tích:**
```
Vấn đề
├── Hiện trạng
├── Nguyên nhân
├── Giải pháp đề xuất
├── Ưu / Nhược điểm
└── Bước tiếp theo
```

**Cho tài liệu / kiến thức:**
```
Chủ đề
├── Khái niệm chính
├── Thành phần / Cấu trúc
├── Cách hoạt động
├── Ứng dụng thực tế
└── Câu hỏi thường gặp
```

---

## Bước 3 — Chuẩn bị JSON và gọi script

### Schema JSON đầu vào

```json
{
  "title": "Tiêu đề node gốc",
  "output_path": "path/to/output.xmind",
  "sheet_title": "Tên sheet (tuỳ chọn)",
  "children": [
    {
      "title": "Nhánh cấp 1",
      "children": [
        {
          "title": "Mục cấp 2",
          "children": [
            { "title": "Chi tiết cấp 3" }
          ]
        },
        { "title": "Mục cấp 2 khác" }
      ]
    },
    { "title": "Nhánh cấp 1 không có con" }
  ]
}
```

**Output path mặc định**: nếu liên quan PBI → `.specify/specs/PBI/{ID}/{ID}-mindmap.xmind`
Nếu là chủ đề tự do → `.specify/mindmaps/{slug-chu-de}.xmind`

### Gọi script (Windows/PowerShell)

```powershell
$tmp = "$env:TEMP\xmind_creator_{slug}.json"
[System.IO.File]::WriteAllText($tmp, $jsonString, [System.Text.UTF8Encoding]::new($false))
cmd /c "type `"$tmp`" | python .claude/skills/xmind-creator/scripts/generate-xmind.py"
Remove-Item $tmp -ErrorAction SilentlyContinue
```

> Script tự tạo thư mục output nếu chưa có. Chạy từ thư mục gốc repo.

---

## Bước 4 — Báo cáo kết quả

Sau khi script chạy xong, thông báo:
```
✅ Đã tạo XMind: {output_path}
   {N} topics | Theme: Professional (xanh #558ED5) | Logic Chart Right
   Nhánh gốc: [liệt kê tên các nhánh cấp 1]
```

---

## Quy tắc nội dung bắt buộc

- **Tiếng Việt có dấu**: Mọi text PHẢI dùng tiếng Việt đầy đủ dấu. Tên kỹ thuật (API endpoint, class name, file path) giữ nguyên.
- **Không vượt 5 con**: Script tự động cắt nếu vượt, nhưng AI phải nhóm gộp trước khi gửi JSON.
- **Cân bằng cây**: Không để 1 nhánh có 5 cấp trong khi nhánh khác chỉ có 1 cấp. Điều chỉnh để cây trông hài hòa khi mở trong XMind.
- **Không trùng lặp**: Một ý chỉ xuất hiện 1 lần trên cây. Nếu liên quan nhiều nhánh → để ở nhánh phù hợp nhất.

---

## Xử lý edge cases

| Tình huống | Hành xử |
|---|---|
| Đầu vào quá ngắn (< 10 từ) | Hỏi thêm context, hoặc tạo cây cơ bản rồi gợi ý bổ sung |
| TFS ID không tồn tại | Báo lỗi, hỏi lại ID |
| File markdown không có heading | Dùng paragraph đầu làm root, các đoạn tiếp theo làm nhánh |
| Nội dung quá dài, nhiều ý | Ưu tiên ý chính, gộp chi tiết vào nhánh "Chi tiết / Xem thêm" |
| User muốn cây cân bằng 2 chiều | Đặt `"structure": "org.xmind.ui.map.unbalanced"` trong JSON |



