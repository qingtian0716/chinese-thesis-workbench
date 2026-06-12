from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path


def load_compute_text_metrics():
    module_path = Path(__file__).resolve().parents[1] / "docx" / "markdown_utils.py"
    spec = importlib.util.spec_from_file_location("markdown_utils", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load markdown utilities: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compute_text_metrics


compute_text_metrics = load_compute_text_metrics()


CHAPTER_RE = re.compile(r"^##\s+(.+)$", flags=re.M)
SECTION_RE = re.compile(r"^###\s+(.+)$", flags=re.M)


def chapter_spans(text: str) -> list[tuple[str, int, int]]:
    matches = list(CHAPTER_RE.finditer(text))
    spans: list[tuple[str, int, int]] = []

    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        spans.append((match.group(1).strip(), start, end))

    return spans


def section_spans(text: str, chapter_start: int, chapter_end: int) -> list[tuple[str, int, int]]:
    """Extract sections within a chapter"""
    chapter_text = text[chapter_start:chapter_end]
    matches = list(SECTION_RE.finditer(chapter_text))
    spans: list[tuple[str, int, int]] = []

    for index, match in enumerate(matches):
        start = chapter_start + match.end()
        end = chapter_start + matches[index + 1].start() if index + 1 < len(matches) else chapter_end
        spans.append((match.group(1).strip(), start, end))

    return spans


def load_section_budgets(budget_path: Path) -> dict[str, int]:
    """Load section budgets from section-word-budget.md"""
    if not budget_path.exists():
        return {}

    budgets = {}
    text = budget_path.read_text(encoding="utf-8")
    current_chapter = ""

    for line in text.splitlines():
        line = line.strip()
        # Match chapter headers: ## 第X章 标题
        chapter_match = re.match(r"^##\s+(.+)$", line)
        if chapter_match:
            current_chapter = chapter_match.group(1).strip()
            continue

        # Match section entries: - 节名称: XXXX字
        section_match = re.match(r"^-\s+(.+?):\s*(\d+)\s*字", line)
        if section_match and current_chapter:
            section_name = section_match.group(1).strip()
            budget = int(section_match.group(2))
            # Use chapter + section as key
            key = f"{current_chapter}/{section_name}"
            budgets[key] = budget

    return budgets


def format_metrics(label: str, metrics: dict[str, int]) -> str:
    return (
        f"{label}\t"
        f"APPROX_WORDS={metrics['approx_word_count']}\t"
        f"CHAR_NO_SPACES={metrics['char_no_spaces']}\t"
        f"CHAR_WITH_SPACES={metrics['char_with_spaces']}\t"
        f"CJK_CHARS={metrics['chinese_chars']}\t"
        f"NON_CJK_WORDS={metrics['non_chinese_words']}\t"
        f"EN_WORDS={metrics['english_words']}"
    )


def budget_line(total_metrics: dict, budget: int) -> str:
    used = total_metrics["approx_word_count"]
    remaining = budget - used
    status = "OK" if remaining >= 0 else "OVER"
    return f"WORD_BUDGET\tTARGET={budget}\tUSED={used}\tREMAINING={remaining}\tSTATUS={status}"


def section_budget_line(section_name: str, section_metrics: dict, budget: int) -> str:
    used = section_metrics["approx_word_count"]
    remaining = budget - used
    status = "OK" if remaining >= 0 else "OVER"
    return f"SECTION_BUDGET\t{section_name}\tTARGET={budget}\tUSED={used}\tREMAINING={remaining}\tSTATUS={status}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Count chapter words in a Markdown thesis file.")
    parser.add_argument("file", type=str, help="Path to the Markdown file")
    parser.add_argument("--budget", type=int, default=None, help="Total word budget; prints a WORD_BUDGET summary line")
    parser.add_argument("--section-budget", type=str, default=None,
                        help="Path to section-word-budget.md for per-section budget checking")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()

    path = Path(args.file)
    text = path.read_text(encoding="utf-8")
    total = compute_text_metrics(text)

    # Load section budgets if provided
    section_budgets = {}
    if args.section_budget:
        section_budgets = load_section_budgets(Path(args.section_budget))

    # Collect results
    results = {
        "total": total,
        "chapters": [],
        "sections": [],
    }

    print(format_metrics("TOTAL", total))

    if args.budget is not None:
        print(budget_line(total, args.budget))

    for chapter_title, chapter_start, chapter_end in chapter_spans(text):
        chapter_metrics = compute_text_metrics(text[chapter_start:chapter_end])
        print(format_metrics(chapter_title, chapter_metrics))

        # Check chapter budget if provided
        if args.budget:
            # Chapter budget is proportional to total
            pass

        # Check section budgets if provided
        if section_budgets:
            for section_title, section_start, section_end in section_spans(text, chapter_start, chapter_end):
                section_metrics = compute_text_metrics(text[section_start:section_end])
                section_key = f"{chapter_title}/{section_title}"

                if section_key in section_budgets:
                    budget = section_budgets[section_key]
                    print(section_budget_line(section_title, section_metrics, budget))
                    results["sections"].append({
                        "chapter": chapter_title,
                        "section": section_title,
                        "metrics": section_metrics,
                        "budget": budget,
                        "status": "OK" if section_metrics["approx_word_count"] <= budget else "OVER",
                    })
                else:
                    print(format_metrics(f"  {section_title}", section_metrics))

    # JSON output
    if args.json:
        json_path = path.with_suffix(".word-count.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✅ JSON 统计已保存: {json_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
