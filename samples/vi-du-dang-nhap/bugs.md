# Danh sách bug (copy dán Jira)

## BUG-01 — Cho phép đăng nhập khi email không có @
- Severity: Major
- TC: DEMO_LOGIN_TC_002
- Môi trường: UAT

**Các bước:**
1. Mở /login
2. Nhập email: test_login_01auto.test
3. Nhập mật khẩu: Test@123
4. Click Đăng nhập

**Mong đợi:** Báo lỗi Email không hợp lệ

**Thực tế:** Đăng nhập thành công

**Bằng chứng:** screenshots/bug01.png
