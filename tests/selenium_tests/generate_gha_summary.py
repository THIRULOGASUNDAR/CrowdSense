#!/usr/bin/env python3
"""
generate_gha_summary.py
=======================
Reads the pytest JSON report and writes a rich Markdown summary
to the GitHub Actions Step Summary ($GITHUB_STEP_SUMMARY).

Usage (called from workflow):
    python tests/selenium_tests/generate_gha_summary.py \
        --json  tests/selenium_tests/reports/report.json \
        --branch main \
        --sha abc1234 \
        --xlsx  CrowdSense_E2E_Report_2026-06-13.xlsx
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime

# ── Status emoji map ──────────────────────────────────────────
STATUS_ICON = {"passed": "✅", "failed": "❌", "error": "❌", "skipped": "⚠️"}
STATUS_LABEL = {"passed": "PASSED", "failed": "FAILED", "error": "FAILED", "skipped": "SKIPPED"}

# ── Category map (mirrors conftest.py) ────────────────────────
CATEGORY_MAP = {
    "test_01_auth":            "🔐 Authentication",
    "test_02_home":            "🏠 Home & Navigation",
    "test_03_search":          "🔍 Search & Discovery",
    "test_04_place":           "📍 Place Details",
    "test_05_crowd":           "👥 Crowd Intelligence",
    "test_06_profile":         "👤 Profile & Account",
    "test_07_favorites":       "❤️  Favorites",
    "test_08_planner":         "🗺️  Travel Planner",
    "test_09_settings":        "⚙️  Settings",
    "test_10_ui_responsive":   "📱 UI/UX & Responsiveness",
    "test_11_performance":     "⚡ Performance",
    "test_12_edge":            "🔬 Edge Cases",
    "test_13_accessibility":   "♿ Accessibility",
    "test_14_smoke":           "💨 Smoke Tests",
    "test_15_real_e2e":        "🔄 E2E Integration",
}


def get_category(nodeid: str) -> str:
    for key, cat in CATEGORY_MAP.items():
        if key in nodeid:
            return cat
    return "📦 General"


def parse_report(json_path: str) -> dict:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    tests = data.get("tests", [])
    summary = data.get("summary", {})

    total   = summary.get("total", len(tests))
    passed  = summary.get("passed", 0)
    failed  = summary.get("failed", 0) + summary.get("error", 0)
    skipped = summary.get("skipped", 0)
    duration = round(data.get("duration", 0), 2)

    pass_rate = round(passed / total * 100, 1) if total else 0.0

    # ── Per-category stats ────────────────────────────────────
    cats: dict[str, dict] = defaultdict(lambda: {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "duration": 0.0})
    failed_tests: list[dict] = []

    for t in tests:
        outcome = t.get("outcome", "unknown")
        cat = get_category(t.get("nodeid", ""))
        cats[cat]["total"]    += 1
        cats[cat]["duration"] += t.get("duration", 0.0) or 0.0
        if outcome == "passed":
            cats[cat]["passed"] += 1
        elif outcome in ("failed", "error"):
            cats[cat]["failed"] += 1
            failed_tests.append({
                "nodeid":   t.get("nodeid", ""),
                "category": cat,
                "duration": round(t.get("duration", 0.0) or 0.0, 2),
                "error":    _extract_error(t),
            })
        elif outcome == "skipped":
            cats[cat]["skipped"] += 1

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "pass_rate": pass_rate,
        "duration": duration,
        "categories": dict(cats),
        "failed_tests": failed_tests,
    }


def _extract_error(t: dict) -> str:
    """Pull the first meaningful error line from a test entry."""
    for phase in ("call", "setup", "teardown"):
        longrepr = t.get(phase, {}) or {}
        if isinstance(longrepr, dict):
            crash = longrepr.get("crash", {}) or {}
            msg = crash.get("message", "")
            if msg:
                # Return only the first 200 chars to keep table readable
                return msg.strip()[:200]
        elif isinstance(longrepr, str) and longrepr:
            return longrepr.strip()[:200]
    return "—"


def overall_badge(pass_rate: float) -> str:
    if pass_rate >= 90:
        return "🟢 **EXCELLENT**"
    elif pass_rate >= 70:
        return "🟡 **GOOD**"
    elif pass_rate >= 50:
        return "🟠 **NEEDS ATTENTION**"
    else:
        return "🔴 **CRITICAL**"


def write_summary(args: argparse.Namespace, stats: dict) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    out = open(summary_path, "a", encoding="utf-8") if summary_path else sys.stdout

    w = out.write

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    badge = overall_badge(stats["pass_rate"])

    # ═══════════════════════════════════════════════════════════
    # HEADER
    # ═══════════════════════════════════════════════════════════
    w("# 📊 CrowdSense E2E Test — Final Analysis\n\n")
    w(f"> **Run:** `{now}` &nbsp;|&nbsp; **Branch:** `{args.branch}` &nbsp;|&nbsp; **Commit:** `{args.sha}`\n\n")
    w(f"> **App URL:** https://thirulogasundar.github.io/CrowdSense\n\n")
    w("---\n\n")

    # ═══════════════════════════════════════════════════════════
    # SCORECARD
    # ═══════════════════════════════════════════════════════════
    w("## 🏆 Overall Result\n\n")
    w(f"### {badge} &nbsp; — &nbsp; Pass Rate: **{stats['pass_rate']}%**\n\n")
    w("| Metric | Value |\n")
    w("|--------|-------|\n")
    w(f"| 🧪 Total Tests Run | **{stats['total']}** |\n")
    w(f"| ✅ Passed | **{stats['passed']}** |\n")
    w(f"| ❌ Failed | **{stats['failed']}** |\n")
    w(f"| ⚠️ Skipped | **{stats['skipped']}** |\n")
    w(f"| 📈 Pass Rate | **{stats['pass_rate']}%** |\n")
    w(f"| ⏱️ Total Duration | **{stats['duration']}s** |\n")
    if args.xlsx:
        w(f"| 📄 XLSX Report | `{args.xlsx}` (download from Artifacts ↓) |\n")
    w("\n---\n\n")

    # ═══════════════════════════════════════════════════════════
    # CATEGORY BREAKDOWN
    # ═══════════════════════════════════════════════════════════
    w("## 📂 Category-wise Breakdown\n\n")
    w("| Category | Total | ✅ Passed | ❌ Failed | ⚠️ Skipped | Pass Rate | Status |\n")
    w("|----------|-------|-----------|-----------|------------|-----------|--------|\n")

    for cat, d in sorted(stats["categories"].items()):
        t = d["total"]
        p = d["passed"]
        f = d["failed"]
        s = d["skipped"]
        rate = round(p / t * 100, 1) if t else 0.0
        if f == 0:
            status = "✅ All Pass"
        elif p == 0:
            status = "🔴 All Fail"
        else:
            status = "🟡 Partial"
        w(f"| {cat} | {t} | {p} | {f} | {s} | {rate}% | {status} |\n")

    w("\n---\n\n")

    # ═══════════════════════════════════════════════════════════
    # FAILED TESTS (if any)
    # ═══════════════════════════════════════════════════════════
    if stats["failed_tests"]:
        w("## ❌ Failed Test Details\n\n")
        w("> These tests need investigation. Check the full error in the XLSX report.\n\n")
        w("| # | Category | Test | Error (truncated) |\n")
        w("|---|----------|------|-------------------|\n")
        for i, ft in enumerate(stats["failed_tests"], 1):
            # Shorten the nodeid to just the test function name
            test_name = ft["nodeid"].split("::")[-1] if "::" in ft["nodeid"] else ft["nodeid"]
            error = ft["error"].replace("|", "\\|").replace("\n", " ")[:180]
            w(f"| {i} | {ft['category']} | `{test_name}` | {error} |\n")
        w("\n---\n\n")
    else:
        w("## 🎉 No Failed Tests!\n\n")
        w("> All executed tests passed. Great job! 🚀\n\n")
        w("---\n\n")

    # ═══════════════════════════════════════════════════════════
    # FOOTER
    # ═══════════════════════════════════════════════════════════
    w("## 📥 Download Report\n\n")
    w("The full **Excel (.xlsx) report** is available in the ")
    w("**Artifacts** section at the bottom of this workflow run page.\n\n")
    w("It contains:\n")
    w("- 📋 **Test Cases** sheet — single-sheet workbook containing all executed test cases, category tags, statuses, durations, and traceback error logs.\n\n")
    w("---\n")
    w("*Generated automatically by CrowdSense Selenium E2E Suite*\n")

    if summary_path:
        out.close()
    print(f"[OK] GitHub Actions summary written → {summary_path or 'stdout'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate GitHub Actions Step Summary from pytest JSON report")
    parser.add_argument("--json",   required=True, help="Path to pytest-json-report output (.json)")
    parser.add_argument("--branch", default="unknown", help="Git branch name")
    parser.add_argument("--sha",    default="unknown", help="Short git SHA")
    parser.add_argument("--xlsx",   default="",        help="XLSX report filename for display")
    args = parser.parse_args()

    if not os.path.exists(args.json):
        print(f"[WARN] JSON report not found at: {args.json} — writing minimal summary")
        summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
        out = open(summary_path, "a", encoding="utf-8") if summary_path else sys.stdout
        out.write("# ⚠️ CrowdSense E2E — No JSON Report Found\n\n")
        out.write("The test runner did not produce a JSON report. Check the test execution step logs.\n")
        if summary_path:
            out.close()
        sys.exit(0)

    stats = parse_report(args.json)
    write_summary(args, stats)


if __name__ == "__main__":
    main()
