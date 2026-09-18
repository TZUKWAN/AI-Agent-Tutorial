# -*- coding: utf-8 -*-
"""
AI Agent 零基础教程 - 架构图绘制公共工具
配色规范严格按需求执行。
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Polygon, Wedge
from matplotlib.lines import Line2D
import numpy as np

# ---------- 路径 ----------
BASE = r"D:\AISOP\AI-Agent-Tutorial\04_图"
PNG_DIR = os.path.join(BASE, "png")
SVG_DIR = os.path.join(BASE, "svg")
os.makedirs(PNG_DIR, exist_ok=True)
os.makedirs(SVG_DIR, exist_ok=True)

# ---------- 配色 ----------
C = {
    "INPUT_F": "#E8F2F5", "INPUT_E": "#58727D",   # 输入/原始信号
    "STD_F":   "#EAF0F6", "STD_E":   "#63758A",   # 已有/标准组件
    "PROC_F":  "#EDE9F4", "PROC_E":  "#7B6A9A",   # 变换/处理
    "HEAD_F":  "#F4EEDC", "HEAD_E":  "#9A7B3F",   # 任务头/输出头
    "CORE_F":  "#F1D7D4", "CORE_E":  "#B44948",   # 核心创新/重点
    "OUT_F":   "#E5F1E3", "OUT_E":   "#5A8A55",   # 输出/结果
}
ARROW_MAIN = "#263238"
ARROW_AUX = "#6B7280"
TXT = "#222222"

# ---------- 字体 ----------
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["svg.fonttype"] = "none"   # SVG 文字可选

# ---------- 绘图工具 ----------
def new_canvas(w=13, h=7.3, title=""):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    if title:
        ax.text(50, 96, title, ha="center", va="center",
                fontsize=19, fontweight="bold", color=TXT)
    return fig, ax

def rbox(ax, x, y, w, h, kind, text, fs=11, fw="normal", sub=None, sub_fs=9.5,
         text_color=None):
    """圆角矩形. x,y 为中心. kind 为配色键前缀."""
    fc = C[kind + "_F"]; ec = C[kind + "_E"]
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle="round,pad=0.3,rounding_size=1.2",
                         linewidth=1.6, edgecolor=ec, facecolor=fc, zorder=2)
    ax.add_patch(box)
    tc = text_color or TXT
    if sub:
        ax.text(x, y + 1.4, text, ha="center", va="center", fontsize=fs,
                fontweight=fw, color=tc, zorder=3)
        ax.text(x, y - 2.6, sub, ha="center", va="center", fontsize=sub_fs,
                color="#444444", zorder=3)
    else:
        ax.text(x, y, text, ha="center", va="center", fontsize=fs,
                fontweight=fw, color=tc, zorder=3)
    return (x, y, w, h)

def arrow(ax, p1, p2, aux=False, label=None, fs=9, curve=0.0, color=None, lw=2.0):
    """p1,p2 为 (x,y). aux=True 用灰色虚线."""
    if color is None:
        color = ARROW_AUX if aux else ARROW_MAIN
    ls = (0, (4, 3)) if aux else "-"
    cs = "arc3,rad=%.2f" % curve if curve else "arc3,rad=0"
    a = FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=16,
                        linewidth=lw if not aux else 1.5,
                        color=color, linestyle=ls, connectionstyle=cs, zorder=1)
    ax.add_patch(a)
    if label:
        mx, my = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
        ax.text(mx, my + 1.6, label, ha="center", va="bottom",
                fontsize=fs, color=color, zorder=4)
    return a

def save(fig, name):
    png = os.path.join(PNG_DIR, name + ".png")
    svg = os.path.join(SVG_DIR, name + ".svg")
    fig.savefig(png, dpi=200, bbox_inches="tight", facecolor="white")
    fig.savefig(svg, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return png, svg

def legend_row(ax, items, y=3):
    """底部语义色图例. items: list of (kind, label)"""
    n = len(items)
    span = 90
    x0 = 5
    step = span / n
    for i, (k, lab) in enumerate(items):
        x = x0 + step*i + step*0.35
        ax.add_patch(FancyBboxPatch((x, y-1.2), 3, 2.4,
                     boxstyle="round,pad=0.1,rounding_size=0.5",
                     linewidth=1.2, edgecolor=C[k+"_E"], facecolor=C[k+"_F"]))
        ax.text(x+3.8, y, lab, ha="left", va="center", fontsize=9.5, color=TXT)

ALL_LEGEND = [("INPUT","输入/原始"),("STD","已有/标准"),("PROC","变换/处理"),
              ("HEAD","任务/输出头"),("CORE","核心/重点"),("OUT","输出/结果")]
