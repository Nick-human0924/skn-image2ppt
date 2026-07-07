# SKN Image2PPT V6.5 Utility Scripts

These scripts implement the V6.5 Engineering QA pass:

- `probe_palette.py`: suggest a safe chroma-key background color.
- `chroma_key.py`: remove a flat key color while preserving object color.
- `slice_grid.py`: slice transparent icon sheets by grid or connected components.
- `layout_guard.py`: validate `source_bbox`, fraction coordinates, and text sizing.
- `placement_qa.py`: draw layout boxes on the source image and rendered preview.
- `visual_compare_qa.py`: create side-by-side, blend, diff heatmap, and metrics.

They are guards and helpers; visual judgment and Polish Pass are still required.
