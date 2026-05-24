# ColorPal · 你的色彩伙伴

![ColorPal hero](./hero.png)

> 拍照养小彩。AI 分析照片的色彩组合，给出 0-100 色彩评分，把主色映射到图鉴标准色，
> 并把颜色能量喂给虚拟伙伴；照片会沉淀为地图上的彩色足迹，也可以分享到社区。

## 架构

```text
Vue 3 + Vite + Pinia
  └── HTTP / multipart upload
FastAPI + SQLAlchemy
  ├── Qwen/DeepSeek-compatible vision/chat API
  ├── Pillow/HSL 本地兜底分析
  ├── SQLite 持久化
  └── /uploads 静态图片服务
```

Vue + FastAPI 两层架构。详细背景与决策见 `.docs/`：

- `.docs/ColorPal-产品需求文档.md` - 产品 PRD
- `.docs/ColorPal-技术方案文档.md` - 系统设计、API、数据模型
- `.docs/ColorPal-技术开发规范文档.md` - 代码规范、目录结构、命名约定
- `.docs/ColorPal-前端开发规范.md` - 前端页面、组件、状态与交互约定
- `.docs/ColorPal-团队分工文档.md` - 4 人 25h 排期

## 当前功能

- 照片上传分析：`POST /api/v1/photo/analyze` 调用视觉模型，失败时自动走 Pillow/HSL 兜底。
- 图鉴标准色：分析结果会映射到 `frontend/src/utils/constants.ts` 的 36 种标准色。
- 小彩养成：照片颜色转为 RGB 能量，驱动小彩能量、心情和阶段展示。
- 结果页：展示图鉴标准色名、色彩评分、参考色块、能量变化和低亮度辅助效果。
- 颜色图鉴：按色系、稀有度查看收集状态，首次收集新颜色会出现图鉴红点提醒。
- 地图日记：保存照片经纬度，地图页展示彩色足迹，并支持路线规划输入。
- 社区：本地 SQLite 社区 feed、发帖、上传图片、点赞、评论和我的帖子。
- 小彩对话：浮动 Agent 对话框；模型不可用时返回本地兜底回复。

## 快速开始

复制环境变量模板：

```bash
cp .env.example .env
# 把 VISION_API_KEY 填上；想暂时只跑兜底分析可以留空
# CHAT_* 留空时会复用 VISION_*，再失败会走本地兜底回复
```

### Docker 一键启动

```bash
docker compose up --build
```

- 前端：http://localhost:8080
- 后端：http://localhost:8000
- Swagger：http://localhost:8000/docs

Docker Compose 会创建两个命名卷：

- `colorpal-data` - SQLite 数据库
- `colorpal-uploads` - 社区上传图片

常用可选环境变量：

```bash
FRONTEND_PORT=8080
BACKEND_PORT=8000
VITE_API_BASE=http://localhost:8000
VITE_AMAP_WEB_SERVICE_KEY=你的高德Web服务Key
PUBLIC_API_BASE_URL=http://localhost:8000
```

如果把服务部署到非本机域名，需要同步设置 `VITE_API_BASE`、`PUBLIC_API_BASE_URL` 和
`CORS_ALLOW_ORIGINS`，然后重新 `docker compose up --build`，因为前端 API 地址会在 Vite
构建时写入静态资源。

### 本地开发（不用 Docker）

后端：

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e .
uvicorn main:app --reload --port 8000
```

前端：

```bash
cd frontend
npm install
npm run dev
```

前端开发服默认在 http://localhost:5173，会去调 `VITE_API_BASE`（默认 `http://localhost:8000`）的 `/api/v1/health`。
地图页周边景点搜索会读取仓库根目录 `.env` 里的 `VITE_AMAP_WEB_SERVICE_KEY`。

常用检查：

```bash
cd frontend && npm run build
cd backend && python -m pytest
cd backend && python -m ruff check .
```

## 仓库结构

```text
.
├── backend/
│   ├── app/routers/      # health/photo/user/task/agent/community API
│   ├── app/services/     # AI 分析、评分、CRUD、Agent 对话等业务逻辑
│   ├── app/models/       # SQLAlchemy 模型
│   ├── app/schemas/      # Pydantic 响应/请求结构
│   └── data/             # 本地 SQLite 数据
├── frontend/
│   └── src/
│       ├── api/          # typed API wrappers
│       ├── components/   # Live2D/Pet、社区、上传、路线输入等组件
│       ├── stores/       # Pinia 状态：palette/pet/community/route
│       ├── utils/        # 标准色图鉴、Live2D、demo pet
│       └── views/        # Home/Result/Collection/Map/Profile/Community
├── docker-compose.yml    # 生产/演示部署
├── .env.example          # 环境变量模板
└── .docs/                # 项目文档（read-only）
```

## 已接入的 API

- `GET /api/v1/health` - 前后端连通性检查
- `POST /api/v1/photo/analyze` - 照片上传、AI 分析、HSL 兜底、SQLite 持久化
- `GET /api/v1/photo/list` - 照片记录列表
- `GET /api/v1/photo/map-points` - 地图彩色点位
- `GET /api/v1/user/profile` - 用户与小人状态
- `POST /api/v1/user/energy` - 同步用户能量和累计经验值
- `GET /api/v1/task/current` / `POST /api/v1/task/generate` - MVP 任务骨架
- `POST /api/v1/agent/chat` - 小彩 Agent 对话，本地兜底回复
- `GET /api/v1/community/posts` - 社区帖子列表
- `GET /api/v1/community/posts/mine` - 当前用户帖子列表
- `POST /api/v1/community/posts` - 创建社区帖子，支持图片上传
- `GET /api/v1/community/posts/{post_id}` - 帖子详情
- `POST /api/v1/community/posts/{post_id}/like` - 点赞/取消点赞
- `GET /api/v1/community/posts/{post_id}/comments` - 评论列表
- `POST /api/v1/community/posts/{post_id}/comments` - 创建评论
- `POST /api/v1/community/dev/inject` - 注入社区调试帖子

## 技术口径

- Pet 表现层使用 Live2D/Pixi，能量、心情、进化阶段作为驱动参数。
- 图像识别主路径使用 Qwen / DeepSeek 视觉模型；后端保留 OpenAI-compatible HTTP 调用形态，方便在 Qwen 云 API、DeepSeek / DeepSeek-VL 自部署或其他兼容网关之间切换。
- AI 输出必须被后端校验和归一化；模型异常、超时、缺 key 或颜色明显失真时使用本地兜底/校正。
- 图鉴展示以 `frontend/src/utils/constants.ts` 的标准色为准，前端不要直接展示任意模型 HEX 作为颜色名称。
- 社区当前为 FastAPI + SQLite MVP；未来接 GitHub Discussions 时应继续由后端适配，不把 GitHub 机制直接暴露给前端。
