---
title: Git nâng cao
description: 'Ghi chú về cách Git lưu dữ liệu trong .git, hiệu năng trên Windows và cách chỉ xem thay đổi trong thư mục hiện tại.'
tags: [git, windows, performance, troubleshooting]
category: git
updated: 2026-10-03
order: 3
---

# Git nâng cao trên Windows

> Ghi chú nhanh về `.git`, hiệu năng và cách giới hạn phạm vi `git status`.

## `git status` trong thư mục hiện tại

Khi repository có nhiều thư mục, có thể chỉ xem thay đổi bên trong thư mục đang đứng:

```bash
git status -- .
```

Ví dụ đang ở `repo/docs/git/`, lệnh chỉ báo trạng thái các file thuộc `docs/git/`, không liệt kê thay đổi ở các thư mục khác.

```text
repo/
├── src/                 ← không nằm trong phạm vi
└── docs/
    └── git/             ← phạm vi được kiểm tra
```

- `--` kết thúc phần tùy chọn; các đối số phía sau được hiểu là đường dẫn.
- `.` là pathspec của thư mục hiện tại. Nếu chạy ở thư mục gốc repository, phạm vi là toàn repository.
- Dùng `git status --short -- .` nếu muốn đầu ra ngắn gọn.
- Lệnh này chỉ giới hạn kết quả theo đường dẫn, không chuyển sang một repository khác.

## Bên trong `.git`

`.git` là cơ sở dữ liệu và trạng thái làm việc của repository. Thư mục này không phải bản sao đơn giản của các file source.

| Thành phần | Vai trò |
|---|---|
| `HEAD` | Cho biết branch hoặc commit hiện tại |
| `index` | Staging area; lưu trạng thái chuẩn bị cho commit tiếp theo |
| `objects/` | Lưu nội dung blob, tree, commit và tag; object có thể được gom vào packfile |
| `refs/` | Các con trỏ như branch và tag |
| `config` | Cấu hình riêng của repository |
| `logs/` | Reflog, ghi lại lịch sử di chuyển của các con trỏ Git |
| `hooks/` | Các script tùy chọn chạy tại một số thời điểm trong workflow |

Luồng cơ bản:

```text
File trong working tree
        │ git add
        ▼
Index (staging)
        │ git commit
        ▼
Object database ── refs/branch ── HEAD
```

### Lưu ý trên Windows

- Thông thường `.git` là thư mục ở gốc repository.
- Với Git worktree hoặc submodule, `.git` có thể là **file trỏ đến Git directory** ở vị trí khác.
- Không tự xóa hoặc sửa file bên trong `.git`; có thể làm mất commit, staging hoặc metadata của repository.
- Không đưa `.git` vào `.gitignore` để xử lý hiệu năng; nó là metadata cần thiết của repository.

## Hiệu năng Git trên Windows

`git status` cần xác định file nào đã thay đổi, file nào chưa được theo dõi. Nó thường chậm khi phải dò một cây thư mục lớn, nhất là nhiều file chưa được ignore.

| Nguyên nhân hay gặp | Hướng xử lý |
|---|---|
| Thư mục sinh ra có rất nhiều file (`node_modules`, output build, cache) | Ignore đúng các file không cần commit bằng `.gitignore` |
| Repository nằm trên ổ đĩa chậm, thư mục đồng bộ hoặc network drive | Thử repository trên ổ local nhanh để so sánh |
| Antivirus/Defender kiểm tra nhiều file trong repository | Kiểm tra chính sách bảo mật và thời gian quét; không tắt bảo vệ tùy tiện |
| Repository hoặc working tree rất lớn | Dùng pathspec như `git status -- .` khi chỉ cần kiểm tra một vùng |

### Kiểm tra trước khi đổi cấu hình

```powershell
# Đo thời gian chạy status
Measure-Command { git status --short }

# Xem số lượng object và dung lượng object database
git count-objects -vH

# Xem cấu hình liên quan cùng nguồn cấu hình
git config --show-origin --get core.fscache
git config --show-origin --get core.untrackedCache
git config --show-origin --get core.fsmonitor
```

Các lệnh `git config --get` trả exit code khác 0 nếu khóa chưa được cấu hình; điều đó không có nghĩa repository bị hỏng.

### Tối ưu có kiểm soát

1. Đưa output, cache và dependency không cần version control vào `.gitignore`.
2. Đo lại `git status` sau khi ignore các đường dẫn phù hợp.
3. Nếu cây thư mục chưa được theo dõi vẫn lớn, cân nhắc untracked cache hoặc filesystem monitor. Hỗ trợ và giá trị mặc định phụ thuộc phiên bản Git.
4. Chỉ thay đổi một thiết lập mỗi lần; so sánh tốc độ và xác nhận `git status` vẫn nhận đúng thay đổi.

Không dùng `git clean` chỉ để làm Git nhanh hơn: lệnh này có thể xóa file chưa được theo dõi.

## Checklist khi Git chậm

- [ ] Có nhiều file chưa được theo dõi hoặc thư mục build/dependency chưa ignore?
- [ ] Repository nằm trên ổ chậm, thư mục sync hoặc network drive?
- [ ] Chậm riêng `git status`, hay cả `log`, `diff`, `commit`?
- [ ] Đã đo trước/sau mỗi thay đổi cấu hình?
- [ ] Có thể thu hẹp phạm vi bằng `git status -- .`?

## Tham khảo

- [Git — git-status](https://git-scm.com/docs/git-status)
- [Git — Repository Layout](https://git-scm.com/docs/gitrepository-layout)
- [Git for Windows](https://gitforwindows.org/)
