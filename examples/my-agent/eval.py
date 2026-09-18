#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eval.py — my-agent 的评测脚本。

它把一组固定测试用例跑一遍，每个用例断言“期望出现在回复里”的片段，
最后输出通过/失败统计。对应 PART 10 的 Evaluation：改完 Agent 后跑同一套用例，
看有没有退化。

除对话用例外，还额外评测：
  - skills/ 技能加载
  - Planner->Executor->Evaluator 三段式流程

运行：python eval.py
"""

from __future__ import annotations

from agent import MyAgent
from pipeline import run_task
from test_agent import STATE_PATH, check


# (用户输入, 期望片段, 审批回调)
CASES = [
    ("现在几点了", "工具:now", None),
    ("计算 1+2*3", "7", None),
    ("计算 100/4", "25", None),
    ("读文件 state.json", "工具:read_file", None),
    ("删除临时文件", "已获人工批准", lambda desc: True),
    ("发邮件给客户", "人工拒绝", lambda desc: False),
    ("讲个笑话", "我目前能做这些事", None),
    # 新增能力：检索笔记
    ("检索笔记 Agent 零件", "工具:search_notes", None),
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
    print(f"对话用例评测完成：{passed}/{total} 通过，{failed} 失败。")

    # ---- 新增能力评测：skills 加载 + 三段式流程 ----
    skill_names = {s["name"] for s in agent.skills}
    if "summarize" in skill_names:
        passed += 1
        check("技能加载[summarize]", True)
    else:
        failed += 1
        check(f"技能加载[summarize] 缺失，实际 {skill_names}", False)

    # 三段式：计算 + 检索，数值与列表双断言
    verdict = run_task(
        "计算 6*7 并检索笔记 RAG",
        [
            {"tool": "calculator", "assert": {"type": "number", "equals": 42}},
            {"tool": "search_notes", "assert": {"type": "list", "min_len": 1, "contains": "RAG"}},
        ],
    )
    if verdict["verdict"]["passed"]:
        passed += 1
        check("三段式流程[计算6*7=42+检索RAG]", True)
    else:
        failed += 1
        check("三段式流程", False)

    total += 2
    print("-" * 50)
    print(f"总评测完成：{passed}/{total} 通过，{failed} 失败。")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
