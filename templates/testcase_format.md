# Định dạng testcases.json (AI ghi file này, script chuyển sang Excel)

```json
{
  "project": "VNEDU",
  "ticket": "VNEDU-1234",
  "requirements": [
    {"id": "REQ-HOCBA-01", "desc": "Sửa điểm học bạ lưu thành công"}
  ],
  "testcases": [
    {
      "tc_id": "VNEDU_HOCBA_TC_001",
      "req_id": "REQ-HOCBA-01",
      "module": "Học bạ",
      "type": "Positive",
      "risk": "High",
      "title": "Sửa điểm hợp lệ và lưu thành công",
      "precondition": "Đăng nhập GV, lớp 10A1 có học sinh",
      "steps":    ["Mở Học bạ lớp 10A1", "Sửa điểm Toán của HS Nguyễn Văn A thành 8.5", "Click Lưu"],
      "expected": ["Hiển thị bảng điểm lớp", "Ô điểm hiện 8.5", "Báo 'Lưu thành công', điểm 8.5 còn sau khi tải lại"],
      "test_data": "HS: Nguyễn Văn A, điểm: 8.5",
      "priority": "High"
    }
  ]
}
```

- `steps` / `expected`: mảng, **khớp 1–1** (bước nào chưa có kết quả quan sát → `""`).
- `type`: Positive | Negative | Boundary. `risk`/`priority`: High | Medium | Low.
- Cột Excel sinh ra: TC ID · REQ ID · Module · Loại · Rủi ro · Tiêu đề · Điều kiện tiên quyết · Các bước · Kết quả mong đợi · Dữ liệu test · Ưu tiên · Kết quả (dropdown) · Bug ID · Ghi chú; thêm sheet **Coverage** (REQ × số TC).
- Muốn đổi cột cho khớp mẫu chính thức của team: sửa danh sách `COLUMNS` ở đầu `scripts/tc_to_xlsx.py`.

# Định dạng results.json (kết quả chạy → report.html)

```json
{
  "title": "Học bạ - task VNEDU-1234", "tester": "QC A", "date": "2026-11-08", "env": "UAT", "ticket": "VNEDU-1234",
  "conclusion": "2 bug Major, chưa nên release.",
  "results": [
    {"tc_id": "VNEDU_HOCBA_TC_001", "title": "...", "status": "Pass|Fail|Blocked|Skip", "actual": "", "bug_id": "BUG-01", "evidence": ["screenshots/TC_001.png"]}
  ],
  "bugs": [
    {"id": "BUG-01", "title": "...", "severity": "Critical|Major|Minor|Trivial", "tc_id": "...",
     "steps": ["..."], "expected": "...", "actual": "...", "evidence": ["screenshots/BUG-01.png"], "jira": ""}
  ]
}
```

- `evidence`: mảng (hoặc chuỗi) đường dẫn ảnh **tương đối so với thư mục chứa results.json** (vd `screenshots/TC_001.png`). `make_report.py` nhúng ảnh base64 vào `report.html` → mở ở đâu cũng xem được; thiếu file sẽ cảnh báo.
