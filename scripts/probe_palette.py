#!/usr/bin/env python3
"""Suggest a safe chroma-key color for an image."""

import argparse
import json
from pathlib import Path

from PIL import Image


CANDIDATES = ["#00ff00", "#ff00ff", "#ff7a00", "#8000ff", "#ff0033", "#00ffff"]


def hex_to_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def distance(a, b):
    return sum((a[i] - b[i]) ** 2 for i in range(3)) ** 0.5


def analyze(path):
    im = Image.open(path).convert("RGB")
    im.thumbnail((320, 320))
    pixels = list(im.getdata())
    result = []
    for color in CANDIDATES:
        rgb = hex_to_rgb(color)
        near = sum(1 for p in pixels if distance(p, rgb) < 75)
        result.append({"color": color, "near_pixel_ratio": near / max(1, len(pixels))})
    result.sort(key=lambda item: item["near_pixel_ratio"])
    return {"recommended_key": result[0]["color"], "candidates": result}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("image")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    data = analyze(Path(args.image))
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"recommended_key: {data['recommended_key']}")
        for item in data["candidates"]:
            print(f"{item['color']}: near_pixel_ratio={item['near_pixel_ratio']:.4f}")


if __name__ == "__main__":
    main()
