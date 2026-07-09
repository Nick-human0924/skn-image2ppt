# SKN Image2PPT V6.6 Utility Scripts

These scripts implement the V6.6 execution engine and Engineering QA pass:

- `probe_palette.py`: suggest a safe chroma-key background color.
- `chroma_key.py`: remove flat key colors with frame-safe/icon-safe presets, supersampling, and line/color preservation.
- `slice_grid.py`: slice transparent icon sheets by grid, auto segmentation, or optional frame-part components; writes contact sheets and edge-touch metadata.
- `layout_guard.py`: validate or fix `source_bbox`, fraction coordinates, text sizing, and all-bold/tiny-text risks.
- `compose_pptx.py`: compose background/frame/icons/texts layout JSON into editable PPTX and preview PNGs.
- `frame_parts_to_icons.py`: optional helper that maps sliced frame parts back into layout icon entries.
- `placement_qa.py`: draw layout boxes on the source image and rendered preview.
- `visual_compare_qa.py`: create side-by-side, blend, diff heatmap, and metrics.
- `pptx_editability_lint.py`: check PPTX ZIP/XML validity, shrink-to-fit, and tiny explicit font runs.

They are guards and helpers; visual judgment and Polish Pass are still required.
