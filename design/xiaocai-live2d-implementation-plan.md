# 小彩 Live2D Demo 实施方案

## Summary

从 `source/dev` 同步后创建 `feat/live-2d`，实现 demo 展示版小彩：直接复用
`https://imuncle.github.io/live2d/` 的 20 号 `wanko` 模型，不改贴图、不重绘，只接入本地
Live2D 展示、基础互动和现有宠物状态。

## Key Changes

- Git：基于 `source/dev` 创建 `feat/live-2d`。
- 资源：将 model 20 的 `wanko.model.json`、贴图、动作文件放入
  `frontend/public/vendor/live2d/wanko/`，demo 不依赖远程模型地址。
- Runtime：前端接入 Cubism 2 加载能力，使用 `pixi.js` +
  `pixi-live2d-display/cubism2`，并提供所需 `live2d.min.js`。
- 组件：新增 `PetDisplay`，默认加载 model 20；支持 idle、点击、喂食、成功反馈动作。
- 页面：首页、结果页、个人页接入小彩展示，复用现有 `PetInfo` / `PetEnergy`，不改后端 API。
- 视觉：只增加轻量主色光晕、能量珠、色滴反馈，表达“吃颜色”的 demo 概念。

## Public Interfaces

- 新增模型配置：`defaultPetModel = '/vendor/live2d/wanko/wanko.model.json'`。
- 新增 `PetDisplay` props：
  - `pet: PetInfo`
  - `size?: 'compact' | 'hero' | 'panel'`
  - `interactive?: boolean`
  - `event?: 'idle' | 'tap' | 'feeding' | 'success' | 'evolve'`
- 不新增后端字段，不调整现有宠物数据结构。

## Test Plan

- 在 `frontend` 执行 `npm run build`。
- 浏览器验证首页、结果页、个人页能加载本地 Live2D。
- 验证点击动作、喂食/成功动作、加载失败兜底。
- 验证移动端布局、不同颜色/能量状态、无远程模型请求。

## Assumptions

- 当前版本只用于 demo 展示，不用于商业发布或正式上架。
- model 20 原样作为小彩 v1 本体。
- 生产发布前需要替换为授权明确或自有的 Live2D 模型资源。
