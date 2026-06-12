# Literature

**Trigger:** Literature review, PDF reference extraction, citation verification, or related work.
**Required inputs:** PDF papers, thesis topics, citation requirements.
**Outputs:** paper-context/literature/* and citation verification artifacts

## Hard Rules

- Read `rules/00-global.md` before applying this phase rule.
- Preserve school/advisor requirements over bundled defaults.
- Update workflow state files when this rule changes scope, progress, blockers, or user decisions.

## Source Guidance


## Literature And PDF Workflow

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

## 鑴氭湰瀵瑰簲鍏崇郴琛?

浠ヤ笅琛ㄦ牸鏄庣‘浜嗘枃鐚伐浣滄祦涓悇鑴氭湰鐨勫姛鑳藉拰璋冪敤椤哄簭锛岄伩鍏嶄笌 SKILL.md Hard Rules 涓殑娴佺▼鎻忚堪娣锋穯銆?

| 娴佺▼姝ラ | SKILL.md 鎻忚堪 | 瀵瑰簲鑴氭湰 | 鍔熻兘璇存槑 | 杈撳叆 | 杈撳嚭 |
|---------|--------------|---------|---------|------|------|
| 1. 鎻愬彇鏂囩尞 | - | `extract_pdf_references.py` | 浠?PDF 涓彁鍙栧弬鑰冩枃鐚?| PDF 鏂囦欢澶?| `reference-extraction.json` |
| 2. 浜ゅ弶寮曠敤 | - | `build_literature_crossrefs.py` | 寤虹珛鏂囩尞涓庝富棰樼殑鍏宠仈绱㈠紩 | `reference-extraction.json` + `topics.md` | `citation-crossrefs.md` |
| 3. 鏋勫缓鍊欓€夋睜 | build pool | `build_reference_pool.py` | **缁熻宸ュ叿**锛氬垎鏋愭枃鐚勾浠姐€佽瑷€鍒嗗竷 | 鍙傝€冩枃鐚?Markdown | 缁熻鎶ュ憡锛堣繎浜斿勾鍗犳瘮绛夛級 |
| 4. 鐢熸垚鏍搁獙娓呭崟 | generate verification checklist | `write_reference_verification_template.py` | 鐢熸垚鏂囩尞鏍搁獙娓呭崟 JSON | `reference-extraction.json`锛堝彲閫夛級 | `鏂囩尞鏍搁獙娓呭崟.json` |
| 5. 鏍搁獙 | verify | 浜哄伐/AI 鏍搁獙 | 楠岃瘉鏂囩尞鐨勭湡瀹炴€с€佸噯纭€?| 鏍搁獙娓呭崟 | 鏇存柊 status 瀛楁 |
| 6. 绛涢€?| filter | 浜哄伐/AI 绛涢€?| 鏍规嵁鏍搁獙缁撴灉绛涢€夋枃鐚?| 鏍搁獙娓呭崟 | 绛涢€夊悗鐨勬枃鐚垪琛?|
| 7. 鏍煎紡鍖?| format | 浜哄伐/AI 鏍煎紡鍖?| 鎸夊鏍¤姹傛牸寮忓寲鍙傝€冩枃鐚?| 绛涢€夊悗鐨勬枃鐚?| 鏈€缁堝弬鑰冩枃鐚垪琛?|

### 閲嶈璇存槑

1. **`build_reference_pool.py` 鏄粺璁″伐鍏?*锛屼笉鍦ㄤ富娴佺▼涓娿€傚畠鐢ㄤ簬鍒嗘瀽鏂囩尞姹犵殑鏁翠綋璐ㄩ噺锛堝杩戜簲骞村崰姣旓級锛岃€屼笉鏄瀯寤烘枃鐚睜鏈韩銆?

2. **涓绘祦绋嬮『搴?*锛歚extract_pdf_references.py` 鈫?`build_literature_crossrefs.py` 鈫?`write_reference_verification_template.py`

3. **Hard Rules 涓殑 "build pool"** 鎸囩殑鏄?`extract_pdf_references.py` + `build_literature_crossrefs.py` 鐨勭粍鍚堬紝鑰屼笉鏄?`build_reference_pool.py`銆?

4. **缃俊搴︾瓑绾ц鏄?*锛坄build_literature_crossrefs.py`锛夛細
   - `strong`锛坰core 鈮?6锛夛細楂樼疆淇″害锛屽叧閿瘝瀹屽叏鍖归厤
   - `weak_match`锛坰core 3-5锛夛細涓疆淇″害锛岄儴鍒嗗尮閰嶆垨骞翠唤鍔犲垎
   - `needs_check`锛坰core < 3锛夛細浣庣疆淇″害锛岄渶瑕佷汉宸ユ牳楠?

5. **骞翠唤缁熻璇存槑**锛坄build_reference_pool.py`锛夛細
   - 杈撳嚭杩戜簲骞存枃鐚崰姣旓紝鑰岄潪閫愭潯鎶?BAD_YEAR
   - 鎸夊鏍¤姹傦紙榛樿 60%锛夊垽鏂槸鍚﹁揪鏍?
   - 鎻愪緵骞翠唤鍒嗗竷缁熻渚涘弬鑰?

---

## 瀹屾暣宸ヤ綔娴佺ず渚?

```powershell
# 1. 浠?PDF 鎻愬彇鍙傝€冩枃鐚?
python scripts/literature/extract_pdf_references.py ./papers --out ./paper-context/literature

# 2. 寤虹珛鏂囩尞涓庝富棰樼殑浜ゅ弶寮曠敤
python scripts/literature/build_literature_crossrefs.py ./paper-context/literature/reference-extraction.json \
  --topics ./paper-context/topics.md \
  --out ./paper-context/literature/citation-crossrefs.md \
  --json-out ./paper-context/literature/citation-crossrefs.json

# 3. 缁熻鏂囩尞姹犺川閲忥紙鍙€夛紝鐢ㄤ簬妫€鏌ヨ繎浜斿勾鍗犳瘮锛?
python scripts/literature/build_reference_pool.py ./paper-context/literature/reference-extraction.md

# 4. 鐢熸垚鏂囩尞鏍搁獙娓呭崟锛堜粠宸叉彁鍙栫殑鏂囩尞鑷姩鐢熸垚锛?
python scripts/literature/write_reference_verification_template.py \
  ./paper-context/literature/鏂囩尞鏍搁獙娓呭崟.json \
  --input ./paper-context/literature/reference-extraction.json \
  --default-status needs_check

# 5. 浜哄伐/AI 鏍搁獙鏂囩尞锛堟洿鏂?status 瀛楁锛?
# 6. 绛涢€夐€氳繃鏍搁獙鐨勬枃鐚?
# 7. 鎸夊鏍¤姹傛牸寮忓寲鍙傝€冩枃鐚?
```

