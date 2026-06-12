# Keyword Generation Strategy

Use this reference when generating a literature search plan.
Read this file alongside `search-module.md`.

## Four-Layer Structure

Every search plan must use exactly four layers. Do not collapse or skip layers.

| Layer | Name | Purpose | Typical count |
| --- | --- | --- | --- |
| L1 | 核心主题词 | Direct decomposition of thesis title and core research question | 2–3 groups |
| L2 | 技术方法词 | Academic terms for the specific technologies and methods used | 3–5 groups |
| L3 | 应用领域词 | Background and domain context for Chapter 1 and literature review | 2–3 groups |
| L4 | 对比参照词 | Competing approaches or baseline methods the thesis compares against | 1–2 groups |

## L1 Rules: Core Topic Keywords

- Do not simply split the thesis title into individual words.
  Identify the **semantic core**: what is the real research question behind the title?
- Always generate both a narrow query (precise, fewer results) and a broad query
  (wider coverage) for each group.
- Example for "基于区块链的时间银行社区服务平台":
  - Narrow: `区块链 AND 时间银行`
  - Broad: `区块链 AND 社区服务`
  - English narrow: `"blockchain" AND "time bank"`
  - English broad: `"blockchain" AND "community service"`
- L1 groups map primarily to Chapter 1 (research background and status)
  and the abstract.

## L2 Rules: Technical Method Keywords

- Never use product or framework names as academic search terms.
  Map them to their academic equivalents:

  | User says | Use in search |
  | --- | --- |
  | Spring Boot | 微服务架构 / microservice architecture |
  | Vue.js / React | 前后端分离 / single-page application |
  | MySQL / PostgreSQL | 关系型数据库设计 / relational database design |
  | Redis | 缓存机制 / distributed caching |
  | Docker / K8s | 容器化部署 / containerized deployment |
  | BERT / GPT | 预训练语言模型 / pre-trained language model |
  | YOLO / ResNet | 目标检测 / object detection |
  | Random Forest / SVM | 集成学习 / ensemble learning |
  | Solidity / Web3 | 智能合约 / smart contract |
  | Hyperledger | 联盟链 / permissioned blockchain |

- L2 groups map primarily to Chapter 2 (related technology) and
  Chapter 3/4 (design and implementation).
- L2 English queries are the most likely to yield high-quality foreign
  literature from IEEE Xplore and ACM DL. Flag these explicitly.

## L3 Rules: Application Domain Keywords

- Identify the **application scenario** and **social/industry context**
  of the thesis, which often requires background literature beyond the
  technical domain.
- Examples:
  - A blockchain community service system → also needs literature on
    `社区养老 / community elderly care`, `互助经济 / mutual aid economy`,
    `社会信任 / social trust`
  - A medical image classification system → also needs literature on
    `医学图像处理 / medical image processing`, `辅助诊断 / computer-aided diagnosis`
  - An e-commerce recommendation system → also needs literature on
    `用户行为分析 / user behavior analysis`, `个性化推荐 / personalized recommendation`
- L3 literature often skews older (2015–present is acceptable).
  This is where the non-recent-five-years quota gets used.
- L3 groups map primarily to Chapter 1 (research significance and background).

## L4 Rules: Comparative Reference Keywords

- Identify what the thesis is **replacing or improving upon**.
  These are the baseline systems or methods that justify the thesis's contribution.
- Examples:
  - A blockchain system → compare against `中心化数据库方案 / centralized database`,
    `传统积分系统 / traditional point system`
  - A deep learning model → compare against `传统机器学习方法 / traditional ML`,
    `手工特征工程 / manual feature engineering`
- L4 literature is often older and is used to establish the "gap" the
  thesis fills. Keep L4 count small (2–4 papers total).
- L4 groups map primarily to Chapter 1 (problem statement and motivation).

## Query Format Rules

Every keyword group must include:

```
中文检索式：[可直接粘贴进知网高级检索的表达式]

英文检索式：[可直接粘贴进 Google Scholar / IEEE 的表达式]

对应章节：第X章 XXXX

推荐数据库：[知网 / 万方 / Google Scholar / IEEE Xplore / ACM DL]

建议年份：[YYYY–至今 或 YYYY–YYYY]

目标篇数：X篇

为什么有效：[一句话说明这组词为何切中论文需要]
```

## Count Distribution Rules

Given total requirement N, foreign minimum F, and recent-years ratio R:

1. Assign target counts to layers so that L1 + L2 + L3 + L4 ≥ N.
   Suggest 10–15% buffer above N to account for duplicates and irrelevant results.
2. Mark which layers are most likely to yield foreign-language papers.
   Typically L2 English queries on IEEE/ACM yield the highest-quality foreign papers.
   Target F papers from L2 English queries first.
3. Distribute year targets:
   - L1 + L2: target year ≥ recent_years_cutoff (default 2020) for ≥ R of total
   - L3: can use 2015–present
   - L4: no year restriction, but keep count small
4. State explicitly which groups cover the "近五年" requirement and which
   cover the "外文文献" requirement. Do not leave this implicit.

## Venue Guidance by Domain

Tell the user which databases are most productive for their domain:

| Domain | Best Chinese DB | Best English DB | Key venues |
| --- | --- | --- | --- |
| 软件工程 / 系统设计 | 知网 | IEEE Xplore, ACM DL | TSE, ICSE, FSE |
| 人工智能 / 机器学习 | 知网 | Google Scholar, arXiv | NeurIPS, ICML, CVPR |
| 区块链 / 分布式系统 | 知网, 万方 | IEEE Xplore | IEEE Blockchain, ICDCS |
| 数据库 / 数据挖掘 | 知网 | ACM DL | SIGMOD, VLDB, KDD |
| 物联网 / 嵌入式 | 知网, 维普 | IEEE Xplore | IoT-J, IPSN |
| 医疗信息 / 健康管理 | 知网, 万方 | PubMed, IEEE | JAMIA, JBHI |
| 教育技术 | 知网, 万方 | ERIC, Google Scholar | BJET, CHI |
| 社会科学 / 管理 | 知网, 万方 | Google Scholar | MISQ, JMIS |

If the domain is not listed, infer from the thesis type and tech stack.
