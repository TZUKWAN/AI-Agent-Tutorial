# my-agent：一个最小但真实可运行的 Agent

这是《AI Agent 零基础工作方法教程》PART 10 的配套项目。它用纯 Python 标准库实现，
**不需要 API Key、不需要联网、不需要 pip 安装任何东西**，就能在你电脑上跑起来。
它把 PART 10 讲的六个核心零件各落了一处代码，让你看见"一个 Agent 到底由什么拼成"。

## 它包含什么

| 文件 | 作用 | 对应 PART 10 的零件 |
|------|------|---------------------|
| `agent.py` | 主程序：意图路由、对话循环、状态保存、人工审批 | Runtime / Context / State / Human-in-the-loop |
| `tools.py` | 三个工具：读文件、安全计算器、查时间 | Tool / Tool Schema |
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

## 六个零件怎么对应到代码

1. **System Prompt**：`system_prompt.txt`。改这个文件，下次启动它就用新的岗位说明。
2. **Tools**：`tools.py` 里的 `read_file / calculator / now`，并在 `TOOLS` 注册表登记。
3. **Context**：`MyAgent.history` 列表，存当前对话每一轮。
4. **State**：`state.json`，每次对话结束自动落盘，记录轮次和任务状态。
5. **Human Approval**：遇到"删除/发送/覆盖"类指令，`_ask_approval` 会停下来问你 `y/N`。
6. **Logging**：所有动作写进 `agent.log`。

## 安全设计（务必理解）

- `calculator` 用 AST 白名单解析，`__import__('os').system(...)` 这类注入会被直接拒绝。
- `read_file` 被限制在项目目录内，`../../etc/passwd` 这类越界路径会被拒绝。
- 删除、发送类动作**只记录"已批准"，不真正执行**——这是一个教学示例，不真删真发。

## 已知边界（诚实说明）

- 它是**规则引擎**，不是大模型：只会识别固定句式，换个说法它就走兜底回复。
- 它不联网、不调用外部 API、没有记忆向量库。
- 它的"工具调用"是关键词路由，不是真正的 Function Calling。
- 这些边界正是 PART 10 讲的"真要接大模型时，哪些零件要换成现成框架"的起点。
