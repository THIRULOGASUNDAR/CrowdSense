@echo off
REM ============================================================================
REM  CrowdSense Appium Mobile E2E Test Runner
REM  run_appium_tests.bat — one-click test execution for Windows
REM  Target Device: Pixel 3a API 37 AVD (Android Emulator)
REM ============================================================================
REM
REM  PRE-REQUISITES (run in order before executing this script):
REM    1. Start Android Studio AVD  : Pixel 3a API 37
REM    2. Start Appium server       : npx appium  (in a separate terminal)
REM    3. Build Flutter APK         : cd frontend && flutter build apk --debug
REM    4. Set credentials (optional):
REM         set CROWDSENSE_EMAIL=your@email.com
REM         set CROWDSENSE_PASSWORD=YourPassword
REM
REM  USAGE:
REM    run_appium_tests.bat              — run ALL 100 Appium tests
REM    run_appium_tests.bat smoke        — run only Smoke tests (AM091–AM100)
REM    run_appium_tests.bat auth         — run only Auth tests (AM001–AM022)
REM    run_appium_tests.bat home         — run only Home/Nav tests (AM023–AM040)
REM    run_appium_tests.bat search       — run only Search/Place tests (AM041–AM060)
REM    run_appium_tests.bat profile      — run only Profile/Settings tests (AM061–AM078)
REM    run_appium_tests.bat planner      — run only Travel Planner tests (AM079–AM090)
REM    run_appium_tests.bat report       — generate XLSX template only (no tests)
REM    run_appium_tests.bat install      — install Python dependencies only
REM
REM ============================================================================

setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
set TESTS_DIR=%SCRIPT_DIR%

REM ── Banner ──────────────────────────────────────────────────────────────────
echo.
echo  ================================================================
echo    CrowdSense Appium Mobile E2E Test Suite
echo    Target  : Pixel 3a API 37 (Android Emulator)
echo    Appium  : UiAutomator2
echo    Tests   : 100 cases (AM001 - AM100)
echo  ================================================================
echo.

REM ── Check Python ────────────────────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found. Please install Python 3.8+ and add to PATH.
    pause
    exit /b 1
)

REM ── Check Appium server ─────────────────────────────────────────────────────
echo  [CHECK] Verifying Appium server at http://127.0.0.1:4723 ...
curl -s --max-time 3 http://127.0.0.1:4723/status >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [WARNING] Appium server is NOT running at http://127.0.0.1:4723
    echo  [WARNING] Please start Appium in a separate terminal:
    echo            npx appium
    echo.
    echo  Press any key to try running tests anyway, or Ctrl+C to abort.
    pause >nul
) else (
    echo  [OK] Appium server is running.
)

REM ── Check APK ───────────────────────────────────────────────────────────────
set APK_PATH=%SCRIPT_DIR%..\frontend\build\app\outputs\flutter-apk\app-debug.apk
if not exist "%APK_PATH%" (
    echo.
    echo  [WARNING] Debug APK not found at:
    echo            %APK_PATH%
    echo.
    echo  Please build the APK first:
    echo    cd frontend
    echo    flutter build apk --debug
    echo.
    echo  Press any key to try anyway - tests will skip - or Ctrl+C to abort.
    pause >nul
) else (
    echo  [OK] APK found: app-debug.apk
)

REM ── Check ADB / Emulator ────────────────────────────────────────────────────
echo  [CHECK] Checking connected Android devices...
adb devices 2>nul | findstr "emulator" >nul
if errorlevel 1 (
    echo  [WARNING] No Android emulator detected via ADB.
    echo  [WARNING] Please launch Pixel 3a API 37 in Android Studio.
) else (
    echo  [OK] Android emulator detected.
)

REM ── Install dependencies ─────────────────────────────────────────────────────
echo.
echo  [SETUP] Checking Python dependencies...
pip show appium-python-client >nul 2>&1
if errorlevel 1 (
    echo  [SETUP] Installing dependencies from requirements.txt...
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

REM ── Route to selected mode ───────────────────────────────────────────────────
if "%1"==""        goto :run_all
if /i "%1"=="smoke"   goto :run_smoke
if /i "%1"=="auth"    goto :run_auth
if /i "%1"=="home"    goto :run_home
if /i "%1"=="search"  goto :run_search
if /i "%1"=="profile" goto :run_profile
if /i "%1"=="planner" goto :run_planner
if /i "%1"=="report"  goto :run_report
if /i "%1"=="install" goto :done
goto :run_all

REM ── Run modes ───────────────────────────────────────────────────────────────

:run_all
echo.
echo  [RUN] Running ALL 100 Appium E2E tests...
echo  [RUN] This may take 20-40 minutes depending on device speed.
echo.
python -m pytest "%TESTS_DIR%" -v --tb=short 2>&1
echo.
echo  [DONE] Full suite complete.
echo  [DONE] Check appium_tests\reports\ for the XLSX report.
goto :done

:run_smoke
echo.
echo  [RUN] Running Smoke tests only (AM091–AM100)...
python -m pytest "%TESTS_DIR%test_06_smoke.py" -v --tb=short -m smoke 2>&1
echo.
echo  [DONE] Smoke tests complete.
goto :done

:run_auth
echo.
echo  [RUN] Running Authentication tests only (AM001–AM022)...
python -m pytest "%TESTS_DIR%test_01_auth.py" -v --tb=short 2>&1
echo.
echo  [DONE] Auth tests complete.
goto :done

:run_home
echo.
echo  [RUN] Running Home & Navigation tests (AM023–AM040)...
python -m pytest "%TESTS_DIR%test_02_home_navigation.py" -v --tb=short 2>&1
echo.
echo  [DONE] Home/Navigation tests complete.
goto :done

:run_search
echo.
echo  [RUN] Running Search & Place tests (AM041–AM060)...
python -m pytest "%TESTS_DIR%test_03_search_place.py" -v --tb=short 2>&1
echo.
echo  [DONE] Search/Place tests complete.
goto :done

:run_profile
echo.
echo  [RUN] Running Profile & Settings tests (AM061–AM078)...
python -m pytest "%TESTS_DIR%test_04_profile_settings.py" -v --tb=short 2>&1
echo.
echo  [DONE] Profile/Settings tests complete.
goto :done

:run_planner
echo.
echo  [RUN] Running Travel Planner & Favorites tests (AM079–AM090)...
python -m pytest "%TESTS_DIR%test_05_travel_planner.py" -v --tb=short 2>&1
echo.
echo  [DONE] Planner/Favorites tests complete.
goto :done

:run_report
echo.
echo  [REPORT] Generating XLSX template (no tests run)...
python "%TESTS_DIR%generate_appium_report.py"
echo.
echo  [DONE] Report template saved to appium_tests\reports\
goto :done

:done
echo.
echo  ================================================================
echo    Report saved to: appium_tests\reports\
echo    Open the XLSX file in Microsoft Excel to review results.
echo  ================================================================
echo.
endlocal
pause
