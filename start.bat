@echo off
chcp 65001 >nul
echo ====================================
echo 电影评分网站 - 一键启动脚本
echo ====================================
echo.

echo [1/4] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.9+
    pause
    exit /b 1
)
echo [√] Python环境正常

echo.
echo [2/4] 检查Node.js环境...
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Node.js，请先安装Node.js 16+
    pause
    exit /b 1
)
echo [√] Node.js环境正常

echo.
echo [3/4] 启动后端服务器...
cd backend
if not exist "database.db" (
    echo [提示] 首次运行，数据库将自动创建
)
start "后端服务器 - FastAPI" cmd /k "uvicorn app.main:app --reload --port 8000"
echo [√] 后端服务器已启动在 http://localhost:8000

echo.
echo [4/4] 启动前端服务器...
cd ..\frontend
if not exist "node_modules" (
    echo [提示] 首次运行，正在安装前端依赖...
    call npm install --registry=https://registry.npmmirror.com
)
start "前端服务器 - React" cmd /k "npm run dev"
echo [√] 前端服务器已启动在 http://localhost:5173

cd ..
echo.
echo ====================================
echo 启动完成！
echo ====================================
echo.
echo 后端API文档: http://localhost:8000/docs
echo 前端应用: http://localhost:5173
echo.
echo 按任意键打开浏览器访问前端应用...
pause >nul

start http://localhost:5173

echo.
echo 提示: 关闭此窗口不会停止服务器
echo 要停止服务器，请关闭对应的命令行窗口
echo.
pause
