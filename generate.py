#!/usr/bin/env python3
"""
Generate SVGs from templates + bubbles.json.
Each JSON entry can specify:
  - file:        output filename
  - template:    path to template (default: templates/bubble.svg.tpl)
  - text, from, to, fontColor: template-specific fields
"""

import json
import os

DATA_PATH = "bubbles.json"
OUTPUT_DIR = "bubbles"

# Bubble defaults
BUBBLE_FONT_SIZE = 35
BUBBLE_HEIGHT = 100
CHAR_WIDTH = 20.0
EMOJI_WIDTH = 28.0
PADDING = 140
MIN_WIDTH = 500
MAX_WIDTH = 1400

DEFAULT_BUBBLE_TEMPLATE = "templates/bubble.svg.tpl"


def estimate_text_width(text: str) -> float:
    total = 0.0
    for ch in text:
        if ord(ch) > 0x1F000 or ch in "⚠✨":
            total += EMOJI_WIDTH
        else:
            total += CHAR_WIDTH
    return total


def fill_bubble_fields(template: str, item: dict) -> str:
    text = item["text"]
    estimated = estimate_text_width(text) + PADDING
    width = int(max(MIN_WIDTH, min(MAX_WIDTH, estimated)))
    right = width - 10
    inner_w = right - 10

    replacements = {
        "{{WIDTH}}": str(width),
        "{{HEIGHT}}": str(BUBBLE_HEIGHT),
        "{{INNER_W}}": str(inner_w),
        "{{RIGHT}}": str(right),
        "{{FONT_SIZE}}": str(BUBBLE_FONT_SIZE),
        "{{FONT_COLOR}}": item.get("fontColor", "#FFFFFF"),
        "{{FROM}}": item.get("from", "#000000"),
        "{{TO}}": item.get("to", "#000000"),
        "{{TEXT}}": text,
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    return template


def fill_sakura_fields(template: str, item: dict) -> str:
    return template.replace("{{TEXT}}", item.get("text", ""))


def main():
    if not os.path.exists(DATA_PATH):
        raise SystemExit(f"Data file not found: {DATA_PATH}")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for item in items:
        if "file" not in item:
            print(f"Skipping malformed entry: {item}")
            continue

        template_path = item.get("template", DEFAULT_BUBBLE_TEMPLATE)
        if not os.path.exists(template_path):
            print(f"Missing template: {template_path}, skipping {item['file']}")
            continue

        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()

        if template_path.endswith("sakura.svg.tpl"):
            svg = fill_sakura_fields(template, item)
        else:
            svg = fill_bubble_fields(template, item)

        out_path = os.path.join(OUTPUT_DIR, item["file"])
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"Generated {out_path}")

    print(f"\nDone. {len(items)} file(s) written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
