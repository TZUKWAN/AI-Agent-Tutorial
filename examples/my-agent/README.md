# my-agent：一个最小但真实可运行的 Agent

这是《AI Agent 零基础工作方法教程》PART 10 的配套项目。它用纯 Python 标准库实现，
**不需要 API Key、不需要联网、不需要 pip 安装任何东西**，就能在你电脑上跑起来。
它把 PART 10 讲的六个核心零件各落了一处代码，让你看见"一个 Agent 到底由什么拼成"。

## 它包含什么

| 文件 | 作用 | 对应 PART 10 的零件 |
|------|------|---------------------|
| `agent.py` | 主程序：意图路由、对话循环、状态保存、人工审批、技能加载 | Runtime / Context / State / Human-in-the-loop |
| `tools.py` | 工具：读文件、安全计算器、查时间、关键词检索笔记 | Tool / Tool Schema |
| `pipeline.py` | Planner→Executor→Evaluator 三段式流程 | Planning / Execution / Evaluation |
| `skills/summarize.md` | 一个技能文件（name/description/instructions） | Skill |
| `docs/note_*.md` | 4 篇小型笔记，供检索 | Knowledge Base |
| `system_prompt.txt` | 岗位说明书（可改） | System Prompt |
| `state.json` | 运行时状态（自动读写） | State |
| `test_agent.py` | 冒烟测试脚本 | Test |
| `eval.py` | 评测脚本，输出通过/失败 | Evaluation |
| `agent.log` | 运行日志（自动生成） | Observability |

## 环境要求

- Windows / macOS / Linux 均可
- Python 3.9 及以上（本机实测 Python 3.14）
- 无第三方依赖

## 三步跑起来

```powershell
cd examples\my-agent

# 1. 跑测试（确认环境正常）
python test_agent.py

# 2. 跑评测（看用例通过情况）
python eval.py

# 3. 交互式和它对话
python agent.py
```

交互式对话示例：

```
你：现在几点了
Agent：[工具:now] 2026-09-18 18:38:06
你：计算 (12+8)*3
Agent：[工具:calculator] 60
你：读文件 system_prompt.txt
Agent：[工具:read_file] 你是一个助教式 Agent……
你：删除旧备份 config.bak
Agent：[人工审批] 检测到危险动作：删除旧备份 config.bak
  批准？(y/N):
```

输入 `quit` 退出。

## 真实现 vs 教学简化（务必诚实区分）

| 能力 | 本项目怎么实现 | 性质 | 证据 |
|------|----------------|------|------|
| 工具调用（计算器/读文件/时间） | 真实函数 + AST 安全沙箱，真实执行 | **真实现** | `test_agent.py` 14 项断言全过 |
| 关键词检索笔记（RAG） | docs/ 真实读取 + 词频打分，真实返回结果 | **真实现（但检索算法是教学简化）** | `test_agent.py` 检索断言 |
| Skills 加载 | 真实扫描 `skills/*.md`、解析 frontmatter | **真实现（但技能来源是本地文件）** | `agent.skills` 加载断言 |
| Planner→Executor→Evaluator | 真实串起规划/执行/断言，真实跑通 | **真实现（但 Planner 是模板不是 LLM）** | `pipeline.run_task` 断言 |
| 日志落盘 | 真实写 `agent.log` | **真实现** | 仓库内 `agent.log` |
| RAG 检索算法 | 词频打分（字面命中），**不是向量/嵌入检索** | 教学简化 | 见 `tools.search_notes` 注释 |
| Planner | 关键词模板生成步骤，**不是 LLM 规划** | 教学简化 | 见 `pipeline.plan` 注释 |
| Skill 体系 | 读本地 `.md`，**不是远程技能市场 / 自动加载第三方技能** | 教学简化 | 见 `MyAgent._load_skills` |
| 意图路由 | 正则关键词路由，**不是 Function Calling** | 教学简化 | 见 `agent._route` |

## LLM 模式什么时候启用

当前是**确定性工具模式**：不需要任何 API Key，`python test_agent.py` 与 `python eval.py`
即可跑通并全部通过。它适合用来理解 Agent 的零件拆分。

要切换到真正的大模型模式，需要满足：

1. **配置 API Key**（如 OpenAI / 兼容接口的 `API_KEY` 环境变量）；
2. 把 `agent._route` 的正则路由替换为 LLM 输出 JSON 的 Function Calling 解析；
3. 把 `pipeline.plan` 的模板替换为 LLM 规划；
4. 把 RAG 从词频打分换成嵌入向量检索。

在没有 API Key 之前，本项目的全部测试与评测都应能离线跑过。

## 六个零件怎么对应到代码

1. **System Prompt**：`system_prompt.txt`。改这个文件，下次启动它就用新的岗位说明。
2. **Tools**：`tools.py` 里的 `read_file / calculator / now / search_notes`，并在 `TOOLS` 注册表登记。
3. **Context**：`MyAgent.history` 列表，存当前对话每一轮。
4. **State**：`state.json`，每次对话结束自动落盘，记录轮次和任务状态。
5. **Human Approval**：遇到"删除/发送/覆盖"类指令，`_ask_approval` 会停下来问你 `y/N`。
6. **Logging**：所有动作写进 `agent.log`。
7. **Skills**：`agent._load_skills` 扫描 `skills/` 目录，加载技能清单。
8. **Planning/Execution/Evaluation**：`pipeline.py` 用模板规划、顺序执行、确定性断言。

## 安全设计（务必理解）

- `calculator` 用 AST 白名单解析，`__import__('os').system(...)` 这类注入会被直接拒绝。
- `read_file` 被限制在项目目录内，`../../etc/passwd` 这类越界路径会被拒绝。
- 删除、发送类动作**只记录"已批准"，不真正执行**——这是一个教学示例，不真删真发。

## 已知边界（诚实说明）

- 它是**规则引擎**，不是大模型：只会识别固定句式，换个说法它就走兜底回复。
- 它不联网、不调用外部 API；笔记检索是**词频打分**，没有记忆向量库。
- 它的"工具调用"是关键词路由，不是真正的 Function Calling。
- Planner 是模板生成，不是 LLM 规划；Skill 只从本地 `skills/` 读，不是技能市场。
- 这些边界正是 PART 10 讲的"真要接大模型时，哪些零件要换成现成框架"的起点。
