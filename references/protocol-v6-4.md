# Image2 to Editable PPT Reconstruction Protocol v6.4

Version: v6.4  
Positioning: Topology-Faithful Premium Visual Asset + Editable Semantic Overlay.  
Goal: preserve the reference page's visual structure, premium visual quality, and business editability.

## 1. Change From V6.3

V6.3 fixed raw-crop, all-vector simplification, and pasted-background failures. V6.4 adds a stricter guardrail:

```text
Do not replace the reference structure with a merely similar theme.
Lock the page topology before creating assets or PPT objects.
Map every meaningful non-text visual element before rebuilding the page.
```

Examples of topology failures:

- radial four-product network rebuilt as four rectangular cards
- two-panel mechanism diagram rebuilt as unrelated tissue scene panels
- 3D evidence pyramid rebuilt as flat bars
- dosing workflow rebuilt without infusion bags, molecules, pumps, brackets, or liposome visuals

## 2. Required Sidecar Files

Create these before final export:

```text
assets_v6/06_layout/
  topology_lock.json
  visual_element_ledger.json
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

## 3. Topology Lock

For each slide, record:

```json
{
  "slide": 2,
  "reference_topology": "two_panel_mechanism_comparison",
  "must_preserve": [
    "left ordinary exposure panel",
    "center upgrade arrow",
    "right liposome delivery panel",
    "right-side vertical mechanism list",
    "three bottom evidence cards"
  ],
  "allowed_deviation": "minor spacing and editable overlay adjustments only",
  "forbidden_deviation": [
    "replace with unrelated theme illustration",
    "remove IV bag, vessel, organ/tumor/tissue visual path",
    "move callout list outside panel"
  ]
}
```

Use these common topology names:

- `radial_product_network`
- `two_panel_mechanism_comparison`
- `evidence_pyramid`
- `dosing_workflow`
- `matrix_or_table`
- `dashboard_orbit`
- `flywheel`
- `process_chain`

## 4. Visual Element Ledger

For each slide, map every meaningful non-text element:

```json
{
  "slide": 7,
  "elements": [
    {"id": "iv_bag_1", "role": "dose_step_visual", "required": true, "treatment": "native_shape_or_text_free_asset"},
    {"id": "liposome_1", "role": "dose_step_visual", "required": true, "treatment": "text_free_asset"},
    {"id": "lv_molecule", "role": "dose_step_visual", "required": true, "treatment": "native_shape"},
    {"id": "infusion_pump", "role": "dose_step_visual", "required": true, "treatment": "native_shape_or_icon"},
    {"id": "q2w_bracket", "role": "cycle_connector", "required": true, "treatment": "native_shape"}
  ]
}
```

Fail QA if any required element is missing, replaced by an unrelated icon, or omitted without a reason.

## 5. Visual Asset Prompt Addendum

Every premium asset prompt must include a topology line:

```text
Topology requirements: preserve [specific structure], include [required sub-elements], keep [relative positions], leave [overlay zones] blank.
```

For mechanism diagrams, prompt for text-free visual bases with the same sub-elements and reading path, not generic tissue scenes.

## 6. Layer Ownership

Use these defaults:

| Reference part | Preferred treatment |
| --- | --- |
| titles, labels, captions, numbers, bullets | editable PPT text |
| tables and simple grids | native PPT shapes/text |
| guide lines, arrows, brackets, numbered badges | native PPT shapes |
| complex scientific art | text-free visual asset |
| 3D evidence pyramid / premium stairs | text-free base with editable overlay text, or high-fidelity native shapes if truly close |
| small meaningful medical icons | native line icons or clean text-free assets; never omit |

## 7. QA Gates

Fail V6.4 QA if:

- `topology_lock.json` or `visual_element_ledger.json` is missing
- the main topology is changed without explicit user approval
- a theme-similar generated asset does not preserve the reference sub-elements
- required small visuals are missing, such as IV bags, molecules, pumps, brackets, node rings, guide lines, or evidence icons
- text is editable but too small relative to the reference and weakens first-read hierarchy
- a premium visual loses depth, glow, gradient, or texture
- asset background mismatch remains visible

## 8. Polish Pass

Check:

- topology match before visual taste
- element ledger coverage before export
- font fullness and text occupancy against the reference
- connector direction, count, and endpoint plausibility
- no baked business text under editable overlays
- no missing small but semantically meaningful icons
