#!/usr/bin/env python3
"""results.json -> report.html (1 file, mở bằng trình duyệt, có lọc theo trạng thái).

Dùng:  python scripts/make_report.py output/<task>/results.json
Kết quả: report.html + bugs.md cùng thư mục.
"""
import base64
import html
import json
import mimetypes
import sys
from collections import Counter
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

STATUS_CLASS = {"Pass": "pass", "Fail": "fail", "Blocked": "blocked", "Skip": "skip"}


def esc(v):
    return html.escape(str(v if v is not None else "")).replace("\n", "<br>")


def lst(v):
    if isinstance(v, list):
        return "\n".join(f"{i}. {s}" for i, s in enumerate(v, 1))
    return v or ""


def evid_list(v):
    if not v:
        return []
    return v if isinstance(v, list) else [x.strip() for x in str(v).replace(";", ",").split(",") if x.strip()]


def imgs(v, base, missing):
    """Nhúng ảnh thẳng vào HTML (base64) -> mở report ở đâu cũng thấy, không phụ thuộc đường dẫn."""
    out = []
    for ev in evid_list(v):
        f = Path(ev)
        if not f.is_absolute():
            f = base / ev
        if not f.is_file():
            missing.append(ev)
            out.append(f'<span class="miss">⚠ thiếu ảnh: {esc(ev)}</span>')
            continue
        mime = mimetypes.guess_type(f.name)[0] or "image/png"
        uri = f"data:{mime};base64,{base64.b64encode(f.read_bytes()).decode()}"
        out.append(f'<a href="{uri}" target="_blank"><img src="{uri}" alt="{esc(f.name)}" title="{esc(f.name)}"></a>')
    return f'<div class="evi">{"".join(out)}</div>' if out else ""


def main(path):
    src = Path(path)
    d = json.loads(src.read_text(encoding="utf-8"))
    results, bugs = d.get("results", []), d.get("bugs", [])
    base, missing = src.parent, []
    count = Counter(r.get("status", "Skip") for r in results)
    total = len(results) or 1
    done = count["Pass"] + count["Fail"]
    pass_rate = round(100 * count["Pass"] / done, 1) if done else 0

    cards = "".join(
        f'<div class="card {STATUS_CLASS[s]}"><b>{count[s]}</b><span>{s}</span></div>'
        for s in ("Pass", "Fail", "Blocked", "Skip")
    )
    rows = "".join(
        f'<tr data-s="{esc(r.get("status"))}"><td>{esc(r.get("tc_id"))}</td><td>{esc(r.get("title"))}</td>'
        f'<td><span class="tag {STATUS_CLASS.get(r.get("status"), "skip")}">{esc(r.get("status"))}</span></td>'
        f'<td>{esc(r.get("actual"))}{imgs(r.get("evidence"), base, missing)}</td><td>{esc(r.get("bug_id"))}</td></tr>'
        for r in results
    )
    bug_html = "".join(
        f'<details class="bug" open><summary><b>{esc(b.get("id"))}</b> · [{esc(b.get("severity"))}] {esc(b.get("title"))}'
        f' <small>(TC: {esc(b.get("tc_id"))} · Jira: {esc(b.get("jira") or "chưa log")})</small></summary>'
        f'<p><b>Các bước tái hiện:</b><br>{esc(lst(b.get("steps")))}</p>'
        f'<p><b>Kết quả mong đợi:</b> {esc(b.get("expected"))}</p>'
        f'<p><b>Kết quả thực tế:</b> {esc(b.get("actual"))}</p>'
        f'<p><b>Môi trường:</b> {esc(b.get("env") or d.get("env"))} · <b>Bằng chứng:</b> {esc(", ".join(evid_list(b.get("evidence"))))}</p>{imgs(b.get("evidence"), base, missing)}</details>'
        for b in bugs
    ) or "<p>Không có bug.</p>"

    page = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Báo cáo test - {esc(d.get("title"))}</title>
<style>
body{{font-family:Segoe UI,Arial,sans-serif;margin:0;background:#f4f6f8;color:#222}}
main{{max-width:1100px;margin:0 auto;padding:20px 16px}}
h1{{margin:0 0 4px}} .meta{{color:#555;margin-bottom:16px}}
.cards{{display:flex;gap:12px;flex-wrap:wrap;margin:16px 0}}
.card{{flex:1;min-width:110px;padding:14px;border-radius:8px;background:#fff;border-left:6px solid #999;display:flex;flex-direction:column}}
.card b{{font-size:28px}} .pass{{border-color:#2e7d32}} .fail{{border-color:#c62828}} .blocked{{border-color:#ef6c00}} .skip{{border-color:#9e9e9e}}
.bar{{height:14px;background:#e0e0e0;border-radius:7px;overflow:hidden;display:flex}}
.bar i{{display:block;height:100%}}
.filters button{{margin:0 6px 8px 0;padding:6px 12px;border:1px solid #bbb;background:#fff;border-radius:16px;cursor:pointer}}
.filters button.on{{background:#1f4e78;color:#fff;border-color:#1f4e78}}
table{{width:100%;border-collapse:collapse;background:#fff}} th,td{{border:1px solid #ddd;padding:7px 9px;text-align:left;vertical-align:top;font-size:14px}}
th{{background:#1f4e78;color:#fff}}
.tag{{padding:2px 8px;border-radius:10px;color:#fff;font-size:12px}}
.tag.pass{{background:#2e7d32}} .tag.fail{{background:#c62828}} .tag.blocked{{background:#ef6c00}} .tag.skip{{background:#9e9e9e}}
.bug{{background:#fff;border:1px solid #ddd;border-left:5px solid #c62828;border-radius:6px;padding:8px 12px;margin:8px 0}}
.evi{{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}} .evi img{{max-width:240px;max-height:160px;border:1px solid #ccc;border-radius:4px;cursor:zoom-in}}
.miss{{color:#c62828;font-size:12px}}
.bug summary{{cursor:pointer}} h2{{margin-top:28px}}
@media(max-width:600px){{th:nth-child(4),td:nth-child(4){{display:none}}}}
</style></head><body><main>
<h1>Báo cáo test: {esc(d.get("title"))}</h1>
<div class="meta">Tester: {esc(d.get("tester"))} · Ngày: {esc(d.get("date"))} · Môi trường: {esc(d.get("env"))} · Ticket: {esc(d.get("ticket"))}</div>
<div class="cards">{cards}<div class="card"><b>{pass_rate}%</b><span>Tỉ lệ Pass (trên TC đã chạy)</span></div></div>
<div class="bar">{"".join(f'<i style="width:{100*count[s]/total}%;background:{c}"></i>' for s, c in (("Pass","#2e7d32"),("Fail","#c62828"),("Blocked","#ef6c00"),("Skip","#9e9e9e")))}</div>
<p><b>Kết luận:</b> {esc(d.get("conclusion") or "")}</p>
<h2>Bug ({len(bugs)})</h2>{bug_html}
<h2>Chi tiết testcase ({len(results)})</h2>
<div class="filters"><button class="on" data-f="">Tất cả</button><button data-f="Fail">Fail</button><button data-f="Blocked">Blocked</button><button data-f="Pass">Pass</button><button data-f="Skip">Skip</button></div>
<table><thead><tr><th>TC ID</th><th>Tiêu đề</th><th>Kết quả</th><th>Thực tế / ghi chú</th><th>Bug</th></tr></thead><tbody id="rows">{rows}</tbody></table>
</main><script>
document.querySelectorAll('.filters button').forEach(b=>b.onclick=()=>{{
 document.querySelectorAll('.filters button').forEach(x=>x.classList.remove('on'));b.classList.add('on');
 document.querySelectorAll('#rows tr').forEach(r=>r.style.display=(!b.dataset.f||r.dataset.s===b.dataset.f)?'':'none');}});
</script></body></html>"""
    out = src.with_name("report.html")
    out.write_text(page, encoding="utf-8")

    md = ["# Danh sách bug (copy dán Jira)\n"]
    for b in bugs:
        md.append(f"## {b.get('id')} — {b.get('title')}\n- Severity: {b.get('severity')}\n- TC: {b.get('tc_id')}\n"
                  f"- Môi trường: {b.get('env') or d.get('env')}\n\n**Các bước:**\n{lst(b.get('steps'))}\n\n"
                  f"**Mong đợi:** {b.get('expected')}\n\n**Thực tế:** {b.get('actual')}\n\n**Bằng chứng:** {b.get('evidence')}\n")
    src.with_name("bugs.md").write_text("\n".join(md), encoding="utf-8")
    if missing:
        print(f"CẢNH BÁO: {len(missing)} ảnh không tìm thấy (đường dẫn tính từ thư mục chứa results.json): {missing}")
    print(f"OK: {out}  | Pass {count['Pass']} · Fail {count['Fail']} · Blocked {count['Blocked']} · Skip {count['Skip']} · {len(bugs)} bug")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
