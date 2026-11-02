#!/usr/bin/env python3
"""
Generate SVG speech bubbles from templates/bubble.svg.tpl + bubbles.json.
Output goes to bubbles/.
"""

import json
import os
import re

TEMPLATE_PATH = "templates/bubble.svg.tpl"
DATA_PATH = "bubbles.json"
OUTPUT_DIR = "bubbles"

# Approximate width-per-character at font-size 35, weight 600.
# Tuned for Segoe UI / Arial. Emojis count as ~1.4x a normal char.
CHAR_WIDTH = 20.0
EMOJI_WIDTH = 28.0
PADDING = 140          # left/right breathing room inside the bubble
MIN_WIDTH = 500
MAX_WIDTH = 1400
FONT_SIZE = 35
HEIGHT = 100


def estimate_text_width(text: str) -> float:
    """Rough width estimate that accounts for emoji being wider."""
    total = 0.0
    for ch in text:
        # Emojis live in higher Unicode planes / common emoji ranges
        if ord(ch) > 0x1F000 or ch in "⚠✨":
            total += EMOJI_WIDTH
        else:
            total += CHAR_WIDTH
    return total


def build_svg(template: str, item: dict) -> str:
    text = item["text"]
    estimated = estimate_text_width(text) + PADDING
    width = int(max(MIN_WIDTH, min(MAX_WIDTH, estimated)))
    # Bubble interior right edge (leave 10px margin like the original path)
    right = width - 10
    inner_w = right - 10

    replacements = {
        "{{WIDTH}}": str(width),
        "{{HEIGHT}}": str(HEIGHT),
        "{{INNER_W}}": str(inner_w),
        "{{RIGHT}}": str(right),
        "{{FONT_SIZE}}": str(FONT_SIZE),
        "{{FONT_COLOR}}": item.get("fontColor", "#FFFFFF"),
        "{{FROM}}": item["from"],
        "{{TO}}": item["to"],
        "{{TEXT}}": text,
    }

    out = template
    for key, value in replacements.items():
        out = out.replace(key, value)
    return out


def main():
    if not os.path.exists(TEMPLATE_PATH):
        raise SystemExit(f"Template not found: {TEMPLATE_PATH}")
    if not os.path.exists(DATA_PATH):
        raise SystemExit(f"Data file not found: {DATA_PATH}")

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for item in items:
        if "file" not in item or "text" not in item:
            print(f"Skipping malformed entry: {item}")
            continue
        svg = build_svg(template, item)
        out_path = os.path.join(OUTPUT_DIR, item["file"])
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"Generated {out_path}  (width={svg.split('width=\"')[1].split('\"')[0]})")

    print(f"\nDone. {len(items)} file(s) written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
