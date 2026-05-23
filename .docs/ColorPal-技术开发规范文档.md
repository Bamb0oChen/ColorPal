# ColorPal 技术开发规范文档

> **版本**：v1.0
> **适用对象**：全体开发成员
> **目标**：统一技术栈、规范代码风格、明确协作流程、预设突发应对

---

## 1. 文件架构

### 1.1 项目目录结构

```
colopal/
├── client/                          # 前端（微信小程序）
│   ├── app.js                       # 小程序入口
│   ├── app.json                     # 全局配置
│   ├── app.wxss                     # 全局样式
│   ├── project.config.json          # 项目配置
│   ├── sitemap.json                 # 搜索配置
│   │
│   ├── pages/                       # 页面
│   │   ├── home/                    # 首页（拍照 + 小人 + 任务）
│   │   │   ├── home.js
│   │   │   ├── home.wxml
│   │   │   ├── home.wxss
│   │   │   └── home.json
│   │   ├── result/                  # 评分结果页
│   │   │   ├── result.js
│   │   │   ├── result.wxml
│   │   │   ├── result.wxss
│   │   │   └── result.json
│   │   ├── map/                     # 地图页
│   │   │   ├── map.js
│   │   │   ├── map.wxml
│   │   │   ├── map.wxss
│   │   │   └── map.json
│   │   ├── collection/              # 图鉴页
│   │   │   ├── collection.js
│   │   │   ├── collection.wxml
│   │   │   ├── collection.wxss
│   │   │   └── collection.json
│   │   └── profile/                 # 个人页
│   │       ├── profile.js
│   │       ├── profile.wxml
│   │       ├── profile.wxss
│   │       └── profile.json
│   │
│   ├── components/                  # 公共组件
│   │   ├── pet-display/             # 小人展示组件
│   │   ├── score-card/              # 评分卡片组件
│   │   ├── task-bubble/             # 任务气泡组件
│   │   └── color-palette/           # 调色板展示组件
│   │
│   ├── services/                    # 服务层（API 封装）
│   │   ├── api.js                   # 通用请求封装
│   │   ├── photo.js                 # 照片相关 API
│   │   ├── user.js                  # 用户相关 API
│   │   └── task.js                  # 任务相关 API
│   │
│   ├── utils/                       # 工具函数
│   │   ├── color.js                 # 色彩工具（RGB/HSL 转换等）
│   │   ├── format.js                # 格式化工具
│   │   └── constants.js             # 常量定义
│   │
│   └── assets/                      # 静态资源
│       ├── images/
│       └── icons/
│
├── cloud/                           # 云开发
│   ├── functions/                   # 云函数
│   │   ├── analyzeColor/            # AI 颜色分析
│   │   │   ├── index.js
│   │   │   ├── prompt.js            # Prompt 模板
│   │   │   └── scoring.js           # 评分规则引擎
│   │   ├── userManager/             # 用户管理
│   │   │   └── index.js
│   │   ├── photoManager/            # 照片管理
│   │   │   └── index.js
│   │   └── taskManager/             # 任务管理
│   │       └── index.js
│   └── database/                    # 数据库
│       ├── schema.md                # 数据模型说明
│       └── init.js                  # 初始化脚本
│
├── docs/                            # 项目文档
│   ├── 产品需求文档.md
│   ├── 技术方案文档.md
│   └── 技术开发规范文档.md
│
├── scripts/                         # 工具脚本
│   └── compress-image.js            # 图片压缩脚本
│
├── .gitignore
├── README.md
└── package.json
```

### 1.2 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 目录名 | 小驼峰 | `petDisplay/`、`scoreCard/` |
| 页面目录 | 全小写 | `pages/home/`、`pages/result/` |
| JS 文件 | 小驼峰 | `home.js`、`colorUtils.js` |
| 组件 | 连字符 | `pet-display`、`score-card` |
| CSS 类名 | 连字符 | `.pet-container`、`.score-value` |
| 云函数 | 小驼峰 | `analyzeColor`、`userManager` |
| 图片资源 | 全小写连字符 | `pet-happy.png`、`icon-camera.svg` |

---

## 2. 主要技术栈

### 2.1 MVP 技术栈

| 层级 | 技术选型 | 版本 | 选型理由 |
|------|----------|------|----------|
| 前端框架 | 微信小程序原生 | — | 开箱即用、分享方便、生态成熟 |
| 地图组件 | 微信内置 map | — | 小程序原生支持，免配置 |
| 后端 | 微信云开发 | — | 与小程序无缝集成，无需运维 |
| 数据库 | 云数据库（MongoDB） | — | 灵活 Schema，适合 MVP |
| AI 视觉 | OpenAI GPT-4V API | gpt-4-vision-preview | 颜色提取 + 评分一次调用 |
| 图片存储 | 云存储 | — | 云开发配套 |
| 小人动画 | Lottie + SVG | lottie-miniprogram@1.x | 轻量动画方案 |

### 2.2 开发工具

| 工具 | 用途 |
|------|------|
| 微信开发者工具 | 小程序开发调试 |
| VSCode | 代码编辑 |
| Git + GitHub | 版本控制 |
| 飞书/钉钉 | 团队沟通 |

---

## 3. 代码规范与协作流程

### 3.1 通用编码规范

#### 缩进与格式
- 使用 **2 空格**缩进，不使用 Tab
- 行尾加分号
- 单行不超过 100 字符
- 文件末尾保留一个空行

#### 命名规范
- **变量/函数**：`camelCase`（小驼峰）
- **常量**：`UPPER_SNAKE_CASE`（全大写下划线）
- **类/构造函数**：`PascalCase`（大驼峰）
- **文件/目录**：遵循 1.2 节命名规范
- **布尔值**：用 `is` / `has` / `should` 前缀，如 `isLoading`、`hasPermission`

#### 注释规范
- 使用**中文注释**（团队沟通方便）
- 函数签名用 JSDoc 风格
- 不写「显而易见」的注释

```javascript
// ✅ 好的注释：解释为什么
// 压缩到 720px 宽度，平衡上传速度与颜色分析质量
const MAX_WIDTH = 720

// ❌ 不好的注释：解释是什么
// 设置最大宽度为 720
const MAX_WIDTH = 720
```

### 3.2 JavaScript 规范

```javascript
// ============ 变量声明 ============
// 优先用 const，只有确定会重新赋值才用 let
const energy = calculateEnergy(score)
let currentTaskId = null

// 解构赋值
const { dominantColor, palette, score } = analysisResult
const [primary, ...rest] = palette

// ============ 函数 ============
// 箭头函数优先
const formatScore = (score) => {
  return Math.min(100, Math.max(0, score))
}

// 异步函数用 async/await
const analyzePhoto = async (imageUrl) => {
  const result = await callAI(imageUrl)
  return validateResult(result)
}

// ============ 对象 ============
// 简写属性
const color = { dominantColor, palette, score }

// 可选链
const comment = result?.analysis?.comment ?? '暂无评价'

// ============ 条件判断 ============
// 早期返回
const getPetMood = (avgScore) => {
  if (avgScore >= 70) return 'happy'
  if (avgScore >= 40) return 'neutral'
  return 'sad'
}
```

### 3.3 微信小程序规范

```javascript
// Page 定义
Page({
  // 数据集中放在 data 顶部
  data: {
    petInfo: null,
    scoreCard: null,
    isLoading: false,
  },

  // 生命周期靠前
  onLoad() {
    this.initData()
  },

  // 自定义方法用小驼峰
  async initData() {
    this.setData({ isLoading: true })
    try {
      const profile = await getUserProfile()
      this.setData({ petInfo: profile.pet })
    } finally {
      this.setData({ isLoading: false })
    }
  },

  // 事件处理函数用 handle 前缀
  handleTakePhoto() {
    wx.chooseMedia({
      success: (res) => this.uploadPhoto(res.tempFilePath),
    })
  },
})
```

### 3.4 云函数规范

```javascript
// 云函数结构：统一使用 exports.main
const cloud = require('wx-server-sdk')
cloud.init()

const ERROR_CODES = {
  INVALID_INPUT: 400,
  AI_TIMEOUT: 502,
  NOT_FOUND: 404,
}

exports.main = async (event, context) => {
  const { action, data } = event

  switch (action) {
    case 'analyze':
      return await handleAnalyze(data)
    case 'detail':
      return await handleDetail(data)
    default:
      return { code: ERROR_CODES.INVALID_INPUT, message: '未知操作' }
  }
}
```

### 3.5 Git 协作流程

#### 分支策略

```
main         ← 稳定版本，可演示
  └── dev    ← 开发分支，所有人合并到此
       ├── feat/camera        ← A 前端的特性分支
       ├── feat/ai-analyze    ← B 算法的特性分支
       ├── feat/user-api      ← C 后端的特性分支
       └── docs/readme        ← D 产品的文档分支
```

#### Commit 规范

```
<type>: <简短中文描述>

# type 类型
feat:    新功能
fix:     修复 Bug
docs:    文档变更
refactor: 重构
style:   代码格式（不影响功能）
chore:   构建/配置变更
```

示例：
```
feat: 拍照后调用 AI 分析并展示评分卡片
fix: 能量槽满后进化按钮未及时亮起
docs: 更新 API 接口文档
```

#### 提交流程

```
1. git pull origin dev          # 拉取最新代码
2. git checkout -b feat/xxx     # 创建特性分支
3. [写代码]
4. git add <文件>                # 按文件添加，不用 git add .
5. git commit -m "feat: xxx"    # 写规范的 commit message
6. git push origin feat/xxx     # 推送
7. → PR → 至少 1 人 Review → 合入 dev
```

#### Code Review 要点

- 检查是否有**硬编码**（token、URL 等）
- 检查**异常处理**是否遗漏（API 失败、用户取消、权限拒绝）
- 检查**命名**是否符合规范
- 检查是否有**未使用的变量或 import**

---

## 4. 突发预警策略

### 4.1 风险分级响应

| 级别 | 定义 | 响应措施 |
|------|------|----------|
| 🔴 **P0 致命** | 核心闭环断裂（拍照→评分→小人无反馈） | 全员暂停手头工作，集中修复 |
| 🟡 **P1 严重** | 某核心功能不可用（任务/图鉴/地图） | 负责人 + 1 人协助，2h 内解决 |
| 🟢 **P2 一般** | 体验问题（动画卡顿、文案错误） | 记录到 issue，排在核心功能后修复 |

### 4.2 典型突发场景与应对

#### 场景 1：视觉 API 超时或不可用 🔴

```
表现：拍照后一直 loading，没有评分结果返回
影响：核心闭环断裂（P0 致命）

响应：
  1. 云函数设置 8s 超时，超时后自动走兜底规则评分
  2. 兜底评分只需计算 HSL + 色彩丰富度，不依赖外部 API
  3. 前端 5s 无返回时展示「AI 思考中」动画，而不是空白
  
预防：
  - B 需在阶段二完成兜底规则评分函数
  - 上线前测试 API 降级路径
```

#### 场景 2：图片上传太慢 🟡

```
表现：用户拍照后等待超过 5s 才进入评分
影响：体验差（P1 严重）

响应：
  1. 前端拍照后立即在前端压缩图片（720px 宽，80% 质量）
  2. 压缩后 < 200KB 再上传
  3. 上传与 AI 分析并行：上传的同时就调用分析接口
  
预防：
  - A 需在拍照功能中内置压缩逻辑
```

#### 场景 3：评审现场网络不佳 🔴

```
表现：演示时 API 调不通
影响：演示失败（P0 致命）

响应：
  1. 手机本地预存 5 张测试照片（覆盖高/中/低分场景）
  2. 预存分析结果在本地缓存
  3. 准备离线演示视频（3 分钟）作为备用方案
  
预防：
  - D 在提交前录制好演示视频
```

#### 场景 4：成员进度严重滞后 🟡

```
表现：某成员预估工时超 50% 仍未完成
影响：影响联调（P1 严重）

响应：
  1. 该成员立即通报 team，不隐瞒
  2. PM 判断：砍掉非核心功能 / 调人协助 / 降低实现复杂度
  3. 如果 A（前端）滞后 → C（后端）协助前端写页面
  4. 如果 B（AI）滞后 → 切换到纯规则评分
  5. 如果 C（后端）滞后 → 砍图鉴/地图 API，前端硬编码演示数据
  6. 如果 D（产品）滞后 → 全员协助海报/文档
```

#### 场景 5：Git 冲突或代码丢失 🟡

```
表现：合并时大量冲突或误删代码
影响：浪费时间（P1 严重）

响应：
  1. 不要惊慌，不要 git push --force
  2. 用 git stash / git merge --abort 回退到安全状态
  3. 通知 team，协商合并策略
  4. 必要时找熟悉 Git 的人协助

预防：
  - 每人建自己的特性分支，不在 dev 上直接改
  - commit 频繁一些，少而精
```

### 4.3 紧急联系

```
遇到 P0 问题 → 群里 @所有人 + 电话
遇到 P1 问题 → 群里 @责任人
遇到 P2 问题 → 记录 issue，下次迭代修
```

---

## 5. AI 示例参考（规范代码风格）

> 以下示例供团队成员参考，也作为 AI 辅助编程时提供给 AI 的 prompt，确保 AI 生成风格一致的代码。

### 5.1 给 AI 的风格指令

```text
请按照以下风格生成代码：

- 语言：JavaScript
- 缩进：2 空格
- 命名：变量/函数用小驼峰，常量用大写下划线，组件用大驼峰
- 异步：使用 async/await
- 分号：行尾加分号
- 注释：用中文，解释「为什么」而非「是什么」
- 早返回：条件判断优先早期返回
- 解构：优先使用解构赋值
- 字符串：使用单引号
- 最长单行限制：100 字符
- 错误处理：try/catch 捕获，错误信息用中文
```

### 5.2 示例：颜色工具类

```javascript
/**
 * 色彩工具函数
 * 提供颜色转换、评分计算等基础能力
 */

// ============ 常量 ============
const HEX_REGEX = /^#([0-9a-fA-F]{6})$/
const SCORE_THRESHOLDS = {
  HIGH: 70,
  MEDIUM: 40,
}

// ============ 颜色转换 ============

/**
 * 将 HEX 色值转为 RGB 对象
 * @param {string} hex - 如 '#FF6B6B'
 * @returns {{ r: number, g: number, b: number }}
 */
const hexToRgb = (hex) => {
  const match = hex.match(HEX_REGEX)
  if (!match) return { r: 0, g: 0, b: 0 }

  const value = parseInt(match[1], 16)
  return {
    r: (value >> 16) & 255,
    g: (value >> 8) & 255,
    b: value & 255,
  }
}

/**
 * 将 RGB 转为 HSL 对象
 * HSL 用于计算色彩属性（色调、饱和度、亮度）
 */
const rgbToHsl = (r, g, b) => {
  r /= 255
  g /= 255
  b /= 255

  const max = Math.max(r, g, b)
  const min = Math.min(r, g, b)
  const delta = max - min

  let h = 0
  let s = 0
  const l = (max + min) / 2

  if (delta !== 0) {
    s = l > 0.5 ? delta / (2 - max - min) : delta / (max + min)

    switch (max) {
      case r: h = ((g - b) / delta + (g < b ? 6 : 0)) * 60; break
      case g: h = ((b - r) / delta + 2) * 60; break
      case b: h = ((r - g) / delta + 4) * 60; break
    }
  }

  return { h: Math.round(h), s: Math.round(s * 100), l: Math.round(l * 100) }
}

// ============ 评分计算 ============

/**
 * 基于色彩理论计算分数（兜底方案）
 * AI 不可用时使用此函数
 *
 * @param {number} saturation - 饱和度 0-100
 * @param {number} brightness - 亮度 0-100
 * @param {number} colorCount - 色彩丰富度 0-100
 * @returns {number} 0-100
 */
const calculateScore = (saturation, brightness, colorCount) => {
  const SAT_WEIGHT = 0.4
  const BRI_WEIGHT = 0.3
  const VAR_WEIGHT = 0.3

  const score = saturation * SAT_WEIGHT
    + brightness * BRI_WEIGHT
    + colorCount * VAR_WEIGHT

  return Math.min(100, Math.max(0, Math.round(score)))
}

/**
 * 获取小人心情状态
 * 基于最近 5 张照片的平均分
 */
const getPetMood = (averageScore) => {
  if (averageScore >= SCORE_THRESHOLDS.HIGH) return 'happy'
  if (averageScore >= SCORE_THRESHOLDS.MEDIUM) return 'neutral'
  return 'sad'
}

// ============ 导出 ============
module.exports = {
  hexToRgb,
  rgbToHsl,
  calculateScore,
  getPetMood,
}
```

### 5.3 示例：AI 分析云函数

```javascript
/**
 * AI 颜色分析云函数
 *
 * 流程：接收图片 URL → 调用 GPT-4V → 解析结果 → 校验 → 返回
 * 降级：GPT-4V 超时或不可用时 → 走兜底规则评分
 */

const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })
const db = cloud.database()

// 导入 Prompt 模板
const { SYSTEM_PROMPT, USER_PROMPT } = require('./prompt')
const { calculateScore } = require('./scoring')

const TIMEOUT_MS = 8000

exports.main = async (event, context) => {
  const { imageUrl } = event

  // 校验入参
  if (!imageUrl) {
    return { code: 400, message: '缺少图片 URL' }
  }

  try {
    // 主路径：调用 AI 分析
    const aiResult = await callAIWithTimeout(imageUrl, TIMEOUT_MS)
    const validated = validateAnalysis(aiResult)

    return {
      code: 0,
      data: validated,
      source: 'ai',
    }
  } catch (err) {
    console.error('[analyzeColor] AI 分析失败，切换到兜底评分:', err.message)

    // 降级路径：规则评分
    const fallback = await fallbackScoring(imageUrl)

    return {
      code: 0,
      data: fallback,
      source: 'fallback',
    }
  }
}

/**
 * 调用 GPT-4V 分析图片
 * 超时后自动中断
 */
const callAIWithTimeout = async (imageUrl, timeoutMs) => {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeoutMs)

  try {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
      },
      body: JSON.stringify({
        model: 'gpt-4-vision-preview',
        messages: [
          { role: 'system', content: SYSTEM_PROMPT },
          {
            role: 'user',
            content: [
              { type: 'text', text: USER_PROMPT },
              { type: 'image_url', image_url: { url: imageUrl } },
            ],
          },
        ],
        max_tokens: 500,
      }),
      signal: controller.signal,
    })

    const json = await response.json()
    const content = JSON.parse(json.choices[0].message.content)
    return content
  } finally {
    clearTimeout(timer)
  }
}

/**
 * 校验 AI 返回结果
 * 确保字段完整、数值合法
 */
const validateAnalysis = (data) => {
  const score = typeof data.score === 'number'
    ? Math.min(100, Math.max(0, Math.round(data.score)))
    : 50

  const dominantColor = HEX_REGEX.test(data.dominant_color)
    ? data.dominant_color
    : '#CCCCCC'

  return {
    dominant_color: dominantColor,
    palette: Array.isArray(data.palette) ? data.palette.slice(0, 5) : [],
    score,
    comment: data.comment || '色彩分析完成',
    color_category: ['warm', 'cool', 'neutral'].includes(data.color_category)
      ? data.color_category
      : 'neutral',
    saturation_level: ['high', 'medium', 'low'].includes(data.saturation_level)
      ? data.saturation_level
      : 'medium',
    brightness_level: ['high', 'medium', 'low'].includes(data.brightness_level)
      ? data.brightness_level
      : 'medium',
  }
}
```

### 5.4 示例：API 服务封装

```javascript
/**
 * API 服务封装
 * 统一处理请求、错误、loading 状态
 */

const BASE_URL = 'https://api.colopal.app'

/**
 * 通用请求封装
 * 自动处理错误提示和 loading
 */
const request = async (options) => {
  const { url, method = 'GET', data, showLoading = true } = options

  if (showLoading) {
    wx.showLoading({ title: '加载中...', mask: true })
  }

  try {
    const response = await new Promise((resolve, reject) => {
      wx.request({
        url: `${BASE_URL}${url}`,
        method,
        data,
        success: resolve,
        fail: reject,
        timeout: 10000,
      })
    })

    if (response.statusCode !== 200) {
      throw new Error(`请求失败: ${response.statusCode}`)
    }

    return response.data
  } catch (err) {
    wx.showToast({ title: '网络开小差了', icon: 'none' })
    throw err
  } finally {
    if (showLoading) {
      wx.hideLoading()
    }
  }
}

// ============ 导出具体 API ============

const uploadPhoto = async (filePath, location) => {
  const result = await wx.cloud.uploadFile({
    cloudPath: `photos/${Date.now()}.jpg`,
    filePath,
  })

  return request({
    url: '/photo/analyze',
    method: 'POST',
    data: { imageUrl: result.fileID, location },
  })
}

const getUserProfile = async () => {
  return request({ url: '/user/profile' })
}

const getCurrentTask = async () => {
  return request({ url: '/tasks/current' })
}

module.exports = {
  uploadPhoto,
  getUserProfile,
  getCurrentTask,
}
```

### 5.5 示例：页面编写规范

```javascript
// pages/home/home.js
// 首页：拍照入口 + 小人展示 + 任务气泡

const { uploadPhoto } = require('../../services/photo')
const { getCurrentTask } = require('../../services/task')

Page({
  data: {
    petInfo: null,
    currentTask: null,
    isLoading: false,
  },

  onLoad() {
    this.loadHomeData()
  },

  onShow() {
    // 从其他页面返回时刷新数据
    if (this.data.petInfo) {
      this.loadHomeData()
    }
  },

  async loadHomeData() {
    this.setData({ isLoading: true })

    try {
      const [profile, task] = await Promise.all([
        getUserProfile(),
        getCurrentTask(),
      ])

      this.setData({
        petInfo: profile.pet,
        currentTask: task,
      })
    } catch (err) {
      console.error('[home] 加载首页数据失败:', err)
    } finally {
      this.setData({ isLoading: false })
    }
  },

  // 点击拍照按钮
  handleTakePhoto() {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['camera', 'album'],
      success: (res) => this.navigateToResult(res.tempFiles[0].tempFilePath),
      fail: () => {
        wx.showToast({ title: '取消拍照', icon: 'none' })
      },
    })
  },

  // 跳转到评分结果页
  navigateToPhotoResult(tempFilePath) {
    wx.navigateTo({
      url: `/pages/result/result?image=${encodeURIComponent(tempFilePath)}`,
    })
  },
})
```

### 5.6 示例：CSS 规范

```css
/* 使用统一的间距和颜色变量 */
page {
  --color-primary: #FF6B6B;
  --color-secondary: #4ECDC4;
  --color-bg: #F8F9FA;
  --color-text: #333333;
  --color-text-light: #999999;
  --spacing-sm: 8rpx;
  --spacing-md: 16rpx;
  --spacing-lg: 32rpx;
  --radius-sm: 8rpx;
  --radius-md: 16rpx;
  --radius-lg: 24rpx;
}

/* 类名用连字符 */
.pet-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--spacing-lg);
}

.score-value {
  font-size: 48rpx;
  font-weight: 700;
  color: var(--color-primary);
}

/* 状态样式用独立类 */
.is-loading {
  opacity: 0.6;
  pointer-events: none;
}

.is-hidden {
  display: none;
}
```

---

## 附录：开发环境准备清单

- [ ] 安装微信开发者工具
- [ ] 注册微信小程序 AppID
- [ ] 开通微信云开发
- [ ] 申请 OpenAI API Key
- [ ] 安装 Git 并配置 SSH
- [ ] 克隆仓库：`git clone <repo-url>`
- [ ] 安装依赖：`npm install`
- [ ] 确认云环境 ID 已配置
