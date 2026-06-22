"""
CrowdSense Selenium E2E — conftest.py
======================================
Central pytest configuration for the CrowdSense Selenium test suite.

Features:
  • Chrome WebDriver setup with WebDriverManager auto-install
  • Module-scoped driver (fast, shared per test module)
  • Auto-generates a detailed Excel (.xlsx) report after every run:
      Sheet 1: Summary        – overall pass/fail/skip counts & timings
      Sheet 2: Passed Tests   – green rows for every passed test
      Sheet 3: Failed Tests   – red rows with full error details
      Sheet 4: Skipped Tests  – yellow rows for skipped tests
      Sheet 5: Execution Log  – chronological INFO/ERROR/SKIP log
      Sheet 6: Test Details   – full table: all tests with status & error
      Sheet 7: Category Stats – breakdown by feature area (pivot-style)

Usage:
  pip install -r requirements.txt
  pytest selenium_tests/ -v
  pytest selenium_tests/ -v --html=report.html  (optional HTML report)
"""
from __future__ import annotations

import datetime
import os
import traceback

import openpyxl
import pytest
from openpyxl.styles import (Alignment, Border, Font, PatternFill, Side)
from openpyxl.utils import get_column_letter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

try:
    from webdriver_manager.chrome import ChromeDriverManager
    _USE_WDM = True
except ImportError:
    _USE_WDM = False

# ─── App Settings ─────────────────────────────────────────────────────────────
BASE_URL = "https://thirulogasundar.github.io/CrowdSense"

# ─── Report output directory ──────────────────────────────────────────────────
REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

# ─── Colour Palette (Professional) ───────────────────────────────────────────
_NAVY       = "1F3864"   # dark navy  — headers
_BLUE       = "2E75B6"   # medium blue — sub-headers
_PASS_BG    = "C6EFCE"   # soft green  — passed
_FAIL_BG    = "FFC7CE"   # soft red    — failed
_SKIP_BG    = "FFEB9C"   # soft amber  — skipped
_ALT_BG     = "EBF2FA"   # light blue  — alternate rows
_WHITE      = "FFFFFF"

# ─── openpyxl Helpers ─────────────────────────────────────────────────────────
def _fill(hex_color: str) -> PatternFill:
    return PatternFill("solid", fgColor=hex_color)

def _font(color=_WHITE, bold=False, size=11, name="Calibri") -> Font:
    return Font(name=name, color=color, bold=bold, size=size)

def _border() -> Border:
    s = Side(style="thin", color="B0B0B0")
    return Border(left=s, right=s, top=s, bottom=s)

CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT   = Alignment(horizontal="left",   vertical="center", wrap_text=True)

HDR_FILL   = _fill(_NAVY)
SUBHDR_FILL= _fill(_BLUE)
PASS_FILL  = _fill(_PASS_BG)
FAIL_FILL  = _fill(_FAIL_BG)
SKIP_FILL  = _fill(_SKIP_BG)
ALT_FILL   = _fill(_ALT_BG)
WHITE_HDR  = _font(bold=True, size=11)
BOLD       = _font(color="000000", bold=True, size=10)
NORMAL     = _font(color="000000", bold=False, size=10)
THIN_BORDER= _border()

# ─── Result store ─────────────────────────────────────────────────────────────
_suite_start: datetime.datetime | None = None
_results: list[dict] = []


# ─── Category mapping ─────────────────────────────────────────────────────────
_CATEGORY_MAP = {
    "test_01_auth":                     "Authentication",
    "test_02_home":                     "Home & Navigation",
    "test_03_search":                   "Search & Discovery",
    "test_04_place":                    "Place Details",
    "test_05_crowd":                    "Crowd Intelligence",
    "test_06_profile":                  "Profile & Account",
    "test_07_favorites":                "Favorites",
    "test_08_planner":                  "Travel Planner",
    "test_09_settings":                 "Settings",
    "test_10_ui_responsive":            "UI/UX & Responsiveness",
    "test_11_performance":              "Performance",
    "test_12_edge":                     "Edge Cases",
    "test_13_accessibility":            "Accessibility",
    "test_14_smoke":                    "Smoke Tests",
    "test_15_real_e2e":                 "E2E Integration Journeys",
    "test_16_vulnerability":            "Vulnerability Tests",
}

def _get_category(nodeid: str) -> str:
    for key, cat in _CATEGORY_MAP.items():
        if key in nodeid:
            return cat
    return "General"


# ─── Pytest Hooks ─────────────────────────────────────────────────────────────
def pytest_sessionstart(session):
    global _suite_start
    _suite_start = datetime.datetime.now()


def pytest_runtest_logreport(report):
    if report.when == "call" or (report.when == "setup" and report.skipped):
        if report.passed:
            status = "PASSED"
            error  = "—"
        elif report.failed:
            status = "FAILED"
            error  = str(report.longrepr)[:1200]
        else:
            status = "SKIPPED"
            error  = str(report.longrepr)[:400] if report.longrepr else "Skipped"

        _results.append({
            "no":       len(_results) + 1,
            "category": _get_category(report.nodeid),
            "module":   report.nodeid.split("::")[0].replace("selenium_tests/", "").replace("\\", "/"),
            "name":     report.nodeid.split("::")[-1],
            "nodeid":   report.nodeid,
            "status":   status,
            "duration": round(report.duration, 3),
            "error":    error,
            "ts":       datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })


def pytest_sessionfinish(session, exitstatus):
    if _results:
        _generate_xlsx_report()


# ─── XLSX Report Generator ────────────────────────────────────────────────────
def _generate_xlsx_report():
    """Build and save a single-sheet Excel E2E test report."""
    suite_end = datetime.datetime.now()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Test Cases"
    
    # ── Title banner ──
    ws.merge_cells("A1:H1")
    t = ws["A1"]
    t.value     = "CrowdSense — E2E Test Cases & Results (Web)"
    t.font      = _font(bold=True, size=16)
    t.fill      = HDR_FILL
    t.alignment = CENTER
    ws.row_dimensions[1].height = 40

    # ── Metadata subtitle ──
    ws.merge_cells("A2:H2")
    sub = ws["A2"]
    sub.value     = (f"Base URL: https://thirulogasundar.github.io/CrowdSense  |  "
                     f"Framework: Selenium 4 + pytest  |  "
                     f"Generated: {suite_end.strftime('%Y-%m-%d %H:%M:%S')}")
    sub.font      = _font(size=10)
    sub.fill      = SUBHDR_FILL
    sub.alignment = CENTER
    ws.row_dimensions[2].height = 20

    # Spacer
    ws.row_dimensions[3].height = 10

    # Headers
    headers = ["No.", "Category", "Module", "Test Case Name", "Status", "Duration (s)", "Error Details", "Timestamp"]
    for col_idx, hdr in enumerate(headers, start=1):
        c = ws.cell(row=4, column=col_idx, value=hdr)
        c.font      = WHITE_HDR
        c.fill      = HDR_FILL
        c.border    = THIN_BORDER
        c.alignment = CENTER
    ws.row_dimensions[4].height = 26

    # Write test cases
    for idx, r in enumerate(_results, start=5):
        vals = [r["no"], r["category"], r["module"], r["name"], r["status"], r["duration"], r["error"], r["ts"]]
        fill = (PASS_FILL if r["status"] == "PASSED" 
                else FAIL_FILL if r["status"] == "FAILED" 
                else SKIP_FILL)
        
        for c_idx, val in enumerate(vals, start=1):
            c = ws.cell(row=idx, column=c_idx, value=val)
            c.font = NORMAL
            c.border = THIN_BORDER
            c.alignment = LEFT if c_idx in (2, 3, 4, 7) else CENTER
            if c_idx == 5:
                c.fill = fill
                c.font = BOLD
                if r["status"] == "PASSED":
                    c.font = _font(color="276221", bold=True, size=10)
                elif r["status"] == "FAILED":
                    c.font = _font(color="9C0006", bold=True, size=10)
                else:
                    c.font = _font(color="7D6608", bold=True, size=10)

        ws.row_dimensions[idx].height = 20

    # Column widths
    widths = [6, 24, 28, 60, 12, 14, 80, 22]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    ws.freeze_panes = "A5"
    
    ts = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    fname = os.path.join(REPORT_DIR, f"CrowdSense_E2E_Report_{ts}.xlsx")
    wb.save(fname)
    print(f"\n[REPORT SAVED] {fname}\n")


# ─── Selenium WebDriver Fixture ───────────────────────────────────────────────

@pytest.fixture(scope="module")
def driver():
    """Module-scoped Chrome WebDriver (shared across all tests in a module)."""
    opts = Options()
    opts.add_argument("--disable-notifications")
    opts.add_argument("--disable-infobars")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--log-level=3")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--remote-debugging-port=9222")
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Auto-enable headless mode in CI (GitHub Actions sets CI=true).
    # Locally, Chrome opens a real window for easy debugging.
    if os.environ.get("CI"):
        opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
    else:
        opts.add_argument("--start-maximized")

    if _USE_WDM:
        service = Service(ChromeDriverManager().install())
    else:
        service = Service()

    drv = webdriver.Chrome(service=service, options=opts)
    drv.implicitly_wait(10)
    drv.set_page_load_timeout(30)
    yield drv
    drv.quit()


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL
