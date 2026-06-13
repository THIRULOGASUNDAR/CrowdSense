@echo off
setlocal EnableDelayedExpansion

:: Set Android SDK Home to fix Appium crashes
set ANDROID_HOME=C:\Users\thiru\AppData\Local\Android\Sdk
set ANDROID_SDK_ROOT=C:\Users\thiru\AppData\Local\Android\Sdk
set PATH=%ANDROID_HOME%\platform-tools;%PATH%

echo ============================================================
echo   CrowdSense Appium Mobile E2E Test Suite
echo   Device: I2223  ^|  100+ Test Cases
echo ============================================================
echo.

:: 1. Check Appium Server
echo [1/5] Force restarting Appium server...
taskkill /F /IM node.exe /T >nul 2>&1
start /b cmd /c "appium --port 4723 --relaxed-security > appium_server.log 2>&1"
echo [+] Waiting 10 seconds for Appium to initialize...
ping -n 11 127.0.0.1 >nul
echo.

:: 2. Check Device Connection
echo [2/5] Checking connected Android devices...
adb devices
echo.

:: 3. Check for Debug APK
echo [3/5] Checking for debug APK...
set APK_PATH=build\app\outputs\flutter-apk\app-debug.apk
IF EXIST "%APK_PATH%" (
    echo [+] Debug APK found.
) ELSE (
    echo [-] Debug APK NOT found. Will test installed version on device.
)
echo.

:: 4. Install Dependencies
echo [4/5] Installing Python dependencies...
python -m pip install -q pytest pytest-html openpyxl appium-python-client selenium
echo [+] Dependencies ready.
echo.

:: 5. Create Reports directory
echo [5/5] Creating reports directory...
IF NOT EXIST "appium_tests\reports" mkdir "appium_tests\reports"
echo [+] Reports directory: appium_tests\reports\
echo.

echo ============================================================
echo   Starting Test Execution...
echo   100+ Test Cases 
echo ============================================================
echo.

:: Run tests
echo [RUN] Executing tests...
python -m pytest appium_tests\test_e2e_full.py %*
echo.

echo ============================================================
echo   Test Run Complete!
echo   Reports saved in: appium_tests\reports\
echo   - Excel:  CrowdSense_Appium_Report_TIMESTAMP.xlsx
echo   - HTML:   appium_report.html
echo ============================================================
pause
