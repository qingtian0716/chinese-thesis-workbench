# Standards

**Trigger:** School templates, advisor requirements, sample documents, or reference style decisions.
**Required inputs:** Templates, standards, advisor notes, sample/template analysis.
**Outputs:** standard-profile.yaml and sample-template-analysis.md

## Hard Rules

- Read `rules/00-global.md` before applying this phase rule.
- Preserve school/advisor requirements over bundled defaults.
- Update workflow state files when this rule changes scope, progress, blockers, or user decisions.

## Source Guidance


## Standards And Template Resolution

# Standards And Template Resolution

Use this reference when a thesis task mentions school templates, undergraduate thesis standards, national standards, reference formatting, or conflicts between bundled defaults and a real school requirement.

## Resolution Order

Apply requirements in this order:

1. School or college thesis template, writing guide, defense notice, and official forms.
2. Advisor, research group, task book, proposal, or project-specific requirement.
3. Ministry-level academic integrity and undergraduate thesis inspection rules.
4. School-specified national standards.
5. Bundled fallback defaults in `thesis-ai-standard/`.

Never let a bundled default override a real school template. If a requirement is missing, label the fallback as `default_not_school_confirmed`.

## Current Public Standard Baseline

As of 2026-05-01:

- `GB/T 7713.1-2025` is the current public baseline for thesis/dissertation writing structure and composition. Use it as a structural reference only unless the school explicitly adopts it.
- `GB/T 7714-2025` has been released and is scheduled for implementation on 2026-07-01. Many schools may still require `GB/T 7714-2015` during the transition. The `standard-profile.yaml` file must record the actual school-required version.
- Education ministry thesis inspection and academic-integrity rules are quality and integrity baselines, not page-layout templates.

## Standard Profile Fields To Fill First

Before drafting, update `thesis-ai-standard/templates/standard-profile.yaml`:

- school, college, major, update date
- exact template path or URL
- advisor or task-book requirement source
- reference style standard and version
- thesis writing standard version if specified by the school
- fallback items that are not school-confirmed
- Word/PDF layout-sensitive items that still need visual review

## Conflict Handling

When two sources conflict:

| Conflict | Action |
| --- | --- |
| school template vs bundled default | follow school template |
| advisor requirement vs bundled chapter model | follow advisor if academically reasonable |
| school requires `GB/T 7714-2015` but bundled docs mention 2025 | use 2015 and record the school source |
| school is silent on an item | use fallback default and mark it as replaceable |
| source is unclear or unofficial | do not enforce it; list as `needs_confirmation` |

## Output Contract

When resolving standards, return:

1. confirmed hard rules
2. fallback defaults
3. conflicts and chosen source
4. missing confirmations
5. layout items that require Word/PDF visual review

Do not write final thesis prose until hard rules and fallback assumptions are separated.


## Style Extraction

# Style Observation Prompt

鐢ㄤ簬杞婚噺瑙傚療妯℃澘鎴栨牱鏂囩殑鐗堝紡鐗瑰緛銆傝瀵熺粨鏋滃彧杩涘叆鏍锋枃/妯℃澘鍒嗘瀽鎶ュ憡銆佺洰褰曠‘璁ゅ拰瀛楁暟棰勭畻锛屼笉鐩存帴椹卞姩 DOCX 鎺掔増銆?

浼樺厛鍏虫敞锛?

- 鐩綍灞傜骇
- 绔犵骇鎴栬妭绾у瓧鏁?
- 鍥俱€佽〃銆佸叕寮忋€佷唬鐮佸嚭鐜拌妭濂?
- 涓€绾с€佷簩绾с€佷笁绾ф爣棰樼殑鍙鏍峰紡
- 姝ｆ枃銆佹憳瑕併€丄bstract銆佸叧閿瘝鐨勫彲瑙佹牱寮?
- 鍥鹃銆佽〃棰樸€佽〃鏍煎唴瀹圭殑鍙鏍峰紡
- 鍙傝€冩枃鐚€佽嚧璋€侀檮褰曠殑鍙缁勭粐鏂瑰紡
- 鏄惁鍒嗛〉銆佹槸鍚﹀眳涓€佸瓧浣撳瓧鍙枫€佹鍓嶆鍚庛€佽璺濄€侀琛岀缉杩涚瓑瑙傚療椤?

杈撳嚭鏃跺繀椤诲尯鍒嗭細

1. 宸茶瀵熷埌鐨勬牱鏂囨ā寮?
2. 涓嶈兘纭鐨勫瓧娈?
3. 闇€瑕佺敤鎴锋垨瀛︽牎瑙勮寖纭鐨勯」鐩?
4. 鍙敤浜庡缓璁洰褰曟垨瀛楁暟棰勭畻鐨勪緷鎹?

濡傛灉鏍锋枃鏄?`.docx`锛屽彲浠ユ墽琛岋細

```powershell
python scripts/docx/analyze_docx.py <sample.docx> --json-out paper-context/workflow/sample-docx-analysis.json
```

鍚庣画鐢熸垚 `.docx` 鏃朵粛浣跨敤鍐呯疆榛樿鏍煎紡銆備笉瑕佹妸瑙ｆ瀽 JSON 褰撴垚 Word 鏍峰紡閰嶇疆浼犵粰鐢熸垚鍣紝涔熶笉瑕佹壙璇鸿嚜鍔ㄥ鍒诲鏍℃ā鏉裤€?


## Default Style

# 榛樿璁烘枃鏍煎紡

鍦ㄤ笉濂楃敤瀛︽牎妯℃澘鏃讹紝DOCX 鐢熸垚鍣ㄤ娇鐢ㄤ互涓嬪唴缃牸寮忋€傝鏍煎紡鐢ㄤ簬鐢熸垚鍙槄璇汇€佸彲澶嶅埗鍒板鏍℃ā鏉夸腑鐨勬鏂囧垵绋匡紝涓嶅０鏄庡凡缁忕鍚堟煇涓€瀛︽牎鐨勬渶缁堢増寮忋€?

## 鍩烘湰鏍煎紡

- 璁烘枃棰樼洰锛氶粦浣?18pt锛屽姞绮楋紝灞呬腑
- 涓€绾ф爣棰橈細榛戜綋 18pt锛屽姞绮?
- 浜岀骇鏍囬锛氶粦浣?15pt锛屽姞绮?
- 涓夌骇鏍囬锛氶粦浣?12pt锛屽姞绮?
- 涓枃姝ｆ枃锛氬畫浣?12pt
- 鑻辨枃姝ｆ枃锛歍imes New Roman 12pt
- 姝ｆ枃娈佃惤锛?.25 鍊嶈璺濓紝棣栬缂╄繘绾?2 瀛楃
- 鎽樿銆丄bstract銆佺洰褰曘€佸弬鑰冩枃鐚€佽嚧璋€侀檮褰曟爣棰樺眳涓?
- 涓枃鍏抽敭璇嶏細鏍囩榛戜綋 12pt 鍔犵矖锛屽唴瀹瑰畫浣?12pt
- 鑻辨枃鍏抽敭璇嶏細鏍囩 Times New Roman 12pt 鍔犵矖锛屽唴瀹?Times New Roman 12pt

## 鍥捐〃鏍煎紡

- 鍥鹃锛氬畫浣?10.5pt锛屽浘涓嬫柟灞呬腑锛屽崟鍊嶈璺?
- 琛ㄩ锛氬畫浣?10.5pt锛岃〃涓婃柟灞呬腑锛屽崟鍊嶈璺?
- 琛ㄦ牸鏂囧瓧锛氬畫浣?10.5pt锛屽眳涓?

## 涓夌嚎琛ㄨ鑼?

琛ㄦ牸蹇呴』浣跨敤涓夌嚎琛紙涓ょ涓嶅皝鍙ｏ級锛岀姝娇鐢ㄧ綉鏍艰〃鎴栧叾浠栫被鍨嬭〃鏍笺€?

- 椤剁嚎锛?.5pt 绮楃嚎
- 鏍忕洰绾匡細0.75pt 缁嗙嚎
- 搴曠嚎锛?.5pt 绮楃嚎
- 鏃犲乏鍙宠竟妗嗙嚎

## 鍏紡涓庡弬鑰冩枃鐚?

- 鍏紡锛氶粯璁や繚鐣?LaTeX/source 鏂囨湰锛涚敤鎴烽€夋嫨 `formula_image` 鏃讹紝鍙寜 image map 鎻掑叆鍏紡鍥剧墖
- 鍙傝€冩枃鐚鏂囷細瀹嬩綋 10.5pt锛屾偓鎸傜缉杩涚害 2 瀛楃

