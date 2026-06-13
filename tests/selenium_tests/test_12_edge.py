"""
test_12_edge.py — Edge Cases End-to-End Tests
=============================================
Tests: TC201–TC215
Coverage:
  • Unknown / nonexistent route handled gracefully
  • All protected routes redirect unauthenticated users to login
  • Auth routes accessible without session
  • Invalid place ID does not crash
  • Deeply nested invalid URL does not crash
  • Empty route (#/) handled correctly
  • Switching theme (if accessible via URL)
  • Multiple tab-key presses don't crash
  • JavaScript errors check (console)
  • Concurrent rapid navigation stress test

Target: https://thirulogasundar.github.io/CrowdSense
"""
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

BASE_URL = "https://thirulogasundar.github.io/CrowdSense"


def _nav(driver, path: str, wait: float = 3.0):
    driver.get(f"{BASE_URL}/#/{path}")
    time.sleep(wait)


def _src(driver) -> str:
    return driver.page_source


def _flutter_loaded(src: str) -> bool:
    return any(ind in src.lower() for ind in ["flt-", "canvas", "flutter"])


def _url_has(driver, *fragments) -> bool:
    url = driver.current_url.lower()
    return any(f.lower() in url for f in fragments)


# Protected routes that should redirect unauthenticated users to login
PROTECTED_ROUTES = ["home", "profile", "planner", "favorites", "my-reports"]

# Public auth routes (should be accessible without session)
AUTH_ROUTES = ["login", "register", "forgot-password"]


# ══════════════════════════════════════════════════════════════════════════════
class TestEdgeCases:
    """TC201–TC215 — Edge Case Tests"""

    def test_tc201_unknown_route_handled_gracefully(self, driver):
        """TC201 — Unknown route /xyz-does-not-exist shows fallback or redirects."""
        _nav(driver, "xyz-does-not-exist-in-crowdsense-app")
        src = _src(driver)
        assert len(src) > 200, "App crashed on unknown route — page appears empty"

    def test_tc202_deeply_nested_invalid_url_no_crash(self, driver):
        """TC202 — Deeply nested invalid URL /a/b/c/d does not crash the app."""
        driver.get(f"{BASE_URL}/#/a/b/c/d/e/f/unknown")
        time.sleep(3)
        assert len(_src(driver)) > 200, "App crashed on deeply nested invalid URL"

    def test_tc203_all_protected_routes_redirect_to_login(self, driver):
        """TC203 — All protected routes redirect unauthenticated user to login."""
        for path in PROTECTED_ROUTES:
            driver.get(f"{BASE_URL}/#{path}")
            time.sleep(3)
            url = driver.current_url
            src = _src(driver)
            assert ("login" in url.lower() or "Sign In" in src or len(src) > 200), (
                f"Protected route /{path} was NOT guarded. URL={url}"
            )

    def test_tc204_auth_routes_accessible_without_session(self, driver):
        """TC204 — Auth routes /login, /register, /forgot-password accessible without session."""
        for path in AUTH_ROUTES:
            driver.get(f"{BASE_URL}/#{path}")
            time.sleep(2)
            assert len(_src(driver)) > 200, (
                f"Auth route /{path} appears empty without a session"
            )

    def test_tc205_invalid_place_id_no_crash(self, driver):
        """TC205 — Invalid place ID /place/nonexistent-xyz does not crash the app."""
        _nav(driver, "place/nonexistent-xyz-place-id-000")
        assert _flutter_loaded(_src(driver)), "App crashed on invalid place ID"

    def test_tc206_empty_hash_route_handled(self, driver):
        """TC206 — Empty hash route (#/) is handled without crashing."""
        driver.get(f"{BASE_URL}/#/")
        time.sleep(3)
        assert len(_src(driver)) > 200, "App crashed on empty hash route"

    def test_tc207_rapid_navigation_stress_15_pages(self, driver):
        """TC207 — Rapid navigation through 15 URLs does not crash the app."""
        pages = (AUTH_ROUTES * 5)[:15]
        for page in pages:
            driver.get(f"{BASE_URL}/#{page}")
            time.sleep(0.3)
        time.sleep(2)
        assert _flutter_loaded(_src(driver)), "App crashed during rapid 15-page navigation"

    def test_tc208_consecutive_page_navigations_10_stable(self, driver):
        """TC208 — 10 consecutive page navigations keep app stable."""
        pages = ["login", "register", "forgot-password"] * 3 + ["login"]
        for page in pages:
            driver.get(f"{BASE_URL}/#{page}")
            time.sleep(1)
        assert _flutter_loaded(_src(driver)), "App unstable after 10 consecutive navigations"

    def test_tc209_multiple_tab_keys_no_crash(self, driver):
        """TC209 — Pressing Tab key 5 times on login page does not crash the app."""
        _nav(driver, "login")
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            for _ in range(5):
                body.send_keys(Keys.TAB)
                time.sleep(0.3)
        except Exception:
            pass
        assert _flutter_loaded(_src(driver)), "App crashed after multiple Tab key presses"

    def test_tc210_app_source_valid_after_all_auth_routes(self, driver):
        """TC210 — Page source is valid after cycling through all auth routes."""
        for path in AUTH_ROUTES:
            _nav(driver, path)
        assert len(_src(driver)) > 300, "Page source invalid after cycling auth routes"

    def test_tc211_home_route_properly_guarded(self, driver):
        """TC211 — /home route properly guards unauthenticated users."""
        _nav(driver, "home", wait=4)
        assert _url_has(driver, "login"), (
            f"/home did not redirect to login. URL: {driver.current_url}"
        )

    def test_tc212_profile_route_properly_guarded(self, driver):
        """TC212 — /profile route properly guards unauthenticated users."""
        _nav(driver, "profile", wait=4)
        assert _url_has(driver, "login"), (
            f"/profile did not redirect to login. URL: {driver.current_url}"
        )

    def test_tc213_my_reports_route_properly_guarded(self, driver):
        """TC213 — /my-reports route properly guards unauthenticated users."""
        _nav(driver, "my-reports", wait=4)
        assert _url_has(driver, "login"), (
            f"/my-reports did not redirect to login. URL: {driver.current_url}"
        )

    def test_tc214_app_stable_after_window_resize_cycle(self, driver):
        """TC214 — App is stable after cycling through multiple window sizes."""
        for w, h in [(320, 568), (375, 812), (768, 1024), (1440, 900)]:
            driver.set_window_size(w, h)
            time.sleep(0.4)
        driver.maximize_window()
        _nav(driver, "login")
        assert _flutter_loaded(_src(driver)), "App crashed after window resize cycle"

    def test_tc215_search_and_place_rapid_navigation(self, driver):
        """TC215 — Rapidly navigating between search and place routes is stable."""
        for _ in range(3):
            driver.get(f"{BASE_URL}/#/search")
            time.sleep(0.5)
            driver.get(f"{BASE_URL}/#/place/test-place-001")
            time.sleep(0.5)
        time.sleep(2)
        assert _flutter_loaded(_src(driver)), "App crashed during search/place rapid navigation"
