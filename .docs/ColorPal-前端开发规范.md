# ColorPal 前端开发规范

> **版本**：v1.0
> **技术栈**：Vue 3 + TypeScript + Vite 5 + Pinia
> **日期**：2026.05

---

## 1. 项目架构

```
frontend/
├── src/
│   ├── components/        # 通用组件
│   ├── views/             # 页面组件（路由级别）
│   ├── stores/            # Pinia 状态管理
│   ├── api/               # HTTP 请求封装
│   ├── router/            # 路由配置
│   ├── types/             # TypeScript 类型定义
│   ├── utils/             # 工具函数 & 常量
│   └── styles/            # 全局样式
├── public/vendor/         # 第三方运行时（Live2D 等）
└── package.json
```

---

## 2. 路由规范

**5 条路由，使用 `vue-router` 的懒加载 + `createWebHistory`**：

| 路径 | 名称 | 视图 | 说明 |
|------|------|------|------|
| `/` | `home` | `HomeView.vue` | 主页：登录/拍照/上传 |
| `/result` | `result` | `ResultView.vue` | 评分结果 |
| `/map` | `map` | `MapView.vue` | 色彩地图 |
| `/collection` | `collection` | `CollectionView.vue` | 颜色图鉴 |
| `/profile` | `profile` | `ProfileView.vue` | 个人资料/成就 |

---

## 3. 组件规范

### 3.1 Live2D 展示 — `PetDisplay.vue`

核心视觉组件，利用 PIXI.js + pixi-live2d-display 渲染 Cubism 2 模型。

**Props**：

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `pet` | `PetInfo` | — | 宠物数据（颜色、能量、心情等） |
| `size` | `PetDisplaySize` | `'hero'` | 尺寸：`'compact'` / `'hero'` / `'panel'` / `'avatar'` |
| `interactive` | `boolean` | `true` | 是否可交互（点击触发动作） |
| `event` | `PetDisplayEvent` | `'idle'` | 触发动画：`'idle'` / `'tap'` / `'feeding'` / `'success'` / `'evolve'` |
| `showStats` | `boolean` | `true` | 是否显示能量统计面板 |
| `offsetY` | `number` | `0.94` | 模型 Y 轴偏移比例（相对容器高度） |
| `modelPath` | `string` | `wanko` | Live2D 模型路径 |

**CSS 比例**：容器使用 `aspect-ratio: 0.74`，模型在 `fitModel()` 中按 `contain` 方式等比缩放。

### 3.2 聊天组件 — `AgentChatWidget.vue`

悬浮式对话框，通过 `localStorage` 持久化聊天记录，支持快速回复和降级兜底回复。

### 3.3 图鉴/成就锁定

未解锁项统一使用遮罩 + 锁图标：

- **色块变灰**，半透明白色遮罩 + `backdrop-filter: blur(2px)`
- **名称**显示 `???`
- **锁图标**用内联 SVG（组件内 `class="lock-icon"`），允许后续替换

---

## 4. 状态管理（Pinia）

| Store | 文件 | 职责 |
|-------|------|------|
| `palette` | `stores/palette.ts` | 已收集颜色列表、强调色计算；持久化到 `localStorage` |
| `pet` | `stores/pet.ts` | 宠物数据（能量、阶段、心情）、用户 Profile |
| `session` | `stores/session.ts` | 登录会话管理 |

---

## 5. 导航规范

- **桌面端**（>760px）：顶部固定导航栏，`backdrop-filter: blur(18px)` 毛玻璃效果
- **移动端**（≤760px）：底部圆点导航条，`backdrop-filter: blur(16px)`
- **手势**：移动端支持左右滑动切页（`touchstart` / `touchend` 监听）
- 导航项配置在 `App.vue` 的 `navItems` 数组中，共 3 项：主页 / 图鉴 / 我的

---

## 6. 样式规范

- **CSS 作用域**：一律使用 `<style scoped>`
- **CSS 变量**：主题色通过 `--accent-color` 传递，响应颜色变化
- **响应式断点**：
  - `760px`：移动端布局切换
  - `960px`：图鉴网格从 4 列降为 2 列
- **工具类命名**：小写 kebab-case（`page-shell`、`color-grid`、`pet-display`）

---

## 7. 颜色系统

36 色完整数据定义在 `utils/constants.ts`：

| 色系 | 数量 | 说明 |
|------|------|------|
| 红色系 | 6 | 常见 ×4 / 稀有 ×2 |
| 橙色系 | 4 | 常见 ×2 / 稀有 ×1 / 史诗 ×1 |
| 黄色系 | 5 | 常见 ×3 / 稀有 ×1 / 史诗 ×1 |
| 绿色系 | 6 | 常见 ×2 / 稀有 ×3 / 史诗 ×1 |
| 蓝色系 | 6 | 常见 ×3 / 稀有 ×2 / 史诗 ×1 |
| 紫色系 | 5 | 常见 ×2 / 稀有 ×2 / 史诗 ×1 |
| 无彩色 | 4 | 稀有 ×1 / 史诗 ×1 / 传说 ×2 |

**稀有度对应颜色**：

| 稀有度 | 颜色 |
|--------|------|
| 常见 | `#B2BEC3` |
| 稀有 | `#74B9FF` |
| 史诗 | `#A29BFE` |
| 传说 | `#FFD700` |

---

## 8. 成就系统

成就定义在 `utils/constants.ts` 的 `ALL_ACHIEVEMENTS` 数组，每个成就包含：

- `id` / `name` / `description` / `category` / `color` / `swatch`
- `swatch` 字段用于成就卡片左侧的色块展示（单色或 CSS 渐变）
- 成就分为 4 类：收集类 / 稀有度类 / 特殊组合 / 地点时间

---

## 9. 开发者模式

图鉴和成就页面各有一个 `Dev` 按钮，启用后：

- **图鉴**：显示所有颜色的真实色值、名称
- **成就**：解锁所有成就
- 仅前端展示，不影响实际数据

---

## 10. 构建与运行

```bash
npm install          # 安装依赖
npm run dev          # 本地开发（Vite HMR）
npm run build        # 生产构建（vue-tsc 类型检查 + Vite 打包）
npm run preview      # 预览生产构建
```

---

## 11. 命名约定

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件文件 | PascalCase | `PetDisplay.vue` |
| 视图文件 | PascalCase | `HomeView.vue` |
| Store | camelCase | `usePaletteStore` |
| 工具函数 | camelCase | `findClosestColor` |
| CSS 类 | kebab-case | `color-grid` |
| 常量 | UPPER_SNAKE | `ALL_COLORS` |
| 环境变量 | UPPER_SNAKE | `VITE_API_BASE` |
