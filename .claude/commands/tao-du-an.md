---
description: Tạo dự án QC mới có cấu trúc y hệt kit này (copy rule, lệnh, skill, checklist chung, script, template — không copy tài khoản và kết quả test)
argument-hint: <đường dẫn thư mục dự án mới> [tên dự án]
---
Tạo dự án mới từ dự án đang mở. Đầu vào: $ARGUMENTS

**Copy nguyên file, không tự viết lại nội dung** (trừ các chỗ nêu ở B3). Mọi câu hỏi dùng `AskUserQuestion`. Không sửa gì trong dự án gốc. Không chạy lệnh git.

## B1. Thư mục đích
- Chưa có đường dẫn → hỏi (gợi ý thư mục cùng cấp dự án này, QC nhập đường dẫn khác qua Other).
- Đích nằm trong dự án gốc → từ chối, hỏi lại. Đích đã có file → liệt kê ngắn và hỏi: *Chọn thư mục khác* (Đề xuất) / *Chỉ thêm file còn thiếu, không ghi đè* / *Dừng*.

## B2. Hỏi phần riêng muốn mang theo
`multiSelect: true`, câu hỏi: *"Mang theo gì từ dự án này?"*
- *Không mang gì, dự án sạch (Đề xuất)*
- *Module nghiệp vụ* (`modules/<module>/` + `.claude/skills/qc-<module>/`) → hỏi tiếp chọn module nào.
- *Checklist dự án* (`checklists/du-an/*.md` ngoài README)

## B3. Copy
Chỉ copy đúng danh sách này (giữ nguyên đường dẫn):

| Copy | Ghi chú |
|---|---|
| `CLAUDE.md`, `HUONG_DAN.md`, `JIRA_MCP.md`, `.gitignore` | |
| `.claude/commands/` | gồm cả lệnh này |
| `.claude/skills/qc-testcase/` | |
| `checklists/field_checklist.md`, `component_checklist.md`, `scenarios_checklist.md`, `du-an/README.md` | |
| `modules/README.md`, `modules/_template/` | |
| `scripts/` | bỏ `__pycache__` |
| `templates/`, `samples/` | |
| `acc.example.yaml` | |
| `luong-*.png` | |
| Module / checklist đã chọn ở B2 | module bỏ thư mục `output/` |

**Cấm copy:** `acc.yaml`, `.auth/`, `.playwright-cli/`, `.claude/settings.local.json`, `.git/`, mọi thư mục `output/`.

Sau khi copy, chỉ sửa trong dự án mới:
1. Tạo `acc.yaml` trống: phần chú thích đầu file theo `acc.example.yaml`, danh sách `accounts:` chỉ có 1 khối mẫu bị comment `#`. Không có tài khoản nào.
2. `.gitignore` phải có `acc.yaml`, `.auth/`, `.claude/settings.local.json`.
3. `modules/README.md` mục "Module hiện có" và `CLAUDE.md` mục "Cấu trúc": chỉ liệt kê module thực sự được mang theo.
4. Có tên dự án → thay tiêu đề dòng đầu `CLAUDE.md`.
5. Tạo thư mục trống `output/`.

## B4. Kiểm tra và báo cáo
- Đủ file theo bảng; không có file nào thuộc danh sách cấm.
- Chạy trong thư mục mới: `python -I scripts/tc_to_xlsx.py` và `scripts/make_report.py` trên bản copy tạm của `samples/vi-du-dang-nhap/` (đặt trong `output/_check/`, kiểm xong xóa).
- Báo ngắn: đường dẫn, số file, mục nào lỗi. Bước tiếp theo của QC: mở thư mục mới trong VS Code, điền `acc.yaml`, kết nối Jira theo `JIRA_MCP.md`.
