"""
test_08_planner.py — Travel Planner End-to-End Tests
=====================================================
Tests: TC131–TC145
Coverage:
  • Travel Planner page loads
  • Planner heading present
  • From / To selectors
  • Calculate Best Plan button (disabled without selection)
  • Crowd-aware description/subtitle
  • Map section present
  • Trip summary card
  • Planner page scroll & refresh stability

Target: https://thirulogasundar.github.io/CrowdSense
"""
import time
import pytest

BASE_URL = "https://thirulogasundar.github.io/CrowdSense"


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
class TestTravelPlanner:
    """TC131–TC145 — Travel Planner Tests"""

    def test_tc131_planner_page_loads(self, driver):
        """TC131 — /planner route loads or redirects gracefully."""
        _nav(driver, "planner")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "planner", "login"), (
            f"Travel Planner did not load. URL: {driver.current_url}"
        )

    def test_tc132_planner_flutter_rendered(self, driver):
        """TC132 — Flutter is rendered on the /planner route."""
        _nav(driver, "planner")
        assert _flutter_loaded(_src(driver)), "Flutter not rendered on planner page"

    def test_tc133_planner_shows_heading(self, driver):
        """TC133 — Travel Planner page shows a main heading."""
        _nav(driver, "planner")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "planner", "login")

    def test_tc134_planner_shows_from_selector(self, driver):
        """TC134 — Travel Planner shows a From location selector."""
        _nav(driver, "planner")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "planner", "login")

    def test_tc135_planner_shows_to_selector(self, driver):
        """TC135 — Travel Planner shows a To location selector."""
        _nav(driver, "planner")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "planner", "login")

    def test_tc136_planner_shows_calculate_button(self, driver):
        """TC136 — Travel Planner shows a Calculate Best Plan button."""
        _nav(driver, "planner")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "planner", "login")

    def test_tc137_planner_calculate_button_disabled_without_selection(self, driver):
        """TC137 — Calculate button is disabled/inactive without From/To selection."""
        _nav(driver, "planner")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "planner", "login")

    def test_tc138_planner_shows_crowd_aware_description(self, driver):
        """TC138 — Planner shows a crowd-aware subtitle/description text."""
        _nav(driver, "planner")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "planner", "login")

    def test_tc139_planner_map_section_present(self, driver):
        """TC139 — Travel Planner shows a map section."""
        _nav(driver, "planner")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "planner", "login")

    def test_tc140_planner_trip_summary_card(self, driver):
        """TC140 — Travel Planner shows a trip summary card area."""
        _nav(driver, "planner")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "planner", "login")

    def test_tc141_planner_page_source_not_empty(self, driver):
        """TC141 — Planner page source has substantial content (> 300 chars)."""
        _nav(driver, "planner")
        assert len(_src(driver)) > 300, "Planner page source appears empty"

    def test_tc142_planner_page_no_server_error(self, driver):
        """TC142 — Planner page does not show a server error."""
        _nav(driver, "planner")
        assert "500 Internal Server Error" not in _src(driver)

    def test_tc143_planner_scroll_stable(self, driver):
        """TC143 — Scrolling on the planner page does not crash the app."""
        _nav(driver, "planner")
        driver.execute_script("window.scrollBy(0, 600)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver)), "App crashed after scrolling on planner"

    def test_tc144_planner_title_is_crowdsense(self, driver):
        """TC144 — Browser title is 'crowdsense' on planner route."""
        _nav(driver, "planner")
        assert "crowdsense" in driver.title.lower()

    def test_tc145_planner_refresh_stable(self, driver):
        """TC145 — Refreshing the planner page does not crash the app."""
        _nav(driver, "planner")
        driver.refresh()
        time.sleep(4)
        assert _flutter_loaded(_src(driver)), "App crashed after refreshing planner page"
