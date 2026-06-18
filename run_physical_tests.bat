@echo off
REM ============================================================================
REM  CrowdSense Appium Physical Device E2E Test Runner
REM  run_physical_tests.bat — Tests on a REAL phone connected via USB cable
REM
REM  HOW IT WORKS (just like Selenium opens Chrome automatically):
REM  ─────────────────────────────────────────────────────────────
REM  1. Plug your Android phone into the laptop via USB cable
REM  2. Enable USB Debugging on your phone (Settings → Developer Options)
REM  3. Run this .bat file
REM  4. Appium will AUTO-OPEN the CrowdSense app on your phone
REM  5. The app will be tested automatically — each screen is opened
REM  6. An Excel report is saved to appium_physical_device_tests\reports\
REM
REM  USAGE:
REM    run_physical_tests.bat              — run ALL 100 tests
REM    run_physical_tests.bat smoke        — run only Smoke tests (10 tests, ~5 min)
REM    run_physical_tests.bat auth         — run only Auth tests (PM001–PM022)
REM    run_physical_tests.bat home         — run only Home/Nav tests (PM023–PM040)
REM    run_physical_tests.bat search       — run only Search/Place tests (PM041–PM060)
REM    run_physical_tests.bat profile      — run only Profile/Settings tests (PM061–PM078)
REM    run_physical_tests.bat planner      — run only Travel Planner tests (PM079–PM090)
REM    run_physical_tests.bat install      — install Python dependencies only
REM    run_physical_tests.bat check        — check device + server (no tests run)
REM ============================================================================

setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
set TESTS_DIR=%SCRIPT_DIR%appium_physical_device_tests\

REM ── Banner ──────────────────────────────────────────────────────────────────
echo.
echo  ================================================================
echo    CrowdSense Appium Physical Device E2E Test Suite
echo    Mode    : REAL USB Android Device (not emulator)
echo    Appium  : UiAutomator2
echo    Tests   : 100 cases (PM001 - PM100)
echo  ================================================================
echo.

REM ── STEP 1: Check Python ────────────────────────────────────────────────────
echo  [STEP 1] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [ERROR] Python not found!
    echo  Please install Python 3.8+ from https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo  [OK] %%v found.

REM ── STEP 2: Check ADB (Android Debug Bridge) ────────────────────────────────
echo.
echo  [STEP 2] Checking ADB (Android Debug Bridge)...
adb version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [ERROR] ADB not found in PATH!
    echo.
    echo  To fix this, add ADB to your system PATH:
    echo    1. Open Android Studio
    echo    2. Go to: File - Settings - Appearance - System Settings - Android SDK
    echo    3. Copy the "Android SDK Location" path - e.g. C:\Users\you\AppData\Local\Android\Sdk
    echo    4. Add this to your PATH: ^<SDK_PATH^>\platform-tools
    echo    5. Restart this terminal and try again.
    echo.
    pause
    exit /b 1
)
echo  [OK] ADB is available.

REM ── STEP 3: Detect USB device ────────────────────────────────────────────────
echo.
echo  [STEP 3] Looking for a USB-connected Android device...
echo.

REM Run adb devices and capture output
adb devices 2>nul

REM Check for any real (non-emulator) device
set DEVICE_FOUND=0
for /f "skip=1 tokens=1,2" %%a in ('adb devices 2^>nul') do (
    if "%%b"=="device" (
        echo %%a | findstr "emulator" >nul
        if errorlevel 1 (
            set DEVICE_SERIAL=%%a
            set DEVICE_FOUND=1
            echo  [OK] Physical device detected: %%a
        )
    )
)

if "%DEVICE_FOUND%"=="0" (
    echo.
    echo  [WARNING] No USB Android device detected!
    echo.
    echo  Please do the following on your Android phone:
    echo    1. Go to Settings ^> About Phone
    echo    2. Tap "Build Number" 7 times to enable Developer Options
    echo    3. Go to Settings ^> Developer Options
    echo    4. Turn ON "USB Debugging"
    echo    5. Plug your phone into the laptop with a USB data cable
    echo       [NOT a charging-only cable]
    echo    6. On your phone, tap "Allow" when prompted for USB Debugging
    echo    7. Run this script again
    echo.
    echo  To verify: open a terminal and run:  adb devices
    echo  Your phone should appear as:  XXXXXXXXXX    device
    echo.
    echo  Press any key to continue anyway, or Ctrl+C to abort.
    pause >nul
) else (
    REM Set the detected device as the target
    set ANDROID_DEVICE_ID=%DEVICE_SERIAL%
    echo  [INFO] Tests will run on device: %DEVICE_SERIAL%
)

REM ── STEP 4: Check APK ───────────────────────────────────────────────────────
echo.
echo  [STEP 4] Checking for CrowdSense debug APK...
set APK_PATH=%SCRIPT_DIR%frontend\build\app\outputs\flutter-apk\app-debug.apk
if not exist "%APK_PATH%" (
    echo.
    echo  [WARNING] Debug APK not found at:
    echo            %APK_PATH%
    echo.
    echo  Building the APK now...
    echo  [This takes 2-3 minutes on first build]
    echo.
    cd "%SCRIPT_DIR%frontend"
    flutter build apk --debug
    if errorlevel 1 (
        echo.
        echo  [ERROR] Flutter build failed!
        echo  Make sure Flutter is installed: https://flutter.dev/docs/get-started/install
        echo  Run: flutter doctor   — to check your Flutter setup.
        echo.
        pause
        exit /b 1
    )
    cd "%SCRIPT_DIR%"
    echo  [OK] APK built successfully.
) else (
    echo  [OK] APK found: app-debug.apk
)

REM ── STEP 5: Check / Start Appium Server ─────────────────────────────────────
echo.
echo  [STEP 5] Checking Appium server at http://127.0.0.1:4723 ...
curl -s --max-time 4 http://127.0.0.1:4723/status >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [INFO] Appium server is NOT running. Starting it now...
    echo  [INFO] Opening a new terminal window for Appium...
    echo.
    start "Appium Server" cmd /k "echo Starting Appium Server... && npx appium && pause"
    echo  [INFO] Waiting 8 seconds for Appium to start...
    timeout /t 8 /nobreak >nul

    REM Check again after starting
    curl -s --max-time 5 http://127.0.0.1:4723/status >nul 2>&1
    if errorlevel 1 (
        echo.
        echo  [WARNING] Appium server may still be starting.
        echo  If tests fail with connection errors, wait for Appium to fully start
        echo  [you will see "Appium REST http interface listener started" in the other window]
        echo  then run this script again.
        echo.
        echo  Press any key to continue...
        pause >nul
    ) else (
        echo  [OK] Appium server started successfully.
    )
) else (
    echo  [OK] Appium server is already running.
)

REM ── Install Python dependencies ──────────────────────────────────────────────
echo.
echo  [SETUP] Checking Python dependencies...
pip show appium-python-client >nul 2>&1
if errorlevel 1 (
    echo  [SETUP] Installing dependencies...
    pip install -r "%TESTS_DIR%requirements.txt"
    if errorlevel 1 (
        echo  [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
    echo  [OK] Dependencies installed.
) else (
    echo  [OK] Dependencies already installed.
)

REM ── Create reports directory ─────────────────────────────────────────────────
if not exist "%TESTS_DIR%reports" (
    mkdir "%TESTS_DIR%reports"
    echo  [OK] Created reports directory.
)

REM ── Route to selected mode ────────────────────────────────────────────────────
if "%1"==""         goto :run_all
if /i "%1"=="check"   goto :check_only
if /i "%1"=="smoke"   goto :run_smoke
if /i "%1"=="auth"    goto :run_auth
if /i "%1"=="home"    goto :run_home
if /i "%1"=="search"  goto :run_search
if /i "%1"=="profile" goto :run_profile
if /i "%1"=="planner" goto :run_planner
if /i "%1"=="install" goto :done
goto :run_all

REM ── Check only ───────────────────────────────────────────────────────────────
:check_only
echo.
echo  [CHECK] Device and server check complete. No tests run.
goto :done

REM ── Run modes ────────────────────────────────────────────────────────────────

:run_all
echo.
echo  ================================================================
echo    STARTING: All 100 Physical Device Tests
echo    Your phone screen will light up and the app will open now!
echo    DO NOT touch your phone during testing.
echo    Estimated time: 25-45 minutes
echo  ================================================================
echo.
python -m pytest "%TESTS_DIR:~0,-1%" -v --tb=short 2>&1
echo.
echo  [DONE] Full suite complete.
echo  [DONE] Open the Excel report in: appium_physical_device_tests\reports\
goto :done

:run_smoke
echo.
echo  ================================================================
echo    STARTING: Smoke Tests Only (PM091-PM100) — ~5 minutes
echo    Your phone screen will light up and the app will open now!
echo  ================================================================
echo.
python -m pytest "%TESTS_DIR%test_06_smoke.py" -v --tb=short -m smoke 2>&1
echo.
echo  [DONE] Smoke tests complete.
goto :done

:run_auth
echo.
echo  ================================================================
echo    STARTING: Authentication Tests (PM001-PM022)
echo    Your phone screen will light up and the app will open now!
echo  ================================================================
echo.
python -m pytest "%TESTS_DIR%test_01_auth.py" -v --tb=short 2>&1
echo.
echo  [DONE] Auth tests complete.
goto :done

:run_home
echo.
echo  ================================================================
echo    STARTING: Home & Navigation Tests (PM023-PM040)
echo    Your phone screen will light up and the app will open now!
echo  ================================================================
echo.
python -m pytest "%TESTS_DIR%test_02_home_navigation.py" -v --tb=short 2>&1
echo.
echo  [DONE] Home/Navigation tests complete.
goto :done

:run_search
echo.
echo  ================================================================
echo    STARTING: Search & Place Tests (PM041-PM060)
echo    Your phone screen will light up and the app will open now!
echo  ================================================================
echo.
python -m pytest "%TESTS_DIR%test_03_search_place.py" -v --tb=short 2>&1
echo.
echo  [DONE] Search/Place tests complete.
goto :done

:run_profile
echo.
echo  ================================================================
echo    STARTING: Profile & Settings Tests (PM061-PM078)
echo    Your phone screen will light up and the app will open now!
echo  ================================================================
echo.
python -m pytest "%TESTS_DIR%test_04_profile_settings.py" -v --tb=short 2>&1
echo.
echo  [DONE] Profile/Settings tests complete.
goto :done

:run_planner
echo.
echo  ================================================================
echo    STARTING: Travel Planner & Favorites Tests (PM079-PM090)
echo    Your phone screen will light up and the app will open now!
echo  ================================================================
echo.
python -m pytest "%TESTS_DIR%test_05_travel_planner.py" -v --tb=short 2>&1
echo.
echo  [DONE] Planner/Favorites tests complete.
goto :done

:done
echo.
echo  ================================================================
echo    Test Report Location:
echo    %TESTS_DIR%reports\
echo.
echo    Open the .xlsx file in Microsoft Excel to see full results.
echo    The report has 5 sheets: Summary, Passed, Failed, Log, Details
echo  ================================================================
echo.
endlocal
pause
