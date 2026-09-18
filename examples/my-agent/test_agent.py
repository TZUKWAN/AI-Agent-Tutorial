#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_agent.py — my-agent 的冒烟测试（不依赖网络、不依赖 API Key、不依赖人工输入）。

覆盖：
  - 时间工具
  - 计算器工具（正常 + 恶意注入被拒）
  - 读文件工具（工作目录内成功 / 越界拒绝）
  - 危险动作触发人工审批（注入自动同意 / 自动拒绝两种回调）
  - 兜底回复
  - State 落到 state.json

运行：python test_agent.py
"""

from __future__ import annotations

import json
from pathlib import Path

from agent import MyAgent

BASE_DIR = Path(__file__).resolve().parent
STATE_PATH = BASE_DIR / "state.json"


def check(name: str, cond: bool, detail: str = "") -> None:
    mark = "PASS" if cond else "FAIL"
    print(f"[{mark}] {name}{('  -> ' + detail) if detail else ''}")
    if not cond:
        raise SystemExit(1)


def main() -> None:
    # 每次测试前重置状态文件，保证可重复
    if STATE_PATH.exists():
        STATE_PATH.unlink()

    agent = MyAgent()

    # 1. 时间
    out = agent.chat("现在几点了")
    check("时间工具返回当前时间", "[工具:now]" in out, out)

    # 2. 计算器：2+3*4 = 14
    out = agent.chat("计算 2+3*4")
    check("计算器 2+3*4=14", "[工具:calculator] 14" in out, out)

    # 3. 计算器：纯表达式 10/2 = 5.0
    out = agent.chat("10/2")
    check("计算器 10/2=5.0", "5.0" in out, out)

    # 4. 恶意表达式被安全拒绝
    out = agent.chat("计算 __import__('os').system('echo hi')")
    check("恶意表达式被拒", "失败" in out or "不允许" in out, out)

    # 5. 读文件：读本项目存在的 tools.py
    out = agent.chat("读文件 tools.py")
    check("读工作目录内文件成功", "[工具:read_file]" in out and "calculator" in out, out[:80])

    # 6. 越界读文件被拒
    out = agent.chat("读文件 ../../etc/passwd")
    check("越界读文件被拒", "拒绝" in out or "失败" in out, out)

    # 7. 危险动作 + 自动同意
    out = agent.chat("删除旧备份 config.bak", approval_callback=lambda desc: True)
    check("危险动作-自动同意", "已获人工批准" in out, out)

    # 8. 危险动作 + 自动拒绝
    out = agent.chat("发送全部客户邮件", approval_callback=lambda desc: False)
    check("危险动作-自动拒绝", "人工拒绝" in out, out)

    # 9. 兜底
    out = agent.chat("今天天气怎么样")
    check("未知指令走兜底", "我目前只能" in out, out)

    # 10. State 落盘
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    check("State 已落盘且轮次正确", state["turns"] == 9 and state["task_status"] == "done",
          f"turns={state['turns']}")

    print("\n全部测试通过。")


if __name__ == "__main__":
    main()
