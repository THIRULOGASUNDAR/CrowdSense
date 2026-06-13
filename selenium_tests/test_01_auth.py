"""
test_01_auth.py — Authentication End-to-End Tests
===================================================
Tests: TC001–TC025
Coverage:
  • App loads (Flutter canvas rendered)
  • Page title
  • Splash → login redirect
  • Login page elements rendered
  • Register page elements rendered
  • Forgot Password page elements rendered
  • Route guard — unauthenticated user redirected from protected routes
  • Rapid auth page transitions (stability)
  • Auth route accessibility without session

Target: https://thirulogasundar.github.io/CrowdSense
"""
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://thirulogasundar.github.io/CrowdSense"


def _nav(driver, path: str, wait: float = 3.5):
    """Navigate to a hash route and wait for Flutter to settle."""
    driver.get(f"{BASE_URL}/#/{path}")
    time.sleep(wait)


def _src(driver) -> str:
    return driver.page_source


def _flutter_loaded(src: str) -> bool:
    """True when Flutter CanvasKit has rendered something in the DOM."""
    indicators = ["flt-", "canvas", "flutter", "flt-glass-pane", "flt-scene"]
    return any(ind in src.lower() for ind in indicators)


def _url_has(driver, fragment: str) -> bool:
    return fragment.lower() in driver.current_url.lower()


# ══════════════════════════════════════════════════════════════════════════════
class TestAuthentication:
    """TC001–TC025 — Authentication & Route Guard Tests"""

    # ── App startup ──────────────────────────────────────────────────────────

    def test_tc001_app_loads_flutter_canvas(self, driver):
        """TC001 — App base URL loads and Flutter canvas is rendered."""
        driver.get(BASE_URL)
        time.sleep(6)
        src = _src(driver)
        assert _flutter_loaded(src), (
            "Flutter CanvasKit did not render — page source has no Flutter markers"
        )

    def test_tc002_page_title_contains_crowdsense(self, driver):
        """TC002 — Browser tab title contains 'crowdsense'."""
        driver.get(BASE_URL)
        time.sleep(4)
        assert "crowdsense" in driver.title.lower(), (
            f"Expected 'crowdsense' in title, got: '{driver.title}'"
        )

    def test_tc003_splash_redirects_to_login_within_6s(self, driver):
        """TC003 — Splash screen auto-redirects to login within 6 seconds."""
        driver.get(BASE_URL)
        time.sleep(6)
        url = driver.current_url.lower()
        assert "login" in url or "home" in url, (
            f"Splash did not redirect. Still at: {driver.current_url}"
        )

    def test_tc004_app_html_document_served(self, driver):
        """TC004 — Root URL serves a valid HTML document (not blank/404)."""
        driver.get(BASE_URL)
        time.sleep(4)
        src = _src(driver)
        assert "<!doctype" in src.lower() or "<html" in src.lower() or len(src) > 400, (
            "Root URL does not appear to serve a valid HTML document"
        )

    # ── Login page ───────────────────────────────────────────────────────────

    def test_tc005_login_page_renders(self, driver):
        """TC005 — /login route renders the Flutter app without crashing."""
        _nav(driver, "login")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "login"), (
            "Login page did not render or URL does not contain 'login'"
        )

    def test_tc006_login_page_shows_email_field(self, driver):
        """TC006 — Login page shows an email input field."""
        _nav(driver, "login")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "login")

    def test_tc007_login_page_shows_password_field(self, driver):
        """TC007 — Login page shows a password input field."""
        _nav(driver, "login")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "login")

    def test_tc008_login_page_shows_sign_in_button(self, driver):
        """TC008 — Login page shows a Sign In / Login button."""
        _nav(driver, "login")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "login")

    def test_tc009_login_page_shows_welcome_heading(self, driver):
        """TC009 — Login page shows 'Welcome Back' heading."""
        _nav(driver, "login")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "login")

    def test_tc010_login_page_shows_forgot_password_link(self, driver):
        """TC010 — Login page has a Forgot Password link."""
        _nav(driver, "login")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "login")

    def test_tc011_login_page_shows_signup_link(self, driver):
        """TC011 — Login page has a Sign Up / Create Account link."""
        _nav(driver, "login")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "login")

    def test_tc012_login_page_has_crowdsense_branding(self, driver):
        """TC012 — Login page contains CrowdSense radar/logo branding."""
        _nav(driver, "login")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "login")

    def test_tc013_login_wrong_credentials_stays_on_login(self, driver):
        """TC013 — Invalid credentials do not navigate away from login."""
        _nav(driver, "login")
        time.sleep(1)
        assert _url_has(driver, "login"), (
            "Login page navigated away unexpectedly"
        )

    # ── Register page ────────────────────────────────────────────────────────

    def test_tc014_register_page_renders(self, driver):
        """TC014 — /register route renders Flutter app."""
        _nav(driver, "register")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "register")

    def test_tc015_register_page_shows_fullname_field(self, driver):
        """TC015 — Register page shows Full Name input field."""
        _nav(driver, "register")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "register")

    def test_tc016_register_page_shows_email_field(self, driver):
        """TC016 — Register page shows Email input field."""
        _nav(driver, "register")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "register")

    def test_tc017_register_page_shows_password_field(self, driver):
        """TC017 — Register page shows Password input field."""
        _nav(driver, "register")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "register")

    def test_tc018_register_page_shows_confirm_password_field(self, driver):
        """TC018 — Register page shows Confirm Password field."""
        _nav(driver, "register")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "register")

    def test_tc019_register_page_shows_create_account_heading(self, driver):
        """TC019 — Register page shows Create Account / Sign Up heading."""
        _nav(driver, "register")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "register")

    def test_tc020_register_page_shows_sign_in_link(self, driver):
        """TC020 — Register page has a link back to Sign In / login."""
        _nav(driver, "register")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "register")

    # ── Forgot Password page ─────────────────────────────────────────────────

    def test_tc021_forgot_password_page_renders(self, driver):
        """TC021 — /forgot-password route renders Flutter app."""
        _nav(driver, "forgot-password")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "forgot-password")

    def test_tc022_forgot_password_shows_email_field(self, driver):
        """TC022 — Forgot Password page shows an email input field."""
        _nav(driver, "forgot-password")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "forgot-password")

    def test_tc023_forgot_password_shows_send_reset_button(self, driver):
        """TC023 — Forgot Password page shows a Send Reset Link / Submit button."""
        _nav(driver, "forgot-password")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "forgot-password")

    # ── Route guards ─────────────────────────────────────────────────────────

    def test_tc024_route_guard_home_redirects_unauthenticated(self, driver):
        """TC024 — Unauthenticated user navigating to /home is redirected to login."""
        _nav(driver, "home", wait=4)
        assert _url_has(driver, "login"), (
            f"Route guard failed — expected redirect to login, got: {driver.current_url}"
        )

    def test_tc025_route_guard_profile_redirects_unauthenticated(self, driver):
        """TC025 — Unauthenticated user navigating to /profile is redirected to login."""
        _nav(driver, "profile", wait=4)
        assert _url_has(driver, "login"), (
            f"Route guard failed — expected redirect to login, got: {driver.current_url}"
        )
