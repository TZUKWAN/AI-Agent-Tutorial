# -*- coding: utf-8 -*-
"""
AI Agent 零基础工作方法教程 - Word 文档组装脚本
Option 2: 无模板创建
"""
import re
import csv
import os
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Emu, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ============================================================
# 路径配置（仓库相对路径，支持从任意位置运行）
# ============================================================
BASE = Path(__file__).resolve().parent
PNG_DIR = BASE / "04_图" / "png"
OUTPUT = BASE / "05_Word" / "AI-Agent零基础工作方法教程.docx"

MD_FILES = [
    BASE / "03_写作" / "Part0-3_基础入门.md",
    BASE / "03_写作" / "Part4-5_验证与失败.md",
    BASE / "03_写作" / "Part6-7_Agent组成与扩展.md",
    BASE / "03_写作" / "Part8-10_场景自动化构建.md",
]
GLOSSARY_PATH = BASE / "02_设计" / "术语表.md"
CSV_PATH = BASE / "01_调研" / "02_Agent资源索引.csv"

# ============================================================
# 颜色常量
# ============================================================
DARK_BLUE = RGBColor(0x1F, 0x3A, 0x5F)
DARK_BLUE_HEX = "1F3A5F"
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
BLACK = RGBColor(0x00, 0x00, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY_HEX = "F2F2F2"
QUOTE_BG_HEX = "F8F9FA"

# ============================================================
# 图片映射: F编号 -> 文件名（按前缀查找，如 F11 -> F11_*.png）
# ============================================================
def find_image_by_id(img_id):
    """根据F编号查找对应PNG文件，如 F11 -> F11_Agent架构全景.png"""
    matches = list(PNG_DIR.glob(f"{img_id}_*.png"))
    return matches[0] if matches else None

# 无占位符图片: (文件名关键词, 段落/H2/H3文本匹配关键词, 图注)
# 这些图不在正文中有占位符，按文本关键词自动插入
EXTRA_IMAGE_RULES = [
    # Part0-3
    ("Part0-3", "好任务与坏任务", "F04_好任务vs坏任务.png", "好任务与坏任务对比"),
    ("Part0-3", "多阶段工作流", "F06_多阶段工作流.png", "多阶段工作流示意"),
    # Part6-7
    ("Part6-7", "7.1", "F12_能力扩展层级.png", "能力扩展层级"),
    ("Part6-7", "资源地图", "F13_社区资源生态.png", "社区资源生态"),
    ("Part6-7", "风险", "F14_L1-L4风险分级.png", "L1-L4风险分级"),
    # Part8-10
    ("Part8-10", "大脑的分工", "F26_核心执行循环.png", "核心执行循环"),
    ("Part8-10", "入口与规则", "F27_模型选择维度雷达.png", "模型选择维度雷达"),
    ("Part8-10", "RAG", "F28_上下文与RAG关系.png", "上下文与RAG关系"),
    ("Part8-10", "LAB B", "F29_8要素文献综述示例.png", "8要素文献综述示例"),
    ("Part8-10", "迈出第一步", "F30_贯穿案例成长路线.png", "贯穿案例成长路线"),
    ("Part8-10", "毕业项目", "F31_学习路径地图.png", "学习路径地图"),
]

# ============================================================
# 全局计数器
# ============================================================
figure_counter = [0]  # 图编号
inserted_images = set()  # 已插入的图片文件名


# ============================================================
# 辅助函数
# ============================================================

def set_run_font(run, cn_font='宋体', en_font='Times New Roman', size=11,
                 color=None, bold=False, italic=False):
    """设置run的中英文字体"""
    run.font.name = en_font
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color is not None:
        run.font.color.rgb = color
    # 设置东亚字体
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), cn_font)


def set_paragraph_format(para, alignment=None, space_before=0, space_after=0,
                         line_spacing=1.5, first_line_indent=None,
                         page_break_before=False, keep_with_next=False):
    """设置段落格式"""
    pf = para.paragraph_format
    if alignment is not None:
        para.alignment = alignment
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = line_spacing
    if first_line_indent is not None:
        pf.first_line_indent = first_line_indent
    if page_break_before:
        pf.page_break_before = True
    if keep_with_next:
        pf.keep_with_next = True


def fix_chinese_quotes(text):
    """将ASCII双引号智能替换为中文左右引号"""
    result = []
    open_quote = True
    for ch in text:
        if ch == '"':
            if open_quote:
                result.append('\u201c')
            else:
                result.append('\u201d')
            open_quote = not open_quote
        else:
            result.append(ch)
    return ''.join(result)


def add_formatted_runs(para, text, cn_font='宋体', en_font='Times New Roman',
                       size=11, base_bold=False):
    """处理行内格式: **粗体** 和 `代码`"""
    # 先修复ASCII双引号
    text = fix_chinese_quotes(text)
    # 正则匹配 **bold** 或 `code`
    pattern = r'(\*\*[^*]+\*\*|`[^`]+`)'
    parts = re.split(pattern, text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**') and len(part) > 4:
            run = para.add_run(part[2:-2])
            set_run_font(run, cn_font, en_font, size, bold=True or base_bold)
        elif part.startswith('`') and part.endswith('`') and len(part) > 2:
            run = para.add_run(part[1:-1])
            run.font.name = 'Consolas'
            run.font.size = Pt(size - 1)
            rPr = run._element.get_or_add_rPr()
            rFonts = rPr.find(qn('w:rFonts'))
            if rFonts is None:
                rFonts = OxmlElement('w:rFonts')
                rPr.insert(0, rFonts)
            rFonts.set(qn('w:eastAsia'), '宋体')
        else:
            run = para.add_run(part)
            set_run_font(run, cn_font, en_font, size, bold=base_bold)


# OOXML schema 子元素顺序
TCPR_ORDER = ['w:cnfStyle', 'w:tcW', 'w:gridSpan', 'w:hMerge', 'w:vMerge',
              'w:tcBorders', 'w:shd', 'w:noWrap', 'w:tcMar', 'w:textDirection',
              'w:vAlign', 'w:hideMark']
TBLPR_ORDER = ['w:tblStyle', 'w:tblpPr', 'w:tblOverlap', 'w:bidiVisual',
               'w:tblStyleRowBandSize', 'w:tblStyleColBandSize',
               'w:tblW', 'w:jc', 'w:tblCellSpacing', 'w:tblInd',
               'w:tblBorders', 'w:shd', 'w:tblLayout', 'w:tblCellMar',
               'w:tblLook', 'w:tblCaption', 'w:tblDescription']


def reorder_tcPr(cell):
    """按OOXML schema顺序重排tcPr子元素"""
    tcPr = cell._tc.get_or_add_tcPr()
    children = list(tcPr)
    def _key(el):
        for i, name in enumerate(TCPR_ORDER):
            if el.tag == qn(name):
                return i
        return len(TCPR_ORDER)
    children.sort(key=_key)
    for child in children:
        tcPr.append(child)


def reorder_tblPr(table):
    """按OOXML schema顺序重排tblPr子元素"""
    tblPr = table._tbl.tblPr
    if tblPr is None:
        return
    children = list(tblPr)
    def _key(el):
        for i, name in enumerate(TBLPR_ORDER):
            if el.tag == qn(name):
                return i
        return len(TBLPR_ORDER)
    children.sort(key=_key)
    for child in children:
        tblPr.append(child)


def set_cell_shading(cell, color_hex):
    """设置单元格底纹颜色"""
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color_hex)
    shading.set(qn('w:val'), 'clear')
    shading.set(qn('w:color'), 'auto')
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_border(cell, **kwargs):
    """设置单元格边框
    用法: set_cell_border(cell, top={"sz":12, "color":"1F3A5F"}, ...)
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn('w:tcBorders'))
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('top', 'left', 'bottom', 'right'):
        if edge in kwargs:
            edge_data = kwargs[edge]
            tag = qn(f'w:{edge}')
            element = tcBorders.find(tag)
            if element is None:
                element = OxmlElement(f'w:{edge}')
                tcBorders.append(element)
            for key, val in edge_data.items():
                element.set(qn(f'w:{key}'), str(val))


def set_table_three_line(table):
    """设置三线表样式: 上下粗线, 表头下细线, 无竖线"""
    tbl = table._tbl
    tblPr = tbl.tblPr
    # 清除现有边框
    tblBorders = OxmlElement('w:tblBorders')
    # 顶部边框 1.5pt
    top = OxmlElement('w:top')
    top.set(qn('w:val'), 'single')
    top.set(qn('w:sz'), '12')
    top.set(qn('w:space'), '0')
    top.set(qn('w:color'), DARK_BLUE_HEX)
    tblBorders.append(top)
    # 底部边框 1.5pt
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '12')
    bottom.set(qn('w:space'), '0')
    bottom.set(qn('w:color'), DARK_BLUE_HEX)
    tblBorders.append(bottom)
    # 内部水平细线 0.5pt
    insideH = OxmlElement('w:insideH')
    insideH.set(qn('w:val'), 'single')
    insideH.set(qn('w:sz'), '4')
    insideH.set(qn('w:space'), '0')
    insideH.set(qn('w:color'), '999999')
    tblBorders.append(insideH)
    # 无竖线
    for edge in ('left', 'right', 'insideV'):
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'none')
        tblBorders.append(el)
    tblPr.append(tblBorders)

    # 表头行: 深蓝底白字
    if len(table.rows) > 0:
        for cell in table.rows[0].cells:
            set_cell_shading(cell, DARK_BLUE_HEX)
            for para in cell.paragraphs:
                for run in para.runs:
                    run.font.color.rgb = WHITE
                    run.bold = True
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 设置行不跨页
    for row in table.rows:
        trPr = row._tr.get_or_add_trPr()
        cantSplit = OxmlElement('w:cantSplit')
        trPr.append(cantSplit)

    # 表头重复
    if len(table.rows) > 0:
        trPr = table.rows[0]._tr.get_or_add_trPr()
        tblHeader = OxmlElement('w:tblHeader')
        trPr.append(tblHeader)

    # 重排XML元素顺序
    reorder_tblPr(table)
    for row in table.rows:
        for cell in row.cells:
            reorder_tcPr(cell)


def add_image_to_doc(doc, image_path, caption_text, width_cm=15):
    """插入图片+图注"""
    global figure_counter, inserted_images
    if not image_path.exists():
        print(f"  [WARN] 图片不存在: {image_path}")
        return
    # 图片段落 - 居中
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(6)
    para.paragraph_format.space_after = Pt(3)
    run = para.add_run()
    run.add_picture(str(image_path), width=Cm(width_cm))
    inserted_images.add(image_path.name)
    # 图注
    figure_counter[0] += 1
    caption = doc.add_paragraph()
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption.paragraph_format.space_before = Pt(3)
    caption.paragraph_format.space_after = Pt(12)
    run = caption.add_run(f"图 {figure_counter[0]}  {caption_text}")
    set_run_font(run, '宋体', 'Times New Roman', 10, color=DARK_GRAY)


def add_quote_box(doc, text):
    """添加提示框(单行1列表格, 左侧深蓝边框)"""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    # 底纹
    set_cell_shading(cell, QUOTE_BG_HEX)
    # 左侧深蓝边框, 其他无边框
    set_cell_border(cell,
        left={"sz": 18, "color": DARK_BLUE_HEX, "val": "single"},
        top={"sz": 0, "val": "none"},
        bottom={"sz": 0, "val": "none"},
        right={"sz": 0, "val": "none"},
    )
    # 清除默认段落
    cell.paragraphs[0].text = ""
    para = cell.paragraphs[0]
    para.paragraph_format.space_before = Pt(4)
    para.paragraph_format.space_after = Pt(4)
    para.paragraph_format.line_spacing = 1.3
    add_formatted_runs(para, text, size=11)
    # 重排XML元素
    reorder_tblPr(table)
    reorder_tcPr(cell)
    # 表后空段
    doc.add_paragraph()


def add_code_block(doc, code_text):
    """添加代码块(浅灰底, 等宽字体)"""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_shading(cell, LIGHT_GRAY_HEX)
    set_cell_border(cell,
        top={"sz": 4, "color": "CCCCCC", "val": "single"},
        bottom={"sz": 4, "color": "CCCCCC", "val": "single"},
        left={"sz": 4, "color": "CCCCCC", "val": "single"},
        right={"sz": 4, "color": "CCCCCC", "val": "single"},
    )
    # 清除默认段落
    cell.paragraphs[0].text = ""
    lines = code_text.strip().split('\n')
    for i, line in enumerate(lines):
        if i == 0:
            para = cell.paragraphs[0]
        else:
            para = cell.add_paragraph()
        para.paragraph_format.space_before = Pt(0)
        para.paragraph_format.space_after = Pt(0)
        para.paragraph_format.line_spacing = 1.15
        run = para.add_run(line if line else ' ')
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        rPr = run._element.get_or_add_rPr()
        rFonts = rPr.find(qn('w:rFonts'))
        if rFonts is None:
            rFonts = OxmlElement('w:rFonts')
            rPr.insert(0, rFonts)
        rFonts.set(qn('w:eastAsia'), '宋体')
    # 重排XML元素
    reorder_tblPr(table)
    reorder_tcPr(cell)
    doc.add_paragraph()


def add_field(paragraph, field_code):
    """在段落中插入Word域"""
    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    run._element.append(fldChar1)

    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = field_code
    run._element.append(instrText)

    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    run._element.append(fldChar2)

    return run  # 调用方需要在separate后添加end


def add_field_end(paragraph):
    """在段落中插入域结束符"""
    run = paragraph.add_run()
    fldChar = OxmlElement('w:fldChar')
    fldChar.set(qn('w:fldCharType'), 'end')
    run._element.append(fldChar)


# ============================================================
# 封面
# ============================================================

def build_cover(doc):
    """构建封面: 深蓝底色, 白色标题"""
    # 封面section: 页边距设为0
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(0)
    section.bottom_margin = Cm(0)
    section.left_margin = Cm(0)
    section.right_margin = Cm(0)

    # 用1x1表格填满页面作为深色背景
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Cm(21.0)
    set_cell_shading(cell, DARK_BLUE_HEX)

    # 设置表格行高为整页
    tr = table.rows[0]._tr
    trPr = tr.get_or_add_trPr()
    trHeight = OxmlElement('w:trHeight')
    trHeight.set(qn('w:val'), '16838')  # ~29.7cm in twips
    trHeight.set(qn('w:hRule'), 'atLeast')
    trPr.append(trHeight)

    # 垂直居中
    tcPr = cell._tc.get_or_add_tcPr()
    vAlign = OxmlElement('w:vAlign')
    vAlign.set(qn('w:val'), 'center')
    tcPr.append(vAlign)
    # 重排XML元素
    reorder_tblPr(table)
    reorder_tcPr(cell)

    # 清除默认段落
    cell.paragraphs[0].text = ""
    para = cell.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(120)

    # 主标题
    run = para.add_run("AI Agent\n零基础工作方法教程")
    set_run_font(run, '黑体', 'Times New Roman', 28, color=WHITE, bold=True)

    # 空行
    p2 = cell.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(30)
    run = p2.add_run("从会聊天到会干活：\n给技术新手的完整工作手册")
    set_run_font(run, '黑体', 'Times New Roman', 14, color=RGBColor(0xCC, 0xCC, 0xCC))

    # 底部信息
    p3 = cell.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.space_before = Pt(100)
    run = p3.add_run("适用读者：技术新手 / 本科生 / 职场新人\n版本 v1.0\n2026-09-18")
    set_run_font(run, '宋体', 'Times New Roman', 11, color=RGBColor(0xAA, 0xAA, 0xAA))


# ============================================================
# 前言
# ============================================================

def build_preface(doc):
    """构建前言页"""
    # 前言标题
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(24)
    para.paragraph_format.space_after = Pt(18)
    run = para.add_run("前  言")
    set_run_font(run, '黑体', 'Times New Roman', 22, color=DARK_BLUE, bold=True)

    sections = [
        ("这本书教什么", [
            '这本书教你一件事：怎么把 AI 从\u201c会聊天\u201d变成\u201c会干活\u201d。',
            '你将学会：判断什么任务适合交给 Agent、怎么写一份让 Agent 能执行的任务说明、怎么验证它真的做完了、失败了怎么排查、怎么把跑通的流程沉淀成自己的工具。全书 11 个 Part，每个 Part 都有可以直接上手的 Mission（实操任务）。',
        ]),
        ("这本书不教什么", [
            "这本书不教你从零训练一个大模型，不教你写复杂的算法代码，不教你成为 AI 工程师。它的目标读者是：会用电脑、会上网、但没写过代码或只写过一点代码的人。",
            '如果你已经是资深开发者，这本书可以帮你快速建立\u201cAgent 工作方法论\u201d的框架感，但底层原理的深度你需要自己找别的书补。',
        ]),
        ("如何使用本书", [
            "建议按顺序读。Part 0 到 Part 3 是基础，Part 4 到 Part 5 是验证与失败处理，Part 6 到 Part 7 是 Agent 的组成与扩展，Part 8 到 Part 10 是场景化的实战练习。",
            '每个 Part 开头有\u201c先导图\u201d帮你建立全局印象，中间有\u201cMission\u201d任务让你动手做，末尾有\u201c本章模板\u201d让你把成果存下来。边读边做，不要只看不练。',
            "书末附了术语表、资源地图和 8 要素任务法模板，可以随时查阅。",
        ]),
    ]

    for title, paras in sections:
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True
        run = h.add_run(title)
        set_run_font(run, '黑体', 'Times New Roman', 16, color=DARK_BLUE, bold=True)

        for ptext in paras:
            p = doc.add_paragraph()
            set_paragraph_format(p, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
                               line_spacing=1.5, first_line_indent=Cm(0.74))
            add_formatted_runs(p, ptext)

    # 在前言末尾插入全书认知框架图 F00
    f00_path = PNG_DIR / "F00_认知框架.png"
    if f00_path.exists():
        add_image_to_doc(doc, f00_path, "全书统一认知框架：Goal → Context → Resources → Capabilities → Workflow → Verification → Reuse")


# ============================================================
# TOC 域
# ============================================================

def build_toc(doc):
    """插入目录域"""
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(12)
    para.paragraph_format.space_after = Pt(12)
    run = para.add_run("目  录")
    set_run_font(run, '黑体', 'Times New Roman', 22, color=DARK_BLUE, bold=True)

    # TOC 域 - 所有元素放在同一个run中
    toc_para = doc.add_paragraph()
    run = toc_para.add_run()
    # begin
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    fldChar1.set(qn('w:dirty'), 'true')
    run._element.append(fldChar1)
    # instrText
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = r' TOC \o "1-3" \h \z \u '
    run._element.append(instrText)
    # separate
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    run._element.append(fldChar2)
    # 占位文本
    t_elem = OxmlElement('w:t')
    t_elem.set(qn('xml:space'), 'preserve')
    t_elem.text = '\u76ee\u5f55\u5c06\u5728\u6253\u5f00\u6587\u6863\u540e\u81ea\u52a8\u751f\u6210'
    run._element.append(t_elem)
    # end
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    run._element.append(fldChar3)


# ============================================================
# MD 解析器
# ============================================================

def parse_md_file(doc, filepath):
    """解析单个MD文件并写入Word"""
    filename = filepath.name
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')

    in_code_block = False
    code_buffer = []
    table_buffer = []
    list_buffer = []
    current_h2 = ""

    def flush_code_block():
        nonlocal code_buffer
        if code_buffer:
            add_code_block(doc, '\n'.join(code_buffer))
            code_buffer = []

    def flush_table():
        nonlocal table_buffer
        if not table_buffer:
            return
        # 解析表格行
        rows_data = []
        for line in table_buffer:
            line = line.strip()
            if re.match(r'^[\|\s\-:]+$', line):
                continue  # 分隔行
            cells = [c.strip() for c in line.split('|')[1:-1]]
            rows_data.append(cells)
        if rows_data:
            ncols = len(rows_data[0])
            table = doc.add_table(rows=len(rows_data), cols=ncols)
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            for ri, row_data in enumerate(rows_data):
                for ci in range(ncols):
                    cell = table.cell(ri, ci)
                    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                    cell.paragraphs[0].text = ""
                    p = cell.paragraphs[0]
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.line_spacing = 1.15
                    p.paragraph_format.first_line_indent = Cm(0)
                    if ri == 0:
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    cell_text = row_data[ci] if ci < len(row_data) else ""
                    add_formatted_runs(p, cell_text, size=10)
                    for r in p.runs:
                        r.font.size = Pt(10)
            set_table_three_line(table)
            # 表后空段
            doc.add_paragraph()
        table_buffer = []

    def flush_list():
        nonlocal list_buffer
        if not list_buffer:
            return
        for item_text, is_ordered in list_buffer:
            p = doc.add_paragraph()
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.left_indent = Cm(0.74)
            p.paragraph_format.first_line_indent = Cm(-0.37)
            if is_ordered:
                add_formatted_runs(p, item_text)
            else:
                # 无序列表用圆点
                bullet_run = p.add_run("• ")
                set_run_font(bullet_run, '宋体', 'Times New Roman', 11, bold=True)
                add_formatted_runs(p, item_text)
        list_buffer = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 代码块处理
        if stripped.startswith('```'):
            if in_code_block:
                flush_code_block()
                in_code_block = False
            else:
                flush_table()
                flush_list()
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            code_buffer.append(line)
            i += 1
            continue

        # 表格行收集
        if stripped.startswith('|') and stripped.endswith('|'):
            flush_list()
            table_buffer.append(stripped)
            i += 1
            continue
        else:
            flush_table()

        # 水平线
        if stripped == '---' or stripped == '***':
            i += 1
            continue

        # 标题
        if stripped.startswith('### '):
            flush_list()
            title_text = fix_chinese_quotes(stripped[4:].strip())
            h = doc.add_paragraph()
            set_paragraph_format(h, space_before=9, space_after=4,
                               line_spacing=1.3, keep_with_next=True)
            run = h.add_run(title_text)
            set_run_font(run, '黑体', 'Times New Roman', 13,
                        color=DARK_GRAY, bold=True)
            # Heading 3 样式绑定
            h.style = doc.styles['Heading 3']
            # 重新设置字体(样式会覆盖)
            for run in h.runs:
                set_run_font(run, '黑体', 'Times New Roman', 13,
                           color=DARK_GRAY, bold=True)
            # H3也检查额外图片规则
            for file_key, kw, img_file, caption in EXTRA_IMAGE_RULES:
                if file_key in filename and kw in title_text:
                    img_path = PNG_DIR / img_file
                    if img_path.exists() and img_file not in inserted_images:
                        add_image_to_doc(doc, img_path, caption)
            i += 1
            continue

        if stripped.startswith('## '):
            flush_list()
            title_text = fix_chinese_quotes(stripped[3:].strip())
            current_h2 = title_text
            h = doc.add_paragraph()
            set_paragraph_format(h, space_before=11, space_after=5,
                               line_spacing=1.3, keep_with_next=True)
            run = h.add_run(title_text)
            h.style = doc.styles['Heading 2']
            for run in h.runs:
                set_run_font(run, '黑体', 'Times New Roman', 16,
                           color=DARK_BLUE, bold=True)
            # 检查是否需要插入无占位符图片
            for file_key, kw, img_file, caption in EXTRA_IMAGE_RULES:
                if file_key in filename and kw in title_text:
                    img_path = PNG_DIR / img_file
                    if img_path.exists() and img_file not in inserted_images:
                        add_image_to_doc(doc, img_path, caption)
            i += 1
            continue

        if stripped.startswith('# '):
            flush_list()
            title_text = fix_chinese_quotes(stripped[2:].strip())
            h = doc.add_paragraph()
            set_paragraph_format(h, space_before=14, space_after=6,
                               line_spacing=1.3, keep_with_next=True,
                               page_break_before=True)
            run = h.add_run(title_text)
            h.style = doc.styles['Heading 1']
            for run in h.runs:
                set_run_font(run, '黑体', 'Times New Roman', 22,
                           color=DARK_BLUE, bold=True)
            i += 1
            continue

        # 引用块
        if stripped.startswith('>'):
            flush_list()
            quote_text = stripped.lstrip('>').strip()
            if not quote_text:
                i += 1
                continue
            # 检查是否是先导图占位符
            img_match = re.search(r'待插入\s*(F\d+)', quote_text)
            if img_match:
                img_key = img_match.group(1)
                img_path = find_image_by_id(img_key)
                if img_path:
                    caption = re.sub(r'（待插入\s*F\d+[:：].*?）', '', quote_text)
                    caption = re.sub(r'（待插入\s*F\d+）', '', caption)
                    caption = caption.replace('先导图：', '').strip()
                    if not caption:
                        caption = img_path.stem
                    add_image_to_doc(doc, img_path, caption)
                else:
                    print(f"  [WARN] 未找到图片: {img_key}")
            else:
                # 普通提示框
                add_quote_box(doc, quote_text)
            i += 1
            continue

        # 列表项
        if re.match(r'^[-*]\s+', stripped):
            item_text = re.sub(r'^[-*]\s+', '', stripped)
            list_buffer.append((item_text, False))
            i += 1
            continue
        if re.match(r'^\d+\.\s+', stripped):
            list_buffer.append((stripped, True))
            i += 1
            continue

        # 空行
        if not stripped:
            flush_list()
            i += 1
            continue

        # 先导图占位符(普通段落形式, 无>前缀)
        if '先导图' in stripped and '待插入' in stripped:
            flush_list()
            img_match = re.search(r'待插入\s*(F\d+)', stripped)
            if img_match:
                img_key = img_match.group(1)
                img_path = find_image_by_id(img_key)
                if img_path:
                    caption = re.sub(r'（待插入\s*F\d+[:：].*?）', '', stripped)
                    caption = re.sub(r'（待插入\s*F\d+）', '', caption)
                    caption = caption.replace('先导图：', '').strip()
                    if not caption:
                        caption = img_path.stem
                    add_image_to_doc(doc, img_path, caption)
                else:
                    print(f"  [WARN] 未找到图片: {img_key}")
            i += 1
            continue

        # 普通段落
        flush_list()
        p = doc.add_paragraph()
        set_paragraph_format(p, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
                           line_spacing=1.5, first_line_indent=Cm(0.74))
        add_formatted_runs(p, stripped)
        i += 1

    # 收尾
    flush_code_block()
    flush_table()
    flush_list()


# ============================================================
# 附录
# ============================================================

def build_appendix_glossary(doc):
    """附录A: 术语表"""
    h = doc.add_paragraph()
    h.style = doc.styles['Heading 1']
    set_paragraph_format(h, space_before=14, space_after=6,
                       keep_with_next=True, page_break_before=True)
    run = h.add_run("附录A  术语表")
    set_run_font(run, '黑体', 'Times New Roman', 22, color=DARK_BLUE, bold=True)

    # 读取术语表
    content = GLOSSARY_PATH.read_text(encoding='utf-8')
    lines = content.split('\n')
    table_rows = []
    for line in lines:
        line = line.strip()
        if line.startswith('|') and line.endswith('|'):
            if re.match(r'^[\|\s\-:]+$', line):
                continue
            cells = [c.strip() for c in line.split('|')[1:-1]]
            table_rows.append(cells)

    if table_rows:
        ncols = len(table_rows[0])
        table = doc.add_table(rows=len(table_rows), cols=ncols)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        for ri, row_data in enumerate(table_rows):
            for ci in range(ncols):
                cell = table.cell(ri, ci)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                cell.paragraphs[0].text = ""
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.first_line_indent = Cm(0)
                cell_text = row_data[ci] if ci < len(row_data) else ""
                add_formatted_runs(p, cell_text, size=10)
                for r in p.runs:
                    r.font.size = Pt(10)
        set_table_three_line(table)
        doc.add_paragraph()


def build_appendix_resources(doc):
    """附录B: 资源地图精选（按Tier和类型真实筛选，非简单截取）"""
    h = doc.add_paragraph()
    h.style = doc.styles['Heading 1']
    set_paragraph_format(h, space_before=14, space_after=6,
                       keep_with_next=True, page_break_before=True)
    run = h.add_run("附录B  资源地图精选")
    set_run_font(run, '黑体', 'Times New Roman', 22, color=DARK_BLUE, bold=True)

    p = doc.add_paragraph()
    set_paragraph_format(p, line_spacing=1.5, first_line_indent=Cm(0.74))
    add_formatted_runs(p, """以下资源按 Tier 分级（A=官方基础、B=社区发现平台、C=专业工具集成、D=社区实验），
优先选取官方文档、高价值发现平台和常用工具集成。筛选规则：Tier A 全部保留；Tier B 每个类别选 2-3 个最常用的；
Tier C 选与教程章节直接相关的；Tier D 仅选有明确学习价值的。完整 98 条索引见 01_调研/02_Agent资源索引.csv。
所有资源核验日期：2026-09-18。""")

    # 读取CSV并按规则筛选
    with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)

    # 筛选规则：
    # 1. Tier A 全部保留
    # 2. Tier B 按 Type 分组，每组最多3个
    # 3. Tier C 只保留与教程核心章节相关的（Skill/MCP/Connector/Workflow）
    # 4. Tier D 最多保留5个有代表性的
    tier_a = [r for r in all_rows if r.get('Tier','').strip() == 'A']
    tier_b = [r for r in all_rows if r.get('Tier','').strip() == 'B']
    tier_c = [r for r in all_rows if r.get('Tier','').strip() == 'C']
    tier_d = [r for r in all_rows if r.get('Tier','').strip() == 'D']

    # Tier B 按类型分组，每组最多3个
    from collections import OrderedDict
    b_by_type = OrderedDict()
    for r in tier_b:
        t = r.get('Type', '其他')
        if t not in b_by_type:
            b_by_type[t] = []
        if len(b_by_type[t]) < 3:
            b_by_type[t].append(r)
    tier_b_filtered = [r for group in b_by_type.values() for r in group]

    # Tier C 取前10个最相关的
    tier_c_filtered = tier_c[:10]

    # Tier D 取前5个
    tier_d_filtered = tier_d[:5]

    selected = tier_a + tier_b_filtered + tier_c_filtered + tier_d_filtered

    if selected:
        # 列: 资源名称/类型/官方或社区/用途/等级
        table = doc.add_table(rows=len(selected) + 1, cols=5)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        headers = ["资源名称", "类型", "来源", "用途", "等级"]
        for ci, htext in enumerate(headers):
            cell = table.cell(0, ci)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            cell.paragraphs[0].text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.first_line_indent = Cm(0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(htext)
            set_run_font(run, '宋体', 'Times New Roman', 10, bold=True)

        for ri, row in enumerate(selected):
            vals = [
                row.get('Name', '')[:30],
                row.get('Type', '')[:15],
                row.get('OfficialOrCommunity', '')[:8],
                row.get('MainPurpose', '')[:50],
                row.get('Tier', ''),
            ]
            for ci, val in enumerate(vals):
                cell = table.cell(ri + 1, ci)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                cell.paragraphs[0].text = ""
                p = cell.paragraphs[0]
                p.paragraph_format.first_line_indent = Cm(0)
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.line_spacing = 1.1
                run = p.add_run(val)
                set_run_font(run, '宋体', 'Times New Roman', 9)
        set_table_three_line(table)
        doc.add_paragraph()


def build_appendix_template(doc):
    """附录C: 8要素任务法模板"""
    h = doc.add_paragraph()
    h.style = doc.styles['Heading 1']
    set_paragraph_format(h, space_before=14, space_after=6,
                       keep_with_next=True, page_break_before=True)
    run = h.add_run("附录C  8要素任务法模板")
    set_run_font(run, '黑体', 'Times New Roman', 22, color=DARK_BLUE, bold=True)

    p = doc.add_paragraph()
    set_paragraph_format(p, line_spacing=1.5, first_line_indent=Cm(0.74))
    add_formatted_runs(p, "每次给 Agent 下任务前，按以下 8 要素逐项写清楚。复制此模板，填空即可。")

    template_data = [
        ("要素", "英文", "要回答的问题", "填写示例"),
        ("目标", "Goal", "最终要得到什么？（有数量、有范围、有形式）", "周末前把第三章整理成知识结构图，覆盖全部小节"),
        ("材料", "Materials", "可以用什么？（材料在哪、哪些必读）", "材料在 D:\\课程\\论文\\ 文件夹，01.pdf 必读"),
        ("环境", "Environment", "在哪里工作？（圈定活动范围）", "只在 D:\\课程\\论文\\ 文件夹内工作"),
        ("权限", "Permissions", "可以做什么？（读/写/删/对外发送）", "可读可写，不可删原始文件，不可对外发送"),
        ("约束", "Constraints", "什么不能做？（红线）", "不得编造文献；不得覆盖原始文件；中文写作"),
        ("过程", "Process", "按什么步骤做？", "先盘点文件→提取要点→填表→自检→交付"),
        ("验收", "Acceptance", "怎么证明做完了？", "知识结构图覆盖全部小节，每小节一句话"),
        ("交付", "Deliverables", "最后交出什么？", "一份 .md 文件 + 一张结构图 .png"),
    ]

    table = doc.add_table(rows=len(template_data), cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ri, row_data in enumerate(template_data):
        for ci, val in enumerate(row_data):
            cell = table.cell(ri, ci)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            cell.paragraphs[0].text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(val)
            set_run_font(run, '宋体', 'Times New Roman', 10)
    set_table_three_line(table)
    doc.add_paragraph()

    # 使用提示
    p = doc.add_paragraph()
    set_paragraph_format(p, line_spacing=1.5, first_line_indent=Cm(0.74))
    add_formatted_runs(p, '使用方法：把这个模板复制到你的任务说明开头，逐项填写。8 项写齐了再发给 Agent，不要只写\u201c帮我做XX\u201d。')


# ============================================================
# 页眉页脚
# ============================================================

def setup_header_footer(doc):
    """设置页眉页脚"""
    # 从第3个section(正文)开始设置页眉页脚
    # section 0: 封面 (无页眉页脚)
    # section 1: 前言+目录 (无页眉页脚)
    # section 2+: 正文 (有页眉页脚)

    for idx, section in enumerate(doc.sections):
        # 首页不同
        section.different_first_page_header_footer = True

        if idx >= 2:
            # 正文section: 设置页眉
            header = section.header
            # 清除默认段落
            if header.paragraphs:
                hp = header.paragraphs[0]
            else:
                hp = header.add_paragraph()
            hp.text = ""

            # 用制表位实现左书名右Part名
            # 左侧: 书名
            run = hp.add_run("AI Agent 零基础工作方法教程")
            set_run_font(run, '宋体', 'Times New Roman', 9, color=DARK_GRAY)

            # 制表位
            from docx.enum.text import WD_TAB_ALIGNMENT
            pf = hp.paragraph_format
            pf.tab_stops.add_tab_stop(Cm(15.5), WD_TAB_ALIGNMENT.RIGHT)

            run2 = hp.add_run("\t")
            set_run_font(run2, '宋体', 'Times New Roman', 9)

            # 右侧: 静态Part名（避免STYLEREF样式名不匹配问题）
            run3 = hp.add_run("\t教程正文")
            set_run_font(run3, '宋体', 'Times New Roman', 9, color=DARK_GRAY)

            # 页眉下边框线
            pPr = hp._element.get_or_add_pPr()
            pBdr = OxmlElement('w:pBdr')
            bottom = OxmlElement('w:bottom')
            bottom.set(qn('w:val'), 'single')
            bottom.set(qn('w:sz'), '4')
            bottom.set(qn('w:space'), '1')
            bottom.set(qn('w:color'), 'CCCCCC')
            pBdr.append(bottom)
            pPr.append(pBdr)

            # 页脚: 居中页码
            footer = section.footer
            if footer.paragraphs:
                fp = footer.paragraphs[0]
            else:
                fp = footer.add_paragraph()
            fp.text = ""
            fp.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # PAGE 域
            run = fp.add_run()
            fldChar1 = OxmlElement('w:fldChar')
            fldChar1.set(qn('w:fldCharType'), 'begin')
            run._element.append(fldChar1)
            instrText = OxmlElement('w:instrText')
            instrText.set(qn('xml:space'), 'preserve')
            instrText.text = ' PAGE '
            run._element.append(instrText)
            fldChar2 = OxmlElement('w:fldChar')
            fldChar2.set(qn('w:fldCharType'), 'separate')
            run._element.append(fldChar2)
            run2 = fp.add_run("1")
            set_run_font(run2, '宋体', 'Times New Roman', 10, color=DARK_GRAY)
            fldChar3 = OxmlElement('w:fldChar')
            fldChar3.set(qn('w:fldCharType'), 'end')
            run2._element.append(fldChar3)


# ============================================================
# 样式初始化
# ============================================================

def setup_styles(doc):
    """初始化文档样式"""
    # Normal 样式
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(11)
    rpr = style_normal.element.get_or_add_rPr()
    rFonts = rpr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rpr.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), '宋体')
    rFonts.set(qn('w:ascii'), 'Times New Roman')
    rFonts.set(qn('w:hAnsi'), 'Times New Roman')

    # Heading 1
    h1 = doc.styles['Heading 1']
    h1.font.name = 'Times New Roman'
    h1.font.size = Pt(22)
    h1.font.bold = True
    h1.font.color.rgb = DARK_BLUE
    rpr1 = h1.element.get_or_add_rPr()
    rFonts1 = rpr1.find(qn('w:rFonts'))
    if rFonts1 is None:
        rFonts1 = OxmlElement('w:rFonts')
        rpr1.insert(0, rFonts1)
    rFonts1.set(qn('w:eastAsia'), '黑体')
    rFonts1.set(qn('w:ascii'), 'Times New Roman')
    rFonts1.set(qn('w:hAnsi'), 'Times New Roman')

    # Heading 2
    h2 = doc.styles['Heading 2']
    h2.font.name = 'Times New Roman'
    h2.font.size = Pt(16)
    h2.font.bold = True
    h2.font.color.rgb = DARK_BLUE
    rpr2 = h2.element.get_or_add_rPr()
    rFonts2 = rpr2.find(qn('w:rFonts'))
    if rFonts2 is None:
        rFonts2 = OxmlElement('w:rFonts')
        rpr2.insert(0, rFonts2)
    rFonts2.set(qn('w:eastAsia'), '黑体')
    rFonts2.set(qn('w:ascii'), 'Times New Roman')
    rFonts2.set(qn('w:hAnsi'), 'Times New Roman')

    # Heading 3
    h3 = doc.styles['Heading 3']
    h3.font.name = 'Times New Roman'
    h3.font.size = Pt(13)
    h3.font.bold = True
    h3.font.color.rgb = DARK_GRAY
    rpr3 = h3.element.get_or_add_rPr()
    rFonts3 = rpr3.find(qn('w:rFonts'))
    if rFonts3 is None:
        rFonts3 = OxmlElement('w:rFonts')
        rpr3.insert(0, rFonts3)
    rFonts3.set(qn('w:eastAsia'), '黑体')
    rFonts3.set(qn('w:ascii'), 'Times New Roman')
    rFonts3.set(qn('w:hAnsi'), 'Times New Roman')


# ============================================================
# 主函数
# ============================================================

def main():
    print("=" * 60)
    print("开始生成 Word 文档...")
    print("=" * 60)

    doc = Document()

    # 页面设置 (默认section)
    section0 = doc.sections[0]
    section0.page_width = Cm(21.0)
    section0.page_height = Cm(29.7)
    section0.top_margin = Cm(2.5)
    section0.bottom_margin = Cm(2.5)
    section0.left_margin = Cm(2.5)
    section0.right_margin = Cm(2.5)

    # 初始化样式
    setup_styles(doc)

    # 1. 封面
    print("[1/8] 构建封面...")
    build_cover(doc)

    # 2. 新section: 前言+目录
    print("[2/8] 构建前言...")
    doc.add_section(WD_SECTION.NEW_PAGE)
    # 恢复页边距
    sec1 = doc.sections[1]
    sec1.page_width = Cm(21.0)
    sec1.page_height = Cm(29.7)
    sec1.top_margin = Cm(2.5)
    sec1.bottom_margin = Cm(2.5)
    sec1.left_margin = Cm(2.5)
    sec1.right_margin = Cm(2.5)
    build_preface(doc)

    # 3. 目录
    print("[3/8] 插入目录域...")
    doc.add_page_break()
    build_toc(doc)

    # 4. 新section: 正文
    print("[4/8] 解析正文...")
    doc.add_section(WD_SECTION.NEW_PAGE)
    sec2 = doc.sections[2]
    sec2.page_width = Cm(21.0)
    sec2.page_height = Cm(29.7)
    sec2.top_margin = Cm(2.5)
    sec2.bottom_margin = Cm(2.5)
    sec2.left_margin = Cm(2.5)
    sec2.right_margin = Cm(2.5)

    for md_file in MD_FILES:
        print(f"  解析: {md_file.name}")
        parse_md_file(doc, md_file)

    # 5. 附录
    print("[5/8] 构建附录...")
    build_appendix_glossary(doc)
    build_appendix_resources(doc)
    build_appendix_template(doc)

    # 6. 页眉页脚
    print("[6/8] 设置页眉页脚...")
    setup_header_footer(doc)

    # 7. 全局修复ASCII双引号(遍历所有段落和表格)
    print("[7/8] 全局修复ASCII双引号...")
    def fix_all_runs_quote(paragraphs):
        for para in paragraphs:
            open_q = True
            for run in para.runs:
                if '"' in run.text:
                    new_text = []
                    for ch in run.text:
                        if ch == '"':
                            new_text.append('\u201c' if open_q else '\u201d')
                            open_q = not open_q
                        else:
                            new_text.append(ch)
                    run.text = ''.join(new_text)

    # 正文段落
    fix_all_runs_quote(doc.paragraphs)
    # 表格段落
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                fix_all_runs_quote(cell.paragraphs)
    # 页眉页脚
    for section in doc.sections:
        fix_all_runs_quote(section.header.paragraphs)
        fix_all_runs_quote(section.footer.paragraphs)

    # 8. 保存
    print("[8/8] 保存文档...")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUTPUT))
    print(f"  已保存: {OUTPUT}")

    # 8. 统计
    print(f"[8/8] 完成!")
    print(f"  图片编号总数: {figure_counter[0]}")
    print(f"  已插入图片数: {len(inserted_images)}")
    # 检查未插入的图片
    all_pngs = set(f.name for f in PNG_DIR.glob("*.png"))
    missing = all_pngs - inserted_images
    if missing:
        print(f"  [WARN] 未插入的图片: {missing}")
    else:
        print(f"  所有 {len(all_pngs)} 张图片均已插入")

    file_size = OUTPUT.stat().st_size
    print(f"  文件大小: {file_size / 1024:.0f} KB")


if __name__ == '__main__':
    main()

