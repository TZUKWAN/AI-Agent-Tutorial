#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eval.py — my-agent 的评测脚本。

它把一组固定测试用例跑一遍，每个用例断言“期望出现在回复里”的片段，
最后输出通过/失败统计。对应 PART 10 的 Evaluation：改完 Agent 后跑同一套用例，
看有没有退化。

运行：python eval.py
"""

from __future__ import annotations

from agent import MyAgent
from test_agent import STATE_PATH, check


# (用户输入, 期望片段, 审批回调)
CASES = [
    ("现在几点了", "工具:now", None),
    ("计算 1+2*3", "7", None),
    ("计算 100/4", "25", None),
    ("读文件 state.json", "工具:read_file", None),
    ("删除临时文件", "已获人工批准", lambda desc: True),
    ("发邮件给客户", "人工拒绝", lambda desc: False),
    ("讲个笑话", "我目前只能", None),
]


def main() -> None:
    if STATE_PATH.exists():
        STATE_PATH.unlink()

    agent = MyAgent()
    passed = 0
    failed = 0

    for user_input, expect, cb in CASES:
        out = agent.chat(user_input, approval_callback=cb)
        ok = expect in out
        if ok:
            passed += 1
            check(f"用例[{user_input}]", True)
        else:
            failed += 1
            check(f"用例[{user_input}] 期望含“{expect}”，实际：{out[:60]}", False)

    total = len(CASES)
    print("-" * 50)
    print(f"评测完成：{passed}/{total} 通过，{failed} 失败。")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
