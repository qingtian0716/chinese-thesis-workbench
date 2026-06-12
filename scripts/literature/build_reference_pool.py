from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


REF_RE = re.compile(r"^\[(\d+)\]\s*(.+)$")


def classify_language(text: str) -> str:
    return "zh" if re.search(r"[\u4e00-\u9fff]", text) else "en"


def extract_year(text: str) -> int | None:
    years = re.findall(r"\b(20\d{2})\b", text)
    return int(years[0]) if years else None


def parse_references(path: Path) -> list[dict]:
    refs = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        m = REF_RE.match(line)
        if not m:
            continue
        body = m.group(2).strip()
        refs.append(
            {
                "raw": line,
                "index": int(m.group(1)),
                "language": classify_language(body),
                "year": extract_year(body),
                "has_doi": "doi" in body.lower(),
            }
        )
    return refs


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python build_reference_pool.py <reference-markdown-file>")
        return 1

    path = Path(sys.argv[1])
    refs = parse_references(path)
    lang_counts = Counter(ref["language"] for ref in refs)

    # \u8ba1\u7b97\u8fd1\u4e94\u5e74\u6587\u732e\u5360\u6bd4
    current_year = datetime.now().year
    recent_threshold = current_year - 5  # \u4f8b\u5982 2026 - 5 = 2021
    recent_refs = [ref for ref in refs if ref["year"] is not None and ref["year"] >= recent_threshold]
    recent_ratio = len(recent_refs) / len(refs) * 100 if refs else 0

    # \u5b66\u6821\u8981\u6c42\uff1a\u8fd1\u4e94\u5e74\u4e0d\u5c11\u4e8e 60%
    school_requirement = 60
    meets_requirement = recent_ratio >= school_requirement

    print(f"TOTAL\t{len(refs)}")
    print(f"ZH\t{lang_counts.get('zh', 0)}")
    print(f"EN\t{lang_counts.get('en', 0)}")
    print(f"RECENT_THRESHOLD\t{recent_threshold}")
    print(f"RECENT_COUNT\t{len(recent_refs)}")
    print(f"RECENT_RATIO\t{recent_ratio:.1f}%")
    print(f"SCHOOL_REQUIREMENT\t{school_requirement}%")
    print(f"MEETS_REQUIREMENT\t{'YES' if meets_requirement else 'NO'}")

    # \u8f93\u51fa\u8be6\u7ec6\u7edf\u8ba1
    if not meets_requirement:
        print(f"\n\u26a0\ufe0f \u8fd1\u4e94\u5e74\u6587\u732e\u5360\u6bd4 {recent_ratio:.1f}%\uff0c\u672a\u8fbe\u5230\u5b66\u6821\u8981\u6c42\u7684 {school_requirement}%")
        print(f"\u5efa\u8bae\u8865\u5145 {school_requirement - recent_ratio:.1f}% \u7684\u8fd1\u4e94\u5e74\u6587\u732e")

    # \u5217\u51fa\u6240\u6709\u6587\u732e\u7684\u5e74\u4efd\u5206\u5e03\uff08\u4f9b\u53c2\u8003\uff09
    year_distribution = Counter(ref["year"] for ref in refs)
    print(f"\n\u5e74\u4efd\u5206\u5e03:")
    for year in sorted(year_distribution.keys(), reverse=True):
        if year is not None:
            print(f"  {year}: {year_distribution[year]} \u7bc7")
    print(f"  \u65e0\u5e74\u4efd: {year_distribution.get(None, 0)} \u7bc7")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
