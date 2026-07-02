# Image2 to Editable PPT Hybrid Reconstruction Protocol v6.1

## V6 + Polish Pass

Version: v6.1  
Positioning: high-fidelity hybrid reconstruction plus a lightweight final polish pass.  
Goal: move Image2-to-PPT output from a usable 80-85% draft toward a 90%+ business-ready editable deck without making the system unnecessarily complex.

---

## 0. Why V6.1 Exists

V5/V6 solves the main direction:

```text
reference image
-> semantic visual analysis
-> complex visual assets preserved with high fidelity
-> business-critical content rebuilt as editable PPT objects
-> manifest/layout-driven PPT generation
```

Testing shows a recurring gap: once the overall layout is close, the remaining defects are small but visible.

Common defects:

- text ghosting from baked text plus editable overlay text
- duplicated lines, points, icons, or labels
- inconsistent icon style
- card radius, border, and shadow mismatch
- text x/y, font size, and line spacing drift
- hard-edged background assets
- bottom bands, timelines, and labels not cleanly aligned

V6.1 does not try to solve this with a much more complex automatic pipeline. Instead:

```text
85% automated hybrid reconstruction
+
15% standardized Polish Pass
```

---

## 1. Core Principles

### 1.1 Do Not Chase 100% Automation

High-quality business PPT production is usually better handled as:

```text
automated first draft
+
standardized final refinement
```

than:

```text
fully automatic pipeline
+
10x complexity
```

### 1.2 Do Not Make Everything Editable

Must be editable:

- title and subtitle
- business assumptions
- amounts, ratios, metrics
- table data
- chart labels
- explanatory text
- conclusions
- stage names

Usually does not need to be editable:

- background waves
- illustrations
- photos
- science/technology textures
- brand logos
- complex shadows
- decorative light effects

Correct target:

```text
business-critical content editable
+
complex visual assets high fidelity
+
overall visual match close to the source image
```

### 1.5 Image Generation Model Policy

When the workflow needs generated or cleaned visual components, prefer explicit API-level model configuration instead of an opaque built-in image tool.

Recommended model policy as of the 2026-05-15 official documentation check:

| Role | Model | Notes |
| --- | --- | --- |
| Primary asset generation/editing | `gpt-image-2` | Best default for high-fidelity component assets when API access is available. |
| ChatGPT-aligned visual behavior | `chatgpt-image-latest` | Use only when the target runtime exposes it. |
| Transparent asset fallback | `gpt-image-1.5` or alpha post-processing | Use because `gpt-image-2` does not currently support transparent backgrounds. |
| Cost-sensitive decorative assets | `gpt-image-1-mini` | Use for low-risk background or decorative pieces. |
| Legacy fallback | `gpt-image-1` | Use when 1.5 is unavailable. |
| Codex built-in image tool | `unknown_builtin_imagegen` | Use only as fallback because the backend model is not selectable or reported. |

As of the 2026-05-15 official documentation check, OpenAI image generation docs list `gpt-image-2`. Use it as the primary model when available, and record the selected model in `image_model_config.json` and the conversion report.

For transparent assets, prefer API transparency when supported. `gpt-image-2` does not currently support transparent backgrounds, so use a transparency-capable fallback or generate against a controlled background and post-process alpha/background removal. Record this choice in `asset_metadata.json`.

### 1.3 Rebuild Simple Charts as a Whole

For simple charts:

- donut charts
- pie charts
- bar charts
- line charts
- simple timelines
- simple process diagrams
- simple funnels

Prefer:

```text
PPT shapes / SVG / native chart rebuild
```

Do not mix:

```text
chart body from image
+
PPT connector lines
+
PPT points
+
editable labels
```

Mixed ownership creates offsets, duplicated lines, and visual dirt.

### 1.4 Use Overlay Carefully

Overlay is appropriate only when:

- the background is clean
- there is no baked text below
- the overlay area has a stable single color
- text coordinates are easy to align

Rule:

```text
base image has text -> do not directly overlay duplicate text
base image has lines -> do not draw duplicate lines
base image has icons -> do not overlay duplicate icons
```

If overlay is required, first cover the base disturbance with a matching light mask.

---

## 2. V6.1 Workflow

```text
Step 1  Analyze reference image
Step 2  Classify elements by editability and fidelity
Step 3  Preserve or rebuild complex visual assets
Step 4  Rebuild business content as editable PPT objects
Step 5  Generate editable PPT draft through manifest/layout compiler
Step 6  Export or generate preview
Step 7  Polish Pass against the reference image
Step 8  Remove or hide reference layers
Step 9  Deliver final PPTX and reports
```

---

## 3. Layer Model

| Layer | Name | Contents | Treatment |
| --- | --- | --- | --- |
| 0 | Background | page fill, gradients, light blobs | PPT gradient/shape or clean background image |
| 1 | Visual assets | waves, texture, shadows, decorative graphics | transparent PNG/SVG |
| 1.5 | SVM | flywheel, funnel, map, mechanism diagram, dashboard base | high-fidelity visual base + editable overlays |
| 2 | Structure | cards, dividers, section bars, simple arrows | native PPT shapes |
| 3 | Editable content | titles, labels, bullets, numbers, tables, chart labels | native PPT text/table/chart |
| 4 | Foreground emphasis | badges, callouts, highlights | PPT shapes/text or small assets |
| 5 | QA | reference overlay, guides, diff notes | hidden or removed before final |

---

## 4. SVM: Semantic Visual Module

Use SVMs for complex visuals whose geometry, gradients, masks, and overlaps are expensive to rebuild as primitive PPT shapes.

Examples:

- flywheel
- funnel
- map
- complex timeline
- scientific mechanism diagram
- dashboard visual base

SVM structure:

```json
{
  "module_type": "SVM_FLYWHEEL",
  "visual_base": "assets_v6/03_svm/flywheel_001/flywheel_visual_base.png",
  "visual_base_locked": true,
  "generation_model": "gpt-image-2",
  "generation_backend": "openai_images_api",
  "editable_overlays": [
    "center_title",
    "segment_titles",
    "segment_bullets",
    "number_badges"
  ],
  "alignment_anchors": ["center", "top", "right", "bottom", "left"],
  "fidelity_priority": "high",
  "editability_priority": "content_only"
}
```

SVM rule:

> The complex visual base can be a locked asset, but business text inside or around it should be rebuilt as editable text whenever possible.

---

## 5. Element Decision Table

| Element Type | Recommended Treatment | Polish Pass |
| --- | --- | --- |
| Main title | PPT text | yes, calibrate font size and position |
| Subtitle | PPT text | yes |
| Number badge | PPT shape + text | yes |
| Logo | high-fidelity image/SVG | yes, calibrate size and position |
| Background gradient | PPT gradient or full clean background | only if color drift is visible |
| Bottom wave | transparent PNG/SVG | yes, position and edge quality |
| Illustration/photo | transparent PNG/image asset | yes, opacity and position |
| Donut/pie/bar/line chart | SVG/PPT/native chart | yes, proportion and line weight |
| Complex flywheel/map/MoA | SVM visual base + overlay | yes |
| Explanatory text | PPT text | yes, wrapping and position |
| Table | PPT table | yes |
| Bottom conclusion band | PPT shape + text | yes |
| Decorative icons | SVG/PNG | yes, unify style |

---

## 6. Polish Pass

Polish Pass is the lightweight refinement round after the editable PPT draft is generated.

It should fix only first-glance visual defects:

1. remove ghosting and baked-text residue
2. delete duplicated semantic elements
3. adjust alignment and coordinates
4. unify radius, border, and shadow
5. unify fonts, font sizes, and line spacing
6. calibrate icon and background asset positions

Do not use a full-slide screenshot to hide defects.

### 6.1 Reference Overlay Method

Temporarily add the source image into the draft:

```text
reference image as bottom or top layer
opacity: 30%-50%
locked or clearly marked as QA-only
adjust slide elements against the reference
hide or delete reference layer before final delivery
```

This is the same idea as using a transparent reference layer in Figma or Photoshop.

### 6.2 Polish Only Sensitive Regions

Focus on:

- title area
- main chart/module area
- right-side explanation area
- bottom conclusion/timeline area
- logo area
- main background waves/decorations

Ignore tiny differences that do not affect business perception.

### 6.3 Editability Floor

Allowed to image-asset:

- background
- complex decoration
- logo
- illustration/photo
- complex visual base

Not allowed to image-asset in the final PPT:

- core title
- core numbers
- explanatory text
- table data
- chart labels
- conclusions

---

## 7. Six Polish Rules

### Rule 1: Ghosting Removal

If editable overlay text sits on top of baked source text:

1. Decide whether the text must be editable.
2. If yes, cover the baked text with a matching mask.
3. Place editable text on top.
4. Keep the mask tight and background-matched.

Common mask colors:

```text
white card: #FFFFFF
light blue page: #F7FBFF / #F3F8FF
card area: same as card fill
border: none
opacity: 0%-5%
```

### Rule 2: Duplicate Element Removal

One semantic element should appear once.

Examples:

- same percentage
- same label
- same connector line
- same dot
- same conclusion sentence

If duplicated:

```text
simple chart -> rebuild the chart system and remove underlying chart residue
complex SVM -> keep visual base and remove duplicate overlays
```

### Rule 3: Chart Ownership

Chart regions must be treated as one ownership set.

Wrong:

```text
chart body from image
connector line from PPT
dot from PPT
label from PPT
original connector still visible
```

Correct:

```text
Option A: whole chart body + connector + dots as visual asset; only text overlays editable
Option B: chart body + connector + dots + labels rebuilt as PPT/SVG/native chart
```

Default:

```text
simple data chart -> Option B
complex visual module -> Option A or SVM
```

### Rule 4: Coordinate Micro-Adjustment

If visibly offset against the reference overlay, adjust:

- `x`
- `y`
- `width`
- `height`
- font size
- line spacing
- anchor point

Offset thresholds:

```text
title offset > 8 px
chart/module offset > 10 px
explanatory text offset > 8 px
bottom band offset > 10 px
```

Adjustment order:

```text
module group position
-> internal module elements
-> individual text
```

Do not micro-adjust every text box independently if a group shift solves the mismatch.

### Rule 5: Business Polish Consistency

If the slide looks like a web dashboard rather than a business BP, check:

- radius too large
- shadow too heavy
- border too dark or hard
- icon looks like emoji
- colors too bright
- font too heavy

Recommended values:

```text
normal card radius: 10-16 px
large card radius: 16-22 px
table/container radius: 10-16 px
shadow: low opacity, small offset, light blur
border: light blue-gray, not dark hard lines
icon: unified SVG/source asset, no emoji
```

### Rule 6: Background Asset Edge Repair

If a background asset has a hard rectangular edge:

1. Check whether it is a rectangular crop.
2. Replace with transparent PNG/SVG if possible.
3. Feather/antialias the edge.
4. If transparency cannot be cleanly produced, use a full clean background asset rather than local hard crops.

Watch especially:

- bottom waves
- illustrations
- photos
- light effects
- semi-transparent textures

---

## 8. Manifest Additions

Add polish-aware metadata to layout/manifest elements.

Editable text example:

```json
{
  "element_id": "label_45_percent",
  "semantic_role": "investment_percentage_label",
  "layer": "editable_content",
  "owner": "ppt_text",
  "polish_required": true,
  "polish_type": ["position", "font_size", "alignment"],
  "reference_bbox": {"x": 910, "y": 210, "w": 88, "h": 52},
  "current_bbox": {"x": 916, "y": 214, "w": 92, "h": 54},
  "max_allowed_offset_px": 8,
  "final_action": "adjust_xy"
}
```

Asset example:

```json
{
  "element_id": "wave_bottom",
  "semantic_role": "bottom_wave_decoration",
  "layer": "visual_asset",
  "owner": "asset",
  "polish_required": true,
  "polish_type": ["position", "edge_quality"],
  "asset_quality": {
    "transparent": true,
    "hard_edge": false,
    "white_box": false
  },
  "final_action": "lock_background"
}
```

---

## 9. Directory Contract

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
      image_model_config.json
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

---

## 10. Quality Scoring

Use two stages.

### Stage 1: Draft Score

| Dimension | Weight |
| --- | ---: |
| Layout similarity | 20 |
| Visual fidelity | 20 |
| Business editability | 25 |
| Asset quality | 15 |
| Business polish | 10 |
| Reusability | 10 |

### Stage 2: After Polish Pass

| Dimension | Weight |
| --- | ---: |
| First-glance similarity | 30 |
| Detail cleanliness | 25 |
| Content editability | 25 |
| Business polish | 10 |
| Maintainability | 10 |

Thresholds:

```text
>= 92: production-ready editable draft
88-91: usable, minor fixes only
82-87: correct direction, needs another Polish Pass
< 82: return to reconstruction stage
```

---

## 11. Final Checklist

### Editability

- [ ] Main title editable
- [ ] Subtitle editable
- [ ] Core numbers editable
- [ ] Explanatory text editable
- [ ] Table data editable
- [ ] Chart labels editable
- [ ] Conclusion copy editable

### Visual Cleanliness

- [ ] No text ghosting
- [ ] No duplicate lines
- [ ] No duplicate dots
- [ ] No baked text plus new overlay text
- [ ] No white-box image assets
- [ ] No hard crop edges

### Layout Similarity

- [ ] Title position close to source
- [ ] Main module/chart position close to source
- [ ] Right explanation area close to source
- [ ] Bottom conclusion/timeline close to source
- [ ] Logo size and position close to source
- [ ] Background wave/decor position close to source

### Business Polish

- [ ] Radius restrained
- [ ] Shadow light
- [ ] Border light
- [ ] Icons unified
- [ ] Font clear
- [ ] No emoji
- [ ] No obvious web-dashboard feel

---

## 12. Generic Prompt

```text
You are an Image2-to-Editable-PPT hybrid reconstruction agent with a final Polish Pass.

Your job is not to paste the full image into PPT, and not to redraw every pixel as editable shapes. Your job is to create a visually close, business-editable PPT.

Follow this workflow:

1. Analyze the reference image.
2. Classify elements into visual assets, native shapes, editable text/table/chart, simple charts to rebuild, and complex modules to assetize or turn into SVMs.
3. Preserve complex non-editable visuals as high-fidelity assets.
4. Rebuild business-critical text, numbers, tables, and labels as native PPT objects.
5. When generating or cleaning image assets, prefer explicit OpenAI Images API configuration with `gpt-image-2`; for transparent assets, use a transparency-capable fallback or post-process alpha. If only Codex built-in imagegen is available, record the model identity as unknown.
6. For simple data charts, rebuild the full chart system instead of mixing image base and overlay lines.
7. Generate the editable PPT draft.
8. Render a preview.
9. Add a Polish Pass:
   - remove text ghosting
   - delete duplicated lines/points/text
   - adjust x/y/size/font against the reference image
   - unify radius, shadow, border, icons
   - correct background asset edges
10. Do not solve small visual issues by inserting a full-slide screenshot.
11. Final PPT must preserve editability of business-critical content.

Final outputs:
- editable_pptx
- preview_png
- assets_folder
- layout_or_manifest_json
- polish_report_md
```

---

## 13. One-Sentence Principle

```text
V6 builds the editable high-fidelity draft; Polish Pass removes the visible dirt.
```

In Chinese:

```text
V6 负责把图变成可编辑 PPT 初稿，Polish Pass 负责把一眼能看出来的细节瑕疵清掉。
```
