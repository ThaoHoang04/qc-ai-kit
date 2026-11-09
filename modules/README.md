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

## Xác định module (AI tự làm khi nhận task)
1. Đọc nhanh mục "Phạm vi" + "Từ khoá nhận diện" của `modules/*/CLAUDE.md` (không đọc hết file).
2. So với tiêu đề/mô tả/component/tên màn hình trong task.
3. Báo kết quả + lý do 1 dòng, **hỏi QC xác nhận** (trắc nghiệm). Nhiều module → hỏi module chính + ảnh hưởng chéo. Không khớp → đề xuất tạo module mới.

## Thêm module mới
1. Copy `modules/_template/` → `modules/<module>/` (bỏ `SKILL.md` ra bước 2).
2. Copy `modules/_template/SKILL.md` → `.claude/skills/qc-<module>/SKILL.md`, thay `<module>`.
3. Điền `CLAUDE.md` + `checklist.md` (mục `[điền]`). Giữ mục nào chưa chắc là `[cần xác nhận]`.
4. Chạy: `/test-task <ticket>` (AI tự nhận module; có thể ghi kèm `module:<module>` để bỏ qua bước đoán).

AI tự thực hiện bước 1–3 khi gặp module mới, sau khi QC đồng ý.

Quy tắc chung (CLAUDE.md gốc + skill `qc-testcase`) luôn áp dụng; rule module chỉ **bổ sung**, không được mâu thuẫn.
