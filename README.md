# SKN Image2PPT

SKN Image2PPT is a Codex skill and reconstruction protocol for turning AI-generated slide images, PPT screenshots, posters, infographics, and other flat reference images into editable PowerPoint files.

It is designed for a common Image2 workflow problem: Image2 or other image-generation models can create visually strong slide images, but those images are not directly editable as PPT. SKN Image2PPT provides a hybrid method to preserve the visual quality of the generated image while rebuilding the business-critical content as editable PowerPoint objects.

## Core Idea

Do not choose between a static screenshot and a simplified editable redraw.

SKN Image2PPT uses a hybrid reconstruction approach:

- Complex visual modules are preserved as high-fidelity visual assets.
- Titles, numbers, labels, bullets, tables, and chart labels are rebuilt as editable PowerPoint objects.
- Layout and asset decisions are recorded in manifest/layout metadata.
- A final Polish Pass removes visible defects such as ghosting, duplicated lines, alignment drift, inconsistent icons, and hard-edged image assets.

The target is:

```text
high visual fidelity
+
business-critical editability
+
reproducible manifest-driven PPT generation
+
final reference-overlay polish
```

## What Problem This Solves

Image-generation tools can produce slide-like images with strong visual quality, but the output is usually a flat PNG/JPEG. That creates practical problems:

- text cannot be edited
- numbers cannot be updated
- tables and labels are baked into pixels
- logos, icons, and charts are hard to reuse
- rebuilding everything as native PPT shapes often destroys visual quality
- pasting the whole image into PowerPoint does not solve editability

SKN Image2PPT addresses this by separating the slide into editable business content and high-fidelity visual assets.

## Reconstruction Philosophy

The skill does not try to make every pixel editable. Instead, it classifies every element by two dimensions:

- how important it is to edit later
- how important it is to preserve visually

Recommended treatment:

| Element | Treatment |
| --- | --- |
| Main title, subtitle, bullets | editable PPT text |
| Numbers, labels, assumptions | editable PPT text/table/chart |
| Cards, dividers, badges | native PPT shapes |
| Simple charts | rebuild as native PPT/SVG/chart as a whole |
| Complex flywheel/map/mechanism diagram | SVM visual base + editable overlays |
| Logo, texture, illustration, photo | high-fidelity visual asset |
| Background glow/wave | transparent PNG/SVG or clean background asset |

## SVM: Semantic Visual Module

An SVM is a complex visual module such as a flywheel, funnel, map, timeline, or mechanism diagram.

For SVMs, SKN Image2PPT keeps a high-fidelity text-free visual base and overlays editable PowerPoint text for business content.

Example:

```text
flywheel_visual_base.png
+
editable center title
+
editable segment labels
+
editable bullet lists
+
editable number badges
```

This avoids the two bad extremes:

- flattening the entire slide into one screenshot
- redrawing complex visuals as crude PPT primitives

## Polish Pass

Version 6.1 adds a final Polish Pass. This is a lightweight production step after the editable draft has been generated.

The Polish Pass fixes the defects that are still obvious by eye:

- text ghosting from baked text plus editable overlay text
- duplicated connector lines, dots, icons, or labels
- small x/y alignment drift
- inconsistent border, radius, shadow, or icon style
- hard rectangular crop edges in background assets
- text size, wrapping, or line spacing mismatch

The Polish Pass may use a temporary reference overlay at 30%-50% opacity, but the overlay must be hidden or removed before final delivery.

## Output Structure

A typical project should produce:

```text
project_slug/
  original_inputs/
  assets_v6/
    00_reference/
    01_background/
    02_visual_assets/
    03_svm/
    04_icons/
    05_components/
    06_layout/
      manifest.json
      layout_v6.json
      asset_metadata.json
      polish_manifest.json
    07_output/
      editable_draft.pptx
      editable_reconstruction.pptx
    08_qa/
      draft_preview.png
      reconstruction_preview.png
      diff_overlay.png
      polish_report.md
      quality_report.md
```

## Deliverables

For each conversion, the expected deliverables are:

- editable PPTX
- asset folder or asset package
- layout/manifest JSON
- preview PNG
- diff overlay PNG
- polish report
- quality report

## Usage Prompt

Example prompt:

```text
Use skn-image2ppt to convert this reference slide image into a high-fidelity editable PPTX.
Keep titles, numbers, labels, bullets, tables, and chart labels editable.
Preserve complex visuals as high-fidelity assets or SVM visual bases.
Run a Polish Pass to remove ghosting, duplication, alignment drift, icon inconsistency, and background crop edges.
Output the PPTX, assets folder, layout JSON, preview, diff overlay, and polish report.
```

## Relationship to bggg-creator-image2ppt

This skill can use `bggg-creator-image2ppt` as the deterministic PPTX compiler. The V6.1 protocol adds a stronger production workflow around it:

- richer element classification
- SVM visual modules
- polish metadata
- reference overlay pass
- two-stage quality scoring
- final visual cleanliness checklist

## Status

This repository contains the skill instructions and protocol reference. It is intended to be used by Codex or another capable agent that can inspect images, generate or extract assets, produce manifest/layout JSON, and build PowerPoint files.