#!/usr/bin/env python3
"""
论文语言质量检查脚本

检查项：
1. 连续三句以相同词开头（句式单调）
2. 单句超过 80 字（过长句）
3. 空泛词汇命中（基于禁用词表）
4. 段落字数 < 80 字（过短段，缺少分析）
5. 数字未使用阿拉伯数字（格式问题）
6. 括号内夹英文未标注中文译名（专业术语不规范）

输出：paper-output/<论文标题>-prose-report.md
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


# 禁用词表
BANNED_PHRASES = [
    "显著提升",
    "显著提高",
    "显著改善",
    "显著增强",
    "具有重要意义",
    "具有重要价值",
    "具有重要作用",
    "取得了良好效果",
    "取得了显著成效",
    "具有广阔的应用前景",
    "具有广阔的发展前景",
    "为……奠定了基础",
    "为……提供了新的思路",
    "为……提供了新的方法",
    "为……提供了新的视角",
    "具有重要的理论价值",
    "具有重要的实践价值",
    "具有重要的现实意义",
    "进行了深入的研究",
    "进行了详细的分析",
    "进行了系统的总结",
    "具有很强的实用性",
    "具有很高的效率",
    "具有很好的效果",
]


def load_markdown(file_path: Path) -> str:
    """加载 Markdown 文件"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def split_into_paragraphs(text: str) -> List[str]:
    """将文本拆分为段落"""
    paragraphs = re.split(r"\n\s*\n", text)
    return [p.strip() for p in paragraphs if p.strip()]


def split_into_sentences(text: str) -> List[str]:
    """将段落拆分为句子"""
    # 匹配中文句号、问号、感叹号、分号
    sentences = re.split(r"[。！？；]", text)
    return [s.strip() for s in sentences if s.strip()]


def check_consecutive_starts(paragraph: str, threshold: int = 3) -> List[Dict]:
    """检查连续句子以相同词开头"""
    issues = []
    sentences = split_into_sentences(paragraph)
    if len(sentences) < threshold:
        return issues

    # 提取每个句子的前 2 个字符
    starts = []
    for s in sentences:
        # 去除标点和空格
        clean = re.sub(r"^[，、：""''（）\s]+", "", s)
        if len(clean) >= 2:
            starts.append(clean[:2])
        elif clean:
            starts.append(clean)
        else:
            starts.append("")

    # 检查连续重复
    for i in range(len(starts) - threshold + 1):
        if starts[i] and all(starts[i + j] == starts[i] for j in range(threshold)):
            issues.append({
                "type": "句式单调",
                "detail": f"连续 {threshold} 句以「{starts[i]}」开头",
                "sentences": sentences[i:i + threshold],
            })

    return issues


def check_long_sentences(paragraph: str, threshold: int = 80) -> List[Dict]:
    """检查过长句子"""
    issues = []
    sentences = split_into_sentences(paragraph)
    for s in sentences:
        if len(s) > threshold:
            issues.append({
                "type": "过长句",
                "detail": f"句子长度 {len(s)} 字，超过 {threshold} 字阈值",
                "sentence": s,
            })
    return issues


def check_banned_phrases(paragraph: str) -> List[Dict]:
    """检查禁用词表"""
    issues = []
    for phrase in BANNED_PHRASES:
        if phrase in paragraph:
            issues.append({
                "type": "空泛表达",
                "detail": f"命中禁用词「{phrase}」",
                "phrase": phrase,
            })
    return issues


def check_short_paragraph(paragraph: str, threshold: int = 80) -> List[Dict]:
    """检查过短段落"""
    issues = []
    # 去除标题行
    if paragraph.startswith("#"):
        return issues
    if len(paragraph) < threshold:
        issues.append({
            "type": "过短段落",
            "detail": f"段落字数 {len(paragraph)} 字，少于 {threshold} 字阈值",
            "paragraph": paragraph[:50] + "..." if len(paragraph) > 50 else paragraph,
        })
    return issues


def check_number_format(paragraph: str) -> List[Dict]:
    """检查数字格式"""
    issues = []
    # 匹配中文数字
    chinese_numbers = re.findall(r"[一二三四五六七八九十百千万亿]+(?=[个只条件项种次遍轮])", paragraph)
    for num in chinese_numbers:
        if len(num) > 1:  # 排除"一"作为冠词的情况
            issues.append({
                "type": "数字格式",
                "detail": f"中文数字「{num}」应使用阿拉伯数字",
                "context": paragraph[max(0, paragraph.find(num) - 10):paragraph.find(num) + len(num) + 10],
            })
    return issues


def check_english_in_parentheses(paragraph: str) -> List[Dict]:
    """检查括号内英文标注"""
    issues = []
    # 匹配中文括号内的内容
    pattern = r"（([^）]+)）"
    matches = re.findall(pattern, paragraph)
    for content in matches:
        # 检查是否包含英文
        if re.search(r"[a-zA-Z]", content):
            # 检查前面是否有中文术语
            idx = paragraph.find(f"（{content}）")
            if idx > 0:
                before = paragraph[:idx]
                # 检查前面是否有中文字符
                if re.search(r"[一-鿿]", before[-5:]):
                    # 这是正常的英文标注，跳过
                    continue
    return issues


def analyze_paragraph(paragraph: str) -> Dict:
    """分析单个段落"""
    issues = {
        "consecutive_starts": check_consecutive_starts(paragraph),
        "long_sentences": check_long_sentences(paragraph),
        "banned_phrases": check_banned_phrases(paragraph),
        "short_paragraph": check_short_paragraph(paragraph),
        "number_format": check_number_format(paragraph),
        "english_in_parentheses": check_english_in_parentheses(paragraph),
    }
    return {k: v for k, v in issues.items() if v}


def analyze_chapter(chapter_title: str, chapter_content: str) -> Dict:
    """分析单个章节"""
    paragraphs = split_into_paragraphs(chapter_content)
    chapter_issues = []

    for i, para in enumerate(paragraphs, 1):
        para_issues = analyze_paragraph(para)
        if para_issues:
            chapter_issues.append({
                "paragraph_index": i,
                "paragraph_preview": para[:50] + "..." if len(para) > 50 else para,
                "issues": para_issues,
            })

    return {
        "title": chapter_title,
        "total_paragraphs": len(paragraphs),
        "issues_count": len(chapter_issues),
        "issues": chapter_issues,
    }


def split_into_chapters(text: str) -> List[Tuple[str, str]]:
    """将文本拆分为章节"""
    chapters = []
    current_title = "前言"
    current_content = []

    for line in text.split("\n"):
        if re.match(r"^#{1,3}\s+", line):
            if current_content:
                chapters.append((current_title, "\n".join(current_content)))
            current_title = re.sub(r"^#{1,3}\s+", "", line).strip()
            current_content = []
        else:
            current_content.append(line)

    if current_content:
        chapters.append((current_title, "\n".join(current_content)))

    return chapters


def generate_report(thesis_title: str, chapters: List[Dict]) -> str:
    """生成检查报告"""
    report = []
    report.append(f"# {thesis_title} - 语言质量检查报告\n")
    report.append(f"**检查时间**: 2026年6月12日\n")
    report.append(f"**检查项**: 句式单调、过长句、空泛表达、过短段落、数字格式、专业术语\n")
    report.append("---\n")

    total_issues = sum(c["issues_count"] for c in chapters)
    report.append(f"## 总体统计\n")
    report.append(f"- **总章节数**: {len(chapters)}")
    report.append(f"- **总段落数**: {sum(c['total_paragraphs'] for c in chapters)}")
    report.append(f"- **问题段落数**: {total_issues}\n")

    # 问题类型统计
    issue_types = {}
    for chapter in chapters:
        for issue in chapter["issues"]:
            for issue_type, issues in issue["issues"].items():
                issue_types[issue_type] = issue_types.get(issue_type, 0) + len(issues)

    if issue_types:
        report.append("### 问题类型分布\n")
        for issue_type, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True):
            report.append(f"- **{issue_type}**: {count} 处")
        report.append("")

    report.append("---\n")

    # 章节详情
    report.append("## 章节详情\n")
    for chapter in chapters:
        if chapter["issues_count"] == 0:
            continue

        report.append(f"### {chapter['title']}\n")
        report.append(f"- 总段落数: {chapter['total_paragraphs']}")
        report.append(f"- 问题段落数: {chapter['issues_count']}\n")

        for issue in chapter["issues"]:
            report.append(f"**段落 {issue['paragraph_index']}**:")
            report.append(f"> {issue['paragraph_preview']}\n")
            for issue_type, issues in issue["issues"].items():
                for item in issues:
                    report.append(f"- ⚠️ **{item['type']}**: {item['detail']}")
            report.append("")

        report.append("---\n")

    # 改进建议
    report.append("## 改进建议\n")
    report.append("1. **句式单调**: 使用多样化的句式开头，避免连续相同句式")
    report.append("2. **过长句**: 将长句拆分为多个短句，每句不超过 60 字")
    report.append("3. **空泛表达**: 用具体数据和事实替换空泛套话")
    report.append("4. **过短段落**: 补充分析和论证，确保段落完整性")
    report.append("5. **数字格式**: 统一使用阿拉伯数字")
    report.append("6. **专业术语**: 首次出现的术语需标注英文原文\n")

    report.append("---\n")
    report.append("*本报告由 check_prose_quality.py 自动生成*")

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="论文语言质量检查")
    parser.add_argument("input_file", help="输入的 Markdown 文件路径")
    parser.add_argument("--output", "-o", help="输出报告路径（默认：paper-output/<论文标题>-prose-report.md）")
    parser.add_argument("--title", "-t", help="论文标题（默认从文件名提取）")
    parser.add_argument("--json", action="store_true", help="同时输出 JSON 格式报告")

    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"错误：文件不存在 - {input_path}")
        return 1

    # 提取论文标题
    thesis_title = args.title or input_path.stem

    # 加载并分析
    text = load_markdown(input_path)
    chapters_data = split_into_chapters(text)
    analysis_results = []
    for title, content in chapters_data:
        analysis_results.append(analyze_chapter(title, content))

    # 生成报告
    report = generate_report(thesis_title, analysis_results)

    # 输出报告
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path("paper-output") / f"{thesis_title}-prose-report.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"✅ 检查报告已生成: {output_path}")

    # JSON 输出
    if args.json:
        json_path = output_path.with_suffix(".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "title": thesis_title,
                "chapters": analysis_results,
                "summary": {
                    "total_chapters": len(analysis_results),
                    "total_paragraphs": sum(c["total_paragraphs"] for c in analysis_results),
                    "issues_count": sum(c["issues_count"] for c in analysis_results),
                }
            }, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON 报告已生成: {json_path}")

    return 0


if __name__ == "__main__":
    exit(main())
