# -*- coding: utf-8 -*-
"""F00, F31, F30, F01, F02, F03, F04, F29, F05, F06"""
from draw_common import *

# ========== F00 认知框架 ==========
def f00():
    fig, ax = new_canvas(14, 7.5, "F00  AI Agent 认知框架：七步工作法")
    steps = [
        ("Goal", "目标", "要什么结果"),
        ("Context", "情境", "背景与材料"),
        ("Resources", "资源", "可用工具/文件"),
        ("Capabilities", "能力", "Agent能做什么"),
        ("Workflow", "流程", "如何一步步做"),
        ("Verification", "验证", "如何证明做对"),
        ("Reuse", "复用", "沉淀为下次经验"),
    ]
    n = len(steps)
    xs = np.linspace(8, 92, n)
    y = 55
    kinds = ["HEAD","INPUT","STD","PROC","PROC","CORE","OUT"]
    for i, ((en, cn, desc), k, x) in enumerate(zip(steps, kinds, xs)):
        rbox(ax, x, y, 11.5, 16, k, cn, fs=13, fw="bold", sub=f"{en}\n{desc}", sub_fs=9)
        if i < n-1:
            arrow(ax, (x+5.9, y), (xs[i+1]-5.9, y))
    ax.text(50, 22, "人负责：定义目标 · 提供判断 · 设置边界 · 承担决策",
            ha="center", fontsize=12, color=C["CORE_E"], fontweight="bold")
    ax.text(50, 14, "Agent负责：检索 · 阅读 · 操作 · 计算 · 制作 · 执行 · 迭代",
            ha="center", fontsize=12, color=C["OUT_E"], fontweight="bold")
    legend_row(ax, ALL_LEGEND)
    return save(fig, "F00_认知框架")

# ========== F31 学习路径地图 ==========
def f31():
    fig, ax = new_canvas(14, 8, "F31  学习路径地图：从「会聊天」到「构建自己的 Agent」")
    levels = [
        ("L0", "会聊天", "把 AI 当搜索框", "INPUT"),
        ("L1", "会交任务", "一句话给目标", "STD"),
        ("L2", "会给材料", "文件/背景/约束", "STD"),
        ("L3", "会管过程", "多步/断点/进度", "PROC"),
        ("L4", "会验结果", "证据/验收/回退", "PROC"),
        ("L5", "会排错", "失败模式与恢复", "CORE"),
        ("L6", "会扩展能力", "Tool/MCP/Skill", "HEAD"),
        ("L7", "会建自己的Agent", "设计并部署工作流", "OUT"),
    ]
    n = len(levels)
    xs = np.linspace(7, 93, n)
    y_base = 50
    for i, (lv, name, desc, k) in enumerate(levels):
        y = y_base + (i % 2) * 16
        rbox(ax, xs[i], y, 10.5, 15, k, name, fs=12.5, fw="bold", sub=f"{lv}\n{desc}", sub_fs=8.8)
        if i < n-1:
            arrow(ax, (xs[i]+5.3, y), (xs[i+1]-5.3, y_base + ((i+1) % 2)*16),
                  curve=0.15 if (i % 2) != ((i+1) % 2) else 0)
    ax.text(50, 88, "能力进阶（每一级都在前一级可用的前提下才成立）",
            ha="center", fontsize=11, color="#444")
    legend_row(ax, ALL_LEGEND)
    return save(fig, "F31_学习路径地图")

# ========== F30 贯穿案例成长路线 ==========
def f30():
    fig, ax = new_canvas(14, 8, "F30  贯穿案例成长路线：四条线随章节一起升级")
    chapters = ["第1-3章\n入门", "第4-6章\n任务与管理", "第7-9章\n架构与生态",
                "第10-12章\n场景实战", "第13-15章\n自动化构建"]
    lines = [
        ("课程学习线", ["用Agent答疑", "整理笔记思维导图", "生成复习提纲", "组学习工作流", "建学习助手"], "INPUT"),
        ("科研论文线", ["查文献", "文献综述8要素", "RAG建库读论文", "数据分析Agent", "投稿准备"], "PROC"),
        ("学生项目线", ["选题讨论", "拆任务给材料", "Milestone管理", "复现+修改", "Git提交"], "STD"),
        ("做软件线", ["描述需求", "读现有项目", "跑起来改代码", "调试+测试", "部署小工具"], "OUT"),
    ]
    # 章节横轴
    xs = np.linspace(18, 92, 5)
    for i, ch in enumerate(chapters):
        ax.text(xs[i], 86, ch, ha="center", fontsize=10, color=C["HEAD_E"],
                fontweight="bold")
    ys = [70, 55, 40, 25]
    for (name, stages, k), y in zip(lines, ys):
        ax.text(8, y, name, ha="center", va="center", fontsize=10.5,
                fontweight="bold", color=C[k+"_E"])
        for i, s in enumerate(stages):
            rbox(ax, xs[i], y, 13, 8.5, k, s, fs=9.5)
            if i < len(stages)-1:
                arrow(ax, (xs[i]+6.6, y), (xs[i+1]-6.6, y), lw=1.4)
    ax.text(50, 12, "同一条主线，在不同章节用越来越完整的 Agent 能力重做一遍",
            ha="center", fontsize=11, color="#444")
    legend_row(ax, ALL_LEGEND, y=5)
    return save(fig, "F30_贯穿案例成长路线")

# ========== F01 从聊天到Agent ==========
def f01():
    fig, ax = new_canvas(13, 7.5, "F01  从聊天到 Agent：能力四级递增")
    cols = [
        ("Chatbot", "聊天机器人", "你问一句\n它答一句\n无记忆/无工具", "INPUT", 15),
        ("Copilot", "副驾驶", "能引用文档\n能补全建议\n你主导执行", "STD", 38),
        ("Agent", "智能体", "能自己拆任务\n调用工具\n多步执行", "PROC", 61),
        ("Autonomous\nWorkflow", "自主工作流", "触发→执行→检查\n→修复→交付\n人只定边界", "CORE", 84),
    ]
    for name, cn, desc, k, x in cols:
        rbox(ax, x, 55, 18, 26, k, cn, fs=13, fw="bold", sub=f"{name}\n{desc}", sub_fs=9.5)
    for x1, x2 in [(24, 29), (47, 52), (70, 75)]:
        arrow(ax, (x1, 55), (x2, 55), lw=2.4)
    ax.text(50, 22, "自主度 ↑  |  你从「每步都操作」变成「只定目标和验收」",
            ha="center", fontsize=11.5, color=C["CORE_E"], fontweight="bold")
    legend_row(ax, ALL_LEGEND)
    return save(fig, "F01_从聊天到Agent")

# ========== F02 工作区与权限模型 ==========
def f02():
    fig, ax = new_canvas(13, 7.8, "F02  工作区与权限模型")
    # 中心
    circ = Circle((50, 55), 11, facecolor=C["HEAD_F"], edgecolor=C["HEAD_E"], lw=2, zorder=2)
    ax.add_patch(circ)
    ax.text(50, 55, "工作区\nWorkspace", ha="center", va="center",
            fontsize=14, fontweight="bold", color=C["HEAD_E"])
    # 周围资源
    res = [("本地文件", 20, 78), ("上传文件", 80, 78),
           ("云盘", 82, 32), ("代码仓库 Repo", 18, 32)]
    for name, x, y in res:
        rbox(ax, x, y, 15, 10, "STD", name, fs=11)
        arrow(ax, (50 + (x-50)*0.28, 55 + (y-55)*0.28),
              (x + (50-x)*0.18, y + (55-y)*0.18), aux=True)
    # 权限等级
    perms = [("读 Read", "查看/引用", "OUT", 20),
             ("写 Write", "新建/修改", "PROC", 40),
             ("删 Delete", "删除/覆盖", "CORE", 62),
             ("发送 Send", "对外发消息", "CORE", 84)]
    ax.text(50, 88, "四级权限（逐级升高，风险递增）", ha="center",
            fontsize=12, fontweight="bold", color="#444")
    for name, desc, k, x in perms:
        rbox(ax, x, 82, 16, 7, k, name, fs=10.5, sub=desc, sub_fs=8.8)
    ax.text(50, 18, "原则：默认最小权限；危险动作（删/发送）前停下来问人",
            ha="center", fontsize=11, color=C["CORE_E"])
    legend_row(ax, ALL_LEGEND, y=8)
    return save(fig, "F02_工作区与权限模型")

# ========== F03 8要素任务法闭环 ==========
def f03():
    fig, ax = new_canvas(12, 8.5, "F03  8 要素任务法闭环")
    elems = ["目标", "材料", "环境", "权限", "约束", "过程", "验收", "交付"]
    kinds = ["HEAD","INPUT","STD","STD","PROC","PROC","CORE","OUT"]
    cx, cy, R = 50, 50, 34
    pts = []
    for i, (e, k) in enumerate(zip(elems, kinds)):
        ang = np.pi/2 - i*(2*np.pi/8)
        x = cx + R*np.cos(ang); y = cy + R*np.sin(ang)
        pts.append((x, y))
        rbox(ax, x, y, 13, 9, k, e, fs=12, fw="bold")
    for i in range(8):
        arrow(ax, pts[i], pts[(i+1)%8], lw=1.8, curve=-0.15)
    circ = Circle((cx, cy), 9, facecolor=C["CORE_F"], edgecolor=C["CORE_E"], lw=2)
    ax.add_patch(circ)
    ax.text(cx, cy, "一次\n完整\n任务", ha="center", va="center",
            fontsize=11, fontweight="bold", color=C["CORE_E"])
    ax.text(50, 7, "缺任何一环，任务都容易跑偏或无法验收", ha="center",
            fontsize=11, color="#444")
    legend_row(ax, ALL_LEGEND, y=2)
    return save(fig, "F03_8要素任务法闭环")

# ========== F04 好任务 vs 坏任务 ==========
def f04():
    fig, ax = new_canvas(13, 7.8, "F04  好任务 vs 坏任务")
    # 左：坏任务
    ax.add_patch(FancyBboxPatch((4, 18), 42, 62, boxstyle="round,pad=0.4,rounding_size=1.5",
                 linewidth=2, edgecolor=C["CORE_E"], facecolor="#FBEDEC", zorder=1))
    ax.text(25, 74, "坏任务（模糊）", ha="center", fontsize=14,
            fontweight="bold", color=C["CORE_E"])
    bad = ["「帮我看看这个文件」", "「随便写点东西」", "「把这件事搞定」",
           "没有材料 / 没有验收标准", "没有边界 / 允许它乱改"]
    for i, t in enumerate(bad):
        ax.text(8, 66 - i*8, "×  " + t, fontsize=10.5, color="#7a3b3a")
    # 右：好任务
    ax.add_patch(FancyBboxPatch((54, 18), 42, 62, boxstyle="round,pad=0.4,rounding_size=1.5",
                 linewidth=2, edgecolor=C["OUT_E"], facecolor="#EDF6EC", zorder=1))
    ax.text(75, 74, "好任务（明确）", ha="center", fontsize=14,
            fontweight="bold", color=C["OUT_E"])
    good = ["「读这3篇PDF，对比方法异同」", "「输出500字综述+表格」", "「存到 output/ 目录」",
            "材料已给 / 验收标准写明", "只允许读，不允许删"]
    for i, t in enumerate(good):
        ax.text(58, 66 - i*8, "√  " + t, fontsize=10.5, color="#3a6b36")
    arrow(ax, (47, 49), (53, 49), lw=2.5)
    ax.text(50, 49, "重写", ha="center", va="center", fontsize=9,
            color="#444", bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#999"))
    ax.text(50, 10, "差别不在句子长短，而在：目标可判、材料可见、边界清楚、能验收",
            ha="center", fontsize=11, color="#444")
    return save(fig, "F04_好任务vs坏任务")

# ========== F29 8要素文献综述示例 ==========
def f29():
    fig, ax = new_canvas(13.5, 8, "F29  8 要素示例：写一篇「AI Agent 教育应用」文献综述")
    items = [
        ("目标", "800字综述+1张对比表", "HEAD"),
        ("材料", "已给5篇PDF+2个链接", "INPUT"),
        ("环境", "工作区 /lit-review/", "STD"),
        ("权限", "只读+新建output", "STD"),
        ("约束", "不编造引用，中文", "PROC"),
        ("过程", "读→摘→比→写", "PROC"),
        ("验收", "引用可溯源/表格无空", "CORE"),
        ("交付", "综述.md + 对比表.xlsx", "OUT"),
    ]
    # 上行4个，下行4个
    for i, (k, v, c) in enumerate(items):
        row = i // 4
        col = i % 4
        x = 16 + col*24
        y = 62 - row*30
        rbox(ax, x, y, 20, 18, c, k, fs=12.5, fw="bold", sub=v, sub_fs=10)
    arrow(ax, (26, 62), (34, 62), lw=1.6)
    arrow(ax, (50, 62), (58, 62), lw=1.6)
    arrow(ax, (74, 62), (82, 62), lw=1.6)
    arrow(ax, (82, 53), (82, 35), lw=1.6)
    arrow(ax, (82, 32), (74, 32), lw=1.6)
    arrow(ax, (58, 32), (50, 32), lw=1.6)
    arrow(ax, (34, 32), (26, 32), lw=1.6)
    ax.text(50, 10, "对照这8格填空，就是一个可交给 Agent 的完整任务",
            ha="center", fontsize=11, color="#444")
    legend_row(ax, ALL_LEGEND, y=5)
    return save(fig, "F29_8要素文献综述示例")

# ========== F05 长任务管理仪表盘 ==========
def f05():
    fig, ax = new_canvas(13, 8, "F05  长任务管理仪表盘")
    circ = Circle((50, 52), 12, facecolor=C["CORE_F"], edgecolor=C["CORE_E"], lw=2)
    ax.add_patch(circ)
    ax.text(50, 52, "长任务\n（跨越多步）", ha="center", va="center",
            fontsize=12, fontweight="bold", color=C["CORE_E"])
    mods = [
        ("TaskList", "待办清单", "INPUT", 18, 78),
        ("Milestone", "里程碑", "HEAD", 82, 78),
        ("Checkpoint", "检查点/快照", "PROC", 84, 30),
        ("Progress", "进度看板", "OUT", 16, 30),
        ("Log", "执行日志", "STD", 50, 86),
        ("Alert", "异常告警", "CORE", 50, 16),
    ]
    for name, desc, k, x, y in mods:
        rbox(ax, x, y, 16, 10, k, name, fs=10.5, sub=desc, sub_fs=9)
        arrow(ax, (50 + (x-50)*0.3, 52 + (y-52)*0.3),
              (x + (50-x)*0.2, y + (52-y)*0.2), aux=True)
    ax.text(50, 6, "仪表盘的目的：人随时知道「现在到哪了 / 下一步是什么 / 哪里卡住了」",
            ha="center", fontsize=10.5, color="#444")
    legend_row(ax, ALL_LEGEND, y=2)
    return save(fig, "F05_长任务管理仪表盘")

# ========== F06 多阶段工作流 ==========
def f06():
    fig, ax = new_canvas(14.5, 7.2, "F06  多阶段工作流：文献分析八步流水线")
    steps = ["搜索", "筛选", "阅读", "建表", "分析", "写作", "审查", "修改"]
    desc = ["关键词\n找候选", "按标准\n去重排序", "通读\n做笔记", "结构化\n入表",
            "对比\n找结论", "初稿", "自检\n查证据", "定稿"]
    kinds = ["INPUT","INPUT","STD","PROC","PROC","PROC","CORE","OUT"]
    n = len(steps)
    xs = np.linspace(7, 93, n)
    for i, ((s, d, k), x) in enumerate(zip(zip(steps, desc, kinds), xs)):
        rbox(ax, x, 55, 10, 20, k, s, fs=12.5, fw="bold", sub=d, sub_fs=9)
        if i < n-1:
            arrow(ax, (x+5.1, 55), (xs[i+1]-5.1, 55), lw=2)
    ax.text(50, 25, "每步有明确输入和产出；前一步产出是后一步输入",
            ha="center", fontsize=11, color="#444")
    ax.text(50, 18, "审查 → 修改 不通过时回到 写作（虚线反馈）",
            ha="center", fontsize=10.5, color=ARROW_AUX)
    arrow(ax, (xs[6], 44), (xs[5], 44), aux=True, curve=-0.25)
    legend_row(ax, ALL_LEGEND)
    return save(fig, "F06_多阶段工作流")
