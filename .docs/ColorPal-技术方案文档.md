# ColorPal 技术方案文档

> **项目代号**：ColorPal
> **版本**：v2.0（两层架构）
> **日期**：2026.05
> **目标**：25 小时 MVP 开发
> **受众**：开发团队

> 详细的代码规范、目录结构、命名约定见同级 [技术开发规范文档](./ColorPal-技术开发规范文档.md)。

---

## 1. 系统架构总览

```
┌─────────────────────────────┐         HTTP         ┌────────────────────────────┐
│  Vue 3 前端 (Web App)        │ ──────────────────→  │  FastAPI 后端              │
│  ┌────────┐ ┌────────┐      │                      │  ┌──────────┐ ┌─────────┐ │
│  │拍照/相册│ │小人展示│      │ ←──────────────────  │  │路由层    │ │业务服务 │ │
│  └────────┘ └────────┘      │                      │  └──────────┘ └────┬────┘ │
│  ┌────────┐ ┌────────┐      │                      │  ┌──────────────┐  │      │
│  │地图页  │ │图鉴/成就│      │                      │  │SQLAlchemy ORM│  │      │
│  └────────┘ └────────┘      │                      │  └──────┬───────┘  │      │
│  Axios 调用层                │                      └─────────┼──────────┼──────┘
└─────────────────────────────┘                                │          │
                                                               ▼          ▼
                                                         ┌──────────┐ ┌────────────┐
                                                         │ SQLite   │ │ GPT-4V API │
                                                         │ (本地文件)│ │ + HSL 兜底 │
                                                         └──────────┘ └────────────┘
```

**关键链路**：浏览器 → FastAPI（同进程内完成 AI 调用 + 兜底 + 持久化）→ 返回评分 & 能量变化。所有外部依赖（OpenAI、地图）由后端封装，前端只看一个域名。

---

## 2. 技术选型

### 2.1 MVP 技术栈

| 层次 | 方案 | 理由 |
|------|------|------|
| 前端框架 | Vue 3 + Vite + TypeScript | 团队最熟悉，生态成熟，移动端浏览器兼容好 |
| 状态管理 | Pinia | Vue 3 官方推荐，类型友好 |
| 视觉模型 | GPT-4V | 一次调用同时完成颜色提取+评分 |
| 兜底评分 | HSL + Pillow 本地计算 | 不依赖外部网络，AI 失败时秒级返回 |
| 后端 | FastAPI（Python 3.11） | AI 与持久化同进程，避免跨服务对齐成本 |
| 数据库 | SQLite + SQLAlchemy 2.0 异步 | 零运维、单文件、可随仓库迁移；上量再换 Postgres |
| 地图 | Leaflet | 纯前端库、轻量，不需要 token |
| 小人动画 | Lottie / SVG + CSS 换色 | 轻量，避免复杂的骨骼动画 |
| 部署 | Docker Compose | 演示当天一行命令拉起前后端 |

### 2.2 备选方案

| 场景 | 主方案 | 备选方案 | 切换条件 |
|------|--------|----------|----------|
| 视觉模型 | GPT-4V | Claude Vision / Gemini Vision | API 成本或响应速度不达标 |
| 颜色评分 | AI + HSL 兜底 | 纯 HSL 规则 | OpenAI key 不可用 / 完全离线演示 |
| 数据库 | SQLite | PostgreSQL（Docker 容器） | 需要并发写入或上线长期运行 |
| 地图 | Leaflet | Mapbox GL JS | 需要矢量瓦片或自定义样式 |
| 前端形态 | 浏览器 Web App | PWA（manifest + service worker） | 需要「装到桌面」体验 |

---

## 3. 开发阶段划分

```
阶段一 (4h) ─── 阶段二 (8h) ─── 阶段三 (8h) ─── 阶段四 (5h)
  地基搭建       核心闭环        体验补全        打磨收尾
```

### 阶段一：地基搭建（预估 4 小时）

**目标**：跑通最小技术链路，验证可行性

| 步骤 | 任务 | 负责人 | 产出 |
|------|------|--------|------|
| 1.1 | 搭建 Vue + Vite + TS 前端工程，跑通 Tab 路由骨架 | 前端 | 可运行的空壳 App |
| 1.2 | 搭建 FastAPI 工程 + SQLAlchemy + 健康检查接口 | 后端 | `/api/v1/health` 200 |
| 1.3 | 申请 OpenAI API Key，测试 GPT-4V 单张调用 | 后端/AI | 确认 API 可用 |
| 1.4 | 建表（users、photos、collections、tasks）+ 初始迁移脚本 | 后端 | 可用的 SQLite 文件 |
| 1.5 | docker-compose.yml 一键拉前后端，确认前端能调通后端 | 全员 | 端到端 hello world |

**阶段一完成标志**：`docker compose up` 后，前端能调通 `/api/v1/health`，FastAPI 能成功调一次 GPT-4V，SQLite 表结构齐全。

### 阶段二：核心闭环（预估 8 小时）

**目标**：跑通「拍照 → 评分 → 小人变化」的核心循环

| 步骤 | 任务 | 负责人 | 前置依赖 |
|------|------|--------|----------|
| 2.1 | 实现 `<input type="file" capture>` 拍照/相册选取 + 客户端压缩 | 前端 | 1.1 |
| 2.2 | 编写 GPT-4V Prompt，封装 `analyze_image()` 服务 | 后端/AI | 1.3 |
| 2.3 | 编写 HSL 兜底评分 `fallback_score()` + Pydantic 后处理校验 | 后端/AI | 2.2 |
| 2.4 | 实现小人能量更新逻辑（RGB 三维向量 + 心情计算） | 后端 | 1.4 |
| 2.5 | 前端拍照 → POST /photo/analyze → 评分卡片渲染 | 前端 | 2.1, 2.3 |
| 2.6 | 前端 PetDisplay 组件（SVG 换色 + 能量条） | 前端 | 2.4 |
| 2.7 | 联调：拍照 → API → 评分 → 小人变化 全链路 | 前后端 | 2.5, 2.6 |

**阶段二完成标志**：用户拍照后，完整跑通评分展示 + 小人颜色/心情变化。

### 阶段三：体验补全（预估 8 小时）

**目标**：补齐任务系统、图鉴、地图、分享功能

| 步骤 | 任务 | 负责人 | 前置依赖 |
|------|------|--------|----------|
| 3.1 | 实现任务系统（任务模板 + 触发 + 完成任务逻辑） | 后端 | 2.4 |
| 3.2 | 前端任务气泡 UI 展示 | 前端 | 3.1 |
| 3.3 | 实现图鉴系统（颜色记录 + 分类展示） | 后端 | 1.4 |
| 3.4 | 前端图鉴页面（解锁颜色网格展示） | 前端 | 3.3 |
| 3.5 | 拍照时获取地理位置 + 存储 | 前后端 | 2.1 |
| 3.6 | 前端地图页（彩色标记点展示） | 前端 | 3.5 |
| 3.7 | 实现分享功能（生成分享图） | 前端 | — |
| 3.8 | 实现小人进化逻辑（条件判断 + 形态切换） | 后端 | 2.4 |

**阶段三完成标志**：任务可触发可完成，图鉴可查看，地图有标记点，可分享。

### 阶段四：打磨收尾（预估 5 小时）

**目标**：修 bug、优化体验、录制演示视频

| 步骤 | 任务 | 负责人 |
|------|------|--------|
| 4.1 | UI 细节打磨（动画过渡、loading 态、空态、错误态） | 前端 |
| 4.2 | 异常处理（网络错误、API 超时、相册权限拒绝等） | 前后端 |
| 4.3 | 性能优化（图片压缩、缓存策略） | 前后端 |
| 4.4 | 准备演示数据（预设几张高/低分测试图） | 全员 |
| 4.5 | 录制 3 分钟演示视频 | 全员 |
| 4.6 | 代码上传 GitHub，写 README | 全员 |
| 4.7 | 打包提交 | 全员 |

---

## 4. 数据模型设计

> 以下数据形态以 JSON 描述（贴近 Pydantic schema 的输出形状）。SQLAlchemy ORM 模型中，`pet`、`stats` 等嵌套对象拆成同表的列或独立的 `user_pet` / `user_stats` 表均可，由后端实现侧自行选择，但对外 JSON 形状以此处为准。

### 4.1 用户表（users）

```json
{
  "_id": "user_id",
  "nickname": "string",
  "avatar": "string (url)",
  "pet": {
    "name": "string",
    "stage": 0,            // 0=幼年, 1=成长, 2=成熟, 3=稀有
    "mood": "happy",       // happy / neutral / sad
    "color": "#FF6B6B",    // 当前主色调
    "energy": {
      "current": 150,
      "max": 300,
      "r": 50,             // 红色能量积累
      "g": 60,             // 绿色能量积累
      "b": 40              // 蓝色能量积累
    }
  },
  "stats": {
    "total_photos": 42,
    "total_score": 3120,
    "highest_score": 92,
    "streak_days": 3,
    "last_photo_at": "2026-05-23T10:30:00Z"
  },
  "created_at": "2026-05-20T08:00:00Z",
  "updated_at": "2026-05-23T10:30:00Z"
}
```

### 4.2 照片记录表（photos）

```json
{
  "_id": "photo_id",
  "user_id": "user_id",
  "image_url": "string",
  "thumbnail_url": "string",
  "analysis": {
    "dominant_color": "#FF6B6B",
    "palette": ["#FF6B6B", "#4ECDC4", "#FFE66D", "#95E1D3", "#F38181"],
    "score": 78,
    "comment": "这个蓝橙互补色很高级",
    "color_category": "warm",     // warm / cool / neutral
    "saturation_level": "high",   // high / medium / low
    "brightness_level": "medium"
  },
  "location": {
    "lat": 30.2672,
    "lng": 120.1528,
    "place_name": "西湖断桥",
    "place_type": "park"          // park / street / gallery / cafe / other
  },
  "task_id": "optional",
  "taken_at": "2026-05-23T10:30:00Z",
  "shared": false
}
```

### 4.3 图鉴表（collections）

```json
{
  "_id": "collection_id",
  "user_id": "user_id",
  "type": "color",               // color / location / special
  "unlocked_colors": [
    {
      "hex": "#FF6B6B",
      "name": "珊瑚红",
      "unlocked_at": "2026-05-23T10:30:00Z",
      "photo_id": "ref"
    }
  ],
  "unlocked_combos": [
    {
      "name": "蓝橙互补",
      "colors": ["#4ECDC4", "#FF6B6B"],
      "unlocked_at": "2026-05-23T10:30:00Z"
    }
  ],
  "unlocked_locations": [
    {
      "type": "park",
      "name": "西湖断桥",
      "unlocked_at": "2026-05-23T10:30:00Z"
    }
  ]
}
```

### 4.4 任务表（tasks）

```json
{
  "_id": "task_id",
  "type": "color_collect",       // color_collect / combo / streak / location / time / community
  "title": "我想看红色的东西",
  "description": "拍一张以红色为主色调的照片",
  "target_color": "#FF0000",
  "target_category": "warm",
  "target_location_type": "park",
  "reward": {
    "energy_bonus": 50,
    "special_color": null,
    "evolution_item": null
  },
  "status": "active",            // active / completed / expired
  "assigned_to": "user_id",
  "assigned_at": "2026-05-23T10:00:00Z",
  "completed_at": null
}
```

---

## 5. AI 视觉模型集成

### 5.1 Prompt 设计（核心）

```text
你是一位专业的色彩分析师。分析这张照片，输出 JSON 格式结果：

{
  "dominant_color": "#FF6B6B",
  "palette": ["#FF6B6B", "#4ECDC4", "#FFE66D", "#95E1D3", "#F38181"],
  "color_category": "warm|cool|neutral",
  "saturation_level": "high|medium|low",
  "brightness_level": "high|medium|low",
  "score": 78,
  "comment": "一个简短的色彩评价（中文，10-20字）",
  "tags": ["日落", "暖色调", "高饱和度"]
}

评分规则（0-100分）：
- 60-100：色彩搭配协调，有明确的配色思路
- 30-59：色彩普通，但有一定可看性
- 0-29：色彩灰暗、单调或过度曝光

打分依据：
1. 互补色/对比色使用（+20分）
2. 色彩饱和度适中（+15分）
3. 亮度分布合理（+15分）
4. 色彩数量丰富但不杂乱（+20分）
5. 整体色彩和谐度（+30分）
```

### 5.2 后处理逻辑

AI 返回原始结果后，需要在服务端做后处理：

```
输入：AI 返回的 JSON
处理：
  1. 校验 score 是否在 0-100 范围，越界则 clamp
  2. 校验 dominant_color 是否合法 hex
  3. 如果 score 缺失 → 用规则公式计算兜底
输出：校验/修正后的颜色数据
```

### 5.3 兜底规则评分（AI 不可用时）

当视觉 API 不可用或超时时，使用基础色彩公式兜底：

```
score = (饱和度评分 × 0.4) + (亮度评分 × 0.3) + (色彩丰富度 × 0.3)

饱和度评分 = 计算 HSL 中 S 通道均值，归一化到 0-100
亮度评分 =  计算 HSL 中 L 通道均值，归一化到 0-100（避开过暗/过亮）
色彩丰富度 = 将图片缩放到 8×8，统计不同颜色的数量，归一化到 0-100
```

---

## 6. 关键模块实现详述

### 6.1 拍照 → 评分流程（最核心链路）

```
用户点击拍照
  → <input type="file" capture="environment"> 触发系统相机
  → 前端 canvas 压缩到 720px / 80% 质量
  → POST /api/v1/photo/analyze (multipart/form-data) 到 FastAPI
    → FastAPI 路由层校验图片格式
    → services/ai_analyzer.analyze_image() 调 GPT-4V (8s 超时)
      ↳ 超时/异常时切换 services/scorer.fallback_score()
    → Pydantic 校验返回值（hex/score 范围）
    → SQLAlchemy 写 photos 表
    → services/pet_state.apply_energy_gain() 更新 users.pet.energy
  → 返回 PhotoAnalysisResponse
  → 前端展示评分卡片 + Pinia 更新小人状态
```

**时间预算**：
- 图片上传：1-3s（取决于图片大小，需要做压缩）
- AI 分析：2-5s（GPT-4V 响应时间）
- 总耗时：3-8s → 需要 loading 动画

### 6.2 小人状态管理

小人状态由 RGB 三个能量维度驱动：

```
能量槽是一个三维向量 (R, G, B)：
- 每次拍照后，主色调的 RGB 分量按比例累加到能量槽
- 例如主色调 #FF6B6B = R:255, G:107, B:107
  → 能量增加：R+25, G+10, B+10（归一化后）

小人外观变化：
- 颜色：取 (R, G, B) 能量占比最大的通道作为主色
- 形态：能量总量达到阈值触发进化
- 心情：最近 5 张照片的平均分决定
  - ≥70 → happy
  - 40-69 → neutral
  - <40 → sad

进化触发条件：
  energy.current >= energy.max  (能量槽满)
  AND 已解锁指定颜色组合
  AND 已完成指定成就
```

### 6.3 任务系统状态机

```
[空闲] --(定时/条件触发)--> [任务发布]
                              |
                         [等待用户完成]
                              |
                 用户拍照后匹配合成条件
                              |
                    [完成] --(给予奖励)--> [空闲]
```

**任务模板（MVP 3 个）**：

| 模板 | 匹配条件 | 奖励 |
|------|----------|------|
| 拍一张 [红色/蓝色/绿色] 的东西 | 照片主色调与目标颜色色差 < 30% | 能量 ×2 |
| 拍一张暖色调的照片 | 照片 color_category === "warm" | 能量 ×2 |
| 拍一张高饱和度的照片 | 照片 saturation_level === "high" | 能量 ×2 |

### 6.4 地图标记点实现

```
前端拍照成功后：
  → 调 `navigator.geolocation.getCurrentPosition()` 获取经纬度
  → 作为 `lat` / `lng` 字段附在 multipart 表单中
  → FastAPI 写入 photos.lat / photos.lng 列

前端地图页加载时：
  → 查询当前用户所有有 location 的 photos
  → 在地图上逐点标注
  → 标记点颜色 = 该照片的 dominant_color
  → 点击标记点显示：缩略图 + 评分 + 颜色
```

> **简化要点**：不做路线连线，不做轨迹回放，不做热力图。

---

## 7. API 接口定义

### 7.1 核心接口

> 所有接口前缀为 `/api/v1/`；返回值字段统一 snake_case，前端在 Axios 拦截器层转 camelCase。

| 方法 | 路径 | 说明 | 请求参数 | 返回 |
|------|------|------|----------|------|
| GET  | `/health` | 健康检查 | — | `{ "status": "ok" }` |
| POST | `/photo/analyze` | 上传照片并分析 | `image: file`, `user_id`, `lat?`, `lng?` | `{photo_id, analysis, energy_change}` |
| GET  | `/user/{user_id}/profile` | 获取用户信息和小人状态 | — | `{user, pet}` |
| POST | `/user/{user_id}/pet/evolve` | 触发进化 | — | `{new_stage}` |
| GET  | `/tasks/current` | 获取当前任务 | `user_id` | `{task}` |
| POST | `/tasks/generate` | 手动触发新任务 | `user_id` | `{new_task}` |
| GET  | `/photos` | 获取照片列表 | `user_id, page=1, limit=20` | `{photos, total}` |
| GET  | `/photos/map` | 获取有位置的照片 | `user_id` | `[{photo_id, dominant_color, lat, lng}]` |
| GET  | `/collections` | 获取图鉴 | `user_id` | `{colors, combos, locations}` |
| POST | `/share/generate` | 生成分享图 | `photo_id` | `{share_image_url}` |

### 7.2 关键接口详述：上传照片

```
POST /api/v1/photo/analyze
Content-Type: multipart/form-data

Request:
  image: File (拍照/选择)
  user_id: string (必填)
  lat: number (可选)
  lng: number (可选)

Response (200):
{
  "photo_id": "p_20260523_001",
  "analysis": {
    "dominant_color": "#FF6B6B",
    "palette": ["#FF6B6B", "#4ECDC4", "#FFE66D"],
    "score": 78,
    "comment": "这个蓝橙互补色很高级",
    "color_category": "warm",
    "saturation_level": "high",
    "brightness_level": "medium"
  },
  "energy_change": {
    "r": 25,
    "g": 10,
    "b": 10,
    "total": 45,
    "pet_mood": "happy"
  },
  "task_completed": null,          // 如果完成了某个任务，返回 task_id
  "achievements_unlocked": []      // 新解锁的成就列表
}

Error (400/500) — FastAPI 标准格式:
{
  "detail": "仅支持 JPEG / PNG / WebP"
}
```

---

## 8. 关键决策记录

| 决策 | 选择 | 理由 |
|------|------|------|
| 拍照后同步分析 vs 异步 | **同步** | MVP 阶段需要即时反馈，异步会打断体验 |
| 本地图片压缩 vs 原图上传 | **压缩后上传** | 减小上传耗时和存储成本，颜色分析不需要高清图 |
| AI 评分 vs 纯规则评分 | **AI + 规则兜底** | AI 能给出有温度的评语，规则用于兜底和校验 |
| 任务系统自动触发 vs 手动 | **手动触发按钮** | MVP 避免复杂的定时逻辑，用户点击「求任务」即可 |
| 进化自动触发 vs 手动 | **手动点击进化** | 让用户有主动感和仪式感 |

---

## 9. 风险矩阵

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| 视觉 API 响应 > 5s | 中 | 高 | 加 loading 动画 + 兜底规则并行调用，谁先回用谁 |
| 视觉 API 成本超预算 | 中 | 中 | 限制每人每天免费分析次数；超过后走纯规则评分 |
| 图片上传太慢 | 低 | 中 | 前端压缩到 720px 宽再上传 |
| 地图 SDK 集成复杂 | 中 | 中 | 先用最简单的标记点 API，不做任何自定义样式 |
| 评审时网络不佳 | 低 | 高 | 预缓存演示数据到本地；准备离线演示视频 |

---

## 10. 检查清单（提交前）

### 功能检查
- [ ] 核心闭环：拍照 → 评分 → 小人变化 完整跑通
- [ ] 至少一个任务能被触发并完成
- [ ] 地图上至少能看到一个彩色标记点
- [ ] 图鉴中至少能看到 1–2 个已解锁颜色
- [ ] 能生成一张分享图

### 体验检查
- [ ] 所有页面有空状态展示（首次使用无数据时）
- [ ] 所有操作有 loading 反馈
- [ ] 错误/超时有提示文案
- [ ] 用户能理解「为什么是这个分数」

### 提交检查
- [ ] 代码已上传 GitHub
- [ ] README 写清楚项目介绍 + 如何运行
- [ ] Pitch Deck 已上传
- [ ] 3 分钟演示视频已录制
- [ ] 演示图片素材已预置在相册中
