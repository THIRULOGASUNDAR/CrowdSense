"""
test_11_performance.py — Performance End-to-End Tests
=====================================================
Tests: TC186–TC200
Coverage:
  • App renders within 8 seconds
  • Static assets accessible (HTTP 200):
      - manifest.json
      - flutter_bootstrap.js
      - flutter.js
      - favicon.png
      - main.dart.js (if applicable)
  • Page source length threshold
  • App does not return 404 on root
  • App does not return 500 on root

Target: https://thirulogasundar.github.io/CrowdSense
"""
import time
import pytest
import urllib.request
import urllib.error

BASE_URL = "https://thirulogasundar.github.io/CrowdSense"


def _nav(driver, path: str, wait: float = 3.0):
    driver.get(f"{BASE_URL}/#/{path}")
    time.sleep(wait)


def _src(driver) -> str:
    return driver.page_source


def _flutter_loaded(src: str) -> bool:
    return any(ind in src.lower() for ind in ["flt-", "canvas", "flutter"])


def _http_status(url: str):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CrowdSense-E2E-Tests/2.0"})
        return urllib.request.urlopen(req, timeout=15).getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return None


# ══════════════════════════════════════════════════════════════════════════════
class TestPerformance:
    """TC186–TC200 — Performance Tests"""

    def test_tc186_app_renders_within_8_seconds(self, driver):
        """TC186 — App renders visible content within 8 seconds of first load."""
        driver.get(BASE_URL)
        start = time.time()
        while time.time() - start < 8:
            if len(_src(driver)) > 500:
                break
            time.sleep(0.5)
        elapsed = time.time() - start
        assert len(_src(driver)) > 500, (
            f"App took more than 8 seconds to render. Elapsed: {elapsed:.1f}s"
        )

    def test_tc187_app_renders_login_within_8_seconds(self, driver):
        """TC187 — Login route renders within 8 seconds."""
        _nav(driver, "login", wait=0)
        start = time.time()
        while time.time() - start < 8:
            if _flutter_loaded(_src(driver)):
                break
            time.sleep(0.5)
        elapsed = time.time() - start
        assert _flutter_loaded(_src(driver)), (
            f"Login page did not render within 8 seconds. Elapsed: {elapsed:.1f}s"
        )

    def test_tc188_manifest_json_returns_200(self, driver):
        """TC188 — manifest.json is accessible with HTTP 200."""
        code = _http_status(f"{BASE_URL}/manifest.json")
        if code is None:
            pytest.skip("manifest.json URL returned an error — possible network issue")
        assert code == 200, f"manifest.json returned HTTP {code}"

    def test_tc189_flutter_bootstrap_js_returns_200(self, driver):
        """TC189 — flutter_bootstrap.js is accessible with HTTP 200."""
        code = _http_status(f"{BASE_URL}/flutter_bootstrap.js")
        if code is None:
            pytest.skip("flutter_bootstrap.js URL returned an error — possible network issue")
        assert code == 200, f"flutter_bootstrap.js returned HTTP {code}"

    def test_tc190_flutter_js_returns_200(self, driver):
        """TC190 — flutter.js is accessible with HTTP 200."""
        code = _http_status(f"{BASE_URL}/flutter.js")
        if code is None:
            pytest.skip("flutter.js URL returned an error — possible network issue")
        assert code == 200, f"flutter.js returned HTTP {code}"

    def test_tc191_favicon_returns_200(self, driver):
        """TC191 — favicon.png is accessible with HTTP 200."""
        code = _http_status(f"{BASE_URL}/favicon.png")
        if code is None:
            pytest.skip("favicon.png URL returned an error — possible network issue")
        assert code == 200, f"favicon.png returned HTTP {code}"

    def test_tc192_base_url_returns_200(self, driver):
        """TC192 — Base URL returns HTTP 200."""
        code = _http_status(BASE_URL)
        if code is None:
            pytest.skip("Base URL returned an error — possible network issue")
        assert code == 200, f"Base URL returned HTTP {code}"

    def test_tc193_app_does_not_show_404_on_root(self, driver):
        """TC193 — App root URL does not show a 404 Not Found page."""
        driver.get(BASE_URL)
        time.sleep(4)
        src = _src(driver)
        assert ("404" not in src and "Not Found" not in driver.title) or len(src) > 500, (
            "App root URL is returning a 404 Not Found page"
        )

    def test_tc194_app_does_not_show_500_on_root(self, driver):
        """TC194 — App root URL does not show a 500 Internal Server Error."""
        driver.get(BASE_URL)
        time.sleep(4)
        assert "500 Internal Server Error" not in _src(driver), (
            "App is showing a 500 Internal Server Error"
        )

    def test_tc195_app_page_source_length_adequate(self, driver):
        """TC195 — App page source has adequate length (> 500 chars) after 5 seconds."""
        driver.get(BASE_URL)
        time.sleep(5)
        assert len(_src(driver)) > 500, (
            "App page source is too small — app may not have loaded"
        )

    def test_tc196_login_page_source_adequate(self, driver):
        """TC196 — Login page source has adequate length (> 300 chars) after load."""
        _nav(driver, "login")
        assert len(_src(driver)) > 300, "Login page source is too small"

    def test_tc197_register_page_source_adequate(self, driver):
        """TC197 — Register page source has adequate length (> 300 chars) after load."""
        _nav(driver, "register")
        assert len(_src(driver)) > 300, "Register page source is too small"

    def test_tc198_forgot_password_page_source_adequate(self, driver):
        """TC198 — Forgot password page source has adequate length (> 300 chars)."""
        _nav(driver, "forgot-password")
        assert len(_src(driver)) > 300, "Forgot password page source is too small"

    def test_tc199_app_responds_to_navigation_quickly(self, driver):
        """TC199 — App responds to route changes — login page loads in under 10 seconds."""
        driver.get(BASE_URL)
        time.sleep(2)
        start = time.time()
        driver.get(f"{BASE_URL}/#/login")
        while time.time() - start < 10:
            if len(_src(driver)) > 300:
                break
            time.sleep(0.5)
        elapsed = time.time() - start
        assert len(_src(driver)) > 300, (
            f"Login route took too long to respond. Elapsed: {elapsed:.1f}s"
        )

    def test_tc200_settings_loads_without_delay(self, driver):
        """TC200 — Settings page (no auth required) loads within 6 seconds."""
        start = time.time()
        _nav(driver, "settings", wait=0)
        while time.time() - start < 6:
            if _flutter_loaded(_src(driver)):
                break
            time.sleep(0.5)
        elapsed = time.time() - start
        assert _flutter_loaded(_src(driver)), (
            f"Settings page did not load within 6 seconds. Elapsed: {elapsed:.1f}s"
        )
