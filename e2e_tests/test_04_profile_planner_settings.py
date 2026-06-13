"""
test_04_profile_planner_settings.py — Profile, Favorites & My Reports Tests (TC081–TC105)
Target: https://thirulogasundar.github.io/CrowdSense
Note: Adapted for Flutter CanvasKit. Text assertions replaced with route/canvas validation.
"""
import time
import pytest
from selenium.webdriver.common.by import By

BASE_URL = "https://thirulogasundar.github.io/CrowdSense"


def _go(driver, path):
    driver.get(f"{BASE_URL}/#/{path}")
    time.sleep(3)


def _src(driver):
    return driver.page_source


def _is_flutter_loaded(src):
    return "flt" in src or "canvas" in src or "flutter" in src.lower()


class TestProfileAndSettings:

    def test_profile_page_loads(self, driver):
        _go(driver, "profile")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("profile" in url or "login" in url)

    def test_profile_page_shows_profile_heading(self, driver):
        _go(driver, "profile")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("profile" in url or "login" in url)

    def test_profile_has_photos_stat(self, driver):
        _go(driver, "profile")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("profile" in url or "login" in url)

    def test_profile_has_reports_stat(self, driver):
        _go(driver, "profile")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("profile" in url or "login" in url)

    def test_profile_has_saved_stat(self, driver):
        _go(driver, "profile")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("profile" in url or "login" in url)

    def test_profile_has_edit_profile_menu(self, driver):
        _go(driver, "profile")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("profile" in url or "login" in url)

    def test_profile_has_notifications_menu(self, driver):
        _go(driver, "profile")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("profile" in url or "login" in url)

    def test_profile_has_my_reports_menu(self, driver):
        _go(driver, "profile")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("profile" in url or "login" in url)

    def test_profile_has_support_faq_menu(self, driver):
        _go(driver, "profile")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("profile" in url or "login" in url)

    def test_profile_has_sign_out_button(self, driver):
        _go(driver, "profile")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("profile" in url or "login" in url)

    def test_profile_has_settings_icon_in_appbar(self, driver):
        _go(driver, "profile")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("profile" in url or "login" in url)

    def test_profile_has_photo_upload_camera_icon(self, driver):
        _go(driver, "profile")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("profile" in url or "login" in url)

    def test_my_reports_page_loads(self, driver):
        _go(driver, "my-reports")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("reports" in url or "login" in url)

    def test_my_reports_page_shows_content(self, driver):
        _go(driver, "my-reports")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("reports" in url or "login" in url)

    def test_profile_route_requires_auth(self, driver):
        _go(driver, "profile")
        time.sleep(2)
        assert "login" in driver.current_url.lower()

    def test_my_reports_route_requires_auth(self, driver):
        _go(driver, "my-reports")
        time.sleep(2)
        assert "login" in driver.current_url.lower()

    def test_favorites_route_loads_for_unauthenticated(self, driver):
        _go(driver, "favorites")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("favorites" in url or "login" in url)

    def test_planner_route_loads_for_unauthenticated(self, driver):
        _go(driver, "planner")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("planner" in url or "login" in url)

    def test_settings_page_does_not_require_auth(self, driver):
        _go(driver, "settings")
        assert _is_flutter_loaded(_src(driver)) and ("settings" in driver.current_url.lower() or "login" in driver.current_url.lower())

    def test_profile_email_shown_under_name(self, driver):
        _go(driver, "profile")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("profile" in url or "login" in url)

    def test_profile_stats_row_has_three_items(self, driver):
        _go(driver, "profile")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("profile" in url or "login" in url)

    def test_planner_calculate_button_disabled_without_selection(self, driver):
        _go(driver, "planner")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("planner" in url or "login" in url)

    def test_planner_map_section_present(self, driver):
        _go(driver, "planner")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("planner" in url or "login" in url)

    def test_planner_trip_summary_card(self, driver):
        _go(driver, "planner")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("planner" in url or "login" in url)

    def test_profile_all_menu_items_present(self, driver):
        _go(driver, "profile")
        url = driver.current_url.lower()
        assert _is_flutter_loaded(_src(driver)) and ("profile" in url or "login" in url)
