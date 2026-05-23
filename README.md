# ColorPal — 你的色彩伙伴 🎨

> **赛道四 · 视觉搜索** | **25 小时 MVP** | **2026.05**

拍一张照片，AI 分析颜色并评分。你的虚拟精灵「吃掉」这个颜色，变得更开心、更漂亮。

**喂它颜色，陪它成长，用新的方式看世界。**

---

## 产品简介

ColorPal 是一个「养精灵」的趣味拍照应用。用户拍照后，AI 提取照片中的颜色并评分，虚拟精灵吸收颜色后成长进化，形成持续探索的正向循环。

- **拍照** → **AI 分析颜色** → **精灵吸收成长** → **解锁图鉴/成就** → **触发新任务**
- 36 种颜色分类 + 4 级稀有度，等你集齐
- 地图记录你的「色彩足迹」

## 快速开始

```bash
# 前端
cd frontend
npm install
npm run dev

# 后端网关（需配置 API Key；无 Key 时走 HSL 兜底）
cd ../gateway
pip install -r requirements.txt
# 配置 .env 中的 OPENAI_API_KEY
uvicorn main:app --reload --port 8000
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + TypeScript + Vite |
| AI 视觉 | Qwen/DeepSeek 兼容接口 + HSL 兜底 |
| 后端 | FastAPI |
| 数据库 | SQLite + SQLAlchemy |
| 地图 | Leaflet |

## 项目结构

```
ColorPal/
├── docs/                          # 文档
│   ├── 配色方案.md                # 颜色系统设计（36色定义/稀有度/成就）
│   ├── 视觉规范.md                # 颜色视觉呈现规则
│   ├── ai-prompt-template.md      # AI 分析 Prompt 模板
│   ├── pet-prompt.txt             # 精灵形象 Prompt
│   ├── 产品需求文档.md             # PRD
│   ├── 技术方案文档.md             # 技术方案
│   ├── 技术开发规范文档.md          # 开发规范
│   └── 团队分工文档.md             # 团队分工
├── frontend/                      # 前端源码
│   └── src/
│       ├── types/photo.ts         # 颜色系统类型定义
│       └── utils/constants.ts     # 36色常量 + 工具函数
└── gateway/                       # FastAPI 后端网关
    └── app/
        ├── models/                # SQLAlchemy ORM
        ├── routers/               # API 路由
        ├── schemas/               # Pydantic 数据模型
        └── services/              # AI 分析与业务服务
```

## 核心功能

- 📸 **拍照评分** — AI 分析照片颜色，输出评分 + 评语
- 🧚 **精灵养成** — 颜色喂食驱动成长、进化、心情变化
- 🎨 **36 色图鉴** — 按色系/稀有度分类收集
- 🏆 **成就系统** — 19 个成就等待解锁
- 🗺️ **色彩地图** — 拍照位置 + 彩色标记点
- 📤 **一键分享** — 生成今日色板/精灵名片

## 团队分工

| 角色 | 人员 | 主责 |
|------|------|------|
| A · 前端开发 | 成员 1 | App UI、相机、精灵动画 |
| B · 算法/AI | 成员 2 | 视觉模型、Prompt、评分 |
| C · 后端开发 | 成员 3 | 云函数、数据库、API |
| D · 产品/设计 | 成员 4 | 产品文档、设计规范、路演 |

## License

MIT
