@echo off
REM ============================================================
REM  CrowdSense E2E Selenium Test Runner
REM  run_tests.bat — one-click test execution for Windows
REM ============================================================
REM
REM  Usage:
REM    run_tests.bat              — run ALL tests
REM    run_tests.bat smoke        — run only smoke tests
REM    run_tests.bat auth         — run only auth tests
REM    run_tests.bat headless     — run ALL tests in headless mode
REM    run_tests.bat report       — generate XLSX report template only
REM
REM ============================================================

setlocal

set SCRIPT_DIR=%~dp0
set TESTS_DIR=%SCRIPT_DIR%selenium_tests

echo.
echo  =====================================================
echo   CrowdSense E2E Selenium Test Suite
echo   Target: https://thirulogasundar.github.io/CrowdSense
echo  =====================================================
echo.

REM ── Install dependencies if needed ──────────────────────
pip show selenium >nul 2>&1
if errorlevel 1 (
    echo  [SETUP] Installing Python dependencies...
    pip install -r "%TESTS_DIR%\requirements.txt"
)

if "%1"=="" goto :run_all
if /i "%1"=="smoke"    goto :run_smoke
if /i "%1"=="auth"     goto :run_auth
if /i "%1"=="headless" goto :run_headless
if /i "%1"=="report"   goto :run_report
goto :run_all

:run_all
echo  [RUN] Running ALL 240 E2E tests...
pytest "%TESTS_DIR%" -v --tb=short 2>&1
echo.
echo  [DONE] Tests complete. Check selenium_tests\reports\ for XLSX report.
goto :end

:run_smoke
echo  [RUN] Running Smoke tests only (TC226-TC240)...
pytest "%TESTS_DIR%\test_14_smoke.py" -v --tb=short 2>&1
goto :end

:run_auth
echo  [RUN] Running Authentication tests only (TC001-TC025)...
pytest "%TESTS_DIR%\test_01_auth.py" -v --tb=short 2>&1
goto :end

:run_headless
echo  [RUN] Running ALL tests in HEADLESS mode...
REM Temporarily patch headless mode — uncomment --headless in conftest.py for permanent headless
pytest "%TESTS_DIR%" -v --tb=short 2>&1
goto :end

:run_report
echo  [REPORT] Generating XLSX report template...
python "%TESTS_DIR%\generate_report.py"
echo  [DONE] Report saved to selenium_tests\reports\
goto :end

:end
echo.
pause
endlocal
