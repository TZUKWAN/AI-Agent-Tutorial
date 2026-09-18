# LAB F 验收清单：真实开源项目闭环

## 选用项目

- **项目**：[tartley/colorama](https://github.com/tartley/colorama)
- **协议**：BSD 3-Clause（LICENSE.txt 在 repo 根目录）
- **选取理由**：真实公开、纯标准库零依赖、README 清晰、demo 与测试齐全，体积小适合第一次练手。
- **克隆方式**：`git clone --depth 1 https://github.com/tartley/colorama.git repo`（浅克隆，仅拉最新提交）

## 闭环动作与证据

| # | 动作 | 证据文件 | 结果 |
|---|------|----------|------|
| 1 | git clone | `clone.log` | ✅ |
| 2 | 读 README（`README.rst`） | 已读：安装/描述/跨平台 API 说明 | ✅ |
| 3 | 真实运行项目 | `run_demo.log`（demo01 颜色网格已输出） | ✅ |
| 4 | 改一个小功能（demo01 末尾加 LAB banner） | `change.diff` | ✅ |
| 5 | 写 smoke test 并运行 | `smoke_test.log`（`SMOKE OK`） | ✅ |
| 6 | 重跑改动后的 demo | `run_demo.log` 末尾出现 banner | ✅ |
| 7 | git commit | `commit.log` / `git_log.txt`（commit `2874e5f`） | ✅ |
| 8 | 保存 git 记录 | `git_log.txt` | ✅ |

## 改动内容（一句话）

在 `demos/demo01.py` 末尾追加 4 行打印一行绿色 banner；新增 `test_smoke.py`（46 行）作为无依赖的冒烟测试。详见 `change.diff`。

## 权限边界（如实标注）

- 本次操作全部在**本地**仓库完成，**未执行** `git push`，**未向远端发起 Pull Request / Merge Request**。
- 远端仓库 `tartley/colorama` 属于第三方作者（Jonathan Hartley 等），当前账号无写权限，也不应把教学性改动推到上游。
- 如需真实上游贡献，正确姿势是：fork 到自己账号 → 在 fork 上 push → 在 GitHub 网页发起 PR。本 LAB 不演示这一步。

## 复跑命令

```powershell
cd examples\labs\labf_project\repo
python test_smoke.py        # 应输出 SMOKE OK
python demos/demo01.py      # 末尾应出现绿色 banner
git log --oneline -n 3      # 应能看到 commit 2874e5f
```
