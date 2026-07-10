#!/usr/bin/env python3
"""Remove a flat chroma-key background from a PNG while preserving object colors."""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def parse_hex(value):
    value = value.lstrip("#")
    return np.array([int(value[i : i + 2], 16) for i in (0, 2, 4)], dtype=np.float32)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--key-color", default="#00ff00")
    ap.add_argument("--tolerance", type=float, default=72.0)
    ap.add_argument("--soft", type=float, default=24.0, help="Feather range after tolerance.")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    out = Path(args.out)
    if out.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite {out}; pass --force.")

    im = Image.open(args.input).convert("RGBA")
    arr = np.asarray(im).astype(np.float32)
    key = parse_hex(args.key_color)
    dist = np.sqrt(((arr[:, :, :3] - key) ** 2).sum(axis=2))
    alpha = np.clip((dist - args.tolerance) / max(args.soft, 1.0), 0.0, 1.0) * 255.0
    arr[:, :, 3] = np.minimum(arr[:, :, 3], alpha)
    out.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA").save(out)
    print(out)


if __name__ == "__main__":
    main()
