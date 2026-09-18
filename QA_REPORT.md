# QA_REPORT.md - V1.1 最终质量报告

> 日期：2026-09-18

## 逐条验收（PASS/FAIL）

### FAIL 1：正文深度重构 — PASS

| 子项 | 状态 | 证据 |
|------|------|------|
| PART 0-5 概念光谱修正 | PASS | Part0-3_基础入门.md 0.4节改为"能力递进光谱" |
| 权限实验（L1-L4） | PASS | 新增1.7节"四级权限实测" |
| 长任务中断恢复 | PASS | 新增3.15节"中断后如何续跑" |
| examples/模板文件 | PASS | WORKLOG.md/TASKS.md/PROGRESS.md/DECISIONS.md 均带真实示例 |
| 故障注入实验（5个） | PASS | Part4-5_验证与失败.md 新增4.14节 |
| PART 6 五层认知结构 | PASS | 6.1-6.20连续，五层：Model→记忆→感官→扩展→编排 |
| PART 7 真实安装演示 | PASS | 7.2.1 Skill（.claude/skills真实路径）、7.7.1 MCP（@modelcontextprotocol/server-filesystem）、7.8.1 Connector（gh CLI真实scopes） |
| PART 8 七个LAB旗舰项目 | PASS | A-G各加旗舰项目模板 |
| LAB B 科研政策修订 | PASS | 删除无依据表述，新增AI使用政策查找方法 |
| PART 9 真实自动化案例 | PASS | daily_monitor.py（GitHub Releases监控，三分支实测）+ email_triage.py（分类审批工作流，分类全对） |
| PART 10 真Agent构建 | PASS | examples/my-agent/：test_agent.py 10/10通过，eval.py 7/7通过，交互模式人工审批正常 |

### FAIL 2：98条资源逐条核验 — PASS

- Active 85 / Slowing 5 / Deprecated 1 / 证据不足 2 / Reference 1
- 12项关键修正（openai/plugins状态升级、Pi-Bench链接错误、MCPZoo数据更正、仓库更名等）
- 证据：FACT_AUDIT.md逐条记录，CSV已更新
- 所有GitHub数据来自 gh api repos/... 真实返回

### FAIL 3：32张图逐张视觉审查 — PASS

- 28张一次通过
- 4张修复后通过：F01（中英文字重叠）、F02（方框重叠）、F25（角色名重叠）、F31（文字溢出）
- 证据：VISUAL_QA.md逐张记录

### FAIL 4：Word PDF逐页视觉检查 — PASS

- PDF总页数：196页
- 封面：深蓝底白字，排版正常
- 目录：含Heading 1-3层级，页码正确
- 页眉："教程正文"静态文本（修复了STYLEREF错误）
- 正文：字体/行距/图注/表格均正常
- 附录C：最后一页正常结束
- word skill audit.py：0错误通过

### FAIL 5：真实案例走通证据 — PASS（部分限制如实标注）

| 操作 | 状态 | 证据 |
|------|------|------|
| daily_monitor.py | 实测通过 | 三分支：首跑建基准→检出新版→幂等静默 |
| email_triage.py | 实测通过 | 三条样例邮件分类全对，approve/reject正常 |
| my-agent test_agent.py | 实测通过 | 10/10断言PASS |
| my-agent eval.py | 实测通过 | 7/7通过 |
| my-agent交互模式 | 实测通过 | 人工审批y/N正常 |
| LAB F Clone/PR/Deploy | 未完成 | 如实标注：需账号和远端权限 |
| 邮件SMTP真发送 | 未完成 | 如实标注：需用户填入SMTP凭据 |

## 文档统计
- 总字数：96,584
- 段落数：3,945
- 标题数：473+
- 表格数：116+
- 图片数：32
- PDF页数：196
- 文件大小：4.5MB

## 构建可复现性
```powershell
pip install -r requirements.txt
python build_docx.py
```
从干净环境可从零复现。
