# AI Agent 零基础工作方法教程

> 版本：v1.2.0 | 日期：2026-09-19
> 适用读者：完全不懂编程的大学新生、文科本硕博
> GitHub：https://github.com/TZUKWAN/AI-Agent-Tutorial

## 项目定位

这不是一本教人"怎么和 AI 聊天"的教程，而是一套帮助技术零基础用户掌握"如何把真实工作交给 AI Agent，并对过程、权限、质量与结果负责"的完整工作方法课程。

## 教程结构（11 Part）

| Part | 主题 | 核心内容 |
|------|------|----------|
| 0 | 工作方式转换 | 从"问 AI"到"把工作交给 AI"：三维度（工具调用/自主推进/持续运行） |
| 1 | 第一次让 Agent 真正完成工作 | 给它桌子和钥匙：工作区、权限、首次 Mission |
| 2 | 怎样给 Agent 下任务 | 告诉它到底干什么：8 要素任务法 |
| 3 | 怎样管理长任务 | 状态管理：State 为中心，TASKS/WORKLOG 最小配置 |
| 4 | 怎样判断 Agent 是否真的做对了 | 四类验证 + 三级强度 |
| 5 | Agent 会怎么失败 | 6 类故障诊断手册 |
| 6 | Agent 到底由什么组成 | 四个基本系统 + 一个扩展接口层 |
| 7 | 给 Agent 安装和扩展能力 | 能力供应链：Skill/Plugin/MCP/Connector 的发现与审计 |
| 8 | 场景实验室 | 核心 LAB（A/C/D/G）、专业 LAB（B/E）、进阶 LAB（F） |
| 9 | 自动化与长期运行 | 从真实工作流拆解 Trigger/Condition/Action/Approval |
| 10 | 构建自己的 Agent | Build-along：13 步从最小 Agent 开始 |

## 快速开始

### 阅读最终教程
直接下载并打开 `05_Word/AI-Agent零基础工作方法教程.docx`（约 5.0 MB，175 页，含 32 张架构图）。也可直接查看 `05_Word/preview.pdf`。

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
- **全书总模型（8 阶段主线）**：定义任务 → 准备上下文与能力 → 执行 → 观察 → 验证 → 修复 → 交付 → 沉淀
- **8 要素任务法**：目标/上下文/环境/权限/约束/过程/验收/交付
- **四条完成原则**：生成结果≠完成任务；执行动作≠得到正确结果；一次验证通过≠整体可靠；Agent 声明完成≠实际完成
- **30 个 Mission**（L0-L7 难度）
- **4 条贯穿案例线**：课程学习/科研论文/学生项目/做软件
- **6 条全书原则**：先定义任务再开始；给最小充分上下文；权限按风险给；长任务有状态和检查点；不接受完成声明只接受证据；跑通后沉淀成模板/Skill/自动化

## 构建与 QA 环境要求

### DOCX 构建（跨平台）
仅需 Python + requirements.txt：
```powershell
pip install -r requirements.txt
python build_docx.py
```

### PDF 导出与逐页 QA（Windows + Word）
完整"docx → pdf → 逐页渲染 → QA"流水线在 **Windows + Microsoft Word** 环境可复现：
```powershell
# 导出 PDF（需 Word COM）
powershell -ExecutionPolicy Bypass -File 05_Word\export_pdf.ps1

# 渲染全部页面 + 自动检查
python 05_Word\render_full.py
```
其他平台需自行用 LibreOffice 或其他工具导出 PDF 后手动检查。

## 质量审计
- word skill audit.py：0 错误通过
- 32 张图逐张视觉审查完成（4 张修复）
- 全部 175 页 PDF 逐页视觉检查通过（0 空白页）
- 98 条资源逐条联网核验（2026-09-18）
- 详见 FACT_AUDIT.md、VISUAL_QA.md、QA_REPORT.md

## 已知限制
- LAB F 的 Push/PR/Deploy 需 GitHub 账号与远端权限，已如实标注
- 邮件 SMTP 真发送需用户自行填入凭据
- RAG 为教学简化版（关键词检索，非向量检索）
- Planner 为模板规则，非 LLM 驱动

