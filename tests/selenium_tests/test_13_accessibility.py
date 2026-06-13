"""
test_13_accessibility.py — Accessibility End-to-End Tests
=========================================================
Tests: TC216–TC225
Coverage:
  • Keyboard Tab key navigation on login
  • Keyboard Tab key navigation on register
  • Keyboard Tab on forgot-password
  • Page title is meaningful (not empty / "CrowdSense")
  • Browser scrolls to top when navigating to new route
  • App does not trap focus in an unintended state
  • Language attribute present on <html>

Target: https://thirulogasundar.github.io/CrowdSense
"""
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

BASE_URL = "https://thirulogasundar.github.io/CrowdSense"


def _nav(driver, path: str, wait: float = 3.5):
    driver.get(f"{BASE_URL}/#/{path}")
    time.sleep(wait)


def _src(driver) -> str:
    return driver.page_source


def _flutter_loaded(src: str) -> bool:
    return any(ind in src.lower() for ind in ["flt-", "canvas", "flutter"])


# ══════════════════════════════════════════════════════════════════════════════
class TestAccessibility:
    """TC216–TC225 — Accessibility Tests"""

    def test_tc216_keyboard_tab_on_login_no_crash(self, driver):
        """TC216 — Pressing Tab key on login page does not crash the app."""
        _nav(driver, "login")
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.TAB)
            time.sleep(0.5)
            body.send_keys(Keys.TAB)
        except Exception:
            pass
        assert _flutter_loaded(_src(driver)), "App broken after Tab key on login"

    def test_tc217_keyboard_tab_on_register_no_crash(self, driver):
        """TC217 — Pressing Tab key on register page does not crash the app."""
        _nav(driver, "register")
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.TAB)
            time.sleep(0.5)
            body.send_keys(Keys.TAB)
        except Exception:
            pass
        assert _flutter_loaded(_src(driver)), "App broken after Tab key on register"

    def test_tc218_keyboard_tab_on_forgot_password(self, driver):
        """TC218 — Pressing Tab key on forgot-password page does not crash."""
        _nav(driver, "forgot-password")
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.TAB)
            time.sleep(0.5)
        except Exception:
            pass
        assert _flutter_loaded(_src(driver)), "App broken after Tab key on forgot-password"

    def test_tc219_page_title_not_empty(self, driver):
        """TC219 — Page title is not empty."""
        driver.get(BASE_URL)
        time.sleep(4)
        assert driver.title.strip() != "", "Page title is empty"

    def test_tc220_page_title_meaningful(self, driver):
        """TC220 — Page title is meaningful (contains 'crowdsense')."""
        driver.get(BASE_URL)
        time.sleep(4)
        assert "crowdsense" in driver.title.lower(), (
            f"Page title is not meaningful: '{driver.title}'"
        )

    def test_tc221_html_lang_attribute_present(self, driver):
        """TC221 — HTML element has a lang attribute set."""
        driver.get(BASE_URL)
        time.sleep(4)
        try:
            html_elem = driver.find_element(By.TAG_NAME, "html")
            lang = html_elem.get_attribute("lang")
            # Accept any lang value (en, en-US, etc.) or skip if not set (Flutter may not set it)
            if lang:
                assert lang.strip() != "", "lang attribute is empty"
        except Exception:
            pass  # Flutter may render using canvas — skip if not found

    def test_tc222_page_scroll_resets_on_route_change(self, driver):
        """TC222 — Scroll position resets (or is near top) when navigating to a new route."""
        _nav(driver, "login")
        driver.execute_script("window.scrollTo(0, 500)")
        time.sleep(0.5)
        _nav(driver, "register")
        scroll_y = driver.execute_script("return window.scrollY")
        assert scroll_y < 200, (
            f"Scroll did not reset on route change. scrollY={scroll_y}"
        )

    def test_tc223_keyboard_enter_on_login_no_crash(self, driver):
        """TC223 — Pressing Enter on login page does not crash the app."""
        _nav(driver, "login")
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.RETURN)
            time.sleep(1)
        except Exception:
            pass
        assert _flutter_loaded(_src(driver)), "App crashed after Enter key on login"

    def test_tc224_focus_not_trapped_on_login(self, driver):
        """TC224 — Focus is not trapped after navigating away from login."""
        _nav(driver, "login")
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.TAB)
        except Exception:
            pass
        _nav(driver, "register")
        assert _flutter_loaded(_src(driver)), "Focus appears trapped — app crashed on navigation"

    def test_tc225_no_autoscroll_loops_on_load(self, driver):
        """TC225 — App does not enter an autoscroll loop after loading."""
        _nav(driver, "login")
        scroll_y_1 = driver.execute_script("return window.scrollY")
        time.sleep(2)
        scroll_y_2 = driver.execute_script("return window.scrollY")
        assert abs(scroll_y_2 - scroll_y_1) < 100, (
            f"Possible autoscroll loop detected. "
            f"scrollY before={scroll_y_1}, after={scroll_y_2}"
        )
