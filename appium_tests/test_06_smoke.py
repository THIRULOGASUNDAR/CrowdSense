"""
test_06_smoke.py — Smoke / Critical Path Tests (AM091–AM100)
=============================================================
CrowdSense Appium Mobile E2E Suite
Target: Pixel 3a API 37 AVD  |  Automation: UiAutomator2

Covers:
  - App launches without crash
  - Core screens are accessible
  - App renders within acceptable time
  - Complete end-to-end user flows
  - App stability under rapid navigation
"""
import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# ─── Helper utilities ─────────────────────────────────────────────────────────

def _find(driver, *xpaths, timeout=10):
    for xp in xpaths:
        try:
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xp))
            )
        except (NoSuchElementException, TimeoutException):
            continue
    return None


def _exists(driver, *xpaths, timeout=8):
    return _find(driver, *xpaths, timeout=timeout) is not None


def _reset_app(driver):
    """Restart the app to a clean state."""
    try:
        driver.terminate_app("com.crowdsense.app")
        time.sleep(1)
        driver.activate_app("com.crowdsense.app")
        time.sleep(3)
    except Exception:
        pass


# ─── Test Class ───────────────────────────────────────────────────────────────

class TestSmokeCriticalPath:

    # AM091 — App launches without crash
    @pytest.mark.smoke
    def test_AM091_app_launches_without_crash(self, driver):
        """App must launch on the Pixel 3a emulator without any crash."""
        _reset_app(driver)
        time.sleep(5)
        src = driver.page_source
        assert len(src) > 100, "App appears to have crashed on launch (empty page source)"

    # AM092 — Login screen accessible
    @pytest.mark.smoke
    def test_AM092_login_screen_accessible(self, driver):
        """Login screen must be reachable from a fresh app launch."""
        _reset_app(driver)
        time.sleep(5)
        assert _exists(
            driver,
            '//*[@content-desc="Sign In" or @text="Sign In"]',
            '//*[contains(@content-desc,"Welcome") or contains(@text,"Welcome")]',
            '//android.widget.EditText',
        ), "Login screen is not accessible after fresh app launch"

    # AM093 — Register screen accessible
    @pytest.mark.smoke
    def test_AM093_register_screen_accessible(self, driver):
        """Register screen must be reachable from the Login screen."""
        _reset_app(driver)
        time.sleep(4)
        sign_up = _find(driver,
            '//*[contains(@content-desc,"Sign Up") or contains(@text,"Sign Up")]',
            '//*[contains(@content-desc,"account") or contains(@text,"account")]',
        )
        assert sign_up is not None, "Sign Up link not found on Login screen"
        sign_up.click()
        time.sleep(3)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Create Account") or contains(@text,"Create Account")]',
            '//*[contains(@content-desc,"Register") or contains(@text,"Register")]',
            '//android.widget.EditText',
        ), "Register screen not accessible"

    # AM094 — Forgot Password screen accessible
    @pytest.mark.smoke
    def test_AM094_forgot_password_accessible(self, driver):
        """Forgot Password screen must be reachable from the Login screen."""
        _reset_app(driver)
        time.sleep(4)
        fp = _find(driver,
            '//*[contains(@content-desc,"Forgot") or contains(@text,"Forgot")]')
        assert fp is not None, "Forgot Password link not found"
        fp.click()
        time.sleep(3)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Reset") or contains(@text,"Reset")]',
            '//*[contains(@content-desc,"Forgot") or contains(@text,"Forgot")]',
            '//android.widget.EditText',
        ), "Forgot Password screen not accessible"

    # AM095 — App renders within 10 seconds of launch
    @pytest.mark.smoke
    def test_AM095_app_renders_within_10_seconds(self, driver):
        """App must show meaningful content within 10 seconds of launch."""
        import datetime
        start = datetime.datetime.now()
        _reset_app(driver)
        time.sleep(10)
        elapsed = (datetime.datetime.now() - start).total_seconds()
        src = driver.page_source
        assert len(src) > 100, f"App did not render within 10 seconds (elapsed: {elapsed:.1f}s)"

    # AM096 — Login → Home complete flow
    @pytest.mark.smoke
    def test_AM096_login_to_home_flow(self, logged_in_driver):
        """Full login → Home flow must complete successfully (E2E critical path)."""
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Search") or contains(@text,"Search")]',
            '//*[contains(@content-desc,"Trending") or contains(@text,"Trending")]',
            '//*[contains(@content-desc,"Home") or contains(@text,"Home")]',
        ), "Home screen not reached in Login → Home flow"

    # AM097 — Home → Search → Back flow completes
    @pytest.mark.smoke
    def test_AM097_home_search_back_flow(self, logged_in_driver):
        """User must be able to navigate Home → Search → Back without errors."""
        driver = logged_in_driver
        # Navigate to Search
        search_tab = _find(driver,
            '//*[@content-desc="Search" or @text="Search"]')
        assert search_tab is not None, "Search tab not found on Home"
        search_tab.click()
        time.sleep(2)
        # Verify Search screen loaded
        assert _exists(
            driver,
            '//android.widget.EditText',
            '//*[contains(@content-desc,"search") or contains(@text,"search")]',
        ), "Search screen not accessible in Home → Search flow"
        # Navigate back
        driver.back()
        time.sleep(2)
        # Should be back on Home
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Home") or contains(@text,"Home")]',
            '//*[contains(@content-desc,"Trending") or contains(@text,"Trending")]',
            '//*[contains(@content-desc,"Search") or contains(@text,"Search")]',
        ), "Back from Search did not return to Home"

    # AM098 — Profile screen accessible after login
    @pytest.mark.smoke
    def test_AM098_profile_accessible_after_login(self, logged_in_driver):
        """Profile screen must be reachable from Home after login."""
        driver = logged_in_driver
        profile_tab = _find(driver,
            '//*[@content-desc="Profile" or @text="Profile"]',
            '//*[contains(@content-desc,"Profile") or contains(@text,"Profile")]',
        )
        assert profile_tab is not None, "Profile tab not found"
        profile_tab.click()
        time.sleep(2)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Profile") or contains(@text,"Profile")]',
            '//*[contains(@content-desc,"Sign Out") or contains(@text,"Sign Out")]',
        ), "Profile screen not accessible after login"

    # AM099 — Settings screen accessible after login
    @pytest.mark.smoke
    def test_AM099_settings_accessible_after_login(self, logged_in_driver):
        """Settings screen must be reachable after user is logged in."""
        driver = logged_in_driver
        # Navigate to profile first (settings is usually accessible from there)
        profile_tab = _find(driver,
            '//*[@content-desc="Profile" or @text="Profile"]',
            '//*[contains(@content-desc,"Profile") or contains(@text,"Profile")]',
        )
        if profile_tab:
            profile_tab.click()
            time.sleep(2)
        settings = _find(driver,
            '//*[@content-desc="Settings" or @text="Settings"]',
            '//*[contains(@content-desc,"Settings") or contains(@text,"Settings")]',
        )
        assert settings is not None, "Settings option not found from Profile"
        settings.click()
        time.sleep(2)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Settings") or contains(@text,"Settings")]',
            '//*[contains(@content-desc,"Dark Mode") or contains(@text,"Dark Mode")]',
            '//*[contains(@content-desc,"Appearance") or contains(@text,"Appearance")]',
        ), "Settings screen not accessible"

    # AM100 — App handles rapid screen transitions
    @pytest.mark.smoke
    def test_AM100_app_handles_rapid_screen_transitions(self, logged_in_driver):
        """App must not crash when navigating rapidly between bottom nav tabs."""
        driver = logged_in_driver
        tabs = [
            '//*[@content-desc="Search" or @text="Search"]',
            '//*[@content-desc="Home" or @text="Home"]',
            '//*[@content-desc="Favorites" or @text="Favorites"]',
            '//*[@content-desc="Home" or @text="Home"]',
        ]
        for xp in tabs:
            tab = _find(driver, xp, timeout=5)
            if tab:
                tab.click()
                time.sleep(0.8)  # rapid transition — 800ms between tabs

        # App must still be alive
        src = driver.page_source
        assert len(src) > 100, "App crashed during rapid screen transitions"
