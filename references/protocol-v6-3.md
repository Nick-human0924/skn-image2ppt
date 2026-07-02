# Image2 to Editable PPT Reconstruction Protocol v6.3

Version: v6.3  
Positioning: Premium Visual Asset + Editable Semantic Overlay.  
Goal: preserve high-end medical/scientific visual quality while keeping business content editable.

## 1. Change From V6.2

V6.2 correctly banned large raw crops, but it can be over-applied as all-vector redrawing. V6.3 adds the opposite guardrail:

```text
Do not raw-crop whole pages or text-heavy modules.
Do not simplify premium scientific visuals into PPT primitive drawings.
Use clean high-quality raster visual assets for visual texture.
Use editable PPT objects for semantics.
```

## 2. Layer Model

| Layer | Contents | Owner |
| --- | --- | --- |
| Template | brand chrome, logo, background arc | source template |
| Premium visual base | liposomes, cells, tissue, delivery scenes, glows, dashboards, flywheels, 3D visual texture | text-free image asset |
| Native structure | cards, borders, grids, dividers, simple badges, simple connectors | PPT shapes |
| Editable semantics | text, numbers, labels, arrows, tables, charts, insight copy, conclusions, sources | PPT text/table/chart/shapes |

## 3. Asset-First Rule For Premium Visuals

Default these to text-free image assets:

- liposome spheres and cutaway structures
- lipid bilayers and encapsulated drug particles
- tumor enrichment, vascular delivery, tissue/cell scenes
- molecular/cellular medical artwork
- premium glows, gradients, depth, micro-texture
- high-end value dashboard bases and closed-loop/flywheel bases

Do not build these mainly from circles, lines, rectangles, and simple PPT gradients if the reference has medical-conference quality.

## 4. Editable Overlay Rule

Always overlay as PPT-editable objects:

- every product name and company name
- all labels, callout titles, mechanism steps
- all arrows and numbering
- all clinical/evidence/commercial claims
- every number, percentage, price, unit, and date
- every table cell and chart label
- conclusions, source notes, compliance notes

## 5. Visual Asset Prompt Template

```text
Create a high-end text-free medical consulting PowerPoint visual asset.
Subject: [specific asset].
Composition: [object placement, camera/view, empty overlay zones].
Style: premium medical conference / pharmaceutical consulting, 3D or 2.5D, teal-blue palette, soft glow, depth, gradient, micro-texture, clean white or pale blue background.
Constraints: no text, no Chinese characters, no labels, no arrows, no numbers, no table, no legend, no logo, no watermark, no UI.
Usability: leave clean blank zones for editable PPT overlays; complete uncropped object; no hard rectangular crop edge; high resolution.
Aspect ratio: [target ratio].
```

## 6. Required Sidecar Files

Create these when possible:

```text
assets_v6/06_layout/
  visual_asset_plan.json
  visual_asset_prompts.json
  overlay_plan.json
  module_ownership.json
  visual_hierarchy.json
  icon_system.json
  premium_visual_qa.json
  manifest.json
  polish_manifest.json
```

## 7. Background Integration Pass

Premium visual assets must blend into the PPT page or card. A correct V6.3 asset should not look pasted on.

Use these treatments:

- **Isolated object**: liposome, vial, single molecule, portrait-like object. Use transparent PNG, alpha matte, or edge-connected near-white background removal. Preserve internal white highlights and membrane details.
- **Scene/panel asset**: drug dispersion scene, tissue delivery scene, dashboard background, flywheel base. Either fill the whole intended panel or feather the asset edges into the PPT/card background.
- **Intentional framed panel**: if the asset is meant to sit in a visible image frame, the frame must be a PPT shape with consistent radius/border/shadow.

Choose and record one treatment per asset:

- `transparent_matte`: edge-connected background removed to alpha; default for isolated liposomes, vials, molecules, and closed-loop motifs.
- `same_color_fill`: generated/edited asset background matches the exact PPT/card fill color.
- `full_panel`: scene asset fills the entire intended panel, with the panel boundary supplied by PPT shapes.
- `edge_feather`: non-critical scene/dashboard background fades into the card fill at final placement size.

Fail QA if a generated asset has a gray/white rectangle, mismatched blue/gray color temperature, or visible pasted edge against the slide background.

`visual_asset_plan.json` must include:

```json
{
  "assets": [
    {
      "id": "p2_liposome_delivery_base",
      "slide": 2,
      "type": "scientific_visual_base",
      "target_bbox": {"x": 720, "y": 160, "w": 500, "h": 330},
      "must_be_text_free": true,
      "background_treatment": "edge_feather",
      "target_background": "#F6FBFF",
      "must_preserve": ["3D depth", "soft glow", "medical illustration texture"],
      "overlay_semantics": ["callout labels", "number badges", "arrows", "conclusion"]
    }
  ]
}
```

## 8. QA Gates

Fail if:

- a full slide is a raster screenshot
- a large text/table/card module is a raw crop
- a liposome/cell/tissue/flywheel/dashboard base contains baked text or arrows
- a premium scientific figure is visibly simplified into low-end PPT vectors
- a generated asset has text-like marks, labels, numbers, UI, watermarks, or hard crop edges
- an asset background does not match the surrounding PPT background or has visible rectangular edges
- editable semantics are missing or misaligned
- a biological/scientific object is distorted by non-uniform scaling

## 9. Polish Pass

Check both visual quality and editability:

- visual base keeps premium conference quality
- visual base blends into the PPT/card background without pasted edges
- overlays align without fighting the base
- text has no ghosting underneath
- cards/tables remain editable and clean
- hierarchy follows the reference
- page does not look over-regular, flat, or internal-training style
