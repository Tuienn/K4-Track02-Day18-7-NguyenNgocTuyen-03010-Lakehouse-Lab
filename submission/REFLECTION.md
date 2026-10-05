# Reflection

Nguyễn Ngọc Tuyền — 2A202603010.

Anti-pattern tôi chọn là xem external vector index như nguồn dữ liệu chính,
trong khi bỏ quên vòng đời dữ liệu gốc. Với RAG học tập,
tài liệu có thể được sửa, thu hồi hoặc hết quyền sử dụng; index chỉ nhận upsert
sẽ tiếp tục trả embedding của tài liệu đã xóa.

NB7 tái hiện rõ rủi ro: bảng nguồn còn 0 hit của subject bị xóa nhưng index cũ
vẫn giữ 8 hit. CDF phát ra 8 delete event, cho phép truyền doc_id cần loại khỏi
index. Giữ vector cùng hàng dữ liệu giảm nguy cơ lệch lifecycle; nếu cần index
riêng cho serving, tôi sẽ coi nó là bản dẫn xuất có thể dựng lại, xử lý delete
idempotent, ghi watermark/version và giám sát độ trễ đồng bộ.

Time travel vẫn có thể giữ bản cũ sau delete. Cần phối hợp retention,
vacuum và kiểm kê các bản sao, không chỉ kiểm tra version hiện tại.

Codex hỗ trợ thực thi, kiểm tra và soạn bản nháp này; khai báo tại
[AI_USAGE.md](AI_USAGE.md). Cần tự xác nhận trước khi nộp.
