# -*- coding: utf-8 -*-
"""
LAB E：数据分析闭环演示
对 dirty_data.csv 做：读取 → 数据字典 → 质量检查 → 清洗 → 描述统计 → 可视化 → 结论
仅用 Python 标准库 + matplotlib。
产物：
  - cleaned_data.csv        清洗后数据
  - quality_report.md       数据字典 + 质量检查报告
  - analysis_report.md      描述统计与分析结论
  - income_by_city.png      各城市平均月收入柱状图
  - lab_e.log               运行日志
"""
import csv
import logging
import os
import re
from collections import defaultdict
from datetime import datetime
from statistics import mean, median

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 中文字体兜底
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

BASE = os.path.dirname(os.path.abspath(__file__))
IN_CSV = os.path.join(BASE, "dirty_data.csv")
OUT_CLEAN = os.path.join(BASE, "cleaned_data.csv")
OUT_QMD = os.path.join(BASE, "quality_report.md")
OUT_AMD = os.path.join(BASE, "analysis_report.md")
OUT_PNG = os.path.join(BASE, "income_by_city.png")
LOG_FILE = os.path.join(BASE, "lab_e.log")

logger = logging.getLogger("lab_e")
logger.setLevel(logging.INFO)
logger.handlers.clear()
_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
_fh = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
_fh.setFormatter(_fmt)
_sh = logging.StreamHandler()
_sh.setFormatter(_fmt)
logger.addHandler(_fh)
logger.addHandler(_sh)

GENDER_MAP = {
    "男": "男", "M": "男", "m": "男", "male": "男", "Male": "男", "MALE": "男",
    "女": "女", "F": "女", "f": "女", "female": "女", "Female": "女", "FEMALE": "女",
}

DATE_FORMATS = ["%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%m/%d/%Y"]


def parse_income(raw):
    """把 '￥9,000.5' / '12000' / '' 统一成 float；非法返回 None。"""
    if raw is None:
        return None
    s = str(raw).strip().replace("￥", "").replace(",", "")
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def parse_date(raw):
    s = (raw or "").strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            continue
    return None


def load_raw(path):
    rows = []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    logger.info("读取原始数据 %d 行，来自 %s", len(rows), os.path.basename(path))
    return rows


def quality_check(rows):
    """返回质量问题清单与统计。"""
    issues = {
        "age_missing": [], "age_invalid": [],
        "income_missing": [], "income_invalid": [],
        "gender_unmapped": [], "date_unparsed": [],
        "income_unit_suspect": [],
    }
    for r in rows:
        cid = r["客户ID"]
        # 年龄
        age_raw = r["年龄"].strip()
        if age_raw == "":
            issues["age_missing"].append(cid)
        else:
            try:
                age = float(age_raw)
                if age < 18 or age > 100:
                    issues["age_invalid"].append((cid, age_raw))
            except ValueError:
                issues["age_invalid"].append((cid, age_raw))
        # 收入
        inc_raw = r["月收入"].strip()
        inc = parse_income(inc_raw)
        if inc is None:
            issues["income_missing"].append(cid)
        elif inc < 1000 or inc > 1_000_000:
            issues["income_invalid"].append((cid, inc_raw))
        elif inc < 10000 and inc_raw.replace("￥", "").replace(",", "").replace(".", "").isdigit() is False:
            pass
        # 单位疑似：整数个位数（如 15 / 9 / 12）明显不是月薪
        if inc is not None and inc < 1000 and inc > 0:
            issues["income_unit_suspect"].append((cid, inc_raw))
        # 性别
        if r["性别"].strip() not in GENDER_MAP:
            issues["gender_unmapped"].append((cid, r["性别"]))
        # 日期
        if parse_date(r["注册日期"]) is None:
            issues["date_unparsed"].append((cid, r["注册日期"]))
    logger.info("质量检查完成：缺年龄%d、异常年龄%d、缺收入%d、异常收入%d、疑似单位错误%d、性别未映射%d、日期未解析%d",
                len(issues["age_missing"]), len(issues["age_invalid"]),
                len(issues["income_missing"]), len(issues["income_invalid"]),
                len(issues["income_unit_suspect"]), len(issues["gender_unmapped"]),
                len(issues["date_unparsed"]))
    return issues


def clean(rows):
    """在副本上清洗，返回 (cleaned_rows, dropped_log)。"""
    cleaned = []
    dropped = []
    valid_ages, valid_incomes = [], []
    for r in rows:
        cid = r["客户ID"]
        # 年龄
        try:
            age = float(r["年龄"]) if r["年龄"].strip() else None
        except ValueError:
            age = None
        if age is None or age < 18 or age > 100:
            dropped.append((cid, "年龄缺失或越界", r["年龄"]))
            continue
        # 收入
        inc = parse_income(r["月收入"])
        if inc is None or inc < 1000 or inc > 1_000_000:
            dropped.append((cid, "收入缺失/异常/单位错误", r["月收入"]))
            continue
        gender = GENDER_MAP.get(r["性别"].strip(), None)
        if gender is None:
            dropped.append((cid, "性别无法标准化", r["性别"]))
            continue
        date = parse_date(r["注册日期"])
        if date is None:
            dropped.append((cid, "日期无法解析", r["注册日期"]))
            continue
        cleaned.append({
            "客户ID": cid, "姓名": r["姓名"],
            "年龄": int(age), "性别": gender,
            "注册日期": date, "月收入": round(inc, 2),
            "城市": r["城市"].strip(),
        })
        valid_ages.append(age)
        valid_incomes.append(inc)
    logger.info("清洗完成：保留 %d 行，剔除 %d 行", len(cleaned), len(dropped))
    return cleaned, dropped, valid_ages, valid_incomes


def describe(cleaned, ages, incomes):
    """描述统计。"""
    by_city = defaultdict(list)
    by_gender = defaultdict(list)
    for r in cleaned:
        by_city[r["城市"]].append(r["月收入"])
        by_gender[r["性别"]].append(r["月收入"])
    stats = {
        "n": len(cleaned),
        "age_mean": round(mean(ages), 2),
        "age_median": median(ages),
        "age_min": min(ages), "age_max": max(ages),
        "inc_mean": round(mean(incomes), 2),
        "inc_median": median(incomes),
        "inc_min": min(incomes), "inc_max": max(incomes),
        "by_city": {k: round(mean(v), 2) for k, v in sorted(by_city.items())},
        "by_gender": {k: round(mean(v), 2) for k, v in sorted(by_gender.items())},
        "city_counts": {k: len(v) for k, v in sorted(by_city.items())},
    }
    logger.info("描述统计：n=%d 年龄均值%.1f 收入均值%.2f",
                stats["n"], stats["age_mean"], stats["inc_mean"])
    return stats


def make_chart(stats, path):
    cities = list(stats["by_city"].keys())
    vals = [stats["by_city"][c] for c in cities]
    counts = [stats["city_counts"][c] for c in cities]
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=120)
    bars = ax.bar(cities, vals, color="#4C78A8")
    ax.set_title("各城市平均月收入（清洗后样本）", fontsize=13)
    ax.set_ylabel("平均月收入（元）")
    ax.set_xlabel("城市")
    for b, v, c in zip(bars, vals, counts):
        ax.text(b.get_x() + b.get_width() / 2, v + 150, f"{v:,.0f}\n(n={c})",
                ha="center", va="bottom", fontsize=9)
    ax.set_ylim(0, max(vals) * 1.25)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    logger.info("图已保存：%s", path)


def write_outputs(rows_raw, issues, cleaned, dropped, stats):
    # cleaned_data.csv
    with open(OUT_CLEAN, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["客户ID", "姓名", "年龄", "性别", "注册日期", "月收入", "城市"])
        w.writeheader()
        w.writerows(cleaned)
    logger.info("清洗后数据已保存：%s（%d 行）", os.path.basename(OUT_CLEAN), len(cleaned))

    # quality_report.md
    qlines = [
        "# LAB E 数据字典与质量检查报告",
        "",
        "## 一、数据字典",
        "",
        "| 列名 | 含义 | 类型 | 备注 |",
        "|------|------|------|------|",
        "| 客户ID | 客户唯一编号 | 文本 | C001 起递增 |",
        "| 姓名 | 客户英文名 | 文本 | 无重复缺失 |",
        "| 年龄 | 周岁年龄 | 整数 | 合理区间 18-100 |",
        "| 性别 | 性别 | 文本 | 原始混杂 M/F/男/女/male/female，已统一为 男/女 |",
        "| 注册日期 | 首次注册日期 | 日期 | 原始格式混杂（-/./空格斜杠），已统一 ISO 格式 |",
        "| 月收入 | 税后月收入（元） | 数值 | 原始含 ￥ 符号、千分位逗号，已清洗 |",
        "| 城市 | 所在城市 | 文本 | 武汉/北京/上海/深圳/广州 |",
        "",
        "## 二、质量检查结果",
        "",
        f"- 原始行数：{len(rows_raw)}",
        f"- 年龄缺失：{len(issues['age_missing'])} 行（{', '.join(issues['age_missing']) or '无'}）",
        f"- 年龄越界/非数值：{len(issues['age_invalid'])} 行"
        f"（{'; '.join(f'{c}={v}' for c, v in issues['age_invalid']) or '无'}）",
        f"- 月收入缺失：{len(issues['income_missing'])} 行（{', '.join(issues['income_missing']) or '无'}）",
        f"- 月收入异常（<1000 或 >1e6）：{len(issues['income_invalid'])} 行"
        f"（{'; '.join(f'{c}={v}' for c, v in issues['income_invalid']) or '无'}）",
        f"- 疑似单位错误（个位数）：{len(issues['income_unit_suspect'])} 行"
        f"（{'; '.join(f'{c}={v}' for c, v in issues['income_unit_suspect']) or '无'}）",
        f"- 性别未映射：{len(issues['gender_unmapped'])} 行"
        f"（{'; '.join(f'{c}={v}' for c, v in issues['gender_unmapped']) or '无'}）",
        f"- 日期未解析：{len(issues['date_unparsed'])} 行"
        f"（{'; '.join(f'{c}={v}' for c, v in issues['date_unparsed']) or '无'}）",
        "",
        "## 三、清洗动作与理由",
        "",
        "1. 性别：按映射表统一为「男 / 女」两类。",
        "2. 注册日期：依次尝试 `%Y-%m-%d`、`%Y/%m/%d`、`%Y.%m.%d`、`%m/%d/%Y` 四种格式后统一输出 ISO。",
        "3. 月收入：去除「￥」与千分位逗号后转 float。",
        "4. 剔除规则：年龄不在 [18,100]、收入为空或不在 [1000, 1e6]、性别无法映射、日期无法解析——一律整行剔除，并在下表留痕。",
        "",
        "| 客户ID | 剔除原因 | 原始值 |",
        "|--------|----------|--------|",
    ]
    for cid, reason, raw in dropped:
        qlines.append(f"| {cid} | {reason} | {raw} |")
    qlines += [
        "",
        f"清洗后保留 **{len(cleaned)}** 行，剔除 **{len(dropped)}** 行。",
        "",
        "> 原始文件 dirty_data.csv 全程只读，未做任何修改。",
    ]
    with open(OUT_QMD, "w", encoding="utf-8") as f:
        f.write("\n".join(qlines) + "\n")
    logger.info("质量报告已保存：%s", os.path.basename(OUT_QMD))

    # analysis_report.md
    alines = [
        "# LAB E 分析结论报告",
        "",
        f"样本：清洗后 {stats['n']} 条客户记录。",
        "",
        "## 一、描述统计",
        "",
        "### 年龄",
        f"- 均值：{stats['age_mean']} 岁；中位数：{stats['age_median']} 岁；"
        f"区间：{stats['age_min']}-{stats['age_max']} 岁。",
        "",
        "### 月收入（元）",
        f"- 均值：{stats['inc_mean']:,.2f}；中位数：{stats['inc_median']:,.2f}；"
        f"区间：{stats['inc_min']:,.2f} - {stats['inc_max']:,.2f}。",
        "",
        "### 分城市平均月收入",
        "",
        "| 城市 | 样本数 | 平均月收入(元) |",
        "|------|--------|----------------|",
    ]
    for city, val in stats["by_city"].items():
        alines.append(f"| {city} | {stats['city_counts'][city]} | {val:,.2f} |")
    alines += [
        "",
        "### 分性别平均月收入",
        "",
        "| 性别 | 平均月收入(元) |",
        "|------|----------------|",
    ]
    for g, val in stats["by_gender"].items():
        alines.append(f"| {g} | {val:,.2f} |")
    top_city = max(stats["by_city"].items(), key=lambda x: x[1])
    low_city = min(stats["by_city"].items(), key=lambda x: x[1])
    alines += [
        "",
        "## 二、分析结论",
        "",
        f"1. 样本平均年龄 {stats['age_mean']} 岁，中位数 {stats['age_median']} 岁，整体偏青年职场段。",
        f"2. 平均月收入 {stats['inc_mean']:,.0f} 元，中位数 {stats['inc_median']:,.0f} 元；"
        f"均值略{'高' if stats['inc_mean'] > stats['inc_median'] else '低'}于中位数，"
        f"说明收入分布{'右偏（高收入拉动均值）' if stats['inc_mean'] > stats['inc_median'] else '左偏'}。",
        f"3. 城市间差异：**{top_city[0]}** 平均月收入最高（{top_city[1]:,.0f} 元），"
        f"**{low_city[0]}** 最低（{low_city[1]:,.0f} 元），"
        f"极差 {top_city[1]-low_city[1]:,.0f} 元。",
        "",
        "## 三、适用范围与局限",
        "",
        f"- 本结论仅基于清洗后 {stats['n']} 条样例数据，**不代表真实市场**；",
        "- 每城市样本数仅个位数，城市间差异未做显著性检验，不可外推；",
        "- 收入为自报字段，未做税务口径校验；",
        "- 所有数字均可由 cleaned_data.csv + run_lab_e.py 复算。",
        "",
        "配图：`income_by_city.png`（各城市平均月收入柱状图）。",
    ]
    with open(OUT_AMD, "w", encoding="utf-8") as f:
        f.write("\n".join(alines) + "\n")
    logger.info("分析报告已保存：%s", os.path.basename(OUT_AMD))


def main():
    logger.info("=" * 60)
    logger.info("LAB E 开始运行")
    raw = load_raw(IN_CSV)
    issues = quality_check(raw)
    cleaned, dropped, ages, incomes = clean(raw)
    stats = describe(cleaned, ages, incomes)
    make_chart(stats, OUT_PNG)
    write_outputs(raw, issues, cleaned, dropped, stats)
    logger.info("LAB E 全部产物：")
    for p in (OUT_CLEAN, OUT_QMD, OUT_AMD, OUT_PNG, LOG_FILE):
        logger.info("  - %s (%d bytes)", os.path.basename(p), os.path.getsize(p))
    logger.info("LAB E 运行成功")


if __name__ == "__main__":
    main()
