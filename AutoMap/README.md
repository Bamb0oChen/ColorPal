# AutoMap - 智能地图探索

基于 Vue 3 + FastAPI + C# (.NET) 的全栈地图探索应用，采用多邻国风格的活泼 UI 设计。

## 功能特性

- 🗺️ **实时地图** - 基于 Leaflet 的交互式地图展示
- 🎯 **定位服务** - 浏览器 GPS 定位，快速获取当前位置
- 🔍 **智能推荐** - 根据搜索文本推荐附近景点、美食等
- 📍 **地点标记** - 美观的地图标记，带序号和分类图标
- 💼 **行程管理** - 底部卡片式地点列表，滑动浏览
- ❤️ **收藏功能** - 一键收藏喜欢的地点

## 技术栈

### 前端
- Vue 3 (Composition API + `<script setup>`)
- TypeScript
- Vite
- Pinia (状态管理)
- Vue Router
- Leaflet (地图)
- Axios

### 网关
- FastAPI
- Pydantic (数据验证)
- httpx (异步 HTTP 客户端)

### 后端
- .NET 8.0
- Entity Framework Core
- SQLite
- ASP.NET Core Web API

## 项目结构

```
AutoMap/
├── frontend/              # Vue 3 前端
│   ├── src/
│   │   ├── views/        # 页面组件
│   │   ├── components/   # 公共组件
│   │   ├── api/          # API 请求
│   │   ├── composables/  # 组合式函数
│   │   └── types/        # TypeScript 类型
│   └── package.json
├── gateway/              # FastAPI 网关
│   ├── app/
│   │   ├── routers/      # 路由
│   │   ├── services/     # 业务服务
│   │   └── models/       # Pydantic 模型
│   └── main.py
├── backend/              # C# .NET 后端
│   └── AutoMap.Api/
│       ├── Controllers/  # API 控制器
│       ├── Services/     # 业务服务
│       ├── Models/       # 数据模型
│       └── Data/         # EF Core
└── docker-compose.yml
```

## 快速开始

### 方式一：使用启动脚本 (Windows)

```bash
cd AutoMap
start-dev.bat
```

### 方式二：手动启动

#### 1. 启动 C# 后端
```bash
cd backend/AutoMap.Api
dotnet restore
dotnet run
```
后端运行在: http://localhost:5000

#### 2. 启动 FastAPI 网关
```bash
cd gateway
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
网关运行在: http://localhost:8000
API 文档: http://localhost:8000/docs

#### 3. 启动 Vue 前端
```bash
cd frontend
npm install
npm run dev
```
前端运行在: http://localhost:5173

### 方式三：Docker Compose

```bash
cd AutoMap
docker-compose up
```

## UI 设计特色

### 多邻国风格元素
- 🎨 **明亮色彩** - 主色调采用活力绿 (Primary #58cc02)
- 🔲 **圆角设计** - 所有组件采用大圆角，增加亲和力
- 📦 **卡片式布局** - 地点卡片、弹窗都采用卡片设计
- ✨ **按钮阴影** - 按钮带底部阴影，点击时有按下效果
- 🎭 **图标装饰** - 大量使用 Emoji 图标，活泼有趣

### 交互体验
- 底部向上滑动的详情面板
- 地图标记带有序号，点击高亮
- 分类标签横向滑动选择
- 实时更新的地点距离信息

## API 接口

### 获取推荐
```
POST /api/v1/map/recommend
Content-Type: application/json

{
  "query": "景点",
  "location": { "lat": 31.2304, "lng": 121.4737 }
}
```

### 获取当前位置
```
GET /api/v1/map/location
```

## 配置说明

复制 `.env.example` 为 `.env` 并配置：
- `BACKEND_BASE_URL` - C# 后端地址
- `OPENAI_API_KEY` - OpenAI API Key (可选，用于 AI 推荐)

## 开发指南

### 前端开发规范
- 使用 Composition API + `<script setup>`
- TypeScript 类型完整
- 组件命名 PascalCase
- 文件使用 2 空格缩进

### 后端开发规范
- 接口统一 JSON 格式
- 使用依赖注入
- EF Core 数据库操作
- 完整的错误处理和日志

## License

MIT
