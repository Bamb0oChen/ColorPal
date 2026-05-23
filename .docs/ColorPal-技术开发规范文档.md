# ColorPal 技术开发规范文档

> **版本**：v2.1
> **适用对象**：全体开发成员
> **技术栈**：Vue 3 + FastAPI（两层架构）
> **日期**：2026.05

---

## 1. 文件架构

### 1.1 系统架构总览

```
┌─────────────┐        HTTP        ┌─────────────────┐
│  Vue 3 前端  │ ──────────────→   │  FastAPI 后端    │
│  (Web App)   │ ←──────────────   │  (AI + 持久化)   │
└─────────────┘                    └────────┬────────┘
                                            │
                                            ├──→ Qwen/DeepSeek 视觉模型
                                            ├──→ HSL 规则评分（兜底）
                                            └──→ SQLite (SQLAlchemy)
```

**数据流向**：
1. 用户拍照 → Vue 前端压缩 → 上传到 FastAPI
2. FastAPI 调 Qwen/DeepSeek 视觉模型分析；超时/失败时走 HSL 规则评分兜底
3. FastAPI 用 SQLAlchemy 写入 SQLite（photos、users.pet.energy）
4. 返回评分 + 能量变化给前端 → 小人状态更新

> **为什么是两层**：MVP 阶段只有 4 人、25 小时。多一层就多一组语言切换、多一组 schema 对齐成本，AI 分析与 CRUD 都在 Python 里写最省时间，且 SQLAlchemy + Pydantic 一套 schema 就够前端对齐。

### 1.2 项目目录结构

```
colorpal/                                 # 项目根目录
│
├── docker-compose.yml                    # 容器编排（生产/演示部署）
├── .env.example                          # 环境变量模板
├── .gitignore
├── README.md
│
├── frontend/                             # Vue 3 前端项目
│   ├── vite.config.ts                    # Vite 构建配置
│   ├── tsconfig.json
│   ├── package.json
│   ├── index.html
│   ├── Dockerfile
│   ├── public/
│   │   └── favicon.ico
│   └── src/
│       ├── main.ts                       # 应用入口
│       ├── App.vue                       # 根组件
│       ├── router/
│       │   └── index.ts                  # 路由配置
│       ├── stores/                       # Pinia 状态管理
│       │   ├── pet.ts
│       │   ├── photo.ts
│       │   └── task.ts
│       ├── api/                          # API 请求层
│       │   ├── request.ts                # Axios 封装
│       │   ├── photo.ts
│       │   ├── user.ts
│       │   └── task.ts
│       ├── views/                        # 页面
│       │   ├── HomeView.vue
│       │   ├── ResultView.vue
│       │   ├── MapView.vue
│       │   ├── CollectionView.vue
│       │   └── ProfileView.vue
│       ├── components/                   # 组件
│       │   ├── pet/
│       │   │   ├── PetDisplay.vue
│       │   │   └── PetEnergyBar.vue
│       │   ├── score/
│       │   │   ├── ScoreCard.vue
│       │   │   └── ColorPalette.vue
│       │   ├── task/
│       │   │   └── TaskBubble.vue
│       │   └── common/
│       │       ├── LoadingSpinner.vue
│       │       └── EmptyState.vue
│       ├── composables/                  # 组合式函数
│       │   ├── useCamera.ts
│       │   ├── useLocation.ts
│       │   └── useShare.ts
│       ├── utils/
│       │   ├── color.ts
│       │   ├── format.ts
│       │   └── constants.ts
│       ├── types/                        # TypeScript 类型
│       │   ├── pet.ts
│       │   ├── photo.ts
│       │   └── task.ts
│       └── styles/
│           ├── variables.css
│           └── global.css
│
├── backend/                              # FastAPI 后端
│   ├── Dockerfile
│   ├── pyproject.toml                    # 依赖与项目配置
│   ├── main.py                           # 应用入口
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py                     # 配置读取（环境变量）
│   │   ├── db.py                         # SQLAlchemy session + 初始化
│   │   ├── routers/                      # 路由
│   │   │   ├── __init__.py
│   │   │   ├── health.py
│   │   │   ├── photo.py
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── services/                     # 业务服务
│   │   │   ├── __init__.py
│   │   │   ├── ai_analyzer.py            # Qwen/DeepSeek 调用
│   │   │   ├── scorer.py                 # HSL 兜底评分
│   │   │   ├── pet_state.py              # 小人能量/心情计算
│   │   │   └── task_matcher.py           # 任务完成匹配
│   │   ├── models/                       # SQLAlchemy ORM 模型
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── photo.py
│   │   │   ├── collection.py
│   │   │   └── task.py
│   │   ├── schemas/                      # Pydantic schemas（接口契约）
│   │   │   ├── __init__.py
│   │   │   ├── photo.py
│   │   │   ├── pet.py
│   │   │   └── task.py
│   │   └── middleware/
│   │       ├── __init__.py
│   │       └── cors.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_scorer.py
│   │   └── test_pet_state.py
│   └── data/                             # SQLite 数据库文件存放
│       └── .gitkeep
│
├── .docs/                                # 项目文档（read-only）
│   ├── ColorPal-产品需求文档.md
│   ├── ColorPal-技术方案文档.md
│   ├── ColorPal-技术开发规范文档.md
│   └── ColorPal-团队分工文档.md
│
├── scripts/
│   ├── start-dev.sh                      # 一键启动开发环境
│   └── seed-data.py                      # 演示数据填充
│
└── assets/                               # 共享设计素材
    ├── pet-sprites/
    └── poster/
```

### 1.3 命名规范

| 层级 | 规范 | 示例 |
|------|------|------|
| 前端组件文件 | PascalCase | `PetDisplay.vue`、`ScoreCard.vue` |
| 前端路由路径 | kebab-case | `/photo-result`、`/color-map` |
| TS 工具文件 | camelCase | `color.ts`、`useCamera.ts` |
| FastAPI 路由路径 | 小写蛇形 | `/api/v1/photo/analyze` |
| Python 文件 | 小写蛇形 | `ai_analyzer.py`、`pet_state.py` |
| SQLAlchemy 模型类 | PascalCase | `User`、`Photo`、`Task` |
| 数据库表 | 小写蛇形复数 | `users`、`photos`、`tasks` |
| Pydantic schema | PascalCase + 用途后缀 | `PhotoCreate`、`PhotoResponse` |

---

## 2. 主要技术栈

### 2.1 技术选型

| 层级 | 技术 | 版本要求 | 说明 |
|------|------|----------|------|
| **前端** | Vue 3 | ^3.4 | Composition API + `<script setup>` |
| | Vite | ^5.0 | 构建工具 |
| | TypeScript | ^5.3 | 类型安全 |
| | Pinia | ^2.1 | 状态管理 |
| | Vue Router | ^4.2 | 路由 |
| | Axios | ^1.6 | HTTP 请求 |
| | Live2D SDK / pixi-live2d-display | 待锁定 | Pet 表现层 |
| | Leaflet | ^1.9 | 地图组件 |
| **后端** | FastAPI | ^0.110 | Python 异步 Web 框架 |
| | Uvicorn | ^0.27 | ASGI 服务器 |
| | Pydantic | ^2.0 | 数据校验 / 接口契约 |
| | SQLAlchemy | ^2.0 | ORM（异步 session） |
| | aiosqlite | ^0.19 | SQLite 异步驱动 |
| | httpx | ^0.27 | 异步 HTTP 客户端（调 Qwen/DeepSeek 视觉模型） |
| | python-multipart | — | 文件上传 |
| | Pillow | ^10.0 | 图像处理（HSL 兜底） |
| **数据库** | SQLite | — | 单文件，零运维；后期可换 PostgreSQL |
| **AI** | Qwen / DeepSeek 视觉模型 | `VISION_MODEL` 配置 | 视觉分析 |
| **部署** | Docker + Docker Compose | — | 容器化 |

### 2.2 关键接口契约位置

Pydantic schema（`backend/app/schemas/`）是**唯一接口契约源**：

- TypeScript 类型（`frontend/src/types/`）手工对齐 Pydantic
- 数据库 ORM 模型（`backend/app/models/`）字段命名与 Pydantic 一致（snake_case），仅在前端层做 camelCase 转换

---

## 3. 代码规范与协作流程

### 3.1 通用编码规范

- **缩进**：2 空格（前端）/ 4 空格（Python）
- **编码**：UTF-8
- **行尾**：LF
- **单行上限**：100 字符
- **文件末尾**：保留一个空行
- **注释**：中文，解释为什么而非是什么
- **配置项**：所有敏感信息（API Key、密钥）通过环境变量加载；不写死在代码里

### 3.2 Vue 3 / TypeScript 规范

```typescript
// frontend/src/types/pet.ts
// 命名导出，不写默认导出
export interface PetInfo {
  name: string
  stage: number
  mood: 'happy' | 'neutral' | 'sad'
  energy: {
    current: number
    max: number
  }
}
```

```vue
<!-- 组件模板：<script setup> + 类型标注 -->
<script setup lang="ts">
import { ref, computed } from 'vue'
import type { PetInfo } from '@/types/pet'

const props = defineProps<{
  petInfo: PetInfo
  isLoading?: boolean
}>()

const emit = defineEmits<{
  takePhoto: []
  evolve: [petId: string]
}>()

const showTask = ref(false)

const energyPercent = computed(() => {
  const { current, max } = props.petInfo.energy
  return Math.min(100, Math.round((current / max) * 100))
})

const handleTap = () => {
  emit('takePhoto')
}
</script>

<template>
  <div class="pet-container" :class="{ 'is-loading': isLoading }">
    <div class="pet-avatar" @click="handleTap">
      <PetEnergyBar :percent="energyPercent" />
    </div>
    <TaskBubble v-if="showTask" />
  </div>
</template>

<style scoped>
.pet-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
```

#### Pinia Store 规范

```typescript
// stores/pet.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getPetProfile } from '@/api/user'
import type { PetInfo } from '@/types/pet'

export const usePetStore = defineStore('pet', () => {
  const petInfo = ref<PetInfo | null>(null)
  const isLoading = ref(false)

  const energyPercent = computed(() => {
    if (!petInfo.value) return 0
    const { current, max } = petInfo.value.energy
    return Math.round((current / max) * 100)
  })

  const fetchProfile = async () => {
    isLoading.value = true
    try {
      petInfo.value = await getPetProfile()
    } finally {
      isLoading.value = false
    }
  }

  return { petInfo, isLoading, energyPercent, fetchProfile }
})
```

#### API 层规范

```typescript
// api/request.ts
import axios from 'axios'
import type { AxiosInstance } from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const http: AxiosInstance = axios.create({
  baseURL: `${API_BASE}/api/v1`,
  timeout: 15000,
})

http.interceptors.response.use(
  (res) => res.data,
  (err) => {
    const message = err.response?.data?.detail || '请求失败，请重试'
    console.error('[API Error]', message)
    return Promise.reject(err)
  },
)

export default http
```

```typescript
// api/photo.ts
import http from './request'
import type { AnalysisResult } from '@/types/photo'

export interface UploadResponse {
  photoId: string
  analysis: AnalysisResult
  energyChange: { r: number; g: number; b: number; total: number }
}

export const uploadAndAnalyze = async (
  file: File,
  location?: { lat: number; lng: number },
): Promise<UploadResponse> => {
  const formData = new FormData()
  formData.append('image', file)
  if (location) {
    formData.append('lat', String(location.lat))
    formData.append('lng', String(location.lng))
  }

  return http.post('/photo/analyze', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}
```

### 3.3 FastAPI 规范

#### 路由层（只负责协议解析 + 调用服务）

```python
# backend/app/routers/photo.py
"""照片分析路由：接收上传，调度 AI 与持久化。"""

import logging

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.photo import PhotoAnalysisResponse
from app.services.ai_analyzer import analyze_image
from app.services.pet_state import apply_energy_gain
from app.models.photo import Photo

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/photo', tags=['photo'])


@router.post('/analyze', response_model=PhotoAnalysisResponse)
async def analyze_photo(
    image: UploadFile = File(...),
    lat: float | None = Form(None),
    lng: float | None = Form(None),
    user_id: str = Form(...),
    db: AsyncSession = Depends(get_session),
):
    """上传照片并返回评分；失败时由 analyze_image 自动降级。"""
    if image.content_type not in ('image/jpeg', 'image/png', 'image/webp'):
        raise HTTPException(status_code=400, detail='仅支持 JPEG / PNG / WebP')

    image_bytes = await image.read()
    analysis = await analyze_image(image_bytes)

    photo = Photo.create_from_analysis(
        user_id=user_id,
        analysis=analysis,
        lat=lat,
        lng=lng,
    )
    db.add(photo)
    energy_change = await apply_energy_gain(db, user_id, analysis)
    await db.commit()

    return PhotoAnalysisResponse(
        photo_id=photo.id,
        analysis=analysis,
        energy_change=energy_change,
    )
```

#### 服务层（外部 IO + 业务规则）

```python
# backend/app/services/ai_analyzer.py
"""Qwen/DeepSeek 视觉模型调用，主路径失败时走 HSL 兜底。"""

import base64
import json
import logging

import httpx

from app.config import settings
from app.services.scorer import fallback_score

logger = logging.getLogger(__name__)

TIMEOUT_SECONDS = 8

SYSTEM_PROMPT = '你是一位专业的色彩分析师。分析照片，输出 JSON。'


async def analyze_image(image_bytes: bytes) -> dict:
    """主路径视觉模型，超时/失败时切换到 HSL 兜底，调用方无需感知。"""
    try:
        return await _call_vision_model(image_bytes)
    except Exception as err:
        logger.warning('视觉模型失败，切换兜底评分: %s', err)
        return fallback_score(image_bytes)


async def _call_vision_model(image_bytes: bytes) -> dict:
    b64 = base64.b64encode(image_bytes).decode()
    async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
        resp = await client.post(
            settings.vision_api_base_url,
            headers={
                'Authorization': f'Bearer {settings.vision_api_key}',
                'Content-Type': 'application/json',
            },
            json={
                'model': settings.vision_model,
                'messages': [
                    {'role': 'system', 'content': SYSTEM_PROMPT},
                    {
                        'role': 'user',
                        'content': [
                            {'type': 'text', 'text': 'analyze this photo'},
                            {
                                'type': 'image_url',
                                'image_url': {'url': f'data:image/jpeg;base64,{b64}'},
                            },
                        ],
                    },
                ],
                'max_tokens': 500,
            },
        )
        resp.raise_for_status()
        content = resp.json()['choices'][0]['message']['content']
        return json.loads(content)
```

#### 数据库层（SQLAlchemy 2.0 异步）

```python
# backend/app/db.py
"""异步 SQLAlchemy session 工厂。"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
SessionFactory = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """所有 ORM 模型的基类。"""


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        yield session
```

```python
# backend/app/models/photo.py
"""照片记录。"""

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Photo(Base):
    __tablename__ = 'photos'

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, index=True)
    dominant_color: Mapped[str] = mapped_column(String(7))
    palette: Mapped[str] = mapped_column(String)  # 逗号分隔的 hex
    score: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(String)
    lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    lng: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

### 3.4 Git 协作流程

#### 分支策略

```
main                  ← 稳定版本，可演示
  └── dev             ← 开发分支
       ├── feat/<scope>-<short-desc>
       ├── fix/<scope>-<short-desc>
       └── docs/<short-desc>
```

`scope` 取值：`frontend` / `backend` / `infra` / `docs`。

#### Commit 规范

```
<type>(<scope>): <简短中文描述>

type: feat / fix / docs / refactor / style / chore
```

示例：

```
feat(frontend): 拍照页集成相机 API
feat(backend): 对接 Qwen 视觉分析接口
fix(backend): AI 超时后未正确降级到兜底评分
docs: 同步技术方案到两层架构
```

#### Code Review 要点

- **接口契约**：FastAPI 返回字段是否与 TypeScript 类型一致（snake_case ↔ camelCase 转换是否到位）
- **错误传播**：路由层是否捕获并转 HTTPException，服务层异常是否分类（用户错误 / 系统错误 / 第三方失败）
- **类型安全**：是否所有 Pydantic schema 都有字段校验（regex、range）
- **配置泄漏**：API Key、连接串是否走 `settings`（环境变量）

---

## 4. 突发预警策略

### 4.1 风险分级

| 级别 | 定义 | 响应 |
|------|------|------|
| **P0** | 前端 → FastAPI 主链路不通 | 全员暂停，集中修复 |
| **P1** | 某模块不可用（任务/图鉴/地图） | 负责人 + 1 人协助，2h 内解决 |
| **P2** | 体验问题（动画卡顿、文案错误） | 记录 issue，优先修 P0/P1 |

### 4.2 典型场景

| 场景 | 级别 | 应对 |
|------|------|------|
| 视觉模型 API 超时或 key 失效 | **P0** | `analyze_image()` 自动降级到 `fallback_score()`，前端无感知 |
| 上传图片体积过大 | **P1** | 前端拍照后压缩到 720px / 80% 质量再上传 |
| 前端 CORS 配置错误 | **P1** | 检查 `backend/app/middleware/cors.py` 的允许域 |
| SQLite 写入冲突 | **P2** | 异步 session 已 serialize；如果出现先确认是否多进程写 |
| 容器启动失败 | **P2** | `docker compose logs` 查看具体报错 |

### 4.3 降级策略

```
Qwen/DeepSeek 可用 ──→ AI 评分（主路径）
      ↓ 不可用或超时（8s）
HSL 规则评分（兜底，纯本地计算）──→ 仍返回评分
      ↓ 也异常
返回 400 + 文案 → 前端展示「分析失败，请重试」
```

演示当天网络风险按 [技术方案文档 §9 风险矩阵] 的最后一行处理（预存离线演示数据 + 备份演示视频）。

---

## 5. AI 示例参考

### 5.1 给 AI 的风格指令模板

```
项目: ColorPal
架构: Vue 3 + FastAPI（两层）

前端 (Vue 3 + TypeScript):
- 使用 Composition API、<script setup>、2 空格缩进
- 单引号、行尾分号、100 字符行宽
- 命名导出，不写默认导出

后端 (FastAPI + Python 3.11):
- 4 空格缩进、单引号
- 使用 async/await、Pydantic v2、SQLAlchemy 2.0 异步 API
- 路由层只做协议解析，业务逻辑放 services/，数据库访问放 models/

通用要求:
- 所有外部调用 (视觉模型、文件 IO) 必须 try/except
- 注释用中文，解释为什么而非是什么
- 配置项一律走环境变量（pydantic-settings）
- 错误返回 FastAPI 的 HTTPException，前端 axios 拦截器统一处理
```

### 5.2 类型契约对齐（Pydantic ↔ TypeScript）

```python
# backend/app/schemas/photo.py
from typing import Literal

from pydantic import BaseModel, Field


class AnalysisResult(BaseModel):
    dominant_color: str = Field(..., pattern=r'^#[0-9a-fA-F]{6}$')
    palette: list[str]
    score: int = Field(..., ge=0, le=100)
    comment: str
    color_category: Literal['warm', 'cool', 'neutral']
    saturation_level: Literal['high', 'medium', 'low']
    brightness_level: Literal['high', 'medium', 'low']


class EnergyChange(BaseModel):
    r: int
    g: int
    b: int
    total: int


class PhotoAnalysisResponse(BaseModel):
    photo_id: str
    analysis: AnalysisResult
    energy_change: EnergyChange
```

```typescript
// frontend/src/types/photo.ts
export interface AnalysisResult {
  dominantColor: string
  palette: string[]
  score: number
  comment: string
  colorCategory: 'warm' | 'cool' | 'neutral'
  saturationLevel: 'high' | 'medium' | 'low'
  brightnessLevel: 'high' | 'medium' | 'low'
}

export interface EnergyChange {
  r: number
  g: number
  b: number
  total: number
}

export interface UploadResponse {
  photoId: string
  analysis: AnalysisResult
  energyChange: EnergyChange
}
```

> **命名风格转换**：FastAPI 返回 snake_case，前端 axios 响应拦截器（或手写映射）统一转 camelCase。

### 5.3 接口示例：POST /api/v1/photo/analyze

**Request**（multipart/form-data）：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `image` | File | ✅ | JPEG / PNG / WebP，建议 ≤200KB |
| `lat` | number | — | 纬度 |
| `lng` | number | — | 经度 |
| `user_id` | string | ✅ | 用户 ID |

**Response 200**：

```json
{
  "photo_id": "p_20260523_001",
  "analysis": {
    "dominant_color": "#FF6B6B",
    "palette": ["#FF6B6B", "#4ECDC4", "#FFE66D"],
    "score": 78,
    "comment": "蓝橙互补，配色高级",
    "color_category": "warm",
    "saturation_level": "high",
    "brightness_level": "medium"
  },
  "energy_change": { "r": 25, "g": 10, "b": 10, "total": 45 }
}
```

**Response 400**（用户错误，如格式不支持）：

```json
{ "detail": "仅支持 JPEG / PNG / WebP" }
```

### 5.4 Vue 页面调用完整流程

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { uploadAndAnalyze } from '@/api/photo'
import { usePetStore } from '@/stores/pet'
import { useRouter } from 'vue-router'

const router = useRouter()
const petStore = usePetStore()
const isUploading = ref(false)

const handleFileSelected = async (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return

  isUploading.value = true
  try {
    const result = await uploadAndAnalyze(file)
    petStore.applyEnergyChange(result.energyChange)
    router.push({ name: 'result', query: { photoId: result.photoId } })
  } catch (err) {
    console.error('上传失败:', err)
  } finally {
    isUploading.value = false
  }
}
</script>
```

---

## 6. 开发环境启动

### 6.1 前置条件

- Node.js >= 18
- Python >= 3.11
- Docker + Docker Compose（推荐，用于一键启动）

### 6.2 本地启动（不用 Docker）

```bash
# 后端
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e .
uvicorn main:app --reload --port 8000

# 前端
cd frontend
npm install
npm run dev
```

### 6.3 Docker 一键启动

```bash
cp .env.example .env       # 填入 VISION_API_KEY
docker compose up --build
```

### 6.4 服务端口

| 服务 | 端口 | 地址 |
|------|------|------|
| Vue 前端 | 5173 | http://localhost:5173 |
| FastAPI | 8000 | http://localhost:8000 |
| FastAPI Swagger | 8000 | http://localhost:8000/docs |
| 健康检查 | 8000 | http://localhost:8000/api/v1/health |

### 6.5 环境变量（`.env`）

| 变量 | 必填 | 默认 | 说明 |
|------|------|------|------|
| `VISION_PROVIDER` | — | `qwen` | 视觉模型供应商标识，仅用于日志和切换说明 |
| `VISION_API_KEY` | ✅ | — | Qwen / DeepSeek 视觉模型调用密钥 |
| `VISION_API_BASE_URL` | — | DashScope 兼容接口 | OpenAI-compatible chat completions 地址 |
| `VISION_MODEL` | — | `qwen-vl-max` | 视觉模型名称 |
| `DATABASE_URL` | — | `sqlite+aiosqlite:///./data/colorpal.db` | SQLAlchemy 连接串 |
| `CORS_ALLOW_ORIGINS` | — | `http://localhost:5173` | 前端域名（逗号分隔多个） |
| `VITE_API_BASE` | — | `http://localhost:8000` | 前端连后端的基础 URL |
