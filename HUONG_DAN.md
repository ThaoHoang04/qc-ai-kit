# QC AI Kit — Hướng dẫn 1 trang

## Cài đặt (1 lần)
1. Cài Claude Code (CLI hoặc extension VS Code) và Python 3.10+.
2. `pip install openpyxl`
3. Mở thư mục `qc-ai-kit` trong VS Code, hoặc chạy `claude` trong thư mục này.
4. (Tuỳ chọn) Kết nối Jira — xem `JIRA_MCP.md`.

## Chọn lệnh theo việc đang làm
| Tình huống | Lệnh | Ví dụ |
|---|---|---|
| Task upcode / yêu cầu mới trên Jira | `/test-task` | `/test-task VNEDU-1234 vnedu` |
| Đã có bộ testcase (kiểm định, regression) | `/test-with-tc` | `/test-with-tc D:\tc\kiem_dinh_hss.xlsx` |
| Hệ thống mới, cần test toàn bộ | `/test-system` | `/test-system https://tsdc.example.vn tsdc` |

Không có Jira MCP: dán thẳng mô tả task thay cho Jira key.

## Luồng làm việc của QC (3 điểm bạn quyết định)
```
Đưa task  →  AI sinh TC (Excel)  →  [1] QC review, bổ sung
          →  chạy test, ghi kết quả  →  AI soạn bug  →  [2] QC xác nhận bug
          →  (log Jira)  →  báo cáo report.html   [3] QC đọc kết luận
```
AI không tự log Jira, không tự chốt TC khi bạn chưa đồng ý.

## Đầu vào cần có
- Mô tả task / tài liệu / link hệ thống.
- **Checklist** của hệ thống. Chưa có thì AI sẽ hỏi bạn: *bạn gửi* hay *AI tự sinh* (rồi bạn duyệt).
- AI luôn hỏi bằng câu trắc nghiệm; muốn trả lời khác thì chọn **Other** và gõ ý bạn.

## Kết quả nằm ở đâu
`output/<tên-task>/`
- `testcases.xlsx` — TC để review (sheet Coverage cho biết REQ nào đã đủ TC; cột "Kết quả" có dropdown)
- `report.html` — báo cáo mở bằng trình duyệt, lọc theo Pass/Fail
- `bugs.md` — bug đã soạn, copy dán Jira

## Báo kết quả test cho AI (khi bạn tự test)
Gõ ngắn: `TC_001 pass; TC_002 fail: nút Lưu không phản hồi; TC_003 blocked: chưa có dữ liệu`

## Mẹo
- Có checklist riêng của dự án → bỏ vào `checklists/du-an/<hệ thống>.md`.
- Ảnh/tài liệu đính kèm: để vào thư mục task và nói đường dẫn cho AI.
- Câu trả lời của AI dài hoặc lạc đề → gõ lại ngắn gọn yêu cầu; đừng dán lại cả tài liệu.
- Muốn đổi cột Excel cho khớp mẫu team: nhờ AI "sửa COLUMNS trong scripts/tc_to_xlsx.py theo mẫu này" và đưa file mẫu.

## Thử nhanh
Xem `samples/vi-du-dang-nhap/` (đã có sẵn testcases.xlsx và report.html để xem đầu ra trông thế nào).
