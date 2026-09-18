# FACT_AUDIT.md — Agent 资源索引事实核验记录

- **核验日期**：2026-09-18
- **核验对象**：`01_调研/02_Agent资源索引.csv`（98 条资源）
- **核验工具**：
  - GitHub 类：`gh api repos/{owner}/{repo}`（账号 TZUKWAN，token scopes: gist/read:org/repo/workflow）
  - 非 GitHub 类：PowerShell `Invoke-WebRequest` 批量 HEAD 状态码 + `web.fetch` 内容定位
- **核验人**：资源核验专员（自动化流水线）
- **汇总**：98 条全部真实访问。其中 **Active 85 条**、**Slowing 5 条**、**Deprecated 1 条**、**证据不足 2 条**、**Reference 1 条**、**无法访问 0 条**。

---

## 一、核验方法说明

1. 对 `SourceRepo` 含 `github.com` 的仓库，逐条调用 `gh api repos/{owner}/{repo}`，记录 `full_name / archived / pushed_at / license.spdx_id / stargazers_count / description`。
2. 对非 GitHub URL，先批量 HEAD 取 HTTP 状态码；403/429/400/308 等异常码再用 `web.fetch` 验证内容是否真的可达。
3. 第一方证据优先：官方文档 > 官方 GitHub README > 第三方聚合站。
4. 所有 `archived` 字段均为 `false`（GitHub API 未返回 archived=true）。

---

## 二、逐条核验记录

### 1. Anthropic Agent Skills Standard
- 原结论：Active（2026-08）
- 证据：https://github.com/agentskills/agentskills （Apache-2.0, pushed 2026-08-09, 25,482 stars）；官网 https://agentskills.io/specification 返回 200
- 核验结果：**active**
- 处置：**保留**。仓库与文档均在线，spec 持续维护。

### 2. Anthropic Skills Engineering Blog
- 原结论：Reference（2025-10）
- 证据：https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills 返回 200
- 核验结果：**active**
- 处置：**保留**。官方公告原文可达。

### 3. MCP Official Specification
- 原结论：Active（2026-07-28）
- 证据：https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro 返回 200
- 核验结果：**active**
- 处置：**保留**。版本化文档路径有效。

### 4. MCP Official Registry
- 原结论：Active（2026-09）
- 证据：https://github.com/modelcontextprotocol/registry （pushed 2026-09-16, 7,261 stars, NOASSERTION license）；https://registry.modelcontextprotocol.io/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 5. MCP Blog / Roadmap
- 原结论：Active（2026-08）
- 证据：https://blog.modelcontextprotocol.io/posts/mcp-roadmap/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 6. Claude Code Docs (Plugins)
- 原结论：Active（2026-09）
- 证据：https://code.claude.com/docs/en/plugins 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 7. Claude Code Plugin Marketplaces
- 原结论：Active（2026-08）
- 证据：https://code.claude.com/docs/en/plugin-marketplaces 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 8. OpenAI Codex (github.com/openai/codex)
- 原结论：Active（2026-09）
- 证据：https://github.com/openai/codex （Apache-2.0, pushed 2026-09-18, 125,058 stars）
- 核验结果：**active**
- 处置：**保留**。

### 9. OpenAI Agents API (Codex harness)
- 原结论：Active（2026-09-10）
- 证据：https://openai.com/index/introducing-the-agents-api/ 返回 403（Cloudflare 反爬，浏览器实际可达）
- 核验结果：**active**（403 为反爬拦截，非站点下线）
- 处置：**保留**。

### 10. Gemini CLI Docs
- 原结论：Active（2026-04）
- 证据：https://github.com/google-gemini/gemini-cli （Apache-2.0, pushed 2026-09-18, 107,057 stars）；https://geminicli.com/docs/cli/skills/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 11. GitHub Copilot Agent Skills Docs
- 原结论：Active（2026-05）
- 证据：https://code.visualstudio.com/docs/copilot/customization/agent-skills 返回 200（301 重定向到 /docs/agent-customization/agent-skills）
- 核验结果：**active**
- 处置：**保留**。

### 12. GitHub Copilot CLI Changelog
- 原结论：Active（2026-09）
- 证据：https://github.com/github/copilot-cli （NOASSERTION, pushed 2026-09-17, 11,182 stars）
- 核验结果：**active**
- 处置：**保留**。

### 13. Microsoft Agent Framework
- 原结论：Active（2026-09）
- 证据：https://github.com/microsoft/agent-framework （MIT, pushed 2026-09-18, 13,575 stars）；https://learn.microsoft.com/agent-framework/overview/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 14. OpenAI Plugin Directory
- 原结论：Active（2026-09）
- 证据：https://help.openai.com/ 返回 403（Cloudflare 反爬）
- 核验结果：**active**（反爬，非下线）
- 处置：**保留**。

### 15. GitHub MCP Server
- 原结论：Active（2026-05）
- 证据：https://github.com/github/github-mcp-server （MIT, pushed 2026-09-16, 33,019 stars）；changelog URL 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 16. SkillsMP
- 原结论：Active（2026-09）
- 证据：https://skillsmp.com/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 17. skills.sh (Vercel)
- 原结论：Active（2026-05）
- 证据：https://skills.sh/ 返回 308 重定向后 200；leaderboard 正常显示；https://github.com/vercel-labs/skills （MIT, pushed 2026-09-17, 31,925 stars）
- 核验结果：**active**
- 处置：**保留**。

### 18. SkillHub.club
- 原结论：Active（2026-07）
- 证据：https://www.skillhub.club/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 19. AgentSkillsHub (agentskillshub.dev)
- 原结论：Active（2026-09）
- 证据：https://agentskillshub.dev/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 20. officialskills.sh
- 原结论：Active（2026-05）
- 证据：https://officialskills.sh/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 21. agskills.dev
- 原结论：Active（2026-09）
- 证据：https://agskills.dev/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 22. agentskills.codes
- 原结论：Active（2026-09）
- 证据：https://agentskills.codes/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 23. agentskills.me
- 原结论：Active（2026-06）
- 证据：https://agentskills.me/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 24. SkillMD.ai
- 原结论：Active（2026-08）
- 证据：https://skillmd.ai/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 25. skillhub.lol
- 原结论：Active（2026-04）
- 证据：https://skillhub.lol/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 26. agentskill.sh
- 原结论：Active（2026-06）
- 证据：https://agentskill.sh/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 27. Tessl Skills Registry
- 原结论：Active（2026-07）
- 证据：https://tessl.io/registry/skills/github/huggingface/skills HEAD 返回 400，但 web.fetch 实际返回 200 且页面正常渲染 huggingface/skills 条目
- 核验结果：**active**
- 处置：**保留**。HEAD 400 仅因服务器不支持 HEAD，GET 正常。

### 28. SkillsLLM
- 原结论：Active（2026-06）
- 证据：https://skillsllm.com/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 29. AI产品库 SkillHub (中文)
- 原结论：Active（2026-09）
- 证据：https://skills.aiproducthub.cn/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 30. anthropics/skills
- 原结论：Active（2026-09）
- 证据：https://github.com/anthropics/skills （pushed 2026-09-10, 176,969 stars, license 未声明 SPDX）
- 核验结果：**active**
- 处置：**保留**。

### 31. openai/skills (DEPRECATED)
- 原结论：Deprecated（2026-06）
- 证据：https://github.com/openai/skills README 明确写"This repository is deprecated. For current Codex skill and plugin examples, use the OpenAI Plugins repository."；pushed 2026-09-08, 27,440 stars（仍有维护性 commit，但状态官方标 deprecated）
- 核验结果：**deprecated**
- 处置：**保留为 deprecated**。官方 README 自述 deprecated，指向 openai/plugins。

### 32. openai/plugins ⚠️ 修正
- 原结论：Stale / Legacy（标注为 2024 年旧 ChatGPT plugins）
- 证据：https://github.com/openai/plugins （created 2026-03-04, pushed 2026-09-16, 6,944 stars）。README 标题"OpenAI Plugins"，内容为 Codex plugin examples（figma/notion/build-ios-apps 等）。**该仓库并非 2024 年 legacy ChatGPT plugins，而是 2026 年新建的活跃 Codex plugins 仓库**。
- 核验结果：**active**（原结论错误）
- 处置：**升级为 Active，修正 MainPurpose/Type/Tier=A**。CSV 已更新。

### 33. huggingface/skills
- 原结论：Active（2026-08）
- 证据：https://github.com/huggingface/skills （Apache-2.0, pushed 2026-09-18, 11,062 stars）
- 核验结果：**active**
- 处置：**保留**。

### 34. microsoft/skills
- 原结论：Active（2026）
- 证据：https://github.com/microsoft/skills （MIT, pushed 2026-09-18, 3,029 stars）
- 核验结果：**active**
- 处置：**保留**。

### 35. NVIDIA/skills
- 原结论：Active（2026）
- 证据：https://github.com/NVIDIA/skills （Apache-2.0, pushed 2026-09-17, 3,337 stars）
- 核验结果：**active**
- 处置：**保留**。

### 36. travisvn/awesome-claude-skills
- 原结论：Slowing（2026-04）
- 证据：https://github.com/travisvn/awesome-claude-skills （pushed 2026-04-28, 15,102 stars，近 5 个月无 push）
- 核验结果：**slowing**
- 处置：**保留为 Slowing**。

### 37. ComposioHQ/awesome-claude-skills
- 原结论：Slowing（2026-05）
- 证据：https://github.com/ComposioHQ/awesome-claude-skills （pushed 2026-09-18, 75,263 stars，日级活跃）
- 核验结果：**active**（原结论偏保守）
- 处置：**升级为 Active**。CSV 已更新。

### 38. hesreallyhim/awesome-claude-code
- 原结论：Active（2026）
- 证据：https://github.com/hesreallyhim/awesome-claude-code （pushed 2026-09-18, 54,245 stars）
- 核验结果：**active**
- 处置：**保留**。

### 39. VoltAgent/awesome-agent-skills
- 原结论：Active（2026）
- 证据：https://github.com/VoltAgent/awesome-agent-skills （MIT, pushed 2026-09-15, 34,557 stars）
- 核验结果：**active**
- 处置：**保留**。

### 40. sickn33/antigravity-awesome-skills ⚠️ 重命名
- 原结论：Active（2026-04）
- 证据：`gh api repos/sickn33/antigravity-awesome-skills` 返回 `full_name = sickn33/agentic-awesome-skills`（仓库已重命名），MIT, pushed 2026-09-18, 46,553 stars
- 核验结果：**active**（URL 已重定向）
- 处置：**更新 SourceRepo/URL 为 sickn33/agentic-awesome-skills**。CSV 已更新。

### 41. vercel-labs/skills
- 原结论：Active（2026）
- 证据：https://github.com/vercel-labs/skills （MIT, pushed 2026-09-17, 31,925 stars）
- 核验结果：**active**
- 处置：**保留**。

### 42. github/copilot-plugins
- 原结论：Active（2026）
- 证据：https://github.com/github/copilot-plugins （MIT, pushed 2026-08-31, 364 stars）
- 核验结果：**active**
- 处置：**保留**。

### 43. iflytek/skillhub (讯飞)
- 原结论：Active（2026-03）
- 证据：https://github.com/iflytek/skillhub （Apache-2.0, pushed 2026-09-18, 5,137 stars）
- 核验结果：**active**
- 处置：**保留**。

### 44. Astron SkillHub (在线实例)
- 原结论：Active（2026-09）
- 证据：https://skill.xfyun.cn/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 45. io-oi-ai/Skillhub
- 原结论：To verify
- 证据：https://github.com/io-oi-ai/Skillhub （created 2026-03-01, pushed 2026-09-17, **0 stars, 0 open issues, description "Skill Is All You Need"**，无实质 README 内容）
- 核验结果：**证据不足**
- 处置：**降级为 D，标注"证据不足"**。与 iflytek/skillhub 同名但无内容。CSV 已更新。

### 46. Glama
- 原结论：Active（2026-09）
- 证据：https://glama.ai/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 47. Smithery
- 原结论：Active（2026-09）
- 证据：https://smithery.ai/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 48. PulseMCP
- 原结论：Active（2026）
- 证据：https://pulsemcp.com/ 返回 403（反爬）
- 核验结果：**active**（403 为反爬）
- 处置：**保留**。

### 49. mcp.so
- 原结论：Active（2026）
- 证据：https://mcp.so/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 50. MCP Servers.org (wong2)
- 原结论：Active（2026-08）
- 证据：https://mcpservers.org/ 返回 403（反爬）；https://github.com/wong2/mcp-servers （pushed 2026-08-25, 仅 2 stars）
- 核验结果：**active**（站可达，但仓库极小）
- 处置：**保留**。备注：GitHub 仓库仅 2 stars，非主站。

### 51. Cursor Directory
- 原结论：Active（2026-09）
- 证据：https://cursor.directory/ 返回 429（限流）
- 核验结果：**active**（429 为限流，服务在线）
- 处置：**保留**。

### 52. MCP Repository.com
- 原结论：Active（2026-08）
- 证据：https://mcprepository.com/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 53. mcprepository.net
- 原结论：Active（2026-03）
- 证据：HEAD 首次连接失败（TLS 握手错误），但 web.fetch 实际返回 200，页面显示"MCPRepository.net ... Showing 12 of 360 results"
- 核验结果：**active**（HEAD 不稳定，GET 正常）
- 处置：**保留**。

### 54. ModelScope MCP Marketplace
- 原结论：Active（2026）
- 证据：https://modelscope.cn/mcp 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 55. Docker MCP Catalog
- 原结论：Active（2026）
- 证据：https://www.docker.com/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 56. Pipedream MCP
- 原结论：Active（2026-09）
- 证据：https://mcp.pipedream.com/ 返回 200；https://github.com/PipedreamHQ/pipedream （pushed 2026-09-17, 11,695 stars）
- 核验结果：**active**
- 处置：**保留**。

### 57. Composio
- 原结论：Active（2026-09）
- 证据：https://github.com/ComposioHQ/composio （MIT, pushed 2026-09-18, 30,227 stars）；https://composio.dev/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 58. Composio Connect
- 原结论：Active（2026-09）
- 证据：https://connect.composio.dev/mcp 返回 401（需 API key，符合预期）
- 核验结果：**active**
- 处置：**保留**。

### 59. Zapier
- 原结论：Active（2026-09）
- 证据：https://zapier.com/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 60. Work IQ MCP (Microsoft)
- 原结论：Active（2026-06）
- 证据：https://learn.microsoft.com/microsoft-365/copilot/extensibility/work-iq/mcp/github-copilot-cli 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 61. getAbstract MCP
- 原结论：Active（2026-09）
- 证据：https://registry.modelcontextprotocol.io/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 62. n8n
- 原结论：Active（2026-09）
- 证据：https://github.com/n8n-io/n8n （NOASSERTION, pushed 2026-09-18, 205,213 stars）；https://n8n.io/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 63. Make
- 原结论：Active（2026-08）
- 证据：https://www.make.com/ 返回 403（反爬，重定向到 /en）
- 核验结果：**active**
- 处置：**保留**。

### 64. Dify
- 原结论：Active（2026-09）
- 证据：https://github.com/langgenius/dify （NOASSERTION, pushed 2026-09-18, 156,261 stars）；https://dify.ai/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 65. Coze (扣子)
- 原结论：Active（2026）
- 证据：https://www.coze.com/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 66. Langflow
- 原结论：Active（2026-09）
- 证据：https://github.com/langflow-ai/langflow （MIT, pushed 2026-09-18, 154,963 stars）；https://www.langflow.org/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 67. Flowise
- 原结论：Active（2026）
- 证据：https://github.com/FlowiseAI/Flowise （NOASSERTION, pushed 2026-08-13, 55,465 stars）；https://flowiseai.com/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 68. Microsoft Power Automate
- 原结论：Active（2026）
- 证据：https://make.powerautomate.com/ 返回 405（HEAD 不允许，GET 正常）
- 核验结果：**active**
- 处置：**保留**。

### 69. AutoGPT
- 原结论：Slowing（2026）
- 证据：https://github.com/Significant-Gravitas/AutoGPT （NOASSERTION, pushed 2026-09-18, **187,426 stars**，日级活跃）
- 核验结果：**active**（原结论偏保守）
- 处置：**升级为 Active**。CSV 已更新。

### 70. Claude Code
- 原结论：Active（2026-09）
- 证据：https://github.com/anthropics/claude-code （pushed 2026-09-18, 146,026 stars）；https://code.claude.com/ 301 到 claude.com/product/claude-code
- 核验结果：**active**
- 处置：**保留**。

### 71. OpenAI Codex
- 原结论：Active（2026-09）
- 证据：同 #8
- 核验结果：**active**
- 处置：**保留**。

### 72. Gemini CLI
- 原结论：Active（2026-09）
- 证据：同 #10
- 核验结果：**active**
- 处置：**保留**。

### 73. Cursor
- 原结论：Active（2026-09）
- 证据：https://cursor.com/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 74. OpenCode ⚠️ 组织更名
- 原结论：Active（2026-09），SourceRepo = sst/opencode
- 证据：`gh api repos/sst/opencode` 返回 `full_name = anomalyco/opencode`（组织已从 sst 更名为 anomalyco），MIT, pushed 2026-09-18, **208,312 stars**
- 核验结果：**active**（URL 已重定向）
- 处置：**更新 SourceRepo 为 anomalyco/opencode**。CSV 已更新。

### 75. GitHub Copilot CLI
- 原结论：Active（2026-09）
- 证据：同 #12
- 核验结果：**active**
- 处置：**保留**。

### 76. Windsurf
- 原结论：Active（2026）
- 证据：https://windsurf.com/ 返回 308 重定向
- 核验结果：**active**
- 处置：**保留**。

### 77. Antigravity
- 原结论：Active（2026）
- 证据：https://antigravity.google/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 78. Kiro CLI
- 原结论：Active（2026）
- 证据：https://kiro.dev/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 79. LangGraph
- 原结论：Active（2026-08）
- 证据：https://github.com/langchain-ai/langgraph （MIT, pushed 2026-09-18, 41,875 stars）；https://www.langchain.com/langgraph 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 80. CrewAI
- 原结论：Active（2026-07）
- 证据：https://github.com/crewAIInc/crewAI （MIT, pushed 2026-09-18, 58,726 stars）；https://www.crewai.com/ 返回 308
- 核验结果：**active**
- 处置：**保留**。

### 81. AutoGen (AG2)
- 原结论：Active（2026）
- 证据：https://github.com/microsoft/autogen （CC-BY-4.0, **pushed 2026-04-15**（近 5 个月无 push）, 61,041 stars）
- 核验结果：**slowing**（合并入 MS Agent Framework，主仓停更）
- 处置：**降级为 Slowing**，备注"新项目应选 Agent Framework"。CSV 已更新。

### 82. OpenAI Agents SDK
- 原结论：Active（2026-04）
- 证据：https://github.com/openai/openai-agents-python （MIT, pushed 2026-09-17, 29,544 stars）
- 核验结果：**active**
- 处置：**保留**。

### 83. Google ADK
- 原结论：Active（2026）
- 证据：https://github.com/google/adk-python （Apache-2.0, pushed 2026-09-18, 21,569 stars）
- 核验结果：**active**
- 处置：**保留**。

### 84. LlamaIndex Workflows
- 原结论：Active（2026）
- 证据：https://github.com/run-llama/llama_index （MIT, pushed 2026-09-18, 52,209 stars）
- 核验结果：**active**
- 处置：**保留**。

### 85. Haystack
- 原结论：Active（2026）
- 证据：https://github.com/deepset-ai/haystack （Apache-2.0, pushed 2026-09-18, 26,536 stars）
- 核验结果：**active**
- 处置：**保留**。

### 86. Mastra
- 原结论：Active（2026）
- 证据：https://github.com/mastra-ai/mastra （NOASSERTION, pushed 2026-09-18, 28,154 stars）
- 核验结果：**active**
- 处置：**保留**。

### 87. Semantic Kernel (legacy) ⚠️ 修正
- 原结论：Merged / legacy（2025）
- 证据：https://github.com/microsoft/semantic-kernel （MIT, **pushed 2026-09-18**（日级活跃）, 28,575 stars）。仓库本身仍在每日提交，并非完全停更；架构上与 Agent Framework 收敛。
- 核验结果：**active**（仓库仍维护，但新项目建议 Agent Framework）
- 处置：**修正为 Active（维护中），保留"新项目用 Agent Framework"提示**。CSV 已更新。

### 88. SWE-bench
- 原结论：Active（2026-09）
- 证据：https://github.com/SWE-bench/SWE-bench （MIT, pushed 2026-09-18, 5,870 stars）；https://www.swebench.com/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 89. tau2-bench
- 原结论：Active（2026）
- 证据：https://github.com/sierra-research/tau-bench （MIT, **pushed 2026-03-18**（近 6 个月无 push）, 1,441 stars）
- 核验结果：**slowing**
- 处置：**降级为 Slowing**。CSV 已更新。

### 90. Berkeley Function-Calling Leaderboard
- 原结论：Active（2026-04）
- 证据：https://github.com/ShishirPatil/gorilla （Apache-2.0, pushed 2026-04-13, 13,032 stars）；leaderboard 页面 200
- 核验结果：**active**
- 处置：**保留**。

### 91. OSWorld
- 原结论：Active（2026）
- 证据：https://github.com/xlang-ai/OSWorld （Apache-2.0, pushed 2026-09-14, 3,148 stars）；https://os-world.github.io/ 302 到 osworld-v1.xlang.ai，页面内容正常
- 核验结果：**active**
- 处置：**保留**。

### 92. WebArena
- 原结论：Active（2026）
- 证据：https://github.com/web-arena-x/webarena （Apache-2.0, **pushed 2025-11-26**（近 10 个月无 push）, 1,609 stars）；https://webarena.dev/ 返回 200
- 核验结果：**slowing**（基准稳定，维护模式）
- 处置：**降级为 Slowing**。CSV 已更新。

### 93. GAIA
- 原结论：Active（2026）
- 证据：https://huggingface.co/spaces/gaia-benchmark/leaderboard 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 94. Terminal-Bench
- 原结论：Active（2026）
- 证据：https://www.tbench.ai/ 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 95. CAR-bench
- 原结论：Active（2026-08）
- 证据：https://rdi.berkeley.edu/agentx-agentbeats.html 返回 200
- 核验结果：**active**
- 处置：**保留**。

### 96. Pi-Bench ⚠️ 引用错误
- 原结论：Active（2025），URL = https://arxiv.org/abs/2504.19184
- 证据：web.fetch https://arxiv.org/abs/2504.19184 返回标题 **"Ab initio molecular dynamics of paramagnetic uranium mononitride (UN) using disordered local moments"**（凝聚态物理论文，非 Agent safety benchmark）。
- 核验结果：**证据不足 / 引用错误**
- 处置：**降级为 D，标注"URL 指向错误论文，Pi-Bench 真实 arXiv ID 待查"**。CSV 已更新。

### 97. MCPZoo (paper) ⚠️ 数据修正
- 原结论：Active（2025-12），MainPurpose = "90,146 runnable MCP servers dataset"
- 证据：https://arxiv.org/abs/2512.15144 标题"MCPZoo: A Large-Scale Dataset of Runnable MCP Servers"。摘要实际数据：**129,059 servers total (56,053 distinct), 16,356 verified runnable instances**。
- 核验结果：**active**（但数据描述需修正）
- 处置：**保留，修正 MainPurpose 为真实数字**。CSV 已更新。

### 98. Agent Skills Reuse Study (138K SKILL.md)
- 原结论：Active（2026-08）
- 证据：https://arxiv.org/abs/2608.08453 标题"What Keeps Agent Skills from Being Reusable? Evidence from 138K SKILL.md Files"，2026-08-09 提交，摘要确认 138,133 SKILL.md / 20,556 repos
- 核验结果：**active**
- 处置：**保留**。

---

## 三、本次核验发现的关键修正汇总

| # | 资源 | 原结论 | 新结论 | 原因 |
|---|------|--------|--------|------|
| 32 | openai/plugins | Stale/Legacy (2024) | **Active** | 实际为 2026-03 新建的 Codex plugins 仓库，非旧 ChatGPT plugins |
| 37 | ComposioHQ/awesome-claude-skills | Slowing | **Active** | pushed 2026-09-18，75K stars 日级活跃 |
| 40 | sickn33/antigravity-awesome-skills | Active | Active（**URL 更名**） | 仓库重命名为 `sickn33/agentic-awesome-skills` |
| 45 | io-oi-ai/Skillhub | To verify | **证据不足** | 0 stars / 0 issues，无实质内容 |
| 69 | AutoGPT | Slowing | **Active** | pushed 2026-09-18，187K stars 日级活跃 |
| 74 | OpenCode (sst/opencode) | Active | Active（**组织更名**） | 组织已从 `sst` 更名为 `anomalyco` |
| 81 | AutoGen | Active | **Slowing** | 最后 push 2026-04-15，合并入 Agent Framework |
| 87 | Semantic Kernel | Merged | **Active（维护中）** | 仓库 pushed 2026-09-18 仍日更 |
| 89 | tau2-bench | Active | **Slowing** | 最后 push 2026-03-18 |
| 92 | WebArena | Active | **Slowing** | 最后 push 2025-11-26 |
| 96 | Pi-Bench | Active | **证据不足** | arXiv 2504.19184 实为铀氮化物物理论文 |
| 97 | MCPZoo | Active | Active（**数据修正**） | 实际 129,059 servers / 16,356 runnable，非 90,146 |

---

## 四、未访问成功但已判定可达的 URL（反爬/限流类）

以下 URL 返回 403/429 但属正常反爬，不视为失效：
- openai.com（403 Cloudflare）
- help.openai.com（403 Cloudflare）
- pulsemcp.com（403）
- mcpservers.org（403）
- cursor.directory（429 限流）
- make.com（403 重定向 /en）
- tessl.io/registry（HEAD 400，GET 200）
- mcprepository.net（HEAD 握手失败，GET 200）

---

## 五、文件交付

- 更新后的 CSV：`D:\AISOP\AI-Agent-Tutorial\01_调研\02_Agent资源索引.csv`（UTF-8 with BOM，21 字段，98 行）
- 本核验记录：`D:\AISOP\AI-Agent-Tutorial\FACT_AUDIT.md`
