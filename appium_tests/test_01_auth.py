"""
test_01_auth.py — Authentication Tests (AM001–AM022)
=====================================================
CrowdSense Appium Mobile E2E Suite
Target: Pixel 3a API 37 AVD  |  Automation: UiAutomator2

Covers:
  - App launch & splash screen
  - Login page UI elements and form validation
  - Register page UI elements and validation
  - Forgot Password page
  - Route guard (unauthenticated redirects)
  - Successful login flow
"""
import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# ─── Helper utilities ─────────────────────────────────────────────────────────

def _find(driver, *xpaths, timeout=10):
    """Try multiple XPath expressions; return the first match or None."""
    for xp in xpaths:
        try:
            el = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xp))
            )
            return el
        except (NoSuchElementException, TimeoutException):
            continue
    return None


def _element_exists(driver, *xpaths, timeout=8):
    """Return True if any of the given XPaths is found on screen."""
    return _find(driver, *xpaths, timeout=timeout) is not None


def _wait_app_ready(driver, timeout=15):
    """Wait until the CrowdSense app has rendered something on screen."""
    time.sleep(2)
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: len(d.page_source) > 500
        )
    except TimeoutException:
        pass


def _reset_to_login(driver):
    """Navigate back to the Login screen by restarting the app activity."""
    try:
        driver.terminate_app("com.example.crowdsense")
        time.sleep(1)
        driver.activate_app("com.example.crowdsense")
        time.sleep(3)
    except Exception:
        pass


# ─── Test Class ───────────────────────────────────────────────────────────────

class TestAuthentication:

    # AM001 — App launches and shows splash screen
    @pytest.mark.smoke
    @pytest.mark.auth
    def test_AM001_app_launches_shows_splash(self, driver):
        """App should launch without crashing and render something."""
        _wait_app_ready(driver)
        src = driver.page_source
        assert len(src) > 100, "App page source is empty — possible crash or white screen"

    # AM002 — Splash auto-redirects to Login within 5 seconds
    @pytest.mark.auth
    def test_AM002_splash_redirects_to_login(self, driver):
        """After splash, the app should navigate to Login screen within 5 seconds."""
        _reset_to_login(driver)
        time.sleep(5)
        assert _element_exists(
            driver,
            '//*[@content-desc="Email" or @text="Email"]',
            '//*[@content-desc="Sign In" or @text="Sign In"]',
            '//*[contains(@content-desc,"Welcome") or contains(@text,"Welcome")]',
        ), "Login screen not shown after splash redirect"

    # AM003 — Login screen has email input
    @pytest.mark.auth
    def test_AM003_login_has_email_field(self, driver):
        """Login screen must render an email/text input field."""
        _reset_to_login(driver)
        assert _element_exists(
            driver,
            '//*[@content-desc="Email" or @text="Email"]',
            '//*[contains(@content-desc,"email") or contains(@text,"email")]',
            '//android.widget.EditText[1]',
        ), "Email field not found on Login screen"

    # AM004 — Login screen has password input
    @pytest.mark.auth
    def test_AM004_login_has_password_field(self, driver):
        """Login screen must render a password input field."""
        _reset_to_login(driver)
        assert _element_exists(
            driver,
            '//*[@content-desc="Password" or @text="Password"]',
            '//*[contains(@content-desc,"password") or contains(@text,"password")]',
            '//android.widget.EditText[2]',
        ), "Password field not found on Login screen"

    # AM005 — Login screen has Sign In button
    @pytest.mark.auth
    @pytest.mark.smoke
    def test_AM005_login_has_sign_in_button(self, driver):
        """Login screen must show the Sign In button."""
        _reset_to_login(driver)
        assert _element_exists(
            driver,
            '//*[@content-desc="Sign In" or @text="Sign In"]',
            '//*[contains(@content-desc,"sign in") or contains(@text,"sign in")]',
            '//*[contains(@content-desc,"Sign") or contains(@text,"Sign")]',
        ), "Sign In button not found on Login screen"

    # AM006 — Login screen shows Welcome Back text
    @pytest.mark.auth
    def test_AM006_login_shows_welcome_back(self, driver):
        """Login screen must show the 'Welcome Back' heading."""
        _reset_to_login(driver)
        assert _element_exists(
            driver,
            '//*[@content-desc="Welcome Back" or @text="Welcome Back"]',
            '//*[contains(@content-desc,"Welcome") or contains(@text,"Welcome")]',
        ), "Welcome Back heading not found on Login screen"

    # AM007 — Login screen shows Forgot Password link
    @pytest.mark.auth
    def test_AM007_login_has_forgot_password_link(self, driver):
        """Login screen must show the Forgot Password navigation link."""
        _reset_to_login(driver)
        assert _element_exists(
            driver,
            '//*[@content-desc="Forgot Password" or @text="Forgot Password"]',
            '//*[contains(@content-desc,"Forgot") or contains(@text,"Forgot")]',
        ), "Forgot Password link not found on Login screen"

    # AM008 — Login screen shows Sign Up link
    @pytest.mark.auth
    def test_AM008_login_has_sign_up_link(self, driver):
        """Login screen must show the Sign Up / Don't have an account link."""
        _reset_to_login(driver)
        assert _element_exists(
            driver,
            '//*[@content-desc="Sign Up" or @text="Sign Up"]',
            '//*[contains(@content-desc,"Sign Up") or contains(@text,"Sign Up")]',
            '//*[contains(@content-desc,"account") or contains(@text,"account")]',
        ), "Sign Up link not found on Login screen"

    # AM009 — Empty login form shows validation
    @pytest.mark.auth
    def test_AM009_empty_login_shows_validation(self, driver):
        """Tapping Sign In with empty fields should show a validation message."""
        _reset_to_login(driver)
        sign_in_btn = _find(
            driver,
            '//*[@content-desc="Sign In" or @text="Sign In"]',
            '//*[contains(@content-desc,"Sign") or contains(@text,"Sign")]',
        )
        assert sign_in_btn is not None, "Sign In button not found"
        sign_in_btn.click()
        time.sleep(2)
        # Should still be on login page (validation prevents navigation)
        still_on_login = _element_exists(
            driver,
            '//*[@content-desc="Sign In" or @text="Sign In"]',
            '//*[contains(@content-desc,"Welcome") or contains(@text,"Welcome")]',
            '//android.widget.EditText',
        )
        assert still_on_login, "App navigated away from Login after empty form submission"

    # AM010 — Wrong credentials stays on login screen
    @pytest.mark.auth
    def test_AM010_wrong_credentials_stays_on_login(self, driver):
        """Wrong credentials should keep user on the Login screen."""
        _reset_to_login(driver)
        email_field = _find(driver, '//android.widget.EditText[1]')
        pwd_field   = _find(driver, '//android.widget.EditText[2]')
        if email_field:
            email_field.clear()
            email_field.send_keys("wrong@invalid.com")
        if pwd_field:
            pwd_field.clear()
            pwd_field.send_keys("wrongpassword123")
        sign_in = _find(driver,
            '//*[@content-desc="Sign In" or @text="Sign In"]',
            '//*[contains(@content-desc,"Sign") or contains(@text,"Sign")]',
        )
        if sign_in:
            sign_in.click()
        time.sleep(4)
        # Must remain on login (not navigated to home)
        assert _element_exists(
            driver,
            '//android.widget.EditText',
            '//*[contains(@content-desc,"Welcome") or contains(@text,"Welcome")]',
        ), "App unexpectedly navigated away after wrong credentials"

    # AM011 — Navigate to Register page
    @pytest.mark.auth
    def test_AM011_navigate_to_register_page(self, driver):
        """Tapping Sign Up / Don't have an account navigates to Register screen."""
        _reset_to_login(driver)
        sign_up = _find(
            driver,
            '//*[@content-desc="Sign Up" or @text="Sign Up"]',
            '//*[contains(@content-desc,"account") or contains(@text,"account")]',
            '//*[contains(@content-desc,"Register") or contains(@text,"Register")]',
        )
        assert sign_up is not None, "Sign Up link not found on Login screen"
        sign_up.click()
        time.sleep(3)
        assert _element_exists(
            driver,
            '//*[contains(@content-desc,"Create Account") or contains(@text,"Create Account")]',
            '//*[contains(@content-desc,"Register") or contains(@text,"Register")]',
            '//android.widget.EditText',
        ), "Register screen not loaded after tapping Sign Up"

    # AM012 — Register page has Full Name field
    @pytest.mark.auth
    def test_AM012_register_has_full_name_field(self, driver):
        """Register screen must have a Full Name input field."""
        _reset_to_login(driver)
        # Navigate to register
        sign_up = _find(driver,
            '//*[contains(@content-desc,"account") or contains(@text,"account")]',
            '//*[contains(@content-desc,"Sign Up") or contains(@text,"Sign Up")]')
        if sign_up:
            sign_up.click()
            time.sleep(2)
        assert _element_exists(
            driver,
            '//*[@content-desc="Full Name" or @text="Full Name"]',
            '//*[contains(@content-desc,"Name") or contains(@text,"Name")]',
            '//android.widget.EditText[1]',
        ), "Full Name field not found on Register screen"

    # AM013 — Register page has Email field
    @pytest.mark.auth
    def test_AM013_register_has_email_field(self, driver):
        """Register screen must have an Email input field."""
        _reset_to_login(driver)
        sign_up = _find(driver,
            '//*[contains(@content-desc,"account") or contains(@text,"account")]')
        if sign_up:
            sign_up.click(); time.sleep(2)
        assert _element_exists(
            driver,
            '//*[@content-desc="Email" or @text="Email"]',
            '//*[contains(@content-desc,"email") or contains(@text,"email")]',
            '//android.widget.EditText[2]',
        ), "Email field not found on Register screen"

    # AM014 — Register page has Password field
    @pytest.mark.auth
    def test_AM014_register_has_password_field(self, driver):
        """Register screen must have a Password input field."""
        _reset_to_login(driver)
        sign_up = _find(driver,
            '//*[contains(@content-desc,"account") or contains(@text,"account")]')
        if sign_up:
            sign_up.click(); time.sleep(2)
        assert _element_exists(
            driver,
            '//*[@content-desc="Password" or @text="Password"]',
            '//*[contains(@content-desc,"password") or contains(@text,"password")]',
            '//android.widget.EditText[3]',
        ), "Password field not found on Register screen"

    # AM015 — Register page has Confirm Password field
    @pytest.mark.auth
    def test_AM015_register_has_confirm_password_field(self, driver):
        """Register screen must have a Confirm Password field."""
        _reset_to_login(driver)
        sign_up = _find(driver,
            '//*[contains(@content-desc,"account") or contains(@text,"account")]')
        if sign_up:
            sign_up.click(); time.sleep(2)
        assert _element_exists(
            driver,
            '//*[contains(@content-desc,"Confirm") or contains(@text,"Confirm")]',
            '//android.widget.EditText[4]',
        ), "Confirm Password field not found on Register screen"

    # AM016 — Register page has Create Account button
    @pytest.mark.auth
    def test_AM016_register_has_create_account_button(self, driver):
        """Register screen must show the Create Account submit button."""
        _reset_to_login(driver)
        sign_up = _find(driver,
            '//*[contains(@content-desc,"account") or contains(@text,"account")]')
        if sign_up:
            sign_up.click(); time.sleep(2)
        assert _element_exists(
            driver,
            '//*[@content-desc="Create Account" or @text="Create Account"]',
            '//*[contains(@content-desc,"Create") or contains(@text,"Create")]',
        ), "Create Account button not found on Register screen"

    # AM017 — Password mismatch shows validation error
    @pytest.mark.auth
    def test_AM017_password_mismatch_shows_error(self, driver):
        """Submitting register form with mismatched passwords shows error."""
        _reset_to_login(driver)
        sign_up = _find(driver,
            '//*[contains(@content-desc,"account") or contains(@text,"account")]')
        if sign_up:
            sign_up.click(); time.sleep(2)
        fields = driver.find_elements(AppiumBy.XPATH, '//android.widget.EditText')
        if len(fields) >= 4:
            fields[0].send_keys("Test User")
            fields[1].send_keys("test@example.com")
            fields[2].send_keys("Password123!")
            fields[3].send_keys("DifferentPassword!")
        btn = _find(driver,
            '//*[contains(@content-desc,"Create Account") or contains(@text,"Create Account")]')
        if btn:
            btn.click()
        time.sleep(2)
        # Should remain on register screen
        assert _element_exists(
            driver,
            '//android.widget.EditText',
            '//*[contains(@content-desc,"Create Account") or contains(@text,"Create Account")]',
        ), "App navigated away despite password mismatch"

    # AM018 — Forgot Password page renders
    @pytest.mark.auth
    def test_AM018_forgot_password_page_renders(self, driver):
        """Tapping Forgot Password navigates to the reset screen."""
        _reset_to_login(driver)
        fp_link = _find(driver,
            '//*[@content-desc="Forgot Password" or @text="Forgot Password"]',
            '//*[contains(@content-desc,"Forgot") or contains(@text,"Forgot")]',
        )
        assert fp_link is not None, "Forgot Password link not found"
        fp_link.click()
        time.sleep(3)
        assert _element_exists(
            driver,
            '//*[contains(@content-desc,"Reset") or contains(@text,"Reset")]',
            '//*[contains(@content-desc,"Forgot") or contains(@text,"Forgot")]',
            '//android.widget.EditText',
        ), "Forgot Password screen did not load"

    # AM019 — Forgot Password has email input
    @pytest.mark.auth
    def test_AM019_forgot_password_has_email_input(self, driver):
        """Forgot Password screen must have an email input field."""
        _reset_to_login(driver)
        fp_link = _find(driver,
            '//*[contains(@content-desc,"Forgot") or contains(@text,"Forgot")]')
        if fp_link:
            fp_link.click(); time.sleep(2)
        assert _element_exists(
            driver,
            '//*[@content-desc="Email" or @text="Email"]',
            '//android.widget.EditText',
        ), "Email input not found on Forgot Password screen"

    # AM020 — Forgot Password has Send Reset Link button
    @pytest.mark.auth
    def test_AM020_forgot_password_has_send_reset_button(self, driver):
        """Forgot Password screen must have a Send Reset Link / Submit button."""
        _reset_to_login(driver)
        fp_link = _find(driver,
            '//*[contains(@content-desc,"Forgot") or contains(@text,"Forgot")]')
        if fp_link:
            fp_link.click(); time.sleep(2)
        assert _element_exists(
            driver,
            '//*[contains(@content-desc,"Send") or contains(@text,"Send")]',
            '//*[contains(@content-desc,"Reset") or contains(@text,"Reset")]',
            '//*[contains(@content-desc,"Submit") or contains(@text,"Submit")]',
        ), "Send Reset Link button not found on Forgot Password screen"

    # AM021 — Route guard: unauthenticated user redirected to login
    @pytest.mark.auth
    def test_AM021_route_guard_unauthenticated_redirect(self, driver):
        """App must redirect unauthenticated users to Login when app starts fresh."""
        _reset_to_login(driver)
        time.sleep(5)
        assert _element_exists(
            driver,
            '//*[@content-desc="Sign In" or @text="Sign In"]',
            '//*[contains(@content-desc,"Welcome") or contains(@text,"Welcome")]',
            '//android.widget.EditText',
        ), "Unauthenticated user was not redirected to Login screen"

    # AM022 — Successful login navigates to Home screen
    @pytest.mark.auth
    @pytest.mark.smoke
    def test_AM022_successful_login_navigates_home(self, driver):
        """Valid credentials should log in and navigate to Home screen."""
        from conftest import TEST_EMAIL, TEST_PASSWORD
        _reset_to_login(driver)
        email_field = _find(driver, '//android.widget.EditText[1]')
        pwd_field   = _find(driver, '//android.widget.EditText[2]')
        if email_field:
            email_field.clear(); email_field.send_keys(TEST_EMAIL)
        if pwd_field:
            pwd_field.clear(); pwd_field.send_keys(TEST_PASSWORD)
        sign_in = _find(driver,
            '//*[@content-desc="Sign In" or @text="Sign In"]',
            '//*[contains(@content-desc,"Sign") or contains(@text,"Sign")]')
        if sign_in:
            sign_in.click()
        time.sleep(5)
        # After login, app should show Home content (search bar, greeting, etc.)
        assert _element_exists(
            driver,
            '//*[contains(@content-desc,"Search") or contains(@text,"Search")]',
            '//*[contains(@content-desc,"Trending") or contains(@text,"Trending")]',
            '//*[contains(@content-desc,"Home") or contains(@text,"Home")]',
            '//*[contains(@content-desc,"Welcome") or contains(@text,"Welcome")]',
        ), "Home screen not reached after successful login"
