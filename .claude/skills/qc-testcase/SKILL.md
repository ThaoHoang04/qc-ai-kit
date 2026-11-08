---
name: qc-testcase
description: Cách viết testcase manual chuẩn cho team QC — định dạng, kỹ thuật, checklist, Quality Gate. Nạp khi sinh hoặc review testcase.
---

# Viết testcase manual (bản rút gọn từ AI-RBT)

## 0. Checklist đầu vào (kiểm tra TRƯỚC khi sinh TC)
Checklist dự án = quy tắc nghiệp vụ/kiểm tra riêng của hệ thống. Thứ tự tìm: file QC đính kèm → `checklists/du-an/<hệ thống>.md`.
Chưa có → hỏi QC bằng `AskUserQuestion` (trắc nghiệm, có Other):
- *QC gửi checklist* → chờ QC đưa file/đường dẫn rồi dùng.
- *AI tự sinh checklist* (đề xuất khi task gấp) → AI sinh `output/<task>/checklist.md` từ mô tả task + checklist chung: mỗi mục là 1 điều kiện kiểm tra cụ thể (nhóm: chức năng chính · validate · phân quyền · dữ liệu/tính toán · giao diện · tích hợp/ảnh hưởng chức năng liên quan), đánh dấu mục nào suy ra từ mô tả (`[Jira]`) và mục nào AI suy luận (`[AI-giả định]`). QC duyệt/sửa, rồi hỏi tiếp: *lưu vào `checklists/du-an/<hệ thống>.md` để dùng lại* hay *chỉ dùng cho task này*.
- *Bỏ qua checklist riêng* → chỉ dùng 3 checklist chung; ghi rõ điều này trong báo cáo.
Mọi REQ/TC sinh ra phải đối chiếu được với checklist (cột `note` hoặc `req_id` chỉ ra mục checklist liên quan).

## 1. Quy trình sinh TC
1. **Rút REQ**: từ mô tả/tài liệu, liệt kê yêu cầu kiểm thử được, mã `REQ-<MODULE>-<số>`, mỗi REQ 1 dòng.
2. **Xếp rủi ro** từng REQ: High (tiền, quyền, dữ liệu quan trọng, luồng chính) / Medium / Low. High → đủ Positive + Negative + Boundary.
3. **Chọn checklist** (đọc đúng phần cần):
   - Có ô nhập → `checklists/field_checklist.md`
   - Có bảng/CRUD/phân quyền/modal/trạng thái → `checklists/component_checklist.md`
   - Task nhạy cảm (tiền, nhập liệu nhiều, nhiều user) → `checklists/scenarios_checklist.md`
   - Có `checklists/du-an/<hệ thống>.md` → bắt buộc đối chiếu.
4. **Kỹ thuật**: field có min/max/format → EP+BVA (test `min-1, min, max, max+1`); ≥3 điều kiện kết hợp → bảng quyết định; ≥3 trạng thái → bảng chuyển trạng thái (cả chuyển hợp lệ lẫn bị chặn).
5. **Ghi `testcases.json`** (batch 15–25 TC), chạy `tc_to_xlsx.py`, chạy Quality Gate.

## 2. Quy tắc viết
- **Mỗi bước 1 hành động.** `steps` và `expected` là mảng; `expected[i]` ứng với `steps[i]` — bước nào không quan sát được kết quả thì để chuỗi rỗng `""`, **không bỏ phần tử** (giữ khớp 1–1).
- **Dữ liệu cụ thể**: ✅ "Nhập mã: KH-2026-0012" ❌ "Nhập mã hợp lệ".
- Tiêu đề bắt đầu bằng hành vi: "Đăng nhập thành công khi...", "Không cho lưu khi...".
- TC độc lập nhau. Mỗi field validation = TC riêng.
- `type`: `Positive` | `Negative` | `Boundary`. `priority`/`risk`: `High` | `Medium` | `Low`.
- TC ID: `<DUAN>_<MODULE>_TC_<3 số>`, không trùng.

## 3. Quality Gate (tự kiểm trước khi báo QC) — 5 mục
- [ ] TC ID không trùng
- [ ] steps/expected khớp 1–1, mỗi bước 1 hành động
- [ ] Không còn dữ liệu mơ hồ ("hợp lệ", "đúng")
- [ ] Mọi REQ có ≥1 TC (script `tc_to_xlsx.py` in cảnh báo REQ thiếu — phải bổ sung hết); REQ High có Positive + Negative
- [ ] Mọi field trên màn hình có ≥1 Positive và ≥2 Negative/Boundary

Kết quả Gate báo QC bằng **một dòng tổng hợp** + danh sách điểm chưa đạt (nếu có). Không in bảng.

## 4. Cấm
- Sinh TC khi chưa hiểu yêu cầu, bịa tính năng không có trong tài liệu.
- Gộp nhiều field/nhiều hành động vào 1 TC hoặc 1 bước.
- Tự ý tạo bug / log Jira khi QC chưa xác nhận.
