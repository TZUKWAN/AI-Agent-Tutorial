# CHANGELOG

## v1.1.1 (2026-09-18)

### 真实案例补齐
- 新增 examples/labs/lab_c_office/：真实Office闭环（CSV→Excel→Word→汇报要点）
- 新增 examples/labs/lab_e_data/：真实数据分析闭环（脏数据→清洗→统计→图→报告）
- 新增 examples/labs/labf_project/：真实开源项目（colorama clone→改功能→测试→commit）
- daily_monitor.py新增live模式：真实GitHub API调用（HTTP 200，10条Release）
- my-agent补齐：Skill加载、RAG关键词检索、Planner/Executor/Evaluator、test 14/14 eval 10/10

### 工程修复
- render_full.py/export_pdf.ps1硬编码路径改为相对路径
- requirements.txt补充pymupdf/openpyxl
- README删除过时V1.2表述，新增构建与QA环境要求
- QA_REPORT重写为严格PASS/PARTIAL/FAIL表

## v1.1.0 (2026-09-18)

### 正文深度重构
- PART 0-3：概念边界改为"能力递进光谱"（非排他定义）；新增1.7节"四级权限实测"；新增3.15节"中断后如何续跑"
- examples/：新增WORKLOG.md/TASKS.md/PROGRESS.md/DECISIONS.md模板（带真实示例）
- PART 4-5：新增4.14节"故障注入实验"（假引用/错误数据/放错文件/失效链接/测试假完成）
- PART 6：重写为五层认知结构（6.1-6.20），每概念用"概念本身→常见实现→平台差异→掌握程度→例子"五段模板
- PART 7：新增真实安装演示（Skill用.claude/skills、MCP用@modelcontextprotocol/server-filesystem、Connector用gh CLI scopes）
- PART 8：七个LAB各加旗舰项目模板；LAB B删除无依据表述并新增AI使用政策查找方法
- PART 9：新增daily_monitor.py（GitHub Releases监控）和email_triage.py（邮件审批工作流）
- PART 10：新增examples/my-agent/完整Agent项目（无API Key可运行，test 10/10 eval 7/7）

### 资源核验
- 98条资源全部重新联网核验（gh api + web.fetch）
- 12项关键修正（openai/plugins、Pi-Bench、MCPZoo、仓库更名等）
- FACT_AUDIT.md逐条记录

### 图形系统
- 32张图逐张Read视觉审查
- 4张修复：F01（文字重叠）、F02（方框重叠）、F25（角色名重叠）、F31（文字溢出）
- VISUAL_QA.md逐张记录

### Word工程
- 修复页眉STYLEREF错误（改为静态文本"教程正文"）
- TOC正确生成（Heading 1-3）
- PDF导出196页，封面/目录/正文视觉检查通过
- audit.py 0错误

### 新增文件
- examples/WORKLOG.md, TASKS.md, PROGRESS.md, DECISIONS.md
- examples/automation/daily_monitor.py, email_triage.py
- examples/my-agent/（agent.py, tools.py, test_agent.py, eval.py, README.md）

## v1.0.0 (2026-09-18)
- 初版发布：11 Part教程、32张图、98条资源索引、Word文档
