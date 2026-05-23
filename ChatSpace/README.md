# ColorPal - 你的色彩伙伴

喂它颜色，陪它成长，用新的方式看世界。

## 项目简介

ColorPal 是一个趣味拍照应用：
- 拍照 → AI 分析颜色并评分
- 虚拟小人"吃掉"颜色成长
- 探索社区，分享你的色彩发现

## 技术栈

- 前端：Vue 3 + TypeScript + Vite + Pinia
- 后端：FastAPI + SQLAlchemy + SQLite
- AI：GPT-4V + 规则评分引擎

## 快速开始

### 前端

```bash
cd frontend
npm install
npm run dev
```

### 后端

```bash
cd gateway
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## 项目结构

```
colopal/
├── frontend/          # Vue 3 前端
├── gateway/           # FastAPI 后端
├── ColorDocs/         # 项目文档
└── assets/            # 设计资源
```
