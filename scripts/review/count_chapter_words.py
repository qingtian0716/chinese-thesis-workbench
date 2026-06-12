from __future__ import annotations

import argparse
import importlib.util
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


def chapter_spans(text: str) -> list[tuple[str, int, int]]:
    matches = list(CHAPTER_RE.finditer(text))
    spans: list[tuple[str, int, int]] = []

    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        spans.append((match.group(1).strip(), start, end))

    return spans


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Count chapter words in a Markdown thesis file.")
    parser.add_argument("file", type=str, help="Path to the Markdown file")
    parser.add_argument("--budget", type=int, default=None, help="Total word budget; prints a WORD_BUDGET summary line")
    args = parser.parse_args()

    path = Path(args.file)
    text = path.read_text(encoding="utf-8")
    total = compute_text_metrics(text)
    print(format_metrics("TOTAL", total))

    if args.budget is not None:
        print(budget_line(total, args.budget))

    for title, start, end in chapter_spans(text):
        print(format_metrics(title, compute_text_metrics(text[start:end])))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
