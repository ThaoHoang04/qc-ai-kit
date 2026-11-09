# -*- coding: utf-8 -*-
"""Sinh 3 ảnh luồng luong-test-*.png (swimlane) bằng HTML + Edge/Chrome headless.
Chạy: python -I scripts/make_flows.py   (sửa nội dung ở FLOWS bên dưới rồi chạy lại)"""
import html, json, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BROWSERS = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"]

# step: (id, lane, row, title, [dòng], số_điểm_dừng|None, style)   lane: qc|ai|out
# edge: (từ, đến, nhãn)
MOD_AI = ("Xác định module (AI tự phân tích)",
          ["So task với Phạm vi + Từ khoá nhận diện", "của modules/*/CLAUDE.md"])
NEW_MOD = ("modules/<module>/",
           ["Khớp → dùng module có sẵn", "Không khớp → module mới: tạo từ _template",
            "(CLAUDE.md · checklist.md · skill qc-<module>)"])

FLOWS = {
 "luong-test-task": dict(
  title="LUỒNG /test-task — TASK UPCODE TRÊN JIRA",
  sub="Đầu vào: Jira key hoặc mô tả task · AI tự xác định module, QC xác nhận",
  steps=[
   (1, "qc", 0, "Giao task", ["gõ: /test-task VNEDU-1234", "(hoặc dán mô tả task)"], None, ""),
   (2, "ai", 0, "Đọc yêu cầu", ["Đọc ticket qua Jira MCP", "mô tả · AC · comment · file đính kèm"], None, ""),
   (20, "out", 0, "Jira", ["ticket nguồn (chỉ ĐỌC ở bước này)"], None, ""),
   (3, "ai", 1, *MOD_AI, None, ""),
   (30, "out", 1, *NEW_MOD, None, "warn"),
   (4, "qc", 2, "Xác nhận module", ["○ Đúng module AI nêu  ○ Chọn module khác", "○ Nhiều module (chính + ảnh hưởng chéo)", "○ Module mới → tạo folder + skill  ○ Other"], 0, ""),
   (5, "ai", 3, "Nạp skill + checklist module", ["Nạp qc-<module> + rule module", "Checklist: modules/<module>/checklist.md", "Chưa có → hỏi QC"], None, ""),
   (6, "qc", 3, "Chưa có checklist → AI hỏi", ["○ QC gửi checklist  ○ AI tự sinh (đề xuất)", "○ Bỏ qua (dùng checklist chung)  ○ Other"], 1, ""),
   (50, "out", 3, "checklist.md", ["AI sinh: mục [Jira] / [AI-giả định]", "QC duyệt → lưu vào module hoặc chỉ task này"], None, "warn"),
   (7, "ai", 4, "Phân tích", ["Rút REQ-… + xếp rủi ro High/Med/Low", "Mơ hồ chặn việc viết TC → hỏi QC"], None, ""),
   (8, "qc", 4, "Trả lời câu hỏi (nếu có)", ["Trắc nghiệm, chọn đáp án hoặc Other"], 2, ""),
   (9, "ai", 5, "Sinh testcase", ["Theo skill qc-testcase + rule/checklist module", "Quality Gate 5 mục · batch 15–25 TC", "Không in bảng ra chat"], None, ""),
   (90, "out", 5, "modules/<module>/output/<task>/", ["testcases.json → testcases.xlsx", "sheet Testcase + sheet Coverage (REQ × TC)"], None, ""),
   (10, "qc", 6, "QC review / bổ sung TC", ["Sửa trong Excel hoặc nhắn AI sửa", "→ xlsx_to_tc.py đồng bộ lại"], 3, ""),
   (11, "ai", 7, "Chạy test & ghi kết quả", ["A: AI chạy playwright-cli / mobile-mcp (QC cho phép)", "B: QC tự test, báo ngắn: TC_001 pass; TC_002 fail: …"], None, ""),
   (110, "out", 7, "results.json (+ screenshots/)", ["mỗi TC: Pass / Fail / Blocked / Skip", "thực tế · bug_id · bằng chứng"], None, ""),
   (12, "ai", 8, "Soạn bug cho TC Fail", ["Theo templates/bug_template.md", "1 bug = 1 nguyên nhân · soát trùng"], None, ""),
   (120, "out", 8, "bugs.md", ["bản nháp bug — chưa gửi đi đâu"], None, ""),
   (13, "qc", 9, "QC xác nhận từng bug", ["Giữ / sửa / gộp / bỏ"], 4, ""),
   (14, "ai", 10, "Log bug lên Jira", ["Chỉ SAU khi QC đồng ý", "Jira MCP tạo Bug, link ticket gốc", "Không có MCP: QC dán từ bugs.md"], None, ""),
   (140, "out", 10, "Jira", ["Bug mới gắn vào ticket gốc", "key ghi lại vào results.json"], None, ""),
   (15, "ai", 11, "Báo cáo", ["make_report.py results.json → report.html"], None, ""),
   (150, "out", 11, "report.html", ["Số Pass/Fail/Blocked · tỉ lệ Pass", "danh sách bug · bảng TC lọc theo trạng thái"], None, ""),
   (16, "qc", 11, "QC đọc kết luận", ["Quyết định release / yêu cầu dev sửa"], None, ""),
  ],
  edges=[(1, 2, ""), (2, 20, ""), (2, 3, ""), (3, 30, ""), (3, 4, "hỏi xác nhận"), (4, 5, "QC OK"), (5, 6, "chưa có"),
         (5, 50, "AI sinh"), (6, 7, "QC trả lời"), (7, 8, "hỏi"), (8, 9, ""), (9, 90, ""), (9, 10, ""), (10, 11, "QC OK"),
         (11, 110, ""), (11, 12, ""), (12, 120, ""), (12, 13, ""), (13, 14, "đồng ý"), (14, 140, ""), (14, 15, ""),
         (15, 150, ""), (15, 16, "")]),
 "luong-test-with-tc": dict(
  title="LUỒNG /test-with-tc — ĐÃ CÓ TESTCASE (kiểm định / regression)",
  sub="Đầu vào: file Excel testcase có sẵn · AI tự xác định module, QC xác nhận · checklist không bắt buộc",
  steps=[
   (1, "qc", 0, "Giao file testcase", ["gõ: /test-with-tc D:\\tc\\kiem_dinh_hss.xlsx", "(+ phạm vi nếu đã biết)"], None, ""),
   (2, "ai", 0, "Nạp testcase", ["xlsx_to_tc.py: tự nhận cột theo tên tiêu đề", "báo: nhận bao nhiêu TC, cột nào nhận / không", "Cột sai → hỏi trắc nghiệm (có Other)"], None, ""),
   (20, "out", 0, "testcases.json", ["bản chuẩn hoá của file Excel gốc", "file Excel gốc KHÔNG bị sửa"], None, ""),
   (3, "ai", 1, *MOD_AI, None, ""),
   (30, "out", 1, *NEW_MOD, None, "warn"),
   (4, "qc", 2, "Xác nhận module", ["○ Đúng module AI nêu  ○ Chọn module khác", "○ Nhiều module  ○ Module mới → tạo folder + skill", "○ Other"], 0, ""),
   (5, "ai", 3, "Hỏi phạm vi + checklist", ["Checklist không bắt buộc (đã có TC)", "Nếu có: báo mục checklist chưa có TC bao phủ"], None, ""),
   (6, "qc", 3, "QC chọn (trắc nghiệm, có Other)", ["Phạm vi: tất cả / theo module / ưu tiên High / ID", "Đối chiếu độ phủ checklist?", "○ QC gửi  ○ AI sinh từ TC + tài liệu  ○ Không cần"], 1, ""),
   (50, "out", 3, "checklist.md (nếu chọn)", ["modules/<module>/checklist.md", "dùng để tìm TC còn thiếu"], None, "warn"),
   (7, "ai", 4, "Chạy test theo nhóm 10–15 TC", ["A: AI chạy playwright-cli / mobile-mcp (QC cho phép)", "B: QC tự test, báo ngắn: TC_001 pass; TC_002 fail: …", "Không sửa TC gốc; TC lỗi thời → danh sách riêng"], None, ""),
   (70, "out", 4, "results.json (+ screenshots/)", ["Pass / Fail / Blocked / Skip + thực tế + bằng chứng", "Danh sách “TC cần cập nhật” (QC quyết sau)"], None, ""),
   (8, "ai", 5, "Soạn bug cho TC Fail", ["Theo templates/bug_template.md", "1 bug = 1 nguyên nhân · soát trùng"], None, ""),
   (80, "out", 5, "bugs.md", ["bản nháp, chưa gửi đi đâu"], None, ""),
   (9, "qc", 6, "QC xác nhận từng bug", ["Giữ / sửa / gộp / bỏ"], 2, ""),
   (10, "ai", 7, "Log bug lên Jira", ["Chỉ SAU khi QC đồng ý", "Jira MCP tạo Bug, link ticket gốc", "Không có MCP: QC dán từ bugs.md"], None, ""),
   (100, "out", 7, "Jira", ["Bug mới, key ghi lại vào results.json"], None, ""),
   (11, "ai", 8, "Báo cáo", ["make_report.py results.json → report.html", "kèm phần “TC cần cập nhật” trong kết luận"], None, ""),
   (110, "out", 8, "report.html", ["Pass/Fail/Blocked · tỉ lệ Pass", "danh sách bug · bảng TC lọc theo trạng thái"], None, ""),
   (12, "qc", 8, "QC đọc kết luận", ["Quyết định release / cập nhật bộ TC / yêu cầu dev sửa"], None, ""),
  ],
  edges=[(1, 2, ""), (2, 20, ""), (2, 3, ""), (3, 30, ""), (3, 4, "hỏi xác nhận"), (4, 5, "QC OK"), (5, 6, "hỏi"), (5, 50, ""),
         (6, 7, "QC chọn"), (7, 70, ""), (7, 8, ""), (8, 80, ""), (8, 9, ""), (9, 10, "đồng ý"), (10, 100, ""),
         (10, 11, ""), (11, 110, ""), (11, 12, "")]),
 "luong-test-system": dict(
  title="LUỒNG /test-system — HỆ THỐNG MỚI, KHÔNG TÀI LIỆU, KHÔNG TESTCASE (vd TSDC)",
  sub="Đầu vào: URL hệ thống + tài khoản · AI tự khảo sát, dựng yêu cầu, đối chiếu module với kit rồi mới sinh testcase",
  steps=[
   (1, "qc", 0, "Giao hệ thống", ["gõ: /test-system https://tsdc… tsdc", "Cung cấp tài khoản theo từng role", "Không có tài khoản/quyền → AI hỏi lại"], None, ""),
   (2, "ai", 0, "Khảo sát bằng trình duyệt thật", ["playwright-cli, desktop 1920×1080", "Đi qua từng menu: màn hình · field · nút · trạng thái", "Không đoán màn hình chưa mở được"], None, ""),
   (20, "out", 0, "evidence/ + “Vùng chưa khảo sát”", ["ảnh từng màn hình / trạng thái", "danh sách chỗ chưa vào được (để QC bổ sung)"], None, ""),
   (3, "ai", 1, "Dựng yêu cầu + checklist theo module", ["Từ những gì thấy trên hệ thống", "Module → REQ-<MODULE>-<số> → rủi ro", "Checklist từng module: AI sinh [Jira]/[AI-giả định]"], None, ""),
   (30, "out", 1, "requirements.md + checklist.md", ["mọi REQ là SUY RA từ khảo sát", "→ cần QC xác nhận đúng nghiệp vụ"], None, "warn"),
   (4, "qc", 2, "QC duyệt, chọn module làm trước", ["Sửa / bỏ / thêm REQ, sửa nghiệp vụ AI hiểu sai", "Chọn module ưu tiên (trắc nghiệm, có Other)"], 0, ""),
   (5, "ai", 3, "Đối chiếu module với kit", ["So từng module khảo sát được với modules/*/", "Có folder → dùng · chưa có → đề xuất tạo mới"], None, ""),
   (50, "out", 3, "modules/<module>/ (mới)", ["tạo từ _template: CLAUDE.md · checklist.md", "+ skill qc-<module> · gắn [cần xác nhận]"], None, "warn"),
   (6, "qc", 4, "QC xác nhận tạo module mới", ["○ Tạo tất cả  ○ Chọn module cần tạo", "○ Không tạo (chỉ chạy lần này)  ○ Other"], 1, ""),
   (7, "ai", 5, "Kế hoạch", ["Bảng ngắn: module · số REQ · ước tính số TC", "Thứ tự: High trước"], None, ""),
   (8, "qc", 5, "QC đồng ý kế hoạch", ["Trắc nghiệm: Đồng ý / Đổi thứ tự / Other"], 2, ""),
   (9, "ai", 6, "Sinh TC song song theo module", ["Mỗi module = 1 subagent, tối đa 4 cùng lúc", "Chỉ nhận REQ + evidence + rule/checklist module đó", "Quality Gate; trả về 1 dòng"], None, ""),
   (90, "out", 6, "modules/<module>/output/<task>/", ["testcases.json → testcases.xlsx (mỗi module 1 file)", "sheet Coverage cảnh báo REQ chưa có TC"], None, ""),
   (10, "ai", 7, "Gộp kết quả", ["Bảng tổng: module · số TC · trạng thái Gate", "Danh sách file .xlsx"], None, ""),
   (11, "qc", 7, "QC review testcase", ["Sửa trong Excel hoặc nhắn AI sửa", "TC dựa trên suy luận → soi kỹ"], 3, ""),
   (12, "ai", 8, "Chạy test · soạn bug", ["QC test hoặc AI chạy (QC cho phép)", "Ghi results.json · soạn bug cho TC Fail"], None, ""),
   (120, "out", 8, "results.json · bugs.md", ["trong modules/<module>/output/<task>/", "1 file cho cả hệ thống hoặc mỗi module 1 file"], None, ""),
   (13, "qc", 9, "QC xác nhận từng bug", ["Giữ / sửa / gộp / bỏ"], 4, ""),
   (14, "ai", 10, "Log Jira + báo cáo", ["Sau khi QC đồng ý: Jira MCP tạo Bug (hoặc QC dán)", "make_report.py → report.html"], None, ""),
   (140, "out", 10, "report.html + Jira", ["báo cáo toàn hệ thống · bug đã log"], None, ""),
   (15, "qc", 10, "QC đọc kết luận", ["Độ phủ theo module, rủi ro còn lại, đề xuất bổ sung TC"], None, ""),
  ],
  edges=[(1, 2, ""), (2, 20, ""), (2, 3, ""), (3, 30, ""), (3, 4, ""), (4, 5, "QC OK"), (5, 50, ""), (5, 6, "hỏi"),
         (6, 7, "QC trả lời"), (7, 8, "hỏi"), (8, 9, "đồng ý"), (9, 90, ""), (9, 10, ""), (10, 11, ""), (11, 12, "QC OK"),
         (12, 120, ""), (12, 13, ""), (13, 14, "đồng ý"), (14, 140, ""), (14, 15, "")]),
}

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#f6f8fb;font-family:'Segoe UI','Be Vietnam Pro',Arial,sans-serif;color:#1f2937;width:2000px}
h1{margin:0;padding:20px 0 2px;text-align:center;font-size:34px;color:#1f2a44}
.sub{text-align:center;color:#556;font-size:19px;margin-bottom:14px}
#wrap{position:relative;margin:0 40px;display:grid;grid-template-columns:1fr 1fr 1fr;column-gap:30px;align-content:start}
.lane{border-radius:18px;border:3px solid;z-index:0}
.lane.qc{background:#fff3df;border-color:#e08a00}
.lane.ai{background:#e8f0fc;border-color:#1f6fcc}
.lane.out{background:#edf6ee;border-color:#2e7d32}
.hd{z-index:1;text-align:center;font-weight:700;font-size:23px;padding:16px 0 6px}
.hd.qc{color:#e08a00}.hd.ai{color:#1f6fcc}.hd.out{color:#2e7d32}
.card{position:relative;z-index:2;margin:16px 26px 22px;background:#fff;border:3px solid;border-radius:12px;padding:16px 18px;text-align:center;align-self:center}
.card.qc{border-color:#e08a00}.card.ai{border-color:#1f6fcc}.card.out{border-color:#2e7d32}.card.warn{background:#fff6dd}
.card b{display:block;font-size:20px;margin-bottom:6px}
.card span{display:block;font-size:16.5px;line-height:1.38}
.stop{position:absolute;right:10px;top:-15px;background:#c62828;color:#fff;border-radius:14px;padding:3px 14px;font-size:16px;font-weight:600}
svg{position:absolute;left:0;top:0;z-index:3;pointer-events:none;overflow:visible}
.foot{text-align:center;color:#556;font-size:16px;padding:14px 0 16px}
"""

JS = """
const L=__DATA__;
const col={qc:'#e08a00',ai:'#444',out:'#2e7d32'};
const w=document.getElementById('wrap'),wr=w.getBoundingClientRect();
const R=id=>{const r=document.getElementById('s'+id).getBoundingClientRect();return {l:r.left-wr.left,r:r.right-wr.left,t:r.top-wr.top,b:r.bottom-wr.top,cx:(r.left+r.right)/2-wr.left,cy:(r.top+r.bottom)/2-wr.top}};
let svg='<defs>'+Object.entries(col).map(([k,c])=>`<marker id="m${k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0L10,5L0,10z" fill="${c}"/></marker>`).join('')+'</defs>';
const lane={};L.steps.forEach(s=>lane[s[0]]=s[1]);
L.edges.forEach(([a,b,lab])=>{
 const A=R(a),B=R(b);
 let c;
 if(lane[b]=='out')c='out'; else if(lane[a]=='qc'||lane[b]=='qc')c='qc'; else c='ai';
 let d,lx,ly;
 if(Math.abs(A.cy-B.cy)<12){const x1=A.cx<B.cx?A.r:A.l,x2=A.cx<B.cx?B.l:B.r;d=`M${x1},${A.cy}L${x2},${B.cy}`;lx=(x1+x2)/2;ly=A.cy-8;}
 else if(Math.abs(A.cx-B.cx)<20){d=`M${A.cx},${A.b}L${B.cx},${B.t}`;lx=A.cx+8;ly=(A.b+B.t)/2;}
 else{const my=(A.b+B.t)/2;d=`M${A.cx},${A.b}L${A.cx},${my}L${B.cx},${my}L${B.cx},${B.t}`;lx=(A.cx+B.cx)/2;ly=my-6;}
 svg+=`<path d="${d}" fill="none" stroke="${col[c]}" stroke-width="3" marker-end="url(#m${c})"/>`;
 if(lab)svg+=`<text x="${lx}" y="${ly}" text-anchor="middle" font-size="15" fill="${col[c]}" stroke="#f6f8fb" stroke-width="4" paint-order="stroke">${lab}</text>`;
});
const S=document.getElementById('svg');S.setAttribute('width',wr.width);S.setAttribute('height',wr.height);S.innerHTML=svg;
document.body.setAttribute('data-h',Math.ceil(document.body.getBoundingClientRect().height)+10);
"""

LANES = [("qc", "QC (bạn)"), ("ai", "AI (Claude Code)"), ("out", "Kết quả / Hệ thống ngoài")]


def build(f):
    e = html.escape
    nrows = max(s[2] for s in f["steps"]) + 1
    parts = [f"<h1>{e(f['title'])}</h1><div class='sub'>{e(f['sub'])}</div><div id='wrap'>"]
    for i, (k, name) in enumerate(LANES):
        parts.append(f"<div class='lane {k}' style='grid-column:{i+1};grid-row:1/span {nrows+1}'></div>"
                     f"<div class='hd {k}' style='grid-column:{i+1};grid-row:1'>{e(name)}</div>")
    col = {"qc": 1, "ai": 2, "out": 3}
    for sid, lane, row, title, lines, stop, style in f["steps"]:
        num = f"{sid}. " if sid < 20 or sid in (50, 90) and False else ""
        if sid >= 20 and sid % 10 == 0:
            num = ""
        elif sid < 20:
            num = f"{sid}. "
        st = f"<div class='stop'>DỪNG {stop}</div>" if stop is not None else ""
        body = "".join(f"<span>{e(x)}</span>" for x in lines)
        parts.append(f"<div class='card {lane} {style}' id='s{sid}' style='grid-column:{col[lane]};grid-row:{row+2}'>{st}<b>{e(num+title)}</b>{body}</div>")
    parts.append("<svg id='svg'></svg></div>")
    parts.append("<div class='foot'>Đỏ = ĐIỂM DỪNG: AI dừng chờ QC · AI không tự chốt TC, không tự log Jira khi QC chưa đồng ý · mọi câu hỏi là trắc nghiệm có Other · rule/checklist/output theo module</div>")
    data = json.dumps({"steps": [[s[0], s[1]] for s in f["steps"]], "edges": f["edges"]}, ensure_ascii=False)
    return ("<!doctype html><html><head><meta charset='utf-8'><style>" + CSS + "</style></head><body>"
            + "".join(parts) + "<script>" + JS.replace("__DATA__", data) + "</script></body></html>")


def run(exe, *a):
    return subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", *a],
                          capture_output=True, text=True, encoding="utf-8", timeout=120)


def main():
    exe = next((b for b in BROWSERS if os.path.exists(b)), None)
    if not exe:
        sys.exit("Không tìm thấy Edge/Chrome")
    tmp = tempfile.mkdtemp()
    for name, f in FLOWS.items():
        p = os.path.join(tmp, name + ".html")
        open(p, "w", encoding="utf-8").write(build(f))
        url = "file:///" + p.replace("\\", "/")
        dom = run(exe, "--window-size=2000,3000", "--dump-dom", url).stdout
        h = int(re.search(r'data-h="(\d+)"', dom).group(1))
        out = os.path.join(ROOT, name + ".png")
        run(exe, f"--window-size=2000,{h}", f"--screenshot={out}", url)
        print(name, h, os.path.exists(out))


if __name__ == "__main__":
    main()
