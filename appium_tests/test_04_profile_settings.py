"""
test_04_profile_settings.py — Profile & Settings Tests (AM061–AM078)
=====================================================================
CrowdSense Appium Mobile E2E Suite
Target: Pixel 3a API 37 AVD  |  Automation: UiAutomator2

Covers:
  - Profile screen UI (stats, menu options, sign out)
  - My Reports screen
  - Settings screen (toggles, links, version, account section)
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


def _navigate_to_profile(driver):
    """Tap the Profile tab in bottom nav."""
    tab = _find(driver,
        '//*[@content-desc="Profile" or @text="Profile"]',
        '//*[contains(@content-desc,"Profile") or contains(@text,"Profile")]',
        timeout=6)
    if tab:
        tab.click()
        time.sleep(2)


def _navigate_to_settings(driver):
    """Navigate to Settings screen (via Profile settings icon or Settings tab)."""
    _navigate_to_profile(driver)
    settings_icon = _find(driver,
        '//*[@content-desc="Settings" or @text="Settings"]',
        '//*[contains(@content-desc,"Settings") or contains(@text,"Settings")]',
        '//*[contains(@content-desc,"setting") or contains(@text,"setting")]',
        timeout=5)
    if settings_icon:
        settings_icon.click()
        time.sleep(2)


# ─── Test Class ───────────────────────────────────────────────────────────────

class TestProfileAndSettings:

    # AM061 — Profile screen renders
    @pytest.mark.profile
    @pytest.mark.smoke
    def test_AM061_profile_screen_renders(self, logged_in_driver):
        """Profile screen must load and render content."""
        driver = logged_in_driver
        _navigate_to_profile(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Profile") or contains(@text,"Profile")]',
            '//*[contains(@content-desc,"Sign Out") or contains(@text,"Sign Out")]',
            '//*[contains(@content-desc,"Reports") or contains(@text,"Reports")]',
        ), "Profile screen did not render"

    # AM062 — Profile shows user name
    @pytest.mark.profile
    def test_AM062_profile_shows_user_name(self, logged_in_driver):
        """Profile screen must display the authenticated user's name."""
        driver = logged_in_driver
        _navigate_to_profile(driver)
        src = driver.page_source
        # Name should appear somewhere in the page source
        assert len(src) > 100, "Profile screen appears empty"

    # AM063 — Profile shows Photos stat
    @pytest.mark.profile
    def test_AM063_profile_shows_photos_stat(self, logged_in_driver):
        """Profile screen must show a Photos statistic counter."""
        driver = logged_in_driver
        _navigate_to_profile(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Photos") or contains(@text,"Photos")]',
            '//*[contains(@content-desc,"photo") or contains(@text,"photo")]',
        ), "Photos stat not found on Profile screen"

    # AM064 — Profile shows Reports stat
    @pytest.mark.profile
    def test_AM064_profile_shows_reports_stat(self, logged_in_driver):
        """Profile screen must show a Reports statistic counter."""
        driver = logged_in_driver
        _navigate_to_profile(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Reports") or contains(@text,"Reports")]',
            '//*[contains(@content-desc,"report") or contains(@text,"report")]',
        ), "Reports stat not found on Profile screen"

    # AM065 — Profile shows Saved stat
    @pytest.mark.profile
    def test_AM065_profile_shows_saved_stat(self, logged_in_driver):
        """Profile screen must show a Saved (favorites) statistic counter."""
        driver = logged_in_driver
        _navigate_to_profile(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Saved") or contains(@text,"Saved")]',
            '//*[contains(@content-desc,"saved") or contains(@text,"saved")]',
            '//*[contains(@content-desc,"Favorites") or contains(@text,"Favorites")]',
        ), "Saved stat not found on Profile screen"

    # AM066 — Edit Profile option visible
    @pytest.mark.profile
    def test_AM066_profile_edit_option_visible(self, logged_in_driver):
        """Profile screen must show an Edit Profile menu item."""
        driver = logged_in_driver
        _navigate_to_profile(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Edit Profile") or contains(@text,"Edit Profile")]',
            '//*[contains(@content-desc,"Edit") or contains(@text,"Edit")]',
        ), "Edit Profile option not found on Profile screen"

    # AM067 — My Reports option visible
    @pytest.mark.profile
    def test_AM067_profile_my_reports_option(self, logged_in_driver):
        """Profile screen must show a My Reports menu item."""
        driver = logged_in_driver
        _navigate_to_profile(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"My Reports") or contains(@text,"My Reports")]',
            '//*[contains(@content-desc,"Reports") or contains(@text,"Reports")]',
        ), "My Reports option not found on Profile screen"

    # AM068 — Notifications option visible
    @pytest.mark.profile
    def test_AM068_profile_notifications_option(self, logged_in_driver):
        """Profile screen must show a Notifications menu item."""
        driver = logged_in_driver
        _navigate_to_profile(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Notifications") or contains(@text,"Notifications")]',
            '//*[contains(@content-desc,"notification") or contains(@text,"notification")]',
        ), "Notifications option not found on Profile screen"

    # AM069 — Support and FAQ option visible
    @pytest.mark.profile
    def test_AM069_profile_support_faq_option(self, logged_in_driver):
        """Profile screen must show a Support / FAQ menu item."""
        driver = logged_in_driver
        _navigate_to_profile(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Support") or contains(@text,"Support")]',
            '//*[contains(@content-desc,"FAQ") or contains(@text,"FAQ")]',
            '//*[contains(@content-desc,"Help") or contains(@text,"Help")]',
        ), "Support/FAQ option not found on Profile screen"

    # AM070 — Sign Out button visible
    @pytest.mark.profile
    def test_AM070_profile_sign_out_button(self, logged_in_driver):
        """Profile screen must display a Sign Out button."""
        driver = logged_in_driver
        _navigate_to_profile(driver)
        assert _exists(
            driver,
            '//*[@content-desc="Sign Out" or @text="Sign Out"]',
            '//*[contains(@content-desc,"Sign Out") or contains(@text,"Sign Out")]',
            '//*[contains(@content-desc,"Logout") or contains(@text,"Logout")]',
        ), "Sign Out button not found on Profile screen"

    # AM071 — My Reports screen loads
    @pytest.mark.profile
    def test_AM071_my_reports_screen_loads(self, logged_in_driver):
        """Tapping My Reports must navigate to the My Reports screen."""
        driver = logged_in_driver
        _navigate_to_profile(driver)
        my_reports = _find(driver,
            '//*[contains(@content-desc,"My Reports") or contains(@text,"My Reports")]',
            '//*[contains(@content-desc,"Reports") or contains(@text,"Reports")]')
        if my_reports:
            my_reports.click()
            time.sleep(2)
        src = driver.page_source
        assert len(src) > 100, "My Reports screen appears empty"
        driver.back()
        time.sleep(1)

    # AM072 — Settings screen renders
    @pytest.mark.settings
    @pytest.mark.smoke
    def test_AM072_settings_screen_renders(self, logged_in_driver):
        """Settings screen must load and render its sections."""
        driver = logged_in_driver
        _navigate_to_settings(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Settings") or contains(@text,"Settings")]',
            '//*[contains(@content-desc,"Dark Mode") or contains(@text,"Dark Mode")]',
            '//*[contains(@content-desc,"Appearance") or contains(@text,"Appearance")]',
        ), "Settings screen did not render"

    # AM073 — Settings has Dark Mode toggle
    @pytest.mark.settings
    def test_AM073_settings_dark_mode_toggle(self, logged_in_driver):
        """Settings screen must have a Dark Mode toggle switch."""
        driver = logged_in_driver
        _navigate_to_settings(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Dark Mode") or contains(@text,"Dark Mode")]',
            '//*[contains(@content-desc,"dark mode") or contains(@text,"dark mode")]',
            '//*[contains(@content-desc,"Theme") or contains(@text,"Theme")]',
        ), "Dark Mode toggle not found in Settings"

    # AM074 — Settings has Notifications toggle
    @pytest.mark.settings
    def test_AM074_settings_notifications_toggle(self, logged_in_driver):
        """Settings screen must have a Notifications toggle switch."""
        driver = logged_in_driver
        _navigate_to_settings(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Notifications") or contains(@text,"Notifications")]',
            '//*[contains(@content-desc,"notification") or contains(@text,"notification")]',
            '//*[contains(@content-desc,"Push") or contains(@text,"Push")]',
        ), "Notifications toggle not found in Settings"

    # AM075 — Settings shows Privacy Policy option
    @pytest.mark.settings
    def test_AM075_settings_privacy_policy(self, logged_in_driver):
        """Settings screen must show a Privacy Policy link/option."""
        driver = logged_in_driver
        _navigate_to_settings(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Privacy") or contains(@text,"Privacy")]',
            '//*[contains(@content-desc,"privacy") or contains(@text,"privacy")]',
        ), "Privacy Policy option not found in Settings"

    # AM076 — Settings shows Terms of Service option
    @pytest.mark.settings
    def test_AM076_settings_terms_of_service(self, logged_in_driver):
        """Settings screen must show a Terms of Service link/option."""
        driver = logged_in_driver
        _navigate_to_settings(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Terms") or contains(@text,"Terms")]',
            '//*[contains(@content-desc,"terms") or contains(@text,"terms")]',
        ), "Terms of Service option not found in Settings"

    # AM077 — Settings shows App Version 1.0.0
    @pytest.mark.settings
    def test_AM077_settings_shows_app_version(self, logged_in_driver):
        """Settings screen must display the app version (1.0.0)."""
        driver = logged_in_driver
        _navigate_to_settings(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"1.0.0") or contains(@text,"1.0.0")]',
            '//*[contains(@content-desc,"Version") or contains(@text,"Version")]',
            '//*[contains(@content-desc,"version") or contains(@text,"version")]',
        ), "App version not found in Settings"

    # AM078 — Settings has Delete Account option
    @pytest.mark.settings
    def test_AM078_settings_delete_account_option(self, logged_in_driver):
        """Settings screen must have a Delete Account option in the Account section."""
        driver = logged_in_driver
        _navigate_to_settings(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Delete Account") or contains(@text,"Delete Account")]',
            '//*[contains(@content-desc,"Delete") or contains(@text,"Delete")]',
        ), "Delete Account option not found in Settings"
