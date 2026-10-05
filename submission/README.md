# Bài nộp Lakehouse Lab cá nhân

Nguyễn Ngọc Tuyền — MSSV 2A202603010 — K4-Track02-Day18.

Phần bắt buộc đã hoàn thành trên máy, mỗi checkpoint 0–9 có một commit.
Bonus tùy chọn chưa thực hiện. Bài chưa được push hoặc gửi lên kênh lớp.

## Hồ sơ

- [Thông tin và tái lập](INFO.md)
- [Kế hoạch checkpoint](PLAN.md)
- [Reflection, dưới 200 từ](REFLECTION.md)
- [Khai báo sử dụng AI](AI_USAGE.md)
- [Dependency lock của lần chạy](requirements-lock.txt)

## Notebook và bằng chứng

- [01_delta_basics](notebooks/01_delta_basics.ipynb) — [ảnh](screenshots/01_delta_basics.png), [output text](evidence/01_delta_basics.txt), [trang output](evidence/01_delta_basics.html).
- [02_optimize_zorder](notebooks/02_optimize_zorder.ipynb) — [ảnh](screenshots/02_optimize_zorder.png), [output text](evidence/02_optimize_zorder.txt), [trang output](evidence/02_optimize_zorder.html).
- [03_time_travel](notebooks/03_time_travel.ipynb) — [ảnh](screenshots/03_time_travel.png), [output text](evidence/03_time_travel.txt), [trang output](evidence/03_time_travel.html).
- [04_medallion](notebooks/04_medallion.ipynb) — [ảnh](screenshots/04_medallion.png), [output text](evidence/04_medallion.txt), [trang output](evidence/04_medallion.html).
- [05_iceberg_catalog](notebooks/05_iceberg_catalog.ipynb) — [ảnh](screenshots/05_iceberg_catalog.png), [output text](evidence/05_iceberg_catalog.txt), [trang output](evidence/05_iceberg_catalog.html).
- [06_maintenance](notebooks/06_maintenance.ipynb) — [ảnh](screenshots/06_maintenance.png), [output text](evidence/06_maintenance.txt), [trang output](evidence/06_maintenance.html).
- [07_vectors_multimodal](notebooks/07_vectors_multimodal.ipynb) — [ảnh](screenshots/07_vectors_multimodal.png), [output text](evidence/07_vectors_multimodal.txt), [trang output](evidence/07_vectors_multimodal.html).
- [08_agents_provenance](notebooks/08_agents_provenance.ipynb) — [ảnh](screenshots/08_agents_provenance.png), [output text](evidence/08_agents_provenance.txt), [trang output](evidence/08_agents_provenance.html).

Ảnh là screenshot Chromium của trang HTML hiển thị nguyên output từ notebook
đã thực thi, không phải ảnh Jupyter UI. Nội dung text được đối chiếu tự động
với output trong ipynb. Notebook có cả giải thích và phần kiểm tra rubric.

## Kiểm tra cuối

- [Smoke checkpoint 0](evidence/checkpoint00_smoke.txt)
- [Pytest môi trường ban đầu](evidence/checkpoint09_pytest.txt)
- [Run-all với dữ liệu mới](evidence/checkpoint09_run_all.txt)
- [Cài lock vào venv mới, offline từ cache](evidence/checkpoint09_clean_setup.txt)
- [Smoke môi trường sạch](evidence/checkpoint09_clean_smoke.txt)
- [Pytest môi trường sạch](evidence/checkpoint09_clean_pytest.txt)
- [Run-all venv mới + dữ liệu mới](evidence/checkpoint09_clean_run_all.txt)
- [Kiểm tra notebook/source/output/ảnh/reflection](evidence/checkpoint09_artifacts.txt)

`make` nhận `VENV=/tmp/lakehouse-day18-clean-venv` trong lần kiểm tra sạch;
`LAKEHOUSE_ROOT` là thư mục mới tạo trong /tmp. Venv này được cài từ lock,
không dùng site-packages của venv cũ. Không cần mạng sau khi cài xong.

Để tạo lại bản nộp có output, chạy từ gốc repo:

```bash
.venv/bin/python scripts/execute_submission.py
```

Sau khi thực thi lại, tạo lại ảnh trước bước verify cuối. Script ảnh dùng
Node.js + Playwright và Chromium cài sẵn; đặt NODE_PATH tới package Playwright
và CHROMIUM_PATH tới executable nếu khác mặc định Linux của máy này:

```bash
node scripts/screenshot_submission.cjs
.venv/bin/python scripts/verify_submission.py
```

Jupyter cần socket loopback để kernel hoạt động; môi trường sandbox có thể
cần quyền chạy kernel/trình duyệt. Scripts không gọi model/API hay gửi dữ liệu.

## Cách đọc kết quả và thay đổi mã

Các assertion gốc và ngưỡng rubric được giữ nguyên hoặc kiểm tra chặt hơn.
NB1 thay PASS hardcoded bằng lỗi append thật và kiểm tra version/count không đổi.
NB2 xác nhận ≥100 file ban đầu và range thực sự chứa target.
NB3 đối chiếu metrics và kết quả 50K update + 50K insert.
NB4 kiểm tra toàn bộ coverage và chất lượng Gold, in đủ các dòng/cột.
NB5 kiểm tra catalog, day(ts), field-ID cùng tập data path trước/sau rename;
metadata:data được ghi đúng mẫu số là data bytes.
NB6 loại checkpoint Parquet khỏi số file dữ liệu, resolve candidate VACUUM
về đường dẫn bảng, phân biệt tombstone candidate và file còn tồn tại, chốt
bytes thu hồi ngay sau vacuum và kiểm tra dữ liệu Delta còn nguyên.
NB7 bổ sung giải thích phạm vi đo footer/quantization/index lifecycle.
NB8 đối chiếu đúng tên policy/bucket và training filter với corpus đã persist.

Gold có 8 ngày ×3 model trong bản chạy này dù generator trải 7 ngày UTC:
DuckDB dùng timezone `Asia/Ho_Chi_Minh`; `CAST(ts AS DATE)` chuyển timestamp
UTC sang ngày địa phương và có phần dữ liệu rơi vào ngày thứ 8. Kết quả vẫn
đạt yêu cầu ≥7 ngày. Muốn ngày UTC trong production cần chốt timezone của SQL
rõ ràng; không thay số output để ép về 7 ngày.

NB7 đo amplification bằng row-group uncompressed bytes từ footer, không đo
actual disk/network I/O; NB8 là mô phỏng và replay theo count, không chứng minh
bảo mật, protocol đầy đủ, equality nội dung hoặc quyền dùng dữ liệu thật.
Các con số bill/latency ngoại suy từ đề chỉ là ví dụ có giả định, không báo giá
hoặc benchmark production.

## Việc còn lại khi nộp

1. Đọc notebook/reflection, tự chạy và xác nhận hiểu kết quả theo RULES.md.
2. Đăng nhập GitHub; đổi tên fork thành
   `K4-Track02-Day18-NguyenNgocTuyen-2A202603010-Lakehouse-Lab` và cập nhật origin.
3. Push các commit, mở PR với tiêu đề
   `[K4-Track02-Day18] NguyenNgocTuyen - 2A202603010 - Lakehouse Lab`.
4. Gửi repo + PR + commit SHA cuối qua kênh lớp; deadline theo thông báo coach.

Không coi các bước GitHub là đã xong: token CLI đang không hợp lệ và remote
hiện sai mẫu. Không có TEAM.md, venv hoặc dữ liệu lakehouse trong bài commit.
