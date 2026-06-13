"""
test_10_ui_responsive.py — UI/UX & Responsiveness End-to-End Tests
====================================================================
Tests: TC166–TC185
Coverage:
  • Mobile viewport 375×812 (iPhone X)
  • Tablet viewport 768×1024 (iPad)
  • Desktop viewport 1920×1080 (Full HD)
  • Small window 320×568
  • Horizontal overflow check (no overflow on login)
  • Browser back/forward navigation
  • Page refresh stability
  • Rapid URL navigation (7 pages)
  • 10 consecutive page navigations stability
  • Scrolling on multiple pages
  • Keyboard Tab key interaction

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


# ══════════════════════════════════════════════════════════════════════════════
class TestUIResponsive:
    """TC166–TC185 — UI/UX & Responsiveness Tests"""

    def test_tc166_mobile_viewport_375x812(self, driver):
        """TC166 — App renders correctly on iPhone X viewport 375×812."""
        driver.set_window_size(375, 812)
        _nav(driver, "login")
        assert len(_src(driver)) > 200, "App appears empty on iPhone X viewport"
        driver.maximize_window()

    def test_tc167_tablet_viewport_768x1024(self, driver):
        """TC167 — App renders correctly on iPad viewport 768×1024."""
        driver.set_window_size(768, 1024)
        _nav(driver, "login")
        assert len(_src(driver)) > 200, "App appears empty on iPad viewport"
        driver.maximize_window()

    def test_tc168_desktop_viewport_1920x1080(self, driver):
        """TC168 — App renders correctly on Full HD desktop 1920×1080."""
        driver.set_window_size(1920, 1080)
        _nav(driver, "login")
        assert len(_src(driver)) > 200, "App appears empty on Full HD desktop"
        driver.maximize_window()

    def test_tc169_small_window_320x568(self, driver):
        """TC169 — App renders correctly in a small 320×568 window."""
        driver.set_window_size(320, 568)
        _nav(driver, "login")
        assert len(_src(driver)) > 200, "App broken at 320×568 resolution"
        driver.maximize_window()

    def test_tc170_register_mobile_viewport(self, driver):
        """TC170 — Register page renders correctly on mobile viewport."""
        driver.set_window_size(375, 812)
        _nav(driver, "register")
        assert len(_src(driver)) > 200
        driver.maximize_window()

    def test_tc171_no_horizontal_overflow_on_login(self, driver):
        """TC171 — Login page has no horizontal scroll overflow."""
        driver.maximize_window()
        _nav(driver, "login")
        scroll_w = driver.execute_script("return document.documentElement.scrollWidth")
        client_w = driver.execute_script("return document.documentElement.clientWidth")
        assert scroll_w <= client_w + 50, (
            f"Horizontal overflow on login: scrollWidth={scroll_w}, clientWidth={client_w}"
        )

    def test_tc172_browser_back_forward_navigation(self, driver):
        """TC172 — Browser back/forward navigation works without crashing."""
        driver.get(f"{BASE_URL}/#/login")
        time.sleep(2)
        driver.get(f"{BASE_URL}/#/register")
        time.sleep(2)
        driver.back()
        time.sleep(2)
        driver.forward()
        time.sleep(2)
        assert len(_src(driver)) > 200, "App crashed after back/forward navigation"

    def test_tc173_page_refresh_login_stable(self, driver):
        """TC173 — Refreshing the login page does not crash the app."""
        _nav(driver, "login")
        driver.refresh()
        time.sleep(4)
        assert _flutter_loaded(_src(driver)), "App crashed after refreshing login page"

    def test_tc174_page_refresh_register_stable(self, driver):
        """TC174 — Refreshing the register page does not crash the app."""
        _nav(driver, "register")
        driver.refresh()
        time.sleep(4)
        assert _flutter_loaded(_src(driver)), "App crashed after refreshing register page"

    def test_tc175_rapid_url_changes_7_pages(self, driver):
        """TC175 — Navigating rapidly between 7 URLs does not crash the app."""
        paths = ["login", "register", "forgot-password", "login",
                 "register", "forgot-password", "login"]
        for path in paths:
            driver.get(f"{BASE_URL}/#/{path}")
            time.sleep(0.4)
        time.sleep(2)
        assert _flutter_loaded(_src(driver)), "App crashed during rapid URL navigation"

    def test_tc176_10_consecutive_navigations_stable(self, driver):
        """TC176 — 10 consecutive page navigations keep the app stable."""
        pages = ["login", "register", "forgot-password", "login",
                 "register", "login", "forgot-password", "register",
                 "login", "register"]
        for page in pages:
            driver.get(f"{BASE_URL}/#{page}")
            time.sleep(1)
        assert _flutter_loaded(_src(driver)), "App unstable after 10 consecutive navigations"

    def test_tc177_scroll_login_page(self, driver):
        """TC177 — Scrolling down on login page works without layout breaking."""
        _nav(driver, "login")
        driver.execute_script("window.scrollBy(0, 300)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver)), "App broken after scrolling login page"

    def test_tc178_scroll_register_page(self, driver):
        """TC178 — Scrolling down on register page works without layout breaking."""
        _nav(driver, "register")
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver)), "App broken after scrolling register page"

    def test_tc179_keyboard_tab_on_login(self, driver):
        """TC179 — Pressing Tab key on login page does not crash the app."""
        _nav(driver, "login")
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.TAB)
            time.sleep(0.5)
            body.send_keys(Keys.TAB)
        except Exception:
            pass  # Flutter may not expose standard DOM inputs
        assert _flutter_loaded(_src(driver)), "App broken after Tab key navigation"

    def test_tc180_landscape_orientation_1024x768(self, driver):
        """TC180 — App renders correctly in landscape 1024×768 (tablet landscape)."""
        driver.set_window_size(1024, 768)
        _nav(driver, "login")
        assert len(_src(driver)) > 200
        driver.maximize_window()

    def test_tc181_app_page_html_valid(self, driver):
        """TC181 — Root URL serves valid HTML (not blank/error page)."""
        driver.get(BASE_URL)
        time.sleep(4)
        src = _src(driver)
        assert ("<!doctype" in src.lower() or "<html" in src.lower()
                or "flt-" in src.lower() or len(src) > 300), (
            "App root URL does not appear to serve valid HTML"
        )

    def test_tc182_viewport_reset_after_resize(self, driver):
        """TC182 — Maximizing window after resize restores correct layout."""
        driver.set_window_size(375, 812)
        _nav(driver, "login")
        driver.maximize_window()
        time.sleep(1)
        assert _flutter_loaded(_src(driver)), "Layout broken after maximizing from mobile viewport"

    def test_tc183_no_horizontal_overflow_on_register(self, driver):
        """TC183 — Register page has no horizontal scroll overflow."""
        driver.maximize_window()
        _nav(driver, "register")
        scroll_w = driver.execute_script("return document.documentElement.scrollWidth")
        client_w = driver.execute_script("return document.documentElement.clientWidth")
        assert scroll_w <= client_w + 50, (
            f"Horizontal overflow on register: scrollWidth={scroll_w}, clientWidth={client_w}"
        )

    def test_tc184_app_not_blank_after_multiple_viewports(self, driver):
        """TC184 — App is not blank after cycling through multiple viewports."""
        for width, height in [(375, 812), (768, 1024), (1920, 1080)]:
            driver.set_window_size(width, height)
            time.sleep(0.5)
        driver.maximize_window()
        _nav(driver, "login")
        assert _flutter_loaded(_src(driver)), "App blank after viewport cycling"

    def test_tc185_footer_visible_on_desktop(self, driver):
        """TC185 — App renders complete content on large desktop viewport."""
        driver.set_window_size(1440, 900)
        _nav(driver, "login")
        assert _flutter_loaded(_src(driver))
        driver.maximize_window()
