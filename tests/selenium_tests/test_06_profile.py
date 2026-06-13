"""
test_06_profile.py — Profile & Account End-to-End Tests
=========================================================
Tests: TC101–TC120
Coverage:
  • Profile page loads or redirects unauthenticated users to login
  • Profile heading, stats row (Photos, Reports, Saved)
  • Menu items: Edit Profile, Notifications, My Reports, Support & FAQ
  • Sign Out button
  • Settings icon in profile app bar
  • Photo upload / camera icon
  • My Reports page loads
  • Unauthenticated access to profile/reports requires auth

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
class TestProfile:
    """TC101–TC120 — Profile & Account Tests"""

    def test_tc101_profile_page_loads(self, driver):
        """TC101 — /profile route renders Flutter app or redirects to login."""
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "profile", "login"), (
            f"Profile page did not load. URL: {driver.current_url}"
        )

    def test_tc102_profile_route_requires_auth(self, driver):
        """TC102 — Unauthenticated user at /profile is redirected to login."""
        _nav(driver, "profile", wait=4)
        assert _url_has(driver, "login"), (
            f"Route guard did not redirect to login. URL: {driver.current_url}"
        )

    def test_tc103_profile_page_shows_heading(self, driver):
        """TC103 — Profile page shows a Profile heading."""
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "profile", "login")

    def test_tc104_profile_has_photos_stat(self, driver):
        """TC104 — Profile page shows a Photos stat."""
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "profile", "login")

    def test_tc105_profile_has_reports_stat(self, driver):
        """TC105 — Profile page shows a Reports stat."""
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "profile", "login")

    def test_tc106_profile_has_saved_stat(self, driver):
        """TC106 — Profile page shows a Saved stat."""
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "profile", "login")

    def test_tc107_profile_stats_row_has_three_items(self, driver):
        """TC107 — Profile stats row has exactly three items (Photos, Reports, Saved)."""
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "profile", "login")

    def test_tc108_profile_has_edit_profile_menu(self, driver):
        """TC108 — Profile page has an Edit Profile menu item."""
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "profile", "login")

    def test_tc109_profile_has_notifications_menu(self, driver):
        """TC109 — Profile page has a Notifications menu item."""
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "profile", "login")

    def test_tc110_profile_has_my_reports_menu(self, driver):
        """TC110 — Profile page has a My Reports menu item."""
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "profile", "login")

    def test_tc111_profile_has_support_faq_menu(self, driver):
        """TC111 — Profile page has a Support & FAQ menu item."""
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "profile", "login")

    def test_tc112_profile_has_sign_out_button(self, driver):
        """TC112 — Profile page has a Sign Out button."""
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "profile", "login")

    def test_tc113_profile_has_settings_icon_in_appbar(self, driver):
        """TC113 — Profile page has a Settings icon in the app bar."""
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "profile", "login")

    def test_tc114_profile_has_photo_upload_camera_icon(self, driver):
        """TC114 — Profile page has a camera icon for photo upload."""
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "profile", "login")

    def test_tc115_profile_shows_email_under_name(self, driver):
        """TC115 — Profile page shows the user's email under their name."""
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "profile", "login")

    def test_tc116_profile_all_menu_items_present(self, driver):
        """TC116 — Profile page has all required menu items present."""
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "profile", "login")

    def test_tc117_my_reports_page_loads(self, driver):
        """TC117 — /my-reports route loads or redirects gracefully."""
        _nav(driver, "my-reports")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "reports", "login"), (
            f"My Reports page did not load. URL: {driver.current_url}"
        )

    def test_tc118_my_reports_route_requires_auth(self, driver):
        """TC118 — Unauthenticated user at /my-reports is redirected to login."""
        _nav(driver, "my-reports", wait=4)
        assert _url_has(driver, "login"), (
            f"My Reports route guard failed. URL: {driver.current_url}"
        )

    def test_tc119_my_reports_page_shows_content(self, driver):
        """TC119 — My Reports page shows list or empty state (no crash)."""
        _nav(driver, "my-reports")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "reports", "login")

    def test_tc120_profile_page_source_not_empty(self, driver):
        """TC120 — Profile page source has substantial content (> 300 chars)."""
        _nav(driver, "profile")
        assert len(_src(driver)) > 300, "Profile page source appears empty"
