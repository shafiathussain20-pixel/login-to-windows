@echo off
REM Push to GitHub Script for Windows
REM This script helps you push your code to GitHub

echo.
echo ============================================================
echo       GitHub Push Helper Script
echo ============================================================
echo.
echo Your GitHub Details:
echo   Username: shafiathussain20-pixel
echo   Repository: login-to-windows
echo.
echo Before running this script, you need:
echo   1. A GitHub Personal Access Token
echo   2. Your repository must exist on GitHub
echo.
echo To get a Personal Access Token:
echo   1. Go to: https://github.com/settings/tokens
echo   2. Click "Generate new token (classic)"
echo   3. Name it: login-app-push
echo   4. Select scopes: repo, workflow
echo   5. Generate and COPY the token
echo.
pause
echo.
set /p TOKEN="Paste your GitHub Personal Access Token (it starts with ghp_): "

echo.
echo Step 1: Adding remote repository...
git remote add origin https://shafiathussain20-pixel:%TOKEN%@github.com/shafiathussain20-pixel/login-to-windows.git
if errorlevel 1 (
    echo ERROR: Failed to add remote
    echo If you see "remote origin already exists", run:
    echo   git remote remove origin
    echo Then try this script again
    pause
    exit /b 1
)
echo ✓ Remote added

echo.
echo Step 2: Pushing code to GitHub (this may take a minute)...
git push -u origin master
if errorlevel 1 (
    echo ERROR: Failed to push
    echo Troubleshooting:
    echo   - Check your token is correct
    echo   - Check your internet connection
    echo   - Check repository exists on GitHub
    pause
    exit /b 1
)
echo ✓ Push successful!

echo.
echo ============================================================
echo       SUCCESS! Your code is now on GitHub! ✓
echo ============================================================
echo.
echo Your repository: https://github.com/shafiathussain20-pixel/login-to-windows
echo.
echo Next steps:
echo   1. Go to your GitHub repository
echo   2. Go to Settings ^> Secrets and variables ^> Actions
echo   3. Add secret: DOCKER_USERNAME = your Docker Hub username
echo   4. Add secret: DOCKER_PASSWORD = your Docker Hub token
echo.
echo Then every push will automatically:
echo   - Run 18 tests
echo   - Scan for security issues
echo   - Build Docker image
echo   - Push to Docker Hub
echo.
pause
