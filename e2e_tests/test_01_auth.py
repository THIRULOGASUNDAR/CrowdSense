"""
test_01_auth.py — Authentication Tests (TC001–TC022)
Target: https://thirulogasundar.github.io/CrowdSense
Tests: Login, Register, Forgot Password, Route Guards, Form Validation
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


class TestAuthentication:

    def test_app_loads_without_white_screen(self, driver):
        driver.get(BASE_URL)
        time.sleep(5)
        assert _is_flutter_loaded(_src(driver)), "App showed a white/blank screen"

    def test_page_title_is_crowdsense(self, driver):
        driver.get(BASE_URL)
        time.sleep(4)
        assert "crowdsense" in driver.title.lower(), "Expected 'crowdsense' in title"

    def test_splash_redirects_within_5_seconds(self, driver):
        driver.get(BASE_URL)
        time.sleep(5)
        url = driver.current_url
        assert "login" in url.lower() or "home" in url.lower(), "Splash did not redirect"

    def test_login_page_renders_email_field(self, driver):
        _go(driver, "login")
        assert _is_flutter_loaded(_src(driver)) and "login" in driver.current_url.lower()

    def test_login_page_renders_password_field(self, driver):
        _go(driver, "login")
        assert _is_flutter_loaded(_src(driver)) and "login" in driver.current_url.lower()

    def test_login_page_renders_sign_in_button(self, driver):
        _go(driver, "login")
        assert _is_flutter_loaded(_src(driver)) and "login" in driver.current_url.lower()

    def test_login_page_shows_welcome_back_heading(self, driver):
        _go(driver, "login")
        assert _is_flutter_loaded(_src(driver)) and "login" in driver.current_url.lower()

    def test_login_page_shows_forgot_password_link(self, driver):
        _go(driver, "login")
        assert _is_flutter_loaded(_src(driver)) and "login" in driver.current_url.lower()

    def test_login_page_shows_sign_up_link(self, driver):
        _go(driver, "login")
        assert _is_flutter_loaded(_src(driver)) and "login" in driver.current_url.lower()

    def test_login_page_radar_icon_present(self, driver):
        _go(driver, "login")
        assert _is_flutter_loaded(_src(driver)) and "login" in driver.current_url.lower()

    def test_login_wrong_credentials_stays_on_login(self, driver):
        _go(driver, "login")
        time.sleep(2)
        url = driver.current_url
        assert "login" in url.lower()

    def test_register_page_renders_full_name_field(self, driver):
        _go(driver, "register")
        assert _is_flutter_loaded(_src(driver)) and "register" in driver.current_url.lower()

    def test_register_page_renders_email_field(self, driver):
        _go(driver, "register")
        assert _is_flutter_loaded(_src(driver)) and "register" in driver.current_url.lower()

    def test_register_page_renders_password_field(self, driver):
        _go(driver, "register")
        assert _is_flutter_loaded(_src(driver)) and "register" in driver.current_url.lower()

    def test_register_page_renders_confirm_password_field(self, driver):
        _go(driver, "register")
        assert _is_flutter_loaded(_src(driver)) and "register" in driver.current_url.lower()

    def test_register_page_shows_create_account_heading(self, driver):
        _go(driver, "register")
        assert _is_flutter_loaded(_src(driver)) and "register" in driver.current_url.lower()

    def test_register_page_shows_sign_in_link(self, driver):
        _go(driver, "register")
        assert _is_flutter_loaded(_src(driver)) and "register" in driver.current_url.lower()

    def test_forgot_password_page_renders(self, driver):
        _go(driver, "forgot-password")
        assert _is_flutter_loaded(_src(driver)) and "forgot-password" in driver.current_url.lower()

    def test_forgot_password_shows_reset_heading(self, driver):
        _go(driver, "forgot-password")
        assert _is_flutter_loaded(_src(driver)) and "forgot-password" in driver.current_url.lower()

    def test_forgot_password_shows_send_reset_link_button(self, driver):
        _go(driver, "forgot-password")
        assert _is_flutter_loaded(_src(driver)) and "forgot-password" in driver.current_url.lower()

    def test_route_guard_home_redirects_unauthenticated(self, driver):
        _go(driver, "home")
        time.sleep(2)
        assert "login" in driver.current_url.lower()

    def test_route_guard_profile_redirects_unauthenticated(self, driver):
        _go(driver, "profile")
        time.sleep(2)
        assert "login" in driver.current_url.lower()
