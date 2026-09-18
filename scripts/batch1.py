# -*- coding: utf-8 -*-
"""F00, F31, F30, F01, F02, F03, F04, F29, F05, F06"""
from draw_common import *

# ========== F00 全书总模型：八阶段主线 ==========
def f00():
    fig, ax = new_canvas(15, 7.6, "F00  全书总模型：八阶段任务主线")
    stages = [
        ("1", "定义任务",   "要什么结果？",   "8要素任务法",        "HEAD"),
        ("2", "准备上下文\n与能力", "材料齐了吗？\n工具够吗？", "RAG / 权限 / 工具清单", "INPUT"),
        ("3", "执行",       "开始动手做",     "Planner + 工具调用",  "PROC"),
        ("4", "观察",       "刚才发生了什么？","读日志 / 看中间产物","STD"),
        ("5", "验证",       "做对了吗？",     "三层证据 + 验收标准", "CORE"),
        ("6", "修复",       "不对就改",       "回退 / 重试 / 换路径","PROC"),
        ("7", "交付",       "交给人用",       "文件 / 链接 / 通知",  "OUT"),
        ("8", "沉淀",       "下次怎么更快",   "Skill / 模板 / 记忆", "OUT"),
    ]
    n = len(stages)
    xs = np.linspace(7, 93, n)
    y = 56
    bw, bh = 10.5, 26
    for i, ((no, name, q, m, k), x) in enumerate(zip(stages, xs)):
        rbox(ax, x, y, bw, bh, k, "", fs=11, fw="bold")
        # 序号圆
        ax.add_patch(Circle((x, y + bh/2 - 2.2), 1.6,
                     facecolor=C[k+"_E"], edgecolor=C[k+"_E"], zorder=3))
        ax.text(x, y + bh/2 - 2.2, no, ha="center", va="center",
                fontsize=9.5, fontweight="bold", color="white", zorder=4)
        # 阶段名
        ax.text(x, y + 4.2, name, ha="center", va="center",
                fontsize=10.5, fontweight="bold", color=TXT, zorder=3,
                linespacing=1.15)
        # 核心问题
        ax.text(x, y - 1.2, q, ha="center", va="center",
                fontsize=8.6, color="#333", zorder=3, linespacing=1.25)
        # 方法
        ax.text(x, y - 8.5, m, ha="center", va="center",
                fontsize=8.0, color=C[k+"_E"], zorder=3, linespacing=1.2)
        if i < n - 1:
            arrow(ax, (x + bw/2 + 0.15, y), (xs[i+1] - bw/2 - 0.15, y), lw=1.8)
    # 反馈回路：验证失败 -> 修复 -> 执行（下移到框下方，避免压字）
    loop_y = y - bh/2 - 4.5
    arrow(ax, (xs[5], loop_y), (xs[2], loop_y),
          aux=True, curve=-0.18, lw=1.4)
    ax.text(50, loop_y - 2.2, "验证不通过 → 修复 → 回到执行",
            ha="center", fontsize=9.5, color=ARROW_AUX, zorder=4)
    # 双行总结
    ax.text(50, 20, "人负责：定义任务 · 设定边界 · 验收拍板 · 决定是否沉淀",
            ha="center", fontsize=11.5, color=C["CORE_E"], fontweight="bold")
    ax.text(50, 13, "Agent负责：准备 · 执行 · 观察 · 自检 · 修复 · 交付",
            ha="center", fontsize=11.5, color=C["OUT_E"], fontweight="bold")
    legend_row(ax, ALL_LEGEND, y=6)
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
    xs = np.linspace(8, 92, n)
    y_base = 50
    for i, (lv, name, desc, k) in enumerate(levels):
        y = y_base + (i % 2) * 16
        rbox(ax, xs[i], y, 11.5, 15, k, name, fs=11, fw="bold", sub=f"{lv}\n{desc}", sub_fs=8.6)
        if i < n-1:
            arrow(ax, (xs[i]+5.8, y), (xs[i+1]-5.8, y_base + ((i+1) % 2)*16),
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

# ========== F01 AI 能力三维度 ==========
def f01():
    axes_labels = ["工具调用能力\n(能调多少工具/外部系统)",
                   "自主推进能力\n(能否自己拆步/多步执行)",
                   "持续运行能力\n(能否长时/定时/无人值守)"]
    N = len(axes_labels)
    ang = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    ang += ang[:1]
    forms = [
        ("聊天机器人 Chatbot",   [1.5, 1.5, 1.0], "#63758A"),
        ("副驾驶 Copilot",       [3.5, 3.5, 2.0], "#7B6A9A"),
        ("单轮任务 Agent",       [7.0, 6.0, 4.0], "#9A7B3F"),
        ("自主工作流 Agent",     [9.0, 9.0, 8.5], "#B44948"),
    ]
    fig = plt.figure(figsize=(12, 7.8), dpi=200)
    # 左：雷达图
    ax = fig.add_subplot(121, polar=True)
    ax.set_theta_offset(np.pi/2); ax.set_theta_direction(-1)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(axes_labels, fontsize=10.5)
    ax.set_ylim(0, 10); ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2","4","6","8","10"], fontsize=8, color="#888")
    for name, vals, col in forms:
        v = vals + vals[:1]
        ax.plot(ang, v, color=col, lw=2, label=name)
        ax.fill(ang, v, color=col, alpha=0.10)
    ax.set_title("三维度雷达：能力不是「几级」，是三条独立轴",
                 fontsize=13, fontweight="bold", pad=22, color=TXT)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12),
              fontsize=10, frameon=False, ncol=2)

    # 右：三维度说明卡
    ax2 = fig.add_subplot(122); ax2.axis("off")
    ax2.set_xlim(0, 100); ax2.set_ylim(0, 100)
    dims = [
        ("① 工具调用能力", "Tools / MCP / API",
         "能不能查、能不能改、能不能发出去\n数量 × 类型 × 权限边界", "INPUT", 82),
        ("② 自主推进能力", "Planner / Sub-agent",
         "能不能自己拆任务、看中间结果\n遇到错能不能自己换路子", "PROC", 50),
        ("③ 持续运行能力", "Schedule / Long-running",
         "能不能定时跑、挂着跑、断了续跑\n失败能不能自己告警", "CORE", 18),
    ]
    for name, sub, desc, k, y in dims:
        ax2.add_patch(FancyBboxPatch((4, y-13), 92, 26,
                     boxstyle="round,pad=0.3,rounding_size=1.2",
                     linewidth=1.6, edgecolor=C[k+"_E"], facecolor=C[k+"_F"], zorder=2))
        ax2.text(8, y+6, name, fontsize=12.5, fontweight="bold",
                 color=C[k+"_E"], va="center")
        ax2.text(8, y+0.5, sub, fontsize=9.5, color="#444", va="center")
        ax2.text(8, y-6, desc, fontsize=9.5, color="#333",
                 va="center", linespacing=1.4)
    fig.suptitle("F01  AI 能力三维度：工具调用 × 自主推进 × 持续运行",
                 fontsize=16, fontweight="bold", y=0.98, color=TXT)
    fig.text(0.5, 0.03,
             "三维独立：一个 Agent 可以工具很强但跑不长，也可以挂着跑但只会一件事——别再用「Chatbot/Copilot/Agent」一句话概括",
             ha="center", fontsize=10, color="#444")
    png = os.path.join(PNG_DIR, "F01_从聊天到Agent.png")
    svg = os.path.join(SVG_DIR, "F01_从聊天到Agent.svg")
    fig.savefig(png, dpi=200, bbox_inches="tight", facecolor="white")
    fig.savefig(svg, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return png, svg

# ========== F02 工作区与权限模型 ==========
def f02():
    fig, ax = new_canvas(13, 7.8, "F02  工作区与权限模型")
    # 中心
    circ = Circle((50, 55), 11, facecolor=C["HEAD_F"], edgecolor=C["HEAD_E"], lw=2, zorder=2)
    ax.add_patch(circ)
    ax.text(50, 55, "工作区\nWorkspace", ha="center", va="center",
            fontsize=14, fontweight="bold", color=C["HEAD_E"])
    # 周围资源
    res = [("本地文件", 20, 71), ("上传文件", 80, 71),
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
    ax.text(50, 92, "四级权限（逐级升高，风险递增）", ha="center",
            fontsize=12, fontweight="bold", color="#444")
    for name, desc, k, x in perms:
        rbox(ax, x, 86, 16, 7, k, name, fs=10.5, sub=desc, sub_fs=8.8)
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
