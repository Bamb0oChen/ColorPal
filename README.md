# ColorPal — 你的色彩伙伴

> 喂它颜色，陪它成长，用新的方式看世界。
> 赛道四 · 视觉搜索

**ColorPal** 是一个「养小人」的趣味拍照应用。用户拍照后，AI 提取照片中的颜色并评分，虚拟小人「吃掉」颜色后成长进化，形成持续探索的正向循环。

---

## 快速开始

### 环境要求

- Node.js >= 18
- Python >= 3.11

### 启动后端

```bash
cd gateway
pip install -r requirements.txt
# 配置 OpenAI API Key（复制 .env.example 为 .env，填入 key）
uvicorn main:app --reload --port 8000
```

API 文档自动生成：http://localhost:8000/docs

### 启动前端

```bash
cd frontend
npm install
npm run dev
```

浏览器打开 http://localhost:5173

---

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Vue 3 + TypeScript + Vite + Pinia |
| 后端 | FastAPI + SQLAlchemy + SQLite |
| AI | GPT-4V（主路径） / Pillow 规则评分（兜底） |
| 部署 | Docker Compose |

---

## 项目结构

```
colopal/
├── frontend/           # Vue 3 前端
│   └── src/
│       ├── views/      # 5 个页面
│       ├── components/ # 组件
│       ├── stores/     # Pinia 状态
│       ├── api/        # Axios 封装
│       └── types/      # 类型定义
│
├── gateway/            # FastAPI 后端（All-in-One）
│   └── app/
│       ├── models/     # ORM 模型
│       ├── schemas/    # 请求/响应
│       ├── routers/    # API 路由
│       └── services/   # 业务逻辑
│           ├── ai_analyzer.py  # GPT-4V 分析
│           └── scorer.py       # 规则评分兜底
│
├── docs/               # 项目文档
└── docker-compose.yml  # 部署编排
```

---

## 核心玩法

1. **拍照 → AI 评分**：拍一张照片，AI 分析主色调 + 配色方案，输出 0-100 分
2. **养小人**：小人「吃掉」颜色 → 积累能量 → 成长进化
3. **做任务**：小人会发布颜色收集任务（「拍一张红色的东西」）
4. **看地图**：每次拍照自动记录位置，在地图上留下彩色足迹
5. **集图鉴**：解锁不同的颜色和地点，完成成就

---

## 模块分工

| 模块 | 成员 | 负责内容 |
|------|------|----------|
| A · 拍照评分 | 成员 1 | 拍照、AI 分析、评分展示 |
| B · 宠物任务 | 成员 2 | 小人、能量、任务系统 |
| C · 地图收集 | 成员 3 | 地图、图鉴、个人主页 |
| D · 产品设计 | 成员 4 | 文档、海报、演示 |

详见 `docs/团队分工文档.md`

---

## 开发计划

25 小时 MVP 开发，详见 `docs/技术方案文档.md`
