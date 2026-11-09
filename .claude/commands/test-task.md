---
description: Test 1 task upcode — đọc Jira + checklist → sinh TC (Excel) → QC review → chạy/ghi kết quả → bug → báo cáo HTML
argument-hint: <Jira key hoặc dán mô tả task> [tên hệ thống: vnedu|hss|ioc|tsdc]
---
Nạp skill `qc-testcase`. Làm theo thứ tự, **dừng ở mỗi ĐIỂM DỪNG**. Đầu vào: $ARGUMENTS

## B0. Xác định module (làm trước, tự phân tích)
Theo `modules/README.md` mục "Xác định module": so khớp nội dung đầu vào với `modules/*/CLAUDE.md` (mục Phạm vi + Từ khoá nhận diện).
- Khớp 1 module → báo 1 dòng "Module: <tên> (lý do)", **hỏi QC xác nhận** (trắc nghiệm: đúng / chọn module khác / task chạm nhiều module).
- Khớp nhiều module → hỏi QC chọn module chính + module ảnh hưởng chéo.
- **Không khớp module nào → module mới**: hỏi QC (trắc nghiệm) có tạo module mới không, và tên module. Đồng ý → tạo `modules/<module>/` + skill `qc-<module>` từ `modules/_template/` (xem `modules/README.md` "Thêm module mới"), điền phần suy ra được từ task (gắn `[cần xác nhận]`), **ĐIỂM DỪNG** cho QC duyệt rule/checklist rồi mới đi tiếp.
- Sau khi chốt: nạp skill `qc-<module>`, đọc `modules/<module>/CLAUDE.md`; output ghi vào `modules/<module>/output/<task>/` (thay cho `output/<task>/` ở các bước dưới).

## B1. Lấy yêu cầu và checklist
- Có Jira key và Jira MCP đã kết nối → đọc ticket (mô tả, acceptance criteria, comment, file đính kèm quan trọng). Không có MCP → xin QC dán mô tả.
- Xác định hệ thống (không rõ thì hỏi trắc nghiệm).
- **Checklist:** tìm theo skill `qc-testcase` mục 0. Chưa có → hỏi QC: gửi checklist hay AI sinh. **ĐIỂM DỪNG 0** cho tới khi có checklist (hoặc QC chọn bỏ qua).
- Tạo thư mục `output/<TICKET>_<mô-tả-ngắn>/`.

## B2. Phân tích (ngắn)
Rút danh sách REQ + xếp rủi ro. Nếu có điểm mơ hồ **chặn** việc viết TC → hỏi QC bằng câu trắc nghiệm (`AskUserQuestion`, có Other) rồi **ĐIỂM DỪNG 1**. Không chặn thì ghi giả định và đi tiếp.

## B3. Sinh TC
Theo skill: ghi `testcases.json` → chạy `python -I scripts/tc_to_xlsx.py output/<task>/testcases.json` → chạy Quality Gate, bổ sung nếu thiếu.
Chat chỉ báo: đường dẫn `.xlsx`, số TC theo Positive/Negative/Boundary, REQ nào còn yếu, giả định đã dùng.
**ĐIỂM DỪNG 2 — QC review/bổ sung TC.** QC sửa trong Excel (hoặc nhắn AI sửa). Nếu QC sửa Excel: chạy `scripts/xlsx_to_tc.py` để đồng bộ lại json.

## B4. Chạy test & ghi kết quả
- Có Playwright MCP và QC cho phép → AI chạy các bước UI, chụp ảnh bằng chứng vào `output/<task>/screenshots/`.
- Không thì QC tự test; QC báo kết quả dạng ngắn: `TC_001 pass; TC_002 fail: <thực tế>; TC_003 blocked: <lý do>`. AI ghi vào `results.json`.

## B5. Bug
Với mỗi TC Fail: soạn bug theo `templates/bug_template.md`, ghi vào `results.json`. **ĐIỂM DỪNG 3 — QC xác nhận từng bug** (sửa/bỏ/gộp).
Sau khi QC đồng ý và có Jira MCP → tạo issue Bug (gắn link ticket gốc), ghi key vào trường `jira`. Không có MCP → để QC dán từ `bugs.md`.

## B6. Báo cáo
`python -I scripts/make_report.py output/<task>/results.json` → báo QC đường dẫn `report.html`, số Pass/Fail/Blocked, và 1 câu kết luận.
