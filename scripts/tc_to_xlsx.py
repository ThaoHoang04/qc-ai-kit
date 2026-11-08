#!/usr/bin/env python3
"""testcases.json -> testcases.xlsx (sheet 'Testcase' + sheet 'Coverage').

Dùng:  python scripts/tc_to_xlsx.py output/<task>/testcases.json
Kết quả: file .xlsx cùng thư mục. Cần: pip install openpyxl
"""
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule

COLUMNS = [
    ("TC ID", "tc_id", 16),
    ("REQ ID", "req_id", 14),
    ("Module", "module", 16),
    ("Loại", "type", 11),
    ("Rủi ro", "risk", 9),
    ("Tiêu đề", "title", 38),
    ("Điều kiện tiên quyết", "precondition", 30),
    ("Các bước", "steps", 48),
    ("Kết quả mong đợi", "expected", 48),
    ("Dữ liệu test", "test_data", 30),
    ("Ưu tiên", "priority", 9),
    ("Kết quả", "result", 11),
    ("Bug ID", "bug_id", 12),
    ("Ghi chú", "note", 24),
]
THIN = Side(style="thin", color="BBBBBB")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def numbered(value):
    """List -> '1. a\n2. b'. Chuỗi giữ nguyên."""
    if isinstance(value, list):
        return "\n".join(f"{i}. {s}" for i, s in enumerate(value, 1))
    return value or ""


def header(ws, titles, row=1):
    for c, t in enumerate(titles, 1):
        cell = ws.cell(row=row, column=c, value=t)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F4E78")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER


def main(path):
    src = Path(path)
    data = json.loads(src.read_text(encoding="utf-8"))
    tcs = data["testcases"]
    reqs = data.get("requirements", [])

    wb = Workbook()
    ws = wb.active
    ws.title = "Testcase"
    header(ws, [c[0] for c in COLUMNS])
    for r, tc in enumerate(tcs, 2):
        for c, (_, key, _) in enumerate(COLUMNS, 1):
            val = tc.get(key, "")
            if key in ("steps", "expected"):
                val = numbered(val)
            if key == "result" and not val:
                val = "Chưa test"
            cell = ws.cell(row=r, column=c, value=val)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = BORDER
    for c, (_, _, w) in enumerate(COLUMNS, 1):
        ws.column_dimensions[ws.cell(row=1, column=c).column_letter].width = w
    ws.row_dimensions[1].height = 28
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = ws.dimensions

    # Cột Kết quả: dropdown + tô màu
    rcol = [k for _, k, _ in COLUMNS].index("result") + 1
    letter = ws.cell(row=1, column=rcol).column_letter
    rng = f"{letter}2:{letter}{max(len(tcs) + 1, 2)}"
    dv = DataValidation(type="list", formula1='"Chưa test,Pass,Fail,Blocked,Skip"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(rng)
    for text, color in (("Pass", "C6EFCE"), ("Fail", "FFC7CE"), ("Blocked", "FFEB9C")):
        ws.conditional_formatting.add(
            rng, CellIsRule(operator="equal", formula=[f'"{text}"'], fill=PatternFill("solid", bgColor=color))
        )

    # Sheet Coverage
    cv = wb.create_sheet("Coverage")
    header(cv, ["REQ ID", "Mô tả", "Số TC", "TC IDs", "Positive", "Negative", "Boundary", "Đánh giá"])
    row = 2
    for rq in reqs:
        mine = [t for t in tcs if t.get("req_id") == rq["id"]]
        kinds = {t.get("type", "") for t in mine}
        pos, neg, bnd = ("Positive" in kinds, "Negative" in kinds, "Boundary" in kinds)
        status = "THIẾU - cần bổ sung" if not mine else ("OK" if pos and neg else "Thiếu Positive/Negative")
        vals = [rq["id"], rq.get("desc", ""), len(mine), ", ".join(t["tc_id"] for t in mine),
                "x" if pos else "", "x" if neg else "", "x" if bnd else "", status]
        for c, v in enumerate(vals, 1):
            cell = cv.cell(row=row, column=c, value=v)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = BORDER
            if c == 8 and status != "OK":
                cell.fill = PatternFill("solid", fgColor="FFC7CE")
        row += 1
    for letter, w in zip("ABCDEFGH", (14, 40, 8, 50, 10, 10, 10, 24)):
        cv.column_dimensions[letter].width = w
    cv.freeze_panes = "A2"

    out = src.with_suffix(".xlsx")
    wb.save(out)
    missing = [r["id"] for r in reqs if not any(t.get("req_id") == r["id"] for t in tcs)]
    print(f"OK: {out}  ({len(tcs)} TC, {len(reqs)} REQ)")
    if missing:
        print("CANH BAO - REQ chua co TC:", ", ".join(missing))
        return 2
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
