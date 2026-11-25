---
description: Test toàn hệ thống mới/lớn (vd TSDC) — khảo sát → danh sách REQ theo module → kế hoạch → sinh TC song song theo module
argument-hint: <URL hệ thống hoặc đường dẫn tài liệu> [tên hệ thống]
---
Nạp skill `qc-testcase`. Đầu vào: $ARGUMENTS

## B1. Khảo sát
- Tài khoản đăng nhập: lấy từ `acc.yaml` trước, không có mới hỏi (CLAUDE.md mục "Tài khoản test").
- Có tài liệu (md/pdf/docx/ảnh) → đọc. Có URL và Playwright MCP → mở desktop 1920x1080, đi qua từng menu, ghi lại màn hình/field/nút/trạng thái, chụp ảnh vào `output/<hệ thống>_<ngày>/evidence/`. **Không đoán** màn hình chưa mở được — ghi vào "Vùng chưa khảo sát".
- Không đủ thông tin đăng nhập/quyền → hỏi QC (trắc nghiệm, có Other).
- **Checklist:** theo skill `qc-testcase` mục 0 — chưa có thì hỏi QC gửi hay AI sinh; với hệ thống mới, AI sinh checklist **theo từng module** và QC duyệt cùng danh sách REQ ở B2.

- Hỏi môi trường cần check (`s99` / `s19` / `prod`, checkbox) theo skill `qc-testcase` mục 0a, **trước khi mở hệ thống**.

## B1b. Đối chiếu module với kit
Với mỗi module khảo sát được, đối chiếu `modules/*/`. Module chưa có folder → hỏi QC (trắc nghiệm) có tạo không; đồng ý → tạo từ `modules/_template/` + skill `qc-<module>` (theo `modules/README.md`), điền phần suy ra được, gắn `[cần xác nhận]`. Output từng module ghi vào `modules/<module>/output/`.

## B2. Danh sách module + REQ
Ghi `output/<hệ thống>_<ngày>/requirements.md`: module → REQ (mã `REQ-<MODULE>-<số>`) → rủi ro. Kèm ma trận phân quyền / trạng thái nếu có. **ĐIỂM DỪNG 1 — QC duyệt danh sách module và REQ, chọn module làm trước** (`AskUserQuestion`, có Other).

## B3. Kế hoạch
Báo 1 bảng ngắn: module · số REQ · ước tính số TC · thứ tự ưu tiên (High trước). **ĐIỂM DỪNG 2 — QC đồng ý** (`AskUserQuestion`: *Đồng ý* / *Đổi thứ tự ưu tiên* / *Thu hẹp phạm vi*, có Other).

## B4. Sinh TC song song
**Trước khi sinh:** hỏi loại TC (happy / unhappy / toàn bộ) theo skill mục 0b, hỏi 1 lần cho cả hệ thống và truyền lựa chọn cho từng subagent (subagent không hỏi lại).
Mỗi module = 1 subagent chạy song song (tối đa 4 cùng lúc), mỗi subagent chỉ nhận: phần REQ + evidence của module đó, skill `qc-testcase`, checklist liên quan. Mỗi subagent ghi `output/<...>/<module>/testcases.json` và chạy `tc_to_xlsx.py`; trả về **chỉ 1 dòng**: số TC, REQ thiếu, vấn đề.
Gộp: báo QC bảng tổng (module · số TC · trạng thái Gate) + đường dẫn các file `.xlsx`. **ĐIỂM DỪNG 3 — QC review** (`AskUserQuestion`: *Duyệt* / *Đã sửa Excel* / *Cần AI bổ sung*, có Other).

## B5. Sau review
Chạy test, bug, báo cáo: như `/test-task` B4–B6 (một `results.json` cho cả hệ thống, hoặc mỗi module một cái nếu nhiều tester).
