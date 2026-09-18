# CHANGELOG

## v1.2.0 (2026-09-19)

### 内容体系重构（V1.2 核心）
- 全书总模型统一：8阶段主线（定义任务→准备上下文与能力→执行→观察→验证→修复→交付→沉淀）替代 GCRWV，其他方法全部挂接到主线
- 8要素定稿：目标/上下文/环境/权限/约束/过程/验收/交付（上下文=材料+背景+当前状态）
- 四条铁律升级为全书通用原则（生成结果≠完成任务；执行动作≠得到正确结果；一次验证通过≠整体可靠；Agent 声明完成≠实际完成），并给出软件/科研/数据分领域版本
- PART 0 工作方式转换（三维度：工具调用/自主推进/持续运行）替代五种类型百科
- PART 1-2 闭环（"给它桌子和钥匙 / 告诉它到底干什么"）；PART 3 状态管理（State 为中心 + 最小配置 TASKS.md/WORKLOG.md/output/）
- PART 4 四类验证核心章（来源/数值/操作/软件 + 三级强度：自测→交叉核验→独立审查）；PART 5 六类故障手册（症状→原因→查→停→恢复→避免）
- PART 6 四系统+扩展接口层（推理/信息/行动/编排 + API/Connector/Plugin/MCP/Skill 接入机制）替代五层架构
- PART 7 能力供应链（8环闭环：缺能力→发现→核验→权限→安装→沙箱验证→升级→撤销）+ 5 条技术纠偏（环境变量/gh CLI/Plugin/MCP/RPA 等表述修正）
- PART 8 LAB 分级（核心 A/C/D/G、专业 B/E、进阶 F）；PART 9 工作流先行教学；PART 10 build-along 13 步（my-agent 为主人公）
- 删除模板疲劳：各 Part 独立教学形式；6 条全书原则（封底/导读）；语言风格统一（核心概念首次出现即准确）

### 图表更新
- F00/F01/F11/F12/F21 按新方法结构重画并逐张复验
- 修复 9 张未引用图（F06/F20/F22/F23/F25/F26/F27/F28/F30）：正文补"待插入 Fxx"占位符 + 修正 build_docx.py 的 EXTRA_IMAGE_RULES 关键词，最终 32/32 全覆盖（SHA-256 哈希核验）

### 篇幅调整（授权内恢复至目标）
- V1.2 初版过度压缩：字数 96,969→53,409、页数 197→105
- 四轮恢复至最终：页数 175（目标 160–180）、字数（contract）104,661
- 恢复内容：操作步骤、真实案例、Mission 走查、故障病例、检查表、工作流代码清单、build-along 读者自检

### 验证与证据
- 重新渲染全部 175 页（05_Word/pages_full/ + page_audit.json，0 空白页）
- QA_REPORT.md / VISUAL_QA.md 更新为最终状态；audit.py 0 错误

## v1.1.1 (2026-09-18)

### 真实案例补齐（commit 10fe76a）
- 新增 examples/labs/lab_c_office/：真实 Office 闭环（CSV→Excel→Word→汇报要点，三方数字一致 62,818）
- 新增 examples/labs/lab_e_data/：真实数据分析闭环（脏数据→清洗→统计→图→报告，清洗后 10 行均值 10,180）
- 新增 examples/labs/labf_project/：真实开源项目（colorama clone→改功能→测试→commit，本地 SHA 2874e5f；commit 880789a 将 repo/ 由 gitlink 修正为 50 个普通文件 vendor 入库，保留 BSD-3 License）
- daily_monitor.py 新增 live 模式：真实 GitHub API 调用（HTTP 200、10 条 Release，examples/automation/http_live/）
- my-agent 补齐：Skill 加载、RAG 关键词检索、Planner/Executor/Evaluator、test 14/14、eval 10/10

### 工程修复
- render_full.py / export_pdf.ps1 硬编码路径改为相对路径
- requirements.txt 补充 pymupdf/openpyxl
- README 删除过时 V1.2 表述，新增构建与 QA 环境要求
- QA_REPORT 重写为严格 PASS/PARTIAL/FAIL 表

## v1.1.0 (2026-09-18)

### 正文深度重构
- PART 0-3：概念边界改为"能力递进光谱"（非排他定义）；新增 1.7 节"四级权限实测"；新增 3.15 节"中断后如何续跑"
- examples/：新增 WORKLOG.md/TASKS.md/PROGRESS.md/DECISIONS.md 模板（带真实示例）
- PART 4-5：新增 4.14 节"故障注入实验"（假引用/错误数据/放错文件/失效链接/测试假完成）
- PART 6：重写为五层认知结构（6.1-6.20），每概念用"概念本身→常见实现→平台差异→掌握程度→例子"五段模板
- PART 7：新增真实安装演示（Skill 用 .claude/skills、MCP 用 @modelcontextprotocol/server-filesystem、Connector 用 gh CLI scopes）
- PART 8：七个 LAB 各加旗舰项目模板；LAB B 删除无依据表述并新增 AI 使用政策查找方法
- PART 9：新增 daily_monitor.py（GitHub Releases 监控）和 email_triage.py（邮件审批工作流）
- PART 10：新增 examples/my-agent/ 完整 Agent 项目（无 API Key 可运行，test 10/10、eval 7/7）

### 资源核验
- 98 条资源全部重新联网核验（gh api + web.fetch，日期 2026-09-18）
- 12 项关键修正（openai/plugins、Pi-Bench、MCPZoo、仓库更名等）
- FACT_AUDIT.md 逐条记录（Active 85 / Slowing 5 / Deprecated 1 / 证据不足 2 / Reference 1）

### 图形系统
- 32 张图逐张 Read 视觉审查
- 4 张修复：F01（文字重叠）、F02（方框重叠）、F25（角色名重叠）、F31（文字溢出）
- VISUAL_QA.md 逐张记录

### Word 工程
- 修复页眉 STYLEREF 错误（改为静态文本"教程正文"）
- TOC 正确生成（Heading 1-3）
- PDF 导出 196 页，封面/目录/正文视觉检查通过
- audit.py 0 错误

### 新增文件
- examples/WORKLOG.md, TASKS.md, PROGRESS.md, DECISIONS.md
- examples/automation/daily_monitor.py, email_triage.py
- examples/my-agent/（agent.py, tools.py, test_agent.py, eval.py, README.md）

## v1.0.0 (2026-09-18)

- 初版发布：11 Part 教程、32 张图、98 条资源索引、Word 文档（commit 4cd733e → 1698906，修复附录 B 空名称列、移除临时锁文件）
