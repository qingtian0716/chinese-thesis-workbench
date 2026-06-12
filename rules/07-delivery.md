# Delivery

**Trigger:** DOCX generation, template fill, existing draft edit, appendix generation, or final package.
**Required inputs:** Confirmed thesis Markdown/spec/assets and chosen delivery mode.
**Outputs:** paper-output DOCX artifacts and delivery report

## Hard Rules

- Read `rules/00-global.md` before applying this phase rule.
- Preserve school/advisor requirements over bundled defaults.
- Update workflow state files when this rule changes scope, progress, blockers, or user decisions.

## Source Guidance


## DOCX Delivery

# DOCX Delivery

鐢ㄤ簬灏嗚鏂囨簮绋胯浆鎴?`.docx`锛屾垨鍦ㄧ敤鎴锋槑纭€夋嫨鏃跺～鍏呭鏍℃ā鏉垮壇鏈€佸眬閮ㄧ紪杈戝凡鏈夊垵绋裤€傛牳蹇冨師鍒欐槸锛氳兘澶嶅埗/缂栬緫灏变繚鐣欏師 DOCX 鏍煎紡锛屼笉鑳藉鍒舵椂鍐嶇敓鎴愮粨鏋勬竻鏅般€佺礌鏉愬畬鏁淬€佸彲澶嶅埗绮樿创鐨?Word 鏂囨。銆?

## Supported Scope

榛樿 DOCX 鍙礋璐ｅ唴缃牸寮忥細

- 棰樼洰
- 鎽樿 / Abstract
- 鍏抽敭璇?/ Keywords
- 鐩綍鏍囬鎴栫洰褰曞崰浣?
- 涓€绾с€佷簩绾с€佷笁绾ф爣棰?
- 姝ｆ枃
- 鍥鹃銆佽〃棰?
- 琛ㄦ牸
- 鍏紡
- 鍙傝€冩枃鐚?
- 鑷磋阿
- 闄勫綍
- 浠ｇ爜鍧?
- 缂哄け绱犳潗鍗犱綅

濡傛灉瀛︽牎瑕佹眰涓ユ牸妯℃澘鏍煎紡锛屼紭鍏堥€夋嫨 M3 妯℃澘鍓湰濉厖锛涘畠澶嶅埗瀛︽牎妯℃澘鏂囦欢鍚庡彧鎻掑叆鎴栨浛鎹㈡枃鏈紝浠嶉渶鐢ㄦ埛鍦?Word 涓汉宸ユ牳瀵圭洰褰曘€佸皝闈€佸浘琛ㄥ拰椤甸潰甯冨眬銆?

## Delivery Modes

- M1 default style generation: creates a new DOCX from Markdown using built-in styles.
- M2 sample style generation: creates a new DOCX from Markdown while applying high-confidence styles from `--sample-analysis`.
- M3 template copy fill: copies a school template DOCX and fills text into the copy. Use this when school formatting fidelity matters most.
- M4 existing draft edit: edits paragraph text in an existing draft with unique anchors.

M3 does not rebuild the table of contents, replace figures/tables, or guarantee every cover-field placeholder will be found. The user should update the TOC in Word and manually verify cover fields, figures, tables, and page layout.

## Default Command

```powershell
python scripts/docx/generate_thesis_docx.py thesis.md output/thesis.docx --image-map image-map.json
```

鏍锋枃鐗堝紡璐磋繎鐢熸垚锛?

```powershell
python scripts/docx/generate_thesis_docx.py thesis.md output/thesis.docx --sample-analysis paper-context/workflow/sample-docx-analysis.json
```

瀛︽牎妯℃澘鍓湰濉厖锛?

```powershell
python scripts/docx/apply_textual_edits.py --from-template school-template.docx --thesis-md paper-output/thesis.md --spec thesis-ai-standard/templates/thesis-ai-spec.yaml --out paper-output/thesis.docx
```

鍏紡榛樿淇濈暀涓?LaTeX 鏂囨湰锛屼究浜庣敤鎴峰悗缁墜鍔ㄨ浆 Word 鍏紡锛?

```powershell
python scripts/docx/generate_thesis_docx.py thesis.md output/thesis.docx --formula-mode latex_text
```

濡傛灉鐢ㄦ埛宸茬粡鎻愪緵娓叉煋濂界殑鍏紡鍥剧墖锛屽苟鍦?image map 涓敤鍏紡鏂囨湰浣滀负 key锛屽彲浠ラ€夋嫨鍥剧墖妯″紡锛?

```powershell
python scripts/docx/generate_thesis_docx.py thesis.md output/thesis.docx --image-map image-map.json --formula-mode formula_image
```

鐢熸垚鍣ㄤ笉鎻愪緵瀛︽牎妯℃澘鍖归厤鍙傛暟銆傛牱鏂囩増寮忚创杩戝彧鏄珮缃俊鏍峰紡鍊煎悎骞讹紝涓嶆槸妯℃澘澶嶅埢銆傚鏍℃ā鏉垮簲璧?`--from-template` 鍓湰濉厖璺緞銆?

## Asset Rules

- 鎴浘銆佸浘琛ㄥ拰鍏紡鍥剧墖閫氳繃 image map 鎻掑叆銆?
- Markdown 琛ㄦ牸搴斿敖閲忚浆鎴?Word 琛ㄦ牸銆?
- 鏃犳硶瑙ｆ瀽涓鸿〃鏍兼椂锛屼繚鐣欐枃鏈垨鏄庣‘鍗犱綅锛屼笉鑳介潤榛樹涪澶便€?
- Mermaid / PlantUML / draw.io 婧愮爜浠嶈繘鍏ラ檮浠?DOCX銆?

## Markdown Cleanup

瀵煎嚭鍓嶅繀椤荤‘璁ゆ鏂囧凡缁忔竻鐞嗘帀 Markdown 鐥曡抗锛屼緥濡傦細

- `**鍔犵矖**`
- `` `code` ``
- `[閾炬帴鏂囧瓧](https://example.com)`

杩欎簺涓嶈兘鍘熸牱杩涘叆鏈€缁?`.docx`锛屼絾 LaTeX 鍏紡婧愮爜鍦?`latex_text` 妯″紡涓嬪彲浠ヤ繚鐣欍€?


## Final Delivery Check

# Final Delivery Check

浜や粯鍓嶉€愰」妫€鏌ワ細

1. 绔犺妭缁撴瀯瀹屾暣锛屾爣棰樺眰绾ц繛缁€?
2. 瀛楁暟鎺ヨ繎宸茬‘璁ょ洰鏍囷紱浼樺厛鏍稿 `python scripts/review/count_chapter_words.py <thesis.md>` 鐨?`APPROX_WORDS`銆?
3. 鍙傝€冩枃鐚暟閲忋€佸勾浠借寖鍥村拰鏍煎紡绗﹀悎宸茬‘璁よ姹傘€?
4. 鍥俱€佽〃銆佸叕寮忕紪鍙疯繛缁紝姝ｆ枃鏈夐娆″紩鐢ㄣ€?
5. 娌℃湁娈嬬暀鍗犱綅绗︺€佸緟琛ヨ鏄庢垨鏈鐞嗘壒娉ㄣ€?
6. 涓?`.docx` 鐪熷疄瀛樺湪锛屾枃浠跺悕浣跨敤璁烘枃棰樼洰鎴栫敤鎴风‘璁ょ殑浜や粯鍚嶃€?
7. 鎽樿銆丄bstract銆佺洰褰曘€佸弬鑰冩枃鐚€佽嚧璋€侀檮褰曠瓑鍏抽敭閮ㄥ垎瀛樺湪涓旀牱寮忎竴鑷淬€?
8. 涓嫳鏂囧拰鏁板瓧瀛椾綋鏃犳槑鏄炬贩涔便€?
9. 鍥捐〃鍜屽叕寮忕礌鏉愬凡鐪熷疄鎻掑叆锛屾垨鏄庣‘淇濈暀涓哄彲澶嶅埗鐨勬枃鏈?鍗犱綅銆?
10. 鏈€缁堟鏂囨病鏈夋畫鐣?`**`銆佸弽寮曞彿銆佽８ Markdown 閾炬帴绛夋帓鐗堢棔杩广€?
11. 濡傛灉闇€瑕侀檮浠?`.docx`锛岀‘璁ら檮浠剁湡瀹炲瓨鍦ㄣ€?
12. 宸茬敓鎴愭垨鏇存柊鏂囩尞鏍搁獙娓呭崟锛屼緥濡?`references-verified.json` 鎴栫瓑浠疯褰曘€?
13. 娌℃湁娣峰叆浣庡彲淇℃棫璇存槑鏂囨。涓殑浜嬪疄銆?

杞欢绯荤粺銆佺郴缁熻璁℃垨鏁版嵁搴撹璁＄被璁烘枃杩橀渶瑕佹鏌ワ細

1. 瀹炵幇/璁捐绔犺妭鏄惁瑕嗙洊涓昏妯″潡锛岃€屼笉鏄彧鍫嗘妧鏈粙缁嶃€?
2. 涓昏妯″潡鏄惁缁戝畾鐪熷疄椤圭洰璇佹嵁锛屼緥濡備唬鐮佽矾寰勩€佹帴鍙ｃ€丼QL銆佽繍琛屾埅鍥俱€佹祴璇曡褰曟垨绛変环鏉愭枡銆?
3. 鏁版嵁搴撳唴瀹规槸鍚﹀湪闇€瑕佹椂鎻愪緵 E-R 鍥俱€佽〃缁撴瀯鎴栧疄浣撳叧绯昏鏄庛€?
4. 椤甸潰鎴浘鏁伴噺鏄惁涓庡姛鑳借寖鍥村尮閰嶏紱涓嶈缃€氱敤涓嬮檺銆?
5. 璁捐鍥炬暟閲忔槸鍚︿笌绔犺妭璁鸿瘉闇€瑕佸尮閰嶏紱涓嶈缃€氱敤涓嬮檺銆?
6. 濡傛灉瀛樺湪鎴浘鍗犱綅锛岀‘璁?`image-map.json` 宸茬敓鎴愭垨鐢ㄦ埛宸叉彁渚涘搴斿浘鐗囥€?
7. 濡傛灉瀛樺湪 Mermaid / PlantUML 鍥撅紝纭闄勪欢 `.docx` 宸茬敓鎴愬苟鏀跺綍婧愮爜銆?

鏈€浣庨獙璇佸懡浠わ細

```powershell
python scripts/review/count_chapter_words.py <thesis.md>
python scripts/figures/ensure_thesis_assets.py <thesis.md> --check-only
```

