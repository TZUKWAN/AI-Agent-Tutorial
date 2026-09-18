# daily_monitor：每日 GitHub Release 监控

`daily_monitor.py` 是一个真实可运行的定时监控脚本：抓取目标仓库的 Releases，
与昨日快照对比，**有新 Release 才写变更摘要，否则静默退出**。
纯标准库实现，无需 pip 安装。

## 两种模式（证据路径不同，切勿混淆）

| 维度 | `live` 模式（默认，真实联网） | `offline` 模式（教学自测，不联网） |
|------|-------------------------------|------------------------------------|
| 数据源 | 真实调用 `https://api.github.com/repos/<repo>/releases` | 内置两份样例数据 A / B |
| 是否联网 | 是（匿名 API，60 次/小时） | 否 |
| 运行日志 | `monitor_live.log` | `monitor.log` |
| 快照文件 | `monitor_snapshot_live.json` | `monitor_snapshot.json` |
| 变更摘要目录 | `reports/live/change_*.md` | `reports/change_*.md` |
| HTTP 请求/返回存档 | `http_live/http_<时间戳>.json` | 无（不产生） |
| 用途 | 真正挂到任务计划程序上跑 | 无网络时演示全流程 |

## 运行方式

```powershell
cd examples\automation

# live 模式：真实抓取 psf/requests
python daily_monitor.py
python daily_monitor.py --repo pallets/click

# offline 模式：用样例数据自测
python daily_monitor.py --offline            # 样例 A（模拟无新版本）
python daily_monitor.py --offline --update   # 样例 B（模拟有新版本）

# 显式指定模式
python daily_monitor.py --mode live
python daily_monitor.py --mode offline
```

## 证据文件怎么看（live 模式真实跑过一次）

一次真实 `live` 运行会留下：

1. `http_live/http_<时间戳>.json` —— 本轮**真实 HTTP 请求与返回数据**存档，
   含请求 URL、请求头、HTTP 状态码、返回的 Release 列表。这是“真联网”的硬证据。
2. `monitor_snapshot_live.json` —— 本轮快照，供下次对比。
3. `monitor_live.log` —— 本轮运行日志。
4. `reports/live/change_*.md` —— **仅当**相对上次快照有新 Release 时才生成。

> 说明：匿名 API 限额为 60 次/小时。若遇到 HTTP 403 `rate limit exceeded`，
> 请等 `X-RateLimit-Reset` 重置后再试，或配置 `GITHUB_TOKEN` 提高额度。
