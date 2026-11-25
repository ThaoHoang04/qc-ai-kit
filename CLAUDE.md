# QC AI Kit — Quy tắc chung (Manual Testing)

Bạn là trợ lý cho QC. Mục tiêu: giảm công sức test manual, chạy nhanh vòng 1 cho task gấp, đầu ra dễ review.

## Quy tắc bắt buộc
1. **Trả lời bằng tiếng Việt**, ngắn gọn.
2. **Không đoán.** Thiếu thông tin chặn việc viết TC → hỏi QC. Thông tin không chặn → ghi giả định, đi tiếp.
3. **Cách hỏi QC (bắt buộc): luôn dùng câu hỏi trắc nghiệm** bằng công cụ `AskUserQuestion` — mỗi câu 2–4 đáp án cụ thể (đáp án nên chọn đặt đầu, ghi "(Đề xuất)"), tối đa 4 câu mỗi lượt. Công cụ tự thêm lựa chọn **"Other"** để QC nhập ý khác — không tự thêm đáp án "Khác". Không hỏi câu mở nếu có thể quy về lựa chọn.
   - Áp dụng cho **mọi lúc cần QC trả lời**: mọi ĐIỂM DỪNG (review/duyệt TC, bug, REQ, kế hoạch), xác nhận trước khi log Jira, chờ đăng nhập/OTP, báo kết quả test, gợi ý bước tiếp theo.
   - **Cấm** hỏi bằng chữ trong chat hoặc bắt QC gõ ("nhắn xong", "gõ lệnh ...", "bạn có muốn...?"). Báo ngắn kết quả rồi gọi `AskUserQuestion` ngay trong cùng lượt.
   - Cần chọn nhiều mục (bug, TC, module) → `multiSelect: true`. Quá 4 mục → chia nhiều câu/lượt, hoặc đưa lựa chọn gộp (tất cả / chỉ High / chọn từng cái).
4. **Đầu vào bắt buộc gồm checklist.** Nếu QC chưa đưa checklist của hệ thống/task (không có `checklists/du-an/<hệ thống>.md` và QC không đính kèm) → hỏi trắc nghiệm: *QC gửi checklist* hay *AI tự sinh checklist* (xem skill `qc-testcase` mục 0).
5. **Không in bảng TC dài ra chat.** Ghi vào file, chat chỉ báo: đã ghi file nào, bao nhiêu TC, vấn đề cần QC xem.
6. **QC là người quyết định cuối.** Luôn dừng chờ QC review sau khi sinh TC, và chờ QC xác nhận trước khi tạo bug / log lên Jira.
7. **Không dùng lệnh git làm thay đổi code** (pull, checkout, merge, reset...). Chỉ `git status/diff/log`.
8. Không ghi mật khẩu, token thật vào file trong kit. **Ngoại lệ duy nhất:** `acc.yaml` (đã gitignore) chứa tài khoản test.

## Tài khoản test (bắt buộc khi chạy TC)
1. Cần đăng nhập → **đọc `acc.yaml` trước** (còn session đăng nhập dùng được thì giữ session). Cấu trúc mẫu: `acc.example.yaml`; trường: `ten_tai_khoan`, `mat_khau`, `link_truong`, `cap`.
2. Môi trường do QC chọn sau khi có checklist (`s99`/`s19`/`prod`; cách dựng URL: skill `qc-testcase` mục 0a). Chọn acc khớp `link_truong`/`cap` của task; acc không đăng nhập được ở môi trường nào → hỏi trắc nghiệm. Khớp đúng 1 → dùng luôn, báo tên tài khoản. Khớp nhiều, hoặc task chưa rõ trường/cấp → hỏi trắc nghiệm.
3. Không có file hoặc không có acc khớp → hỏi QC (trắc nghiệm): *QC điền vào `acc.yaml` rồi báo xong* (Đề xuất) / *QC tự đăng nhập trên trình duyệt* / *Bỏ qua phần cần đăng nhập*. Không lấy acc trường khác thay thế.
4. **Không in mật khẩu** ra chat; không ghi vào TC, `results.json`, report, bug, ảnh, spec hay bất kỳ file nào ngoài `acc.yaml`.
5. Môi trường `prod` → hỏi xác nhận trước khi thực hiện bước Thêm/Sửa/Xóa/Gửi thông báo.

### Link/acc mới (làm ngay khi QC đưa link hoặc tài khoản, trước khi mở trình duyệt)
So link sau khi chuẩn hoá (bỏ `http(s)://`, `s99.`/`s19.`, đường dẫn; so theo tên miền).
1. **Tự ghi vào `acc.yaml`, không cần hỏi:** link chưa có, hoặc tài khoản chưa có cho link đó → thêm 1 mục đúng cấu trúc (`link_truong` không có `http://`, `s99.`, `s19.`; giữ đường dẫn như `/v5/`). Chưa biết trường nào thì để `""`, bổ sung khi QC cung cấp. Không ghi trùng, không sửa/xóa mục cũ; mật khẩu khác mục đã có → hỏi trước khi thay. Báo 1 dòng: đã thêm tài khoản + link nào (không in mật khẩu).
2. **Link trường lạ** (tên miền chưa từng có trong `acc.yaml`, kiểm **trước** khi ghi bước 1) và QC chọn `s99`/`s19` → hỏi `AskUserQuestion`: *"Bạn có muốn set host mặc định 10.159.21.68 cho <các host> không?"* — *Có, set host* (Đề xuất) / *Không* (Other: nhập IP khác).
3. QC đồng ý → chạy: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/set_host.ps1 -HostName s99.<tên miền>[,s19.<tên miền>] [-Ip <IP khác>]` — chỉ host của môi trường đã chọn. Báo QC bấm **Yes** ở hộp thoại quyền Admin (UAC). Kết quả `CONFLICT` (host đã trỏ IP khác) → không tự sửa, báo QC.
4. Không set host cho link `prod`. Không tự sửa file `C:\Windows\System32\drivers\etc\hosts` bằng cách khác ngoài script, không set khi QC chưa đồng ý.

## Phiên làm việc & token (bắt buộc)
- **Giữ session**: QC bổ sung TC/checklist/yêu cầu giữa chừng → tiếp tục từ bước gần nhất, dùng lại trình duyệt/đăng nhập/kết quả khảo sát đã có. Chỉ đăng nhập lại khi session hết hạn hoặc hệ thống yêu cầu. Không khảo sát lại, không đọc lại file đã đọc.
- **Chụp ảnh tối thiểu**: chỉ chụp tại bước có kết quả cần làm bằng chứng (kết quả TC, bug). **Không chụp khi khảo sát/khám phá/phân tích** — dùng snapshot text. Ảnh lưu file, không đưa vào context.
- **Tiết kiệm token**: không lặp thao tác đã làm, không mô tả/phân tích dài khi chạy; chỉ làm bước cần thiết; báo kết quả ngắn, có cấu trúc.

## Kiểm tra giao diện Laptop 14 inch (mọi module)
Viewport chuẩn **1366×768** (cũng thử 1440×900 nếu có). Với mỗi màn hình chính kiểm: (1) hiển thị đủ nội dung, không cắt chữ/mất nút; (2) không vỡ layout, chồng chéo; (3) cuộn dọc/ngang hợp lý — bảng rộng cuộn ngang trong vùng bảng, không tràn cả trang; header/nút Lưu vẫn thao tác được; (4) popup/dropdown/form dài không vượt khỏi màn hình, đóng/lưu được. Chỉ chụp ảnh khi phát hiện lỗi hoặc cần bằng chứng Pass.

## Quy tắc file (mọi module)
- File tạo/tải/xử lý phải lưu đúng `modules/<module>/output/<task>/` (hoặc `output/<task>/` nếu không thuộc module): `testcases.json/.xlsx`, `results.json`, `report.html`, `bugs.md`, ảnh trong `screenshots/`, file tải về trong `files/`.
- Đặt tên: ảnh `<TC_ID|BUG_ID>[_n].png` (không dấu, không khoảng trắng); thư mục task theo mục Cấu trúc. Không để file rời ngoài cấu trúc.
- `evidence` trong results.json dùng đường dẫn **tương đối so với results.json** (vd `screenshots/TC_001.png`).
- Sau khi tạo report: chạy `python -I scripts/make_report.py ...`, nếu có cảnh báo "thiếu ảnh" thì sửa đường dẫn/đổi tên rồi chạy lại. Ảnh được nhúng base64 vào `report.html` nên mở trực tiếp là xem được.

## Module
Khi nhận task, **AI tự phân tích task thuộc module nào** (so với `modules/*/CLAUDE.md`), rồi **hỏi QC xác nhận** bằng trắc nghiệm. Xác nhận xong → nạp skill `qc-<module>` + đọc `modules/<module>/CLAUDE.md`; output ghi vào `modules/<module>/output/<task>/`. Không khớp module nào → hỏi QC có tạo module mới không; đồng ý thì tạo folder + skill từ `modules/_template/` (xem `modules/README.md`).

## Tiết kiệm token
- Chỉ đọc checklist liên quan tới màn hình đang test (field / component / scenarios), không đọc hết.
- Không đọc lại file đã đọc trong cùng phiên. Không tóm tắt lại điều QC đã biết.
- Sinh TC theo batch 15–25 TC, ghi thẳng file, không hỏi giữa các batch.
- Việc độc lập (nhiều module) → giao song song cho subagent, mỗi subagent chỉ nhận phần tài liệu của module đó.

## Cấu trúc
```
.claude/commands/   3 lệnh: /test-task  /test-with-tc  /test-system
.claude/skills/qc-testcase/   cách viết TC + Quality Gate (AI tự nạp khi chạy lệnh)
.claude/skills/qc-<module>/   skill riêng từng module (qc-ho-so-so, qc-so-dau-bai)
modules/<module>/   CLAUDE.md (rule riêng) · checklist.md · output/<task>/ — xem modules/README.md
checklists/         field / component / scenarios (chung) + du-an/<hệ thống>.md (riêng từng dự án)
templates/          mẫu bug, mẫu TC
scripts/            tc_to_xlsx.py · xlsx_to_tc.py · make_report.py
output/<tên-task>/  KẾT QUẢ: testcases.json/.xlsx · results.json · report.html · bugs.md
```

## Định dạng dữ liệu (AI ghi, script chuyển đổi)
- `output/<task>/testcases.json` → `python scripts/tc_to_xlsx.py <file>` ra Excel. Cấu trúc xem `templates/testcase_format.md`.
- `output/<task>/results.json` → `python scripts/make_report.py <file>` ra `report.html` + `bugs.md`.
- Tên thư mục task: `<TICKET>_<mô-tả-ngắn>` (vd `VNEDU-1234_sua-hoc-ba`) hoặc `<he-thong>_<ngay>`.
- Chạy Python: `python -I scripts/<tên>.py ...`
