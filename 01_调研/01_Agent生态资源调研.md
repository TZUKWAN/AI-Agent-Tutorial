# AI Agent 生态资源调研报告

> **项目**：《AI Agent 零基础工作方法教程》生态调研子任务
> **基准日期**：2026-09-18
> **调研方法**：联网检索 + 官方文档/源仓库交叉核验；所有 URL 均为本次调研期间实际访问到的真实链接
> **重要声明**：
> - GitHub Star 数仅作活跃度记录，**不**作为安全或质量证据
> - 聚合站的数量/排名/评分**不**作为质量事实
> - "Official" 开头的社区站**不等于**厂商官方站
> - 同名 SkillHub 已逐一区分
> - 所有条目均标注"核验日期：2026-09-18"

---

## 目录

- [A. 官方标准与规范（Tier A）](#a-官方标准与规范tier-a)
- [B. Skill 发现平台/目录（Tier B）](#b-skill-发现平台目录tier-b)
- [C. GitHub Skill 仓库（Tier A/D）](#c-github-skill-仓库tier-ad)
- [D. MCP Registry / Directory / 托管平台（Tier B/C）](#d-mcp-registry--directory--托管平台tier-bc)
- [E. Tool / Connector / Integration 平台（Tier C）](#e-tool--connector--integration-平台tier-c)
- [F. Workflow / Automation 平台（Tier C/D）](#f-workflow--automation-平台tier-cd)
- [G. Coding Agent 生态（Tier A/C）](#g-coding-agent-生态tier-ac)
- [H. Agent Framework / SDK（Tier A/C）](#h-agent-framework--skdtier-ac)
- [I. 学术与评测资源（Tier A/D）](#i-学术与评测资源tier-ad)
- [附录：已标注 deprecated / 过时资源](#附录已标注-deprecated--过时资源)

---

## A. 官方标准与规范（Tier A）

> 这一类是"地基"：所有 Skill、MCP、Plugin 的格式和协议都由这里定义。教程正文必须以这些官方源为准。

### A1. Anthropic Agent Skills 开放标准（SKILL.md 格式）
- **一句话说明**：由 Anthropic 发起、2025-10 首次公布、2026-01 作为开放标准发布的"技能包"格式；一个 Skill 就是一个含 `SKILL.md` 的目录，YAML frontmatter 必须含 `name` 与 `description`，正文是 Markdown 指令，可附 `scripts/`、`references/`、`assets/`。
- **关键事实**：
  - 2026-01-22 Anthropic 博客宣布"Agent Skills as an open standard"，目标是跨工具/跨平台可移植
  - 与 MCP 并列被定位为 Anthropic 推动的两大开放标准之一
  - 渐进式加载（progressive disclosure）：启动时只加载 name+description，相关时才加载全文
- **证据 URL**：
  - https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
  - https://claude.com/blog/building-agents-with-skills-equipping-agents-for-specialized-work
  - https://www.anthropic.com/news/skills
- **核验日期**：2026-09-18

### A2. agentskills.io —— 社区维护的 Agent Skills 规范站点
- **一句话说明**：独立于 Anthropic 的社区规范站点，维护 SKILL.md 的字段约束（name ≤64 字符、description ≤1024 字符等），被多家 Coding Agent 实现引用为事实标准。
- **关键事实**：
  - 规范页：name 仅允许小写字母/数字/连字符；license、compatibility、metadata 为可选字段
  - 被 LangChain、多个开源 Agent SDK 引用
  - 注意：这是**社区/中立标准站点**，不是 Anthropic 官方；Anthropic 官方文档在 platform.claude.com
- **证据 URL**：https://agentskills.io/specification ；https://agentskills.io/home
- **核验日期**：2026-09-18

### A3. Model Context Protocol（MCP）官方规范
- **一句话说明**：2024-11 由 Anthropic 发起并开源的开放协议，定义 Host/Client/Server 三方基于 JSON-RPC 2.0 的通信；2026-07-28 发布迄今最大修订版（无状态核心、MCP Apps UI 扩展、Tasks 长任务扩展、OAuth/OIDC 对齐）。
- **关键事实**：
  - 官方文档站 modelcontextprotocol.io，规范有版本号（2025-03-26、2025-11-25、2026-07-28 等）
  - 2026-08 发布新路线图：传输演进、Agent 通信、治理成熟、企业就绪
  - 灵感来自 Language Server Protocol（LSP）
- **证据 URL**：https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro ；https://blog.modelcontextprotocol.io/posts/mcp-roadmap/
- **核验日期**：2026-09-18

### A4. MCP 官方 Registry
- **一句话说明**：2025-09-08 上线的官方 MCP Server 元数据注册中心，由 Anthropic、GitHub、PulseMCP、Microsoft 等共同背书；提供命名空间 DNS 校验、REST API、标准化安装配置。
- **关键事实**：
  - 生产环境：registry.modelcontextprotocol.io；另有 staging
  - 开源，允许构建兼容子注册表
  - 2026-09 仍活跃，每日有新 server 提交
- **证据 URL**：https://modelcontextprotocol.io/registry/about ；https://registry.modelcontextprotocol.io/ ；https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/
- **核验日期**：2026-09-18

### A5. Claude Code 官方文档（Plugins / Skills / Hooks / Marketplace）
- **一句话说明**：Anthropic 官方 Coding Agent Claude Code 的文档站，定义了 Plugin 包格式（含 skills/、commands/、hooks/、MCP 配置）与两个官方公共 marketplace（claude-plugins-official 等）。
- **关键事实**：
  - Plugin 可包含 skills/ 目录或单个 SKILL.md
  - Hook 通过 stdin 接收 JSON，用 jq 提取参数
  - 官方 marketplace 首次交互式启动时自动注册
- **证据 URL**：https://code.claude.com/docs/en/plugins ；https://code.claude.com/docs/en/plugin-marketplaces
- **核验日期**：2026-09-18

### A6. OpenAI Codex CLI 与 AGENTS.md 约定
- **一句话说明**：OpenAI 开源的终端 Coding Agent，仓库 github.com/openai/codex；通过 `AGENTS.md` 文件（个人 `~/.codex/AGENTS.md` + 项目根 `AGENTS.md` 自上而下合并）注入上下文。
- **关键事实**：
  - 2026-01 OpenAI 发布"Unrolling the Codex agent loop"技术博客
  - 2026-03 发布 Codex app；2026-09-10 发布 Agents API（Codex harness 云端托管）
  - AGENTS.md 已成为跨厂商事实约定（Codex、Gemini CLI、OpenCode 等都支持）
- **证据 URL**：https://github.com/openai/codex ；https://openai.com/index/unrolling-the-codex-agent-loop/ ；https://learn.microsoft.com/azure/foundry/openai/how-to/codex
- **核验日期**：2026-09-18

### A7. Google Gemini CLI 官方文档（Extensions / Skills / GEMINI.md）
- **一句话说明**：Google 开源终端 Agent，官方文档站 geminicli.com；Extensions 是官方扩展包格式，捆绑 MCP 配置、GEMINI.md 上下文、skills/ 目录。
- **关键事实**：
  - User skills 位于 `~/.gemini/skills/` 或 `~/.agents/skills/`；Workspace skills 位于 `.gemini/skills/`
  - 支持 subagents（可通过 `enableAgents: false` 关闭）
  - 有 Policy Engine 做工具级 deny 规则
- **证据 URL**：https://geminicli.com/docs/cli/skills/ ；https://geminicli.com/docs/extensions/reference/ ；https://codelabs.developers.google.com/getting-started-gemini-cli-extensions
- **核验日期**：2026-09-18

### A8. Microsoft / GitHub Copilot Agent Skills 官方文档
- **一句话说明**：GitHub Copilot（VS Code、Visual Studio、Copilot CLI、cloud agent）已原生支持开放 Agent Skills 标准，workspace skills 放在 `.github/skills/`、`.claude/skills/`、`.agents/skills/`；个人 skills 在 `~/.copilot/skills/`。
- **关键事实**：
  - VS Code 文档明确"Agent Skills is an open standard that works across multiple AI agents"
  - Visual Studio Insider 2026 新增 Skills 面板
  - Copilot CLI 有 `/plugin marketplace add`、`/plugin install` 命令族
- **证据 URL**：https://code.visualstudio.com/docs/copilot/customization/agent-skills ；https://learn.microsoft.com/visualstudio/ide/copilot-agent-skills
- **核验日期**：2026-09-18

### A9. OpenAI Plugin Directory（替代旧 App Directory / openai/skills）
- **一句话说明**：2026-07-09 OpenAI 将 App Directory 迁移为 Plugin Directory；Plugin 可打包 skills、apps、app templates；这是 openai/skills 仓库 deprecated 后的官方继任入口。
- **关键事实**：
  - 2026-06-22 openai/skills README 标注 deprecated，指向 Codex 文档
  - 企业/Edu 用户在 Plugins 侧栏的 Skills tab 查找
  - 支持从 GitHub 导入/同步 plugin marketplace（JSON catalog）
- **证据 URL**：https://help.openai.com/（Apps in ChatGPT 更新说明，2026-09-11）；https://agentconn.com/blog/openai-skills-catalog-directory-threat/
- **核验日期**：2026-09-18

### A10. Microsoft Agent Framework 官方文档
- **一句话说明**：2025-10 发布、2026-04 v1.0 的微软统一 Agent SDK，合并 AutoGen 与 Semantic Kernel；支持 Agent、Harness Agent、Functional/Graph Workflows，原生对接 MCP。
- **关键事实**：
  - GitHub: github.com/microsoft/agent-framework（MIT）
  - 支持 Microsoft Foundry、Anthropic、Azure OpenAI、OpenAI、Ollama
  - 可直接把 GitHub Copilot SDK 或 Claude Code 作为 harness
- **证据 URL**：https://learn.microsoft.com/agent-framework/overview/ ；https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/
- **核验日期**：2026-09-18

---

## B. Skill 发现平台/目录（Tier B）

> 这一类用于"找 Skill"。**注意：聚合站只用于发现，安装前必须回到源仓库审计。**

### B1. SkillsMP（skillsmp.com）
- **一句话说明**：最大的公开 SKILL.md 聚合搜索站之一，索引 GitHub 上 239 万+ SKILL.md 文件，覆盖 Claude Skills、Claude Code、Codex、ChatGPT agent skills。
- **关键事实**：
  - 自称 71,000+ skills（不同时间点口径不同：2026-06 显示 2,396,488 collected files）
  - 支持按作者、职业（SOC job roles）、分类浏览
  - 平台自身明确**不认证**质量和安全性
- **证据 URL**：https://skillsmp.com/ ；https://skillsmp.com/pt
- **核验日期**：2026-09-18

### B2. skills.sh（Vercel 出品）
- **一句话说明**：Vercel 于 2026-01-20 推出的 Agent Skills 目录 + leaderboard，配套开源 CLI `npx skills add <owner>/<repo>`；被称"Agent Skills 的 npm"。
- **关键事实**：
  - CLI 开源：github.com/vercel-labs/skills
  - 支持 20+ Agent：Claude Code、Cursor、Copilot、Codex、Kiro CLI、OpenCode、Antigravity 等
  - 自动识别仓库中 skills/、.agents/skills/、.claude/skills/、.claude-plugin/marketplace.json
  - 有 `/api/v1/skills/curated` 返回"官方一手 skills"
- **证据 URL**：https://skills.sh/ ；https://skills.sh/docs ；https://skills.sh/docs/api
- **核验日期**：2026-09-18

### B3. SkillHub.club
- **一句话说明**：AI 评估过的 Skill 市场，覆盖 Claude Code、Codex、Gemini CLI、OpenCode、OpenClaw 5 个平台；115.3K published skills、65 categories。
- **关键事实**：
  - 提供 quality/security signals 对比
  - 有付费 Premium Skill Stacks（如 Garry Tan 的 Startup CEO Stack）
  - 2026-07-16 更新 catalog
- **证据 URL**：https://www.skillhub.club/
- **核验日期**：2026-09-18

### B4. AgentSkillsHub（agentskillshub.dev）
- **一句话说明**：安全分级的 MCP server + AI agent skills 目录，索引 156,000+ GitHub 仓库，每 8 小时刷新；给每个仓库打 SAFE/CAUTION/UNSAFE/UNAUDITED 等级。
- **关键事实**：
  - 10 维加权质量分（0-100）：维护频率、文档深度、代码质量、社区验证、安全红旗等
  - 支持粘贴任意 GitHub 链接做实时安全审计
  - 注意域名是 **agentskillshub.dev**（不是 agentskillhub.dev）
- **证据 URL**：https://agentskillshub.dev/ ；https://aitoolly.com/product/agent-skills-hub
- **核验日期**：2026-09-18

### B5. officialskills.sh
- **一句话说明**：**社区项目**，是 awesome-agent-skills GitHub 仓库的可浏览前端；581+ 个由"实际写产品的厂商团队"发布的官方 skill（Microsoft、OpenAI、Anthropic、Google 等），48 个 dev teams、9 个分类。
- **关键事实**：
  - ⚠️ **名称含 "Official" 但不是厂商官方平台**，是社区 curated 目录
  - 只收录厂商一手团队发布的 skill，不收 AI 批量生成的 filler
- **证据 URL**：https://www.everydev.ai/tools/official-agent-skills/llms.txt ；https://agentify.ia.br/blog/officialskills-sh
- **核验日期**：2026-09-18

### B6. agskills.dev
- **一句话说明**：另一个 Agent Skills Marketplace，索引 published SKILL.md workflow，按 owner/repo 组织，提供 `npx skills add <url> --skill <name>` 安装命令。
- **关键事实**：
  - 明确提示"This repository contains Anthropic's implementation of skills for Claude. For information about the Agent Skills standard, see agentskills.io"
  - 分页浏览（386+ 页），规模可观
- **证据 URL**：https://agskills.dev/ ；https://agskills.dev/anthropics/skills/skill-creator
- **核验日期**：2026-09-18

### B7. agentskills.codes
- **一句话说明**：自称"installable skills 的开放 registry"，19,296 个 skills，每日扫描；支持一行命令安装到主流 coding agent。
- **关键事实**：
  - 免费开源
  - 定位与 skills.sh 类似，但独立项目
- **证据 URL**：https://agentskills.codes/
- **核验日期**：2026-09-18

### B8. agentskills.me
- **一句话说明**：另一个 Agent Skills 发现站，按技术领域（Convex、diagram-as-code 等）组织。
- **关键事实**：社区项目，与 agentskills.io（规范站）、agentskills.codes（registry）不同名
- **证据 URL**：https://agentskills.me/
- **核验日期**：2026-09-18

### B9. SkillMD.ai（skillmd.ai）
- **一句话说明**：围绕 SKILL.md 生态的教程+资源站，提供"如何构建 skill"指南和资源侦察（resource-scout）skill 本身。
- **关键事实**：
  - 自身也是一个"教你怎么找 skill 的 skill"
  - 整理了 SkillsMP、SkillHub.club、Claude Skills Hub 等来源对比表
- **证据 URL**：https://skillmd.ai/how-to-build/resource-scout/
- **核验日期**：2026-09-18

### B10. skillhub.lol
- **一句话说明**：raw public skills 的"更干净"市场层，outcome-first 导航；12 skills、7 maintainers、656.1K stars 总量。
- **关键事实**：保留原始来源链接，强调按结果而非仓库名找 skill
- **证据 URL**：https://skillhub.lol/
- **核验日期**：2026-09-18

### B11. agentskill.sh
- **一句话说明**：Claude Code plugin marketplace，主打 `/learn` 命令——让 agent 从使用中学习新技能。
- **关键事实**：
  - 安装方式：`/plugin marketplace add https://agentskill.sh/marketplace.json`
  - 要求 Claude Code ≥ 1.0.33
- **证据 URL**：https://agentskill.sh/install
- **核验日期**：2026-09-18

### B12. Tessl Skills Registry（tessl.io/registry）
- **一句话说明**：Tessl 平台的 skills registry，按 GitHub org/repo 组织（如 huggingface/skills），标注最近更新时间。
- **关键事实**：每个 skill 页展示 SKILL.md 内容和最后更新时间
- **证据 URL**：https://tessl.io/registry/skills/github/huggingface/skills
- **核验日期**：2026-09-18

### B13. SkillsLLM（skillsllm.com）
- **一句话说明**：第三方 skill 索引站，给每个 skill 打安全分、可靠性分、af_score；如 iflytek/skillhub 条目显示 5,093 GitHub stars。
- **关键事实**：聚合站，事实需回源仓库核验
- **证据 URL**：https://skillsllm.com/skill/skillhub
- **核验日期**：2026-09-18

### B14. skills.aiproducthub.cn（中文 SkillHub）
- **一句话说明**：AI 产品库旗下中文 Skill 收录平台，面向中文用户，收录 AI Skills、Agents、Plugins。
- **关键事实**：中文界面，适合国内用户发现
- **证据 URL**：https://skills.aiproducthub.cn/
- **核验日期**：2026-09-18

### B15. claude skills info / claudeskills.info
- **一句话说明**：UI 友好的 Claude Skills 浏览站（被 SkillMD.ai 资源侦察文档列为主要来源之一）。
- **关键事实**：聚合站，需回源
- **证据 URL**：https://skillmd.ai/how-to-build/resource-scout-1/（引用 claudeskills.info）
- **核验日期**：2026-09-18

### B16. skillget.dev
- **一句话说明**：skill 目录+扫描状态展示（如 travisvn/awesome-claude-skills 标注 "Warn" 扫描状态）。
- **关键事实**：提供 scan status、贡献指南
- **证据 URL**：https://skillget.dev/listings/travisvn-awesome-claude-skills
- **核验日期**：2026-09-18

---

## C. GitHub Skill 仓库（Tier A/D）

> ⚠️ 同名项目必须区分；Star 数仅记录，不作质量证据。

### C1. anthropics/skills（官方）
- **一句话说明**：Anthropic 官方 Skill 仓库，含文档类生产 skill（Word/PDF/PPT/Excel，source-available 许可）和示例 skill（创意设计、开发、MCP builder、webapp-testing 等）。
- **关键事实**：
  - Apache 2.0（示例部分）；文档 skills 为 source-available，商业使用有限制
  - 含 skill-creator skill（也内置在 Claude.ai 和 Claude Code）
  - 安装：`git clone https://github.com/anthropics/skills ~/.claude/skills/`
- **证据 URL**：https://github.com/anthropics/skills ；https://www.anthropic.com/news/skills
- **核验日期**：2026-09-18

### C2. openai/skills（⚠️ 已 deprecated）
- **一句话说明**：OpenAI 曾发布的 skills 仓库，2026-06-22 README 标注 deprecated，指向 Codex 官方文档；技能体系迁移到托管 Plugin Directory。
- **关键事实**：
  - 2026-09-07 曾因 deprecated 上 GitHub Trending
  - 教程**不应**再照抄旧安装方法
- **证据 URL**：https://github.com/openai/skills ；https://agentconn.com/blog/openai-skills-catalog-directory-threat/
- **核验日期**：2026-09-18

### C3. openai/plugins（⚠️ 旧 Plugins 仓库，已被 Plugin Directory 取代）
- **一句话说明**：OpenAI 早期 ChatGPT plugins 仓库；ChatGPT plugins beta（2023-03）已迁移为 GPTs actions，后又演进为 2026-07 的 Plugin Directory。
- **关键事实**：旧仓库内容已过时，教程需以最新 Plugin Directory 文档为准
- **证据 URL**：https://github.com/openai/plugins
- **核验日期**：2026-09-18

### C4. huggingface/skills（官方）
- **一句话说明**：Hugging Face 官方 Skill 仓库，9 个 ML 工作流 skill（hf-cli、model-trainer、best-model 选择、community evals、Gradio 等）。
- **关键事实**：
  - 支持 `pip install -e ./skills` 或 `gemini extensions install .`
  - 与 HF Hub、Spaces、Skills-over-MCP 发现流集成
- **证据 URL**：https://github.com/huggingface/skills ；https://ubos.tech/news/hugging-face-launches-open-source-agent-skills-repository-for-next-gen-ai-agents/
- **核验日期**：2026-09-18

### C5. microsoft/skills（官方）
- **一句话说明**：Microsoft 官方 Skill 仓库，配合 GitHub Copilot / VS Code / Visual Studio 使用；Skills for Fabric 等企业集成为代表。
- **关键事实**：
  - workspace skills 约定 `.github/skills/`
  - Skills for Fabric 通过 Copilot CLI 或 Claude Code 安装
- **证据 URL**：https://learn.microsoft.com/visualstudio/ide/copilot-agent-skills ；https://learn.microsoft.com/fabric/fundamentals/skills-for-fabric-install
- **核验日期**：2026-09-18

### C6. NVIDIA/skills（官方）
- **一句话说明**：NVIDIA 官方 Skill 仓库，被多个开源 agent（如 NousResearch/hermes-agent）列为默认 tap 之一。
- **关键事实**：在 hermes-agent 文档中与 openai/skills、anthropics/skills、huggingface/skills 并列默认源
- **证据 URL**：http://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/features/skills.md
- **核验日期**：2026-09-18

### C7. travisvn/awesome-claude-skills
- **一句话说明**：社区 curated Claude Code skills 列表，按分类组织，约 10K-14K stars（不同来源口径）。
- **关键事实**：持续更新；被多个教程列为入门起点
- **证据 URL**：https://github.com/travisvn/awesome-claude-skills
- **核验日期**：2026-09-18

### C8. ComposioHQ/awesome-claude-skills
- **一句话说明**：Composio 团队维护的大型 community skills 列表，约 66K stars（2026-05 数据）。
- **关键事实**：第三方审计指出其"多为链接索引 + 一家公司平台 skill"，且 2026-05 后更新放缓
- **证据 URL**：https://tellian.io/tag/mcp/
- **核验日期**：2026-09-18

### C9. hesreallyhim/awesome-claude-code
- **一句话说明**：覆盖 Claude Code 全生态的 awesome list：skills、hooks、slash commands、MCP servers、plugins，含可搜索 CSV。
- **关键事实**：比单一 skills 列表更广
- **证据 URL**：https://github.com/hesreallyhim/awesome-claude-code
- **核验日期**：2026-09-18

### C10. VoltAgent/awesome-agent-skills
- **一句话说明**：13,400+ stars 的跨 Agent skills 列表，1,000+ skills 兼容 Claude Code、Codex、Gemini CLI、Cursor。
- **关键事实**：跨平台兼容是卖点
- **证据 URL**：https://github.com/VoltAgent/awesome-agent-skills
- **核验日期**：2026-09-18

### C11. sickn33/antigravity-awesome-skills
- **一句话说明**：registry 式组织的 1,400+ agentic skills 库，含 installer CLI、bundles、workflows。
- **关键事实**：兼容 Claude Code、Cursor、Codex CLI、Gemini CLI、Antigravity
- **证据 URL**：https://github.com/sickn33/antigravity-awesome-skills
- **核验日期**：2026-09-18

### C12. vercel-labs/skills
- **一句话说明**：Vercel Labs 官方 skills 仓库，是 skills.sh CLI 的数据源；自称 900K+ weekly installs。
- **关键事实**：skills.sh 的官方源仓库
- **证据 URL**：https://skillsmp.com/creators/kevin-liu-01/agent-machines/knowledge-skills-find-skills（引用 vercel-labs/skills）
- **核验日期**：2026-09-18

### C13. github/copilot-plugins
- **一句话说明**：GitHub 官方 Copilot plugins marketplace 源仓库，通过 `/plugin marketplace add github/copilot-plugins` 添加。
- **关键事实**：含 advanced-security 等官方 plugin
- **证据 URL**：https://github.blog/changelog/2026-05-11-secret-scanning-with-github-mcp-server-is-now-generally-available/
- **核验日期**：2026-09-18

### C14. openai/codex
- **一句话说明**：OpenAI 官方 Codex CLI 开源仓库，定义 AGENTS.md、sandbox、agent loop。
- **关键事实**：2026-01 技术博客公开设计决策
- **证据 URL**：https://github.com/openai/codex
- **核验日期**：2026-09-18

### C15. google-gemini/gemini-cli
- **一句话说明**：Google 官方 Gemini CLI 开源仓库，含 extensions、skills、subagents、policy engine 文档。
- **关键事实**：文档在 docs/extensions/、docs/cli/skills/
- **证据 URL**：https://github.com/google-gemini/gemini-cli
- **核验日期**：2026-09-18

### C16. iflytek/skillhub（讯飞开源，同名 SkillHub 之一）
- **一句话说明**：科大讯飞 2026-03-15 开源的**企业级自托管 Skill 注册中心**，面向企业私有技能市场；支持语义版本、team namespace、RBAC、审计日志，Docker/K8s 部署。
- **关键事实**：
  - ⚠️ **这是同名 SkillHub 之一**，与 skillhub.club（公网市场）、io-oi-ai/Skillhub、CassianFlorin/skill-hub（Go CLI）都不同
  - 在线实例：skill.xfyun.cn（Astron SkillHub）
  - 约 5,093 GitHub stars
- **证据 URL**：https://opensource.iflytek.com/blog/skillhub-release-announcement ；https://github.com/iflytek/skillhub ；https://skill.xfyun.cn/
- **核验日期**：2026-09-18

### C17. io-oi-ai/Skillhub
- **一句话说明**：种子列表中提到的另一个同名 SkillHub 仓库；本次检索未在公网搜索结果中直接命中其 README 主体，需在教程写作阶段直接访问 GitHub 复核。
- **关键事实**：⚠️ 同名项目，需与 iflytek/skillhub、skillhub.club 严格区分
- **证据 URL**：https://github.com/io-oi-ai/Skillhub
- **核验日期**：2026-09-18（标记为待二次复核）

### C18. MeteorsLiu/skillhub-mvp
- **一句话说明**：另一个 skillhub-mvp 项目，含 agent-facing guidance 文档，教 host 如何发现和加载 SkillHub skills。
- **关键事实**：社区 MVP 项目
- **证据 URL**：https://github.com/MeteorsLiu/skillhub-mvp
- **核验日期**：2026-09-18

### C19. agentskills/agentskills（规范参考实现）
- **一句话说明**：agentskills.io 背后的 GitHub org，含 skills-ref 参考库。
- **关键事实**：规范站的代码/参考实现
- **证据 URL**：https://github.com/agentskills/agentskills
- **核验日期**：2026-09-18

---

## D. MCP Registry / Directory / 托管平台（Tier B/C）

### D1. 官方 MCP Registry（registry.modelcontextprotocol.io）
- 见 A4，Tier A。

### D2. Glama（glama.ai）
- **一句话说明**：自称"官方 MCP Registry 的超集"，每个 server 经 maintainer-verified、持续重建、质量/安全打分；支持浏览器内测试、本地安装、一键部署。
- **关键事实**：2026-09-17 索引显示 88,663 MCP servers、21,861 connectors、831,075 tools
- **证据 URL**：https://glama.ai/
- **核验日期**：2026-09-18

### D3. Smithery（smithery.ai）
- **一句话说明**：MCP server 发现/部署/管理平台，提供 CLI（`smithery mcp search/publish/update`）、托管远程 server、managed OAuth。
- **关键事实**：约 7,000-7,300 servers；支持 .mcpb bundle 发布
- **证据 URL**：https://smithery.ai/ ；https://smithery.ai/docs/concepts/cli.md
- **核验日期**：2026-09-18

### D4. PulseMCP（pulsemcp.com）
- **一句话说明**：创始人每日人工审核的高质量 MCP server 目录，约 11,840-14,900 servers（不同时点），记录周访客估计数、official vs community 分类。
- **关键事实**：MCPZoo 数据集六大来源之一
- **证据 URL**：https://www.automationswitch.com/ai-workflows/where-to-find-mcp-servers-2026
- **核验日期**：2026-09-18

### D5. mcp.so
- **一句话说明**：社区驱动的第三方 MCP server 收集平台，最小审核、按服务组织。
- **关键事实**：MCPZoo 数据集来源之一
- **证据 URL**：https://mcpserver.cc/directory
- **核验日期**：2026-09-18

### D6. MCP Servers.org（mcpservers.org）
- **一句话说明**：wong2 维护的 awesome MCP servers 社区目录，约 2,402 servers；分官方/vendor/community 三类。
- **关键事实**：一键 "Add to Cursor"、复制 JSON for Claude
- **证据 URL**：https://mcpservers.org/
- **核验日期**：2026-09-18

### D7. Cursor Directory（cursor.directory）
- **一句话说明**：面向 Cursor 用户的 MCP/插件目录，开发者发布 server 触达 250K+ 月活 Cursor 用户。
- **关键事实**：客户端画廊类，非通用 registry
- **证据 URL**：https://cursor.directory/
- **核验日期**：2026-09-18

### D8. MCP Repository（mcprepository.com）
- **一句话说明**：MCP server 目录，约 13,596 servers；PulseMCP 团队在其上维护自己的 server。
- **关键事实**：MCPZoo 数据集来源之一
- **证据 URL**：https://mcprepository.com/
- **核验日期**：2026-09-18

### D9. mcprepository.net
- **一句话说明**：另一个 MCP server 搜索/学习中心，提供专业托管解决方案。
- **关键事实**：与 mcprepository.com 不同站点，注意区分
- **证据 URL**：https://mcprepository.net/about/
- **核验日期**：2026-09-18

### D10. ModelScope MCP Marketplace（modelscope.cn/mcp）
- **一句话说明**：阿里 ModelScope 的中文 MCP 市场，约 5,441 servers（2025 年论文数据）。
- **关键事实**：面向中文开发者
- **证据 URL**：https://arxiv.org/pdf/2503.23278（引用 modelscope.cn/mcp）
- **核验日期**：2026-09-18

### D11. Docker MCP Catalog
- **一句话说明**：Docker 官方维护的容器化、安全扫描过的 MCP server 市场。
- **关键事实**：容器化+安全扫描是差异化点
- **证据 URL**：https://designrevision.com/blog/best-mcp-marketplaces-and-registries
- **核验日期**：2026-09-18

### D12. Pipedream MCP（mcp.pipedream.com）
- **一句话说明**：Pipedream 把每个 SaaS app 的 action 暴露为 MCP tool；静态 URL `https://mcp.pipedream.net/v2`，按用户 ID 解析 OAuth。
- **关键事实**：详见 E2
- **证据 URL**：https://mcp.pipedream.com/
- **核验日期**：2026-09-18

---

## E. Tool / Connector / Integration 平台（Tier C）

### E1. Composio（composio.dev）
- **一句话说明**：AI-native agent 集成平台，850-1000+ 预构建 connector，统一管理 OAuth、工具发现、路由、权限；提供 MCP Gateway（connect.composio.dev/mcp）暴露 7 个 meta-tool。
- **关键事实**：
  - 支持 Gmail、Notion、Slack、GitHub、Linear、HubSpot、Strava 等
  - SDK + CLI + hosted MCP endpoint
  - 避免把数千 tool definition 同时塞进模型上下文
- **证据 URL**：https://composio.dev/ ；https://docs.composio.dev/docs/composio-connect
- **核验日期**：2026-09-18

### E2. Pipedream（pipedream.com / mcp.pipedream.com）
- **一句话说明**：开发者自动化平台，数千 app 的 action 库；每个 app 的 action 自动暴露为 MCP tool，ChatGPT/Claude 等 MCP client 可直接接入。
- **关键事实**：
  - 静态 MCP URL：https://mcp.pipedream.net/v2
  - 按 end-user ID 解析账号，你不存 token
  - 也有传统 workflow 自动化能力
- **证据 URL**：https://pipedream.com/ ；https://mcp.pipedream.com/configuration
- **核验日期**：2026-09-18

### E3. Zapier（zapier.com）
- **一句话说明**：9,000+ app 的云自动化平台；2026 年提供 Zapier MCP，让 ChatGPT/Claude/Cursor 等 agent 通过 MCP 访问全部 9,000+ actions；有 AI Guardrails 和 human-in-the-loop。
- **关键事实**：
  - SOC 2 Type II / SOC 3 / GDPR / CCPA
  - Professional $19.99/月起
  - 非技术用户最易上手
- **证据 URL**：https://zapier.com/compare ；https://zapier.com/compare/zapier-vs-make
- **核验日期**：2026-09-18

### E4. GitHub MCP Server
- **一句话说明**：GitHub 官方 MCP server，2026-05 secret scanning with GitHub MCP Server GA；Copilot CLI 中通过 `/plugin install advanced-security@copilot-plugins` 安装。
- **关键事实**：官方一手 GitHub 数据访问
- **证据 URL**：https://github.blog/changelog/2026-05-11-secret-scanning-with-github-mcp-server-is-now-generally-available/
- **核验日期**：2026-09-18

### E5. Work IQ MCP（Microsoft）
- **一句话说明**：Microsoft 365 的 Work IQ MCP server，通过 `/plugin marketplace add microsoft/work-iq` 安装到 Copilot CLI。
- **关键事实**：把 Microsoft 365 工作上下文带给 coding agent
- **证据 URL**：https://learn.microsoft.com/microsoft-365/copilot/extensibility/work-iq/mcp/github-copilot-cli
- **核验日期**：2026-09-18

### E6. Composio Connect（connect.composio.dev/mcp）
- **一句话说明**：Composio 的托管 MCP endpoint，一次连接让 agent 访问 1000+ apps，通过 7 个 meta-tool 做发现/授权/执行。
- **关键事实**：单连接多 app，避免 N 个 MCP server
- **证据 URL**：https://docs.composio.dev/docs/composio-connect
- **核验日期**：2026-09-18

### E7. getAbstract MCP
- **一句话说明**：getAbstract 书摘库的 MCP server，在官方 MCP Registry 中可检索；支持语义搜索和问答。
- **关键事实**：知识类 SaaS connector 示例
- **证据 URL**：https://staging.registry.modelcontextprotocol.io/
- **核验日期**：2026-09-18

### E8. ModelScope MCP（见 D10）
- 中文云厂商的 connector 入口。

---

## F. Workflow / Automation 平台（Tier C/D）

### F1. n8n
- **一句话说明**：source-available 的工作流自动化平台，500+ 集成；2026-09 推出 n8n Agents（定义一次、可在 chat/workflow/Slack/schedule 任意使用）。
- **关键事实**：
  - 自托管免费 Community Edition；Cloud $20/月起
  - 支持 MCP node、AI Agent node、human-in-the-loop
  - 非线性分支/循环可视化
- **证据 URL**：https://n8n.io/ ；https://community.n8n.io/t/introducing-n8n-agents/306323
- **核验日期**：2026-09-18

### F2. Make（make.com）
- **一句话说明**：可视化 scenario builder，无 scenario 复杂度上限；2026 年内置 AI Agents。
- **关键事实**：Free tier；Core $9/月起
- **证据 URL**：https://www.make.com/en/blog/best-automated-workflow-tools-for-scaling-manual-processes
- **核验日期**：2026-09-18

### F3. Dify（dify.ai）
- **一句话说明**：开源 LLM 应用/Agent 开发平台，138K+ GitHub stars，1M+ deployed apps；可视化 workflow + RAG pipeline + LLMOps。
- **关键事实**：自托管免费；Cloud $59/月起；v1.16 起 Agent Beta + sandboxed Linux 执行
- **证据 URL**：https://dify.ai/ ；https://theplanettools.ai/tools/dify
- **核验日期**：2026-09-18

### F4. Coze（扣子）
- **一句话说明**：字节跳动旗下 Bot/Agent 搭建平台，中文生态活跃；可视化编排、知识库、插件。
- **关键事实**：与 Dify/n8n 并列国内常用 agent builder
- **证据 URL**：https://00011000.com/en/articles/2026-ai-agent-builder-platform-review
- **核验日期**：2026-09-18

### F5. Langflow（langflow.org）
- **一句话说明**：低代码 AI builder，可视化拖曳构建 agent 和 MCP server；45K+ stars；内置 API 和 MCP server，把每个 workflow 变成可被其他框架调用的工具。
- **关键事实**：LangChain 生态可视化前端
- **证据 URL**：https://www.langflow.org/
- **核验日期**：2026-09-18

### F6. Flowise（flowiseai.com）
- **一句话说明**：LangChain 系可视化 flow builder，35K+ stars；2025 年被 Workday 收购。
- **关键事实**：快速原型、RAG pipeline
- **证据 URL**：https://ossalt.com/guides/dify-vs-flowise-vs-langflow-2026/raw.md
- **核验日期**：2026-09-18

### F7. Microsoft Power Automate
- **一句话说明**：微软官方 RPA + 自动化平台，与 Microsoft 365/桌面应用深度集成；适合 legacy desktop 软件自动化。
- **关键事实**：桌面流 RPA 层
- **证据 URL**：https://www.make.com/en/blog/best-automated-workflow-tools-for-scaling-manual-processes
- **核验日期**：2026-09-18

### F8. AutoGPT（agpt）
- **一句话说明**：早期 autonomous agent 项目，2026 年仍作为多 agent 对比基准之一被提及。
- **关键事实**：原型/实验性质
- **证据 URL**：https://autogpt.net/top-ai-agent-frameworks/
- **核验日期**：2026-09-18

---

## G. Coding Agent 生态（Tier A/C）

### G1. Claude Code（Anthropic）
- **一句话说明**：Anthropic 官方终端 Coding Agent；plugins/skills/commands/hooks/MCP 全生态；官方 marketplace claude-plugins-official。
- **关键事实**：
  - `~/.claude/skills/` 个人、`.claude/skills/` 项目
  - Plugin 可含 skills/、commands/、hooks/、MCP 配置
  - 2026-09 文档持续更新
- **证据 URL**：https://code.claude.com/docs/en/plugins
- **核验日期**：2026-09-18

### G2. OpenAI Codex CLI / Codex app
- **一句话说明**：OpenAI 官方 Coding Agent；AGENTS.md 约定、sandbox、worktree、cloud environment；2026-09 推出 Agents API（Codex harness 云端）。
- **关键事实**：见 A6
- **证据 URL**：https://github.com/openai/codex
- **核验日期**：2026-09-18

### G3. Gemini CLI（Google）
- **一句话说明**：Google 开源终端 Agent；Extensions 包格式、skills/、GEMINI.md、subagents、policy engine。
- **关键事实**：见 A7
- **证据 URL**：https://github.com/google-gemini/gemini-cli
- **核验日期**：2026-09-18

### G4. Cursor（cursor.com）
- **一句话说明**：Anysphere 出品的 AI IDE；Rules 系统（.cursor/rules/*.mdc 四种触发模式：Always Apply / Apply Intelligently / Apply to Specific Files）。
- **关键事实**：
  - 老的 `.cursorrules` 单文件已演进为 `.cursor/rules/` 目录
  - Project / User / Team 三级 rules
  - 也支持 `.cursor/skills/`
- **证据 URL**：https://cursor.com/docs/rules
- **核验日期**：2026-09-18

### G5. OpenCode（opencode.ai）
- **一句话说明**：SST 团队出品的完全开源（MIT）Coding Agent，160K+ GitHub stars、7.5M 月活；model-agnostic（75+ provider），支持 SKILL.md、MCP、custom agents、plugins。
- **关键事实**：
  - 不绑定厂商、不把代码传到外部服务器
  - 2026-01 Anthropic 封锁第三方工具后反而增长
  - 原生 `skill` tool 按需加载
- **证据 URL**：https://opencode.ai/ ；https://opencode.ai/docs/en/skills/
- **核验日期**：2026-09-18

### G6. GitHub Copilot CLI
- **一句话说明**：GitHub 官方终端 Coding Agent；`/plugin marketplace`、`/plugin install`、`/mcp reload`、PermissionRequest hook；读取 `.mcp.json`、`.vscode/mcp.json`。
- **关键事实**：
  - workspace skills 放 `.github/skills/`
  - 2026 年版本号 v1.0.73 等持续迭代
  - BYOK Anthropic provider
- **证据 URL**：https://github.com/github/copilot-cli
- **核验日期**：2026-09-18

### G7. GitHub Copilot（VS Code / Visual Studio）
- **一句话说明**：IDE 内 Copilot Chat agent mode；原生 Agent Skills 支持；VS Code 文档在 code.visualstudio.com。
- **关键事实**：Skills 面板在 Visual Studio Insider 2026
- **证据 URL**：https://code.visualstudio.com/docs/copilot/customization/agent-skills
- **核验日期**：2026-09-18

### G8. Windsurf（Codeium）
- **一句话说明**：AI IDE，skills 目录约定 `~/.codeium/windsurf/skills/` 或 `.agents/skills/`。
- **关键事实**：跨 Agent 技能路径对照表中列出
- **证据 URL**：https://goddaehee.tistory.com/m/553
- **核验日期**：2026-09-18

### G9. Antigravity
- **一句话说明**：Google 出品的 AI IDE/Agent，被 skills.sh 和 antigravity-awesome-skills 列为支持平台之一。
- **关键事实**：较新产品
- **证据 URL**：https://agentify.ia.br/blog/skills-sh/
- **核验日期**：2026-09-18

### G10. Kiro CLI
- **一句话说明**：AWS 出品的终端 Coding Agent，被 skills.sh 列为支持平台。
- **关键事实**：skills.sh 兼容 20+ agent 之一
- **证据 URL**：https://agentify.ia.br/blog/skills-sh/
- **核验日期**：2026-09-18

### G11. Trae / 其他
- **一句话说明**：字节跳动 Trae 等国产 AI IDE 也在跟进 Agent Skills 标准。
- **关键事实**：教程写作阶段需逐个复核
- **证据 URL**：（待二次核验）
- **核验日期**：2026-09-18

---

## H. Agent Framework / SDK（Tier A/C）

### H1. LangChain / LangGraph
- **一句话说明**：LangChain 生态的低层编排框架；LangGraph 是图式有状态多 agent runtime；33.9K stars、34.5M PyPI 月下载；客户含 Klarna、Replit、Elastic、Cisco、Uber、LinkedIn、BlackRock、JPMorgan。
- **关键事实**：human-in-the-loop、moderation、持久记忆
- **证据 URL**：https://www.langchain.com/langgraph ；https://the-agent-report.com/2026/07/ai-agent-frameworks-comparison-2026-langgraph-crewai-autogen/
- **核验日期**：2026-09-18

### H2. CrewAI
- **一句话说明**：角色驱动多 agent "crew" 模式，52.8K stars、5.2M 月下载；20 行 Python 出原型。
- **关键事实**：上手最低，但生产成熟度中等
- **证据 URL**：https://the-agent-report.com/2026/07/ai-agent-frameworks-comparison-2026-langgraph-crewai-autogen/
- **核验日期**：2026-09-18

### H3. AutoGen（AG2）
- **一句话说明**：微软研究院起源的多 agent 对话框架；GroupChat 模式；2025-10 起其能力并入 Microsoft Agent Framework，但 AG2 社区版仍维护。
- **关键事实**：多 agent 辩论/协作
- **证据 URL**：https://autogpt.net/top-ai-agent-frameworks/
- **核验日期**：2026-09-18

### H4. OpenAI Agents SDK
- **一句话说明**：OpenAI 官方多 agent workflow SDK（Python/TypeScript），MIT，26.9K stars、10.3M 月下载；通过 LiteLLM provider-agnostic；2026-04 加 model-native harness + sandbox。
- **关键事实**：handoffs、guardrails、tracing
- **证据 URL**：https://openai.com/index/the-next-evolution-of-the-agents-sdk/
- **核验日期**：2026-09-18

### H5. Microsoft Agent Framework
- 见 A10。

### H6. Google ADK（Agent Development Kit）
- **一句话说明**：Google 官方 Agent 开发框架，Apache 2.0；GCP-native 团队首选。
- **关键事实**：与 LangChain 对比表中列出
- **证据 URL**：https://www.langchain.com/resources/ai-agent-frameworks
- **核验日期**：2026-09-18

### H7. LlamaIndex Workflows
- **一句话说明**：LlamaIndex 的事件驱动多 agent workflow 层，MIT；文档中心型应用首选。
- **关键事实**：从 RAG 框架演进到 agent workflow
- **证据 URL**：https://www.langchain.com/resources/ai-agent-frameworks
- **核验日期**：2026-09-18

### H8. Haystack
- **一句话说明**：deepset 出品的企业级 RAG/Agent 框架，19K+ stars。
- **关键事实**：企业搜索场景
- **证据 URL**：https://the-agent-report.com/2026/07/ai-agent-frameworks-comparison-2026-langgraph-crewai-autogen/
- **核验日期**：2026-09-18

### H9. Mastra
- **一句话说明**：TypeScript 团队生产级 agent 应用框架，部分开源。
- **关键事实**：TS 生态首选之一
- **证据 URL**：https://www.langchain.com/resources/ai-agent-frameworks
- **核验日期**：2026-09-18

### H10. Semantic Kernel
- **一句话说明**：微软企业级 SDK，2025-10 起与 AutoGen 统一为 Microsoft Agent Framework。
- **关键事实**：⚠️ 新项目应直接用 Microsoft Agent Framework，不要新学 Semantic Kernel
- **证据 URL**：https://devblogs.microsoft.com/foundry/introducing-microsoft-agent-framework-the-open-source-engine-for-agentic-ai-apps/
- **核验日期**：2026-09-18

---

## I. 学术与评测资源（Tier A/D）

### I1. SWE-bench（Princeton NLP）
- **一句话说明**：评估 LLM 解决真实 GitHub issue 能力的基准；2,294 任务、12 个 Python 仓库；HuggingFace 数据集 `princeton-nlp/SWE-bench`。
- **关键事实**：
  - 衍生 Lite / Verified / Multilingual / Pro / Live 多个版本
  - SWE-bench Pro 由 Scale AI 发布，1,8xx 长程任务
  - 2026-04 Berkeley RDI 论文证明存在 exploit agent 可在 8 大基准刷满分而不解题——**读分数时要警惕 benchmark gaming**
- **证据 URL**：https://www.swebench.com/ ；https://arxiv.org/pdf/2509.16941
- **核验日期**：2026-09-18

### I2. tau2-bench（Sierra）
- **一句话说明**：多轮工具调用基准，agent 与 LLM 模拟用户+政策文档对话；retail 114 任务、airline 50、telecom 新增；核心指标 pass^k。
- **关键事实**：测多轮连贯性，区别于单调用 BFCL
- **证据 URL**：https://rdi.berkeley.edu/agentx-agentbeats.html ；https://futureagi.com/blog/evaluating-tool-calling-agents-2026/
- **核验日期**：2026-09-18

### I3. Berkeley Function-Calling Leaderboard（BFCL）
- **一句话说明**：UC Berkeley Gorilla 项目维护的函数调用排行榜，已到 V4；AST 评估指标；Python/Java/JS/REST API。
- **关键事实**：官方榜 gorilla.cs.berkeley.edu/leaderboard，JS 渲染，不要抄二手表
- **证据 URL**：https://gorilla.cs.berkeley.edu/leaderboard
- **核验日期**：2026-09-18

### I4. OSWorld
- **一句话说明**：真实桌面 GUI 自动化基准（Ubuntu/Windows/macOS），369+43 Windows 任务；agent 看截图、动鼠标、敲键盘。
- **关键事实**：人类基线 72.36%；2026-05 Claude Mythos Preview 79.6%
- **证据 URL**：https://aiwiki.ai/wiki/osworld
- **核验日期**：2026-09-18

### I5. WebArena
- **一句话说明**：沙箱网站 web agent 基准，812 个 templated 任务、241 templates、4 个域。
- **关键事实**：与 OSWorld/WebVoyager/GAIA 并列四大
- **证据 URL**：https://aiwiki.ai/wiki/osworld
- **核验日期**：2026-09-18

### I6. GAIA
- **一句话说明**：通用 AI assistant 基准，466 任务，混合 web 搜索/文件/工具；分 Level 1/2/3。
- **关键事实**：Made By Agents 等站维护 live leaderboard
- **证据 URL**：https://www.awesomeagents.ai/leaderboards/agentic-ai-benchmarks-leaderboard/
- **核验日期**：2026-09-18

### I7. Terminal-Bench
- **一句话说明**：终端环境编码基准；2026 年 Claude Opus 4.6 排名第一。
- **关键事实**：命令行 coding 能力
- **证据 URL**：https://fleeceai.app/blog/ai-agent-benchmarks-2026-explained
- **核验日期**：2026-09-18

### I8. CAR-bench
- **一句话说明**：Computer Use / Web Agent 基准，Berkeley RDI AgentX 竞赛收录。
- **关键事实**：与 OSWorld-Verified 并列 computer use 类
- **证据 URL**：https://rdi.berkeley.edu/agentx-agentbeats.html
- **核验日期**：2026-09-18

### I9. Pi-Bench
- **一句话说明**：Agent safety 基准，Berkeley RDI AgentX 竞赛收录。
- **关键事实**：安全方向
- **证据 URL**：https://rdi.berkeley.edu/agentx-agentbeats.html
- **核验日期**：2026-09-18

### I10. MCP-Atlas
- **一句话说明**：跨 server 工具协调基准；2026-09 Gemini 3.1 Pro 69.2%。
- **关键事实**：MCP 生态特有评测
- **证据 URL**：https://fleeceai.app/blog/ai-agent-benchmarks-2026-explained
- **核验日期**：2026-09-18

### I11. MCPZoo（arXiv 2025-12）
- **一句话说明**：90,146 个可运行 MCP server 的大规模数据集论文，从六大公开来源（MCP World、MCP Store、MCP Servers Repository、AIbase MCP、Mcp.so、PulseMCP）采集。
- **关键事实**：学术研究用途，非产品
- **证据 URL**：https://arxiv.org/pdf/2512.15144
- **核验日期**：2026-09-18

### I12. Agent Skills 复用性研究（arXiv 2026-08）
- **一句话说明**："What Keeps Agent Skills from Being Reusable? Evidence from 138K SKILL.md Files"——爬取 138K SKILL.md 文件研究复用性障碍。
- **关键事实**：第一届 Agent Skills Workshop 论文
- **证据 URL**：https://arxiv.org/html/2608.08453v1
- **核验日期**：2026-09-18

---

## 附录：已标注 deprecated / 过时资源

| 资源 | 状态 | 替代/继任 | 证据 |
|---|---|---|---|
| openai/skills | 2026-06-22 deprecated | OpenAI Plugin Directory（ChatGPT/Codex 内） | https://github.com/openai/skills |
| openai/plugins（旧 ChatGPT plugins） | 已被 Plugin Directory 取代（2026-07-09 app directory → plugin directory） | ChatGPT Plugin Directory | https://help.openai.com/ |
| 旧 ChatGPT plugins blog post（2023-03） | 已过时 | GPTs actions → Plugin Directory | https://openai.com/blog/chatgpt-plugins |
| Semantic Kernel（独立新项目） | 2025-10 起并入 Microsoft Agent Framework | microsoft/agent-framework | https://devblogs.microsoft.com/foundry/introducing-microsoft-agent-framework/ |
| 老 `.cursorrules` 单文件 | 已演进为 `.cursor/rules/*.mdc` 目录 | cursor.com/docs/rules | https://cursor.com/docs/rules |
| ComposioHQ/awesome-claude-skills | 2026-05 后更新放缓 | 用 VoltAgent/awesome-agent-skills 等替代 | https://tellian.io/tag/mcp/ |

---

## 调研说明与局限

1. **本报告所有 URL 均为 2026-09-18 联网检索结果中实际出现的链接**，未编造。
2. 部分聚合站（skillsmp、skillhub.club 等）的"X 个 skills"数字在不同时间点口径差异大，本报告只记录检索当次看到的数字，不做质量背书。
3. `io-oi-ai/Skillhub` 在本次公网搜索中未直接命中 README，已在 C17 标注"待二次复核"，教程写作阶段需直接访问 GitHub 确认其定位。
4. GitHub Star 数仅在文字中作为活跃度旁证，**不作为安全/质量证据**。
5. 同名 SkillHub 已区分：
   - **skillhub.club**：公网 AI-evaluated 市场
   - **iflytek/skillhub**：讯飞企业级自托管注册中心
   - **io-oi-ai/Skillhub**：待复核
   - **CassianFlorin/skill-hub**：Go 编写的 CLI 包管理器
   - **MeteorsLiu/skillhub-mvp**：MVP 项目
   - **skillhub.lol**：另一个市场层
   - **agentskillshub.dev**：安全分级目录（注意拼写）
6. 本报告为 Phase 1 生态调研产出；教程正式写作前（Phase 9）需再做一次快速变化内容复核。
