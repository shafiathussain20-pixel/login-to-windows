@echo off
REM Docker Registry Push Script for Windows

setlocal enabledelayedexpansion

REM Configuration
set REGISTRY=%1
if "!REGISTRY!"=="" set REGISTRY=docker.io

set USERNAME=%2
if "!USERNAME!"=="" set USERNAME=your-username

set IMAGE_NAME=login-app
set IMAGE_TAG=latest
set FULL_IMAGE_NAME=!USERNAME!/!IMAGE_NAME!:!IMAGE_TAG!

echo.
echo ==========================================
echo Docker Registry Push Script
echo ==========================================
echo Registry: !REGISTRY!
echo Image: !FULL_IMAGE_NAME!
echo.

REM Step 1: Login to registry
echo [1/4] Logging into !REGISTRY!...
docker login -u !USERNAME! !REGISTRY!
if errorlevel 1 (
    echo ❌ Login failed. Exiting.
    exit /b 1
)
echo ✓ Login successful
echo.

REM Step 2: Build the image
echo [2/4] Building image: !FULL_IMAGE_NAME!...
docker build -t !FULL_IMAGE_NAME! .
if errorlevel 1 (
    echo ❌ Build failed. Exiting.
    exit /b 1
)
echo ✓ Build successful
echo.

REM Step 3: Run tests (optional)
echo [3/4] Running unit tests...
docker run --rm !FULL_IMAGE_NAME! python -m unittest test_app.py -v
if errorlevel 1 (
    echo ⚠ Tests failed, but continuing with push...
) else (
    echo ✓ All tests passed
)
echo.

REM Step 4: Push to registry
echo [4/4] Pushing image to !REGISTRY!...
docker push !FULL_IMAGE_NAME!
if errorlevel 1 (
    echo ❌ Push failed. Exiting.
    exit /b 1
)
echo ✓ Push successful
echo.

echo ==========================================
echo ✓ Successfully pushed !FULL_IMAGE_NAME!
echo ==========================================
echo.
echo To pull this image later, run:
echo   docker pull !FULL_IMAGE_NAME!
echo.
echo To run the image, use:
echo   docker run -it -v ./users.db:/app/users.db !FULL_IMAGE_NAME!
