# Image2 to Editable PPT Reconstruction Protocol v6.5

Version: v6.5  
Positioning: Topology-Faithful Premium Visual Asset + Engineering QA.  
Goal: keep the V6.4 topology/editability model while fixing practical failures: uncopyable icons, text rendered too small, and layout drift.

## 1. Change From V6.4

V6.4 protected the reference topology and high-end visual assets. Testing shows the remaining failures are execution failures:

- icons stay baked into image bases or cannot be copied independently;
- text boxes use thumbnail measurements, so text renders too small;
- `x/y/w/h` use one coordinate system while `source_bbox` uses another;
- generated visual bases drift a few pixels, but attached text is not recalibrated;
- QA relies on human eyeballing instead of reproducible overlays and diff images.

V6.5 adds an engineering layer:

```text
topology lock
+ visual element ledger
+ source_bbox contract
+ icon extraction plan
+ layout/font guard
+ placement overlay
+ visual compare QA
+ frame-anchor calibration
```

## 2. RUN_ROOT Contract

Every conversion must start in a unique task root:

```text
image2pptx_runs/<yyyymmdd-hhmmss>_<source-slug>/
  original_inputs/
  editable/01/
    source.png
    assets/
    icons/
    prompts/
    layout.json
    icon_extraction_plan.json
    placement_fix_notes.json
    qa/
  out/
    preview/
    final.pptx
```

Do not read from old fixed folders such as `out/`, `editable/01/`, or prior projects unless the user explicitly asks to reuse them.

## 3. Source BBox Coordinate Contract

Every positioned object must preserve both:

- `source_bbox`: `[x_px, y_px, w_px, h_px]` in the original source image's actual pixel coordinate system.
- `x/y/w/h`: final normalized fraction coordinates derived from `source_bbox`.

Formula:

```text
x = source_bbox[0] / ref_width
y = source_bbox[1] / ref_height
w = source_bbox[2] / ref_width
h = source_bbox[3] / ref_height
```

If measurements come from a displayed thumbnail, first convert back:

```text
source_x = thumbnail_x * source_width / thumbnail_width
source_y = thumbnail_y * source_height / thumbnail_height
source_w = thumbnail_w * source_width / thumbnail_width
source_h = thumbnail_h * source_height / thumbnail_height
```

Never mix source-image width with thumbnail y coordinates.

## 4. Text Size Contract

The default text-size calculation should use source pixel height:

```text
pt = source_text_height_px * slide_height_in * 72 / ref_height
```

For a 16:9 deck at 7.5 in high:

```text
pt = source_text_height_px * 540 / ref_height
```

Rules:

- Record `source_text_height_px` or infer it from `source_bbox` line height.
- Correct font size before correcting x/y placement.
- If text looks too small relative to the reference, do not solve it by moving the box; recalculate the point size.
- For tiny footnotes, mark `small_text_ok: true`.
- Do not set all body text to bold unless the reference is truly all bold.

## 5. Icon Extraction Plan

Create `icon_extraction_plan.json` before final layout:

```json
{
  "icons": [
    {
      "id": "benefit_icon_01",
      "role": "benefit list icon",
      "required": true,
      "source_bbox": [118, 422, 42, 42],
      "treatment": "svg_or_transparent_png",
      "final_file": "icons/benefit_icon_01.png",
      "status": "placed_icon",
      "copyable": true,
      "qa": {
        "clipped": false,
        "duplicated": false,
        "too_small": false
      }
    }
  ]
}
```

Allowed treatments:

- `native_shape`
- `svg_icon`
- `transparent_png`
- `generated_icon_sheet_slice`
- `covered_by_text_free_asset` only when the icon is decorative and does not need to be independently copied
- `intentionally_omitted` only with reason

Fail QA if a meaningful icon is missing, clipped, merged with another icon, duplicated, too small, or not independently selectable when it should be copyable.

## 6. Optional Icon Sheet Pipeline

Use this for many small icons or decorative assets:

1. Generate or clean an icon sheet on a high-contrast flat background.
2. Remove the key color with a color-preserving chroma-key pass.
3. Slice by grid or connected transparent components.
4. Generate a contact sheet.
5. Inspect the contact sheet before placing icons.
6. Place each icon using source-image bbox center and size.

Do not slice the original slide screenshot to create icons unless the user explicitly accepts bitmap-crop fallback.

## 7. Frame-Anchor Calibration

Some visual bases or frame assets drift relative to the source after generation/cleanup. Text attached to a frame must follow the final frame, not only the source bbox.

Apply to:

- card titles
- button text
- bottom conclusion bars
- ribbon labels
- section headers inside generated visual frames
- labels attached to generated mechanism/flywheel bases

Record adjustments:

```json
{
  "text": "核心优势",
  "frame_anchor": "left_card_title_bar",
  "old_source_bbox": [112, 330, 180, 32],
  "new_source_bbox": [112, 338, 180, 32],
  "dx_px": 0,
  "dy_px": 8,
  "reason": "final generated title bar is 8px lower than reference"
}
```

## 8. Engineering QA Pass

Run this after the draft layout exists and before delivery:

1. `layout_guard`: verify `ref_width/ref_height`, `source_bbox`, fraction coordinates, text size, and bold flags.
2. `placement_qa`: draw text/icon/asset boxes over the source image.
3. Render the PPT preview.
4. `placement_qa`: draw boxes over the rendered preview.
5. `visual_compare_qa`: generate side-by-side, blend, and diff heatmap.
6. Correct:
   - icon center and size;
   - text point size and line spacing;
   - text bbox and wrapping;
   - frame-anchor offsets;
   - duplicated or missing icons.
7. Re-render and repeat until the major visual drift is resolved.

## 9. Tooling

Use bundled scripts when available:

```text
scripts/probe_palette.py
scripts/chroma_key.py
scripts/slice_grid.py
scripts/layout_guard.py
scripts/placement_qa.py
scripts/visual_compare_qa.py
```

These scripts are utility guards. They do not replace visual judgment, but they prevent common numerical and asset-preparation failures.

## 10. QA Gates

Fail V6.5 QA if any is true:

- `RUN_ROOT` is missing or files are written to reused fixed folders.
- `ref_width/ref_height` does not match the actual source image.
- positioned text/icon elements lack `source_bbox`.
- fraction coordinates do not match `source_bbox`.
- main text is visibly too small relative to the reference.
- a meaningful icon is missing, clipped, too small, duplicated, or baked into an uncopyable large asset without reason.
- no placement overlay is generated for dense pages.
- no visual diff/side-by-side QA is generated for final preview.
- frame-attached text is visibly offset after asset generation and lacks frame-anchor correction.

## 11. Final Deliverables

Include:

- final PPTX
- rendered preview
- side-by-side QA image
- blend QA image
- diff heatmap
- layout JSON
- `topology_lock.json`
- `visual_element_ledger.json`
- `icon_extraction_plan.json`
- `placement_fix_notes.json`
- `engineering_qa_report.json`
- `polish_report.md`

## 12. One-Sentence Principle

```text
V6.5 keeps the V6.4 reconstruction philosophy, then adds measurable guards so icons, text scale, and placement actually match the reference.
```
