from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create reference verification checklist from extracted references."
    )
    parser.add_argument(
        "target_json",
        type=Path,
        help="Output JSON file path for verification checklist"
    )
    parser.add_argument(
        "--input", "-i",
        type=Path,
        help="Input JSON file from extract_pdf_references.py (reference-extraction.json)"
    )
    parser.add_argument(
        "--default-status",
        choices=["needs_check", "verified", "rejected"],
        default="needs_check",
        help="Default status for references (default: needs_check)"
    )
    return parser.parse_args()


def load_extracted_references(input_path: Path) -> List[Dict]:
    """Load references from extract_pdf_references.py output"""
    if not input_path.exists():
        print(f"警告：输入文件不存在 - {input_path}")
        return []

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 处理不同的 JSON 格式
    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and "references" in data:
        return data["references"]
    elif isinstance(data, dict) and "refs" in data:
        return data["refs"]
    else:
        print(f"警告：无法识别的 JSON 格式 - {input_path}")
        return []


def convert_to_verification_format(ref: Dict, default_status: str) -> Dict:
    """Convert extracted reference to verification format"""
    # 提取基本信息
    title = ref.get("title", ref.get("raw", ""))
    authors = ref.get("authors", [])
    year = ref.get("year", "")
    source = ref.get("source", ref.get("journal", ref.get("conference", "")))
    doi_or_url = ref.get("doi", ref.get("url", ""))
    citation_count = ref.get("citation_count", "")
    relevance_note = ref.get("relevance_note", "")

    # 如果 authors 是字符串，转换为列表
    if isinstance(authors, str):
        authors = [authors]

    return {
        "title": title,
        "authors": authors,
        "year": str(year) if year else "",
        "source": source,
        "doi_or_url": doi_or_url,
        "citation_count_if_available": str(citation_count) if citation_count else "",
        "relevance_note": relevance_note,
        "status": default_status,
        "original_index": ref.get("index", ""),
        "language": ref.get("language", ""),
        "has_doi": ref.get("has_doi", False),
    }


def main() -> int:
    args = parse_args()
    args.target_json.parent.mkdir(parents=True, exist_ok=True)

    # 如果提供了输入文件，从已提取的文献生成
    if args.input and args.input.exists():
        extracted_refs = load_extracted_references(args.input)
        verification_refs = [
            convert_to_verification_format(ref, args.default_status)
            for ref in extracted_refs
        ]
        print(f"✅ 从 {args.input} 加载了 {len(verification_refs)} 条文献")
    else:
        # 如果没有输入文件，生成空模板
        if args.input:
            print(f"⚠️ 输入文件 {args.input} 不存在，生成空模板")
        verification_refs = [
            {
                "title": "",
                "authors": [],
                "year": "",
                "source": "",
                "doi_or_url": "",
                "citation_count_if_available": "",
                "relevance_note": "",
                "status": args.default_status,
                "original_index": "",
                "language": "",
                "has_doi": False,
            }
        ]
        print("⚠️ 生成了空模板，请手动填入文献信息")

    template = {
        "metadata": {
            "generated_from": str(args.input) if args.input else "manual",
            "total_references": len(verification_refs),
            "default_status": args.default_status,
            "status_options": {
                "needs_check": "待核验",
                "verified": "已验证",
                "rejected": "已拒绝",
            }
        },
        "references": verification_refs,
    }

    args.target_json.write_text(
        json.dumps(template, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"✅ 核验清单已生成: {args.target_json}")
    print(f"   文献总数: {len(verification_refs)}")
    print(f"   默认状态: {args.default_status}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
