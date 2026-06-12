# Literature And PDF Workflow

Use this reference when a thesis needs literature review, related work, citation cleanup, citation placement, or reference extraction from PDF papers.

## Inputs

Preferred inputs:

- PDF papers in one folder
- thesis title, abstract, keywords, chapter outline, or `thesis-ai-spec.yaml`
- school reference style requirement
- existing reference list, if any

## PDF Reference Extraction

Run:

```powershell
python .\scripts\literature\extract_pdf_references.py .\papers --out .\paper-context\literature
```

Outputs:

```text
paper-context/literature/
  reference-extraction.json
  reference-extraction.md
```

The script extracts candidate reference sections. Treat output as raw evidence. Verify bibliographic fields manually or with trusted sources before final formatting.

## Citation Cross-References

If a topic outline exists, create a citation cross-reference index:

`paper-context/topics.md` is a lightweight topic file. It can be drafted from the confirmed outline, `thesis-ai-spec.yaml`, or user-provided keywords. Use one topic per bullet; include methods, domain terms, chapter names, and known acronyms that should guide citation placement.

Example:

```markdown
# Thesis Topics

- Chapter 1: research background; domestic and international status; problem definition
- Chapter 2: key theories; core technologies; evaluation methods
- Chapter 3: requirement analysis; system architecture; database design
- Chapter 4: implementation modules; algorithms; user workflow
- Chapter 5: testing; experiment results; comparison baseline
- Keywords: recommender system; collaborative filtering; Vue; Spring Boot
```

```powershell
python .\scripts\literature\build_literature_crossrefs.py .\paper-context\literature\reference-extraction.json --topics .\paper-context\topics.md --out .\paper-context\literature\citation-crossrefs.md --json-out .\paper-context\literature\citation-crossrefs.json
```

Cross-reference rules:

- Match references to claims by overlap with topic terms, methods, domain words, and known acronyms.
- Prefer recent and directly relevant papers for research status sections.
- Prefer method papers for method/theory sections.
- Prefer system/application papers for design comparison sections.
- Do not cite a paper merely because a keyword appears once.
- Mark weak matches as `needs_check`.

After generating cross-references, update `thesis-ai-standard/templates/citation-crossref-register.yaml` or a project copy of it. The register is the closure layer:

- body claim -> citation candidate
- citation candidate -> verified reference-list entry
- reference-list entry -> body citation location
- unresolved candidate -> `needs_check`, `rejected`, or `missing_source`

## Writing Literature Review

Structure by theme, not by one-paper-per-paragraph:

1. Define the research or engineering problem.
2. Group literature into 2-4 themes.
3. Compare methods, data, systems, or conclusions.
4. Identify the gap that the thesis addresses.
5. Connect the gap to the thesis work.

Avoid:

- fabricated author/year/venue
- references not cited in body text
- body citations missing from final reference list
- DOI or URL hallucination
- "AI found" or "the uploaded paper says" wording

## Final Checks

- Every cited source appears in the reference list.
- Every reference-list item is cited, unless school rules allow uncited background references.
- `citation-crossref-register.yaml` or equivalent notes record the body/reference closure.
- Reference format follows `standard-profile.yaml`.
- Extraction uncertainty is resolved before final submission.

---

## 脚本对应关系表

以下表格明确了文献工作流中各脚本的功能和调用顺序，避免与 SKILL.md Hard Rules 中的流程描述混淆。

| 流程步骤 | SKILL.md 描述 | 对应脚本 | 功能说明 | 输入 | 输出 |
|---------|--------------|---------|---------|------|------|
| 1. 提取文献 | - | `extract_pdf_references.py` | 从 PDF 中提取参考文献 | PDF 文件夹 | `reference-extraction.json` |
| 2. 交叉引用 | - | `build_literature_crossrefs.py` | 建立文献与主题的关联索引 | `reference-extraction.json` + `topics.md` | `citation-crossrefs.md` |
| 3. 构建候选池 | build pool | `build_reference_pool.py` | **统计工具**：分析文献年份、语言分布 | 参考文献 Markdown | 统计报告（近五年占比等） |
| 4. 生成核验清单 | generate verification checklist | `write_reference_verification_template.py` | 生成文献核验清单 JSON | `reference-extraction.json`（可选） | `文献核验清单.json` |
| 5. 核验 | verify | 人工/AI 核验 | 验证文献的真实性、准确性 | 核验清单 | 更新 status 字段 |
| 6. 筛选 | filter | 人工/AI 筛选 | 根据核验结果筛选文献 | 核验清单 | 筛选后的文献列表 |
| 7. 格式化 | format | 人工/AI 格式化 | 按学校要求格式化参考文献 | 筛选后的文献 | 最终参考文献列表 |

### 重要说明

1. **`build_reference_pool.py` 是统计工具**，不在主流程上。它用于分析文献池的整体质量（如近五年占比），而不是构建文献池本身。

2. **主流程顺序**：`extract_pdf_references.py` → `build_literature_crossrefs.py` → `write_reference_verification_template.py`

3. **Hard Rules 中的 "build pool"** 指的是 `extract_pdf_references.py` + `build_literature_crossrefs.py` 的组合，而不是 `build_reference_pool.py`。

4. **置信度等级说明**（`build_literature_crossrefs.py`）：
   - `strong`（score ≥ 6）：高置信度，关键词完全匹配
   - `weak_match`（score 3-5）：中置信度，部分匹配或年份加分
   - `needs_check`（score < 3）：低置信度，需要人工核验

5. **年份统计说明**（`build_reference_pool.py`）：
   - 输出近五年文献占比，而非逐条报 BAD_YEAR
   - 按学校要求（默认 60%）判断是否达标
   - 提供年份分布统计供参考

---

## 完整工作流示例

```powershell
# 1. 从 PDF 提取参考文献
python scripts/literature/extract_pdf_references.py ./papers --out ./paper-context/literature

# 2. 建立文献与主题的交叉引用
python scripts/literature/build_literature_crossrefs.py ./paper-context/literature/reference-extraction.json \
  --topics ./paper-context/topics.md \
  --out ./paper-context/literature/citation-crossrefs.md \
  --json-out ./paper-context/literature/citation-crossrefs.json

# 3. 统计文献池质量（可选，用于检查近五年占比）
python scripts/literature/build_reference_pool.py ./paper-context/literature/reference-extraction.md

# 4. 生成文献核验清单（从已提取的文献自动生成）
python scripts/literature/write_reference_verification_template.py \
  ./paper-context/literature/文献核验清单.json \
  --input ./paper-context/literature/reference-extraction.json \
  --default-status needs_check

# 5. 人工/AI 核验文献（更新 status 字段）
# 6. 筛选通过核验的文献
# 7. 按学校要求格式化参考文献
```
