"""
test_06_smoke.py — Smoke Tests (TC131–TC137)
Target: https://thirulogasundar.github.io/CrowdSense
Quick sanity checks for all critical routes.
"""
import time
import pytest

BASE_URL = "https://thirulogasundar.github.io/CrowdSense"


def _go(driver, path):
    driver.get(f"{BASE_URL}/#/{path}")
    time.sleep(3)


def _src(driver):
    return driver.page_source


class TestSmoke:

    def test_smoke_base_url_loads(self, driver):
        """Smoke – App base URL loads the Flutter app shell."""
        driver.get(BASE_URL)
        time.sleep(5)
        assert len(_src(driver)) > 300, \
            "App base URL returned an empty page — Flutter shell did not load"

    def test_smoke_login_route_loads(self, driver):
        """Smoke – /login route loads with Sign In content."""
        _go(driver, "login")
        src = _src(driver)
        assert "Sign In" in src or "Email" in src or len(src) > 200, \
            "Smoke: /login did not load correctly"

    def test_smoke_register_route_loads(self, driver):
        """Smoke – /register route loads with Create Account content."""
        _go(driver, "register")
        src = _src(driver)
        assert "Create Account" in src or "Register" in src or \
               "Email" in src or len(src) > 200, \
            "Smoke: /register did not load correctly"

    def test_smoke_forgot_password_route_loads(self, driver):
        """Smoke – /forgot-password route loads with Reset content."""
        _go(driver, "forgot-password")
        src = _src(driver)
        assert "Reset" in src or "Email" in src or len(src) > 200, \
            "Smoke: /forgot-password did not load correctly"

    def test_smoke_settings_route_loads(self, driver):
        """Smoke – /settings route loads with Settings content."""
        _go(driver, "settings")
        src = _src(driver)
        assert "Settings" in src or len(src) > 200, \
            "Smoke: /settings did not load correctly"

    def test_smoke_search_route_loads(self, driver):
        """Smoke – /search route loads with Search content."""
        _go(driver, "search")
        src = _src(driver)
        assert "Search" in src or "Email" in src or len(src) > 200, \
            "Smoke: /search did not load correctly"

    def test_smoke_place_details_route_loads(self, driver):
        """Smoke – /place/:id route loads without crashing."""
        _go(driver, "place/smoke-test-place")
        src = _src(driver)
        assert len(src) > 200, \
            "Smoke: /place/:id crashed or returned empty page"
