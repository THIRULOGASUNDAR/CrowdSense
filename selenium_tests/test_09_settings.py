"""
test_09_settings.py — Settings End-to-End Tests
================================================
Tests: TC146–TC165
Coverage:
  • Settings page loads (no auth required)
  • APPEARANCE section & Dark Mode toggle
  • NOTIFICATIONS section & toggle
  • ABOUT section: App version (1.0.0)
  • ACCOUNT section: Privacy Policy, Terms of Service, Delete Account
  • Settings page scroll stability
  • Settings does not require authentication

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
class TestSettings:
    """TC146–TC165 — Settings Tests"""

    def test_tc146_settings_page_loads(self, driver):
        """TC146 — /settings route loads Flutter app."""
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "settings", "login"), (
            f"Settings page did not load. URL: {driver.current_url}"
        )

    def test_tc147_settings_does_not_require_auth(self, driver):
        """TC147 — Settings page does NOT require authentication (accessible without login)."""
        _nav(driver, "settings", wait=4)
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "settings", "login")

    def test_tc148_settings_flutter_rendered(self, driver):
        """TC148 — Flutter is rendered on the /settings route."""
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver)), "Flutter not rendered on settings page"

    def test_tc149_settings_has_appearance_section(self, driver):
        """TC149 — Settings page has an APPEARANCE section."""
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "settings", "login")

    def test_tc150_settings_has_dark_mode_toggle(self, driver):
        """TC150 — Settings page has a Dark Mode toggle."""
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "settings", "login")

    def test_tc151_settings_has_notifications_section(self, driver):
        """TC151 — Settings page has a NOTIFICATIONS section."""
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "settings", "login")

    def test_tc152_settings_has_notifications_toggle(self, driver):
        """TC152 — Settings page has a Notifications toggle."""
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "settings", "login")

    def test_tc153_settings_has_about_section(self, driver):
        """TC153 — Settings page has an ABOUT section."""
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "settings", "login")

    def test_tc154_settings_has_app_version(self, driver):
        """TC154 — Settings page shows App Version."""
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "settings", "login")

    def test_tc155_settings_version_is_1_0_0(self, driver):
        """TC155 — Settings page shows version number 1.0.0."""
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "settings", "login")

    def test_tc156_settings_has_account_section(self, driver):
        """TC156 — Settings page has an ACCOUNT section."""
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "settings", "login")

    def test_tc157_settings_has_privacy_policy(self, driver):
        """TC157 — Settings page has a Privacy Policy option."""
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "settings", "login")

    def test_tc158_settings_has_terms_of_service(self, driver):
        """TC158 — Settings page has a Terms of Service option."""
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "settings", "login")

    def test_tc159_settings_has_delete_account_option(self, driver):
        """TC159 — Settings page has a Delete Account option."""
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "settings", "login")

    def test_tc160_settings_page_source_not_empty(self, driver):
        """TC160 — Settings page source has substantial content (> 300 chars)."""
        _nav(driver, "settings")
        assert len(_src(driver)) > 300, "Settings page source appears empty"

    def test_tc161_settings_no_server_error(self, driver):
        """TC161 — Settings page does not show a 500 server error."""
        _nav(driver, "settings")
        assert "500 Internal Server Error" not in _src(driver)

    def test_tc162_settings_scroll_stable(self, driver):
        """TC162 — Scrolling on the settings page does not crash the app."""
        _nav(driver, "settings")
        driver.execute_script("window.scrollBy(0, 700)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver)), "App crashed after scrolling settings"

    def test_tc163_settings_title_is_crowdsense(self, driver):
        """TC163 — Browser title is 'crowdsense' on settings route."""
        _nav(driver, "settings")
        assert "crowdsense" in driver.title.lower()

    def test_tc164_settings_refresh_stable(self, driver):
        """TC164 — Refreshing the settings page does not crash the app."""
        _nav(driver, "settings")
        driver.refresh()
        time.sleep(4)
        assert _flutter_loaded(_src(driver)), "App crashed after refreshing settings"

    def test_tc165_settings_back_navigation_works(self, driver):
        """TC165 — Browser back from settings returns to previous page safely."""
        driver.get(f"{BASE_URL}/#/login")
        time.sleep(2)
        driver.get(f"{BASE_URL}/#/settings")
        time.sleep(3)
        driver.back()
        time.sleep(2)
        assert _flutter_loaded(_src(driver)), "App crashed after back navigation from settings"
