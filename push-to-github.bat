@echo off
chcp 65001 >nul
echo ========================================
echo   推送暑假补习计划到 GitHub
echo ========================================
echo.
cd /d "C:\Users\Tebon\BangMaker\Claw"
git push origin main
echo.
if %errorlevel% equ 0 (
    echo ✅ 推送成功！
    echo 查看: https://github.com/Levi-Li1/food-picker
) else (
    echo ❌ 推送失败，请检查网络或 GitHub 登录状态
)
pause
