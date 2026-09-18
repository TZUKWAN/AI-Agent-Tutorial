#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
daily_monitor.py — 每日信息监控（PART 9 案例 1 的完整可运行实现），支持两种模式。

工作流（对应 9.1-9.8 八个零件）：
  Schedule  : 由 Windows 任务计划程序（schtasks）每天定时调用本脚本
  Action    : 抓取目标 GitHub 仓库的 Releases（稳定只读数据源）
  Condition : 与昨日快照对比，只有“出现新 Release”才算有变化
  Notification: 有变化时写一份摘要文件；无变化静默退出
  Logging   : 每一轮都写日志文件，失败可追溯

本脚本只做只读抓取与本地比对，不对外发送任何消息，因此不需要人工审批节点。
纯标准库实现，无需 pip 安装任何第三方包。

========================================================================
两种模式（务必区分，证据路径不同）
========================================================================

[live 模式] —— 默认模式，真实联网
  - 真实调用 GitHub 公开 API（https://api.github.com/repos/<repo>/releases）
  - 匿名调用，无需 Token；注意匿名额度为 60 次/小时，超限会返回 HTTP 403
  - 证据文件（全部落在本目录下）：
      monitor_live.log              —— 本轮 live 运行日志
      monitor_snapshot_live.json     —— live 模式的“昨日快照”
      reports/live/change_*.md       —— 有新 Release 时生成的变更摘要
      http_live/http_<时间戳>.json   —— 真实 HTTP 请求与返回数据的存档
  - 用法：
      python daily_monitor.py                       # 真实监控 psf/requests
      python daily_monitor.py --repo pallets/click  # 真实监控指定仓库
      python daily_monitor.py --mode live           # 等价于默认

[offline 模式] —— 教学自测，不联网
  - 用内置两份样例数据（A=旧集合，B=注入一个新版本）跑通全流程
  - 不访问网络，不产生真实 HTTP 证据
  - 证据文件：
      monitor.log                  —— offline 运行日志
      monitor_snapshot.json        —— offline 快照
      reports/change_*.md          —— offline 变更摘要
  - 用法：
      python daily_monitor.py --offline            # 用样例 A（模拟“无新版本”）
      python daily_monitor.py --offline --update   # 用样例 B（模拟“有新版本”）
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

# 两种模式各自的证据文件路径，互不污染
MODE_PATHS = {
    "live": {
        "log": BASE_DIR / "monitor_live.log",
        "snapshot": BASE_DIR / "monitor_snapshot_live.json",
        "report_dir": BASE_DIR / "reports" / "live",
        "http_dir": BASE_DIR / "http_live",
    },
    "offline": {
        "log": BASE_DIR / "monitor.log",
        "snapshot": BASE_DIR / "monitor_snapshot.json",
        "report_dir": BASE_DIR / "reports",
        "http_dir": None,  # offline 不产生 HTTP 证据
    },
}


def _build_logger(log_path: Path) -> logging.Logger:
    logger = logging.getLogger(f"daily_monitor.{log_path.stem}")
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(sh)
    return logger


# ---- 数据源（live 模式真实联网） ----------------------------------------
def fetch_github_releases(repo: str) -> tuple[list[dict], dict]:
    """调用 GitHub 公开 API，拉取某仓库最近的 Release 列表。

    返回 (releases, http_evidence)：
      releases      —— [{"tag","name","published_at","url"}, ...]
      http_evidence —— 本轮真实 HTTP 请求/响应的存档（用于证据留痕）。

    网络失败时抛出异常，由上层记录日志并以非零码退出。
    """
    import urllib.error
    import urllib.request

    url = f"https://api.github.com/repos/{repo}/releases?per_page=10"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "daily-monitor-tutorial",
    }
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            status = resp.getcode()
            raw_bytes = resp.read()
            raw = json.loads(raw_bytes.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        # 把限流/鉴权等错误也留痕，方便排查
        body = ""
        try:
            body = exc.read().decode("utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            pass
        evidence = {
            "request": {"method": "GET", "url": url, "headers": headers},
            "response": {
                "status": exc.code,
                "fetched_at": datetime.now().isoformat(timespec="seconds"),
                "error_body": body[:1000],
            },
        }
        raise RuntimeError(f"GitHub API HTTP {exc.code}: {body[:200]}") from exc
    except Exception as exc:  # noqa: BLE001
        evidence = {
            "request": {"method": "GET", "url": url, "headers": headers},
            "response": {
                "status": None,
                "fetched_at": datetime.now().isoformat(timespec="seconds"),
                "error": repr(exc),
            },
        }
        raise

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

    http_evidence = {
        "request": {"method": "GET", "url": url, "headers": headers},
        "response": {
            "status": status,
            "fetched_at": datetime.now().isoformat(timespec="seconds"),
            "count": len(releases),
            "releases": releases,
        },
    }
    return releases, http_evidence


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
def load_previous(snapshot_path: Path) -> list[dict]:
    if not snapshot_path.exists():
        return []
    try:
        return json.loads(snapshot_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        log.warning("旧快照读取失败，按空快照处理：%s", exc)
        return []


def save_current(current: list[dict], snapshot_path: Path) -> None:
    snapshot_path.write_text(
        json.dumps(current, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def diff_new_releases(prev: list[dict], current: list[dict]) -> list[dict]:
    """只返回“当前有、但上次快照里没有”的 Release（按 tag 判重）。"""
    prev_tags = {item.get("tag") for item in prev}
    return [item for item in current if item.get("tag") not in prev_tags]


# ---- 摘要与通知 ----------------------------------------------------------
def write_report(report_dir: Path, repo: str, new_items: list[dict]) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = report_dir / f"change_{stamp}.md"

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


def save_http_evidence(http_dir: Path, evidence: dict) -> Path:
    http_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = http_dir / f"http_{stamp}.json"
    path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


# ---- 主流程 ---------------------------------------------------------------
def run(repo: str, mode: str, offline_update: bool) -> int:
    paths = MODE_PATHS[mode]
    global log
    log = _build_logger(paths["log"])

    snapshot_path: Path = paths["snapshot"]
    report_dir: Path = paths["report_dir"]
    http_dir = paths["http_dir"]

    started = datetime.now().isoformat(timespec="seconds")
    log.info("=== 监控开始 repo=%s mode=%s ===", repo, mode)

    # Action：抓取
    if mode == "offline":
        current = _OFFLINE_SNAPSHOT_B if offline_update else _OFFLINE_SNAPSHOT_A
        log.info("[offline] 使用内置样例数据（%d 条），不访问网络。", len(current))
    else:
        try:
            current, evidence = fetch_github_releases(repo)
        except Exception as exc:  # noqa: BLE001 — 顶层要兜住，定时任务不能崩
            log.error("[live] 抓取失败：%s", exc)
            log.error("[live] 提示：匿名 API 限额为 60 次/小时，若返回 403 rate limit，"
                      "请等待 X-RateLimit-Reset 后再试，或配置 GITHUB_TOKEN。")
            return 2
        log.info("[live] 抓取成功：%d 条 Release。", len(current))
        if http_dir is not None:
            p = save_http_evidence(http_dir, evidence)
            log.info("[live] HTTP 请求/返回数据已存档：%s", p)

    # Condition：与昨日对比
    previous = load_previous(snapshot_path)
    is_first_run = len(previous) == 0
    new_items = diff_new_releases(previous, current)

    if is_first_run:
        # 首次运行没有“昨日快照”作基准：只建立基准，不发通知。
        # 这是“无事不打扰”原则的体现——首次不算变更。
        log.info("首次运行：建立基准快照（%d 条），不生成通知。snapshot=%s",
                 len(current), snapshot_path.name)
        save_current(current, snapshot_path)
        return 0

    if not new_items:
        # 无事不通知：这一轮静默退出，只在日志里留一行
        log.info("无新 Release，静默退出。started=%s", started)
        save_current(current, snapshot_path)  # 无论有无变化都刷新快照，保证下次对比基准最新
        return 0

    # 有变化：写摘要文件（Notification）
    report_path = write_report(report_dir, repo, new_items)
    log.info("发现 %d 条新 Release，摘要已写入：%s", len(new_items), report_path)
    save_current(current, snapshot_path)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="每日信息监控：抓取 GitHub Releases 并与昨日快照对比（live 真实联网 / offline 样例自测）"
    )
    parser.add_argument("--repo", default="psf/requests", help="要监控的 GitHub 仓库，格式 owner/name")
    parser.add_argument(
        "--mode", choices=["live", "offline"], default="live",
        help="live=真实调用 GitHub API（默认）；offline=内置样例自测",
    )
    parser.add_argument("--offline", action="store_true", help="等价于 --mode offline")
    parser.add_argument("--update", action="store_true", help="配合 offline 模式，模拟“今天有新版本发布”")
    args = parser.parse_args()

    mode = "offline" if args.offline else args.mode
    return run(args.repo, mode, args.update)


if __name__ == "__main__":
    raise SystemExit(main())
