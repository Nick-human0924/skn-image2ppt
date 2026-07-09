# Image2 to Editable PPT Reconstruction Protocol v6.6

Version: v6.6  
Positioning: Topology-Faithful Premium Visual Asset + Execution Engine QA.  
Goal: keep V6.5's topology, source-bbox, icon, and font-size guardrails, then add a repeatable execution layer inspired by GordenImage2PPTX: standard composition, stronger chroma-key cleanup, stronger icon slicing, imagegen evidence, and optional frame-layer reconstruction.

## 1. Change From V6.5

V6.5 made the right failure modes visible: uncopyable icons, tiny text, and coordinate drift. V6.6 makes the process more repeatable:

- use `compose_pptx.py` for standard layered PPTX generation and PNG previews;
- use `chroma_key.py --preset frame-safe/icon-safe --scale 2` for generated frame/icon layers;
- use `slice_grid.py --auto --pad 24 --contact-sheet` for icon sheets;
- use `frame_parts_to_icons.py` only when the user explicitly requests movable frame parts;
- require `imagegen-assets-manifest.json` for generated background/frame/icon layers;
- require the current source image to be loaded as the imagegen edit target before extraction-style generation.

## 2. Reconstruction Modes

Choose one mode per page and record it in `run_manifest.json` or the slide layout:

- `hybrid_mode` (default): preserve complex/premium visuals as high-quality assets, rebuild business semantics as editable PPT objects, and use native shapes for simple structures.
- `native_structure_mode`: use PPT shapes/tables/connectors when the page is simple enough to remain faithful and more editable.
- `frame_layer_mode`: use a full-slide transparent `frame.png` for dense frames, fills, glows, dividers, chart skeletons, and other non-text visual structure that would drift if rebuilt one shape at a time. Text, numbers, labels, arrows, and tables still stay editable.

Do not use `frame_layer_mode` to bake business text or chart/table values into images.

## 3. RUN_ROOT Contract

Every conversion starts in a unique task root:

```text
image2pptx_runs/<yyyymmdd-hhmmss>_<source-slug>/
  original_inputs/
  editable/01/
    source.png
    prompts/
    background.png
    frame_raw.png
    frame.png
    icons_raw_1.png
    icons_t_1.png
    icons/
    layout.json
    imagegen-assets-manifest.json
    icon_extraction_plan.json
    placement_fix_notes.json
    qa/
  out/
    preview/
    final.pptx
```

Do not read from fixed historical folders such as `editable/01`, `out`, `qa`, or prior project outputs unless the user explicitly asks to reuse them.

## 4. Imagegen Edit-Target Evidence

When using image generation to extract or recreate layers from a source slide:

1. Open/view the current source image first so it is the visible edit target.
2. In the prompt, explicitly state that the just-shown image is the only edit target.
3. Save the prompt to `prompts/`.
4. Copy the generated output into the current `RUN_ROOT`.
5. Record the layer in `imagegen-assets-manifest.json`.

Manifest schema:

```json
{
  "layers": [
    {
      "layer": "frame",
      "backend": "imagegen",
      "prompt_file": "prompts/frame.txt",
      "generated_source": "C:/Users/.../generated_images/.../image.png",
      "copied_to": "D:/.../RUN_ROOT/editable/01/frame_raw.png",
      "key_color": "#00ff00",
      "source_image": "D:/.../RUN_ROOT/editable/01/source.png",
      "edit_target_confirmed": true
    }
  ]
}
```

Fail QA if generated layers lack backend, prompt file, generated source, copied output, or edit-target confirmation.

## 5. Standard Layered Layout

For the standard execution path, use `compose_pptx.py` with a `layout.json` or `deck.json`:

```json
{
  "slide_width_in": 13.333,
  "slide_height_in": 7.5,
  "units": "fraction",
  "ref_width": 2134,
  "ref_height": 1200,
  "background": "background.png",
  "frame": "frame.png",
  "icons": [
    {"file": "icons/ic_01.png", "x": 0.07, "y": 0.40, "w": 0.04, "h": 0.07,
     "source_bbox": [150, 480, 86, 84]}
  ],
  "texts": [
    {"text": "逐字原文", "x": 0.12, "y": 0.08, "w": 0.50, "h": 0.08,
     "source_bbox": [256, 96, 1067, 96],
     "size_ratio": 0.035, "color": "#12306F", "bold": true,
     "align": "left", "valign": "top", "font": "Microsoft YaHei"}
  ]
}
```

Layer order is: background -> optional full-frame image -> shapes/native structure -> icons/assets -> editable text.

## 6. Strong Chroma-Key And Icon Slicing

Use:

```bash
python scripts/chroma_key.py --input frame_raw.png --out frame.png --preset frame-safe --scale 2 --force
python scripts/chroma_key.py --input icons_raw_1.png --out icons_t_1.png --preset icon-safe --scale 2 --force
python scripts/slice_grid.py icons_t_1.png icons --auto --pad 24 --contact-sheet --prefix ic
```

Rules:

- Use a safe key color from `probe_palette.py`; if the slide contains green, use a non-green key color such as `#ff00ff`.
- Inspect the gray/background preview manually when available.
- Inspect `icons_contact_sheet.png`; regenerate or reslice if icons are clipped, merged, edge-touching, or missing.
- Do not slice the original slide screenshot to create icons unless the user explicitly accepts bitmap-crop fallback.

## 7. Optional Frame Parts

Keep `frame.png` as one full-frame transparent layer by default. This preserves fills, glows, dividers, and chart skeletons with the least drift.

Only when the user explicitly asks for movable frame parts:

```bash
python scripts/slice_grid.py frame.png frame_parts --components --pad 0 --contact-sheet --prefix fp
python scripts/frame_parts_to_icons.py frame_parts/icons_manifest.json --ref-width <source_w> --ref-height <source_h> --out frame_parts/frame_parts_layout_icons.json
```

Do not use square padding for frame parts; bbox replay must reconstruct the original full frame.

## 8. Coordinate And Text Contracts

Keep V6.5 contracts:

```text
x = source_bbox[0] / ref_width
y = source_bbox[1] / ref_height
w = source_bbox[2] / ref_width
h = source_bbox[3] / ref_height
pt = source_text_height_px * slide_height_in * 72 / ref_height
```

Run:

```bash
python scripts/layout_guard.py source.png layout.json --strict
```

If coordinates came from a same-aspect thumbnail, use the guard's fix options only when you know the scale relationship, then visually recheck source boxes:

```bash
python scripts/layout_guard.py source.png layout.json --fix-ref-to-source --fix-fractions --in-place
```

## 9. Compose And QA Loop

```bash
python scripts/layout_guard.py source.png layout.json --strict
python scripts/placement_qa.py source.png layout.json --slide-index 1 --out-dir qa/source-boxes
python scripts/compose_pptx.py layout.json out/final.pptx --preview-dir out/preview
python scripts/placement_qa.py source.png layout.json --slide-index 1 --preview out/preview/slide_01.png --out-dir qa/placement
python scripts/visual_compare_qa.py source.png out/preview/slide_01.png --out-dir qa/visual
python scripts/pptx_editability_lint.py out/final.pptx --json
```

At least one correction loop is required for dense pages:

1. correct icon center and visual size;
2. correct text point size, line spacing, and wrapping;
3. correct `source_bbox` and fraction coordinates;
4. correct frame-anchor offsets for text attached to image-generated frames;
5. rerender and compare again.

## 10. QA Gates

Fail V6.6 QA if any is true:

- `RUN_ROOT` is missing or old fixed folders are reused.
- `ref_width/ref_height` does not match the actual source image.
- positioned text/icon/assets lack `source_bbox`.
- fraction coordinates do not match `source_bbox`.
- normal text is visibly smaller than the source.
- meaningful icons are missing, clipped, edge-touching, duplicated, too small, or uncopyable without reason.
- generated layers lack `imagegen-assets-manifest.json` evidence.
- imagegen prompts did not use the current source image as edit target.
- no `compose_pptx.py` preview is generated for the standard layered path.
- no placement overlay or visual diff is generated for dense pages.
- PPTX ZIP/XML validation fails or normal text relies on unexpected shrink-to-fit.
- frame-attached text visibly misses the final frame and lacks frame-anchor correction.

## 11. One-Sentence Principle

```text
V6.6 keeps SKN's editability decisions, then adds Gorden-style execution controls so the reconstruction can be repeated, inspected, and corrected.
```
