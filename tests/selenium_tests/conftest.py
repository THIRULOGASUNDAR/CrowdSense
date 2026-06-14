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
    """Build and save the multi-sheet Excel report."""
    suite_end = datetime.datetime.now()

    passed  = [r for r in _results if r["status"] == "PASSED"]
    failed  = [r for r in _results if r["status"] == "FAILED"]
    skipped = [r for r in _results if r["status"] == "SKIPPED"]
    total   = len(_results)
    pass_rate = round(len(passed) / total * 100, 2) if total else 0
    total_dur = sum(r["duration"] for r in _results)

    wb = openpyxl.Workbook()

    # ── Sheet 1: Summary ──────────────────────────────────────────────────────
    ws1 = wb.active
    ws1.title = "Summary"
    _write_summary_sheet(ws1, total, len(passed), len(failed), len(skipped),
                         pass_rate, total_dur, suite_end)

    # ── Sheet 2: Passed Tests ─────────────────────────────────────────────────
    ws2 = wb.create_sheet("Passed Tests")
    _write_status_sheet(ws2, passed, "PASSED", PASS_FILL)

    # ── Sheet 3: Failed Tests ─────────────────────────────────────────────────
    ws3 = wb.create_sheet("Failed Tests")
    _write_failed_sheet(ws3, failed)

    # ── Sheet 4: Skipped Tests ────────────────────────────────────────────────
    ws4 = wb.create_sheet("Skipped Tests")
    _write_status_sheet(ws4, skipped, "SKIPPED", SKIP_FILL)

    # ── Sheet 5: Execution Log ────────────────────────────────────────────────
    ws5 = wb.create_sheet("Execution Log")
    _write_log_sheet(ws5)

    # ── Sheet 6: Test Details (all tests) ─────────────────────────────────────
    ws6 = wb.create_sheet("Test Details")
    _write_details_sheet(ws6)

    # ── Sheet 7: Category Stats ───────────────────────────────────────────────
    ws7 = wb.create_sheet("Category Stats")
    _write_category_sheet(ws7)

    ts    = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    fname = os.path.join(REPORT_DIR, f"CrowdSense_E2E_Report_{ts}.xlsx")
    wb.save(fname)
    print(f"\n{'='*60}")
    print(f"  [REPORT SAVED] {fname}")
    print(f"{'='*60}\n")


# ─── Individual Sheet Writers ─────────────────────────────────────────────────

def _hdr_row(ws, columns: list[str], row: int = 1):
    """Write a bold navy header row and auto-set height."""
    for col_idx, hdr in enumerate(columns, start=1):
        c = ws.cell(row=row, column=col_idx, value=hdr)
        c.font      = WHITE_HDR
        c.fill      = HDR_FILL
        c.border    = THIN_BORDER
        c.alignment = CENTER
    ws.row_dimensions[row].height = 28


def _set_col_widths(ws, widths: list[int]):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def _write_summary_sheet(ws, total, passed, failed, skipped,
                          pass_rate, total_dur, suite_end):
    # ── Title banner ──
    ws.merge_cells("A1:H1")
    t = ws["A1"]
    t.value     = "CrowdSense — End-to-End Selenium Test Report"
    t.font      = _font(bold=True, size=18)
    t.fill      = HDR_FILL
    t.alignment = CENTER
    ws.row_dimensions[1].height = 50

    # ── App info ──
    ws.merge_cells("A2:H2")
    sub = ws["A2"]
    sub.value     = (f"Application: CrowdSense Web App  |  "
                     f"URL: https://thirulogasundar.github.io/CrowdSense  |  "
                     f"Framework: Selenium 4 + pytest  |  "
                     f"Generated: {suite_end.strftime('%Y-%m-%d %H:%M:%S')}")
    sub.font      = _font(size=9)
    sub.fill      = _fill(_BLUE)
    sub.alignment = CENTER
    ws.row_dimensions[2].height = 18

    # ── Stats cards ──
    ws.row_dimensions[3].height = 12  # spacer

    stat_data = [
        ("Total Tests",   total,      _fill("2E75B6"), _font(bold=True, size=14)),
        ("✅ Passed",      passed,     PASS_FILL,       _font(color="276221", bold=True, size=14)),
        ("❌ Failed",      failed,     FAIL_FILL,       _font(color="9C0006", bold=True, size=14)),
        ("⚠️ Skipped",    skipped,    SKIP_FILL,       _font(color="7D6608", bold=True, size=14)),
        ("Pass Rate",      f"{pass_rate}%", _fill("D9E2F3"), _font(color="1F3864", bold=True, size=14)),
        ("Duration (s)",  round(total_dur, 2), _fill("D9E2F3"), _font(color="1F3864", bold=True, size=14)),
    ]
    ws.row_dimensions[4].height = 22
    ws.row_dimensions[5].height = 38

    for col_idx, (label, value, fill, font) in enumerate(stat_data, start=1):
        lc = ws.cell(row=4, column=col_idx, value=label)
        lc.font = _font(color="000000", bold=True, size=10)
        lc.fill = fill
        lc.alignment = CENTER
        lc.border = THIN_BORDER

        vc = ws.cell(row=5, column=col_idx, value=value)
        vc.font = font
        vc.fill = fill
        vc.alignment = CENTER
        vc.border = THIN_BORDER

    # ── Info table ──
    ws.row_dimensions[6].height = 12  # spacer
    info_headers = ["Property", "Value"]
    _hdr_row(ws, info_headers, row=7)
    info_rows = [
        ("Application",       "CrowdSense"),
        ("Type",              "Flutter Web App"),
        ("Test Framework",    "Selenium 4 + pytest"),
        ("Environment",       "Production — GitHub Pages"),
        ("Base URL",          "https://thirulogasundar.github.io/CrowdSense"),
        ("Total Tests Run",   str(total)),
        ("Passed",            str(passed)),
        ("Failed",            str(failed)),
        ("Skipped",           str(skipped)),
        ("Pass Rate",         f"{pass_rate}%"),
        ("Total Duration",    f"{round(total_dur, 2)} seconds"),
        ("Suite Start",       _suite_start.strftime("%Y-%m-%d %H:%M:%S") if _suite_start else "—"),
        ("Suite End",         suite_end.strftime("%Y-%m-%d %H:%M:%S")),
        ("Prepared By",       "CrowdSense Automated Test Suite"),
        ("Report Version",    "v2.0"),
    ]
    for r_idx, (k, v) in enumerate(info_rows, start=8):
        fill = ALT_FILL if r_idx % 2 == 0 else None
        for col, val in [(1, k), (2, v)]:
            c = ws.cell(row=r_idx, column=col, value=val)
            c.font = BOLD if col == 1 else NORMAL
            c.border = THIN_BORDER
            c.alignment = LEFT
            if fill:
                c.fill = fill
        ws.row_dimensions[r_idx].height = 18

    _set_col_widths(ws, [20, 20, 20, 20, 20, 20, 10, 10])


def _write_status_sheet(ws, rows: list[dict], status: str, fill):
    title_map = {
        "PASSED":  "✅ Passed Tests",
        "SKIPPED": "⚠️ Skipped Tests",
    }
    ws.merge_cells("A1:F1")
    t = ws["A1"]
    t.value     = f"CrowdSense E2E — {title_map.get(status, status)}"
    t.font      = _font(bold=True, size=14)
    t.fill      = HDR_FILL
    t.alignment = CENTER
    ws.row_dimensions[1].height = 36

    cols = ["No.", "Category", "Module", "Test Name", "Duration (s)", "Status"]
    _hdr_row(ws, cols, row=2)

    for r_idx, r in enumerate(rows, start=3):
        vals = [r["no"], r["category"], r["module"], r["name"], r["duration"], r["status"]]
        for c_idx, val in enumerate(vals, start=1):
            c = ws.cell(row=r_idx, column=c_idx, value=val)
            c.font      = NORMAL
            c.fill      = fill
            c.border    = THIN_BORDER
            c.alignment = LEFT
        ws.row_dimensions[r_idx].height = 18

    _set_col_widths(ws, [6, 24, 32, 70, 14, 12])
    ws.freeze_panes = "A3"


def _write_failed_sheet(ws, rows: list[dict]):
    ws.merge_cells("A1:G1")
    t = ws["A1"]
    t.value     = "CrowdSense E2E — ❌ Failed Tests"
    t.font      = _font(bold=True, size=14)
    t.fill      = _fill("C00000")
    t.alignment = CENTER
    ws.row_dimensions[1].height = 36

    cols = ["No.", "Category", "Module", "Test Name", "Error / Traceback", "Duration (s)", "Timestamp"]
    _hdr_row(ws, cols, row=2)

    for r_idx, r in enumerate(rows, start=3):
        vals = [r["no"], r["category"], r["module"], r["name"],
                r["error"], r["duration"], r["ts"]]
        for c_idx, val in enumerate(vals, start=1):
            c = ws.cell(row=r_idx, column=c_idx, value=val)
            c.font      = NORMAL
            c.fill      = FAIL_FILL
            c.border    = THIN_BORDER
            c.alignment = LEFT
        ws.row_dimensions[r_idx].height = 55  # taller for error details

    _set_col_widths(ws, [6, 24, 32, 60, 90, 14, 22])
    ws.freeze_panes = "A3"


def _write_log_sheet(ws):
    ws.merge_cells("A1:D1")
    t = ws["A1"]
    t.value     = "CrowdSense E2E — Chronological Execution Log"
    t.font      = _font(bold=True, size=14)
    t.fill      = HDR_FILL
    t.alignment = CENTER
    ws.row_dimensions[1].height = 36

    _hdr_row(ws, ["Timestamp", "Level", "Category", "Message"], row=2)

    for r_idx, r in enumerate(_results, start=3):
        level = "INFO" if r["status"] == "PASSED" else ("WARN" if r["status"] == "SKIPPED" else "ERROR")
        fill  = PASS_FILL if r["status"] == "PASSED" else (SKIP_FILL if r["status"] == "SKIPPED" else FAIL_FILL)
        msg   = f"[{r['name']}] → {r['status']} in {r['duration']}s"
        if r["status"] == "FAILED":
            msg += f" | Error: {r['error'][:200]}"

        for c_idx, val in enumerate([r["ts"], level, r["category"], msg], start=1):
            c = ws.cell(row=r_idx, column=c_idx, value=val)
            c.font   = NORMAL
            c.fill   = fill
            c.border = THIN_BORDER
            c.alignment = LEFT
        ws.row_dimensions[r_idx].height = 18

    _set_col_widths(ws, [22, 10, 26, 110])
    ws.freeze_panes = "A3"


def _write_details_sheet(ws):
    ws.merge_cells("A1:I1")
    t = ws["A1"]
    t.value     = "CrowdSense E2E — Complete Test Details"
    t.font      = _font(bold=True, size=14)
    t.fill      = HDR_FILL
    t.alignment = CENTER
    ws.row_dimensions[1].height = 36

    cols = ["No.", "Category", "Module", "Test Name", "Status",
            "Duration (s)", "Error / Details", "Timestamp", "Node ID"]
    _hdr_row(ws, cols, row=2)

    for r_idx, r in enumerate(_results, start=3):
        fill = (PASS_FILL if r["status"] == "PASSED"
                else FAIL_FILL if r["status"] == "FAILED"
                else SKIP_FILL)
        vals = [r["no"], r["category"], r["module"], r["name"], r["status"],
                r["duration"], r["error"], r["ts"], r["nodeid"]]
        for c_idx, val in enumerate(vals, start=1):
            c = ws.cell(row=r_idx, column=c_idx, value=val)
            c.font      = NORMAL
            c.fill      = fill
            c.border    = THIN_BORDER
            c.alignment = LEFT
        ws.row_dimensions[r_idx].height = 22

    _set_col_widths(ws, [6, 24, 32, 68, 12, 14, 80, 22, 80])
    ws.freeze_panes = "A3"
    ws.auto_filter.ref = f"A2:I{len(_results) + 2}"


def _write_category_sheet(ws):
    ws.merge_cells("A1:F1")
    t = ws["A1"]
    t.value     = "CrowdSense E2E — Category-wise Test Statistics"
    t.font      = _font(bold=True, size=14)
    t.fill      = HDR_FILL
    t.alignment = CENTER
    ws.row_dimensions[1].height = 36

    cols = ["Category", "Total", "Passed", "Failed", "Skipped", "Pass Rate %"]
    _hdr_row(ws, cols, row=2)

    # Build per-category pivot
    cat_data: dict[str, dict] = {}
    for r in _results:
        cat = r["category"]
        if cat not in cat_data:
            cat_data[cat] = {"total": 0, "passed": 0, "failed": 0, "skipped": 0}
        cat_data[cat]["total"]   += 1
        cat_data[cat][r["status"].lower()] += 1

    for r_idx, (cat, data) in enumerate(sorted(cat_data.items()), start=3):
        total   = data["total"]
        passed  = data["passed"]
        failed  = data["failed"]
        skipped = data["skipped"]
        rate    = f"{round(passed / total * 100, 1)}%" if total else "0%"
        fill    = PASS_FILL if failed == 0 else (FAIL_FILL if passed == 0 else SKIP_FILL)

        for c_idx, val in enumerate([cat, total, passed, failed, skipped, rate], start=1):
            c = ws.cell(row=r_idx, column=c_idx, value=val)
            c.font      = NORMAL
            c.fill      = fill
            c.border    = THIN_BORDER
            c.alignment = LEFT if c_idx == 1 else CENTER
        ws.row_dimensions[r_idx].height = 20

    _set_col_widths(ws, [32, 10, 10, 10, 10, 14])


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
