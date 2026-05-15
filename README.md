# SKN Image2PPT

## 中文说明

SKN Image2PPT 是一个专门解决 **Image2 / AI 生图结果无法直接转成可编辑 PPT** 问题的 Codex skill 和重建协议。

很多 Image2、GPT 生图、PPT 截图或海报生成工具可以产出视觉效果很好的页面图片，但这些图片通常只是 PNG/JPEG：文字不能编辑，数字不能更新，表格、图标、标签和图表都被烘焙进像素里。直接把整张图贴进 PowerPoint 只能保留外观，不能满足后续修改；如果把所有元素都强行用 PPT 原生形状重画，又容易损失原图质感。

SKN Image2PPT 的核心思想是 **高保真混合重建**：

```text
复杂视觉资产高保真保留
+
核心业务内容可编辑重建
+
manifest / layout 驱动 PPT 生成
+
Polish Pass 最终精修
```

### 适用场景

- Image2 生成了一张 PPT 风格图片，需要变成真正的 `.pptx`。
- 只有 PPT 截图，但希望还原成可编辑 PPT。
- 需要把商业计划书、咨询页、医药 BP、路线图、战略页、信息图转成可维护 PPT。
- 希望保留原图视觉质感，同时让标题、数字、标签、要点、表格和图表标签可编辑。

### 处理原则

SKN Image2PPT 不追求“所有像素都可编辑”，而是按元素类型决策：

| 元素 | 推荐处理 |
| --- | --- |
| 标题、副标题、正文、要点 | PPT 可编辑文本 |
| 数字、标签、表格、图表标签 | PPT 文本 / 表格 / 图表 |
| 卡片、分割线、徽章、阶段条 | PPT 原生形状 |
| 简单图表 | 整体用 PPT/SVG/native chart 重建 |
| 飞轮、地图、机制图等复杂模块 | SVM 视觉底座 + 可编辑覆盖层 |
| Logo、纹理、插画、照片 | 高保真图片或 SVG 资产 |
| 背景光效、波浪 | 透明 PNG / SVG / 干净背景资产 |

### SVM 语义视觉模块

SVM 用于飞轮、地图、漏斗、机制图、复杂 timeline 等视觉复杂模块。它把复杂几何、渐变、阴影、遮挡关系保留为高保真视觉底座，再把业务文字、编号、标签作为可编辑 PPT 对象覆盖上去。

这样可以避免两个极端：

- 整页截图，完全不可编辑。
- 全部用 PPT shape 重画，视觉质量明显下降。

### Polish Pass 精修

V6.1 增加了 Polish Pass，用来处理初稿已经接近原图后仍然肉眼可见的小问题：

- 文字重影或底图文字残留
- 重复线条、重复圆点、重复图标
- 坐标、字号、行距轻微偏移
- 圆角、边框、阴影不统一
- 图标像 emoji 或占位符
- 背景资产有白底、硬边、矩形裁切感

Polish Pass 可以临时使用 30%-50% 透明度的 reference overlay 对照原图，但最终交付前必须隐藏或删除参考层。

## 生图模型策略

如果需要生成或清理组件图片、去文字背景、生成透明图标、生成 SVM 视觉底图，优先使用可明确指定模型的 OpenAI Images API，而不是依赖不透明的内置生图工具。

当前建议配置：

```json
{
  "generation_backend": "openai_images_api",
  "primary_model": "gpt-image-1.5",
  "chatgpt_alignment_model": "chatgpt-image-latest",
  "transparent_asset_strategy": "api_transparency_or_postprocess_alpha"
}
```

说明：

- Codex 内置 `imagegen` 不暴露模型选择，也不会返回后端模型名，所以只能在报告中标记为 `unknown_builtin_imagegen`。
- 截至 2026-05-15 官方文档检查，OpenAI 文档里的 GPT Image 模型包括 `gpt-image-1.5`、`gpt-image-1`、`gpt-image-1-mini` 等；不要在 skill 里硬写未确认的 `gpt-image-2`。
- 如果用户明确要求“image2”，应先核对当前官方模型列表，再决定是否切换 `image_model_config.example.json`。
- 透明素材优先使用 API 支持的透明输出；如果当前路径不支持，就用纯色/高对比背景生成，再做 alpha 或背景移除后处理。

### 典型输出

```text
project_slug/
  original_inputs/
  assets_v6/
    00_reference/
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

### 示例 Prompt

```text
使用 skn-image2ppt，把这张参考图转换成高保真、可编辑的 PPTX。
标题、数字、标签、要点、表格和图表标签必须保持可编辑。
复杂视觉模块可以保留为高保真视觉资产或 SVM 视觉底座。
如需生成或清理组件图片，优先使用 image_model_config.example.json 中定义的 OpenAI Images API 模型策略。
生成后执行 Polish Pass，清理重影、重复元素、对齐偏差、图标不统一和背景硬边问题。
输出 PPTX、资产文件夹、layout JSON、预览图、diff overlay 和 polish report。
```

---

## English

SKN Image2PPT is a Codex skill and reconstruction protocol for turning AI-generated slide images, PPT screenshots, posters, infographics, and other flat reference images into editable PowerPoint files.

It is designed for a common Image2 workflow problem: Image2 or other image-generation models can create visually strong slide images, but those images are not directly editable as PPT. SKN Image2PPT provides a hybrid method to preserve the visual quality of the generated image while rebuilding the business-critical content as editable PowerPoint objects.

## Core Idea

Do not choose between a static screenshot and a simplified editable redraw.

SKN Image2PPT uses a hybrid reconstruction approach:

- Complex visual modules are preserved as high-fidelity visual assets.
- Titles, numbers, labels, bullets, tables, and chart labels are rebuilt as editable PowerPoint objects.
- Layout and asset decisions are recorded in manifest/layout metadata.
- A final Polish Pass removes visible defects such as ghosting, duplicated lines, alignment drift, inconsistent icons, and hard-edged image assets.
- Generated assets use an explicit image model policy when OpenAI Images API access is available.

## Image Model Policy

For generated or cleaned component assets, prefer explicit OpenAI Images API configuration.

Recommended default:

- primary model: `gpt-image-1.5`
- ChatGPT-aligned option: `chatgpt-image-latest`, when available
- cost fallback: `gpt-image-1-mini`
- legacy fallback: `gpt-image-1`
- Codex built-in `imagegen`: fallback only, reported as `unknown_builtin_imagegen`

Do not hard-code `gpt-image-2` unless the current official OpenAI docs or target runtime explicitly expose that model.

## Status

This repository contains the skill instructions, protocol reference, and model configuration example. It is intended to be used by Codex or another capable agent that can inspect images, generate or extract assets, produce manifest/layout JSON, and build PowerPoint files.
