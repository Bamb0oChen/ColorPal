# ColorPal - 快速启动指南

## 项目结构

```
ColorPal/
├── frontend/          # Vue 3 前端
├── gateway/           # FastAPI 后端
├── ColorDocs/         # 项目文档
└── GETTING_STARTED.md # 本文件
```

## 环境要求

- Python 3.11+
- Node.js 18+

## 启动步骤

### 1. 后端启动

```bash
# 进入后端目录
cd gateway

# 安装依赖
pip install -r requirements.txt

# 填充示例数据（可选，建议执行）
python scripts/seed_data.py

# 启动后端服务
uvicorn main:app --reload --port 8000
```

后端 API 文档地址：http://localhost:8000/docs

### 2. 前端启动

打开一个新的终端窗口：

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动前端服务
npm run dev
```

前端访问地址：http://localhost:5173

## 社区功能说明

你负责的社区模块已完全实现，包括：

### 页面
- **社区首页** (`/community`) - 动态列表，显示所有用户分享的内容
- **发布动态** (`/community/post`) - 上传图片、编辑文字并发布
- **动态详情** (`/community/post/:id`) - 查看详情、评论互动

### 功能特性
- ✅ 浏览动态列表
- ✅ 发布新动态（支持多图上传）
- ✅ 点赞/取消点赞
- ✅ 查看和发布评论
- ✅ 显示照片色彩信息（色卡 + 评分）
- ✅ 精美的 UI 设计（参考截图风格）

### 技术亮点
- 前端：Vue 3 + TypeScript + Pinia 状态管理
- 后端：FastAPI + SQLAlchemy + SQLite
- 完整的 RESTful API 设计
- 响应式布局，支持移动端

## 数据

后端会自动创建一个演示用户，并填充了示例动态数据，你可以立即看到效果！

## 下一步

项目基础框架已搭建好，其他模块（拍照、小人、任务、地图）可以参考社区模块的实现方式继续开发。
