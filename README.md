# ColorPal · 你的色彩伙伴

> 拍照养小人。AI 分析照片色彩，虚拟小人「吃掉」颜色逐步成长进化，在地图上沉淀为彩色足迹。

## 架构

```
Vue 3 + Vite (Web App)
       │
       ├── Live2D 宠物展示
       ├── Leaflet 色彩地图 + 路线规划
       ├── Agent 对话小彩
       └── 社区 / 图鉴 / 成就
               │ HTTP
               ▼
    FastAPI (AI 分析 + 持久化)
       │
       ├── Qwen VL / DeepSeek 视觉模型
       ├── Qwen Chat 对话模型 (agent_chat)
       ├── HSL 兜底评分 (scorer)
       └── SQLite (SQLAlchemy)
```

## 功能

| 模块 | 说明 |
|------|------|
| **拍照识色** | 上传照片，AI 分析主色、调色板，0-100 评分 + 文字点评 |
| **小彩宠物** | Live2D 驱动，随收集颜色成长进化，分阶段 200-500-1000 XP |
| **色彩图鉴** | 36 种标准颜色按色系/稀有度收集，全收集进度追踪 |
| **色彩地图** | Leaflet + 高德底图，附近景点颜色渲染，路线规划 |
| **AI 对话** | 小彩 Agent 浮动窗口，Qwen 驱动，可问任务/能量/拍照建议 |
| **社区** | 发布色彩故事、评论、点赞 |
| **成就系统** | 7 类收集成就 + 4 类稀有度成就 + 4 种特殊组合 |
| **每日任务** | 随机生成拍照任务，完成后奖励能量 |

## 快速开始

```bash
cp .env.example .env
# 填入 VISION_API_KEY 和 CHAT_API_KEY（均可使用 Qwen 通义千问）
```

### Docker 一键启动

```bash
docker compose up --build
```

- 前端：http://localhost:8080
- 后端：http://localhost:8000
- Swagger：http://localhost:8000/docs

### 本地开发

**后端：**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e .
uvicorn main:app --reload --port 8000
```

**前端：**
```bash
cd frontend
npm install
npm run dev
```

前端开发服默认在 http://localhost:5173，调后端 `VITE_API_BASE`（默认 `http://localhost:8000`）。

## 仓库结构

```
.
├── backend/
│   ├── app/
│   │   ├── routers/       # FastAPI 路由（auth, photo, user, task, agent, community）
│   │   ├── services/      # 业务逻辑（ai_analyzer, agent_chat, scorer, crud_*）
│   │   ├── models/        # SQLAlchemy 模型
│   │   └── schemas/       # Pydantic 请求/响应
│   ├── main.py            # 入口
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── components/    # Vue 组件（PetDisplay, AgentChatWidget, LoginPanel 等）
│   │   ├── views/         # 页面（Home, Map, Collection, Result, Profile, Community）
│   │   ├── stores/        # Pinia 状态管理
│   │   ├── api/           # HTTP 请求封装
│   │   ├── types/         # TypeScript 类型
│   │   └── router/        # Vue Router 配置
│   └── package.json
│
├── docker-compose.yml
├── .env.example
└── .docs/                 # 项目文档
```

## API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/health` | 健康检查 |
| POST | `/api/v1/auth/register` | 注册 |
| POST | `/api/v1/auth/login` | 登录 |
| POST | `/api/v1/photo/analyze` | 照片上传 + AI 分析 |
| GET | `/api/v1/photo/list` | 照片记录 |
| GET | `/api/v1/photo/map-points` | 地图点位 |
| GET | `/api/v1/user/profile` | 用户 + 宠物状态 |
| PATCH | `/api/v1/user/energy` | 更新能量 |
| GET | `/api/v1/task/current` | 当前任务 |
| POST | `/api/v1/task/generate` | 生成新任务 |
| POST | `/api/v1/agent/chat` | 小彩 AI 对话 |
| GET | `/api/v1/community/posts` | 社区帖子列表 |
| POST | `/api/v1/community/posts` | 发布帖子 |
