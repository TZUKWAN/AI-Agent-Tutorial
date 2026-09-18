#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fix EXTRA_IMAGE_RULES in build_docx.py"""

with open('build_docx.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find EXTRA_IMAGE_RULES start and end
start = None
end = None
for i, line in enumerate(lines):
    if 'EXTRA_IMAGE_RULES = [' in line:
        start = i
    if start is not None and i > start and line.strip() == ']':
        end = i
        break

print(f"Found EXTRA_IMAGE_RULES at lines {start}-{end}")

new_rules = [
    'EXTRA_IMAGE_RULES = [\n',
    '    # Part0-3\n',
    '    ("Part0-3", "好任务与坏任务", "F04_好任务vs坏任务.png", "好任务与坏任务对比"),\n',
    '    ("Part0-3", "四条铁律从这里开始钉", "F20_四大铁律警示.png", "四大铁律警示"),\n',
    '    ("Part0-3", "最小配置：三份就够", "F06_多阶段工作流.png", "多阶段工作流示意"),\n',
    '    # Part6-7\n',
    '    ("Part6-7", "7.1", "F12_能力扩展层级.png", "能力扩展层级"),\n',
    '    ("Part6-7", "资源地图", "F13_社区资源生态.png", "社区资源生态"),\n',
    '    ("Part6-7", "风险", "F14_L1-L4风险分级.png", "L1-L4风险分级"),\n',
    '    ("Part6-7", "推理系统 Model", "F27_模型选择维度雷达.png", "模型选择维度雷达"),\n',
    '    ("Part6-7", "信息系统", "F28_上下文与RAG关系.png", "上下文与RAG关系"),\n',
    '    ("Part6-7", "编排系统", "F26_核心执行循环.png", "核心执行循环"),\n',
    '    # Part8-10\n',
    '    ("Part8-10", "开工前先对齐", "F30_贯穿案例成长路线.png", "贯穿案例成长路线"),\n',
    '    ("Part8-10", "从一个真实愿望拆开", "F22_每日信息监控.png", "每日信息监控"),\n',
    '    ("Part8-10", "人工审批", "F23_邮件处理审批.png", "邮件处理审批"),\n',
    '    ("Part8-10", "从一个能运行的最小 Agent 开始", "F25_Planner-Executor-Evaluator.png", "Planner-Executor-Evaluator"),\n',
    '    ("Part8-10", "LAB B", "F29_8要素文献综述示例.png", "8要素文献综述示例"),\n',
    '    ("Part8-10", "毕业项目", "F31_学习路径地图.png", "学习路径地图"),\n',
    ']\n',
]

# Replace
new_lines = lines[:start] + new_rules + lines[end+1:]

with open('build_docx.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Replaced lines {start}-{end} with {len(new_rules)} new lines")
print("Done")
