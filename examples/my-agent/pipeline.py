#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pipeline.py — my-agent 的 Planner / Executor / Evaluator 三段式（教学简化版）。

注意边界（README 会再次强调）：
  - Planner 是**关键词模板**规划，不是 LLM 规划。
  - Executor 只是按顺序调用 tools.py 里注册的工具，没有 ReAct 循环。
  - Evaluator 只做确定性断言（类型 / 关键词 / 数值），不做语义打分。

没有 API Key 也能跑通完整流程。
"""

from __future__ import annotations

import re
from typing import Any

from tools import TOOLS


# ---- Planner：按关键词模板把任务翻译成步骤清单 ---------------------------
def plan(task: str) -> list[dict]:
    """根据任务文本里的关键词，生成一张确定性步骤清单。

    返回 [{"tool": str, "arg": str|None}, ...]，顺序即执行顺序。
    """
    steps: list[dict] = []

    # 计算意图：“计算 2+3*4” —— 只截取连续的算术片段，避免把后半句中文也塞进去
    m = re.search(r"(?:计算|算一下|算算|calculate)[:：]?\s*([0-9\s+\-*/%().]+)", task, re.IGNORECASE)
    if m:
        steps.append({"tool": "calculator", "arg": m.group(1).strip()})
    elif re.fullmatch(r"[0-9\s+\-*/%().]+", task.strip()):
        steps.append({"tool": "calculator", "arg": task.strip()})

    # 检索笔记意图
    if re.search(r"(笔记|检索|查一下笔记|搜索笔记|note)", task, re.IGNORECASE):
        # 把整个任务文本作为查询词（教学版不做复杂抽取）
        steps.append({"tool": "search_notes", "arg": task})

    # 时间意图
    if re.search(r"(几点|时间|现在|今天.*日期)", task):
        steps.append({"tool": "now", "arg": None})

    # 读文件意图
    m = re.search(r"(?:读|打开|查看)(?:一下)?文件[:：]?\s*(\S+)", task)
    if m:
        steps.append({"tool": "read_file", "arg": m.group(1)})

    return steps


# ---- Executor：按步骤清单调用工具 ----------------------------------------
def execute(steps: list[dict]) -> list[dict]:
    results: list[dict] = []
    for step in steps:
        tool_name = step["tool"]
        arg = step.get("arg")
        func, _desc = TOOLS[tool_name]
        tool_out = func(arg) if arg is not None else func()
        results.append(
            {
                "tool": tool_name,
                "arg": arg,
                "ok": tool_out.get("ok"),
                "result": tool_out.get("result"),
                "error": tool_out.get("error"),
            }
        )
    return results


# ---- Evaluator：对每步结果做确定性断言 ------------------------------------
def _assert_one(result: Any, assertion: dict) -> tuple[bool, str]:
    """对单个工具结果做一条断言，返回 (是否通过, 说明)。"""
    want_type = assertion.get("type")
    if want_type == "number":
        if not isinstance(result, (int, float)):
            return False, f"期望 number，实际 {type(result).__name__}={result!r}"
    elif want_type == "string":
        if not isinstance(result, str):
            return False, f"期望 string，实际 {type(result).__name__}={result!r}"
    elif want_type == "list":
        if not isinstance(result, list):
            return False, f"期望 list，实际 {type(result).__name__}"
        if "min_len" in assertion and len(result) < assertion["min_len"]:
            return False, f"列表长度 {len(result)} < 期望 {assertion['min_len']}"
    elif want_type == "bool":
        if not isinstance(result, bool):
            return False, f"期望 bool，实际 {type(result).__name__}"

    if "equals" in assertion:
        if result != assertion["equals"]:
            return False, f"期望等于 {assertion['equals']!r}，实际 {result!r}"

    if "contains" in assertion:
        needle = assertion["contains"]
        container = result if isinstance(result, str) else str(result)
        if needle not in container:
            return False, f"结果不包含期望片段 {needle!r}"

    return True, "ok"


def evaluate(results: list[dict], expectations: list[dict]) -> dict:
    """对照 expectations 评估执行结果。

    expectations 每项形如：{"tool": "calculator", "assert": {"type":"number","equals":14}}
    返回 {"passed": bool, "checks": [...]}。
    """
    checks = []
    passed = True
    for exp in expectations:
        tool_name = exp["tool"]
        # 找到该工具对应的那一步结果
        match = next((r for r in results if r["tool"] == tool_name), None)
        if match is None:
            passed = False
            checks.append({"tool": tool_name, "ok": False, "detail": "未执行该工具"})
            continue
        ok, detail = _assert_one(match["result"], exp["assert"])
        if not ok or not match["ok"]:
            passed = False
        checks.append(
            {"tool": tool_name, "ok": ok and bool(match["ok"]), "detail": detail}
        )
    return {"passed": passed, "checks": checks}


# ---- 串起来：一次完整的 Planner->Executor->Evaluator ---------------------
def run_task(task: str, expectations: list[dict]) -> dict:
    steps = plan(task)
    results = execute(steps)
    verdict = evaluate(results, expectations)
    return {
        "task": task,
        "steps": steps,
        "results": results,
        "verdict": verdict,
    }
