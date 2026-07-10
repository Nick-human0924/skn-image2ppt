#!/usr/bin/env python3
"""Validate V6.5 layout coordinate and text-size contracts."""

import argparse
import json
from pathlib import Path

from PIL import Image


def iter_slides(deck):
    if "slides" in deck:
        yield from deck["slides"]
    else:
        yield deck


def iter_items(slide):
    for kind in ("texts", "icons", "images", "assets", "shapes"):
        for item in slide.get(kind, []):
            yield kind, item


def close(a, b, eps=0.003):
    return abs(float(a) - float(b)) <= eps


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source_image")
    ap.add_argument("layout")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    src = Image.open(args.source_image)
    deck = json.loads(Path(args.layout).read_text(encoding="utf-8"))
    ref_w = int(deck.get("ref_width", src.width))
    ref_h = int(deck.get("ref_height", src.height))
    errors = []
    warnings = []

    if ref_w != src.width or ref_h != src.height:
        errors.append(f"ref_width/ref_height {ref_w}x{ref_h} != source image {src.width}x{src.height}")

    for si, slide in enumerate(iter_slides(deck), 1):
        slide_ref_w = int(slide.get("ref_width", ref_w))
        slide_ref_h = int(slide.get("ref_height", ref_h))
        for kind, item in iter_items(slide):
            label = item.get("id") or item.get("text") or item.get("file") or kind
            bbox = item.get("source_bbox")
            if bbox:
                exp = [bbox[0] / slide_ref_w, bbox[1] / slide_ref_h, bbox[2] / slide_ref_w, bbox[3] / slide_ref_h]
                got = [item.get("x"), item.get("y"), item.get("w"), item.get("h")]
                if any(v is None for v in got):
                    errors.append(f"slide {si} {kind} {label}: missing x/y/w/h")
                elif not all(close(got[i], exp[i]) for i in range(4)):
                    errors.append(f"slide {si} {kind} {label}: fraction box does not match source_bbox")
            elif kind in ("texts", "icons", "images", "assets"):
                errors.append(f"slide {si} {kind} {label}: missing source_bbox")

            if kind == "texts":
                if "size" not in item and "size_ratio" not in item and "source_text_height_px" not in item:
                    warnings.append(f"slide {si} text {label}: missing size/size_ratio/source_text_height_px")
                if item.get("source_text_height_px") and item.get("size"):
                    expected = item["source_text_height_px"] * float(deck.get("slide_height_in", 7.5)) * 72 / slide_ref_h
                    if float(item["size"]) < expected * 0.75 and not item.get("small_text_ok"):
                        warnings.append(f"slide {si} text {label}: size appears too small; expected about {expected:.1f}pt")

    report = {"errors": errors, "warnings": warnings}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if errors or (args.strict and warnings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
