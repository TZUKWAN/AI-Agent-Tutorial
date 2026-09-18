#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agent.py — my-agent：一个最小但真实可运行的 Agent。

它演示 PART 10 讲的六个零件，且**没有 API Key 也能跑**（确定性规则引擎模式）：

  1. System Prompt   —— 岗位说明书，内置默认值，也可从文件加载
  2. Tools           —— 调用 tools.py 里的 read_file / calculator / now
  3. Context         —— 维护当前对话历史
  4. State           —— 任务状态落到 state.json
  5. Human Approval  —— 危险操作（删除/发送/覆盖）前停下来等人确认
  6. Logging         —— 每一步写 agent.log

交互用法：
  python agent.py
  > 现在几点
  > 计算 (12+8)*3
  > 读文件 state.json
  > 删除 config.bak     （会触发人工审批）

非交互测试请用 test_agent.py / eval.py。
"""

from __future__ import annotations

import json
import logging
import re
import sys
from pathlib import Path

from tools import TOOLS

BASE_DIR = Path(__file__).resolve().parent
STATE_PATH = BASE_DIR / "state.json"
LOG_PATH = BASE_DIR / "agent.log"
SYSTEM_PROMPT_PATH = BASE_DIR / "system_prompt.txt"
SKILLS_DIR = BASE_DIR / "skills"

DEFAULT_SYSTEM_PROMPT = (
    "你是一个助教式 Agent，服务于零基础学习者。"
    "你能做三件事：查当前时间、做算术计算、读取工作目录里的文本文件。"
    "凡是删除、发送、覆盖类的动作，一律先请求人工批准，不得自行执行。"
)

# 危险动作关键词：命中即走人工审批
DANGEROUS_PATTERNS = ["删除", "删掉", "发送", "发邮件", "覆盖", "清空", "删除文件", "rm "]


class MyAgent:
    def __init__(self, system_prompt: str | None = None):
        # 1. System Prompt：优先读文件，否则用默认值
        if system_prompt is not None:
            self.system_prompt = system_prompt
        elif SYSTEM_PROMPT_PATH.exists():
            self.system_prompt = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
        else:
            self.system_prompt = DEFAULT_SYSTEM_PROMPT

        # 3. Context：当前对话历史
        self.history: list[dict] = []
        # 4. State：从 state.json 恢复
        self.state = self._load_state()
        # 加载 skills/ 目录下的技能清单（教学简化：只解析 name/description）
        self.skills = self._load_skills()

        # 6. Logging
        self.logger = logging.getLogger("my_agent")
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            fh = logging.FileHandler(LOG_PATH, encoding="utf-8")
            fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
            self.logger.addHandler(fh)

    # ---- State 读写 ------------------------------------------------------
    def _load_state(self) -> dict:
        if STATE_PATH.exists():
            try:
                return json.loads(STATE_PATH.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        return {"task_status": "idle", "turns": 0, "last_message": None}

    def _save_state(self) -> None:
        STATE_PATH.write_text(
            json.dumps(self.state, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # ---- Skills 加载（教学简化：本地文件扫描，非远程注册中心） ----------
    @staticmethod
    def _load_skills() -> list[dict]:
        """扫描 skills/*.md，解析 frontmatter 里的 name/description。

        这是教学简化版：只认 `---` 包裹的 name:/description: 两行，
        不做完整 YAML 解析，也不联网拉取技能。
        """
        skills: list[dict] = []
        if not SKILLS_DIR.exists():
            return skills
        for path in sorted(SKILLS_DIR.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            name = path.stem
            description = ""
            if text.startswith("---"):
                parts = text.split("---", 2)
                if len(parts) >= 3:
                    for line in parts[1].splitlines():
                        if line.strip().lower().startswith("name:"):
                            name = line.split(":", 1)[1].strip() or name
                        elif line.strip().lower().startswith("description:"):
                            description = line.split(":", 1)[1].strip()
            skills.append({"file": path.name, "name": name, "description": description})
        return skills

    # ---- 意图路由（确定性规则引擎） --------------------------------------
    def _route(self, user_text: str) -> dict:
        """把用户输入路由到一个工具或一条策略。返回动作字典。"""
        text = user_text.strip()

        # 危险动作：优先拦截，走人工审批
        if any(p in text for p in DANGEROUS_PATTERNS):
            return {"action": "approval", "desc": text}

        # 时间意图
        if re.search(r"(几点|时间|现在|今天.*日期|what time)", text, re.IGNORECASE):
            return {"action": "tool", "tool": "now", "arg": None}

        # 计算意图：去掉“计算/算一下/calculate”后，把剩下的当表达式
        m = re.search(r"(?:计算|算一下|算算|calculate)[:：]?\s*(.+)", text, re.IGNORECASE)
        if m:
            return {"action": "tool", "tool": "calculator", "arg": m.group(1).strip()}
        # 纯算术表达式（如 "12*3+5"）也直接算
        if re.fullmatch(r"[0-9\s+\-*/%().]+", text):
            return {"action": "tool", "tool": "calculator", "arg": text}

        # 读文件意图：“读文件 xxx”
        m = re.search(r"(?:读|打开|查看)(?:一下)?文件[:：]?\s*(\S+)", text)
        if m:
            return {"action": "tool", "tool": "read_file", "arg": m.group(1)}

        # 检索笔记意图：在 docs/ 下关键词检索（教学简化版 RAG）
        if re.search(r"(检索|查笔记|找笔记|搜索笔记|相关笔记|笔记里)", text):
            return {"action": "tool", "tool": "search_notes", "arg": text}

        return self._fallback(text)

    def _fallback(self, text: str) -> dict:
        return {
            "action": "reply",
            "text": (
                "我目前能做这些事：查时间、做算术计算（说“计算 2+3*4”）、"
                "读文件（说“读文件 xxx.txt”）、检索笔记（说“检索笔记 …”）。"
                "删除/发送类动作我会先请你确认。"
            ),
        }

    # ---- 主对话循环 ------------------------------------------------------
    def chat(self, user_text: str, approval_callback=None) -> str:
        self.history.append({"role": "user", "text": user_text})
        self.state["turns"] += 1
        self.state["task_status"] = "running"
        self.state["last_message"] = user_text
        self.logger.info("用户输入：%s", user_text)

        route = self._route(user_text)

        if route["action"] == "reply":
            answer = route["text"]

        elif route["action"] == "tool":
            func, _ = TOOLS[route["tool"]]
            result = func(route["arg"]) if route["arg"] is not None else func()
            self.logger.info("调用工具 %s 参数=%s -> %s", route["tool"], route["arg"], result)
            if result["ok"]:
                answer = f"[工具:{route['tool']}] {result['result']}"
            else:
                answer = f"[工具:{route['tool']}] 失败：{result['error']}"

        elif route["action"] == "approval":
            # 5. Human Approval：危险动作前停下等人
            approved = self._ask_approval(route["desc"], approval_callback)
            if approved:
                answer = f"已获人工批准：你要求执行“{route['desc']}”。本最小示例仅记录批准，不真正执行删除/发送。"
                self.logger.warning("危险动作已获批准：%s", route["desc"])
            else:
                answer = f"人工拒绝：未执行“{route['desc']}”。"
                self.logger.warning("危险动作被拒绝：%s", route["desc"])
        else:
            answer = "无法识别的指令。"

        self.history.append({"role": "assistant", "text": answer})
        self.state["task_status"] = "done"
        self._save_state()
        self.logger.info("回复：%s", answer)
        return answer

    def _ask_approval(self, desc: str, callback) -> bool:
        """测试时注入 callback(desc)->bool；交互时用 input()。"""
        if callback is not None:
            return bool(callback(desc))
        try:
            ans = input(f"[人工审批] 检测到危险动作：{desc}\n  批准？(y/N): ").strip().lower()
            return ans in {"y", "yes"}
        except EOFError:
            return False


def main():
    agent = MyAgent()
    print("my-agent 已启动（输入 quit 退出）")
    print(f"System Prompt：{agent.system_prompt}\n")
    while True:
        try:
            user = input("你：").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user.lower() in {"quit", "exit", "退出"}:
            break
        if not user:
            continue
        print("Agent：", agent.chat(user))
    print("再见。")


if __name__ == "__main__":
    main()
