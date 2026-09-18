# LAB E 验收清单：数据分析闭环

| # | 验收项 | 证据文件 | 结果 |
|---|--------|----------|------|
| 1 | 自建含脏数据样例（缺失/异常/格式不一致） | `dirty_data.csv`（22 行，含 3 类脏数据） | ✅ |
| 2 | 数据字典说明 | `quality_report.md` 第一节 | ✅ |
| 3 | 质量检查报告（缺失/异常/格式不一致） | `quality_report.md` 第二节（缺年龄3、异常年龄2、异常收入5、单位错误4） | ✅ |
| 4 | 数据清洗并留痕 | `cleaned_data.csv`（10 行）+ 剔除留痕表 | ✅ |
| 5 | 描述统计 | `analysis_report.md`（年龄均值 31.1、收入均值 10180.05） | ✅ |
| 6 | matplotlib 出图 | `income_by_city.png`（中文正常、带样本量标注） | ✅ |
| 7 | 分析结论报告 | `analysis_report.md`（含「适用范围与局限」一节） | ✅ |
| 8 | 运行日志落盘 | `lab_e.log` | ✅ |
| 9 | 原始脏数据只读未改 | `dirty_data.csv` 全程只读 | ✅ |

## 复跑命令

```powershell
cd examples\labs\lab_e_data
python run_lab_e.py
```

复跑后应重新生成 `cleaned_data.csv` / `quality_report.md` / `analysis_report.md` / `income_by_city.png` / `lab_e.log`，清洗后行数恒为 **10**，收入均值恒为 **10180.05 元**。
