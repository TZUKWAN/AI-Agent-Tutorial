# CHANGELOG

## v1.1.0 (2026-09-18)

### 修复
- build_docx.py 绝对路径硬编码改为仓库相对路径（Path(__file__).resolve().parent）
- 删除 F 编号临时兼容映射（原 F001→F00、F01→F11 等），统一为 F00-F31 直接对应
- 附录B资源表从"简单截前50行"改为按 Tier 分级真实筛选
- TOC 从 1-2 级扩展到 1-3 级
- 前言后插入 F00 全书认知框架图
- 删除根目录重复 docx（canonical 唯一文件在 05_Word/）

### 新增
- requirements.txt（python-docx, lxml, Pillow, matplotlib）
- LICENSE（MIT）
- 目录现在覆盖 Heading 1-3 全部层级

### 已知限制
- PART 6-10 正文内容仍为 V1.0 版本，深度重构（五层认知结构、真实安装演示、真自动化案例、真Agent构建）待后续迭代
- 32 张图未经逐张视觉审计（当前仅验证文件存在、大小、基本配色）
- 资源索引 98 条未逐条重新联网核验（沿用上一版核验结果）
