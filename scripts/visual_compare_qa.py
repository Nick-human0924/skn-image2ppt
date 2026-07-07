#!/usr/bin/env python3
"""Create side-by-side, blend, diff heatmap, and metrics for source vs preview."""

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageOps


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source")
    ap.add_argument("preview")
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    src = Image.open(args.source).convert("RGB")
    prv = Image.open(args.preview).convert("RGB")
    src = ImageOps.fit(src, prv.size, method=Image.Resampling.LANCZOS)

    side = Image.new("RGB", (src.width * 2, src.height), "white")
    side.paste(src, (0, 0))
    side.paste(prv, (src.width, 0))
    side.save(out / "side_by_side.png")

    Image.blend(src, prv, 0.5).save(out / "blend.png")

    diff = ImageChops.difference(src, prv)
    arr = np.asarray(diff).astype(np.float32)
    gray = np.clip(arr.mean(axis=2) * 3, 0, 255).astype(np.uint8)
    heat = ImageOps.colorize(Image.fromarray(gray, "L"), black="#000000", white="#ff3300")
    heat.save(out / "diff_heatmap.png")

    report = {
        "source": str(Path(args.source).resolve()),
        "preview": str(Path(args.preview).resolve()),
        "size": list(prv.size),
        "mean_abs_diff": float(arr.mean()),
        "p95_abs_diff": float(np.percentile(arr, 95)),
    }
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out / "report.json")


if __name__ == "__main__":
    main()
