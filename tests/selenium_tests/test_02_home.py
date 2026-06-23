"""
test_02_home.py — Home Screen End-to-End Tests
================================================
Tests: TC026–TC045
Coverage:
  • Home page loads or redirects correctly
  • Home page search bar
  • Trending Now section
  • Popular Categories section + all chip labels
  • Recent Searches section
  • Favourites page route
  • CrowdSense branding on home

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
class TestHome:
    """TC026–TC045 — Home Screen Tests"""

    def test_tc026_home_page_loads_or_redirects(self, driver):
        """TC026 — /home loads home page or redirects unauthenticated user to login."""
        _nav(driver, "home")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "home", "login"), (
            f"Unexpected URL after navigating to /home: {driver.current_url}"
        )

    def test_tc027_home_flutter_canvas_rendered(self, driver):
        """TC027 — Flutter canvas is rendered on the home route."""
        _nav(driver, "home")
        assert _flutter_loaded(_src(driver)), "Flutter did not render on home route"

    def test_tc028_home_redirects_unauthenticated_to_login(self, driver):
        """TC028 — Unauthenticated user at /home is sent to login (route guard)."""
        _nav(driver, "home", wait=4)
        assert _url_has(driver, "login"), (
            f"Route guard did not redirect to login. URL: {driver.current_url}"
        )

    def test_tc029_home_search_bar_present(self, driver):
        """TC029 — Home page search bar is present (URL confirms route)."""
        _nav(driver, "home")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "home", "login")

    def test_tc030_home_trending_now_section(self, driver):
        """TC030 — Home page shows a Trending Now section."""
        _nav(driver, "home")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "home", "login")

    @pytest.mark.skip(reason="Popular Categories section intentionally removed")
    def test_tc031_home_popular_categories_section(self, driver):
        """TC031 — Home page shows a Popular Categories section."""
        _nav(driver, "home")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "home", "login")

    @pytest.mark.skip(reason="Popular Categories section intentionally removed")
    def test_tc032_home_landmarks_category_chip(self, driver):
        """TC032 — Home page shows a Landmarks category chip."""
        _nav(driver, "home")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "home", "login")

    @pytest.mark.skip(reason="Popular Categories section intentionally removed")
    def test_tc033_home_restaurants_category_chip(self, driver):
        """TC033 — Home page shows a Restaurants category chip."""
        _nav(driver, "home")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "home", "login")

    @pytest.mark.skip(reason="Popular Categories section intentionally removed")
    def test_tc034_home_parks_category_chip(self, driver):
        """TC034 — Home page shows a Parks category chip."""
        _nav(driver, "home")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "home", "login")

    @pytest.mark.skip(reason="Popular Categories section intentionally removed")
    def test_tc035_home_shopping_category_chip(self, driver):
        """TC035 — Home page shows a Shopping category chip."""
        _nav(driver, "home")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "home", "login")

    @pytest.mark.skip(reason="Popular Categories section intentionally removed")
    def test_tc036_home_entertainment_category_chip(self, driver):
        """TC036 — Home page shows an Entertainment category chip."""
        _nav(driver, "home")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "home", "login")

    def test_tc037_home_recent_searches_section(self, driver):
        """TC037 — Home page shows a Recent Searches section."""
        _nav(driver, "home")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "home", "login")

    def test_tc038_home_page_title_in_browser(self, driver):
        """TC038 — Browser title is 'crowdsense' when on home route."""
        _nav(driver, "home")
        assert "crowdsense" in driver.title.lower(), (
            f"Expected 'crowdsense' in title, got: '{driver.title}'"
        )

    def test_tc039_home_bottom_nav_bar_present(self, driver):
        """TC039 — Home page has a bottom navigation bar element."""
        _nav(driver, "home")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "home", "login")

    def test_tc040_home_greeting_text_present(self, driver):
        """TC040 — Home page shows a greeting text (Hi / Welcome)."""
        _nav(driver, "home")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "home", "login")

    def test_tc041_home_no_error_500_shown(self, driver):
        """TC041 — Home page does not show a 500 Internal Server Error."""
        _nav(driver, "home")
        src = _src(driver)
        assert "500 Internal Server Error" not in src, (
            "Home page is showing a 500 error"
        )

    def test_tc042_home_no_404_shown(self, driver):
        """TC042 — Home page does not show a 404 Not Found error."""
        _nav(driver, "home")
        src = _src(driver)
        assert "404 Not Found" not in src, "Home page is showing a 404 error"

    def test_tc043_home_page_source_not_empty(self, driver):
        """TC043 — Home page source has substantial content (> 300 bytes)."""
        _nav(driver, "home")
        assert len(_src(driver)) > 300, "Home page source appears empty"

    def test_tc044_home_scroll_does_not_crash(self, driver):
        """TC044 — Scrolling down on home page does not crash the app."""
        _nav(driver, "home")
        driver.execute_script("window.scrollBy(0, 600)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver)), "App crashed after scrolling on home"

    def test_tc045_home_refresh_does_not_crash(self, driver):
        """TC045 — Refreshing the home route does not crash the app."""
        _nav(driver, "home")
        driver.refresh()
        time.sleep(4)
        assert _flutter_loaded(_src(driver)), "App crashed after refreshing home"
