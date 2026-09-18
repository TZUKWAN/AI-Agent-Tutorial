#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools.py — my-agent 的工具函数集合。

三个工具：
  - read_file(rel_path)  在允许的工作目录内读一个文本文件
  - calculator(expr)    安全计算一个算术表达式（用 ast 白名单，禁止任意函数调用）
  - now()               返回当前日期时间

每个工具都返回 dict：{"ok": bool, "result": ..., "error": ...}，
这样上层 Agent 可以统一处理成功与失败。
"""

from __future__ import annotations

import ast
import operator
import re
from datetime import datetime
from pathlib import Path

# Agent 允许读写的根目录（本项目目录），防止 read_file 读到系统任意位置
WORKSPACE = Path(__file__).resolve().parent
DOCS_DIR = WORKSPACE / "docs"


# ---- 安全计算器：只允许算术运算 -----------------------------------------
_ALLOWED_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_ALLOWED_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _eval_node(node):
    if isinstance(node, ast.Constant):  # Python 3.8+ 常量（3.14 已移除 ast.Num）
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"不允许的常量类型：{type(node.value).__name__}")
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BIN_OPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_BIN_OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARY_OPS:
        return _ALLOWED_UNARY_OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError("表达式只允许数字和 + - * / // % ** 运算")


def calculator(expr: str):
    """安全计算算术表达式。任何非算术语法直接拒绝。"""
    try:
        tree = ast.parse(expr, mode="eval")
        value = _eval_node(tree.body)
        return {"ok": True, "result": value, "error": None}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "result": None, "error": f"计算失败：{exc}"}


# ---- 文件读取（限定工作目录） -------------------------------------------
def read_file(rel_path: str, max_bytes: int = 8000):
    """在 WORKSPACE 内读取文本文件。拒绝越出工作目录的路径。"""
    target = (WORKSPACE / rel_path).resolve()
    try:
        target.relative_to(WORKSPACE.resolve())
    except ValueError:
        return {"ok": False, "result": None, "error": f"拒绝访问工作目录之外的文件：{rel_path}"}

    if not target.exists():
        return {"ok": False, "result": None, "error": f"文件不存在：{rel_path}"}

    text = target.read_text(encoding="utf-8", errors="replace")
    if len(text) > max_bytes:
        text = text[:max_bytes] + "\n...（已截断）"
    return {"ok": True, "result": text, "error": None}


# ---- 时间 ----------------------------------------------------------------
def now():
    """返回当前日期时间字符串。"""
    return {"ok": True, "result": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "error": None}


# ---- 轻量笔记检索（教学简化版：关键词词频打分，非向量检索） -----------------
_CJK = r"\u4e00-\u9fff"


def _tokenize(text: str) -> list[str]:
    """极简分词：英文按 [a-z0-9_] 成词；中文按单字 + 相邻二元组。

    这是刻意的教学简化：不做停用词、不做词形还原、不做向量嵌入。
    """
    text = text.lower()
    tokens: list[str] = []
    # 英文/数字词
    for m in re.findall(r"[a-z0-9_]+", text):
        tokens.append(m)
    # 中文：单字 + 二元组
    cjk_chars = re.findall(f"[{_CJK}]", text)
    tokens.extend(cjk_chars)
    tokens.extend(
        "".join(pair) for pair in zip(cjk_chars, cjk_chars[1:])
    )
    return tokens


def _load_docs() -> list[dict]:
    docs = []
    if not DOCS_DIR.exists():
        return docs
    for path in sorted(DOCS_DIR.glob("*.md")):
        docs.append({"path": path.name, "text": path.read_text(encoding="utf-8")})
    return docs


def search_notes(query: str, top_k: int = 3):
    """在 docs/ 目录下按关键词词频打分检索相关笔记。

    教学简化版：不是向量检索，不理解语义，只按查询词在文档中的字面命中次数排序。
    返回 {"ok", "result": [{"file","score","snippet"}], "error"}。
    """
    if not query or not query.strip():
        return {"ok": False, "result": None, "error": "查询为空"}
    q_tokens = _tokenize(query)
    if not q_tokens:
        return {"ok": False, "result": None, "error": "查询未解析出任何词"}

    docs = _load_docs()
    if not docs:
        return {"ok": True, "result": [], "error": None}

    scored = []
    for doc in docs:
        d_tokens = _tokenize(doc["text"])
        d_counter: dict[str, int] = {}
        for t in d_tokens:
            d_counter[t] = d_counter.get(t, 0) + 1
        score = sum(d_counter.get(tok, 0) for tok in q_tokens)
        if score > 0:
            snippet = doc["text"].strip().splitlines()[0][:60]
            scored.append({"file": doc["path"], "score": score, "snippet": snippet})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return {"ok": True, "result": scored[:top_k], "error": None}


# 工具注册表：名字 -> (函数, 一句话说明)
TOOLS = {
    "read_file": (read_file, "读取工作目录内的文本文件，参数：相对路径"),
    "calculator": (calculator, "计算算术表达式，参数：如 '2+3*4'"),
    "now": (now, "返回当前日期时间，无参数"),
    "search_notes": (search_notes, "在 docs/ 下按关键词检索笔记，参数：查询词"),
}


if __name__ == "__main__":
    # 简单自检
    print(calculator("2+3*4"))
    print(calculator("__import__('os').system('echo hi')"))  # 应被拒绝
    print(now())
