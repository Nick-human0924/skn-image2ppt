---
name: skn-image2ppt
description: V6.4 topology-faithful Premium Visual Asset + Editable Semantic Overlay Image2PPT conversion. Use when Codex needs to convert PPT screenshots, slide images, posters, infographics, HTML/SVG designs, or Image2 visual drafts into editable PowerPoint while preserving the reference page's main visual structure. This skill avoids full-slide screenshots, large raw crops with baked business text, low-quality all-vector redraws, and theme-only regenerated assets. It rebuilds business text, tables, labels, arrows, numbers, charts, insight cards, and conclusion bars as editable PPT objects, while preserving or generating high-quality text-free visual assets for scientific/medical illustrations, mechanism diagrams, evidence pyramids, dosing workflows, liposomes, cells, drug-delivery scenes, 3D objects, dashboards, flywheels, glows, gradients, and micro-texture.
---

# SKN Image2PPT

Use this skill to rebuild a flat reference image into a visually close, business-editable `.pptx`.

Default to **V6.4 / Topology-Faithful Premium Visual Asset + Editable Semantic Overlay** for every new task. V6.4 keeps the V6.3 visual-asset approach and adds a stronger rule: do not replace the reference page's main structure with a merely similar theme.

## Core Principle

```text
No full-slide screenshot.
No large raw crop with baked business text.
No low-quality vector simplification of premium scientific visuals.

High-quality text-free visual asset layer
+ editable PPT semantic layer
+ native PPT simple structure layer
+ topology lock + visual element ledger
= business-editable, visually premium reconstruction.
```

Use Image2 / image generation / image cleanup for **visual assets only**, not for complete PPT pages. Codex builds the editable information layer in PowerPoint.

## When To Read References

- Read `references/protocol-v6-4.md` for the current protocol, topology lock, visual element ledger, asset schemas, QA gates, and prompt templates.
- Read `references/protocol-v6-3.md` only when maintaining older V6.3 projects.
- Read `references/protocol-v6-2.md` only when maintaining older V6.2 projects.
- Use `image_model_config.example.json` when the runtime supports API-level image generation.

## V6.4 Workflow

1. Create the project directory and copy source images into:
   - `original_inputs/`
   - `assets_v6/00_reference/`
2. Analyze each reference slide:
   - visual hierarchy and first-read object
   - page topology, such as radial network, two-panel mechanism, evidence pyramid, dosing workflow, matrix, flywheel, dashboard, or table
   - premium visual modules
   - every non-text visual element, including small icons, vials, bags, molecules, pumps, brackets, guide lines, arrows, connectors, shadows, and glows
   - editable semantic content
   - tables/charts/processes
   - template and brand chrome
3. Build `topology_lock.json` and `visual_element_ledger.json` before generating slides:
   - lock the reference slide's main structure and allowed deviation level
   - map every non-text visual element to `native_shape`, `text_free_asset`, `icon`, `template`, or `intentionally_omitted`
   - fail QA if a core structure is changed or a required visual element is missing without a recorded reason
4. Build `visual_asset_plan.json` before generating slides:
   - list every high-quality text-free visual asset needed
   - define each asset's target bounding box and aspect ratio
   - classify the asset as scientific illustration, dashboard/flywheel base, glow/texture, atomic object, or clean background
   - write reverse prompts that include required sub-elements, relative placement, empty overlay zones, and target background
5. Generate or clean visual assets:
   - assets must contain **no text, no labels, no arrows, no numbers, no tables, no legends, no logo, no watermark**
   - assets must match the reference structure, not only the reference topic
   - preserve 3D depth, glow, gradient, micro-texture, medical illustration quality, and composition
   - reject assets that contain text-like marks or low-quality simplified geometry
6. Run Background Integration Pass:
   - isolated objects such as liposomes/vials must use transparent or alpha-matted backgrounds
   - scene assets should either fill the whole visual panel or have feathered edges
   - asset background color must match the PPT/card/template background
   - record the target PPT/card background color and the selected treatment (`transparent_matte`, `same_color_fill`, `full_panel`, or `edge_feather`)
   - inspect assets at final slide size; faint gray rectangles and mismatched color temperature still fail even if the edge is soft
   - do not leave hard rectangular white, gray, or blue asset edges unless the rectangle is an intentional framed panel
7. Build the editable PPT:
   - place visual assets as locked/image base components
   - overlay all titles, labels, numbers, arrows, tables, bullets, legends, insight cards, and conclusions as editable PPT objects
   - rebuild simple cards, borders, table grids, badges, and connectors as native PPT shapes
8. Run Topology + Hierarchy Pass:
   - compare each reconstructed page with `topology_lock.json`
   - keep radial nodes radial, pyramids pyramidal, workflows procedural, and two-panel mechanisms two-panel unless the user requests redesign
   - preserve guide-line direction, connector count, major object placement, and reference reading path
   - preserve reference first-read dominance
   - do not shrink premium visuals into small cards
   - avoid overly regular internal-training style layouts when the reference has a high-end consulting/medical-conference look
9. Run Premium Polish Pass:
   - remove ghosted text and duplicate semantics
   - tune spacing, line weights, shadows, radius, numbering, icon style, and text rhythm
   - ensure visual assets retain premium depth and are not distorted or hard-edged
10. Render all slides and inspect:
   - visual asset quality
   - overlay alignment
   - text overflow/clipping
   - editability of all business content
11. Deliver PPTX plus sidecar artifacts:
   - `topology_lock.json`
   - `visual_element_ledger.json`
   - `visual_asset_plan.json`
   - `visual_asset_prompts.json`
   - `overlay_plan.json`
   - `module_ownership.json`
   - `visual_hierarchy.json`
   - `icon_system.json`
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

Fail V6.4 QA if any is true:

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
- visual asset count
- native shape count
- whether the PPTX reopened/validated
- known differences from the reference image

## One-Sentence Principle

```text
V6.4 preserves reference topology, uses Image2 for premium text-free visual assets, and uses Codex for editable PPT semantics.
```
