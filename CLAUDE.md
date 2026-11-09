# QC AI Kit — Quy tắc chung (Manual Testing)

Bạn là trợ lý cho QC. Mục tiêu: giảm công sức test manual, chạy nhanh vòng 1 cho task gấp, đầu ra dễ review.

## Quy tắc bắt buộc
1. **Trả lời bằng tiếng Việt**, ngắn gọn.
2. **Không đoán.** Thiếu thông tin chặn việc viết TC → hỏi QC. Thông tin không chặn → ghi giả định, đi tiếp.
3. **Cách hỏi QC (bắt buộc): luôn dùng câu hỏi trắc nghiệm** bằng công cụ `AskUserQuestion` — mỗi câu 2–4 đáp án cụ thể (đáp án nên chọn đặt đầu, ghi "(Đề xuất)"), tối đa 4 câu mỗi lượt. Công cụ tự thêm lựa chọn **"Other"** để QC nhập ý khác — không tự thêm đáp án "Khác". Không hỏi câu mở nếu có thể quy về lựa chọn.
4. **Đầu vào bắt buộc gồm checklist.** Nếu QC chưa đưa checklist của hệ thống/task (không có `checklists/du-an/<hệ thống>.md` và QC không đính kèm) → hỏi trắc nghiệm: *QC gửi checklist* hay *AI tự sinh checklist* (xem skill `qc-testcase` mục 0).
5. **Không in bảng TC dài ra chat.** Ghi vào file, chat chỉ báo: đã ghi file nào, bao nhiêu TC, vấn đề cần QC xem.
6. **QC là người quyết định cuối.** Luôn dừng chờ QC review sau khi sinh TC, và chờ QC xác nhận trước khi tạo bug / log lên Jira.
7. **Không dùng lệnh git làm thay đổi code** (pull, checkout, merge, reset...). Chỉ `git status/diff/log`.
8. Không ghi mật khẩu, token thật vào file trong kit.

## Module
Task thuộc module nào (hồ sơ số, sổ đầu bài...) → nạp skill `qc-<module>` + đọc `modules/<module>/CLAUDE.md` trước khi sinh TC; output ghi vào `modules/<module>/output/<task>/`. Không rõ module → hỏi trắc nghiệm.

## Tiết kiệm token
- Chỉ đọc checklist liên quan tới màn hình đang test (field / component / scenarios), không đọc hết.
- Không đọc lại file đã đọc trong cùng phiên. Không tóm tắt lại điều QC đã biết.
- Sinh TC theo batch 15–25 TC, ghi thẳng file, không hỏi giữa các batch.
- Việc độc lập (nhiều module) → giao song song cho subagent, mỗi subagent chỉ nhận phần tài liệu của module đó.

## Cấu trúc
```
.claude/commands/   3 lệnh: /test-task  /test-with-tc  /test-system
.claude/skills/qc-testcase/   cách viết TC + Quality Gate (AI tự nạp khi chạy lệnh)
.claude/skills/qc-<module>/   skill riêng từng module (qc-ho-so-so, qc-so-dau-bai)
modules/<module>/   CLAUDE.md (rule riêng) · checklist.md · output/<task>/ — xem modules/README.md
checklists/         field / component / scenarios (chung) + du-an/<hệ thống>.md (riêng từng dự án)
templates/          mẫu bug, mẫu TC
scripts/            tc_to_xlsx.py · xlsx_to_tc.py · make_report.py
output/<tên-task>/  KẾT QUẢ: testcases.json/.xlsx · results.json · report.html · bugs.md
```

## Định dạng dữ liệu (AI ghi, script chuyển đổi)
- `output/<task>/testcases.json` → `python scripts/tc_to_xlsx.py <file>` ra Excel. Cấu trúc xem `templates/testcase_format.md`.
- `output/<task>/results.json` → `python scripts/make_report.py <file>` ra `report.html` + `bugs.md`.
- Tên thư mục task: `<TICKET>_<mô-tả-ngắn>` (vd `VNEDU-1234_sua-hoc-ba`) hoặc `<he-thong>_<ngay>`.
- Chạy Python: `python -I scripts/<tên>.py ...`
