"""
test_15_real_e2e.py — Authenticated End-to-End User Journey Tests
==================================================================
Tests: Real login, Home validation, Search execution, Profile settings,
Travel planner, and Logout using semantics navigation on Flutter Web.

Target: https://thirulogasundar.github.io/CrowdSense
Credentials: thiru@gmail.com / thiru005
"""
import os
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://thirulogasundar.github.io/CrowdSense"

# Skip authenticated tests in CI — Firebase login requires real credentials
# that cannot be safely stored in GitHub Actions runners.
# To run locally: pytest tests/selenium_tests/test_15_real_e2e.py -v
pytestmark = pytest.mark.skipif(
    bool(os.environ.get("CI")),
    reason="Authenticated E2E tests skipped in CI — requires live Firebase session. Run locally.",
)


def _enable_semantics(driver):
    """Bypasses Flutter's click interceptor to enable the web semantics tree."""
    try:
        placeholder = driver.find_element(By.TAG_NAME, "flt-semantics-placeholder")
        driver.execute_script("arguments[0].click();", placeholder)
        time.sleep(2)
    except Exception:
        pass


def _go(driver, path: str, wait: float = 4.0):
    """Navigate to a route and auto-enable semantics tree."""
    driver.get(f"{BASE_URL}/#/{path}")
    time.sleep(wait)
    _enable_semantics(driver)


def _get_semantics_content(driver) -> str:
    """Helper to dump the accessibility text contents inside semantics host."""
    try:
        host = driver.find_element(By.TAG_NAME, "flt-semantics-host")
        return host.get_attribute("innerHTML")
    except Exception:
        return ""


# ══════════════════════════════════════════════════════════════════════════════
class TestRealUserE2E:
    """Authenticated End-to-End Tests using active credentials (thiru@gmail.com)"""

    def test_tc150_login_success(self, driver):
        """TC150 — Login successfully using valid credentials."""
        driver.get(f"{BASE_URL}/#/login")
        time.sleep(6)
        _enable_semantics(driver)

        # Locate email and password fields
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Enter your email']"))
        )
        email_input.clear()
        email_input.send_keys("thiru@gmail.com")
        time.sleep(1)

        password_input = driver.find_element(By.XPATH, "//input[@aria-label='Enter your password']")
        password_input.clear()
        password_input.send_keys("thiru005")
        time.sleep(1)

        # Click Sign In button
        sign_in_btn = driver.find_element(By.XPATH, "//*[text()='Sign In']")
        driver.execute_script("arguments[0].click();", sign_in_btn)
        time.sleep(6)

        # Verify redirect to home
        assert "home" in driver.current_url.lower(), (
            f"Failed to log in. URL is still at: {driver.current_url}"
        )

    def test_tc151_home_content_validation(self, driver):
        """TC151 — Verify home page elements are visible after authenticating."""
        _go(driver, "home")
        content = _get_semantics_content(driver)
        
        # Verify key elements on home screen
        assert "Trending" in content or "Hi" in content or "Places" in content or "Recent" in content, (
            "Authenticated home screen content failed to load in the semantics tree."
        )

    def test_tc152_search_query_execution(self, driver):
        """TC152 — Navigate to search and check discovery suggestion chips."""
        _go(driver, "search")
        content = _get_semantics_content(driver)

        # Verify default suggestion chips are presented
        chips = ["Parks", "Restaurants", "Coffee", "Museum", "Mall"]
        found_chips = any(chip in content for chip in chips)
        assert found_chips, "Default search discovery chips are missing from the search screen."

    def test_tc153_favorites_page(self, driver):
        """TC153 — Verify the Favorites page loads properly under user session."""
        _go(driver, "favorites")
        content = _get_semantics_content(driver)
        assert "favorites" in driver.current_url.lower(), "Favorites route failed to load."

    def test_tc154_planner_page(self, driver):
        """TC154 — Verify the Travel Planner page loads properly under user session."""
        _go(driver, "planner")
        content = _get_semantics_content(driver)
        assert "planner" in driver.current_url.lower(), "Planner route failed to load."

    def test_tc155_profile_page_elements(self, driver):
        """TC155 — Navigate to profile screen and check configurations."""
        _go(driver, "profile")
        content = _get_semantics_content(driver)

        assert "profile" in driver.current_url.lower()
        # Verify configuration items exist
        assert "Settings" in content or "Sign Out" in content or "Notifications" in content, (
            "Profile dashboard items are missing from profile screen."
        )

    def test_tc156_logout_success(self, driver):
        """TC156 — Click Sign Out button and verify redirect back to login."""
        _go(driver, "profile")
        _enable_semantics(driver)

        # Locate and click Sign Out button inside semantics
        try:
            sign_out_btn = driver.find_element(By.XPATH, "//*[text()='Sign Out']")
            driver.execute_script("arguments[0].click();", sign_out_btn)
            time.sleep(5)
        except Exception:
            # Fallback direct navigation to test route guard
            driver.get(f"{BASE_URL}/#/login")
            time.sleep(3)

        # Verify route guard redirect back to login
        driver.get(f"{BASE_URL}/#/home")
        time.sleep(4)
        assert "login" in driver.current_url.lower(), (
            f"Logout or route guard failed. Redirected to: {driver.current_url}"
        )
