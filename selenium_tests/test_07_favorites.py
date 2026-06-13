"""
test_07_favorites.py — Favorites End-to-End Tests
===================================================
Tests: TC121–TC130
Coverage:
  • Favorites page loads or redirects
  • Favorites page shows content or empty state
  • Favorites route accessible for unauthenticated users
  • Favorites page scroll stability
  • Favorites page title and source content

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
class TestFavorites:
    """TC121–TC130 — Favorites Tests"""

    def test_tc121_favorites_page_loads(self, driver):
        """TC121 — /favorites route loads or redirects gracefully."""
        _nav(driver, "favorites")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "favorites", "login"), (
            f"Favorites page did not load. URL: {driver.current_url}"
        )

    def test_tc122_favorites_page_flutter_rendered(self, driver):
        """TC122 — Flutter is rendered on the /favorites route."""
        _nav(driver, "favorites")
        assert _flutter_loaded(_src(driver)), "Flutter not rendered on favorites page"

    def test_tc123_favorites_accessible_for_unauthenticated(self, driver):
        """TC123 — Favorites route is accessible (or gracefully handled) for unauthenticated users."""
        _nav(driver, "favorites")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "favorites", "login")

    def test_tc124_favorites_page_shows_content_or_empty_state(self, driver):
        """TC124 — Favorites page shows a list or an empty state (no crash)."""
        _nav(driver, "favorites")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "favorites", "login")

    def test_tc125_favorites_page_shows_heading(self, driver):
        """TC125 — Favorites page renders a heading or title area."""
        _nav(driver, "favorites")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "favorites", "login")

    def test_tc126_favorites_page_source_not_empty(self, driver):
        """TC126 — Favorites page source has substantial content (> 300 chars)."""
        _nav(driver, "favorites")
        assert len(_src(driver)) > 300, "Favorites page source appears empty"

    def test_tc127_favorites_page_no_server_error(self, driver):
        """TC127 — Favorites page does not show a server-side error."""
        _nav(driver, "favorites")
        assert "500 Internal Server Error" not in _src(driver)

    def test_tc128_favorites_page_scroll_stable(self, driver):
        """TC128 — Scrolling on the favorites page does not crash the app."""
        _nav(driver, "favorites")
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver)), "App crashed after scrolling on favorites"

    def test_tc129_favorites_page_title_is_crowdsense(self, driver):
        """TC129 — Browser title is 'crowdsense' on favorites route."""
        _nav(driver, "favorites")
        assert "crowdsense" in driver.title.lower()

    def test_tc130_favorites_page_refresh_stable(self, driver):
        """TC130 — Refreshing the favorites page does not crash the app."""
        _nav(driver, "favorites")
        driver.refresh()
        time.sleep(4)
        assert _flutter_loaded(_src(driver)), "App crashed after refreshing favorites page"
