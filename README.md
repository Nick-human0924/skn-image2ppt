# SKN Image2PPT

## 中文说明

SKN Image2PPT 是一个专门解决 **Image2 / AI 生图结果无法直接转成可编辑 PPT** 问题的 Codex skill 和重建协议。

很多 Image2、GPT 生图、PPT 截图或海报生成工具可以产出视觉效果很好的页面图片，但这些图片通常只是 PNG/JPEG：文字不能编辑，数字不能更新，表格、图标、标签和图表都被烘焙进像素里。直接把整张图贴进 PowerPoint 只能保留外观，不能满足后续修改；如果把所有元素都强行用 PPT 原生形状重画，又容易损失原图质感。

SKN Image2PPT V6.5 的核心思想是 **拓扑保真 + 工程化 QA 的高保真混合重建**：

```text
RUN_ROOT 任务隔离
+
source_bbox 坐标契约
+
大模块结构化重建 / 高保真无字视觉底座
+
核心业务内容可编辑重建
+
图标可复制、可移动、可校验
+
字号按源图像素高度计算
+
placement overlay / visual diff / Polish Pass 最终精修
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
| 飞轮、地图、机制图、表格、卡片组等大模块 | 优先结构化重建；必要时使用干净视觉底座 + 可编辑覆盖层 |
| Logo、纹理、插画、照片 | 高保真图片或 SVG 资产 |
| 背景光效、波浪 | 透明 PNG / SVG / 干净背景资产 |

V6.5 明确禁止把大模块直接裁成图片来冒充重构，也针对实际测试中常见的三个问题增加硬门禁：图标不能复制、文字比原图小、排版错位。每个文本/图标/资产都必须记录源图像素级 `source_bbox`，再换算成 PPT 坐标。

### SVM 语义视觉模块

SVM 用于飞轮、地图、漏斗、机制图、复杂 timeline 等视觉复杂模块。V6.2 中 SVM 不是“裁图 fallback”，而是四种明确模式：

- `SVM_NATIVE`：表格、卡片组、流程、飞轮、证据阶梯等用 PPT 形状和可编辑文本重建。
- `SVM_CLEAN_BASE_PLUS_OVERLAY`：细胞、脂质体、肿瘤组织等复杂科学图只保留无文字底图，上层箭头、标签、编号全部可编辑。
- `SVM_ATOMIC_ASSET`：瓶身、logo、单个脂质体/细胞、医生插画等原子对象可保留为图像。
- `SVM_GENERATIVE_BASE`：当大科学图裁切会残缺、重影或比例失真时，先把图反向拆解成 prompt，生成无文字科学视觉底座，再叠加可编辑业务层。

这样可以避免两个极端：

- 整页截图，完全不可编辑。
- 全部用 PPT shape 重画，视觉质量明显下降。

### Engineering QA + Polish Pass

V6.5 的 Polish Pass 前先做 Engineering QA，不只处理小脏点，还要检查页面层级、比例、编号、图标系统、字号和坐标：

- 文字重影或底图文字残留
- 重复线条、重复圆点、重复图标
- 坐标、字号、行距轻微偏移
- 圆角、边框、阴影不统一
- 图标像 emoji 或占位符
- 背景资产有白底、硬边、矩形裁切感
- 第一视觉焦点被压低
- 页面过度规整但不高级
- 编号圆点、图标线宽、图标容器不统一
- 图标没有独立对象，无法复制/移动
- 文本字号来自缩略图坐标，导致比原图小
- `source_bbox` 和 `x/y/w/h` 坐标系不一致
- 预览图和源图没有 placement overlay / diff 对比

Polish Pass 可以临时使用 30%-50% 透明度的 reference overlay 对照原图，但最终交付前必须隐藏或删除参考层。

## 生图模型策略

如果需要生成或清理组件图片、去文字背景、生成透明图标、生成 SVM 科学视觉底图，优先使用可明确指定模型的 OpenAI Images API，而不是依赖不透明的内置生图工具。

V6.2 允许对脂质体、细胞结构、肿瘤组织、药物释放等大科学图做“反向拆解成 prompt 再生成”，但生成结果只能作为 **无文字视觉底座**；所有标签、箭头、数字、证据说明、结论必须回到 PPT 可编辑对象。

当前建议配置：

```json
{
  "generation_backend": "openai_images_api",
  "primary_model": "gpt-image-2",
  "chatgpt_alignment_model": "chatgpt-image-latest",
  "transparent_asset_strategy": "api_transparency_or_postprocess_alpha"
}
```

说明：

- Codex 内置 `imagegen` 不暴露模型选择，也不会返回后端模型名，所以只能在报告中标记为 `unknown_builtin_imagegen`。
- 截至 2026-05-15 官方文档检查，OpenAI 文档明确列出了 `gpt-image-2`、`gpt-image-1.5`、`gpt-image-1`、`gpt-image-1-mini` 等 GPT Image 模型。
- 主模型使用 `gpt-image-2`；如果目标运行时没有开放该模型，再降级到 `gpt-image-1.5`。
- `gpt-image-2` 当前不支持透明背景；透明素材使用支持透明的路径，或用纯色/高对比背景生成后做 alpha / 背景移除后处理。

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
      topology_lock.json
      visual_element_ledger.json
      icon_extraction_plan.json
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
      placement_source_overlay.png
      placement_preview_overlay.png
      side_by_side.png
      blend.png
      diff_overlay.png
      engineering_qa_report.json
      polish_report.md
      quality_report.md
```

### 示例 Prompt

```text
使用 skn-image2ppt V6.5，把这张参考图转换成高保真、可编辑的 PPTX。
标题、数字、标签、要点、表格和图表标签必须保持可编辑。
大模块必须结构化重建；不要直接裁成局部大图使用。
每个文本、图标和资产都记录 source_bbox；字号按源图实际像素高度换算，避免文字变小。
图标必须尽量独立成可复制/可移动对象；生成 icon_extraction_plan.json。
脂质体、细胞结构等复杂科学图可以反向拆解成 prompt，生成无文字视觉底座，再叠加可编辑标签、箭头和说明。
如需生成或清理组件图片，优先使用 image_model_config.example.json 中定义的 OpenAI Images API 模型策略。
生成后执行 Engineering QA：layout guard、placement overlay、visual diff、frame-anchor calibration，再执行 Polish Pass。
输出 PPTX、资产文件夹、layout JSON、预览图、side-by-side、diff overlay、engineering QA report 和 polish report。
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
- V6.5 adds engineering QA for source coordinate contracts, icon extraction, font sizing, placement overlays, and visual diff.

## Image Model Policy

For generated or cleaned component assets, prefer explicit OpenAI Images API configuration.

Recommended default:

- primary model: `gpt-image-2`
- ChatGPT-aligned option: `chatgpt-image-latest`, when available
- transparent asset fallback: `gpt-image-1.5` or alpha post-processing
- cost fallback: `gpt-image-1-mini`
- legacy fallback: `gpt-image-1`
- Codex built-in `imagegen`: fallback only, reported as `unknown_builtin_imagegen`

`gpt-image-2` is the preferred model when available, but it does not currently support transparent backgrounds.

## Status

This repository contains the skill instructions, protocol reference, and model configuration example. It is intended to be used by Codex or another capable agent that can inspect images, generate or extract assets, produce manifest/layout JSON, and build PowerPoint files.
