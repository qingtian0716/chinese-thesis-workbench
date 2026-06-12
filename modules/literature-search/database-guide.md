# Database Search Guide

检索操作参考手册。按 `search-plan.md` 拿到关键词后，参考本指南完成检索和下载。

## 知网（CNKI）高级检索

地址：https://kns.cnki.net/kns8/AdvSearch

操作步骤：
1. 选择文献类型：学术期刊 + 学位论文（本科论文默认以这两类为主）
2. 检索字段选"主题"，输入关键词，多个词用 AND 连接
3. 时间范围：按 search-plan.md 的"建议年份"设置
4. 点击"检索"，按"相关度"或"被引"排序
5. 优先阅读摘要判断相关性，再决定是否下载全文
6. 下载格式选 PDF；导出引用格式选"GB/T 7714-2015"

常见问题：
- 搜索结果太多（>200）：在当前结果内继续加词缩小范围
- 搜索结果太少（<5）：去掉 AND 后面的词，只用核心词搜索
- 找不到全文：点击"在线阅读"或"CAJ 下载"，或通过学校图书馆 VPN 访问

## 万方数据

地址：https://www.wanfangdata.com.cn/search/searchList.do

操作基本同知网，适合补充知网找不到的学位论文和会议论文。

## Google Scholar

地址：https://scholar.google.com

基础搜索语法：

```
"blockchain" AND "time bank"          精确短语用引号

"recommender system" -"survey"        减号排除不想要的词

"federated learning" after:2020       限制年份下限

"object detection" site:arxiv.org     限定来源网站
```

操作步骤：
1. 将 search-plan.md 里的英文检索式直接粘贴搜索框
2. 点击左侧"Since 2020"等时间筛选
3. 点击论文标题下方"被引用次数"排序找高引论文
4. 点击"所有 X 个版本"找免费 PDF 下载链接
5. 点击引用图标，选"BibTeX"或"GB/T 7714"格式复制引文

找不到免费 PDF 的处理方式：
- 看作者主页或 ResearchGate 是否有预印本
- 在 arXiv.org 搜索论文题目（适合 AI/CS 领域）
- 通过学校图书馆数据库下载

## IEEE Xplore

地址：https://ieeexplore.ieee.org

适合：软件工程、区块链、物联网、信号处理、通信方向的外文文献

操作步骤：
1. 点击顶部"Advanced Search"
2. 在"Search Terms"输入英文关键词，字段选"All Metadata"
3. 添加"Year"筛选
4. 勾选"Open Access Only"可找免费全文
5. 导出引用选"Citation"→"BibTeX"

## ACM Digital Library

地址：https://dl.acm.org

适合：软件工程、人机交互、数据库、算法方向的外文文献

操作步骤：
1. 在搜索框输入英文关键词
2. 左侧 Publication Date 筛选年份
3. 左侧 ACM Content Type 选 Research Article
4. 部分论文可免费下载 PDF（标注 Open Access）

## 文件整理规范

下载完成后，按以下规范整理文件，方便后续脚本处理：

```
papers/
  zh_区块链_时间银行_作者姓_2023.pdf
  zh_智能合约_安全性分析_作者姓_2022.pdf
  en_blockchain_community_Smith_2021.pdf
  en_smart_contract_formal_verification_Li_2020.pdf
```

命名格式：`语言前缀_关键词1_关键词2_作者姓_年份.pdf`

整理完成后，运行以下命令提取引用信息：

```powershell
python scripts/literature/extract_pdf_references.py ./papers \
  --out paper-context/literature
```

然后可运行覆盖度检查：

```powershell
python scripts/literature-search/validate_coverage.py \
  --plan paper-context/literature/search-plan/search-plan.json \
  --extracted paper-context/literature/reference-extraction.json \
  --out paper-context/literature/search-plan/coverage-report.md
```

## 外文文献不够时的补救策略

如果 L2 英文检索找到的外文文献不足学校要求：

1. 把 L1 的英文检索式也跑一遍 Google Scholar
2. 在 IEEE/ACM 搜索 L3 领域词的英文版本
3. 搜索论文中引用了哪些经典外文综述（在知网看参考文献列表）
4. 如果论文用了开源框架或算法，搜索该框架/算法的原始论文（通常是高引外文）

注意：外文文献不需要全文精读，但引用时必须确认标题、作者、年份、期刊/会议名称真实存在。
