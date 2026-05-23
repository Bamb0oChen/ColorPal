# ColorPal 技术开发规范文档

> **版本**：v2.0
> **适用对象**：全体开发成员
> **技术栈**：Vue 3 + FastAPI + C# (.NET)
> **日期**：2026.05

---

## 1. 文件架构

### 1.1 系统架构总览

```
┌─────────────┐     HTTP     ┌──────────────┐     gRPC/HTTP    ┌────────────┐
│  Vue 3 前端  │ ──────────→  │  FastAPI 网关  │ ─────────────→  │  C# 后端服务 │
│  (Web App)   │ ←──────────  │  (中间层)     │ ←─────────────  │  (.NET)     │
└─────────────┘              └──────┬───────┘                  └────────────┘
                                    │
                                    ├──→ GPT-4V Vision API
                                    └──→ 规则评分引擎 (兜底)
```

**数据流向**：
1. 用户拍照 → Vue 3 前端 → 上传图片 → FastAPI → GPT-4V 分析
2. AI 结果 → FastAPI 校验/后处理 → C# 后端存储 → 返回给前端
3. 前端展示评分结果 → 更新小人状态 → 完成闭环

### 1.2 项目目录结构

```
colopal/                                  # 项目根目录
│
├── docker-compose.yml                    # 【第一层】全局容器编排配置
├── .env                                  # 【第一层】全局环境变量
├── .env.example                          # 【第一层】环境变量模板
├── .gitignore
├── README.md
├── package.json                          # 根级脚本（可选）
│
├── config/                               # 【第一层】配置文件目录
│   ├── frontend/                         # 前端配置
│   │   ├── .env.development
│   │   ├── .env.production
│   │   └── proxy.conf.js                 # 开发代理配置
│   ├── gateway/                          # FastAPI 配置
│   │   ├── config.dev.yaml
│   │   ├── config.prod.yaml
│   │   └── logging.conf
│   └── backend/                          # C# 后端配置
│       ├── appsettings.json
│       ├── appsettings.Development.json
│       └── appsettings.Production.json
│
├── frontend/                             # Vue 3 前端项目
│   ├── vite.config.ts                    # Vite 构建配置
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── package.json
│   ├── index.html
│   ├── public/
│   │   ├── favicon.ico
│   │   └── images/                       # 静态图片
│   └── src/
│       ├── main.ts                       # 应用入口
│       ├── App.vue                       # 根组件
│       ├── router/
│       │   └── index.ts                  # 路由配置
│       ├── stores/                       # Pinia 状态管理
│       │   ├── pet.ts                    # 小人状态
│       │   ├── photo.ts                  # 照片状态
│       │   └── task.ts                   # 任务状态
│       ├── api/                          # API 请求层
│       │   ├── request.ts                # Axios 封装
│       │   ├── photo.ts                  # 照片 API
│       │   ├── user.ts                   # 用户 API
│       │   └── task.ts                   # 任务 API
│       ├── views/                        # 页面组件
│       │   ├── HomeView.vue              # 首页（拍照入口 + 小人）
│       │   ├── ResultView.vue            # 评分结果页
│       │   ├── MapView.vue               # 地图页
│       │   ├── CollectionView.vue        # 图鉴页
│       │   └── ProfileView.vue           # 个人页
│       ├── components/                   # 公共组件
│       │   ├── pet/
│       │   │   ├── PetDisplay.vue        # 小人展示
│       │   │   └── PetEnergyBar.vue      # 能量条
│       │   ├── score/
│       │   │   ├── ScoreCard.vue         # 评分卡片
│       │   │   └── ColorPalette.vue      # 调色板
│       │   ├── task/
│       │   │   └── TaskBubble.vue        # 任务气泡
│       │   └── common/
│       │       ├── LoadingSpinner.vue
│       │       └── EmptyState.vue
│       ├── composables/                  # 组合式函数
│       │   ├── useCamera.ts              # 相机逻辑
│       │   ├── useLocation.ts            # 定位逻辑
│       │   └── useShare.ts               # 分享逻辑
│       ├── utils/                        # 工具函数
│       │   ├── color.ts                  # 色彩转换
│       │   ├── format.ts                 # 格式化
│       │   └── constants.ts              # 常量定义
│       ├── types/                        # TypeScript 类型
│       │   ├── pet.ts
│       │   ├── photo.ts
│       │   └── task.ts
│       └── styles/                       # 全局样式
│           ├── variables.css             # CSS 变量
│           └── global.css                # 全局样式
│
├── gateway/                              # FastAPI 中间层
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── main.py                          # 应用入口
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py                    # 配置读取
│   │   ├── routers/                     # 路由
│   │   │   ├── __init__.py
│   │   │   ├── photo.py                 # 照片分析路由
│   │   │   ├── user.py                  # 用户路由（转发）
│   │   │   └── task.py                  # 任务路由（转发）
│   │   ├── services/                    # 业务服务
│   │   │   ├── __init__.py
│   │   │   ├── ai_analyzer.py           # AI 视觉分析
│   │   │   ├── scorer.py                # 评分规则引擎
│   │   │   └── backend_client.py        # C# 后端 HTTP 客户端
│   │   ├── models/                      # Pydantic 模型
│   │   │   ├── __init__.py
│   │   │   ├── photo.py
│   │   │   └── pet.py
│   │   └── middleware/                  # 中间件
│   │       ├── __init__.py
│   │       ├── cors.py                  # 跨域配置
│   │       └── logging.py               # 日志
│   └── tests/                           # 测试
│       ├── __init__.py
│       ├── test_ai_analyzer.py
│       └── test_scorer.py
│
├── backend/                              # C# (.NET) 后端服务
│   ├── Colopal.sln                       # 解决方案文件
│   ├── Dockerfile
│   ├── Directory.Build.props             # 全局构建配置
│   └── Colopal.Api/                     # Web API 项目
│       ├── Program.cs                    # 应用入口
│       ├── Colopal.Api.csproj
│       ├── Controllers/                  # API 控制器
│       │   ├── PhotoController.cs
│       │   ├── UserController.cs
│       │   ├── TaskController.cs
│       │   └── CollectionController.cs
│       ├── Models/                       # 数据模型
│       │   ├── User.cs
│       │   ├── Photo.cs
│       │   ├── Pet.cs
│       │   └── Task.cs
│       ├── Services/                     # 业务服务
│       │   ├── IUserService.cs           # 接口
│       │   ├── UserService.cs            # 实现
│       │   ├── ITaskService.cs
│       │   ├── TaskService.cs
│       │   ├── IPhotoService.cs
│       │   └── PhotoService.cs
│       ├── Data/                         # 数据访问
│       │   ├── AppDbContext.cs
│       │   └── Migrations/
│       ├── DTOs/                         # 数据传输对象
│       │   ├── PhotoDto.cs
│       │   └── UserDto.cs
│       └── Middleware/
│           ├── ExceptionMiddleware.cs
│           └── RequestLoggingMiddleware.cs
│
├── docs/                                 # 项目文档
│   ├── 产品需求文档.md
│   ├── 技术方案文档.md
│   ├── 技术开发规范文档.md
│   └── 团队分工文档.md
│
├── scripts/                              # 工具脚本
│   ├── start-dev.sh                      # 一键启动开发环境
│   ├── compress-image.py                 # 图片压缩
│   └── seed-data.py                      # 演示数据填充
│
└── assets/                               # 共享设计资源
    ├── pet-sprites/                      # 小人素材
    └── poster/                           # 路演海报素材
```

### 1.3 命名规范

| 层级 | 规范 | 示例 |
|------|------|------|
| 前端组件 | PascalCase | `PetDisplay.vue`、`ScoreCard.vue` |
| 前端路由 | kebab-case | `/photo-result`、`/color-map` |
| FastAPI 路由 | 小写蛇形 | `/api/v1/photo/analyze` |
| C# Controller | PascalCase + Controller 后缀 | `PhotoController.cs` |
| C# 接口 | I + PascalCase | `IPhotoService.cs` |
| Python 文件 | 小写蛇形 | `ai_analyzer.py`、`backend_client.py` |
| 数据库集合/表 | 小写蛇形 | `users`、`photo_records` |
| 配置文件 | 按层级嵌套 | `config/gateway/config.dev.yaml` |

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
| | Lottie Web | ^5.12 | 小人动画 |
| | Leaflet / Mapbox GL JS | — | 地图组件 |
| **网关** | FastAPI | ^0.110 | Python 异步 Web 框架 |
| | httpx | ^0.27 | 异步 HTTP 客户端（调用 C# + AI） |
| | python-multipart | — | 文件上传支持 |
| | Pydantic | ^2.0 | 数据校验 |
| **后端** | .NET 8 | 8.0+ | C# Web API |
| | Entity Framework Core | 8.0+ | ORM |
| | SQLite / PostgreSQL | — | 数据库 |
| | Swashbuckle | — | Swagger 文档 |
| **AI** | OpenAI API | gpt-4-vision-preview | 视觉分析 |
| **部署** | Docker + Docker Compose | — | 容器化 |

### 2.2 数据流说明

```
[浏览器]                    [FastAPI]                  [C# Backend]
   │                          │                           │
   │── POST /api/v1/photo ──→ │                           │
   │  (multipart: image)      │── httpx ──→ GPT-4V ──→   │
   │                          │←── JSON 结果 ───────────  │
   │                          │                           │
   │                          │── httpx ──→ POST /photo ─→│
   │                          │         (分析结果)         │── 存入数据库
   │                          │←── 201 Created ──────────│
   │                          │                           │
   │←── 评分 + 小人能量变化 ── │                           │
```

FastAPI 是**唯一入口**，前端只与 FastAPI 通信，不直接调用 C#：

```
前端 → FastAPI (AI 分析 + 路由转发) → C# (持久化 + 业务逻辑)
     ←                             ←
```

---

## 3. 代码规范与协作流程

### 3.1 通用编码规范

- **缩进**：2 空格（所有语言统一）
- **编码**：UTF-8
- **行尾**：LF（不是 CRLF）
- **单行上限**：100 字符（前端/网关）/ 120 字符（C#）
- **文件末尾**：保留一个空行
- **注释**：用中文，解释为什么而非是什么

### 3.2 Vue 3 / TypeScript 规范

```typescript
// ============ 组件规范：<script setup> + TypeScript ============

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
<!-- 组件模板：script setup + 类型标注 -->
<script setup lang="ts">
import { ref, computed } from 'vue'
import type { PetInfo } from '@/types/pet'

// Props 用类型标注
const props = defineProps<{
  petInfo: PetInfo
  isLoading?: boolean
}>()

// Emits 用类型标注
const emit = defineEmits<{
  takePhoto: []
  evolve: [petId: string]
}>()

// 响应式数据
const showTask = ref(false)

// 计算属性
const energyPercent = computed(() => {
  const { current, max } = props.petInfo.energy
  return Math.min(100, Math.round((current / max) * 100))
})

// 方法：普通函数
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
  // state
  const petInfo = ref<PetInfo | null>(null)
  const isLoading = ref(false)

  // getter
  const energyPercent = computed(() => {
    if (!petInfo.value) return 0
    return Math.round(petInfo.value.energy.current / petInfo.value.energy.max * 100)
  })

  // action
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
import type { AxiosInstance, AxiosRequestConfig } from 'axios'

const GATEWAY_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const http: AxiosInstance = axios.create({
  baseURL: `${GATEWAY_BASE}/api/v1`,
  timeout: 15000,
})

// 响应拦截
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

```python
# app/routers/photo.py
"""
照片分析路由
接收前端上传的图片，调用 AI 分析，转发结果到 C# 后端
"""

import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.ai_analyzer import analyze_image
from app.services.backend_client import save_photo_record
from app.models.photo import PhotoAnalysisResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/photo", tags=["photo"])


@router.post("/analyze", response_model=PhotoAnalysisResponse)
async def analyze_photo(
    image: UploadFile = File(...),
    lat: float = Form(None),
    lng: float = Form(None),
):
    """
    上传照片并分析颜色
    - 先调用 GPT-4V 分析
    - AI 失败时走兜底规则评分
    - 将结果转发给 C# 后端持久化
    """
    # 校验图片格式
    if image.content_type not in ("image/jpeg", "image/png", "image/webp"):
        raise HTTPException(status_code=400, detail="不支持的图片格式")

    try:
        image_bytes = await image.read()

        # 主路径：AI 分析
        analysis = await analyze_image(image_bytes)

        # 转发到 C# 后端持久化
        saved = await save_photo_record(
            image_bytes=image_bytes,
            analysis=analysis,
            location={"lat": lat, "lng": lng} if lat else None,
        )

        return PhotoAnalysisResponse(
            photo_id=saved["id"],
            analysis=analysis,
            energy_change=saved["energy_change"],
        )

    except Exception as err:
        logger.exception("照片分析失败")
        raise HTTPException(status_code=500, detail=f"分析失败: {str(err)}")
```

```python
# app/services/ai_analyzer.py
"""
AI 视觉分析服务
主路径调用 GPT-4V，兜底走规则评分
"""

import json
import httpx
from app.core.config import settings
from app.services.scorer import fallback_score

SYSTEM_PROMPT = """你是一位专业的色彩分析师。分析这张照片，输出 JSON。"""

TIMEOUT_SECONDS = 15


async def analyze_image(image_bytes: bytes) -> dict:
    """分析图片颜色，返回评分 + 调色板"""
    try:
        return await call_gpt4v(image_bytes)
    except Exception as err:
        logger.warning(f"GPT-4V 失败，切换到兜底评分: {err}")
        return fallback_score(image_bytes)


async def call_gpt4v(image_bytes: bytes) -> dict:
    """调用 OpenAI GPT-4V API"""
    base64_image = base64.b64encode(image_bytes).decode()

    async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4-vision-preview",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": USER_PROMPT},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                },
                            },
                        ],
                    },
                ],
                "max_tokens": 500,
            },
        )
        resp.raise_for_status()
        result = resp.json()
        return json.loads(result["choices"][0]["message"]["content"])
```

```python
# app/services/backend_client.py
"""
C# 后端 HTTP 客户端
将分析结果转发给 .NET 服务持久化
"""

import httpx
from app.core.config import settings


async def save_photo_record(
    image_bytes: bytes,
    analysis: dict,
    location: dict | None,
) -> dict:
    """将分析结果保存到 C# 后端"""
    base64_image = base64.b64encode(image_bytes).decode()

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{settings.BACKEND_BASE_URL}/api/photos",
            json={
                "image_base64": base64_image,
                "analysis": analysis,
                "location": location,
            },
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
```

### 3.4 C# 规范

```csharp
// Controllers/PhotoController.cs
using Microsoft.AspNetCore.Mvc;
using Colopal.Api.Services;
using Colopal.Api.DTOs;

namespace Colopal.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class PhotoController : ControllerBase
{
    private readonly IPhotoService _photoService;
    private readonly ILogger<PhotoController> _logger;

    public PhotoController(IPhotoService photoService, ILogger<PhotoController> logger)
    {
        _photoService = photoService;
        _logger = logger;
    }

    /// <summary>
    /// 保存照片分析结果
    /// 由 FastAPI 网关调用，前端不直接访问此接口
    /// </summary>
    [HttpPost]
    public async Task<ActionResult<PhotoSaveResponse>> SavePhoto(
        [FromBody] SavePhotoRequest request)
    {
        if (request.Analysis == null)
            return BadRequest(new { message = "缺少分析结果" });

        try
        {
            var result = await _photoService.SaveAsync(request);
            return Created($"/api/photos/{result.Id}", result);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "保存照片失败");
            return StatusCode(500, new { message = "保存失败" });
        }
    }

    /// <summary>
    /// 获取用户的地图标记点
    /// </summary>
    [HttpGet("map-points/{userId}")]
    public async Task<ActionResult<List<MapPointDto>>> GetMapPoints(
        string userId)
    {
        var points = await _photoService.GetMapPointsAsync(userId);
        return Ok(points);
    }
}
```

```csharp
// Services/PhotoService.cs
namespace Colopal.Api.Services;

public class PhotoService : IPhotoService
{
    private readonly AppDbContext _db;
    private readonly ILogger<PhotoService> _logger;

    public PhotoService(AppDbContext db, ILogger<PhotoService> logger)
    {
        _db = db;
        _logger = logger;
    }

    public async Task<PhotoSaveResponse> SaveAsync(SavePhotoRequest request)
    {
        var photo = new Photo
        {
            Id = Guid.NewGuid().ToString(),
            ImageBase64 = request.ImageBase64,
            DominantColor = request.Analysis.DominantColor,
            Score = request.Analysis.Score,
            Comment = request.Analysis.Comment,
            Palette = string.Join(",", request.Analysis.Palette),
            Latitude = request.Location?.Lat,
            Longitude = request.Location?.Lng,
            CreatedAt = DateTime.UtcNow,
        };

        _db.Photos.Add(photo);

        // 更新用户能量
        var user = await _db.Users.FindAsync(request.UserId);
        if (user != null)
        {
            var (r, g, b) = ParseColor(request.Analysis.DominantColor);
            user.EnergyR += r;
            user.EnergyG += g;
            user.EnergyB += b;
            user.TotalPhotos++;
            user.LastPhotoAt = DateTime.UtcNow;
        }

        await _db.SaveChangesAsync();

        return new PhotoSaveResponse
        {
            Id = photo.Id,
            EnergyChange = new EnergyChangeDto
            {
                R = user?.EnergyR ?? 0,
                G = user?.EnergyG ?? 0,
                B = user?.EnergyB ?? 0,
            },
        };
    }

    private static (int r, int g, int b) ParseColor(string hex)
    {
        // #FF6B6B → (25, 10, 10) 归一化能量增量
        var value = Convert.ToInt32(hex.TrimStart('#'), 16);
        return (
            ((value >> 16) & 255) / 10,
            ((value >> 8) & 255) / 10,
            (value & 255) / 10
        );
    }
}
```

### 3.5 Git 协作流程

#### 分支策略

```
main                  ← 稳定版本，可演示
  └── dev             ← 开发分支
       ├── feat/photo-upload          ← 前端 A
       ├── feat/ai-integration        ← 网关 B
       ├── feat/photo-api             ← 后端 C
       └── docs/poster                ← 产品 D
```

#### Commit 规范

```
<type>(<scope>): <简短中文描述>

scope 示例：frontend / gateway / backend / docs
type: feat / fix / docs / refactor / style / chore
```

示例：
```
feat(frontend): 拍照页集成相机 API
feat(gateway): 对接 GPT-4V 分析接口
feat(backend): 实现照片 CRUD 接口
fix(gateway): AI 超时后未正确降级到兜底评分
```

#### Code Review 要点

- **跨语言接口**：FastAPI 的返回格式与 C# DTO 是否对齐
- **错误传播**：C# 的错误是否被 FastAPI 正确捕获并返回给前端
- **类型安全**：TypeScript 类型与 Pydantic 模型是否一致
- **配置泄漏**：API Key、连接串等是否已提取到环境变量

---

## 4. 突发预警策略

### 4.1 风险分级

| 级别 | 定义 | 响应 |
|------|------|------|
| **P0** | 前端 → FastAPI → C# 全链路不通 | 全员暂停，集中修复 |
| **P1** | 某个模块功能不可用 | 负责人 + 1 人协助，2h 内解决 |
| **P2** | 体验/视觉问题 | 记录 issue，优先修 P0/P1 |

### 4.2 典型场景

| 场景 | 级别 | 应对 |
|------|------|------|
| GPT-4V API 超时或 key 失效 | **P0** | FastAPI 自动降级到规则评分，前端无感知 |
| C# 后端服务 down | **P1** | FastAPI 缓存最近结果，返回 cache 数据 + 标记 `source: cache` |
| 前端 CORS 配置错误 | **P1** | 检查 `config/gateway/config.dev.yaml` 的 CORS 配置 |
| 团队联调接口格式对不上 | **P1** | 以 FastAPI 的 Pydantic model 为「接口契约」，C# 和前端都对齐它 |
| 容器启动失败 | **P2** | 用 `docker compose logs` 查看具体报错 |

### 4.3 降级策略（核心）

```
GPT-4V 可用 ──→ AI 评分（主路径）
      ↓ 不可用
规则评分引擎（兜底）──→ 仍可返回评分结果
      ↓ 也不可用
返回缓存数据 + 标记 → 前端展示「上次分析结果」
```

---

## 5. AI 示例参考

> 以下示例可作为 Prompt 提供给 AI，确保其生成的代码风格与本项目一致。

### 5.1 给 AI 的风格指令模板

```
请按以下风格生成代码：

项目: ColorPal
前端 Vue 3 + TypeScript: 使用 Composition API、<script setup>、4 空格缩进
网关 FastAPI + Python: 使用 async/await、Pydantic v2、httpx
后端 C# .NET 8: 使用 Controller 模式、依赖注入、EF Core

通用要求:
- 接口返回值统一格式: { code: 0, data: ..., message: "ok" }
- 所有外部调用必须有 try/catch
- 注释用中文，解释为什么而非是什么
- 配置文件中的敏感信息使用环境变量
```

### 5.2 示例：类型定义（TypeScript ↔ Pydantic ↔ C# DTO 对齐）

```typescript
// frontend/src/types/photo.ts — TypeScript
export interface AnalysisResult {
  dominantColor: string    // "#FF6B6B"
  palette: string[]       // ["#FF6B6B", "#4ECDC4", ...]
  score: number           // 0-100
  comment: string
  colorCategory: 'warm' | 'cool' | 'neutral'
  saturationLevel: 'high' | 'medium' | 'low'
  brightnessLevel: 'high' | 'medium' | 'low'
}
```

```python
# gateway/app/models/photo.py — Pydantic (接口契约)
from pydantic import BaseModel, Field
from typing import Literal


class AnalysisResult(BaseModel):
    dominant_color: str = Field(..., pattern=r"^#[0-9a-fA-F]{6}$")
    palette: list[str]
    score: int = Field(..., ge=0, le=100)
    comment: str
    color_category: Literal["warm", "cool", "neutral"]
    saturation_level: Literal["high", "medium", "low"]
    brightness_level: Literal["high", "medium", "low"]
```

```csharp
// backend/Colopal.Api/DTOs/PhotoDto.cs — C# DTO
namespace Colopal.Api.DTOs;

public class AnalysisResultDto
{
    public string DominantColor { get; set; } = string.Empty;
    public List<string> Palette { get; set; } = new();
    public int Score { get; set; }
    public string Comment { get; set; } = string.Empty;
    public string ColorCategory { get; set; } = "neutral";
    public string SaturationLevel { get; set; } = "medium";
    public string BrightnessLevel { get; set; } = "medium";
}
```

### 5.3 示例：全链路接口格式

```typescript
// 前端调用 FastAPI 的请求/响应格式
// POST /api/v1/photo/analyze

// Request: multipart/form-data
//   image: File
//   lat?: number
//   lng?: number

// Response:
{
  "code": 0,
  "data": {
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
    "energy_change": { "r": 25, "g": 10, "b": 10 },
    "task_completed": null
  },
  "message": "ok"
}

// Error Response:
{
  "code": 40001,
  "data": null,
  "message": "不支持的图片格式，仅支持 JPEG/PNG/WebP"
}
```

### 5.4 示例：Vue 页面调用完整流程

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { uploadAndAnalyze } from '@/api/photo'
import { usePetStore } from '@/stores/pet'
import { useRouter } from 'vue-router'
import type { UploadResponse } from '@/api/photo'

const router = useRouter()
const petStore = usePetStore()
const isUploading = ref(false)

const handleFileSelected = async (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return

  isUploading.value = true

  try {
    const result: UploadResponse = await uploadAndAnalyze(file)
    // 更新本地状态
    petStore.updateEnergy(result.energyChange)
    // 跳转到结果页
    router.push({
      name: 'result',
      query: { photoId: result.photoId },
    })
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
- .NET SDK 8.0
- Docker + Docker Compose（可选）

### 6.2 启动步骤

```bash
# 1. 启动 C# 后端
cd backend/Colopal.Api
dotnet restore
dotnet run

# 2. 启动 FastAPI 网关
cd gateway
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 3. 启动 Vue 前端
cd frontend
npm install
npm run dev
```

### 6.3 服务端口

| 服务 | 端口 | 地址 |
|------|------|------|
| Vue 前端 | 5173 | http://localhost:5173 |
| FastAPI 网关 | 8000 | http://localhost:8000 |
| FastAPI Swagger | 8000 | http://localhost:8000/docs |
| C# 后端 | 5000 | http://localhost:5000 |
| C# Swagger | 5000 | http://localhost:5000/swagger |
