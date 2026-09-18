# QA_REPORT.md - V1.1 质量报告

> 日期：2026-09-18

## 本轮修复完成项（PASS）
1. build_docx.py 相对路径化 ✅
2. F 编号临时映射删除，统一 F00-F31 直接对应 ✅
3. 附录B资源表按 Tier 真实筛选（非简单截前50行） ✅
4. TOC 扩展到 1-3 级 ✅
5. F00 认知框架图插入前言后 ✅
6. 根目录重复 docx 清理（canonical 唯一在 05_Word/） ✅
7. requirements.txt 新增 ✅
8. LICENSE (MIT) 新增 ✅
9. CHANGELOG.md 新增 ✅
10. FACT_AUDIT.md 新增 ✅
11. VISUAL_QA.md 新增 ✅
12. word skill audit.py 退出码 0 ✅
13. catalogue.py 目录更新成功 ✅
14. 32 张图全部嵌入 ✅

## 未完成项（FAIL / 待迭代）
1. 正文深度重构（PART 6 五层认知结构、PART 7 真实安装演示、PART 8 旗舰项目、PART 9 真自动化、PART 10 真Agent构建）— 待 V1.2
2. 98 条资源逐条重新联网核验 — 待 V1.2
3. 32 张图逐张视觉审查（render→inspect→revise）— 待 V1.2
4. Word PDF 逐页视觉检查 — 待 V1.2
5. README 完善（预览图、Quick Start、构建说明）— 待 V1.2
6. 故障注入实验、WORKLOG 示例等实操增强 — 待 V1.2

## 构建可复现性
- 从干净环境：pip install -r requirements.txt && python build_docx.py 即可重建
- 依赖：python-docx, lxml, Pillow, matplotlib
- 输入：4 个 Markdown + 32 PNG + 术语表 + CSV
