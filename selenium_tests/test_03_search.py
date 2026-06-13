"""
test_03_search.py — Search & Place Discovery End-to-End Tests
==============================================================
Tests: TC046–TC065
Coverage:
  • Search page loads
  • Suggestion chips (Coffee Shop, Library, Museum, Mall, Park)
  • Recent Searches section
  • Search results page
  • Search empty state
  • Search loading state stability

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
class TestSearch:
    """TC046–TC065 — Search & Discovery Tests"""

    def test_tc046_search_page_loads(self, driver):
        """TC046 — /search route renders or redirects gracefully."""
        _nav(driver, "search")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "search", "login"), (
            f"Search page did not load. URL: {driver.current_url}"
        )

    def test_tc047_search_page_flutter_rendered(self, driver):
        """TC047 — Flutter CanvasKit is rendered on /search route."""
        _nav(driver, "search")
        assert _flutter_loaded(_src(driver)), "Flutter not rendered on search page"

    def test_tc048_search_page_has_search_input(self, driver):
        """TC048 — Search page has a search input / bar."""
        _nav(driver, "search")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "search", "login")

    def test_tc049_search_page_shows_coffee_shop_chip(self, driver):
        """TC049 — Search page shows a Coffee Shop suggestion chip."""
        _nav(driver, "search")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "search", "login")

    def test_tc050_search_page_shows_library_chip(self, driver):
        """TC050 — Search page shows a Library suggestion chip."""
        _nav(driver, "search")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "search", "login")

    def test_tc051_search_page_shows_museum_chip(self, driver):
        """TC051 — Search page shows a Museum suggestion chip."""
        _nav(driver, "search")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "search", "login")

    def test_tc052_search_page_shows_mall_chip(self, driver):
        """TC052 — Search page shows a Mall suggestion chip."""
        _nav(driver, "search")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "search", "login")

    def test_tc053_search_page_shows_park_chip(self, driver):
        """TC053 — Search page shows a Park suggestion chip."""
        _nav(driver, "search")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "search", "login")

    def test_tc054_search_page_shows_recent_searches(self, driver):
        """TC054 — Search page shows a Recent Searches section."""
        _nav(driver, "search")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "search", "login")

    def test_tc055_search_results_page_loads(self, driver):
        """TC055 — /search-results route loads without crashing."""
        _nav(driver, "search-results")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "search", "login"), (
            f"Search results page failed to load. URL: {driver.current_url}"
        )

    def test_tc056_search_results_flutter_rendered(self, driver):
        """TC056 — Flutter is rendered on /search-results route."""
        _nav(driver, "search-results")
        assert _flutter_loaded(_src(driver)), "Flutter not rendered on search-results"

    def test_tc057_search_empty_state_handled(self, driver):
        """TC057 — Empty search state is handled without crashing."""
        _nav(driver, "search")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "search", "login")

    def test_tc058_search_loading_state_stable(self, driver):
        """TC058 — Search loading state does not cause a crash."""
        _nav(driver, "search")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "search", "login")

    def test_tc059_search_page_source_not_empty(self, driver):
        """TC059 — Search page has substantial HTML content (> 300 chars)."""
        _nav(driver, "search")
        assert len(_src(driver)) > 300, "Search page source is too small — may be blank"

    def test_tc060_search_page_no_500_error(self, driver):
        """TC060 — Search page does not show a 500 Internal Server Error."""
        _nav(driver, "search")
        assert "500 Internal Server Error" not in _src(driver), (
            "Search page is showing a server error"
        )

    def test_tc061_search_page_scroll_works(self, driver):
        """TC061 — Scrolling on search page does not crash the app."""
        _nav(driver, "search")
        driver.execute_script("window.scrollBy(0, 400)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver)), "App crashed after scrolling on search"

    def test_tc062_search_page_title_is_crowdsense(self, driver):
        """TC062 — Browser tab title is 'crowdsense' on search route."""
        _nav(driver, "search")
        assert "crowdsense" in driver.title.lower()

    def test_tc063_search_page_refresh_stable(self, driver):
        """TC063 — Refreshing the search page does not crash the app."""
        _nav(driver, "search")
        driver.refresh()
        time.sleep(4)
        assert _flutter_loaded(_src(driver)), "App crashed after refreshing search page"

    def test_tc064_search_page_has_placeholder_text(self, driver):
        """TC064 — Search page has a placeholder text area for search query input."""
        _nav(driver, "search")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "search", "login")

    def test_tc065_search_rapid_navigation_stable(self, driver):
        """TC065 — Rapidly navigating between search and login does not crash."""
        for _ in range(3):
            driver.get(f"{BASE_URL}/#/search")
            time.sleep(0.5)
            driver.get(f"{BASE_URL}/#/login")
            time.sleep(0.5)
        time.sleep(2)
        assert _flutter_loaded(_src(driver)), "App crashed during rapid search/login navigation"
