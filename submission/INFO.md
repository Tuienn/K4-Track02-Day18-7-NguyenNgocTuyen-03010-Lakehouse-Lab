# Thông tin bài làm cá nhân

- Họ tên: Nguyễn Ngọc Tuyền
- MSSV: 2A202603010
- Mã bài: K4-Track02-Day18
- Hình thức: cá nhân, phần bắt buộc checkpoint 0–9; chưa làm bonus tùy chọn.
- Đường chạy: lightweight cho cả 8 notebook.
- Python: 3.14.7
- Hệ điều hành: Linux-7.2.8-200.fc44.x86_64-x86_64-with-glibc2.43
- Ngày thực thi: 05/10/2026 (Asia/Ho_Chi_Minh).
- Dữ liệu: dữ liệu giả do scripts của đề bài sinh; không dùng API key.
- Phiên bản dependencies: `requirements-lock.txt` ghi các gói đã cài.
- Khai báo hỗ trợ AI: [AI_USAGE.md](AI_USAGE.md).

## Repo bài nộp

Tên yêu cầu: `K4-Track02-Day18-NguyenNgocTuyen-2A202603010-Lakehouse-Lab`.
Remote đang có: `git@github.com:Tuienn/K4-Track02-Day18-7-NguyenNgocTuyen-03010-Lakehouse-Lab.git`.
Tên remote chưa đúng mẫu/MSSV. Cần đổi tên fork trên GitHub, cập nhật origin,
push và mở PR khi nộp. Các bước này chưa được thực hiện trong lần làm local.
GitHub CLI hiện báo token không hợp lệ. Không coi bài local là đã nộp.

## Tái lập

Từ gốc repo, dùng Python 3.14 như bản chạy này hoặc khoảng hỗ trợ trong README:

```bash
python3 -m venv .venv
uv pip install --python .venv/bin/python -r submission/requirements-lock.txt
make smoke
make data
make data-ai
make test
make run-all
.venv/bin/python scripts/execute_submission.py
```

Notebook bản nộp chạy được khi kernel dùng venv và thư mục làm việc là gốc repo;
cell bootstrap tìm `scripts/` và `notebooks/` từ gốc repo hoặc vị trí bài nộp.
Dữ liệu `_lakehouse/` và `.venv/` không được commit.
