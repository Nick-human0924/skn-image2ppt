---
name: skn-image2ppt
description: High-fidelity hybrid Image2PPT reconstruction with a final Polish Pass. Use when Codex needs to convert PPT screenshots, slide images, posters, infographics, HTML/SVG designs, or Image2 visual drafts into editable PowerPoint files while preserving complex visual assets, rebuilding business-critical text/data as editable PPT objects, generating layout/manifest metadata, preview/diff artifacts, and polishing visible issues such as ghosting, duplicated elements, misalignment, inconsistent icons, border/radius mismatch, and hard-edged background assets.
---

# SKN Image2PPT

Use this skill to rebuild a flat reference image into a visually close, business-editable `.pptx`.

V6.1 combines:

- high-fidelity hybrid reconstruction
- SVM visual modules for complex visuals
- editable PowerPoint text/table/chart overlays for business content
- manifest/layout-driven deterministic PPT generation
- a final Polish Pass against the reference image

Read `references/protocol-v6-1.md` for the full protocol and schemas.

## Workflow

1. Create a project directory and copy the source image into:
   - `original_inputs/`
   - `assets_v6/00_reference/original.png`
2. Analyze the reference image:
   - slide size and aspect ratio
   - major regions
   - complex visual modules
   - text hierarchy
   - cards/containers/dividers
   - logos/icons/background assets
3. Classify elements:
   - visual assets
   - native shapes
   - editable text/table/chart
   - simple charts to rebuild as a whole
   - complex modules to assetize as SVMs
4. Build the editable draft:
   - Preserve complex non-editable visuals as high-fidelity assets.
   - Rebuild business-critical text, numbers, labels, tables, and chart labels as editable PPT objects.
   - Rebuild cards, borders, dividers, badges, and simple containers as native PPT shapes.
   - For simple charts, rebuild the whole chart system instead of mixing image base and overlay lines.
5. Compile the PPTX with a deterministic manifest/layout builder. If `bggg-creator-image2ppt` is installed, use its `image2pptx.py build` script as the compiler.
6. Generate or render a draft preview.
7. Run Polish Pass:
   - remove text ghosting and baked-text residue
   - delete duplicated lines, points, icons, and labels
   - adjust x/y/size/font against the reference image
   - unify radius, border, shadow, font size, and line spacing
   - correct icon style and background asset edges
8. Remove or hide any temporary reference overlay.
9. Deliver final PPTX, assets, layout/manifest JSON, preview, diff overlay, and polish report.

## Directory Contract

Use this structure by default:

```text
project_slug/
  original_inputs/
  assets_v6/
    00_reference/
      original.png
      reference_overlay.png
      page_analysis.json
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

## Key Rules

- Do not use a full-slide screenshot as the final solution unless the user explicitly asks for bitmap fallback.
- Do not make all elements editable if doing so visibly reduces quality.
- Do not leave business-critical text baked into visual assets when it should be editable.
- Do not overlay editable text directly on top of baked text; mask or clean the base first.
- Do not duplicate lines, dots, icons, or labels across the asset layer and PPT layer.
- Do not mix ownership inside simple chart regions; either rebuild the whole chart or keep the whole visual base as an asset and overlay only editable labels.
- Do not use emoji or placeholder glyphs as final icons.
- Do not use hard rectangular crops, white boxes, or rough asset edges.

## Polish Pass Rules

Run Polish Pass after the editable draft preview exists.

1. **Ghosting removal**: if baked text remains under editable text, cover only the residue with a matching mask, then place editable text.
2. **Duplicate removal**: one semantic element appears once; delete duplicate lines, dots, labels, and icons.
3. **Chart ownership**: simple chart regions should be fully rebuilt; complex chart/module regions should be SVM assets plus editable overlays.
4. **Coordinate micro-adjustment**: adjust whole modules first, internal groups second, individual text last.
5. **Business polish consistency**: keep radius restrained, shadows light, borders pale, icons unified, and fonts clear.
6. **Background edge repair**: feather or replace hard-edged image assets; use full clean background assets instead of visible local crop blocks.

## Reference Overlay

For high-fidelity alignment, create a temporary reference overlay:

```text
source image layer
opacity: 30%-50%
locked or marked QA-only
used for alignment
removed or hidden before final delivery
```

Use it to check only high-sensitivity regions:

- title area
- main visual/chart area
- right-side explanation area
- bottom timeline/conclusion area
- logo area
- major background decoration

## Manifest Metadata

Include polish metadata when possible:

```json
{
  "element_id": "segment_1_title",
  "semantic_role": "flywheel segment title",
  "layer": "editable_content",
  "owner": "ppt_text",
  "polish_required": true,
  "polish_type": ["position", "font_size", "alignment"],
  "reference_bbox": {"x": 690, "y": 166, "w": 180, "h": 28},
  "current_bbox": {"x": 696, "y": 170, "w": 184, "h": 30},
  "max_allowed_offset_px": 8,
  "final_action": "adjust_xy"
}
```

## Compatibility With bggg-creator-image2ppt

If the original `bggg-creator-image2ppt` skill is available:

- Use it as the PPTX compiler.
- Store visual assets in the project folder.
- Generate a standard `manifest.json` with `background`, `image`, `text`, `shape`, and `table` elements.
- Keep V6.1 metadata in sidecar files:
  - `layout_v6.json`
  - `asset_metadata.json`
  - `polish_manifest.json`
  - `polish_report.md`

## Delivery Report

In the final response, include:

- final PPTX path
- asset folder or package path
- preview path
- diff overlay path
- layout/manifest path
- polish report path
- editable text count
- visual asset count
- native shape count
- whether the PPTX was reopened/validated
- whether a true PowerPoint/LibreOffice render was available
- known differences from the reference image

Use the scoring thresholds in `references/protocol-v6-1.md`.