---
name: qc-<module>
description: Dùng khi test module <Tên module> — nạp rule + checklist riêng của module rồi sinh TC theo qc-testcase. Nạp TRƯỚC khi viết TC cho module này.
---

# Test module <Tên module>

1. Nạp skill `qc-testcase` (quy tắc viết TC + Quality Gate chung).
2. Đọc `modules/<module>/CLAUDE.md` (rule) và **chỉ phần liên quan** của `modules/<module>/checklist.md`.
3. Checklist đầu vào = `modules/<module>/checklist.md` (thay `checklists/du-an/<hệ thống>.md` ở mục 0 của `qc-testcase`). Thiếu mục cho task → hỏi QC gửi hay AI sinh bổ sung (trắc nghiệm).
4. Output ghi vào `modules/<module>/output/<task>/`.

## Điểm nhấn của module
- [điền: kỹ thuật ưu tiên, vd bảng chuyển trạng thái / bảng quyết định phân quyền]
- [điền: dữ liệu mẫu cụ thể dùng cho TC]

## Gate bổ sung
- [ ] [điền]
