@echo off
chcp 65001 >nul
echo ====================================
echo 电影评分网站 - 停止所有服务
echo ====================================
echo.

echo [1/2] 停止后端服务器 (uvicorn)...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq 后端服务器*" >nul 2>&1
if errorlevel 1 (
    echo [提示] 后端服务器未运行或已停止
) else (
    echo [√] 后端服务器已停止
)

echo.
echo [2/2] 停止前端服务器 (node)...
taskkill /F /IM node.exe /FI "WINDOWTITLE eq 前端服务器*" >nul 2>&1
if errorlevel 1 (
    echo [提示] 前端服务器未运行或已停止
) else (
    echo [√] 前端服务器已停止
)

echo.
echo ====================================
echo 所有服务已停止
echo ====================================
echo.
pause
