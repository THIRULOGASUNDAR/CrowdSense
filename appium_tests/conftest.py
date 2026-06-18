"""
CrowdSense Appium Mobile E2E — conftest.py
==========================================
- Appium driver fixture for Pixel 3a API 37 AVD (UiAutomator2)
- Logged-in driver fixture (performs Firebase login once per module)
- pytest hooks to auto-generate 5-sheet XLSX report after test session

Environment Variables:
    CROWDSENSE_EMAIL      : Firebase login email  (default: test@crowdsense.app)
    CROWDSENSE_PASSWORD   : Firebase login password (default: Test@1234)
    APPIUM_HOST           : Appium server host     (default: 127.0.0.1)
    APPIUM_PORT           : Appium server port     (default: 4723)
    APK_PATH              : Absolute path to the debug APK
                            (default: ../frontend/build/app/outputs/flutter-apk/app-debug.apk)
"""
import os
import time
import datetime
import pytest
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

from appium import webdriver as appium_webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

# ── Configuration ─────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_APK = os.path.join(
    _HERE, "..", "frontend", "build", "app", "outputs",
    "flutter-apk", "app-debug.apk"
)

APPIUM_HOST      = os.environ.get("APPIUM_HOST",         "127.0.0.1")
APPIUM_PORT      = int(os.environ.get("APPIUM_PORT",     "4723"))
APK_PATH         = os.path.abspath(os.environ.get("APK_PATH", _DEFAULT_APK))
TEST_EMAIL       = os.environ.get("CROWDSENSE_EMAIL",    "test@crowdsense.app")
TEST_PASSWORD    = os.environ.get("CROWDSENSE_PASSWORD", "Test@1234")

APPIUM_SERVER    = f"http://{APPIUM_HOST}:{APPIUM_PORT}"
REPORTS_DIR      = os.path.join(_HERE, "reports")

# ── Excel style constants ──────────────────────────────────────────────────────
HDR_FILL     = PatternFill("solid", fgColor="1F3864")    # dark navy
PASS_FILL    = PatternFill("solid", fgColor="C6EFCE")    # light green
FAIL_FILL    = PatternFill("solid", fgColor="FFC7CE")    # light red
SKIP_FILL    = PatternFill("solid", fgColor="FFEB9C")    # amber
WHITE_FONT   = Font(name="Calibri", color="FFFFFF", bold=True)
BOLD_FONT    = Font(name="Calibri", bold=True)
NORMAL_FONT  = Font(name="Calibri")
thin         = Side(style="thin", color="B0B0B0")
THIN_BORDER  = Border(left=thin, right=thin, top=thin, bottom=thin)
CENTER       = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT         = Alignment(horizontal="left",   vertical="center", wrap_text=True)

# ── Global result store ────────────────────────────────────────────────────────
_suite_start: datetime.datetime = None
_results: list = []   # list[dict]: no, category, name, status, duration, error, ts


# ─────────────────────────────────────────────────────────────────────────────
# pytest hooks
# ─────────────────────────────────────────────────────────────────────────────

def pytest_sessionstart(session):
    global _suite_start
    _suite_start = datetime.datetime.now(datetime.timezone.utc)


def pytest_runtest_logreport(report):
    global _results
    if report.when == "call":
        if report.passed:
            status = "PASSED"
        elif report.failed:
            status = "FAILED"
        else:
            status = "SKIPPED"

        error = (
            str(report.longrepr)[:800]
            if report.failed
            else "None — test passed successfully."
        )
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _results.append({
            "no":       len(_results) + 1,
            "category": _get_category(report.nodeid),
            "name":     report.nodeid.split("::")[-1],
            "status":   status,
            "duration": round(report.duration, 2),
            "error":    error,
            "ts":       ts,
        })


def pytest_sessionfinish(session, exitstatus):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    _generate_xlsx()


# ─────────────────────────────────────────────────────────────────────────────
# Category mapping helper
# ─────────────────────────────────────────────────────────────────────────────

def _get_category(nodeid: str) -> str:
    mapping = {
        "test_01_auth":              "Authentication",
        "test_02_home_navigation":   "Home & Navigation",
        "test_03_search_place":      "Search & Place",
        "test_04_profile_settings":  "Profile & Settings",
        "test_05_travel_planner":    "Travel Planner & Favorites",
        "test_06_smoke":             "Smoke Tests",
    }
    for key, cat in mapping.items():
        if key in nodeid:
            return cat
    return "General"


# ─────────────────────────────────────────────────────────────────────────────
# XLSX report writer
# ─────────────────────────────────────────────────────────────────────────────

def _generate_xlsx():
    if not _results:
        print("\n[REPORT] No test results to write.")
        return

    suite_end = datetime.datetime.now(datetime.timezone.utc)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Test Cases"

    # ── Title banner ──
    ws.merge_cells("A1:G1")
    t = ws["A1"]
    t.value     = "CrowdSense — E2E Test Cases & Results (Appium Mobile)"
    t.font      = Font(name="Calibri", color="FFFFFF", bold=True, size=16)
    t.fill      = PatternFill("solid", fgColor="1A3A5C")
    t.alignment = CENTER
    ws.row_dimensions[1].height = 40

    # ── Metadata subtitle ──
    ws.merge_cells("A2:G2")
    sub = ws["A2"]
    sub.value = (
        f"Device: Pixel 3a API 37  |  Platform: Android  |  "
        f"Automation: UiAutomator2  |  Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    sub.font      = Font(name="Calibri", color="FFFFFF", size=10)
    sub.fill      = PatternFill("solid", fgColor="2D5F8A")
    sub.alignment = CENTER
    ws.row_dimensions[2].height = 20
    ws.row_dimensions[3].height = 10

    # Headers
    headers = ["No.", "Category", "Test Name", "Status", "Duration (s)", "Error Details", "Timestamp"]
    for col_idx, hdr in enumerate(headers, start=1):
        c = ws.cell(row=4, column=col_idx, value=hdr)
        c.font      = WHITE_FONT
        c.fill      = HDR_FILL
        c.border    = THIN_BORDER
        c.alignment = CENTER
    ws.row_dimensions[4].height = 26

    # Write test cases
    for idx, r in enumerate(_results, start=5):
        vals = [r["no"], r["category"], r["name"], r["status"], r["duration"], r["error"], r["ts"]]
        fill = (PASS_FILL if r["status"] == "PASSED" 
                else FAIL_FILL if r["status"] == "FAILED" 
                else SKIP_FILL)
        
        for c_idx, val in enumerate(vals, start=1):
            c = ws.cell(row=idx, column=c_idx, value=val)
            c.font = NORMAL_FONT
            c.border = THIN_BORDER
            c.alignment = LEFT if c_idx in (2, 3, 6) else CENTER
            if c_idx == 4:
                c.fill = fill
                c.font = BOLD_FONT
                if r["status"] == "PASSED":
                    c.font = Font(name="Calibri", color="276221", bold=True)
                elif r["status"] == "FAILED":
                    c.font = Font(name="Calibri", color="9C0006", bold=True)
                else:
                    c.font = Font(name="Calibri", color="7D6608", bold=True)

        ws.row_dimensions[idx].height = 20

    widths = [6, 24, 60, 12, 14, 80, 22]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w

    ws.freeze_panes = "A5"

    ts    = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    fname = os.path.join(REPORTS_DIR, f"Appium_E2E_Report_CrowdSense_{ts}.xlsx")
    wb.save(fname)
    print(f"\n[REPORT] Appium XLSX report saved → {fname}")


def _write_header(ws, columns, row=1):
    for col_idx, hdr in enumerate(columns, start=1):
        c = ws.cell(row=row, column=col_idx, value=hdr)
        c.font      = WHITE_FONT
        c.fill      = HDR_FILL
        c.border    = THIN_BORDER
        c.alignment = CENTER
    ws.row_dimensions[row].height = 26




# ─────────────────────────────────────────────────────────────────────────────
# Appium driver fixtures
# ─────────────────────────────────────────────────────────────────────────────

def _build_options() -> UiAutomator2Options:
    """Build Appium UiAutomator2 desired capabilities for Pixel 3a API 37."""
    options = UiAutomator2Options()
    options.platform_name          = "Android"
    options.device_name            = "emulator-5554"        # Default AVD port
    options.avd                    = "Pixel_3a"             # AVD name in Android Studio
    options.platform_version       = "13.0"                 # API 37 → Android 13
    options.app                    = APK_PATH
    options.app_package            = "com.crowdsense.app"   # Flutter app package
    options.app_activity           = "com.crowdsense.app.MainActivity"
    options.automation_name        = "UiAutomator2"
    options.no_reset               = False                  # Fresh install each session
    options.full_reset             = False
    options.new_command_timeout    = 120                    # seconds
    options.android_install_timeout= 90000                  # ms

    # Flutter semantics — required for element discovery
    options.set_capability("settings[waitForIdleTimeout]", 10)
    options.set_capability("settings[waitForSelectorTimeout]", 10000)
    options.set_capability("disableWindowAnimation", True)

    return options


@pytest.fixture(scope="session")
def driver():
    """
    Session-scoped Appium driver fixture.
    Connects to a running Appium server, installs the Flutter APK on
    the Pixel 3a API 37 AVD, and yields the driver for the full session.
    """
    if not os.path.isfile(APK_PATH):
        pytest.skip(
            f"[SKIP] APK not found at: {APK_PATH}\n"
            "Build it with: cd frontend && flutter build apk --debug"
        )

    options = _build_options()
    drv = appium_webdriver.Remote(APPIUM_SERVER, options=options)
    drv.implicitly_wait(10)
    yield drv
    drv.quit()


@pytest.fixture(scope="module")
def logged_in_driver(driver):
    """
    Module-scoped fixture that performs a Firebase login once.
    Reuses the session driver but navigates to login and signs in.
    Returns the driver already on the Home screen.
    """
    _perform_login(driver)
    yield driver


def _perform_login(drv):
    """Helper: tap email field, enter credentials, tap Sign In."""
    try:
        # Wait for login screen (email field)
        email_field = drv.find_element(AppiumBy.XPATH,
            '//*[@content-desc="Email" or @text="Email" or contains(@resource-id,"email")]')
        email_field.clear()
        email_field.send_keys(TEST_EMAIL)

        pwd_field = drv.find_element(AppiumBy.XPATH,
            '//*[@content-desc="Password" or @text="Password" or contains(@resource-id,"password")]')
        pwd_field.clear()
        pwd_field.send_keys(TEST_PASSWORD)

        sign_in_btn = drv.find_element(AppiumBy.XPATH,
            '//*[@content-desc="Sign In" or @text="Sign In" or contains(@resource-id,"sign_in")]')
        sign_in_btn.click()
        time.sleep(4)  # Wait for Firebase auth + navigation
    except Exception as e:
        print(f"[WARN] Login helper failed (may already be logged in): {e}")


@pytest.fixture
def app_package():
    return "com.crowdsense.app"


@pytest.fixture
def appium_server():
    return APPIUM_SERVER
