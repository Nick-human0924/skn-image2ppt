#!/usr/bin/env python3
"""Draw V6.5 layout boxes on source and optional preview images."""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw


COLORS = {"texts": "red", "icons": "blue", "images": "purple", "assets": "purple", "shapes": "green"}


def iter_slides(deck):
    if "slides" in deck:
        yield from deck["slides"]
    else:
        yield deck


def draw_boxes(base, slide, ref_w, ref_h):
    im = base.convert("RGB")
    draw = ImageDraw.Draw(im)
    sx = im.width / ref_w
    sy = im.height / ref_h
    for kind in ("texts", "icons", "images", "assets", "shapes"):
        for idx, item in enumerate(slide.get(kind, []), 1):
            if item.get("source_bbox"):
                x, y, w, h = item["source_bbox"]
            else:
                x = float(item.get("x", 0)) * ref_w
                y = float(item.get("y", 0)) * ref_h
                w = float(item.get("w", 0)) * ref_w
                h = float(item.get("h", 0)) * ref_h
            box = [x * sx, y * sy, (x + w) * sx, (y + h) * sy]
            color = COLORS.get(kind, "black")
            draw.rectangle(box, outline=color, width=3)
            draw.text((box[0] + 3, box[1] + 3), f"{kind[:1]}{idx}", fill=color)
    return im


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source_image")
    ap.add_argument("layout")
    ap.add_argument("--preview")
    ap.add_argument("--slide-index", type=int, default=1)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    deck = json.loads(Path(args.layout).read_text(encoding="utf-8"))
    slide = list(iter_slides(deck))[args.slide_index - 1]
    source = Image.open(args.source_image)
    ref_w = int(slide.get("ref_width", deck.get("ref_width", source.width)))
    ref_h = int(slide.get("ref_height", deck.get("ref_height", source.height)))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    draw_boxes(source, slide, ref_w, ref_h).save(out_dir / f"slide_{args.slide_index:02d}_source_boxes.png")
    if args.preview:
        preview = Image.open(args.preview)
        draw_boxes(preview, slide, ref_w, ref_h).save(out_dir / f"slide_{args.slide_index:02d}_preview_boxes.png")
    print(out_dir)


if __name__ == "__main__":
    main()
