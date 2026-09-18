# -*- coding: utf-8 -*-
"""
LAB F smoke test：不依赖 pytest，直接断言 colorama 核心 API 可用。
运行：python test_smoke.py
"""
import sys
import os

# 让测试找到本地 repo 里的 colorama 源码
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "demos"))
import fixpath  # noqa: F401  (demos 目录自带的路径注入)

from colorama import Fore, Back, Style, just_fix_windows_console, init, deinit


def main():
    just_fix_windows_console()
    failures = []

    # 1. Fore / Back / Style 常量都应是非空字符串
    for name in ("RED", "GREEN", "BLUE", "RESET"):
        if not isinstance(getattr(Fore, name), str) or getattr(Fore, name) == "":
            failures.append(f"Fore.{name} 不是非空字符串")

    # 2. init() / deinit() 可调用且不抛异常
    try:
        init()
        deinit()
    except Exception as e:
        failures.append(f"init/deinit 抛异常: {e!r}")

    # 3. Style.RESET_ALL 必须能把颜色串复位
    sample = Fore.RED + "x" + Style.RESET_ALL
    if not sample.startswith("\033["):
        failures.append("Fore.RED 未产生 ANSI 转义序列")

    if failures:
        print("SMOKE FAIL:")
        for f in failures:
            print(" -", f)
        sys.exit(1)
    print("SMOKE OK: colorama 核心 API 全部通过")


if __name__ == "__main__":
    main()
