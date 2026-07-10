---
name: skn-image2ppt
description: V6.5 topology-faithful, engineering-guarded Image2PPT conversion. Use when Codex needs to convert PPT screenshots, slide images, posters, infographics, HTML/SVG designs, or Image2 visual drafts into editable PowerPoint while preserving the reference page's main visual structure, icon fidelity, text scale, and placement accuracy. This skill avoids full-slide screenshots, large raw crops with baked business text, low-quality all-vector redraws, theme-only regenerated assets, broken or uncopyable icons, tiny text boxes, and coordinate drift. It rebuilds business text, tables, labels, arrows, numbers, charts, insight cards, and conclusion bars as editable PPT objects, while preserving or generating high-quality text-free visual assets and requiring RUN_ROOT isolation, source_bbox coordinate contracts, icon extraction QA, placement overlays, visual diff, and frame-anchor calibration.
---

# SKN Image2PPT

Use this skill to rebuild a flat reference image into a visually close, business-editable `.pptx`.

Default to **V6.5 / Topology-Faithful Premium Visual Asset + Engineering QA** for every new task. V6.5 keeps the V6.4 topology lock, then adds an engineering pass for the failure modes seen in practice: uncopyable icons, text that renders too small, and layout drift.

## Core Principle

```text
No full-slide screenshot.
No large raw crop with baked business text.
No low-quality vector simplification of premium scientific visuals.

RUN_ROOT task isolation
+ source_bbox coordinate contract
+ high-quality text-free visual asset layer
+ editable PPT semantic layer
+ native PPT simple structure layer
+ topology lock + visual element ledger
+ icon extraction QA + placement overlay + visual diff
= business-editable, visually closer reconstruction.
```

Use Image2 / image generation / image cleanup for **visual assets only**, not for complete PPT pages. Codex builds the editable information layer in PowerPoint.

## When To Read References

- Read `references/protocol-v6-5.md` for the current protocol, engineering QA pass, coordinate contract, icon pipeline, QA gates, and prompt templates.
- Read `references/protocol-v6-4.md` only when maintaining older V6.4 projects.
- Read `references/protocol-v6-3.md` only when maintaining older V6.3 projects.
- Read `references/protocol-v6-2.md` only when maintaining older V6.2 projects.
- Use `image_model_config.example.json` when the runtime supports API-level image generation.
- Use `scripts/` utilities when available:
  - `probe_palette.py` for safe chroma-key color selection.
  - `chroma_key.py` for color-preserving transparent asset cleanup.
  - `slice_grid.py` for icon/contact-sheet extraction from generated icon sheets.
  - `layout_guard.py` for source_bbox/fraction/font-size contract checks.
  - `placement_qa.py` for source/preview bbox overlays.
  - `visual_compare_qa.py` for side-by-side, blend, and diff heatmap QA.
  - `pptx_editability_lint.py` for PPTX ZIP/XML, shrink-to-fit, and tiny-font checks.

## V6.5 Workflow

1. Create a unique task directory:
   - `image2pptx_runs/<timestamp>_<slug>/`
   - store all source images, assets, prompts, layout files, previews, QA images, and outputs inside it
   - do not read from or write to fixed historical folders unless the user explicitly requests reuse
2. Copy source images into:
   - `original_inputs/`
   - `assets_v6/00_reference/`
3. Analyze each reference slide:
   - visual hierarchy and first-read object
   - page topology, such as radial network, two-panel mechanism, evidence pyramid, dosing workflow, matrix, flywheel, dashboard, or table
   - premium visual modules
   - every non-text visual element, including small icons, vials, bags, molecules, pumps, brackets, guide lines, arrows, connectors, shadows, and glows
   - editable semantic content
   - tables/charts/processes
   - template and brand chrome
4. Build `topology_lock.json` and `visual_element_ledger.json` before generating slides:
   - lock the reference slide's main structure and allowed deviation level
   - map every non-text visual element to `native_shape`, `text_free_asset`, `icon`, `template`, or `intentionally_omitted`
   - fail QA if a core structure is changed or a required visual element is missing without a recorded reason
5. Build `visual_asset_plan.json` and `icon_extraction_plan.json` before generating slides:
   - list every high-quality text-free visual asset needed
   - define each asset's target bounding box and aspect ratio
   - classify the asset as scientific illustration, dashboard/flywheel base, glow/texture, atomic object, or clean background
   - write reverse prompts that include required sub-elements, relative placement, empty overlay zones, and target background
   - list every icon, art-word, decorative mark, tiny symbol, badge, and meaningful line icon that must be independently movable or copyable
6. Generate or clean visual assets:
   - assets must contain **no text, no labels, no arrows, no numbers, no tables, no legends, no logo, no watermark**
   - assets must match the reference structure, not only the reference topic
   - preserve 3D depth, glow, gradient, micro-texture, medical illustration quality, and composition
   - reject assets that contain text-like marks or low-quality simplified geometry
7. Run Icon Extraction Pass:
   - use supplied icons/SVGs when available
   - otherwise generate or clean text-free transparent PNG icon assets
   - record every icon in `icon_extraction_plan.json` with `source_bbox`, final file, and placement status
   - if using an icon sheet, run chroma-key cleanup, slice to components, and inspect the contact sheet
   - fail QA if an icon is missing, clipped, merged with another icon, too small, duplicated, or not independently selectable/copyable
8. Run Background Integration Pass:
   - isolated objects such as liposomes/vials must use transparent or alpha-matted backgrounds
   - scene assets should either fill the whole visual panel or have feathered edges
   - asset background color must match the PPT/card/template background
   - record the target PPT/card background color and the selected treatment (`transparent_matte`, `same_color_fill`, `full_panel`, or `edge_feather`)
   - inspect assets at final slide size; faint gray rectangles and mismatched color temperature still fail even if the edge is soft
   - do not leave hard rectangular white, gray, or blue asset edges unless the rectangle is an intentional framed panel
9. Build the editable PPT:
   - place visual assets as locked/image base components
   - overlay all titles, labels, numbers, arrows, tables, bullets, legends, insight cards, and conclusions as editable PPT objects
   - rebuild simple cards, borders, table grids, badges, and connectors as native PPT shapes
   - for every text/icon/asset, store `source_bbox` in source-image pixels and `x/y/w/h` in fraction coordinates
   - calculate text size from source pixel height: `pt = source_text_height_px * slide_height_in * 72 / ref_height`
10. Run Topology + Hierarchy Pass:
   - compare each reconstructed page with `topology_lock.json`
   - keep radial nodes radial, pyramids pyramidal, workflows procedural, and two-panel mechanisms two-panel unless the user requests redesign
   - preserve guide-line direction, connector count, major object placement, and reference reading path
   - preserve reference first-read dominance
   - do not shrink premium visuals into small cards
   - avoid overly regular internal-training style layouts when the reference has a high-end consulting/medical-conference look
11. Run Engineering QA Pass:
   - run coordinate/font checks before rendering
   - render preview and generate source/preview placement overlays
   - generate side-by-side, blend, and diff heatmap QA images
   - lint the PPTX package for ZIP/XML validity, `normAutofit`, and unexpectedly small explicit font runs
   - correct text scale before correcting text position
   - correct icon size/center before correcting surrounding text
   - run frame-anchor calibration for text attached to generated or image-based frames
12. Run Premium Polish Pass:
   - remove ghosted text and duplicate semantics
   - tune spacing, line weights, shadows, radius, numbering, icon style, and text rhythm
   - ensure visual assets retain premium depth and are not distorted or hard-edged
13. Render all slides and inspect:
   - visual asset quality
   - overlay alignment
   - text overflow/clipping
   - editability of all business content
14. Deliver PPTX plus sidecar artifacts:
   - `run_manifest.json`
   - `topology_lock.json`
   - `visual_element_ledger.json`
   - `visual_asset_plan.json`
   - `icon_extraction_plan.json`
   - `visual_asset_prompts.json`
   - `overlay_plan.json`
   - `module_ownership.json`
   - `visual_hierarchy.json`
   - `icon_system.json`
   - `engineering_qa_report.json`
   - `premium_visual_qa.json`
   - `manifest.json`
   - `polish_report.md`

## Ownership Rules

### High-Quality Visual Asset Layer

Use image assets, not PPT primitive redraws, for:

- liposome cutaways, lipid bilayers, encapsulated drug particles
- tumor tissue, cells, microenvironment, vascular delivery scenes
- molecular/cellular backgrounds and medical mechanism art
- evidence pyramids, 3D stair models, premium process bases, and complex workflow diagrams when gradients/depth/glow carry the design quality
- 3D scientific objects, depth-of-field particle fields, soft glows, micro-textures
- premium dashboards, value orbits, flywheels, and closed-loop bases where glow/gradient/depth carries the design quality
- product vials, photos, portraits, logos, and supplied bitmap identity assets

These assets must be complete, clean, high-resolution, and text-free.

### Editable Semantic Layer

Always rebuild as editable PPT objects:

- page titles and subtitles
- product names, claims, bullets, labels, legends
- numeric values, percentages, units, dates
- arrows, connector labels, numbered badges
- tables, chart labels, axis labels, matrix cells
- insight cards, callouts, conclusion bars, source notes

Do not bake business claims, numbers, arrows, or labels into generated images.

### Native Structure Layer

Use PPT shapes for:

- card containers and borders
- table grids and dividers
- simple badges, pills, ribbons, arrows, and callout frames
- simple line icons when they are not the main visual quality carrier

Do not use native shapes to approximate complex scientific art when that would visibly lower the page quality.

## Hard Rules

- Do not generate a complete slide image and then split it into PPT pieces.
- Do not change the reference page topology, such as replacing a radial product network with product cards, a mechanism figure with an unrelated theme image, a 3D pyramid with flat bars, or a dosing workflow with missing process visuals.
- Do not crop a large reference module if it contains baked text, arrows, numbers, table data, borders, labels, or layout furniture.
- Do not replace high-end scientific illustrations with simplified vector circles, lines, and icons.
- Do not stretch liposomes, cells, tissue scenes, flywheels, dashboards, vials, or 3D visuals non-uniformly.
- Do not paste assets with mismatched backgrounds or visible hard rectangular edges.
- Do not accept a generated visual asset only because it is text-free; it must also blend with the actual PPT background or card fill at final placement size.
- Do not overlay editable text directly on baked source text. Clean or regenerate the base first.
- Do not leave chart/table values baked into images.
- Do not use emoji or placeholder glyphs as final icons.
- Do not omit small but meaningful visual elements such as infusion bags, molecule structures, pumps, brackets, guide lines, node rings, evidence icons, or arrow systems.
- Do not let icons remain baked into a large screenshot when the user expects them to be independently movable/copyable.
- Do not place text using thumbnail coordinates; convert all measured boxes back to source-image pixels first.
- Do not accept text that is visibly smaller than the reference. Fix font size using the source-pixel-height formula before moving boxes.
- Do not deliver without at least one preview-to-reference placement QA pass for pages with dense icons or labels.
- Do not deliver a PPTX that requires PowerPoint repair or relies on unexpected shrink-to-fit for normal body text.
- If a visual base cannot be generated cleanly, explicitly mark the fallback in the reports.

## Prompt Contract For Visual Assets

Every premium asset prompt must include:

```text
Create a high-end text-free medical consulting PowerPoint visual asset.
Subject: ...
Composition: ...
Style: premium medical conference / pharmaceutical consulting, 3D or 2.5D, soft depth, glow, gradient, micro-texture, clean white or pale-blue background.
Topology requirements: include the required sub-elements and relative placement from the reference image; preserve the reference reading path and blank overlay zones.
Constraints: no text, no Chinese characters, no labels, no arrows, no numbers, no table, no legend, no logo, no watermark, no UI.
Usability: leave clean blank zones for editable PPT overlays; complete uncropped object; no hard rectangular crop edge; high resolution.
Aspect ratio: ...
```

Store prompt, reverse analysis, backend/model identity, source reference, output path, and overlay plan in `visual_asset_prompts.json`.

## Mandatory Asset Examples

For pharmaceutical comparison decks, generate or clean assets like:

- P1 center 3D liposome sphere with no product text
- P1 radial four-product node network structure: circles, guide lines, central liposome, and bottom flow arrows must stay structurally faithful
- P2 ordinary irinotecan dispersion scene, no labels
- P2 liposome tumor enrichment / delivery scene, no labels
- P4 evidence hierarchy pyramid base, no labels or numbers
- P7 dosing workflow visuals: infusion bag, liposome, molecule, pump, repeat bracket, no baked business text
- P5 TEA8SOS liposome cutaway, no labels
- P5 liposome II cutaway, no labels
- P8 four-dimensional hospital value dashboard base, no text
- P9 three-value closed-loop / flywheel base, no text

Then overlay all semantics in PPT.

## QA Gates

Fail V6.5 QA if any is true:

- a full slide is a screenshot
- a large module is a raw crop with baked business content
- a complex scientific visual is redrawn as visibly simplified PPT vectors
- a premium dashboard/flywheel loses glow, gradient, micro-texture, or 3D depth and looks like internal training material
- the main reference topology is changed without user approval
- `visual_element_ledger.json` is missing or leaves required visual elements unmapped
- a generated asset is theme-similar but structurally different from the reference
- a visual asset contains text-like marks, labels, arrows, numbers, legends, tables, logos, or watermarks
- a visual asset has a visible background mismatch or hard rectangular edge against the PPT page/card
- editable business text is missing for titles, labels, tables, chart labels, source notes, or conclusion bars
- scientific visuals are cropped, distorted, or non-uniformly scaled
- first-read hierarchy is weaker than the reference

## Delivery Report

In the final response, include:

- final PPTX path
- asset folder/package path
- preview path
- diff/QA path
- prompt/asset plan path
- polish report path
- editable text count
- source_bbox coverage count
- visual asset count
- independently movable/copyable icon count
- native shape count
- whether the PPTX reopened/validated
- whether coordinate/font guard passed
- whether PPTX editability/package lint passed
- whether placement overlay and visual diff were generated
- known differences from the reference image

## One-Sentence Principle

```text
V6.5 preserves topology, then uses engineering QA to keep icons copyable, text at source scale, and layout aligned.
```

Chinese:

```text
V6.5 不只是规定怎么重建，还要用坐标守卫、图标切片、摆放标注和视觉 diff 把“更像原图”落到可检查流程里。
```
