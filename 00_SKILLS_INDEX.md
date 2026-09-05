# Codex Skills 精简索引与路由规则

本文件是 `/home/ubuntu/.codex/skills` 的按需路由索引，不是默认工作流。全局行为和安全边界以 `/home/ubuntu/.codex/AGENTS.md` 为准。

更新时间：2026-09-05（UTC+8）

## 使用规则

1. 不在每个任务开始时扫描本文件，也不因“可能相关”而加载 skill。
2. 仅在用户明确点名、专有 API/工具流程、高风险交易/钱包操作，或需要 skill 内确定性脚本时查本索引。
3. 先选择一个最窄的领域 skill；确有缺口再追加。禁止叠加通用规划、调试、TDD、审查或验证流程。
4. 本文件只保留稳定路由，不复制 `SKILL.md` 说明。路径或数量冲突时，以真实目录为准并同步修正本文件。
5. 下单、撤单、swap、转账、签名、授权和广播等资金副作用仍须按 `AGENTS.md` 逐项确认。

## 总览

- Skills 总数：68
- 系统管理：6
- 用户/工作区管理：61
- 已移除：通用元流程、重复开发教程、无关行业、创意、泛办公、社交、游戏和媒体类 skills

## 系统管理（6）

不要手工删除或改写 `.system/`：

- `.system/imagegen`
- `.system/openai-docs`
- `.system/plugin-creator`
- `.system/review-agent`
- `.system/skill-creator`
- `.system/skill-installer`

## 加密市场与交易（26）

### Binance

- `binance-funding-monitor`：资金费率筛选与监控
- `binance-monitor-runtime`：持续扫描、评分和 Telegram 推送
- `binance-readonly`：行情、K 线、订单簿、账户和挂单只读查询

### 市场研究

- `crypto-market`：跨交易所、非账户型加密市场研究和历史行情
- `douyin-strategy-doc`：从视频提取并复核可回测交易策略

### OKX

- CEX 行情与账户：`okx/okx-cex-market`、`okx/okx-cex-portfolio`
- CEX 交易与策略：`okx/okx-cex-trade`、`okx/okx-cex-bot`、`okx/okx-cex-earn`、`okx/okx-cex-skill-mp`
- DEX 行情与信号：`okx/okx-dex-market`、`okx/okx-dex-signal`、`okx/okx-dex-token`、`okx/okx-dex-trenches`、`okx/okx-dex-ws`
- DEX 与 DeFi 操作：`okx/okx-dex-swap`、`okx/okx-defi-invest`、`okx/okx-defi-portfolio`
- 钱包与链上：`okx/okx-agentic-wallet`、`okx/okx-wallet-portfolio`、`okx/okx-onchain-gateway`
- 安全、审计与情绪：`okx/okx-security`、`okx/okx-audit-log`、`okx/okx-sentiment-tracker`
- 支付：`okx/okx-x402-payment`

## 研究与文档（6）

- `surf`：明确指定 Surf 或需要跨源、社交、DeFi、钱包、预测市场和链上聚合
- `summarize`：URL、文件、视频和音频摘要
- `research/arxiv`：arXiv 检索与论文获取
- `research/polymarket`：Polymarket 查询
- `pdf`：PDF 读取、提取和处理
- `productivity/ocr-and-documents`：OCR 与文档提取

## 浏览器与网页数据（6）

- `playwright-mcp`：真实浏览器导航、点击、填表、截图和提取
- `webapp-testing`：本地 Web 应用测试
- `dogfood`：探索式网页 QA
- `ecc-imports/browser-qa`：浏览器 QA 流程
- `ecc-imports/data-scraper-agent`：采用其 Python/Gemini/GitHub Actions/外部存储方案的新建定时采集系统
- `ecc-imports/e2e-testing`：端到端测试

## 数据与运行环境（6）

- `data-science/jupyter-live-kernel`：交互式数据分析
- `ecc-imports/clickhouse-io`：ClickHouse 数据工作流
- `ecc-imports/postgres-patterns`：PostgreSQL 模式
- `ecc-imports/database-migrations`：数据库迁移
- `ecc-imports/docker-patterns`：Docker 与容器
- `devops/webhook-subscriptions`：Webhook 订阅

## 链上与代码安全（6）

- `ecc-imports/defi-amm-security`：DeFi / AMM 安全检查
- `ecc-imports/evm-token-decimals`：EVM token decimals 精度保护
- `ecc-imports/llm-trading-agent-security`：LLM 交易代理安全
- `ecc-imports/nodejs-keccak256`：Node.js Keccak-256 正确性
- `ecc-imports/security-review`：安全审查
- `ecc-imports/security-scan`：安全扫描

## 开发集成与恢复（11）

### GitHub

- `github`：`gh` CLI 通用入口
- `github/codebase-inspection`
- `github/github-auth`
- `github/github-code-review`
- `github/github-issues`
- `github/github-pr-workflow`
- `github/github-repo-management`

### MCP

- `mcp-builder`
- `mcp/native-mcp`
- `ecc-imports/mcp-server-patterns`

### 恢复

- `openclaw-backup`：OpenClaw 备份与恢复

## 维护

- 创建、修改或沉淀 skill：使用系统管理的 `.system/skill-creator`。
- 安装缺失 skill：仅在用户明确要求时使用 `.system/skill-installer`。
- 新增、删除或移动 skill 后，重新统计真实 `SKILL.md` 并同步本文件；不要恢复已删除的全量说明和强制路由链。

---

文档版本：3.0
Skills 总数：68
统计口径：`/home/ubuntu/.codex/skills/**/SKILL.md`
