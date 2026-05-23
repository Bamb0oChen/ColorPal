# ColorPal · 你的色彩伙伴

> 拍照养小人。AI 分析照片的色彩组合给一个 0-100 的分数，虚拟小人「吃掉」颜色逐步成长进化；照片在地图上沉淀为彩色足迹的「色彩日记」。

## 架构

```
Vue 3 (Web App) --HTTP--> FastAPI (AI + 持久化) --> Qwen/DeepSeek / HSL 兜底
                                            └----> SQLite
```

Vue + FastAPI 两层架构。详细背景与决策见 `.docs/`：

- `.docs/ColorPal-产品需求文档.md` - 产品 PRD
- `.docs/ColorPal-技术方案文档.md` - 系统设计、API、数据模型
- `.docs/ColorPal-技术开发规范文档.md` - 代码规范、目录结构、命名约定
- `.docs/ColorPal-团队分工文档.md` - 4 人 25h 排期

## 快速开始

复制环境变量模板：

```bash
cp .env.example .env
# 把 VISION_API_KEY 填上；想暂时只跑兜底评分可以留空
```

### Docker 一键启动

```bash
docker compose up --build
```

- 前端：http://localhost:8080
- 后端：http://localhost:8000
- Swagger：http://localhost:8000/docs

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

## 仓库结构

```
.
├── backend/           # FastAPI + SQLAlchemy（AI 服务 + 持久化）
├── frontend/          # Vue 3 + Vite + TypeScript
├── docker-compose.yml # 生产/演示部署
├── .env.example       # 环境变量模板
└── .docs/             # 项目文档（read-only）
```

## 已接入的后端骨架

- `GET /api/v1/health` - 前后端连通性检查
- `POST /api/v1/photo/analyze` - 照片上传、AI 分析、HSL 兜底、SQLite 持久化
- `GET /api/v1/photo/list` - 照片记录列表
- `GET /api/v1/photo/map-points` - 地图彩色点位
- `GET /api/v1/user/profile` - 用户与小人状态
- `GET /api/v1/task/current` / `POST /api/v1/task/generate` - MVP 任务骨架

## 两个技术口径

- Pet 表现层最终用 Live2D 实现，能量、心情、进化阶段只作为驱动参数，不再用 SVG/Lottie 作为正式方案。
- 图像识别主路径使用 Qwen / DeepSeek 视觉模型；后端保留 OpenAI-compatible HTTP 调用形态，方便在 Qwen 云 API、DeepSeek / DeepSeek-VL 自部署或其他兼容网关之间切换。
