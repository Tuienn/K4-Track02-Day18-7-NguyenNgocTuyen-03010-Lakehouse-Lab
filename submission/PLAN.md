# Kế hoạch thực hiện Lakehouse Lab cá nhân

Nguyễn Ngọc Tuyền — 2A202603010. Mỗi checkpoint 0–9 tương ứng một commit Git.

Tài liệu đã đọc: README và toàn bộ 6 Markdown trong docs/, gồm hai bản bonus.
Phần bắt buộc là phạm vi thực hiện; bonus không ảnh hưởng điểm phần bắt buộc.

1. CP0: kiểm tra venv, ghi phiên bản, smoke 9 bước, thông tin cá nhân và kế hoạch.
2. CP1: Delta log, lỗi age sai kiểu thật, schema evolution tier; bỏ PASS hardcoded.
3. CP2: tái hiện ≥100 file; đo trước/sau và kiểm tra speedup ≥3× hoặc pruning ≥10×.
4. CP3: MERGE 100K, kiểm tra update/insert; time travel và history ≥5 gồm RESTORE.
5. CP4: Bronze/Silver/Gold; dedup, đủ ≥7 ngày ×3 model và kiểm tra chất lượng Gold.
6. CP5: catalog, day(ts), pruning ≥5×, metadata và field-ID/partition evolution.
7. CP6: 5 maintenance job; orphan/vacuum/expiry và kiểm tra dữ liệu còn nguyên.
8. CP7: multimodal, quantization và recall; tái hiện stale-index lifecycle bug và CDF.
9. CP8: trajectory medallion, version pin, MCP mô phỏng và provenance có giới hạn.
10. CP9: make smoke/test/run-all, kiểm tra 8 notebook có output/ảnh, reflection ≤200 từ.

Mỗi CP1–8 lưu notebook thực thi thật, bằng chứng output và ảnh chụp trang output.
Không giảm ngưỡng, không bỏ assertion, không tạo số liệu. Chỉnh code nếu cần để
kiểm chứng đúng rubric; giải thích thay đổi tại từng checkpoint.

CP0 và CP9 có phần GitHub chưa hoàn tất: remote hiện sai mẫu và gh token không
hợp lệ. Không thay remote sang URL chưa tồn tại, không tuyên bố đã push/nộp.
