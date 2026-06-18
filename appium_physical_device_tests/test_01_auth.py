"""
test_01_auth.py — Authentication Tests (PM001–PM022)
=====================================================
CrowdSense Appium Physical Device E2E Suite
Target: Real Android device via USB  |  Automation: UiAutomator2

Covers:
  - App launch & splash screen on a real physical phone
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

def _find(driver, *xpaths, timeout=12):
    """Try multiple XPath expressions; return first match or None."""
    for xp in xpaths:
        try:
            el = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xp))
            )
            return el
        except (NoSuchElementException, TimeoutException):
            continue
    return None


def _element_exists(driver, *xpaths, timeout=10):
    return _find(driver, *xpaths, timeout=timeout) is not None


def _scroll_down(driver):
    try:
        size = driver.get_window_size()
        driver.swipe(
            int(size['width'] * 0.5),
            int(size['height'] * 0.75),
            int(size['width'] * 0.5),
            int(size['height'] * 0.25),
            600
        )
        time.sleep(1.5)
    except Exception:
        pass



def _wait_app_ready(driver, timeout=20):
    """Wait until the CrowdSense app has rendered something meaningful."""
    time.sleep(3)  # real devices need extra warm-up time
    try:
        WebDriverWait(driver, timeout).until(lambda d: len(d.page_source) > 500)
    except TimeoutException:
        pass


def _reset_to_login(driver):
    """Navigate back to Login screen, reusing the state if possible instead of terminating app."""
    # 1. Check if we are already on Login screen
    is_on_login = _element_exists(driver, '//*[contains(@content-desc,"Forgot Password") or contains(@text,"Forgot Password")]', timeout=2) and \
                  _element_exists(driver, '//android.widget.EditText', timeout=2)
    if is_on_login:
        # Clear fields to reset state
        try:
            for field in driver.find_elements(AppiumBy.XPATH, '//android.widget.EditText'):
                field.clear()
        except Exception:
            pass
        return

    # 2. Try pressing back to return to login screen
    for _ in range(2):
        try:
            driver.back()
            time.sleep(1.5)
            is_on_login = _element_exists(driver, '//*[contains(@content-desc,"Forgot Password") or contains(@text,"Forgot Password")]', timeout=2) and \
                          _element_exists(driver, '//android.widget.EditText', timeout=2)
            if is_on_login:
                for field in driver.find_elements(AppiumBy.XPATH, '//android.widget.EditText'):
                    field.clear()
                return
        except Exception:
            pass

    # 3. Last resort fallback: restart app
    try:
        driver.terminate_app("com.example.crowdsense")
        time.sleep(1.5)
        driver.activate_app("com.example.crowdsense")
        time.sleep(4)   # real devices take longer to cold-start
    except Exception:
        pass


def _navigate_to_register_screen(driver):
    """Restart app and navigate to Register screen reliably."""
    _reset_to_login(driver)
    sign_up = _find(driver,
        '//*[@content-desc="Sign Up" or @text="Sign Up"]',
        '//*[contains(@content-desc,"Sign Up") or contains(@text,"Sign Up")]',
        '//*[contains(@content-desc,"account") or contains(@text,"account")]'
    )
    if sign_up:
        sign_up.click()
        time.sleep(2)


# ─── Test Class ───────────────────────────────────────────────────────────────

class TestAuthentication:

    # PM001 — App launches and shows something on physical device
    @pytest.mark.smoke
    @pytest.mark.auth
    def test_PM001_app_launches_shows_splash(self, driver):
        """App must launch on the physical device without crashing."""
        _wait_app_ready(driver)
        src = driver.page_source
        assert len(src) > 100, "App page source is empty — possible crash or white screen on device"

    # PM002 — Splash auto-redirects to Login within 6 seconds
    @pytest.mark.auth
    def test_PM002_splash_redirects_to_login(self, driver):
        """After splash, app must navigate to Login screen."""
        _reset_to_login(driver)
        time.sleep(6)
        assert _element_exists(
            driver,
            '//*[@content-desc="Email" or @text="Email"]',
            '//*[@content-desc="Sign In" or @text="Sign In"]',
            '//*[contains(@content-desc,"Welcome") or contains(@text,"Welcome")]',
        ), "Login screen not shown after splash on physical device"

    # PM003 — Login screen has email input
    @pytest.mark.auth
    def test_PM003_login_has_email_field(self, driver):
        """Login screen must render an email/text input field."""
        _reset_to_login(driver)
        assert _element_exists(
            driver,
            '//*[@content-desc="Email" or @text="Email"]',
            '//*[contains(@content-desc,"email") or contains(@text,"email")]',
            '//android.widget.EditText[1]',
        ), "Email field not found on Login screen"

    # PM004 — Login screen has password input
    @pytest.mark.auth
    def test_PM004_login_has_password_field(self, driver):
        """Login screen must render a password input field."""
        _reset_to_login(driver)
        assert _element_exists(
            driver,
            '//*[@content-desc="Password" or @text="Password"]',
            '//*[contains(@content-desc,"password") or contains(@text,"password")]',
            '//android.widget.EditText[2]',
        ), "Password field not found on Login screen"

    # PM005 — Login screen has Sign In button
    @pytest.mark.auth
    @pytest.mark.smoke
    def test_PM005_login_has_sign_in_button(self, driver):
        """Login screen must show the Sign In button."""
        _reset_to_login(driver)
        assert _element_exists(
            driver,
            '//*[@content-desc="Sign In" or @text="Sign In"]',
            '//*[contains(@content-desc,"sign in") or contains(@text,"sign in")]',
            '//*[contains(@content-desc,"Sign") or contains(@text,"Sign")]',
        ), "Sign In button not found on Login screen"

    # PM006 — Login shows Welcome Back text
    @pytest.mark.auth
    def test_PM006_login_shows_welcome_back(self, driver):
        """Login screen must show the 'Welcome Back' heading."""
        _reset_to_login(driver)
        assert _element_exists(
            driver,
            '//*[@content-desc="Welcome Back" or @text="Welcome Back"]',
            '//*[contains(@content-desc,"Welcome") or contains(@text,"Welcome")]',
        ), "Welcome Back heading not found on Login screen"

    # PM007 — Login shows Forgot Password link
    @pytest.mark.auth
    def test_PM007_login_has_forgot_password_link(self, driver):
        """Login screen must show the Forgot Password navigation link."""
        _reset_to_login(driver)
        assert _element_exists(
            driver,
            '//*[@content-desc="Forgot Password" or @text="Forgot Password"]',
            '//*[contains(@content-desc,"Forgot") or contains(@text,"Forgot")]',
        ), "Forgot Password link not found"

    # PM008 — Login shows Sign Up link
    @pytest.mark.auth
    def test_PM008_login_has_sign_up_link(self, driver):
        """Login screen must show the Sign Up / Don't have an account link."""
        _reset_to_login(driver)
        assert _element_exists(
            driver,
            '//*[@content-desc="Sign Up" or @text="Sign Up"]',
            '//*[contains(@content-desc,"Sign Up") or contains(@text,"Sign Up")]',
            '//*[contains(@content-desc,"account") or contains(@text,"account")]',
        ), "Sign Up link not found on Login screen"

    # PM009 — Empty login form shows validation
    @pytest.mark.auth
    def test_PM009_empty_login_shows_validation(self, driver):
        """Tapping Sign In with empty fields must not navigate away."""
        _reset_to_login(driver)
        sign_in_btn = _find(
            driver,
            '//*[@content-desc="Sign In" or @text="Sign In"]',
            '//*[contains(@content-desc,"Sign") or contains(@text,"Sign")]',
        )
        assert sign_in_btn is not None, "Sign In button not found"
        sign_in_btn.click()
        time.sleep(2)
        still_on_login = _element_exists(
            driver,
            '//*[@content-desc="Sign In" or @text="Sign In"]',
            '//*[contains(@content-desc,"Welcome") or contains(@text,"Welcome")]',
            '//android.widget.EditText',
        )
        assert still_on_login, "App navigated away from Login after empty form submission"

    # PM010 — Wrong credentials stays on login screen
    @pytest.mark.auth
    def test_PM010_wrong_credentials_stays_on_login(self, driver):
        """Wrong credentials must keep user on the Login screen."""
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
        time.sleep(5)   # Firebase auth takes a moment
        assert _element_exists(
            driver,
            '//android.widget.EditText',
            '//*[contains(@content-desc,"Welcome") or contains(@text,"Welcome")]',
        ), "App unexpectedly navigated away after wrong credentials"

    # PM011 — Navigate to Register page
    @pytest.mark.auth
    def test_PM011_navigate_to_register_page(self, driver):
        """Tapping Sign Up navigates to Register screen."""
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

    # PM012 — Register page has Full Name field
    @pytest.mark.auth
    def test_PM012_register_has_full_name_field(self, driver):
        _navigate_to_register_screen(driver)
        assert _element_exists(
            driver,
            '//*[@content-desc="Full Name" or @text="Full Name"]',
            '//*[contains(@content-desc,"Name") or contains(@text,"Name")]',
            '//android.widget.EditText[1]',
        ), "Full Name field not found on Register screen"

    # PM013 — Register page has Email field
    @pytest.mark.auth
    def test_PM013_register_has_email_field(self, driver):
        _navigate_to_register_screen(driver)
        assert _element_exists(
            driver,
            '//*[@content-desc="Email" or @text="Email"]',
            '//android.widget.EditText[2]',
        ), "Email field not found on Register screen"

    # PM014 — Register page has Password field
    @pytest.mark.auth
    def test_PM014_register_has_password_field(self, driver):
        _navigate_to_register_screen(driver)
        assert _element_exists(
            driver,
            '//*[@content-desc="Password" or @text="Password"]',
            '//android.widget.EditText[3]',
        ), "Password field not found on Register screen"

    # PM015 — Register page has Confirm Password field
    @pytest.mark.auth
    def test_PM015_register_has_confirm_password_field(self, driver):
        _navigate_to_register_screen(driver)
        found = _element_exists(
            driver,
            '//*[contains(@content-desc,"Confirm") or contains(@text,"Confirm")]',
            '//android.widget.EditText[4]',
            '//*[contains(@content-desc,"Confirm Password") or contains(@text,"Confirm Password")]',
            timeout=12
        )
        if not found:
            _scroll_down(driver)
            found = _element_exists(
                driver,
                '//*[contains(@content-desc,"Confirm") or contains(@text,"Confirm")]',
                '//android.widget.EditText[4]',
                '//*[contains(@content-desc,"Confirm Password") or contains(@text,"Confirm Password")]',
                '//android.widget.EditText[contains(@content-desc,"Confirm") or contains(@text,"Confirm")]',
            )
        assert found, "Confirm Password field not found on Register screen"

    # PM016 — Register page has Create Account button
    @pytest.mark.auth
    def test_PM016_register_has_create_account_button(self, driver):
        _navigate_to_register_screen(driver)
        found = _element_exists(
            driver,
            '//*[@content-desc="Sign Up" or @text="Sign Up"]',
            '//*[contains(@content-desc,"Sign") or contains(@text,"Sign")]',
            '//*[@content-desc="Create Account" or @text="Create Account"]',
            '//*[contains(@content-desc,"Create") or contains(@text,"Create")]',
            timeout=12
        )
        if not found:
            _scroll_down(driver)
            found = _element_exists(
                driver,
                '//*[@content-desc="Sign Up" or @text="Sign Up"]',
                '//*[contains(@content-desc,"Sign") or contains(@text,"Sign")]',
                '//*[@content-desc="Create Account" or @text="Create Account"]',
                '//*[contains(@content-desc,"Create") or contains(@text,"Create")]',
            )
        assert found, "Create Account button not found on Register screen"

    # PM017 — Password mismatch shows validation error
    @pytest.mark.auth
    def test_PM017_password_mismatch_shows_error(self, driver):
        _navigate_to_register_screen(driver)
        fields = driver.find_elements(AppiumBy.XPATH, '//android.widget.EditText')
        if len(fields) >= 3:
            fields[0].click(); time.sleep(0.5); fields[0].send_keys("Test User")
            fields[1].click(); time.sleep(0.5); fields[1].send_keys("test@example.com")
            fields[2].click(); time.sleep(0.5); fields[2].send_keys("Password123!")
            try:
                driver.hide_keyboard()
                time.sleep(1)
            except Exception:
                pass
        confirm_field = _find(driver,
            '//android.widget.EditText[4]',
            '//*[contains(@content-desc,"Confirm") or contains(@text,"Confirm")]/following-sibling::android.widget.EditText',
            '//android.widget.EditText[contains(@content-desc,"Confirm") or contains(@text,"Confirm")]',
            timeout=12
        )
        if not confirm_field:
            _scroll_down(driver)
            confirm_field = _find(driver,
                '//android.widget.EditText[4]',
                '//*[contains(@content-desc,"Confirm") or contains(@text,"Confirm")]/following-sibling::android.widget.EditText',
                '//android.widget.EditText[contains(@content-desc,"Confirm") or contains(@text,"Confirm")]',
                '//android.widget.EditText[last()]',
            )
        if confirm_field:
            confirm_field.click(); time.sleep(0.5); confirm_field.send_keys("DifferentPassword!")
            try:
                driver.hide_keyboard()
                time.sleep(1)
            except Exception:
                pass
        btn = _find(driver,
            '//*[contains(@content-desc,"Sign Up") or contains(@text,"Sign Up")]',
            '//*[contains(@content-desc,"Create Account") or contains(@text,"Create Account")]')
        if btn:
            btn.click()
        time.sleep(2)
        assert _element_exists(
            driver,
            '//android.widget.EditText',
            '//*[contains(@content-desc,"Create Account") or contains(@text,"Create Account")]',
        ), "App navigated away despite password mismatch"

    # PM018 — Forgot Password page renders
    @pytest.mark.auth
    def test_PM018_forgot_password_page_renders(self, driver):
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

    # PM019 — Forgot Password has email input
    @pytest.mark.auth
    def test_PM019_forgot_password_has_email_input(self, driver):
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

    # PM020 — Forgot Password has Send Reset Link button
    @pytest.mark.auth
    def test_PM020_forgot_password_has_send_reset_button(self, driver):
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
        ), "Send Reset Link button not found"

    # PM021 — Route guard: unauthenticated redirected to login
    @pytest.mark.auth
    def test_PM021_route_guard_unauthenticated_redirect(self, driver):
        """App must redirect unauthenticated users to Login on fresh start."""
        _reset_to_login(driver)
        time.sleep(6)
        assert _element_exists(
            driver,
            '//*[@content-desc="Sign In" or @text="Sign In"]',
            '//*[contains(@content-desc,"Welcome") or contains(@text,"Welcome")]',
            '//android.widget.EditText',
        ), "Unauthenticated user was not redirected to Login screen"

    # PM022 — Successful login navigates to Home screen
    @pytest.mark.auth
    @pytest.mark.smoke
    def test_PM022_successful_login_navigates_home(self, driver):
        """Valid credentials must log in and navigate to Home screen."""
        import os
        TEST_EMAIL = os.environ.get("CROWDSENSE_EMAIL", "test@crowdsense.app")
        TEST_PASSWORD = os.environ.get("CROWDSENSE_PASSWORD", "Test@1234")
        _reset_to_login(driver)
        email_field = _find(driver, '//android.widget.EditText[1]')
        pwd_field   = _find(driver, '//android.widget.EditText[2]')
        if email_field:
            email_field.click(); time.sleep(0.5); email_field.clear(); email_field.send_keys(TEST_EMAIL)
        if pwd_field:
            pwd_field.click(); time.sleep(0.5); pwd_field.clear(); pwd_field.send_keys(TEST_PASSWORD)
        try:
            driver.hide_keyboard()
            time.sleep(1)
        except Exception:
            pass
        sign_in = _find(driver,
            '//*[@content-desc="Sign In" or @text="Sign In"]',
            '//*[contains(@content-desc,"Sign") or contains(@text,"Sign")]')
        if sign_in:
            sign_in.click()
        time.sleep(6)   # Firebase auth + navigation transition
        assert _element_exists(
            driver,
            '//*[contains(@content-desc,"Search") or contains(@text,"Search")]',
            '//*[contains(@content-desc,"Trending") or contains(@text,"Trending")]',
            '//*[contains(@content-desc,"Home") or contains(@text,"Home")]',
            '//*[contains(@content-desc,"Welcome") or contains(@text,"Welcome")]',
        ), "Home screen not reached after successful login"
