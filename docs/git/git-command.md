---
title: Git Commands — Các lệnh Git hay dùng nhất
description: 'Danh sách các lệnh Git thông dụng nhất: branch, commit, reset, restore, conflict, credential — kèm giải thích ngắn gọn.'
tags: [git, command, reference]
category: git
updated: 2026-07-05
order: 2
---

# Git Commands — Các lệnh Git hay dùng nhất

> Tổng hợp các lệnh Git hữu ích nhất trong công việc hàng ngày — quản lý branch, commit, undo, conflict và credential. Không phải danh sách đầy đủ; xem [tài liệu chính thức](https://git-scm.com/docs) để biết toàn bộ.

---

## Branch — Quản lý nhánh

```bash
# Danh sách branch local (dấu * là branch hiện tại)
git branch

# Danh sách branch remote
git branch -r

# Tạo branch mới
git branch <tên-branch>

# Tạo và chuyển sang branch mới
git checkout -b <tên-branch>

# Chuyển sang branch khác
git checkout <tên-branch>

# Xoá branch local (đã merge)
git branch -d <tên-branch>

# Xoá branch local (chưa merge, force)
git branch -D <tên-branch>

```

---

## Commit — Quản lý commit

```bash
# Stage file và commit
git add <file>
git commit -m "message"

# Stage tất cả và commit (lệnh ngắn)
git commit -am "message"

# Sửa commit gần nhất (message hoặc quên stage file)
git commit --amend -m "message mới"

# Xem lịch sử commit (dạng đồ hoạ)
git log --oneline --graph --all

# Xem commit gần nhất
git log -1

# Xem chi tiết thay đổi trong commit
git show <commit-hash>

# Tìm commit theo nội dung message
git log --grep="từ khóa"
```

---

## Reset & Restore — Undo các cấp độ

### Chưa stage (sửa trong working directory)

```bash
# Undo thay đổi file (trở về trạng thái commit gần nhất)
git restore <file>
```

### Đã stage (git add rồi nhưng chưa commit)

```bash
# Unstage file (giữ nguyên thay đổi trong file)
git restore --staged <file>

# Unstage + undo thay đổi file (về commit gần nhất)
git restore --staged --worktree <file>
```

### Đã commit — Reset về commit cũ hơn

<!-- Có 3 chế độ --soft / --mixed (mặc định) / --hard -->

```bash
# --soft: giữ nguyên staging + working directory
git reset --soft HEAD~1

# --mixed: bỏ staging, giữ working directory (mặc định)
git reset HEAD~1
# hoặc
git reset --mixed HEAD~1

# --hard: xoá sạch staging + working directory (nguy hiểm)
git reset --hard HEAD~1
```

> **Phân biệt:**
> | Lệnh | Staging | Working directory | Dùng khi |
> |------|---------|-------------------|----------|
> | `--soft` | giữ | giữ | Muốn commit lại với message khác |
> | `--mixed` | xoá | giữ | Stage sai file, muốn stage lại |
> | `--hard` | xoá | xoá | Muốn bỏ hẳn commit sai (mất code) |

---

## Conflict — Xử lý xung đột

Khi merge/rebase báo conflict, Git chèn marker vào file:

```text
<<<<<<< HEAD
Nội dung branch hiện tại
=======
Nội dung branch đang merge vào
>>>>>>> feature-branch
```

### VS Code — Git Conflict UI

Hỗ trợ sẵn, không cần cài extension. Khi file có conflict, VS Code hiển thị:

- **Accept Current Change** — giữ branch hiện tại
- **Accept Incoming Change** — giữ branch đang merge vào
- **Accept Both Changes** — giữ cả hai
- **Compare Changes** — xem diff bên cạnh

> VS Code cũng có **Source Control** view (Ctrl+Shift+G) cho phép stage/unstage, commit, push, pull, xem diff — xử lý conflict hoàn toàn bằng GUI.

### Visual Studio — Git UI

Visual Studio có **Git Changes** tab (View → Git Changes):

- Xem danh sách file conflict
- Double-click file để mở **Merge Editor** (so sánh 3 chiều)
- Chọn từng thay đổi hoặc edit trực tiếp
- Nhấn **Accept Merge** khi xong

---

## Alias — Cấu hình lệnh tắt

Git alias cho phép gõ lệnh ngắn thay vì gõ đầy đủ. Config trong `~/.gitconfig` hoặc dùng lệnh `git config`.

### Cấu hình alias

```bash
# Cú pháp
git config --global alias.<tên-tắt> "<lệnh-gốc>"

# Ví dụ
git config --global alias.co "checkout"
git config --global alias.br "branch"
git config --global alias.ci "commit"
git config --global alias.st "status"
git config --global alias.unstage "reset HEAD --"
git config --global alias.last "log -1 HEAD"
git config --global alias.lg "log --oneline --graph --all --decorate"
```

Sau khi config, thay vì gõ:

```bash
git checkout -b feature
# gõ tắt:
git co -b feature

git log --oneline --graph --all --decorate
# gõ tắt:
git lg
```

### Alias nâng cao — dùng hàm

```bash
# Tìm commit theo nội dung
git config --global alias.find "!f() { git log --oneline --all --grep \"$@\"; }; f"

# Xoá tất cả branch local trừ main/master
git config --global alias.clean-branches "!git branch | grep -v 'main\\|master' | xargs git branch -D"
```

### Xem danh sách alias đã config

```bash
git config --global --get-regexp alias
```

hoặc mở file config trực tiếp:

```bash
git config --global --edit
```

Đoạn config trong `~/.gitconfig` sẽ có dạng:

```ini
[alias]
	b = branch
	d = status
	unstage = reset HEAD --
	last = log -1 HEAD
	lg = log --oneline --graph --all --decorate
```

> **Mẹo:** Dành 5 phút config alias sẽ tiết kiệm rất nhiều thao tác gõ lệnh hàng ngày.

---

## Tham khảo thêm

- [Git Documentation — toàn bộ lệnh](https://git-scm.com/docs)
- [Git Book — sách hướng dẫn](https://git-scm.com/book/en/v2)
- [Git Command Explorer](https://gitexplorer.com/) — tool chọn lệnh theo tình huống
- [Oh Shit, Git!?!](https://ohshitgit.com/) — fix lỗi git thường gặp
