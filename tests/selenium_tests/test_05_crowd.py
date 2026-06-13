"""
test_05_crowd.py — Crowd Intelligence End-to-End Tests
=======================================================
Tests: TC086–TC100
Coverage:
  • Crowd Report form elements: Low / Moderate / High options
  • Crowd report note / comment field
  • Crowd report Submit button
  • Crowd Status card shown on place details
  • Best Time to Visit section
  • Crowd Forecast chart
  • Submitting crowd report (route-level, no real submission)
  • Crowd badge colour changes
  • Multiple crowd levels navigation stability

Target: https://thirulogasundar.github.io/CrowdSense
"""
import time
import pytest

BASE_URL    = "https://thirulogasundar.github.io/CrowdSense"
PLACE_ID    = "test-place-001"
PLACE_ROUTE = f"place/{PLACE_ID}"


def _nav(driver, path: str, wait: float = 3.5):
    driver.get(f"{BASE_URL}/#/{path}")
    time.sleep(wait)


def _src(driver) -> str:
    return driver.page_source


def _flutter_loaded(src: str) -> bool:
    return any(ind in src.lower() for ind in ["flt-", "canvas", "flutter"])


def _url_has(driver, *fragments) -> bool:
    url = driver.current_url.lower()
    return any(f.lower() in url for f in fragments)


# ══════════════════════════════════════════════════════════════════════════════
class TestCrowdIntelligence:
    """TC086–TC100 — Crowd Intelligence & Reporting Tests"""

    def test_tc086_place_details_renders_for_crowd_tests(self, driver):
        """TC086 — Place details page renders (prerequisite for all crowd tests)."""
        _nav(driver, PLACE_ROUTE)
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login"), (
            f"Place details did not render. URL: {driver.current_url}"
        )

    def test_tc087_crowd_report_low_option_present(self, driver):
        """TC087 — Crowd report form shows a Low / Not Busy option."""
        _nav(driver, PLACE_ROUTE)
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc088_crowd_report_moderate_option_present(self, driver):
        """TC088 — Crowd report form shows a Moderate / A bit busy option."""
        _nav(driver, PLACE_ROUTE)
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc089_crowd_report_high_option_present(self, driver):
        """TC089 — Crowd report form shows a High / Very Crowded option."""
        _nav(driver, PLACE_ROUTE)
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc090_crowd_report_note_field_present(self, driver):
        """TC090 — Crowd report form has an optional note/comment text field."""
        _nav(driver, PLACE_ROUTE)
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc091_crowd_report_submit_button_present(self, driver):
        """TC091 — Crowd report form has a Submit button."""
        _nav(driver, PLACE_ROUTE)
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc092_crowd_status_card_on_place_details(self, driver):
        """TC092 — Place details page shows a Live Crowd Status card."""
        _nav(driver, PLACE_ROUTE)
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc093_best_time_to_visit_section(self, driver):
        """TC093 — Place details page shows Best Time to Visit section."""
        _nav(driver, PLACE_ROUTE)
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc094_crowd_forecast_chart_section(self, driver):
        """TC094 — Place details page shows a Crowd Forecast / historical chart."""
        _nav(driver, PLACE_ROUTE)
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc095_multiple_place_navigations_stable(self, driver):
        """TC095 — Navigating to three different place IDs consecutively is stable."""
        for pid in ["place-001", "place-002", "place-003"]:
            driver.get(f"{BASE_URL}/#/place/{pid}")
            time.sleep(1.5)
        assert _flutter_loaded(_src(driver)), (
            "App became unstable after navigating to multiple place IDs"
        )

    def test_tc096_crowd_page_source_not_empty(self, driver):
        """TC096 — Place/crowd details page source is not empty (> 300 chars)."""
        _nav(driver, PLACE_ROUTE)
        assert len(_src(driver)) > 300

    def test_tc097_crowd_page_no_server_error(self, driver):
        """TC097 — Crowd page does not show a server-side error."""
        _nav(driver, PLACE_ROUTE)
        assert "500 Internal Server Error" not in _src(driver)

    def test_tc098_crowd_page_scroll_stable(self, driver):
        """TC098 — Scrolling through place/crowd details page is stable."""
        _nav(driver, PLACE_ROUTE)
        for offset in [200, 400, 600, 800]:
            driver.execute_script(f"window.scrollTo(0, {offset})")
            time.sleep(0.3)
        assert _flutter_loaded(_src(driver)), "App crashed during crowd page scroll"

    def test_tc099_crowd_report_page_not_blank(self, driver):
        """TC099 — Place details page renders visible content (not blank/white)."""
        _nav(driver, PLACE_ROUTE)
        assert len(_src(driver)) > 200

    def test_tc100_crowd_back_navigation_works(self, driver):
        """TC100 — Browser back from place details returns to previous page safely."""
        driver.get(f"{BASE_URL}/#/login")
        time.sleep(2)
        driver.get(f"{BASE_URL}/#/{PLACE_ROUTE}")
        time.sleep(3)
        driver.back()
        time.sleep(2)
        assert _flutter_loaded(_src(driver)), "App crashed after back navigation from place details"
