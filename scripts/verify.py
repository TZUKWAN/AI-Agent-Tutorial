# -*- coding: utf-8 -*-
import os
from PIL import Image

PNG_DIR = r"D:\AISOP\AI-Agent-Tutorial\04_图\png"
SVG_DIR = r"D:\AISOP\AI-Agent-Tutorial\04_图\svg"

expected = [
    "F00_认知框架","F31_学习路径地图","F30_贯穿案例成长路线","F01_从聊天到Agent",
    "F02_工作区与权限模型","F03_8要素任务法闭环","F04_好任务vs坏任务","F29_8要素文献综述示例",
    "F05_长任务管理仪表盘","F06_多阶段工作流","F07_验证三层证据模型","F08_验收闭环",
    "F09_失败模式分类","F10_恢复策略决策树","F11_Agent架构全景","F12_能力扩展层级",
    "F13_社区资源生态","F14_L1-L4风险分级","F15_Skill安装安全审查","F16_场景实验室导航",
    "F17_科研Agent链路","F18_数据分析Agent流程","F19_软件开发Agent流程","F20_四大铁律警示",
    "F21_自动化闭环","F22_每日信息监控","F23_邮件处理审批","F24_构建Agent蓝图",
    "F25_Planner-Executor-Evaluator","F26_核心执行循环","F27_模型选择维度雷达","F28_上下文与RAG关系",
]

print(f"期望图数: {len(expected)}")
fails = []
for name in expected:
    png = os.path.join(PNG_DIR, name + ".png")
    svg = os.path.join(SVG_DIR, name + ".svg")
    if not os.path.exists(png):
        fails.append(f"缺PNG: {name}"); continue
    if not os.path.exists(svg):
        fails.append(f"缺SVG: {name}"); continue
    sz = os.path.getsize(png)
    if sz < 10*1024:
        fails.append(f"PNG过小({sz//1024}KB): {name}")
    with Image.open(png) as im:
        w, h = im.size
    print(f"  OK  {name:38s} {sz//1024:4d}KB  {w}x{h}")

# 反向检查：目录里有没有多出来的文件
png_files = {f[:-4] for f in os.listdir(PNG_DIR) if f.endswith('.png')}
extra = png_files - set(expected)
missing = set(expected) - png_files
print("\n=== 总结 ===")
print(f"PNG 文件数: {len(png_files)}  期望: {len(expected)}")
print(f"缺失: {missing or '无'}")
print(f"多余: {extra or '无'}")
print(f"失败项: {fails or '无'}")
