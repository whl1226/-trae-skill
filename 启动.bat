@echo off
chcp 65001 >nul
echo ========================================
echo   Trae Skill 一键导入工具
echo ========================================
echo.
python skill_importer.py
if errorlevel 1 (
    echo.
    echo 运行出错！请确保已安装Python。
    pause
)
