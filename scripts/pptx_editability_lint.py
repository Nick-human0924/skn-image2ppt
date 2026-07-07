#!/usr/bin/env python3
"""Lint editable PPTX exports for common Image2PPT failure modes.

Checks are intentionally conservative:
- ZIP integrity
- XML parse validity
- unexpected PowerPoint shrink-to-fit text boxes (`a:normAutofit`)
- very small explicit font runs

Usage:
  python pptx_editability_lint.py deck.pptx --json
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}


def iter_xml_files(zf: zipfile.ZipFile):
    for name in zf.namelist():
        if name.endswith(".xml") or name.endswith(".rels"):
            yield name


def lint_pptx(path: Path, min_body_font_pt: float) -> dict:
    report = {
        "pptx": str(path),
        "zip_valid": False,
        "xml_valid": False,
        "xml_errors": [],
        "slide_count": 0,
        "norm_autofit_count": 0,
        "small_font_runs": [],
        "min_explicit_font_pt": None,
        "warnings": [],
    }

    try:
        with zipfile.ZipFile(path) as zf:
            bad = zf.testzip()
            report["zip_valid"] = bad is None
            if bad is not None:
                report["warnings"].append(f"ZIP CRC failure at {bad}")

            all_xml_valid = True
            for name in iter_xml_files(zf):
                try:
                    ET.fromstring(zf.read(name))
                except Exception as exc:  # noqa: BLE001
                    all_xml_valid = False
                    report["xml_errors"].append({"file": name, "error": str(exc)})
            report["xml_valid"] = all_xml_valid

            slide_names = sorted(
                n for n in zf.namelist()
                if n.startswith("ppt/slides/slide") and n.endswith(".xml")
            )
            report["slide_count"] = len(slide_names)

            min_font = None
            for slide_index, slide_name in enumerate(slide_names, 1):
                root = ET.fromstring(zf.read(slide_name))
                norm_autofit = root.findall(".//a:normAutofit", NS)
                report["norm_autofit_count"] += len(norm_autofit)

                for run in root.findall(".//a:r", NS):
                    rpr = run.find("a:rPr", NS)
                    if rpr is None:
                        continue
                    sz = rpr.attrib.get("sz")
                    if not sz:
                        continue
                    try:
                        pt = int(sz) / 100
                    except ValueError:
                        continue
                    min_font = pt if min_font is None else min(min_font, pt)
                    if pt < min_body_font_pt:
                        text_node = run.find("a:t", NS)
                        text_preview = text_node.text[:40] if text_node is not None and text_node.text else ""
                        report["small_font_runs"].append({
                            "slide": slide_index,
                            "font_pt": round(pt, 2),
                            "text_preview": text_preview,
                        })
            report["min_explicit_font_pt"] = None if min_font is None else round(min_font, 2)
    except Exception as exc:  # noqa: BLE001
        report["warnings"].append(str(exc))

    if report["norm_autofit_count"]:
        report["warnings"].append("Unexpected shrink-to-fit text boxes detected.")
    if report["small_font_runs"]:
        report["warnings"].append(f"Explicit font runs below {min_body_font_pt:g} pt detected.")
    if not report["zip_valid"] or not report["xml_valid"]:
        report["warnings"].append("PPTX package integrity failed; PowerPoint may repair the file.")
    return report


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--min-body-font-pt", type=float, default=9.0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = lint_pptx(args.pptx, args.min_body_font_pt)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"PPTX: {report['pptx']}")
        print(f"ZIP valid: {report['zip_valid']}")
        print(f"XML valid: {report['xml_valid']}")
        print(f"Slides: {report['slide_count']}")
        print(f"normAutofit: {report['norm_autofit_count']}")
        print(f"Min explicit font pt: {report['min_explicit_font_pt']}")
        print(f"Small font runs: {len(report['small_font_runs'])}")
        for warning in report["warnings"]:
            print(f"WARNING: {warning}")
    return 1 if report["warnings"] else 0


if __name__ == "__main__":
    sys.exit(main())
