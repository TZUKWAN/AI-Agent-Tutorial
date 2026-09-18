# -*- coding: utf-8 -*-
"""F16 F17 F18 F19 F20 F21 F22 F23 F24 F25 F26 F27 F28"""
from draw_common import *

# ========== F16 场景实验室导航 ==========
def f16():
    fig, ax = new_canvas(13.5, 7.8, "F16  场景实验室导航：7 个 LAB")
    labs = [
        ("LAB1 学习", "答疑/笔记/复习", "INPUT", 18, 72),
        ("LAB2 科研", "文献综述/写作", "PROC", 50, 80),
        ("LAB3 Office", "文档/表格/PPT", "STD", 82, 72),
        ("LAB4 网络研究", "检索/对比/取证", "INPUT", 18, 40),
        ("LAB5 数据", "清洗/分析/可视化", "PROC", 50, 32),
        ("LAB6 开发", "读码/改码/测试", "HEAD", 82, 40),
        ("LAB7 效率", "自动化/批处理", "OUT", 50, 14),
    ]
    cx, cy = 50, 55
    circ = Circle((cx, cy), 7, facecolor=C["CORE_F"], edgecolor=C["CORE_E"], lw=2)
    ax.add_patch(circ)
    ax.text(cx, cy, "选场景\n练手", ha="center", va="center",
            fontsize=10.5, fontweight="bold", color=C["CORE_E"])
    for name, desc, k, x, y in labs:
        rbox(ax, x, y, 18, 11, k, name, fs=10.5, sub=desc, sub_fs=8.8)
        arrow(ax, (cx+(x-cx)*0.13, cy+(y-cy)*0.13),
              (x+(cx-x)*0.1, y+(cy-y)*0.1), aux=True)
    ax.text(50, 5, "按自己的真实需求挑一个 LAB 开始，不要顺序全做",
            ha="center", fontsize=10.5, color="#444")
    legend_row(ax, ALL_LEGEND, y=1.5)
    return save(fig, "F16_场景实验室导航")

# ========== F17 科研Agent链路（18步） ==========
def f17():
    fig, ax = new_canvas(15, 8, "F17  科研 Agent 完整链路（18 步）")
    steps = ["研究问题","拆子问题","关键词","检索文献","去重筛选","下载PDF",
             "结构化阅读","提取方法/数据","建对比表","找空白","形成论点",
             "找证据链","写初稿","自检引用","数据分析","作图","改稿","投稿准备"]
    kinds = (["INPUT"]*4 + ["STD"]*4 + ["PROC"]*5 + ["CORE"]*2 + ["OUT"]*3)
    n = len(steps)
    per = 6
    for i, (s, k) in enumerate(zip(steps, kinds)):
        r = i // per; c = i % per
        x = 9 + c*16.2
        y = 74 - r*24
        rbox(ax, x, y, 13.5, 15, k, s, fs=10, fw="bold")
        if c < per-1:
            arrow(ax, (x+6.8, y), (x+9.4, y), lw=1.2)
        elif r < 2:
            arrow(ax, (x, y-7.7), (9, y-16.3), aux=True, lw=1.2)
    ax.text(50, 20, "前半段管「读全读准」，中段管「比出论点」，后半段管「写得能投」",
            ha="center", fontsize=11, color="#444")
    legend_row(ax, ALL_LEGEND, y=8)
    return save(fig, "F17_科研Agent链路")

# ========== F18 数据分析Agent流程 ==========
def f18():
    fig, ax = new_canvas(13.5, 7, "F18  数据分析 Agent 流程")
    steps = ["读取数据","清洗","EDA探索","可视化","统计分析","建模","出报告"]
    desc = ["CSV/Excel\n读进来", "缺失/异常\n去重", "分布/相关\n看一眼", "图表\n看懂",
            "假设检验\n回归", "可选\n不强行", "结论+图\n可复现"]
    kinds = ["INPUT","STD","PROC","PROC","PROC","HEAD","OUT"]
    n = len(steps)
    xs = np.linspace(8, 92, n)
    for i, ((s, d, k), x) in enumerate(zip(zip(steps, desc, kinds), xs)):
        rbox(ax, x, 55, 11.5, 21, k, s, fs=11.5, fw="bold", sub=d, sub_fs=8.8)
        if i < n-1:
            arrow(ax, (x+5.8, 55), (xs[i+1]-5.8, 55), lw=1.8)
    ax.text(50, 22, "关键：每步都保留脚本和中间文件，结论必须能被重新跑出来",
            ha="center", fontsize=11, color=C["CORE_E"])
    legend_row(ax, ALL_LEGEND)
    return save(fig, "F18_数据分析Agent流程")

# ========== F19 软件开发Agent流程 ==========
def f19():
    fig, ax = new_canvas(14.5, 7, "F19  软件开发 Agent 流程")
    steps = ["说清需求","找现有项目","Clone仓库","先跑起来","改代码",
             "写/跑测试","Git提交","小范围部署"]
    desc = ["要解决什么","别从零写","拉到本地","读懂再动","小步改",
            "改了要测","留快照","给人用"]
    kinds = ["HEAD","INPUT","STD","STD","PROC","PROC","OUT","OUT"]
    n = len(steps)
    xs = np.linspace(7, 93, n)
    for i, ((s, d, k), x) in enumerate(zip(zip(steps, desc, kinds), xs)):
        rbox(ax, x, 56, 10.5, 20, k, s, fs=10.8, fw="bold", sub=d, sub_fs=8.5)
        if i < n-1:
            arrow(ax, (x+5.3, 56), (xs[i+1]-5.3, 56), lw=1.6)
    ax.text(50, 22, "铁律：先跑起来再改；每改一步就 Git 提交，可回退",
            ha="center", fontsize=11, color=C["CORE_E"], fontweight="bold")
    legend_row(ax, ALL_LEGEND)
    return save(fig, "F19_软件开发Agent流程")

# ========== F20 四大铁律警示 ==========
def f20():
    fig, ax = new_canvas(13, 8, "F20  四大铁律（违反任何一条都可能出事）")
    rules = [
        ("铁律一", "不编造证据", "引用、数据、结果必须可溯源；查不到就说查不到"),
        ("铁律二", "先跑起来再改", "不要凭想象改代码；先复现问题，再小步修"),
        ("铁律三", "危险动作先问人", "删除、覆盖、对外发送、花钱——停下来等确认"),
        ("铁律四", "每步留快照", "Git/备份/检查点；出问题能回到上一个好状态"),
    ]
    for i, (no, t, d) in enumerate(rules):
        r = i // 2; c = i % 2
        x = 27 + c*46; y = 65 - r*34
        ax.add_patch(FancyBboxPatch((x-22, y-13), 44, 26,
                     boxstyle="round,pad=0.4,rounding_size=1.5",
                     linewidth=2.4, edgecolor=C["CORE_E"], facecolor=C["CORE_F"]))
        ax.text(x-18, y+6, no, fontsize=11, color=C["CORE_E"], fontweight="bold")
        ax.text(x, y+6, t, ha="center", fontsize=15, fontweight="bold", color=C["CORE_E"])
        ax.text(x, y-4, d, ha="center", fontsize=10, color="#5a3030")
    ax.text(50, 8, "这四条不依赖具体工具，换任何平台都成立",
            ha="center", fontsize=11, color="#444")
    return save(fig, "F20_四大铁律警示")

# ========== F21 自动化闭环 ==========
def f21():
    fig, ax = new_canvas(11, 8, "F21  自动化闭环")
    elems = [("Trigger", "触发\n(时间/事件)", "INPUT"),
             ("Condition", "条件\n(满足才做)", "HEAD"),
             ("Action", "动作\n(执行任务)", "PROC"),
             ("Notification", "通知\n(告诉人结果)", "OUT")]
    cx, cy, R = 50, 50, 30
    pts = []
    for i, (en, cn, k) in enumerate(elems):
        ang = np.pi/2 - i*(2*np.pi/4)
        x = cx + R*np.cos(ang); y = cy + R*np.sin(ang)
        pts.append((x, y))
        rbox(ax, x, y, 18, 13, k, en, fs=11.5, fw="bold", sub=cn, sub_fs=9.5)
    for i in range(4):
        arrow(ax, pts[i], pts[(i+1)%4], lw=2, curve=-0.2)
    ax.text(cx, cy, "无人值守\n自动跑", ha="center", va="center",
            fontsize=11, color=C["CORE_E"], fontweight="bold")
    ax.text(50, 8, "前提：任务本身可验收，且失败路径有人能接手",
            ha="center", fontsize=10.5, color="#444")
    legend_row(ax, ALL_LEGEND, y=2)
    return save(fig, "F21_自动化闭环")

# ========== F22 每日信息监控 ==========
def f22():
    fig, ax = new_canvas(14, 6.5, "F22  每日信息监控时间线")
    events = [
        ("08:00", "定时触发", "INPUT", 8),
        ("08:05", "抓取订阅源", "STD", 28),
        ("08:10", "对比昨日", "PROC", 48),
        ("08:15", "判断价值", "HEAD", 68),
        ("08:20", "生成摘要 / 静默", "OUT", 88),
    ]
    # 时间轴
    ax.plot([6, 94], [50, 50], color=ARROW_MAIN, lw=2.2, zorder=1)
    for tm, act, k, x in events:
        ax.plot([x], [50], marker="o", markersize=11,
                markerfacecolor=C[k+"_F"], markeredgecolor=C[k+"_E"], zorder=3)
        ax.text(x, 62, tm, ha="center", fontsize=10.5, fontweight="bold", color=C[k+"_E"])
        ax.text(x, 38, act, ha="center", fontsize=10, color="#333")
    arrow(ax, (88, 26), (88, 44), aux=True)
    ax.text(88, 20, "有重要变化才推送\n否则保持安静", ha="center",
            fontsize=9.5, color=ARROW_AUX)
    ax.text(50, 10, "原则：监控是为了不刷屏——没变化就不打扰人",
            ha="center", fontsize=10.5, color="#444")
    return save(fig, "F22_每日信息监控")

# ========== F23 邮件处理审批 ==========
def f23():
    fig, ax = new_canvas(13.5, 6.8, "F23  邮件处理：人在环上审批")
    steps = [
        ("收到邮件", "INPUT", 10),
        ("分析意图", "PROC", 28),
        ("起草回复", "PROC", 46),
        ("人工批准", "CORE", 66),
        ("发送", "OUT", 88),
    ]
    for s, k, x in steps:
        rbox(ax, x, 55, 14, 16, k, s, fs=11.5, fw="bold")
    for x1, x2 in [(17, 21), (35, 39), (53, 59), (73, 81)]:
        arrow(ax, (x1, 55), (x2, 55), lw=2)
    # 人工审批强调框
    ax.add_patch(FancyBboxPatch((57, 42), 18, 26,
                 boxstyle="round,pad=0.3,rounding_size=1.2",
                 linewidth=2.2, edgecolor=C["CORE_E"], facecolor="none",
                 linestyle="--", zorder=1))
    ax.text(66, 36, "唯一人工节点", ha="center", fontsize=10,
            color=C["CORE_E"], fontweight="bold")
    # 不通过回流
    arrow(ax, (66, 47), (46, 47), aux=True, curve=-0.3, label="不通过：改草稿")
    ax.text(50, 18, "Agent 做大部分；「发送」这个不可逆动作必须人点确认",
            ha="center", fontsize=11, color="#444")
    legend_row(ax, ALL_LEGEND, y=8)
    return save(fig, "F23_邮件处理审批")

# ========== F24 构建Agent蓝图 ==========
def f24():
    fig, ax = new_canvas(13, 8.5, "F24  构建自己的 Agent：从 Prompt 到部署")
    blocks = [
        ("System Prompt", "角色/目标/边界", "HEAD", 50, 84, 50, 9),
        ("知识与材料", "RAG/文件/记忆", "INPUT", 20, 66, 22, 9),
        ("工具集", "Tools/MCP/Skill", "STD", 50, 66, 22, 9),
        ("权限与安全", "分级/白名单", "CORE", 80, 66, 22, 9),
        ("工作流编排", "Planner+多步", "PROC", 30, 48, 24, 9),
        ("验收与护栏", "检查/回退", "PROC", 70, 48, 24, 9),
        ("部署", "触发/通知/运行", "OUT", 50, 30, 30, 9),
    ]
    for t, d, k, x, y, w, h in blocks:
        rbox(ax, x, y, w, h, k, t, fs=11.5, fw="bold", sub=d, sub_fs=9)
    arrow(ax, (50, 79.5), (50, 70.5), lw=1.8)
    arrow(ax, (30, 61.5), (30, 52.5), lw=1.5)
    arrow(ax, (50, 61.5), (42, 52.5), aux=True)
    arrow(ax, (80, 61.5), (70, 52.5), aux=True)
    arrow(ax, (30, 43.5), (42, 34.5), lw=1.5)
    arrow(ax, (70, 43.5), (58, 34.5), lw=1.5)
    ax.text(50, 16, "顺序：先把任务跑通，再加工具和护栏，最后才谈部署",
            ha="center", fontsize=10.5, color="#444")
    legend_row(ax, ALL_LEGEND, y=8)
    return save(fig, "F24_构建Agent蓝图")

# ========== F25 Planner-Executor-Evaluator 三角 ==========
def f25():
    fig, ax = new_canvas(11, 8, "F25  Planner - Executor - Evaluator 三角架构")
    tri = [("Planner\n规划", "拆任务\n定步骤", "HEAD", 50, 78),
           ("Executor\n执行", "调工具\n做动作", "PROC", 22, 32),
           ("Evaluator\n评估", "对照标准\n判好坏", "CORE", 78, 32)]
    pts = []
    for t, d, k, x, y in tri:
        pts.append((x, y))
        rbox(ax, x, y, 24, 16, k, t, fs=12, fw="bold", sub=d, sub_fs=9.5)
    # Planner -> Executor
    arrow(ax, (43, 71), (27, 40), label="任务计划")
    # Executor -> Evaluator
    arrow(ax, (35, 32), (65, 32), label="执行结果")
    # Evaluator -> Planner
    arrow(ax, (73, 40), (55, 71), aux=True, label="反馈/重做", curve=0.2)
    ax.text(50, 12, "三角闭环：规划→执行→评估→再规划，直到评估通过",
            ha="center", fontsize=10.5, color="#444")
    legend_row(ax, ALL_LEGEND, y=5)
    return save(fig, "F25_Planner-Executor-Evaluator")

# ========== F26 核心执行循环 ==========
def f26():
    fig, ax = new_canvas(12, 8, "F26  核心执行循环")
    elems = [("定义", "目标/边界", "HEAD"),
             ("规划", "拆步骤", "PROC"),
             ("执行", "调工具", "PROC"),
             ("观察", "看结果", "STD"),
             ("检查", "对照标准", "CORE"),
             ("交付", "完成退出", "OUT")]
    cx, cy, R = 50, 50, 32
    pts = []
    for i, (e, d, k) in enumerate(elems):
        ang = np.pi/2 - i*(2*np.pi/6)
        x = cx + R*np.cos(ang); y = cy + R*np.sin(ang)
        pts.append((x, y))
        rbox(ax, x, y, 14, 10, k, e, fs=11.5, fw="bold", sub=d, sub_fs=8.8)
    for i in range(5):
        arrow(ax, pts[i], pts[i+1], lw=1.8, curve=-0.15)
    # 不符合 -> 回到执行
    arrow(ax, pts[5], pts[2], aux=True, curve=-0.4, label="不符合：修复后重执")
    ax.text(cx, cy, "符合→交付", ha="center", va="center",
            fontsize=11, color=C["OUT_E"], fontweight="bold")
    ax.text(50, 8, "这一圈转得越快、检查越严，Agent 越靠谱",
            ha="center", fontsize=10.5, color="#444")
    legend_row(ax, ALL_LEGEND, y=2)
    return save(fig, "F26_核心执行循环")

# ========== F27 模型选择维度雷达 ==========
def f27():
    axes_labels = ["推理", "编码", "上下文", "工具调用", "多模态", "速度"]
    N = len(axes_labels)
    ang = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    ang += ang[:1]
    models = [
        ("模型A：推理旗舰", [9, 8, 7, 8, 7, 4], "#B44948"),
        ("模型B：编码型", [7, 9, 8, 8, 5, 7], "#7B6A9A"),
        ("模型C：轻量快速", [5, 6, 5, 7, 6, 9], "#5A8A55"),
    ]
    fig = plt.figure(figsize=(11, 8), dpi=200)
    ax = fig.add_subplot(111, polar=True)
    ax.set_theta_offset(np.pi/2); ax.set_theta_direction(-1)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(axes_labels, fontsize=12)
    ax.set_ylim(0, 10); ax.set_yticks([2,4,6,8,10])
    ax.set_yticklabels(["2","4","6","8","10"], fontsize=8, color="#888")
    for name, vals, col in models:
        v = vals + vals[:1]
        ax.plot(ang, v, color=col, lw=2, label=name)
        ax.fill(ang, v, color=col, alpha=0.12)
    ax.set_title("F27  模型选择维度雷达（示例）", fontsize=17,
                 fontweight="bold", pad=24, color=TXT)
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), fontsize=10.5)
    fig.text(0.5, 0.06, "按任务需求选：科研重推理，工程重编码，自动化重工具调用与速度",
             ha="center", fontsize=10.5, color="#444")
    png = os.path.join(PNG_DIR, "F27_模型选择维度雷达.png")
    svg = os.path.join(SVG_DIR, "F27_模型选择维度雷达.svg")
    fig.savefig(png, dpi=200, bbox_inches="tight", facecolor="white")
    fig.savefig(svg, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return png, svg

# ========== F28 上下文与RAG关系 ==========
def f28():
    fig, ax = new_canvas(13, 7.5, "F28  上下文 vs RAG：别把所有东西都塞进去")
    # 左：全部塞入
    ax.add_patch(FancyBboxPatch((4, 20), 40, 60, boxstyle="round,pad=0.4,rounding_size=1.5",
                 linewidth=1.8, edgecolor=C["CORE_E"], facecolor="#FBEDEC"))
    ax.text(24, 74, "做法一：全部塞进上下文", ha="center", fontsize=12.5,
            fontweight="bold", color=C["CORE_E"])
    left = ["· 材料越多越好", "· 模型看不过来", "· 重要信息被淹没",
            "· 成本高/变慢", "· 容易抓错重点"]
    for i, t in enumerate(left):
        ax.text(8, 64 - i*8, t, fontsize=10.5, color="#7a3b3a")
    # 右：检索+上下文
    ax.add_patch(FancyBboxPatch((56, 20), 40, 60, boxstyle="round,pad=0.4,rounding_size=1.5",
                 linewidth=1.8, edgecolor=C["OUT_E"], facecolor="#EDF6EC"))
    ax.text(76, 74, "做法二：RAG 检索相关片段", ha="center", fontsize=12.5,
            fontweight="bold", color=C["OUT_E"])
    right = ["· 先建库索引全部材料", "· 按问题检索相关片段",
             "· 只把相关片段放进上下文", "· 上下文小而准", "· 大材料也能用"]
    for i, t in enumerate(right):
        ax.text(60, 64 - i*8, t, fontsize=10.5, color="#3a6b36")
    arrow(ax, (46, 50), (54, 50), lw=2.2)
    ax.text(50, 14, "上下文是「工作台面」，RAG 是「资料室」——按问题取相关资料上台面",
            ha="center", fontsize=11, color="#444")
    return save(fig, "F28_上下文与RAG关系")
