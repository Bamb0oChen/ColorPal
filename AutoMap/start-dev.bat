@echo off
echo ========================================
echo AutoMap - 启动开发环境
echo ========================================
echo.

echo [1/3] 启动 C# 后端...
cd backend\AutoMap.Api
start "AutoMap Backend" cmd /k "dotnet run"
cd ..\..

timeout /t 5 /nobreak > nul

echo [2/3] 启动 FastAPI 网关...
cd gateway
start "AutoMap Gateway" cmd /k "pip install -r requirements.txt && uvicorn main:app --reload --port 8000"
cd ..

timeout /t 5 /nobreak > nul

echo [3/3] 启动 Vue 前端...
cd frontend
start "AutoMap Frontend" cmd /k "npm install && npm run dev"
cd ..

echo.
echo ========================================
echo 所有服务启动中...
echo 前端: http://localhost:5173
echo 网关: http://localhost:8000/docs
echo 后端: http://localhost:5000/swagger
echo ========================================
pause
