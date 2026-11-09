---
description: Test khi ĐÃ CÓ testcase (bộ kiểm định/regression) — nạp file Excel TC, chạy, ghi kết quả, bug, báo cáo HTML
argument-hint: <đường dẫn file .xlsx testcase> [phạm vi: module/ID/ưu tiên]
---
Nạp skill `qc-testcase`. Đầu vào: $ARGUMENTS

## B0. Xác định module (làm trước, tự phân tích)
Theo `modules/README.md` mục "Xác định module": so khớp nội dung đầu vào với `modules/*/CLAUDE.md` (mục Phạm vi + Từ khoá nhận diện).
- Khớp 1 module → báo 1 dòng "Module: <tên> (lý do)", **hỏi QC xác nhận** (trắc nghiệm: đúng / chọn module khác / task chạm nhiều module).
- Khớp nhiều module → hỏi QC chọn module chính + module ảnh hưởng chéo.
- **Không khớp module nào → module mới**: hỏi QC (trắc nghiệm) có tạo module mới không, và tên module. Đồng ý → tạo `modules/<module>/` + skill `qc-<module>` từ `modules/_template/` (xem `modules/README.md` "Thêm module mới"), điền phần suy ra được từ task (gắn `[cần xác nhận]`), **ĐIỂM DỪNG** cho QC duyệt rule/checklist rồi mới đi tiếp.
- Sau khi chốt: nạp skill `qc-<module>`, đọc `modules/<module>/CLAUDE.md`; output ghi vào `modules/<module>/output/<task>/` (thay cho `output/<task>/` ở các bước dưới).

## B1. Nạp TC và checklist
- `python -I scripts/xlsx_to_tc.py "<file.xlsx>" output/<task>/testcases.json` (thêm `--sheet <tên>` nếu nhiều sheet).
- Báo QC: nhận bao nhiêu TC, cột nào nhận được / không nhận được. Cột sai thì hỏi QC (trắc nghiệm, có Other) cột nào là cột nào.
- Checklist: không bắt buộc để chạy TC có sẵn, nhưng hỏi QC (trắc nghiệm) có muốn AI **đối chiếu độ phủ** TC với checklist không: *QC gửi checklist* / *AI sinh checklist từ TC + tài liệu* / *Không cần*. Nếu có → báo mục checklist chưa có TC nào bao phủ.
- Hỏi phạm vi chạy bằng câu trắc nghiệm (tất cả / theo module / theo ưu tiên High / danh sách ID). **ĐIỂM DỪNG 1.**

## B2. Chạy test theo phạm vi
- Mặc định **không sửa nội dung TC gốc**. Nếu thấy TC lỗi thời/sai → ghi vào danh sách "TC cần cập nhật" cho QC quyết.
- Chạy theo từng nhóm 10–15 TC: có Playwright MCP và QC cho phép → AI chạy; không thì QC báo kết quả ngắn `TC_001 pass; TC_002 fail: ...`. Ghi vào `results.json` sau mỗi nhóm.

## B3. Bug & báo cáo
Giống `/test-task` B5, B6: soạn bug cho TC Fail → QC xác nhận → (Jira MCP) log → `make_report.py`.
Thêm vào báo cáo phần "TC cần cập nhật" (nếu có) trong `conclusion`.
