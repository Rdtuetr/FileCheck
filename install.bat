@echo off
setlocal enabledelayedexpansion

:: 检查是否以管理员权限运行
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 请以管理员权限运行此脚本
    pause
    exit /b 1
)

:: 检查Python是否已安装
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo Python未安装，请先安装Python
    pause
    exit /b 1
)

:: 安装PyInstaller
echo 正在安装PyInstaller...
pip install pyinstaller

:: 使用PyInstaller创建程序
echo 正在创建程序...
cd /d "%~dp0"
pyinstaller --onefile --name filec filecheck.py --noconfirm

:: 创建安装目录
set "INSTALL_DIR=%ProgramFiles%\FileCheck"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: 复制可执行文件
copy /Y "dist\filec.exe" "%INSTALL_DIR%"

:: 添加到PATH环境变量
echo 正在配置用户环境变量...
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path ^| findstr /i "^[[:space:]]*Path"') do set "CURRENT_PATH=%%b"

echo %CURRENT_PATH% | findstr /i /c:"%INSTALL_DIR%" >nul
if %errorLevel% neq 0 (
    setx /M PATH "%CURRENT_PATH%;%INSTALL_DIR%"
)

:: 清理临时文件
rd /s /q build
rd /s /q dist
del /q filec.spec

echo 安装完成，现在可以在命令行中使用filec命令了
echo 请重新打开命令提示符或PowerShell以使命令生效
pause