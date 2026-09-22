#!/usr/bin/env python3
"""静态站点资源与锚点自检脚本。

用途：在没有构建步骤的纯静态仓库里，替代「构建」环节做正确性校验。

检查项：
  1. 本地资源引用是否存在 —— 覆盖 <img src>、<link href>、<script src>
     以及 CSS 中的 url('...') 引用（本仓库的封面图正是通过 url() 引用的）。
  2. 站内锚点是否有对应元素 —— href="#gallery" 必须能找到 id="gallery"。
  3. 是否残留本地绝对路径或失效的常见占位写法。

外部资源（http/https/协议相对）只记录不校验，避免 CI 因网络波动误报。

用法：
    python3 scripts/check_assets.py [file ...]
    不带参数时默认检查 index.html

退出码：0 全部通过；1 存在错误。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

# src="..." / href="..." —— 允许单引号或双引号
ATTR_RE = re.compile(
    r"""\b(?:src|href)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""",
    re.IGNORECASE,
)

# CSS url( ... ) —— 允许可选引号、允许 url() 内含转义引号
URL_RE = re.compile(
    r"""url\(\s*(?:"([^"]*)"|'([^']*)'|([^)]*))\s*\)""",
    re.IGNORECASE,
)

ID_RE = re.compile(r"""\bid\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.IGNORECASE)

# 不需要落盘校验的前缀
EXTERNAL_PREFIXES = ("http://", "https://", "//", "data:", "mailto:", "tel:", "#")

# 明显是待替换占位符的标记
PLACEHOLDER_MARKERS = ("YOUR_", "TODO", "FIXME", "xxx", "localhost")


def _first(groups: tuple[str | None, ...]) -> str:
    """从正则的多个可选捕获组中取出第一个非空值。"""
    for g in groups:
        if g:
            return g.strip()
    return ""


def extract_references(html: str) -> list[tuple[str, str]]:
    """返回 [(引用值, 来源说明)]，保持出现顺序。"""
    refs: list[tuple[str, str]] = []

    for m in ATTR_RE.finditer(html):
        value = _first(m.groups())
        if value:
            refs.append((value, f"属性 {m.group(0).split('=')[0].strip().lower()}"))

    for m in URL_RE.finditer(html):
        value = _first(m.groups())
        if value:
            refs.append((value, "CSS url()"))

    return refs


def extract_ids(html: str) -> set[str]:
    return {_first(m.groups()) for m in ID_RE.finditer(html) if _first(m.groups())}


def main(argv: list[str]) -> int:
    targets = [Path(p) for p in (argv[1:] or ["index.html"])]

    missing_files: list[str] = []
    broken_anchors: list[str] = []
    placeholders: list[str] = []
    local_refs: list[str] = []
    external_refs: list[str] = []

    for path in targets:
        if not path.is_file():
            print(f"[错误] 目标文件不存在：{path}")
            return 1

        html = path.read_text(encoding="utf-8")
        base_dir = path.parent
        ids = extract_ids(html)

        for raw, source in extract_references(html):
            value = raw.strip()

            # ── 锚点单独处理 ──
            if value.startswith("#"):
                anchor = value[1:]
                if anchor and anchor not in ids:
                    broken_anchors.append(f"{path}: {source} → {value}（找不到 id=\"{anchor}\"）")
                continue

            # ── 外部资源只统计 ──
            if value.lower().startswith(EXTERNAL_PREFIXES):
                external_refs.append(f"{path}: {source} → {value}")
                continue

            if not value:
                continue

            # ── 本地资源 ──
            # 去掉查询串与片段，再做 URL 解码（支持中文文件名）
            clean = unquote(value.split("?")[0].split("#")[0])
            resolved = (base_dir / clean).resolve()
            local_refs.append(f"{path}: {source} → {value}")

            if not resolved.is_file():
                missing_files.append(f"{path}: {source} → {value}（文件不存在：{resolved}）")
                continue

            # ── 占位符检查 ──
            lowered = value.lower()
            if any(marker.lower() in lowered for marker in PLACEHOLDER_MARKERS):
                placeholders.append(f"{path}: {source} → {value}")

    # ── 输出报告 ──
    print("=" * 68)
    print("静态资源自检报告")
    print("=" * 68)
    print(f"本地资源引用：{len(local_refs)} 项")
    for line in local_refs:
        print(f"  ✓ {line}")
    print(f"\n外部资源引用：{len(external_refs)} 项（不校验可达性）")
    for line in external_refs[:20]:
        print(f"  · {line}")
    if len(external_refs) > 20:
        print(f"  ... 其余 {len(external_refs) - 20} 项已省略")

    print("\n" + "-" * 68)

    if not missing_files and not broken_anchors:
        print("结果：通过 —— 本地资源与站内锚点全部有效。")
        if placeholders:
            print(f"\n提示：发现 {len(placeholders)} 处疑似占位符（不阻断 CI）：")
            for line in placeholders:
                print(f"  ! {line}")
        return 0

    if missing_files:
        print(f"结果：失败 —— {len(missing_files)} 处本地资源缺失：")
        for line in missing_files:
            print(f"  ✗ {line}")

    if broken_anchors:
        print(f"\n结果：失败 —— {len(broken_anchors)} 处锚点无对应元素：")
        for line in broken_anchors:
            print(f"  ✗ {line}")

    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
