# Intake

**Trigger:** Material collection, project start, or workspace reuse decision.
**Required inputs:** User thesis request and available materials.
**Outputs:** material-inventory.md, user-decisions.md, user-dashboard.md

## Hard Rules

- Read `rules/00-global.md` before applying this phase rule.
- Preserve school/advisor requirements over bundled defaults.
- Update workflow state files when this rule changes scope, progress, blockers, or user decisions.

## Source Guidance


## Intake Prompt

# Intake Prompt

鐢ㄤ簬閿佸畾鐢ㄦ埛杈撳叆绾︽潫銆?

纭害鏉燂細

- 绗竴娆″洖澶嶆椂锛屽厛鏀惰祫鏂欙紝涓嶅紑鍐欏垵绋裤€?
- 鑻ョ敤鎴峰皻鏈彁渚涙ā鏉裤€佹牱鏂囥€佷换鍔′功銆佸紑棰樻姤鍛婄瓑杈呭姪璧勬枡锛屽繀椤讳紭鍏堢储瑕侊紝闄ら潪鐢ㄦ埛鏄庣‘璇粹€滄病鏈夆€濇垨鈥滄寜椤圭洰鑷繁鍐欌€濄€?
- 濡傛灉宸茬粡缁欎簡鏍锋枃鎴栨ā鏉匡紝蹇呴』鍏堝垎鏋愶紝鍐嶅洖浼犵洰褰曘€佸瓧鏁板拰鐗堝紡瑙傚療锛屼笉寰楄烦杩囧垎鏋愮洿鎺ュ啓姝ｆ枃銆?
- 杈撳叆浼樺厛绾ч粯璁ゆ槸锛氬鏍℃ā鏉?> 浠诲姟涔?寮€棰樻姤鍛?> 鐢ㄦ埛鏄庣‘瑕佹眰 > 鏍锋枃 > 椤圭洰婧愮爜 > README > 鏃ц鏄庢枃妗ｃ€?
- 鏃ч儴缃茶鏄庛€佸巻鍙查」鐩粙缁嶃€佹紨绀烘枃妗ｉ粯璁よ涓轰綆鍙俊鏉ユ簮銆?
- 姣忎竴椤规潗鏂欓兘蹇呴』鍦?`paper-context/workflow/material-inventory.md` 涓爣璁颁负 `required`銆乣strongly_recommended` 鎴?`optional`锛屽苟鍐欐竻缂哄け褰卞搷銆佹槸鍚﹀彲鏈夐檺缁х画銆佺敤鎴蜂笅涓€姝ャ€?

蹇呴』纭锛?

1. 璁烘枃绫诲瀷
2. 璇鹃鍚嶇О
3. 鏄惁鏈夊鏍℃ā鏉?
4. 鏄惁鏈夊線灞婃牱鏂?
5. 鏄惁鏈夊瓧鏁拌姹?
6. 鏄惁蹇呴』浜や粯 `.docx`
7. 鏄惁鏈夊紑棰樻姤鍛娿€佷换鍔′功鎴栧皝闈㈠瓧娈佃姹?
8. 濡傛灉闇€瑕佺湡瀹為〉闈㈡埅鍥撅紝绯荤粺璁块棶鍦板潃鎴栧惎鍔ㄦ柟寮忔槸浠€涔?
9. 涓昏鏂囨枃浠跺悕鏄惁蹇呴』浣跨敤璁烘枃鏍囬
10. 鏄惁闇€瑕侀澶栭檮浠?`.docx`

蹇呴』閫夋嫨浜や粯璺緞锛?

1. 浠庨浂鐢熸垚锛堥粯璁ゆ牱寮忥級
2. 浠庨浂鐢熸垚锛堟寜鏍锋枃鐗堝紡璐磋繎锛?
3. 瀛︽牎妯℃澘鍓湰濉厖锛堟帹鑽愮敤浜庢牸寮忚姹備弗鏍肩殑瀛︽牎锛?
4. 鍦ㄥ凡鏈夊垵绋夸笂鍋氬眬閮ㄥ鍒犳敼

閫夋嫨缁撴灉蹇呴』璁板綍鍒?`paper-context/workflow/user-decisions.md`銆?

棣栨鍥炲鏃讹紝蹇呴』鏄庣‘鍛婅瘔鐢ㄦ埛鍙互鐩存帴鍙戦€佹湰鍦拌矾寰勶紝绀轰緥锛?

- `D:\璁烘枃妯℃澘.docx`
- `D:\鍘嗗眾鏍锋枃.pdf`
- `D:\寮€棰樻姤鍛?docx`

濡傛灉鐢ㄦ埛涓€娆℃病缁欏叏锛屼笉瑕佽繛缁姏寰堝闂銆備紭鍏堢‘璁わ細

1. 鏄惁鏈夋ā鏉挎垨鏍锋枃
2. 鏄惁鏈夊紑棰樻姤鍛婃垨浠诲姟涔?
3. 鏄惁鏈夊瓧鏁拌姹?
4. 鏄惁鏈€缁堣 Word
5. 濡傛灉闇€瑕佹埅鍥撅紝绯荤粺濡備綍鎵撳紑
6. 璁烘枃鏍囬鏄粈涔?

鏉愭枡涓嶅叏鏃讹紝涓嶈鍙鈥滆琛ユ潗鏂欌€濄€傚繀椤诲憡璇夌敤鎴凤細

1. 缂哄け鏉愭枡褰卞搷鍝簺绔犺妭鎴栦氦浠樼墿
2. 褰撳墠鏄惁鍙互鏈夐檺缁х画
3. 鏈夐檺缁х画浼氱壓鐗蹭粈涔?
4. 鐢ㄦ埛鍙互閫夋嫨琛ュ厖銆佺‘璁ゆ病鏈夈€佹垨鏆傜紦
5. 鎺ㄨ崘璺緞鏄粈涔?

鎷垮埌妯℃澘銆佹牱鏂囨垨寮€棰樻姤鍛婂悗锛屼笉瑕佺珛鍒诲紑鍐欙紝蹇呴』鍏堝垎鏋愩€傝繖閲岀殑鍒嗘瀽鍙敤浜庣洰褰曘€佸瓧鏁般€佺増寮忚瀵熷拰鍥捐〃鑺傚锛涜В鏋愮粨鏋滀笉寰楃洿鎺ラ┍鍔?DOCX 鎺掔増锛岄櫎闈炵敤鎴锋槑纭€夋嫨鏍锋枃鐗堝紡璐磋繎鐢熸垚鎴栧鏍℃ā鏉垮壇鏈～鍏咃細

1. 鐩綍缁撴瀯鏄惁瀹屾暣
2. 鍚勭珷澶ц嚧瀛楁暟
3. 鏍囬銆佹鏂囥€佹憳瑕併€佸叧閿瘝銆佸浘棰樸€佽〃棰樸€佽〃鏍煎唴瀹圭殑鐗堝紡瑙傚療
4. 鍥俱€佽〃銆佷唬鐮侀€氬父鍑虹幇鍦ㄤ粈涔堢珷鑺?

濡傛灉鏍锋枃鎴栨ā鏉挎槸 `.docx`锛屼紭鍏堟墽琛岃В鏋愯剼鏈垨鎺ユ敹鐢ㄦ埛/澶栭儴宸ュ叿鎻愪緵鐨勭瓑浠疯В鏋愮粨鏋滐細

- `python scripts/docx/analyze_docx.py <sample.docx> --json-out paper-context/workflow/sample-docx-analysis.json`

濡傛灉鏍锋枃鏄?PDF锛屼紭鍏堟墽琛岃В鏋愯剼鏈垨鎺ユ敹鐢ㄦ埛/澶栭儴宸ュ叿鎻愪緵鐨勭瓑浠疯В鏋愮粨鏋滐細

- `python scripts/docx/analyze_sample_pdf.py <sample.pdf> --json-out paper-context/workflow/sample-analysis.json`

瑙ｆ瀽鑴氭湰鍙槸杞婚噺鍒嗘瀽杈撳叆灞傘€傝嫢鑴氭湰杈撳嚭涓嶈冻銆佸け璐ユ垨鍙兘缁欏嚭寮辩粨鏋勭粨鏋滐紝涓嶈鎶婅剼鏈棶棰樺綋浣滆鏂囨祦绋嬭兘鍔涘凡缁忓畬鎴愶紱搴斿湪鏍锋枃/妯℃澘鍒嗘瀽鎶ュ憡涓爣璁?`partial`銆乣failed` 鎴?`needs_confirmation`锛屽苟缁х画鐢熸垚鏈夐檺鐨勭敤鎴峰彲璇诲垎鏋愩€傝В鏋愮粨鏋滀笉寰楃洿鎺ヤ綔涓?DOCX 鎺掔増瑙勫垯锛岄櫎闈炵敤鎴锋槑纭€夋嫨 `--sample-analysis` 鏍锋枃鐗堝紡璐磋繎鐢熸垚鎴?`--from-template` 妯℃澘鍓湰濉厖銆?

鍒嗘瀽瀹屾垚鍚庯紝蹇呴』鍏堝洖缁欑敤鎴凤細

1. 杈撳叆璧勬枡琛?
2. 褰撳墠寤鸿鐩綍琛?
3. 鍚勭珷瀛楁暟棰勭畻琛?
4. 鐗堝紡瑙傚療涓庨渶瑕佷汉宸ョ‘璁ょ殑椤圭洰
5. 鏂囦欢鍛藉悕鏂规
6. 鏄惁棰濆鐢熸垚闄勪欢 `.docx`

骞剁瓑寰呯敤鎴风‘璁ゆ垨淇敼銆?

