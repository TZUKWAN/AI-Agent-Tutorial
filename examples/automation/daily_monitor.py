#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
daily_monitor.py — 每日信息监控（PART 9 案例 1 的完整可运行实现）

工作流（对应 9.1-9.8 八个零件）：
  Schedule  : 由 Windows 任务计划程序（schtasks）每天定时调用本脚本
  Action    : 抓取目标 GitHub 仓库的 Releases（稳定只读数据源）
  Condition : 与昨日快照对比，只有“出现新 Release”才算有变化
  Notification: 有变化时写一份摘要文件；无变化静默退出
  Logging   : 每一轮都写 monitor.log，失败可追溯

本脚本只做只读抓取与本地比对，不对外发送任何消息，因此不需要人工审批节点。
纯标准库实现，无需 pip 安装任何第三方包。

用法示例：
  python daily_monitor.py                      # 默认监控 psf/requests 的 Releases
  python daily_monitor.py --repo pallets/click # 监控指定仓库
  python daily_monitor.py --offline            # 离线自测：用内置样例数据跑通全流程
  python daily_monitor.py --offline --update   # 离线自测第二遍：模拟“出现新版本”
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

# ---- 路径与日志 ----------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
SNAPSHOT_PATH = BASE_DIR / "monitor_snapshot.json"
LOG_PATH = BASE_DIR / "monitor.log"
REPORT_DIR = BASE_DIR / "reports"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("daily_monitor")


# ---- 数据源 --------------------------------------------------------------
def fetch_github_releases(repo: str) -> list[dict]:
    """调用 GitHub 公开 API，拉取某仓库最近的 Release 列表。

    返回 [{"tag": ..., "name": ..., "published_at": ..., "url": ...}, ...]。
    网络失败时抛出异常，由上层记录日志并以非零码退出。
    """
    import urllib.request

    url = f"https://api.github.com/repos/{repo}/releases?per_page=10"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "daily-monitor-tutorial",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = json.loads(resp.read().decode("utf-8"))

    releases = []
    for item in raw:
        releases.append(
            {
                "tag": item.get("tag_name", ""),
                "name": item.get("name", "") or item.get("tag_name", ""),
                "published_at": item.get("published_at", ""),
                "url": item.get("html_url", ""),
            }
        )
    return releases


# 离线自测用的两份样例：第一轮是“旧版本集合”，第二轮注入一个新版本，
# 用来在没有网络的情况下也能演示“有变化 -> 生成摘要”这条分支。
_OFFLINE_SNAPSHOT_A = [
    {
        "tag": "v2.31.0",
        "name": "v2.31.0",
        "published_at": "2026-08-01T00:00:00Z",
        "url": "https://example.com/release/v2.31.0",
    },
    {
        "tag": "v2.30.0",
        "name": "v2.30.0",
        "published_at": "2026-06-15T00:00:00Z",
        "url": "https://example.com/release/v2.30.0",
    },
]
_OFFLINE_SNAPSHOT_B = _OFFLINE_SNAPSHOT_A + [
    {
        "tag": "v2.32.0",
        "name": "v2.32.0 (self-test)",
        "published_at": "2026-09-18T00:00:00Z",
        "url": "https://example.com/release/v2.32.0",
    },
]


# ---- 快照读写 ------------------------------------------------------------
def load_previous() -> list[dict]:
    if not SNAPSHOT_PATH.exists():
        return []
    try:
        return json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        log.warning("旧快照读取失败，按空快照处理：%s", exc)
        return []


def save_current(current: list[dict]) -> None:
    SNAPSHOT_PATH.write_text(
        json.dumps(current, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def diff_new_releases(prev: list[dict], current: list[dict]) -> list[dict]:
    """只返回“当前有、但上次快照里没有”的 Release（按 tag 判重）。"""
    prev_tags = {item.get("tag") for item in prev}
    return [item for item in current if item.get("tag") not in prev_tags]


# ---- 摘要与通知 ----------------------------------------------------------
def write_report(repo: str, new_items: list[dict]) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"change_{stamp}.md"

    lines = [
        f"# {repo} Release 变更摘要",
        "",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"新增 Release 数量：{len(new_items)}",
        "",
    ]
    for item in new_items:
        lines.append(f"- {item['tag']}  {item['name']}")
        lines.append(f"    发布时间：{item['published_at']}")
        lines.append(f"    链接：{item['url']}")
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


# ---- 主流程 --------------------------------------------------------------
def run(repo: str, offline: bool, offline_update: bool) -> int:
    started = datetime.now().isoformat(timespec="seconds")
    log.info("=== 监控开始 repo=%s offline=%s ===", repo, offline)

    # Action：抓取
    if offline:
        current = _OFFLINE_SNAPSHOT_B if offline_update else _OFFLINE_SNAPSHOT_A
        log.info("离线模式：使用内置样例数据（%d 条）", len(current))
    else:
        try:
            current = fetch_github_releases(repo)
        except Exception as exc:  # noqa: BLE001 — 顶层要兜住，定时任务不能崩
            log.error("抓取失败：%s", exc)
            return 2
        log.info("抓取成功：%d 条 Release", len(current))

    # Condition：与昨日对比
    previous = load_previous()
    is_first_run = len(previous) == 0
    new_items = diff_new_releases(previous, current)

    if is_first_run:
        # 首次运行没有“昨日快照”作基准：只建立基准，不发通知。
        # 这是“无事不打扰”原则的体现——首次不算变更。
        log.info("首次运行：建立基准快照（%d 条），不生成通知。", len(current))
        save_current(current)
        return 0

    if not new_items:
        # 无事不通知：这一轮静默退出，只在日志里留一行
        log.info("无新 Release，静默退出。started=%s", started)
        save_current(current)  # 无论有无变化都刷新快照，保证下次对比基准最新
        return 0

    # 有变化：写摘要文件（Notification）
    report_path = write_report(repo, new_items)
    log.info("发现 %d 条新 Release，摘要已写入：%s", len(new_items), report_path)
    save_current(current)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="每日信息监控：抓取 GitHub Releases 并与昨日快照对比")
    parser.add_argument("--repo", default="psf/requests", help="要监控的 GitHub 仓库，格式 owner/name")
    parser.add_argument("--offline", action="store_true", help="离线自测：使用内置样例数据，不访问网络")
    parser.add_argument("--update", action="store_true", help="配合 --offline，模拟“今天有新版本发布”")
    args = parser.parse_args()
    return run(args.repo, args.offline, args.update)


if __name__ == "__main__":
    raise SystemExit(main())
