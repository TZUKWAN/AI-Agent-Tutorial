#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
email_triage.py — 邮件分类审批工作流（PART 9 案例 2 的完整可运行实现）

对应 PART 9 的第二个流程：
  读邮件（只读，可自动跑）→ 分类 → 起草回复草稿 → 写入 pending 队列（停住）
  → 人工审批（approve / reject）→ 发送（对外动作，必须人工点头）

安全设计：
  - 分类、起草全部是只读和本地动作，可以全自动跑；
  - “发送”是对外、不可逆动作，本脚本默认只把待发内容落进 outbox 日志，
    只有当环境变量 SMTP_HOST / SMTP_USER / SMTP_PASS 都配齐时才真正发信。
    也就是说：没有凭据 = 永远不会真的把邮件发出去。

子命令：
  python email_triage.py run                 # 扫描 emails/ 目录，分类+起草+入队
  python email_triage.py list                # 查看 pending 队列
  python email_triage.py approve <id>         # 人工批准某条草稿，尝试发送（无凭据则落 outbox 日志）
  python email_triage.py reject <id>         # 人工拒绝，标记为不回复

纯标准库实现，无需第三方依赖。
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import smtplib
import sys
import uuid
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EMAIL_DIR = BASE_DIR / "emails"
QUEUE_PATH = BASE_DIR / "pending.json"
LOG_PATH = BASE_DIR / "triage.log"
OUTBOX_PATH = BASE_DIR / "outbox.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("email_triage")


# ---- 规则分类（确定性，不依赖大模型） -----------------------------------
WORK_KEYWORDS = ["会议", "报告", "客户", "项目", "合同", "deadline", "截止",
                 "汇报", "需求", "评审", "面试", "周报", "方案", "签约"]
PERSONAL_KEYWORDS = ["生日", "聚会", "吃饭", "周末", "朋友", "家人", "婚礼",
                     "约吗", "近况"]
NOTICE_KEYWORDS = ["noreply", "no-reply", "通知", "alert", "发票", "账单",
                   "验证码", "newsletter", "订阅", "系统", "自动", "发票", "物流"]


def classify(subject: str, body: str) -> str:
    """按关键词把邮件分成 工作 / 个人 / 通知 三类。命中最多的类别胜出，平局归“通知”。"""
    text = f"{subject}\n{body}".lower()
    scores = {
        "工作": sum(1 for k in WORK_KEYWORDS if k.lower() in text),
        "个人": sum(1 for k in PERSONAL_KEYWORDS if k.lower() in text),
        "通知": sum(1 for k in NOTICE_KEYWORDS if k.lower() in text),
    }
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "通知"


def draft_reply(category: str, subject: str, sender: str) -> str:
    """按类别起草一段简短回复草稿。真实项目里这里可以换成调用大模型。"""
    if category == "工作":
        return (
            f"您好，收到您关于“{subject}”的邮件。我会在今天内梳理并回复具体进展，"
            f"如有紧急事项请直接电话联系。"
        )
    if category == "个人":
        return f"收到！关于“{subject}”的事，我们约个时间细聊，我这周方便。"
    return "（系统/通知类邮件，无需人工回复，已归档。）"


# ---- 邮件读取 ------------------------------------------------------------
def parse_mail_file(path: Path) -> dict:
    """读一个 .eml 或 .txt 文件，抽出发件人、主题、正文。

    .eml 用标准库 email 解析；.txt 简化为三行：FROM / SUBJECT / BODY。
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".eml":
        import email
        from email import policy
        msg = email.message_from_string(text, policy=policy.default)
        sender = str(msg.get("From", ""))
        subject = str(msg.get("Subject", ""))
        body = msg.get_body(("plain",))
        body_text = body.get_content() if body else text
    else:
        # 简化格式：第一行 FROM: ...，第二行 SUBJECT: ...，其余为正文
        lines = text.splitlines()
        sender = lines[0].replace("FROM:", "").strip() if lines else ""
        subject = lines[1].replace("SUBJECT:", "").strip() if len(lines) > 1 else ""
        body_text = "\n".join(lines[2:])
    return {"from": sender, "subject": subject, "body": body_text, "file": path.name}


# ---- 队列读写 ------------------------------------------------------------
def load_queue() -> list[dict]:
    if not QUEUE_PATH.exists():
        return []
    try:
        return json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def save_queue(queue: list[dict]) -> None:
    QUEUE_PATH.write_text(
        json.dumps(queue, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# ---- 子命令实现 ----------------------------------------------------------
def cmd_run() -> int:
    if not EMAIL_DIR.exists():
        log.error("邮件目录不存在：%s", EMAIL_DIR)
        return 1
    files = sorted([p for p in EMAIL_DIR.iterdir() if p.suffix.lower() in {".txt", ".eml"}])
    if not files:
        log.warning("邮件目录为空，没有可处理的邮件：%s", EMAIL_DIR)
        return 0

    queue = load_queue()
    seen_files = {item["source_file"] for item in queue}

    for path in files:
        if path.name in seen_files:
            continue  # 已经入队过，不重复处理
        mail = parse_mail_file(path)
        category = classify(mail["subject"], mail["body"])
        draft = draft_reply(category, mail["subject"], mail["from"])
        item = {
            "id": uuid.uuid4().hex[:8],
            "source_file": path.name,
            "from": mail["from"],
            "subject": mail["subject"],
            "category": category,
            "draft": draft,
            "status": "draft",           # draft / approved / sent / rejected
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        queue.append(item)
        log.info("已分类 %s -> [%s]，草稿入队 id=%s", path.name, category, item["id"])

    save_queue(queue)
    log.info("处理完成，队列共 %d 条待审批。", len([q for q in queue if q["status"] == "draft"]))
    return 0


def cmd_list() -> int:
    queue = load_queue()
    if not queue:
        print("（队列为空，先运行 python email_triage.py run）")
        return 0
    print(f"{'ID':<10}{'状态':<10}{'类别':<6}发件人 / 主题")
    print("-" * 70)
    for q in queue:
        print(f"{q['id']:<10}{q['status']:<10}{q['category']:<6}{q['from']} | {q['subject']}")
    return 0


def _find(queue: list[dict], item_id: str) -> dict | None:
    return next((q for q in queue if q["id"] == item_id), None)


def _try_send(item: dict) -> bool:
    """真正发信需要 SMTP 凭据。没有凭据时，把待发内容落进 outbox.log，绝不真发。"""
    host = os.environ.get("SMTP_HOST")
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASS")

    if not (host and user and password):
        with OUTBOX_PATH.open("a", encoding="utf-8") as f:
            f.write(
                f"\n[{datetime.now().isoformat(timespec='seconds')}] 待发（无 SMTP 凭据，未真正发送）\n"
                f"  收件人: {item['from']}\n"
                f"  主题: Re: {item['subject']}\n"
                f"  正文: {item['draft']}\n"
            )
        log.warning("未配置 SMTP 凭据，邮件已记入 outbox.log（未真正发送）。")
        return False

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = item["from"]
    msg["Subject"] = f"Re: {item['subject']}"
    msg.set_content(item["draft"])
    with smtplib.SMTP_SSL(host, 465, timeout=15) as s:
        s.login(user, password)
        s.send_message(msg)
    log.info("已通过 SMTP 发送给 %s", item["from"])
    return True


def cmd_approve(item_id: str) -> int:
    queue = load_queue()
    item = _find(queue, item_id)
    if not item:
        log.error("找不到 id=%s 的条目", item_id)
        return 1
    if item["status"] != "draft":
        log.error("id=%s 当前状态为 %s，不可重复审批", item_id, item["status"])
        return 1

    sent = _try_send(item)
    item["status"] = "sent" if sent else "approved"  # 无凭据时记为 approved，待人工外发
    item["approved_at"] = datetime.now().isoformat(timespec="seconds")
    save_queue(queue)
    log.info("id=%s 审批通过，状态 -> %s", item_id, item["status"])
    return 0


def cmd_reject(item_id: str) -> int:
    queue = load_queue()
    item = _find(queue, item_id)
    if not item:
        log.error("找不到 id=%s 的条目", item_id)
        return 1
    item["status"] = "rejected"
    item["rejected_at"] = datetime.now().isoformat(timespec="seconds")
    save_queue(queue)
    log.info("id=%s 已标记为不回复。", item_id)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="邮件分类审批工作流")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("run", help="扫描 emails/ 目录，分类+起草+入队")
    sub.add_parser("list", help="查看 pending 队列")
    p_app = sub.add_parser("approve", help="批准某条草稿并尝试发送")
    p_app.add_argument("id")
    p_rej = sub.add_parser("reject", help="拒绝某条草稿")
    p_rej.add_argument("id")

    args = parser.parse_args()
    if args.cmd == "run":
        return cmd_run()
    if args.cmd == "list":
        return cmd_list()
    if args.cmd == "approve":
        return cmd_approve(args.id)
    if args.cmd == "reject":
        return cmd_reject(args.id)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
