# Chapter Writer Prompt

用于按样文章节节奏写作。样文节奏是参考，不得覆盖学校/导师要求、证据链和当前论文类型。

## Step 0：字数预算分配（开写前只做一次）

开写前，AI 必须先完成字数分配：

1. 读取论文目录
2. 读取 `paper-context/workflow/chapter-word-budget.md`（章级总预算）
3. 对每一章：
   - 列出该章所有子节（按目录结构）
   - 评估每个子节的内容权重：核心内容节多写，过渡节、小结节少写
   - 分配字数，使该章所有子节字数之和 ≈ 章级总预算
   - 每个分配项标注优先级（high / medium / low）和理由
4. 将完整分配表保存到 `paper-context/workflow/section-word-budget.md`

## 写作流程

### 逐节写作

- 读取 `section-word-budget.md` 获取当前节的字数目标
- 每节按目标字数写作，不超出 10%
- 语言风格贴近本科论文样文，但避免机械套用样文结构
- 软件系统/系统设计类论文中，第 4 章或"系统详细设计与实现"通常是全文最长章节；其他论文类型按研究问题和学校要求安排篇幅
- 软件系统/系统设计类论文的实现章节可按"模块说明 -> 流程图/结构图 -> 关键实现 -> 页面截图"展开
- 软件系统/系统设计类论文的主要模块建议提供页面截图、核心代码、SQL 或关键实现片段；非软件类论文使用实验、调研、文本分析或数据材料替代
- 系统设计类论文可在设计章放置架构图、流程图、数据模型图等；图数量由证据和学校要求决定，不设固定张数
- 只有涉及数据库设计的系统设计类论文才要求 E-R 图或等价数据设计证据
- 如果任务书要求与源码实现不一致，正文必须优先按源码事实写，并在相关段落中保持口径一致

### 每节写后校验

- 写完一节后立即统计字数，运行：
  `python scripts/review/count_chapter_words.py <thesis.md> --budget <当前章目标字数>`
- 如果输出 STATUS=OVER：压缩该章中字数最多的节，直到 STATUS=OK
- 不能残留 `**`、反引号、Markdown 链接等标记

### 语言风格检查（每节写后）

写完每节后，必须进行语言风格检查：

1. **禁用词检查**：扫描 `references/writing/prose-style-guide.md` 中的禁用词表
   - 发现空泛表达（如"显著提升"、"具有重要意义"）必须替换为具体数据
   - 发现口语化表达（如"做了"、"搞了"）必须替换为学术表达

2. **句式检查**：
   - 避免连续三句以相同词开头
   - 单句不超过 60 字，超过必须拆分
   - 避免连续使用"通过……"句式

3. **段落结构检查**：
   - 每段必须包含：论点句 → 证据/数据句 → 分析句
   - 段落字数不少于 80 字，不超过 300 字

4. **参考表达**：
   - 使用 `references/writing/chinese-academic-phrases.md` 中的推荐表达
   - 避免表中的"避免表达"

5. **术语规范**：
   - 专业术语首次出现需标注英文原文
   - 参考 `references/writing/domain-vocab.yaml` 中的术语对照

### 全章写后校验

- 全章所有节写完后，再运行一次 `count_chapter_words.py --budget` 确认全章总字数在预算范围内
- 如果仍超出，定点压缩超出最多的节

### 其他要求

- 如果软件系统/系统设计类正文缺少架构图、E-R 图、关键流程图、数据表、测试用例表或页面截图占位，执行
  `python scripts/figures/ensure_thesis_assets.py <thesis.md> --check-only`
  并在继续写作前确认缺失项是否确实由当前论文范围需要
- 数据库设计部分只有在论文实际包含数据库设计时才要求 E-R 图或等价数据设计证据
- 页面截图数量不设通用下限；按系统功能、论文范围和学校要求决定
- 参考文献必须先核验后回填，不能边猜边写
- 文风应贴近本科论文样文，但避免空泛套话和机械排比
- 如果正文存在截图占位，优先执行：
  `python scripts/screenshots/extract_screenshot_placeholders.py <thesis.md> --json-out labels.json`
  `python scripts/screenshots/build_screenshot_plan.py labels.json paper-context/workflow/screenshot-plan.json --base-url <system-url>`
  `python scripts/screenshots/capture_thesis_screenshots.py paper-context/workflow/screenshot-plan.json`
- 如果正文存在 Mermaid / PlantUML 图，完成主文稿后必须额外生成附件 `.docx`，收录这些图的源码版本
