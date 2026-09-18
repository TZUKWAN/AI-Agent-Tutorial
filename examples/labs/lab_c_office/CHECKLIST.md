# LAB C 验收清单：Office 闭环

| # | 验收项 | 证据文件 | 结果 |
|---|--------|----------|------|
| 1 | 输入材料为 10-20 行销售数据表 | `input_data.csv`（15 行明细） | ✅ |
| 2 | 脚本可独立运行 | `run_lab_c.py` | ✅ |
| 3 | openpyxl 生成含汇总表的 Excel | `sales_report.xlsx`（明细/区域汇总/产品汇总 3 张表） | ✅ |
| 4 | python-docx 生成 Word 报告 | `sales_report.docx`（2 张表 + 结论） | ✅ |
| 5 | 生成汇报要点 | `talking_points.md` | ✅ |
| 6 | 运行日志落盘 | `lab_c.log` | ✅ |
| 7 | 三方数字一致（复算证据） | Excel 区域/产品合计均为 62818.00 元，Word 总额同为 62,818.00 元 | ✅ |
| 8 | 原始输入未被修改 | `input_data.csv` 保持只读使用，脚本只读不写 | ✅ |

## 复跑命令

```powershell
cd examples\labs\lab_c_office
python run_lab_c.py
```

复跑后应重新生成 `sales_report.xlsx` / `sales_report.docx` / `talking_points.md` / `lab_c.log`，合计数应始终为 **62818.00 元**。
