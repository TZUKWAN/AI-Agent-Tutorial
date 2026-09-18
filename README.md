# AI Agent 零基础工作方法教程

> 版本：v1.1 | 日期：2026-09-18
> 适用读者：完全不懂编程的大学新生、文科本硕博
> GitHub：https://github.com/TZUKWAN/AI-Agent-Tutorial

## 项目定位

这不是一本教人"怎么和 AI 聊天"的教程，而是一套帮助技术零基础用户掌握"如何把真实工作交给 AI Agent，并对过程、权限、质量与结果负责"的完整工作方法课程。

## 教程结构（11 Part）

| Part | 主题 | 核心内容 |
|------|------|----------|
| 0 | 为什么要学 Agent | 从 Chatbot 到 Agent 的能力跃迁 |
| 1 | 第一次让 Agent 真正完成工作 | 工作区、权限、首次 Mission |
| 2 | 怎样给 Agent 下任务 | 8 要素任务法 |
| 3 | 怎样管理长任务 | Plan/Milestone/Checkpoint/WORKLOG |
| 4 | 怎样判断 Agent 是否真的做对了 | 三层证据模型 |
| 5 | Agent 会怎么失败 | 21 种失败模式与恢复策略 |
| 6 | Agent 到底由什么组成 | 19 个核心概念五层结构 |
| 7 | 给 Agent 安装和扩展能力 | Skill/MCP/Connector 安装与安全 |
| 8 | 场景实验室 | 学习/科研/Office/网络/数据/开发/效率 |
| 9 | 自动化与长期运行 | Trigger/Schedule/Workflow |
| 10 | 构建自己的 Agent | 从零设计并实现 |

## 快速开始

### 阅读最终教程
直接下载并打开 `05_Word/AI-Agent零基础工作方法教程.docx`（约 4.6 MB，含 32 张架构图）。

### 从源码重新构建 Word
```powershell
# 安装依赖
pip install -r requirements.txt

# 构建 Word
python build_docx.py

# 运行审计
python "<word-skill路径>\scripts\audit.py" audit "05_Word\AI-Agent零基础工作方法教程.docx"

# 更新目录
python "<word-skill路径>\scripts\catalogue.py" --file "05_Word\AI-Agent零基础工作方法教程.docx"
```

### 重新生成架构图
```powershell
python scripts/batch1.py
python scripts/batch2.py
python scripts/batch3.py
```

## 目录结构
```
├── 01_调研/          # 生态资源调研与索引
├── 02_设计/          # 目录设计与术语表
├── 03_写作/          # 正文 Markdown 源文件
├── 04_图/            # 32 张架构图（PNG + SVG）
├── 05_Word/          # 最终 Word 文档（canonical）
├── scripts/          # 绘图脚本
├── build_docx.py     # Word 构建脚本
├── requirements.txt  # Python 依赖
├── LICENSE           # MIT
├── CHANGELOG.md      # 版本变更
├── FACT_AUDIT.md     # 事实核验记录
├── VISUAL_QA.md      # 视觉 QA 记录
└── QA_REPORT.md      # 质量报告
```

## 核心方法论
- **统一认知框架**：Goal → Context → Resources → Capabilities → Workflow → Verification → Reuse
- **8 要素任务法**：目标/材料/环境/权限/约束/过程/验收/交付
- **核心执行循环**：定义→规划→执行→观察→检查→（修复重执/交付）
- **30 个 Mission**（L0-L7 难度）
- **4 条贯穿案例线**：课程学习/科研论文/学生项目/做软件

## 质量审计
- word skill audit.py：0 错误通过
- 所有资源核验日期：2026-09-18
- 详见 FACT_AUDIT.md、VISUAL_QA.md、QA_REPORT.md

## 已知限制
- V1.1 已修复工程构建问题，正文深度重构（真实安装演示、真自动化案例、真 Agent 构建）计划在 V1.2 完成
- 32 张图未经逐张 PDF 渲染视觉审查
- 资源索引 98 条沿用上一版核验结果
