# Module: Sổ đầu bài — Rule riêng
Bổ sung cho `CLAUDE.md` gốc và skill `qc-testcase`. Skill: `qc-so-dau-bai`. Checklist: `modules/so-dau-bai/checklist.md`.

## Phạm vi
- Màn hình/chức năng: [cần xác nhận] chọn lớp/môn/tiết · ghi nội dung bài · điểm danh/xếp loại tiết · nhận xét · duyệt/khoá sổ
- Ngoài phạm vi: [điền]

## Từ khoá nhận diện (để AI xếp task vào module)
- [cần xác nhận] sổ đầu bài, tiết học, nội dung bài, nhận xét tiết, khoá sổ, thời khoá biểu
- [điền] tên màn hình, thuật ngữ, component Jira, từ hay gặp trong ticket

## Vai trò & phân quyền
| Vai trò | Quyền chính | Tài khoản test (tên biến, KHÔNG ghi mật khẩu) |
|---|---|---|
| [điền] | [điền] | [điền] |

## Thuật ngữ
- [điền]

## Trạng thái & chuyển trạng thái
- [cần xác nhận] Chưa ghi → Đã ghi → Đã duyệt → Khoá (quá hạn chỉnh sửa). Test sửa sau khi khoá. (vd: Nháp → Chờ duyệt → Đã duyệt → Khoá)

## Quy tắc nghiệp vụ bắt buộc kiểm
- [cần xác nhận] Đúng thời khoá biểu/tiết · giáo viên chỉ ghi lớp mình dạy · không ghi ngày tương lai/trùng tiết · liên thông điểm danh

## Ảnh hưởng chéo (module/chức năng liên quan phải hồi quy)
- [điền]

## Quy ước TC
- Mã TC: `<DUAN>_<MODULE>_TC_<3 số>`; mã REQ: `REQ-<MODULE>-<số>`
- Output: `modules/so-dau-bai/output/<task>/`

## Cấm riêng module
- [điền]
