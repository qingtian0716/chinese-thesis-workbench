# Literature Search Module

Use this module when the user asks to find literature, generate search keywords,
build a retrieval plan, or check whether downloaded papers cover the thesis topics.
This module is fully independent — it does not modify or trigger any step in the
main thesis workflow.

## Boundary

- Read: `thesis-ai-standard/templates/thesis-ai-spec.yaml` (if exists),
  `paper-context/evidence/tech-stack.md` (if exists), user-provided input.
- Write: `paper-context/literature/search-plan/` only.
- Never modify workflow logs, spec files, figure registry, or any file outside
  `paper-context/literature/search-plan/`.
- Never fabricate real paper titles, author names, journal names, DOI values,
  or publication years as examples. Doing so misleads the user into citing
  nonexistent sources.
- Never claim a specific paper exists. Only provide search directions.
- After delivering the plan, explicitly tell the user:
  "以上是检索方向，不是真实文献。请按关键词去数据库查找并验证。"

## Trigger Phrases

Enter this module when the user says any of the following (or similar):

- "帮我找文献" / "我需要文献"
- "给我检索关键词" / "生成检索方案"
- "我不知道要查什么" / "文献从哪里找"
- "帮我规划一下参考文献"
- "literature" / "search keywords" / "references plan"

Do NOT enter the main thesis writing workflow for these requests.

## Required Inputs

Before generating a plan, confirm the following. If context.json exists from
`collect_thesis_context.py`, read it first; otherwise ask the user directly.

必须确认：
1. 论文题目（或研究方向描述）
2. 核心技术或研究方法（如：区块链、机器学习、问卷调查等）
3. 学校参考文献要求（总篇数、外文篇数下限、近五年比例）
4. 论文章节结构（可选，有则更精准）

If the user cannot provide item 3, use the default from `references/writing/reference-selection.md`.
If the user cannot provide item 4, generate a plan based on a standard software-system
or research-paper chapter structure.

Do not wait for all four items before starting — if the user provides at least
items 1 and 2, proceed and note assumptions clearly.

## AI Reasoning Requirements

Read `references/literature-search/keyword-strategy.md` before generating keywords.

When reasoning about keywords, do the following:

1. **Identify the research layer**: Is this an engineering implementation thesis,
   an algorithm improvement thesis, or an applied survey thesis? The literature
   distribution strategy differs for each.

2. **Map tech stack to academic terms**: e.g., "Spring Boot" → "微服务架构 /
   microservice architecture"; "Vue.js" → "前后端分离 / single-page application";
   "BERT" → "预训练语言模型 / pre-trained language model". Never use product names
   as academic search terms.

3. **Infer hidden literature needs**: Beyond what the user explicitly mentions,
   identify the underlying research problems. e.g., a blockchain thesis implicitly
   needs literature on "去中心化信任 / decentralized trust" and "数据不可篡改性 /
   data immutability" for Chapter 1's problem statement.

4. **Identify the best venues** for each keyword group: tell the user which
   journals or conferences are most likely to have relevant papers
   (e.g., "该方向主要发表在 IEEE Transactions on Services Computing 和 ACM SIGMOD").

5. **Balance Chinese and English coverage**: explicitly flag which keyword groups
   are best suited for English databases (IEEE Xplore, ACM DL, Google Scholar)
   to help the user meet the foreign-literature requirement.

## Output

Generate two files:

### `paper-context/literature/search-plan/search-plan.md`

Human-readable retrieval plan. Structure:

```
文献检索方案

论文信息
（题目、类型、检索目标总结）

检索目标
（总篇数、外文下限、近五年比例目标、各章分配）

L1 核心主题词（必检）
（每组：中文检索式 / 英文检索式 / 对应章节 / 推荐数据库 /
建议年份 / 目标篇数 / 为什么这组词有效）

L2 技术方法词（必检）
（同上格式）

L3 应用领域词（建议检）
（同上格式）

L4 对比参照词（可选检）
（同上格式）

检索操作说明
（参考 references/literature-search/database-guide.md）

完成后的下一步
（告知用户下载 PDF 后可运行 extract_pdf_references.py，
以及可运行 validate_coverage.py 检查覆盖情况）
```

### `paper-context/literature/search-plan/search-plan.json`

Machine-readable version. Structure:

```json
{
  "schema_version": "1.0",
  "thesis_title": "",
  "thesis_type": "",
  "requirement": {
    "total": 0,
    "foreign_min": 0,
    "recent_years_ratio": 0.0,
    "recent_years_cutoff": 2020
  },
  "layers": [
    {
      "layer": "L1",
      "name": "核心主题词",
      "priority": "required",
      "groups": [
        {
          "zh_query": "",
          "en_query": "",
          "target_chapter": "",
          "databases": [],
          "year_range": "",
          "target_count": 0,
          "rationale": ""
        }
      ]
    }
  ]
}
```

## Coverage Check

After the user downloads papers and runs `extract_pdf_references.py`, they can
optionally run:

```powershell
python scripts/literature-search/validate_coverage.py \
  --plan paper-context/literature/search-plan/search-plan.json \
  --extracted paper-context/literature/reference-extraction.json \
  --out paper-context/literature/search-plan/coverage-report.md
```

The coverage report shows whether each layer's target count is met, whether the
Chinese/foreign ratio is on track, and which directions still need more papers.
