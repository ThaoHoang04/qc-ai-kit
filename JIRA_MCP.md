# Kết nối Jira qua MCP (tuỳ chọn)

Chưa chốt loại Jira của team nên đây là hướng dẫn chung — cần xác nhận lại khi cấu hình.

| Loại Jira | Cách |
|---|---|
| Jira Cloud (xxx.atlassian.net) | Dùng Atlassian Remote MCP: `claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse`, rồi `/mcp` trong Claude Code để đăng nhập. |
| Jira Server / Data Center nội bộ | Cần MCP server cộng đồng dùng Personal Access Token (PAT) của từng QC. Chọn gói, cấu hình `JIRA_URL` + PAT trong `.mcp.json` hoặc biến môi trường — **không commit token**. |

Quy tắc dùng:
- Mỗi QC dùng token/tài khoản riêng của mình.
- AI chỉ **đọc** ticket tự do; **tạo/sửa issue chỉ sau khi QC xác nhận** (đã ghi trong các lệnh).
- Khi chưa kết nối: dán mô tả task vào lệnh, bug lấy từ `bugs.md` rồi dán lên Jira.

Việc cần làm tiếp: xác nhận loại Jira (Cloud/Server), chọn MCP server, thử `/test-task` với 1 ticket thật.
