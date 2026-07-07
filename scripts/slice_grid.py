#!/usr/bin/env python3
"""Slice a transparent icon sheet by grid or connected components and write a manifest."""

import argparse
import json
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def bbox_from_mask(mask):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)


def crop_save(im, bbox, out, pad=0):
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(im.width, x1 + pad)
    y1 = min(im.height, y1 + pad)
    im.crop((x0, y0, x1, y1)).save(out)
    return [x0, y0, x1 - x0, y1 - y0]


def components(mask, min_area):
    h, w = mask.shape
    seen = np.zeros(mask.shape, dtype=bool)
    found = []
    for sy in range(h):
        for sx in range(w):
            if not mask[sy, sx] or seen[sy, sx]:
                continue
            q = deque([(sx, sy)])
            seen[sy, sx] = True
            xs, ys = [], []
            while q:
                x, y = q.popleft()
                xs.append(x)
                ys.append(y)
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < w and 0 <= ny < h and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((nx, ny))
            if len(xs) >= min_area:
                found.append((min(xs), min(ys), max(xs) + 1, max(ys) + 1))
    return sorted(found, key=lambda b: (b[1], b[0]))


def contact_sheet(icon_paths, out):
    cols = 4
    cell = 160
    rows = max(1, (len(icon_paths) + cols - 1) // cols)
    sheet = Image.new("RGB", (cols * cell, rows * cell), "white")
    draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(icon_paths):
        im = Image.open(path).convert("RGBA")
        im.thumbnail((120, 120))
        x = (i % cols) * cell
        y = (i // cols) * cell
        sheet.paste(im, (x + (cell - im.width) // 2, y + 12), im)
        draw.text((x + 8, y + 132), path.name[:22], fill=(0, 0, 0))
    sheet.save(out)


def parse_grid(raw):
    a, b = raw.lower().replace("*", "x").split("x")
    return int(a), int(b)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("image")
    ap.add_argument("out_dir")
    ap.add_argument("--grid", help="Rows x cols, e.g. 4x4.")
    ap.add_argument("--alpha", type=int, default=12)
    ap.add_argument("--pad", type=int, default=8)
    ap.add_argument("--min-area", type=int, default=80)
    ap.add_argument("--prefix", default="ic")
    ap.add_argument("--contact-sheet", action="store_true")
    args = ap.parse_args()

    im = Image.open(args.image).convert("RGBA")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"source": str(Path(args.image).resolve()), "items": []}
    paths = []

    if args.grid:
        rows, cols = parse_grid(args.grid)
        cw, ch = im.width / cols, im.height / rows
        for r in range(rows):
            for c in range(cols):
                cell = im.crop((int(c * cw), int(r * ch), int((c + 1) * cw), int((r + 1) * ch)))
                arr = np.asarray(cell)
                bbox = bbox_from_mask(arr[:, :, 3] > args.alpha)
                if bbox is None:
                    continue
                out = out_dir / f"{args.prefix}_r{r+1}c{c+1}.png"
                local = crop_save(cell, bbox, out, args.pad)
                source_bbox = [int(c * cw) + local[0], int(r * ch) + local[1], local[2], local[3]]
                manifest["items"].append({"file": out.name, "grid": [r + 1, c + 1], "source_bbox": source_bbox})
                paths.append(out)
    else:
        arr = np.asarray(im)
        boxes = components(arr[:, :, 3] > args.alpha, args.min_area)
        for i, bbox in enumerate(boxes, 1):
            out = out_dir / f"{args.prefix}_{i:02d}.png"
            source_bbox = crop_save(im, bbox, out, args.pad)
            manifest["items"].append({"file": out.name, "source_bbox": source_bbox})
            paths.append(out)

    (out_dir / "icons_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.contact_sheet:
        contact_sheet(paths, out_dir / "icons_contact_sheet.png")
    print(out_dir / "icons_manifest.json")


if __name__ == "__main__":
    main()
