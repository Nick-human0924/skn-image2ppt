# Image2 to Editable PPT Reconstruction Protocol v6.2

Version: v6.2  
Positioning: reconstruction-first Image2PPT with asset guardrails, hierarchy pass, generative visual-base reconstruction, and Polish Pass.  
Goal: prevent raw-crop pseudo-reconstruction and produce a closer, more premium, business-editable PPTX.

## Table Of Contents

1. Upgrade From V6.1
2. Core Principle
3. Layer And Ownership Model
4. Large-Module Guardrails
5. SVM Modes
6. Generative Visual-Base Reconstruction
7. Page Hierarchy Pass
8. Proportional Fidelity Rules
9. Icon And Numbering System
10. Premium Polish Rules
11. Manifest Requirements
12. QA Gates
13. Final Checklist
14. Prompt Templates

---

## 1. Upgrade From V6.1

V6.1 allowed complex modules to become SVM assets. In practice, agents may overuse cropped reference regions as large assets, which causes:

- cropped or incomplete diagrams;
- baked text under editable overlays;
- distorted scientific visuals after resizing;
- weak hierarchy because large visual focus areas are shrunk into cards;
- overly regular but low-premium page layouts;
- inconsistent numbered badges and icon systems.

V6.2 changes the default:

```text
large page module -> reconstruct structurally
atomic visual object -> assetize
scientific visual base -> clean/regenerate text-free, then overlay editable content
```

Raw cropping is no longer a normal SVM solution.

---

## 2. Core Principle

The final slide should look like a rebuilt PPT page, not a collage of cropped screenshots.

```text
reference image
-> detect hierarchy and module ownership
-> rebuild structure as PPT objects
-> regenerate/clean only visual bases that should not be editable
-> overlay editable business content
-> render, compare, polish
```

Editability floor:

- editable: titles, subtitles, bullets, evidence labels, numbers, table cells, chart labels, legends, insight text, conclusion bars, source notes;
- native shape: cards, dividers, ribbons, arrows, table grids, process steps, badges, callout frames;
- image asset: logo, product vial, molecule/cell/liposome illustration, clean background, decorative texture;
- generative base: scientific visual texture or mechanism art with no text/labels/arrows.

---

## 3. Layer And Ownership Model

| Layer | Name | Contents | V6.2 Treatment |
| --- | --- | --- | --- |
| 0 | Template/background | brand chrome, background waves, slide theme | preserve or rebuild cleanly |
| 1 | Atomic visuals | logos, vials, portraits, single liposome/cell/molecule | image/SVG asset |
| 1.5 | Visual base | text-free scientific/mechanism art | clean/regenerate, locked |
| 2 | Structure | cards, grids, dividers, arrows, panels, table lines | native PPT shapes |
| 3 | Editable content | text, labels, numbers, table cells, legends | native PPT text/table/chart |
| 4 | Emphasis | highlight pills, numbered badges, seals, callouts | native shapes + text |
| 5 | QA | reference overlay, guides, diff notes | hidden/deleted before delivery |

No module may mix ownership silently. Each module needs one of:

- `native_module`
- `clean_visual_base_plus_editable_overlay`
- `atomic_asset`
- `raw_crop_fallback` with explicit failure note

---

## 4. Large-Module Guardrails

### 4.1 Raw Crop Ban

Do not use a raw crop as a final asset when any condition is true:

- the crop is larger than 12-15% of the slide canvas;
- it contains more than one semantic object group;
- it contains business text, numbers, labels, arrows, legends, or table data;
- it contains card borders, table lines, chart axes, process connectors, or numbered rows;
- it is a dominant first-read or second-read visual area;
- it must be resized non-uniformly to fit the target page.

### 4.2 Must-Rebuild Modules

Always rebuild these structurally:

- comparison card strips;
- tables and matrices;
- evidence ladders;
- process flows;
- timeline bands;
- insight cards;
- safety cards;
- bottom conclusion bars;
- numbered key point lists;
- simple chart systems.

### 4.3 Asset-Allowed Objects

These may remain images:

- logo or official mark supplied by source/template;
- vial/product/photo/portrait;
- individual liposome/cell/molecule illustration with no baked labels;
- decorative molecular texture;
- text-free mechanism background;
- generated text-free visual base.

### 4.4 Degradation Order

If time or tool limitations make full reconstruction hard, degrade in this order:

1. rebuild structure and editable content natively;
2. use generated/clean visual base with editable overlays;
3. use small atomic crops inside rebuilt frames;
4. use raw crop fallback only when the user explicitly accepts it or the report marks `V6.2_FAIL_RAW_CROP_FALLBACK`.

---

## 5. SVM Modes

### SVM_NATIVE

Use for large structured modules that are visually complex but composed of cards, arrows, lines, badges, and text.

Examples:

- evidence ladder;
- value flywheel with text;
- table/matrix;
- dosing process;
- safety checklist.

Treatment:

- rebuild geometry with native PPT shapes;
- rebuild text, numbers, and labels as editable objects;
- use icons from a unified library or generated SVG set.

### SVM_CLEAN_BASE_PLUS_OVERLAY

Use for scientific visuals where organic geometry is hard to draw but the business layer must be editable.

Examples:

- tumor cell cluster;
- liposome release mechanism;
- vascular/tissue background;
- molecular shell or particle field.

Treatment:

- create a clean text-free base image;
- overlay all arrows, labels, badges, numbers, and explanatory text as editable PPT objects;
- avoid direct overlay over baked text.

### SVM_ATOMIC_ASSET

Use for single objects only.

Examples:

- one vial;
- one logo;
- one standalone liposome;
- one doctor/person illustration.

Treatment:

- preserve as high-fidelity image/SVG;
- do not include surrounding cards, captions, borders, or bullets inside the crop.

### SVM_GENERATIVE_BASE

Use when the reference scientific visual is too cropped, text-contaminated, low resolution, or mismatched to the target layout.

Treatment:

- reverse-analyze visual properties into a prompt;
- generate a text-free base;
- overlay editable business content;
- record prompt and model/backend.

### Disallowed Mode

`SVM_RAW_CROP_WITH_TEXT` is disallowed by default.

If used, mark:

```json
{
  "module_status": "V6.2_FAIL_RAW_CROP_FALLBACK",
  "reason": "why a native or clean-base reconstruction was not feasible",
  "user_accepted": false
}
```

---

## 6. Generative Visual-Base Reconstruction

### 6.0 Mandatory Scientific Figure Workflow

For large scientific visuals, do not crop the reference panel and resize it into the PPT. Use this workflow instead:

1. **Reverse-analyze the figure**  
   Identify the scientific subject, scene structure, camera/viewpoint, color palette, material style, density, depth, background, light direction, and intended blank zones for overlays.

2. **Separate visual base from semantic layer**  
   Visual base includes liposome/cell/tissue/molecule illustration, soft background, particle field, and organic texture.  
   Semantic layer includes arrows, labels, numbered badges, legends, captions, callout text, conclusions, source notes, and all factual claims.

3. **Write a text-free generation prompt**  
   The prompt must describe only the visual base and must explicitly exclude text, labels, arrows, numbers, legends, logos, UI, watermark, and trial claims.

4. **Generate or clean the base**  
   Generate a complete, uncropped, text-free scientific visual base at the target module aspect ratio, or clean an existing asset until no baked semantic layer remains. Preserve biological proportions and do not non-uniformly stretch the base.

5. **Rebuild the semantic layer natively**  
   Add arrows, connector lines, numbered badges, labels, legends, captions, conclusions, and source notes as editable PPT objects. Use the deck's icon/numbering system.

6. **Record the prompt and overlay plan**  
   Create or update `scientific_visual_prompts.json` with the reverse analysis, prompt, model/backend, asset path, rejected generations if any, and editable overlay list.

7. **Run scientific-base QA**  
   Reject/regenerate if the base has text-like marks, cut-off cells/liposomes, baked arrows, hard crop edges, distorted anatomy/particles, or too much clutter for readable overlays.

This workflow is mandatory for liposomes, cells, tumor/tissue structures, molecular shells, vascular/tissue delivery scenes, and mechanism artwork when the figure is larger than an atomic object or controls page hierarchy.

### 6.1 When To Use

Use prompt-based generation for large scientific visual bases when:

- the reference module is visibly cropped or incomplete;
- the module includes baked labels/arrows that would ghost under overlays;
- scaling the crop would distort liposomes/cells;
- the illustration is too low-resolution for the target size;
- the target template needs different whitespace while preserving the same scientific feel.

### 6.2 What Generation May Produce

Allowed:

- text-free liposome particle;
- tumor cell cluster;
- vascular/tissue scene;
- cellular/molecular texture;
- drug-release visual background;
- clean mechanism illustration base;
- transparent or flat-background icon-like scientific object.

Not allowed:

- clinical evidence claims;
- exact molecular structures unless provided/verified;
- product logos or pseudo-official branding;
- text, labels, numbers, arrows, legends, axes, tables;
- fake trial data or fake source citation visuals.

### 6.3 Prompt Recipe

Every generative visual-base prompt should specify:

- subject: what biological/scientific object is shown;
- composition: angle, crop, focus, density, depth;
- style: medical PPT, clean 3D/2.5D, white/light background, teal/blue palette;
- constraints: no text, no numbers, no arrows, no labels, no watermark;
- usability: leave blank zones for editable labels, clean edges, high resolution;
- aspect ratio: match the target module bounding box.

Store:

```json
{
  "asset_id": "s05_liposome_base",
  "mode": "SVM_GENERATIVE_BASE",
  "source_reference": "source_05.png",
  "prompt": "...",
  "generation_backend": "openai_images_api | unknown_builtin_imagegen | other",
  "model": "gpt-image-2 | unknown | ...",
  "final_use": "text-free scientific visual base with editable overlays",
  "not_for_factual_claims": true
}
```

`scientific_visual_prompts.json` example:

```json
{
  "figures": [
    {
      "module_id": "liposome_delivery_base",
      "source_reference": "source_02.png",
      "reverse_analysis": {
        "subject": "liposomal irinotecan delivery near tumor tissue",
        "composition": "large blue-teal liposome above soft tumor cluster, subtle particles, white medical slide background",
        "style": "premium pharmaceutical 3D/2.5D illustration",
        "blank_overlay_zones": ["right callout column", "top label strip"]
      },
      "prompt": "Create a text-free premium medical PPT illustration base...",
      "negative_constraints": [
        "no text",
        "no labels",
        "no arrows",
        "no numbers",
        "no legends",
        "no logo",
        "no watermark"
      ],
      "generation_backend": "openai_images_api | unknown_builtin_imagegen | other",
      "model": "gpt-image-2 | unknown | ...",
      "asset_path": "assets_v6/03_svm/liposome_delivery_base.png",
      "editable_overlay_plan": [
        "PPT arrows",
        "PPT numbered badges",
        "PPT callout labels",
        "PPT conclusion text"
      ],
      "qa_status": "accepted | regenerate_required",
      "qa_notes": []
    }
  ]
}
```

### 6.4 Required Checks

Reject and regenerate if:

- text-like marks appear;
- label/arrow remnants appear;
- object edges are cut off unintentionally;
- the asset contains a rectangular white box edge;
- visual density prevents readable overlays;
- scientific appearance is inconsistent with the reference page.
- any semantic content that should be editable is baked into the image.

---

## 7. Page Hierarchy Pass

Before building slides, create `visual_hierarchy.json` for each page.

Required fields:

```json
{
  "slide": 1,
  "first_read": "dominant module or claim",
  "second_read": "supporting chart/table/process",
  "insight_zone": "right/side/bottom card",
  "conclusion_zone": "bottom bar",
  "source_zone": "footer",
  "dominance_ratios": {
    "first_read_area_pct": 35,
    "insight_area_pct": 15,
    "footer_area_pct": 4
  },
  "must_not_shrink": ["main mechanism diagram"],
  "safe_area_adjustments": []
}
```

Rules:

- preserve the original first-read object unless the user asked for a redesign;
- do not demote the main image/table into a small card;
- do not make all cards equal if the reference has clear visual dominance;
- keep insight cards visually secondary to the proof module;
- keep source notes small and low-contrast.

---

## 8. Proportional Fidelity Rules

Use reference coordinate mapping first:

```text
source 1600x900 -> PPT 1280x720
scale_x = 0.8
scale_y = 0.8
```

Then adjust only for:

- template logo/slogan/safe areas;
- PowerPoint font metrics;
- readability;
- intentional design improvement documented in `deviation_log`.

Do not:

- stretch biological objects non-uniformly;
- crop large module edges to fit a new grid;
- replace organic mechanism art with unrelated icon cards;
- shrink a complex module below readable scale.

Use `max_allowed_offset_px` by element type:

| Element | Offset Limit |
| --- | ---: |
| page title | 8 px |
| main visual module | 10 px |
| table/matrix bounds | 10 px |
| insight card bounds | 10 px |
| conclusion bar | 8 px |
| source note | 14 px |

---

## 9. Icon And Numbering System

Create `icon_system.json` before final build.

Required decisions:

- icon source: lucide, supplied SVGs, generated SVG set, or native minimal pictograms;
- stroke width;
- corner style;
- filled vs outline;
- primary colors;
- number badge diameter;
- number font size;
- number alignment;
- icon-to-label spacing.

Rules:

- use one icon style per deck;
- do not use emoji;
- do not mix thick filled icons with thin outline icons unless the reference does and it is intentional;
- align number badges to a consistent optical center;
- keep numbered rows at consistent height;
- group icon + number + label so the system moves as one unit;
- do not crop icons from a large screenshot if they can be rebuilt.

Suggested default:

```json
{
  "number_badge": {
    "diameter_px": 24,
    "font_px": 11,
    "font_weight": "bold",
    "fill": "#0BA29A",
    "text": "#FFFFFF"
  },
  "icon": {
    "style": "medical line icon",
    "stroke_px": 2,
    "color": "#0054A6",
    "container": "optional pale blue circle"
  }
}
```

---

## 10. Premium Polish Rules

V6.2 Polish Pass fixes not only dirt, but also design maturity.

Check:

- hierarchy: first-read area is dominant;
- visual rhythm: not every card has identical size and weight;
- whitespace: dense proof area balanced by lighter insight area;
- color discipline: one main color family plus one emphasis color;
- depth: shadows are subtle and consistent;
- typography: title, module title, body, labels, footnotes follow a clear scale;
- icon system: no mixed visual languages;
- conclusion bar: strong but not overpowering;
- source note: present but visually quiet.

Do not solve polish by:

- adding more cards;
- shrinking all content;
- covering bad crops with white boxes;
- using decorative gradients/orbs unrelated to the reference;
- using a full-slide screenshot.

---

## 11. Manifest Requirements

Add these files when possible:

```text
assets_v6/06_layout/
  manifest.json
  layout_v6.json
  asset_metadata.json
  scientific_visual_prompts.json
  visual_hierarchy.json
  icon_system.json
  module_ownership.json
  polish_manifest.json
```

`module_ownership.json` example:

```json
{
  "modules": [
    {
      "id": "main_mechanism",
      "bbox": {"x": 60, "y": 150, "w": 600, "h": 330},
      "area_pct": 22,
      "contains_text": true,
      "ownership": "SVM_CLEAN_BASE_PLUS_OVERLAY",
      "raw_crop_allowed": false,
      "reason": "large structured mechanism panel with labels and arrows"
    }
  ]
}
```

`asset_metadata.json` must distinguish:

- user-provided atomic crop;
- cleaned visual base;
- generated visual base;
- supplied template asset;
- raw crop fallback.

---

## 12. QA Gates

### 12.1 Hard Failures

Fail V6.2 QA if any is true:

- a large module is a raw crop with baked text;
- table/matrix data is not editable;
- bottom conclusion is not editable;
- main title is not editable;
- visual base has visible baked text underneath editable text;
- scientific visual is cut off or visibly distorted;
- raw crop has a hard rectangular edge;
- icon/numbering system mixes styles without a documented reason;
- first-read hierarchy is weaker than the reference by inspection.

### 12.2 Scoring

Stage 1 draft:

| Dimension | Weight |
| --- | ---: |
| Structural reconstruction | 25 |
| Content editability | 25 |
| Visual hierarchy fidelity | 20 |
| Asset/base quality | 15 |
| Proportional fidelity | 10 |
| Reusability metadata | 5 |

Stage 2 after Polish:

| Dimension | Weight |
| --- | ---: |
| First-glance similarity | 25 |
| Large-module reconstruction quality | 25 |
| Content editability | 20 |
| Premium polish | 15 |
| Icon/numbering consistency | 10 |
| Maintainability | 5 |

Thresholds:

```text
>= 92: production-ready editable reconstruction
88-91: usable, minor polish remaining
82-87: structurally valid but needs another polish pass
< 82: return to reconstruction stage
any hard failure: do not deliver as V6.2 success
```

---

## 13. Final Checklist

### Reconstruction

- [ ] Large modules rebuilt or clean-base-plus-overlay, not raw cropped.
- [ ] Tables/matrices are editable or intentionally native-looking shape tables.
- [ ] Mechanism/process arrows and labels are editable.
- [ ] Scientific visuals are not cut off or distorted.
- [ ] Main visual hierarchy matches the reference.

### Editability

- [ ] Title editable.
- [ ] Subtitle editable.
- [ ] Core numbers editable.
- [ ] Explanatory text editable.
- [ ] Table data editable.
- [ ] Chart labels editable.
- [ ] Conclusion copy editable.
- [ ] Source note editable.

### Visual Quality

- [ ] No ghosting.
- [ ] No duplicate lines/dots/icons.
- [ ] No hard crop edges.
- [ ] No non-uniform scaling of biological visuals.
- [ ] White space and rhythm feel intentional.

### Systems

- [ ] Icon system defined.
- [ ] Numbering system defined.
- [ ] Color hierarchy consistent.
- [ ] Fonts and sizes consistent.
- [ ] Raw crop fallbacks documented if any.

---

## 14. Prompt Templates

### 14.1 Generic V6.2 Task Prompt

```text
Use skn-image2ppt V6.2 to convert this reference image into a high-fidelity editable PPTX.

Do not use raw crops for large modules. Rebuild tables, card groups, flows, insight cards, conclusion bars, and simple charts as structured PPT objects. Use images only for atomic visual assets or clean/generated text-free scientific visual bases.

Create module_ownership.json, visual_hierarchy.json, icon_system.json, manifest.json, preview, diff overlay, and polish report. Run the V6.2 hard-failure QA gate before delivery.
```

### 14.2 Scientific Visual-Base Prompt Template

```text
Create a text-free medical PPT scientific illustration base.

Subject: [liposomal irinotecan particle / tumor cell cluster / vascular tissue delivery scene].
Composition: [same broad composition as the reference: central particle, left-to-right flow, circular cluster, etc.].
Style: premium pharmaceutical consulting slide, clean 3D/2.5D medical illustration, white or very pale blue background, teal-blue palette with subtle depth.
Constraints: no text, no labels, no numbers, no arrows, no legends, no watermark, no UI, no logo.
Usability: leave clean whitespace for editable PPT labels and arrows; keep edges complete; avoid hard rectangular background edge; high resolution.
Aspect ratio: [target ratio].
```

### 14.3 Reverse-Analysis Notes Template

```json
{
  "reference_visual": "source_02 mechanism panel",
  "semantic_subject": "liposomal irinotecan delivery through tumor vasculature",
  "visual_features": [
    "central blue-teal liposome particle",
    "soft tissue/tumor cluster below",
    "small orange drug particles",
    "clinical PPT style, white background"
  ],
  "do_not_generate": [
    "Chinese labels",
    "arrows",
    "trial claims",
    "brand logo"
  ],
  "overlay_plan": [
    "editable arrows",
    "editable callout labels",
    "editable numbered benefits"
  ]
}
```

---

## One-Sentence Principle

```text
V6.2 rebuilds the page; assets support reconstruction, they do not replace it.
```

Chinese:

```text
V6.2 的核心是先重构页面，大图素材只能辅助重构，不能替代重构。
```
