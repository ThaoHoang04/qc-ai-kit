# -*- coding: utf-8 -*-
"""Sinh 3 ảnh luồng toàn dự án luong-tong-quan-*.png (dùng chung khung vẽ của make_flows.py).
Chạy: python -I scripts/make_flows_overview.py"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_flows as mf

# step: (id, lane, row, title, [dòng], điểm_dừng|None, style) · id < 20 được đánh số, ô kết quả dùng id 20, 30...
FLOWS = {
 "luong-tong-quan-1": dict(
  title="1/3 — TỔNG QUAN TOÀN DỰ ÁN QC AI KIT",
  sub="Từ giao việc đến báo cáo · chi tiết bước chuẩn bị ở ảnh 2, bước chạy test ở ảnh 3",
  steps=[
   (1, "qc", 0, "Chọn lệnh theo đầu vào", ["/test-task: ticket Jira hoặc mô tả task", "/test-with-tc: file Excel testcase", "/test-system: hệ thống mới (URL)"], None, ""),
   (2, "ai", 0, "Nạp rule + skill", ["CLAUDE.md · .claude/commands", "skill qc-testcase"], None, ""),
   (20, "out", 0, "Bộ quy tắc của kit", ["checklists/ (field · component · scenarios · du-an)", "templates/ · scripts/"], None, ""),
   (3, "ai", 1, "Đọc đầu vào", ["Ticket + comment / file TC / khảo sát hệ thống"], None, ""),
   (30, "out", 1, "Nguồn yêu cầu", ["Jira MCP · file .xlsx · trình duyệt"], None, ""),
   (4, "ai", 2, "Xác định module", ["So với Phạm vi + Từ khoá nhận diện", "Không khớp → đề xuất module mới"], None, ""),
   (5, "qc", 2, "Xác nhận module", ["Trắc nghiệm, có Other"], 0, ""),
   (40, "out", 2, "modules/<module>/", ["CLAUDE.md · checklist.md", "skill qc-<module>"], None, "warn"),
   (6, "ai", 3, "Chuẩn bị (ảnh 2)", ["Checklist · môi trường · tài khoản · host", "Loại TC cần sinh"], None, ""),
   (60, "out", 3, "acc.yaml · file hosts", ["tài khoản test (không commit)", "s99/s19 → IP test"], None, ""),
   (7, "ai", 4, "Sinh hoặc nạp testcase", ["Quality Gate · ghi file, không in bảng"], None, ""),
   (8, "qc", 4, "Review testcase", ["Duyệt / đã sửa Excel / AI bổ sung"], 1, ""),
   (70, "out", 4, "testcases.json / .xlsx", ["modules/<module>/output/<task>/"], None, ""),
   (9, "ai", 5, "Chạy test (ảnh 3)", ["Web: playwright-cli · App: mobile-mcp", "hoặc QC tự test và báo kết quả"], None, ""),
   (90, "out", 5, "results.json + screenshots/", ["Pass / Fail / Blocked / Skip"], None, ""),
   (10, "ai", 6, "Soạn bug cho TC Fail", ["Theo bug_template.md"], None, ""),
   (11, "qc", 6, "Xác nhận từng bug", ["Log / bỏ / gộp"], 2, ""),
   (100, "out", 6, "bugs.md", ["bản nháp bug"], None, ""),
   (12, "ai", 7, "Log Jira + báo cáo", ["Chỉ log sau khi QC đồng ý", "make_report.py"], None, ""),
   (13, "qc", 7, "Đọc kết luận", ["Quyết định release / yêu cầu sửa"], None, ""),
   (120, "out", 7, "report.html + Jira", ["báo cáo nhúng ảnh bằng chứng"], None, ""),
   (14, "qc", 8, "Nhân bản kit (khi cần)", ["gõ: /tao-du-an <thư mục mới>", "chọn module / checklist mang theo"], None, ""),
   (15, "ai", 8, "Tạo dự án mới", ["Copy cấu trúc, kiểm tra script", "Không copy acc, session, output"], None, ""),
   (150, "out", 8, "Dự án QC mới", ["cùng cấu trúc, acc.yaml trống"], None, "warn"),
  ],
  edges=[(1, 2, ""), (2, 20, ""), (2, 3, ""), (3, 30, ""), (3, 4, ""), (4, 40, ""), (4, 5, "hỏi"), (5, 6, "QC OK"),
         (6, 60, ""), (6, 7, ""), (7, 70, ""), (7, 8, ""), (8, 9, "duyệt"), (9, 90, ""), (9, 10, ""), (10, 100, ""),
         (10, 11, ""), (11, 12, "đồng ý"), (12, 120, ""), (12, 13, ""), (14, 15, ""), (15, 150, "")]),
 "luong-tong-quan-2": dict(
  title="2/3 — CHUẨN BỊ TRƯỚC KHI TEST",
  sub="Checklist → môi trường → link và tài khoản → set host → loại testcase · mọi câu hỏi là trắc nghiệm có Other",
  steps=[
   (1, "ai", 0, "Tìm checklist", ["File QC đính kèm → checklist module / dự án", "Chưa có → hỏi"], None, ""),
   (2, "qc", 0, "Chọn nguồn checklist", ["QC gửi / AI tự sinh / bỏ qua"], 0, ""),
   (20, "out", 0, "checklist.md", ["[QC] · [Jira] · [AI-giả định]"], None, ""),
   (3, "ai", 1, "Hỏi môi trường", ["Ô tick, chọn nhiều"], None, ""),
   (4, "qc", 1, "Chọn môi trường", ["☐ s99   ☐ s19   ☐ prod"], 1, ""),
   (30, "out", 1, "URL được dựng", ["s99 → http://s99.<link trường>", "s19 → http://s19.<link trường>", "prod → <link trường>"], None, ""),
   (5, "ai", 2, "Đối chiếu link + tài khoản", ["Kiểm link có lạ không, rồi mới ghi", "Chưa có → tự thêm vào file", "Mật khẩu khác mục cũ → hỏi"], None, ""),
   (50, "out", 2, "acc.yaml", ["ten_tai_khoan · mat_khau", "link_truong · cap"], None, ""),
   (6, "ai", 3, "Link lạ + chọn s99/s19?", ["Tên miền chưa từng có trong acc.yaml", "Không phải → bỏ qua bước set host"], None, ""),
   (7, "qc", 3, "Set host 10.159.21.68?", ["Có / Không / Other: IP khác"], 2, ""),
   (8, "ai", 4, "Chạy set_host.ps1", ["Chỉ khi QC đồng ý · không set cho prod", "Host đã trỏ IP khác → chỉ báo"], None, ""),
   (9, "qc", 4, "Bấm Yes (UAC)", ["cấp quyền Admin"], None, ""),
   (80, "out", 4, "drivers\\etc\\hosts", ["<IP>  s99.<link trường>"], None, "warn"),
   (10, "ai", 5, "Hỏi loại testcase", ["Ô tick, chọn nhiều"], None, ""),
   (11, "qc", 5, "Chọn loại TC", ["☐ Toàn bộ   ☐ Happy   ☐ Unhappy"], 3, ""),
   (12, "ai", 6, "Phân tích + sinh testcase", ["REQ + rủi ro → TC → Quality Gate", "batch 15–25 TC"], None, ""),
   (120, "out", 6, "testcases.json / .xlsx", ["sheet Testcase + Coverage"], None, ""),
   (13, "qc", 7, "Review testcase", ["Duyệt rồi sang bước chạy test (ảnh 3)"], 4, ""),
  ],
  edges=[(1, 2, "hỏi"), (1, 20, ""), (2, 3, ""), (8, 80, ""), (3, 4, "hỏi"), (3, 30, ""), (4, 5, ""), (5, 50, "ghi"), (5, 6, ""), (6, 7, "hỏi"),
         (7, 8, "đồng ý"), (8, 9, ""), (8, 10, ""), (10, 11, "hỏi"), (11, 12, ""), (12, 120, ""), (12, 13, "")]),
 "luong-tong-quan-3": dict(
  title="3/3 — CHẠY TEST, GHI BUG, BÁO CÁO",
  sub="Giữ session · chụp ảnh tối thiểu · không in mật khẩu · AI không tự log Jira",
  steps=[
   (1, "ai", 0, "Kiểm session đăng nhập", ["Còn hiệu lực → dùng lại", "Hết hạn → đăng nhập"], None, ""),
   (2, "ai", 1, "Đăng nhập", ["Ưu tiên acc.yaml theo link + cấp"], None, ""),
   (3, "qc", 1, "Khi cần QC", ["Không có acc khớp, nhiều acc, QR/OTP", "Chọn đáp án hoặc tự đăng nhập"], 0, ""),
   (20, "out", 1, "acc.yaml", ["không ghi mật khẩu ra nơi khác"], None, ""),
   (4, "ai", 2, "Môi trường prod?", ["Trước Thêm / Sửa / Xóa / Gửi thông báo"], None, ""),
   (5, "qc", 2, "Xác nhận thao tác prod", ["Đồng ý / bỏ qua"], 1, ""),
   (6, "ai", 3, "Chạy TC theo từng môi trường", ["playwright-cli / mobile-mcp", "Chỉ chụp ảnh ở bước cần bằng chứng"], None, ""),
   (60, "out", 3, "screenshots/ · files/", ["<TC_ID|BUG_ID>[_n].png"], None, ""),
   (7, "ai", 4, "Kiểm giao diện laptop 14 inch", ["1366×768 (thử thêm 1440×900)", "đủ nội dung · không vỡ · cuộn · popup"], None, ""),
   (8, "ai", 5, "Ghi kết quả", ["Pass / Fail / Blocked / Skip + thực tế"], None, ""),
   (80, "out", 5, "results.json", ["nhiều môi trường:", "output/<task>/<môi trường>/"], None, ""),
   (9, "ai", 6, "Soạn bug", ["1 bug = 1 nguyên nhân"], None, ""),
   (10, "qc", 6, "Xác nhận từng bug", ["Log / bỏ / gộp"], 2, ""),
   (90, "out", 6, "bugs.md", ["bản nháp"], None, ""),
   (11, "ai", 7, "Log bug lên Jira", ["Chỉ sau khi QC đồng ý", "Không có MCP → QC dán từ bugs.md"], None, ""),
   (110, "out", 7, "Jira", ["bug gắn ticket gốc"], None, ""),
   (12, "ai", 8, "Sinh báo cáo", ["make_report.py", "thiếu ảnh → sửa rồi chạy lại"], None, ""),
   (13, "qc", 8, "Đọc kết luận", ["QC là người quyết định cuối"], None, ""),
   (120, "out", 8, "report.html", ["mở trực tiếp xem được ảnh"], None, ""),
  ],
  edges=[(1, 2, ""), (2, 20, ""), (2, 3, "hỏi"), (2, 4, ""), (4, 5, "prod"), (4, 6, ""), (6, 60, ""), (6, 7, ""), (7, 8, ""),
         (8, 80, ""), (8, 9, ""), (9, 90, ""), (9, 10, ""), (10, 11, "đồng ý"), (11, 110, ""), (11, 12, ""), (12, 120, ""),
         (12, 13, "")]),
}

if __name__ == "__main__":
    mf.FLOWS = FLOWS
    mf.main()
