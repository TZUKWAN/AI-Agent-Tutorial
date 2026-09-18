# -*- coding: utf-8 -*-
"""F07 F08 F09 F10 F11 F12 F13 F14 F15"""
from draw_common import *

# ========== F07 验证三层证据模型 ==========
def f07():
    fig, ax = new_canvas(12, 8, "F07  验证三层证据模型（金字塔）")
    # 三层金字塔，下宽上窄
    layers = [
        (40, 78, "底层：执行证据", "日志 / 命令记录 / 中间产物", "STD"),
        (55, 52, "中层：输出证据", "文件 / 表格 / 数据 / 可复算结果", "PROC"),
        (70, 26, "顶层：验证证据", "对照验收标准 / 抽检 / 人确认", "CORE"),
    ]
    for y, w, name, desc, k in layers:
        x = 50
        ax.add_patch(FancyBboxPatch((x-w/2, y-9), w, 18,
                     boxstyle="round,pad=0.3,rounding_size=1.2",
                     linewidth=1.8, edgecolor=C[k+"_E"], facecolor=C[k+"_F"]))
        ax.text(x, y+2.5, name, ha="center", fontsize=13, fontweight="bold",
                color=C[k+"_E"])
        ax.text(x, y-3.5, desc, ha="center", fontsize=10.5, color="#333")
    # 向上箭头
    arrow(ax, (88, 35), (88, 65), lw=2)
    ax.text(92, 50, "证据\n越往上\n越接近\n真完成", ha="left", va="center",
            fontsize=10, color=C["CORE_E"])
    ax.text(50, 90, "「它说做完了」不算证据；三层都站得住才算完成",
            ha="center", fontsize=11.5, color="#444")
    legend_row(ax, ALL_LEGEND, y=8)
    return save(fig, "F07_验证三层证据模型")

# ========== F08 验收闭环 ==========
def f08():
    fig, ax = new_canvas(12, 8, "F08  验收闭环")
    elems = ["要求", "证据", "结果", "问题", "修复", "复验"]
    kinds = ["HEAD","STD","OUT","CORE","PROC","PROC"]
    cx, cy, R = 50, 48, 32
    pts = []
    for i, (e, k) in enumerate(zip(elems, kinds)):
        ang = np.pi/2 - i*(2*np.pi/6)
        x = cx + R*np.cos(ang); y = cy + R*np.sin(ang)
        pts.append((x, y))
        rbox(ax, x, y, 14, 10, k, e, fs=12, fw="bold")
    for i in range(6):
        arrow(ax, pts[i], pts[(i+1)%6], lw=1.8, curve=-0.18)
    ax.text(cx, cy, "验收\n通过→交付\n不通过→回修", ha="center", va="center",
            fontsize=11, color=C["CORE_E"], fontweight="bold")
    ax.text(50, 8, "验收不是走形式：每一条要求都要能对应到一条证据",
            ha="center", fontsize=10.5, color="#444")
    legend_row(ax, ALL_LEGEND, y=2)
    return save(fig, "F08_验收闭环")

# ========== F09 失败模式分类 ==========
def f09():
    fig, ax = new_canvas(13.5, 8.2, "F09  Agent 失败模式四大类")
    circ = Circle((50, 52), 9, facecolor=C["CORE_F"], edgecolor=C["CORE_E"], lw=2)
    ax.add_patch(circ)
    ax.text(50, 52, "Agent\n失败", ha="center", va="center",
            fontsize=12, fontweight="bold", color=C["CORE_E"])
    cats = [
        ("幻觉类", ["编造引用", "无中生有", "把不确定当确定"], "PROC", 20, 80),
        ("操作类", ["点错按钮", "改错文件", "越权/误删"], "CORE", 80, 80),
        ("上下文类", ["忘了前面", "信息塞不下", "主次混淆"], "STD", 80, 24),
        ("外部类", ["网络断", "API报错", "权限不足"], "INPUT", 20, 24),
    ]
    for name, items, k, x, y in cats:
        rbox(ax, x, y+6, 26, 9, k, name, fs=12.5, fw="bold")
        for j, it in enumerate(items):
            ax.text(x, y - 1 - j*5, "· " + it, ha="center", fontsize=9.8, color="#333")
        arrow(ax, (50+(x-50)*0.32, 52+(y-4)*0.32),
              (x+(50-x)*0.42, y+3+(52-(y+3))*0.42), aux=True)
    ax.text(50, 8, "先归类，再选择恢复策略：不同类的失败，修法完全不同",
            ha="center", fontsize=10.5, color="#444")
    legend_row(ax, ALL_LEGEND, y=3)
    return save(fig, "F09_失败模式分类")

# ========== F10 恢复策略决策树 ==========
def f10():
    fig, ax = new_canvas(13, 8.5, "F10  出错后怎么办：恢复策略决策树")
    # 决策节点
    nodes = [
        (50, 86, "发生错误", "CORE", 16, 8),
        (30, 68, "能回退吗？", "HEAD", 16, 7),
        (70, 68, "已有备份？", "HEAD", 16, 7),
        (18, 48, "用 Git/版本 回退", "OUT", 20, 7),
        (42, 48, "从备份恢复", "OUT", 18, 7),
        (66, 48, "手动重做这一步", "PROC", 20, 7),
        (88, 48, "原样重试一次", "OUT", 18, 7),
        (30, 26, "修好后继续", "OUT", 16, 7),
        (70, 26, "停下问人", "CORE", 16, 7),
    ]
    for x, y, t, k, w, h in nodes:
        rbox(ax, x, y, w, h, k, t, fs=10.5, fw="bold")
    # 边
    arrow(ax, (50, 82), (34, 71.5), label="是")
    arrow(ax, (50, 82), (66, 71.5), label="否")
    arrow(ax, (26, 65), (19, 51.5), label="有")
    arrow(ax, (34, 65), (41, 51.5), label="无")
    arrow(ax, (66, 65), (66, 51.5), label="有")
    arrow(ax, (74, 65), (85, 51.5), label="无")
    arrow(ax, (18, 44.5), (26, 29.5))
    arrow(ax, (42, 44.5), (34, 29.5))
    arrow(ax, (66, 44.5), (66, 29.5))
    arrow(ax, (88, 44.5), (74, 29.5))
    ax.text(50, 8, "原则：能回退优先回退；不能回退且不能重试 → 立刻停下交给人",
            ha="center", fontsize=10.5, color=C["CORE_E"])
    legend_row(ax, ALL_LEGEND, y=3)
    return save(fig, "F10_恢复策略决策树")

# ========== F11 Agent 认知模型：四系统 + 扩展接口层 ==========
def f11():
    fig, ax = new_canvas(13, 8.6, "F11  Agent 认知模型：四个基本系统 + 一个扩展接口层")
    # 顶部：扩展接口层
    ax.add_patch(FancyBboxPatch((5, 80), 90, 9,
                 boxstyle="round,pad=0.3,rounding_size=1.2",
                 linewidth=1.8, edgecolor=C["HEAD_E"], facecolor=C["HEAD_F"], zorder=2))
    ax.text(50, 86.5, "扩展接口层（Extensibility Layer）",
            ha="center", va="center", fontsize=11.5, fontweight="bold",
            color=C["HEAD_E"], zorder=3)
    ax.text(50, 82.5, "API   ·   Connector   ·   Plugin   ·   MCP   ·   Skill",
            ha="center", va="center", fontsize=10.5, color="#333", zorder=3)

    # 四个基本系统 2x2
    sys4 = [
        ("① 推理系统", "Model",
         "大模型 / 推理 / 决策\n「想」这一步怎么做", "HEAD", 27, 62),
        ("② 信息系统", "Context / Memory / State / RAG",
         "上下文窗口 · 长期记忆\n当前状态 · 检索增强", "INPUT", 73, 62),
        ("③ 行动系统", "Tools",
         "函数调用 · 浏览器\n文件 · 代码执行", "PROC", 27, 38),
        ("④ 编排系统", "Workflow / Planner / Sub-agent",
         "主循环 · 任务拆解\n子 Agent 调度", "CORE", 73, 38),
    ]
    bw, bh = 38, 20
    for name, sub, desc, k, x, y in sys4:
        rbox(ax, x, y, bw, bh, k, "", fs=12)
        ax.text(x, y + 5.5, name, ha="center", va="center",
                fontsize=12.5, fontweight="bold", color=TXT, zorder=3)
        ax.text(x, y + 1.8, sub, ha="center", va="center",
                fontsize=9.5, color=C[k+"_E"], zorder=3, fontweight="bold")
        ax.text(x, y - 4.5, desc, ha="center", va="center",
                fontsize=9.2, color="#444", zorder=3, linespacing=1.35)
        # 从扩展接口层向下的虚线
        arrow(ax, (x, 80), (x, y + bh/2 + 0.4), aux=True, lw=1.2)

    # 系统间协作箭头（顺时针）
    arrow(ax, (46, 62), (54, 62), lw=1.4)            # 推理 -> 信息
    arrow(ax, (73, 48), (73, 52), aux=True, lw=1.2)  # 信息 -> 编排
    arrow(ax, (54, 38), (46, 38), lw=1.4)            # 编排 -> 行动
    arrow(ax, (27, 48), (27, 52), aux=True, lw=1.2)  # 行动 -> 推理

    # 底部说明
    ax.text(50, 22,
            "四个系统缺一不可：推理是脑，信息是记忆与感官，行动是手脚，编排是指挥链",
            ha="center", fontsize=10.5, color=TXT)
    ax.text(50, 16,
            "扩展接口层横切四层：所有外部能力都通过这一层接进来，不污染内部结构",
            ha="center", fontsize=10, color=C["HEAD_E"])
    legend_row(ax, ALL_LEGEND, y=8)
    return save(fig, "F11_Agent架构全景")

# ========== F12 能力供应链 ==========
def f12():
    fig, ax = new_canvas(15, 7.4, "F12  能力供应链：从「发现一个能力」到「安全用上它」")
    steps = [
        ("发现",      "Discover",     "GitHub / 社区\n文档 / 同事推荐",      "INPUT"),
        ("判断来源",  "Source Check", "谁做的？\n是否官方/可信？",          "HEAD"),
        ("读权限",    "Read Perm.",   "要读什么？\n要写什么？要不要钱？",   "STD"),
        ("安装",      "Install",      "隔离环境\n锁定版本",                 "PROC"),
        ("沙箱验证",  "Sandbox Test", "跑一遍看行为\n对照 L1-L4 风险",      "CORE"),
        ("升级",      "Upgrade",      "按需升级\n变更点要重验",             "PROC"),
        ("撤销",      "Rollback",     "出问题卸载\n恢复原状",               "OUT"),
    ]
    n = len(steps)
    xs = np.linspace(7, 93, n)
    y = 56
    bw, bh = 10.8, 26
    for i, ((cn, en, desc, k), x) in enumerate(zip(steps, xs)):
        rbox(ax, x, y, bw, bh, k, "", fs=11, fw="bold")
        ax.text(x, y + 7.5, cn, ha="center", va="center",
                fontsize=12.5, fontweight="bold", color=TXT, zorder=3)
        ax.text(x, y + 3.5, en, ha="center", va="center",
                fontsize=8.8, color=C[k+"_E"], zorder=3, style="italic")
        ax.text(x, y - 3.5, desc, ha="center", va="center",
                fontsize=8.6, color="#444", zorder=3, linespacing=1.35)
        if i < n - 1:
            arrow(ax, (x + bw/2 + 0.15, y), (xs[i+1] - bw/2 - 0.15, y), lw=1.8)
    # 撤销回到发现的反馈虚线（供应链回流，下移避免压字）
    loop_y = y - bh/2 - 4.5
    arrow(ax, (xs[6], loop_y), (xs[0], loop_y),
          aux=True, curve=-0.15, lw=1.4)
    ax.text(50, loop_y - 2.2, "能力出问题 → 撤销 → 重新评估（供应链回流）",
            ha="center", fontsize=9.5, color=ARROW_AUX, zorder=4)
    ax.text(50, 20, "原则：能力不是「装上就行」，而是一条可审计、可回退的供应链",
            ha="center", fontsize=11.5, color=C["CORE_E"], fontweight="bold")
    ax.text(50, 13, "每一步都留痕：来源、权限、验证结果、版本号——出事能定位到哪一环",
            ha="center", fontsize=10.5, color="#444")
    legend_row(ax, ALL_LEGEND, y=6)
    return save(fig, "F12_能力扩展层级")

# ========== F13 社区资源生态 ==========
def f13():
    fig, ax = new_canvas(13, 8, "F13  社区资源生态：Agent 能力从哪里来")
    circ = Circle((50, 52), 11, facecolor=C["CORE_F"], edgecolor=C["CORE_E"], lw=2)
    ax.add_patch(circ)
    ax.text(50, 52, "Agent\n能力扩展", ha="center", va="center",
            fontsize=12, fontweight="bold", color=C["CORE_E"])
    cats = [
        ("Skill", "现成工作方法", "PROC", 18, 80),
        ("MCP", "外部系统连接", "PROC", 82, 80),
        ("Plugin", "工具包", "STD", 86, 26),
        ("Connector", "数据源接入", "INPUT", 50, 14),
        ("Framework", "开发框架", "HEAD", 14, 26),
    ]
    for name, desc, k, x, y in cats:
        rbox(ax, x, y, 17, 10, k, name, fs=11, sub=desc, sub_fs=9)
        arrow(ax, (50+(x-50)*0.3, 52+(y-52)*0.3),
              (x+(50-x)*0.22, y+(52-y)*0.22), aux=True)
    ax.text(50, 6, "先判断缺的是「方法」「连接」还是「工具包」，再去社区找对应类型",
            ha="center", fontsize=10.5, color="#444")
    legend_row(ax, ALL_LEGEND, y=2)
    return save(fig, "F13_社区资源生态")

# ========== F14 L1-L4 风险分级 ==========
def f14():
    fig, ax = new_canvas(13, 7.8, "F14  第三方资源风险分级 L1-L4")
    rows = [
        ("L1", "低风险", "只读公开资料", "可直接用", "OUT"),
        ("L2", "中低", "装公开 Skill/Plugin", "看一眼来源即可", "STD"),
        ("L3", "中高", "联网/可写文件", "12问审查后再装", "PROC"),
        ("L4", "高风险", "可删/可发送/可执行", "默认拒绝，必须人确认", "CORE"),
    ]
    colors = ["#5A8A55","#7BA05B","#C9A24B","#B44948"]
    for i, (lv, name, ex, str_, k) in enumerate(rows):
        y = 72 - i*15
        h = 10 + i*3
        x0 = 8 + i*1.5
        ax.add_patch(FancyBboxPatch((x0, y-h/2), 86-i*3, h,
                     boxstyle="round,pad=0.2,rounding_size=1",
                     linewidth=1.6, edgecolor=colors[i],
                     facecolor=C[k+"_F"]))
        ax.text(13, y, lv, fontsize=13, fontweight="bold", color=colors[i], va="center")
        ax.text(22, y+1.5, name, fontsize=11.5, fontweight="bold", va="center")
        ax.text(40, y+1.5, "示例：" + ex, fontsize=10.5, va="center")
        ax.text(40, y-2.5, "策略：" + str_, fontsize=10, va="center", color="#444")
    ax.text(50, 6, "风险随「能否影响外部/能否不可逆」递增，不随热度递减",
            ha="center", fontsize=10.5, color="#444")
    return save(fig, "F14_L1-L4风险分级")

# ========== F15 Skill 安装安全审查 ==========
def f15():
    fig, ax = new_canvas(14.5, 7.5, "F15  Skill 安装安全审查：12 问流程")
    steps = ["发现 Skill", "看作者/来源", "看用途说明", "看装了哪些工具",
             "要不要联网", "读写哪些目录", "会不会删文件", "会不会对外发送",
             "要什么密钥", "最近更新/维护", "有无差评/投诉", "确认安装"]
    kinds = ["INPUT","STD","STD","PROC","PROC","PROC","CORE","CORE","CORE","PROC","STD","OUT"]
    n = len(steps)
    cols = 4
    for i, (s, k) in enumerate(zip(steps, kinds)):
        r = i // cols; c = i % cols
        x = 16 + c*24.5
        y = 70 - r*24
        num = f"{i+1:02d}"
        rbox(ax, x, y, 20, 16, k, f"{num}  {s}", fs=10.5, fw="bold")
        if c < cols-1:
            arrow(ax, (x+10.2, y), (x+14.3, y), lw=1.3)
        elif r < 2:
            arrow(ax, (x, y-8.2), (x-14.5, y-15.8), aux=True, lw=1.3)
    ax.text(50, 8, "任何一问答不上来 → 暂停，不要装",
            ha="center", fontsize=11.5, color=C["CORE_E"], fontweight="bold")
    legend_row(ax, ALL_LEGEND, y=3)
    return save(fig, "F15_Skill安装安全审查")
