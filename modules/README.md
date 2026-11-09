# Modules

Mỗi module (hồ sơ số, sổ đầu bài, ...) = 1 thư mục riêng, gồm:

| Thành phần | Vị trí | Vai trò |
|---|---|---|
| Rule riêng | `modules/<module>/CLAUDE.md` | Tự nạp khi làm việc trong thư mục module: thuật ngữ, vai trò, trạng thái, quy tắc nghiệp vụ, cấm |
| Checklist riêng | `modules/<module>/checklist.md` | Điều kiện kiểm tra riêng của module (thay `checklists/du-an/`) |
| Skill riêng | `.claude/skills/qc-<module>/SKILL.md` | Cách sinh TC cho module (bắt buộc đặt ở `.claude/skills` để AI tự nhận) |
| Kết quả | `modules/<module>/output/<task>/` | testcases · results · report · bugs |

## Module hiện có
- `ho-so-so` — Hồ sơ số (mẫu)
- `so-dau-bai` — Sổ đầu bài (mẫu)

## Thêm module mới
1. Copy `modules/_template/` → `modules/<module>/` (bỏ `SKILL.md` ra bước 2).
2. Copy `modules/_template/SKILL.md` → `.claude/skills/qc-<module>/SKILL.md`, thay `<module>`.
3. Điền `CLAUDE.md` + `checklist.md` (mục `[điền]`). Giữ mục nào chưa chắc là `[cần xác nhận]`.
4. Chạy: `/test-task <ticket> module:<module>`.

Quy tắc chung (CLAUDE.md gốc + skill `qc-testcase`) luôn áp dụng; rule module chỉ **bổ sung**, không được mâu thuẫn.
