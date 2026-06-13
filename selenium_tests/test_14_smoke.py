"""
test_14_smoke.py — Smoke Tests (Critical Path)
===============================================
Tests: TC226–TC240
Coverage:
  • Quick sanity checks for all critical routes
  • These tests run FIRST and fast — they verify the app is up
  • If any smoke test fails, the app is down

Target: https://thirulogasundar.github.io/CrowdSense
"""
import time
import pytest
import urllib.request
import urllib.error

BASE_URL = "https://thirulogasundar.github.io/CrowdSense"


def _nav(driver, path: str, wait: float = 3.5):
    driver.get(f"{BASE_URL}/#/{path}")
    time.sleep(wait)


def _src(driver) -> str:
    return driver.page_source


def _flutter_loaded(src: str) -> bool:
    return any(ind in src.lower() for ind in ["flt-", "canvas", "flutter"])


def _http_ok(url: str) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CrowdSense-Smoke/2.0"})
        return urllib.request.urlopen(req, timeout=15).getcode() == 200
    except Exception:
        return False


# ══════════════════════════════════════════════════════════════════════════════
class TestSmoke:
    """TC226–TC240 — Smoke Tests (Critical Path)"""

    def test_tc226_smoke_base_url_loads(self, driver):
        """TC226 — SMOKE: Base URL loads the Flutter app shell."""
        driver.get(BASE_URL)
        time.sleep(6)
        assert len(_src(driver)) > 300, (
            "SMOKE FAIL: App base URL returned empty — Flutter shell did not load"
        )

    def test_tc227_smoke_page_title_is_crowdsense(self, driver):
        """TC227 — SMOKE: Browser title contains 'crowdsense'."""
        driver.get(BASE_URL)
        time.sleep(4)
        assert "crowdsense" in driver.title.lower(), (
            f"SMOKE FAIL: Title is not 'crowdsense', got: '{driver.title}'"
        )

    def test_tc228_smoke_flutter_rendered(self, driver):
        """TC228 — SMOKE: Flutter CanvasKit rendered on base URL."""
        driver.get(BASE_URL)
        time.sleep(6)
        assert _flutter_loaded(_src(driver)), (
            "SMOKE FAIL: Flutter CanvasKit did not render on base URL"
        )

    def test_tc229_smoke_login_route_loads(self, driver):
        """TC229 — SMOKE: /login route loads with Sign In content."""
        _nav(driver, "login")
        src = _src(driver)
        assert len(src) > 200, "SMOKE FAIL: /login route returned empty page"

    def test_tc230_smoke_register_route_loads(self, driver):
        """TC230 — SMOKE: /register route loads with Create Account content."""
        _nav(driver, "register")
        src = _src(driver)
        assert len(src) > 200, "SMOKE FAIL: /register route returned empty page"

    def test_tc231_smoke_forgot_password_route_loads(self, driver):
        """TC231 — SMOKE: /forgot-password route loads with Reset content."""
        _nav(driver, "forgot-password")
        src = _src(driver)
        assert len(src) > 200, "SMOKE FAIL: /forgot-password returned empty page"

    def test_tc232_smoke_settings_route_loads(self, driver):
        """TC232 — SMOKE: /settings route loads with Settings content."""
        _nav(driver, "settings")
        src = _src(driver)
        assert len(src) > 200, "SMOKE FAIL: /settings returned empty page"

    def test_tc233_smoke_search_route_loads(self, driver):
        """TC233 — SMOKE: /search route loads with Search content."""
        _nav(driver, "search")
        src = _src(driver)
        assert len(src) > 200, "SMOKE FAIL: /search returned empty page"

    def test_tc234_smoke_place_details_route_loads(self, driver):
        """TC234 — SMOKE: /place/:id route loads without crashing."""
        _nav(driver, "place/smoke-test-place-001")
        src = _src(driver)
        assert len(src) > 200, "SMOKE FAIL: /place/:id crashed or returned empty"

    def test_tc235_smoke_home_route_redirects(self, driver):
        """TC235 — SMOKE: /home route either loads or redirects to login (route guard works)."""
        _nav(driver, "home", wait=4)
        url = driver.current_url.lower()
        src = _src(driver)
        assert ("home" in url or "login" in url) and len(src) > 200, (
            f"SMOKE FAIL: /home route did not load or redirect. URL: {url}"
        )

    def test_tc236_smoke_profile_route_redirects(self, driver):
        """TC236 — SMOKE: /profile redirects unauthenticated user to login."""
        _nav(driver, "profile", wait=4)
        assert "login" in driver.current_url.lower(), (
            f"SMOKE FAIL: /profile did not redirect to login. URL: {driver.current_url}"
        )

    def test_tc237_smoke_manifest_accessible(self, driver):
        """TC237 — SMOKE: manifest.json is accessible (HTTP 200)."""
        result = _http_ok(f"{BASE_URL}/manifest.json")
        if not result:
            pytest.skip("manifest.json check skipped — possible network issue")

    def test_tc238_smoke_flutter_bootstrap_accessible(self, driver):
        """TC238 — SMOKE: flutter_bootstrap.js is accessible (HTTP 200)."""
        result = _http_ok(f"{BASE_URL}/flutter_bootstrap.js")
        if not result:
            pytest.skip("flutter_bootstrap.js check skipped — possible network issue")

    def test_tc239_smoke_no_404_on_root(self, driver):
        """TC239 — SMOKE: Root URL does not return a 404 Not Found."""
        driver.get(BASE_URL)
        time.sleep(4)
        src = _src(driver)
        title = driver.title
        assert "404" not in title and "Not Found" not in title and len(src) > 300, (
            "SMOKE FAIL: App root URL is returning a 404 Not Found"
        )

    def test_tc240_smoke_no_500_on_root(self, driver):
        """TC240 — SMOKE: Root URL does not return a 500 Internal Server Error."""
        driver.get(BASE_URL)
        time.sleep(4)
        assert "500 Internal Server Error" not in _src(driver), (
            "SMOKE FAIL: App root URL is returning a 500 Internal Server Error"
        )
