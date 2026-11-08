#!/usr/bin/env python3
"""File Excel testcase có sẵn -> testcases.json (để dùng cho /test-with-tc).

Dùng:  python scripts/xlsx_to_tc.py <file.xlsx> [output.json] [--sheet TÊN]
Tự nhận cột theo tên tiêu đề (không phân biệt hoa thường/dấu). Cột lạ bị bỏ qua.
Cần: pip install openpyxl
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from openpyxl import load_workbook

ALIASES = {
    "tc_id": ["tc id", "id", "ma tc", "testcase id", "test case id", "tc"],
    "req_id": ["req id", "requirement", "ma yeu cau"],
    "module": ["module", "chuc nang", "man hinh"],
    "type": ["loai", "type"],
    "risk": ["rui ro", "risk", "risk level"],
    "title": ["tieu de", "title", "test title", "ten testcase", "test case", "muc dich"],
    "precondition": ["dieu kien tien quyet", "pre-condition", "precondition", "tien dieu kien"],
    "steps": ["cac buoc", "test steps", "steps", "buoc thuc hien"],
    "expected": ["ket qua mong doi", "expected result", "expected", "ket qua du kien"],
    "test_data": ["du lieu test", "test data", "du lieu"],
    "priority": ["uu tien", "priority", "do uu tien"],
    "result": ["ket qua", "result", "status", "trang thai"],
    "bug_id": ["bug id", "bug"],
    "note": ["ghi chu", "note", "notes"],
}


def norm(s):
    s = unicodedata.normalize("NFD", str(s or "").lower().replace("đ", "d"))
    return re.sub(r"\s+", " ", "".join(c for c in s if unicodedata.category(c) != "Mn")).strip()


def split_steps(text):
    parts = [re.sub(r"^\s*\d+[\.\)]\s*", "", p).strip() for p in str(text).splitlines() if p.strip()]
    return parts or [str(text)]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sheet = None
    if "--sheet" in sys.argv:
        sheet = sys.argv[sys.argv.index("--sheet") + 1]
        args = [a for a in args if a != sheet]
    if not args:
        sys.exit(__doc__)
    src = Path(args[0])
    out = Path(args[1]) if len(args) > 1 else src.with_suffix(".json")
    wb = load_workbook(src, data_only=True)
    ws = wb[sheet] if sheet else wb.worksheets[0]

    rows = list(ws.iter_rows(values_only=True))
    # tìm dòng tiêu đề: dòng đầu có >= 3 cột khớp alias
    colmap, hdr_idx = {}, 0
    for i, row in enumerate(rows[:15]):
        m = {}
        for j, cell in enumerate(row):
            n = norm(cell)
            for key, names in ALIASES.items():
                if n in names and key not in m.values():
                    m[j] = key
        if len(m) >= 3:
            colmap, hdr_idx = m, i
            break
    if not colmap:
        sys.exit("Không nhận ra dòng tiêu đề. Kiểm tra tên cột hoặc dùng --sheet.")

    tcs = []
    for row in rows[hdr_idx + 1:]:
        tc = {key: row[j] for j, key in colmap.items() if j < len(row) and row[j] is not None}
        if not tc.get("tc_id") and not tc.get("title"):
            continue
        for k in ("steps", "expected"):
            if k in tc:
                tc[k] = split_steps(tc[k])
        tcs.append({k: (str(v) if not isinstance(v, list) else v) for k, v in tc.items()})

    out.write_text(json.dumps({"testcases": tcs, "requirements": []}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {out}  ({len(tcs)} TC, sheet '{ws.title}', cột nhận được: {sorted(set(colmap.values()))})")


if __name__ == "__main__":
    main()
