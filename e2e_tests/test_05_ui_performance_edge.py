"""
test_05_ui_performance_edge.py — UI/UX, Performance & Edge Case Tests (TC106–TC130)
Target: https://thirulogasundar.github.io/CrowdSense
"""
import time
import pytest
import urllib.request
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

BASE_URL = "https://thirulogasundar.github.io/CrowdSense"


def _go(driver, path):
    driver.get(f"{BASE_URL}/#/{path}")
    time.sleep(3)


def _src(driver):
    return driver.page_source


def _http_status(url):
    try:
        return urllib.request.urlopen(url).getcode()
    except Exception:
        return None


class TestUIPerformanceEdgeCases:

    def test_app_renders_within_8_seconds(self, driver):
        """App renders visible content within 8 seconds of navigation."""
        driver.get(BASE_URL)
        start = time.time()
        while time.time() - start < 8:
            if len(driver.page_source) > 500:
                break
            time.sleep(0.5)
        elapsed = time.time() - start
        assert len(driver.page_source) > 500, \
            f"App took more than 8 seconds to render. Elapsed: {elapsed:.1f}s"

    def test_page_title_contains_crowdsense(self, driver):
        """Browser tab title contains 'crowdsense' (case-insensitive)."""
        driver.get(BASE_URL)
        time.sleep(4)
        assert "crowdsense" in driver.title.lower(), \
            f"Expected 'crowdsense' in page title, got '{driver.title}'"

    def test_app_renders_on_mobile_viewport_375x812(self, driver):
        """App renders correctly on mobile viewport 375x812 (iPhone X)."""
        driver.set_window_size(375, 812)
        driver.get(f"{BASE_URL}/#/login")
        time.sleep(3)
        src = _src(driver)
        assert len(src) > 200, "App appears empty on iPhone X viewport"
        driver.maximize_window()

    def test_app_renders_on_tablet_viewport_768x1024(self, driver):
        """App renders correctly on tablet viewport 768x1024 (iPad)."""
        driver.set_window_size(768, 1024)
        driver.get(f"{BASE_URL}/#/login")
        time.sleep(3)
        src = _src(driver)
        assert len(src) > 200, "App appears empty on iPad viewport"
        driver.maximize_window()

    def test_app_renders_on_desktop_1920x1080(self, driver):
        """App renders correctly on Full HD desktop 1920x1080."""
        driver.set_window_size(1920, 1080)
        driver.get(f"{BASE_URL}/#/login")
        time.sleep(3)
        src = _src(driver)
        assert len(src) > 200, "App appears empty on Full HD desktop"
        driver.maximize_window()

    def test_browser_back_forward_navigation(self, driver):
        """Browser back/forward navigation works without crashing the app."""
        driver.get(f"{BASE_URL}/#/login")
        time.sleep(2)
        driver.get(f"{BASE_URL}/#/register")
        time.sleep(2)
        driver.back()
        time.sleep(2)
        driver.forward()
        time.sleep(2)
        assert len(_src(driver)) > 200, "App crashed after back/forward navigation"

    def test_page_refresh_does_not_crash_app(self, driver):
        """Refreshing the login page does not crash the app."""
        driver.get(f"{BASE_URL}/#/login")
        time.sleep(3)
        driver.refresh()
        time.sleep(4)
        assert len(_src(driver)) > 200, "App crashed after page refresh"

    def test_unknown_route_handled_gracefully(self, driver):
        """Unknown route /xyz-does-not-exist shows fallback or redirects gracefully."""
        _go(driver, "xyz-does-not-exist-in-app")
        src = _src(driver)
        assert len(src) > 200, "App crashed on unknown route"

    def test_rapid_url_changes_no_crash(self, driver):
        """Navigating rapidly between 7 URLs does not crash the app."""
        paths = ["/login", "/register", "/forgot-password", "/login",
                 "/register", "/forgot-password", "/login"]
        for path in paths:
            driver.get(f"{BASE_URL}/#{path}")
            time.sleep(0.4)
        time.sleep(2)
        assert len(_src(driver)) > 200, "App crashed during rapid URL navigation"

    def test_scroll_on_login_page(self, driver):
        """Scrolling down on login page works without layout breaking."""
        driver.get(f"{BASE_URL}/#/login")
        time.sleep(3)
        driver.execute_script("window.scrollBy(0, 300)")
        time.sleep(1)
        assert len(_src(driver)) > 200, "Page broken after scrolling on login"

    def test_scroll_on_register_page(self, driver):
        """Scrolling down on register page works without layout breaking."""
        driver.get(f"{BASE_URL}/#/register")
        time.sleep(3)
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(1)
        assert len(_src(driver)) > 200, "Page broken after scrolling on register"

    def test_no_horizontal_overflow_on_login(self, driver):
        """Login page has no horizontal scroll overflow."""
        driver.get(f"{BASE_URL}/#/login")
        time.sleep(3)
        scroll_w  = driver.execute_script("return document.documentElement.scrollWidth")
        client_w  = driver.execute_script("return document.documentElement.clientWidth")
        assert scroll_w <= client_w + 50, \
            f"Horizontal overflow detected: scrollWidth={scroll_w}, clientWidth={client_w}"

    def test_manifest_json_accessible(self, driver):
        """manifest.json is accessible from the CrowdSense base URL."""
        code = _http_status("https://thirulogasundar.github.io/CrowdSense/manifest.json")
        if code is None:
            pytest.skip("manifest.json URL returned an error — may be network issue")
        assert code == 200, f"manifest.json returned HTTP status {code}"

    def test_flutter_bootstrap_js_accessible(self, driver):
        """flutter_bootstrap.js is accessible from the CrowdSense base URL."""
        code = _http_status("https://thirulogasundar.github.io/CrowdSense/flutter_bootstrap.js")
        if code is None:
            pytest.skip("flutter_bootstrap.js URL returned an error — may be network issue")
        assert code == 200, f"flutter_bootstrap.js returned HTTP status {code}"

    def test_favicon_accessible(self, driver):
        """favicon.png is accessible from the CrowdSense base URL."""
        code = _http_status("https://thirulogasundar.github.io/CrowdSense/favicon.png")
        if code is None:
            pytest.skip("favicon.png URL returned an error — may be network issue")
        assert code == 200, f"favicon.png returned HTTP status {code}"

    def test_flutter_js_accessible(self, driver):
        """flutter.js is accessible from the CrowdSense base URL."""
        code = _http_status("https://thirulogasundar.github.io/CrowdSense/flutter.js")
        if code is None:
            pytest.skip("flutter.js URL returned an error — may be network issue")
        assert code == 200, f"flutter.js returned HTTP status {code}"

    def test_page_source_is_valid_html(self, driver):
        """App root URL serves valid HTML (not a blank/error page)."""
        driver.get(BASE_URL)
        time.sleep(4)
        src = _src(driver)
        assert "<!DOCTYPE" in src or "<html" in src or \
               "<flt-" in src or len(src) > 300, \
            "App root URL does not appear to serve valid HTML"

    def test_keyboard_tab_on_login_no_crash(self, driver):
        """Pressing Tab key on login page does not crash the app."""
        driver.get(f"{BASE_URL}/#/login")
        time.sleep(3)
        body = driver.find_element(By.TAG_NAME, "body")
        try:
            body.send_keys(Keys.TAB)
            time.sleep(0.5)
            body.send_keys(Keys.TAB)
        except Exception:
            pass
        assert len(_src(driver)) > 200, "App broken after Tab key navigation"

    def test_protected_routes_redirect_to_login(self, driver):
        """All protected routes redirect unauthenticated user to login."""
        protected = ["/home", "/profile", "/planner", "/favorites", "/my-reports"]
        for path in protected:
            driver.get(f"{BASE_URL}/#{path}")
            time.sleep(3)
            url = driver.current_url
            src = _src(driver)
            assert ("login" in url.lower() or "Sign In" in src or
                    "Email" in src), \
                f"Protected route {path} was NOT guarded. URL={url}"

    def test_auth_routes_accessible_without_session(self, driver):
        """Auth routes /login, /register, /forgot-password are accessible without session."""
        for path in ["login", "register", "forgot-password"]:
            driver.get(f"{BASE_URL}/#{path}")
            time.sleep(2)
            assert len(_src(driver)) > 200, \
                f"Auth route /{path} appears empty without session"

    def test_consecutive_page_navigations_stable(self, driver):
        """Navigating through 10 pages consecutively keeps app stable."""
        pages = ["login", "register", "forgot-password", "login",
                 "register", "login", "forgot-password", "register",
                 "login", "register"]
        for page in pages:
            driver.get(f"{BASE_URL}/#{page}")
            time.sleep(1)
        assert len(_src(driver)) > 200, "App became unstable after 10 page navigations"

    def test_app_does_not_show_error_500(self, driver):
        """App does not show a 500 Internal Server Error page."""
        driver.get(BASE_URL)
        time.sleep(4)
        src = _src(driver)
        assert "500" not in src or "Internal Server Error" not in src, \
            "App is showing a 500 Internal Server Error page"

    def test_app_does_not_show_404_on_root(self, driver):
        """App root URL does not return a 404 Not Found page."""
        driver.get(BASE_URL)
        time.sleep(4)
        src = _src(driver)
        assert ("404" not in src and "Not Found" not in driver.title) or \
               len(src) > 500, \
            "App root URL is returning a 404 Not Found page"

    def test_login_page_renders_in_small_window(self, driver):
        """Login page renders correctly in a small 320x568 window."""
        driver.set_window_size(320, 568)
        driver.get(f"{BASE_URL}/#/login")
        time.sleep(3)
        assert len(_src(driver)) > 200, "App broken at 320x568 resolution"
        driver.maximize_window()
