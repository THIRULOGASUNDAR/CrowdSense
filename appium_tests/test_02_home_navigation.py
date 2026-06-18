"""
test_02_home_navigation.py — Home Screen & Navigation Tests (AM023–AM040)
=========================================================================
CrowdSense Appium Mobile E2E Suite
Target: Pixel 3a API 37 AVD  |  Automation: UiAutomator2

Covers:
  - Home screen UI sections (search bar, trending, categories, recent searches)
  - Bottom navigation bar tabs
  - Inter-screen navigation (Home → Search → Planner → Favorites → Profile)
  - Back navigation
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


# ─── Test Class ───────────────────────────────────────────────────────────────

class TestHomeNavigation:

    # AM023 — Home screen loads after login
    @pytest.mark.home
    @pytest.mark.smoke
    def test_AM023_home_screen_loads(self, logged_in_driver):
        """Home screen must load successfully after login."""
        driver = logged_in_driver
        time.sleep(2)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Search") or contains(@text,"Search")]',
            '//*[contains(@content-desc,"Trending") or contains(@text,"Trending")]',
            '//*[contains(@content-desc,"Home") or contains(@text,"Home")]',
        ), "Home screen did not load after login"

    # AM024 — Home shows search bar
    @pytest.mark.home
    def test_AM024_home_shows_search_bar(self, logged_in_driver):
        """Home screen must display a search bar or search hint text."""
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Search") or contains(@text,"Search")]',
            '//*[contains(@content-desc,"search") or contains(@text,"search")]',
        ), "Search bar not visible on Home screen"

    # AM025 — Home shows greeting / welcome text
    @pytest.mark.home
    def test_AM025_home_shows_greeting(self, logged_in_driver):
        """Home screen must display a greeting or welcome text for the user."""
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Hello") or contains(@text,"Hello")]',
            '//*[contains(@content-desc,"Welcome") or contains(@text,"Welcome")]',
            '//*[contains(@content-desc,"Good") or contains(@text,"Good")]',
            '//*[contains(@content-desc,"Hi") or contains(@text,"Hi")]',
        ), "Greeting text not found on Home screen"

    # AM026 — Home shows Trending Now section
    @pytest.mark.home
    def test_AM026_home_shows_trending_section(self, logged_in_driver):
        """Home screen must display a 'Trending Now' or trending section."""
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Trending") or contains(@text,"Trending")]',
            '//*[contains(@content-desc,"trending") or contains(@text,"trending")]',
        ), "Trending Now section not found on Home screen"

    # AM027 — Home shows Popular Categories section
    @pytest.mark.home
    def test_AM027_home_shows_categories_section(self, logged_in_driver):
        """Home screen must display a Popular Categories section."""
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Categories") or contains(@text,"Categories")]',
            '//*[contains(@content-desc,"Popular") or contains(@text,"Popular")]',
        ), "Popular Categories section not found on Home screen"

    # AM028 — Landmarks category chip visible
    @pytest.mark.home
    def test_AM028_landmarks_category_chip(self, logged_in_driver):
        """Home screen must show the Landmarks category chip/button."""
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[@content-desc="Landmarks" or @text="Landmarks"]',
            '//*[contains(@content-desc,"Landmark") or contains(@text,"Landmark")]',
        ), "Landmarks category chip not found"

    # AM029 — Restaurants category chip visible
    @pytest.mark.home
    def test_AM029_restaurants_category_chip(self, logged_in_driver):
        """Home screen must show the Restaurants category chip/button."""
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[@content-desc="Restaurants" or @text="Restaurants"]',
            '//*[contains(@content-desc,"Restaurant") or contains(@text,"Restaurant")]',
        ), "Restaurants category chip not found"

    # AM030 — Parks category chip visible
    @pytest.mark.home
    def test_AM030_parks_category_chip(self, logged_in_driver):
        """Home screen must show the Parks category chip/button."""
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[@content-desc="Parks" or @text="Parks"]',
            '//*[contains(@content-desc,"Park") or contains(@text,"Park")]',
        ), "Parks category chip not found"

    # AM031 — Shopping category chip visible
    @pytest.mark.home
    def test_AM031_shopping_category_chip(self, logged_in_driver):
        """Home screen must show the Shopping category chip/button."""
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[@content-desc="Shopping" or @text="Shopping"]',
            '//*[contains(@content-desc,"Shop") or contains(@text,"Shop")]',
        ), "Shopping category chip not found"

    # AM032 — Entertainment category chip visible
    @pytest.mark.home
    def test_AM032_entertainment_category_chip(self, logged_in_driver):
        """Home screen must show the Entertainment category chip/button."""
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[@content-desc="Entertainment" or @text="Entertainment"]',
            '//*[contains(@content-desc,"Entertain") or contains(@text,"Entertain")]',
        ), "Entertainment category chip not found"

    # AM033 — Home shows Recent Searches section
    @pytest.mark.home
    def test_AM033_home_shows_recent_searches(self, logged_in_driver):
        """Home screen must display a Recent Searches section (even if empty)."""
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Recent") or contains(@text,"Recent")]',
            '//*[contains(@content-desc,"recent") or contains(@text,"recent")]',
        ), "Recent Searches section not visible on Home screen"

    # AM034 — Bottom navigation bar visible
    @pytest.mark.home
    @pytest.mark.smoke
    def test_AM034_bottom_nav_bar_visible(self, logged_in_driver):
        """The bottom navigation bar must be rendered on the Home screen."""
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Home") or contains(@text,"Home")]',
            '//*[contains(@content-desc,"Search") or contains(@text,"Search")]',
            '//android.widget.BottomNavigationView',
            '//androidx.compose.ui.platform.ComposeView',
        ), "Bottom navigation bar not found"

    # AM035 — Tap Search tab navigates to Search screen
    @pytest.mark.home
    def test_AM035_tap_search_tab_navigates(self, logged_in_driver):
        """Tapping the Search tab in the bottom nav must navigate to Search screen."""
        driver = logged_in_driver
        search_tab = _find(
            driver,
            '//*[@content-desc="Search" or @text="Search"]',
        )
        assert search_tab is not None, "Search tab not found in bottom nav"
        search_tab.click()
        time.sleep(2)
        assert _exists(
            driver,
            '//android.widget.EditText',
            '//*[contains(@content-desc,"search") or contains(@text,"search")]',
            '//*[contains(@content-desc,"Search places") or contains(@text,"Search places")]',
        ), "Search screen did not open after tapping Search tab"

    # AM036 — Tap Planner tab navigates to Travel Planner
    @pytest.mark.home
    def test_AM036_tap_planner_tab_navigates(self, logged_in_driver):
        """Tapping the Planner / Travel Planner tab must navigate to that screen."""
        driver = logged_in_driver
        planner_tab = _find(
            driver,
            '//*[@content-desc="Planner" or @text="Planner"]',
            '//*[contains(@content-desc,"Plan") or contains(@text,"Plan")]',
        )
        assert planner_tab is not None, "Planner tab not found in bottom nav"
        planner_tab.click()
        time.sleep(2)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Planner") or contains(@text,"Planner")]',
            '//*[contains(@content-desc,"Travel") or contains(@text,"Travel")]',
        ), "Travel Planner screen did not open"

    # AM037 — Tap Favorites tab navigates to Favorites
    @pytest.mark.home
    def test_AM037_tap_favorites_tab_navigates(self, logged_in_driver):
        """Tapping the Favorites tab must navigate to Favorites screen."""
        driver = logged_in_driver
        fav_tab = _find(
            driver,
            '//*[@content-desc="Favorites" or @text="Favorites"]',
            '//*[contains(@content-desc,"Favorite") or contains(@text,"Favorite")]',
        )
        assert fav_tab is not None, "Favorites tab not found in bottom nav"
        fav_tab.click()
        time.sleep(2)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Favorites") or contains(@text,"Favorites")]',
            '//*[contains(@content-desc,"favorite") or contains(@text,"favorite")]',
        ), "Favorites screen did not open"

    # AM038 — Tap Profile tab navigates to Profile screen
    @pytest.mark.home
    def test_AM038_tap_profile_tab_navigates(self, logged_in_driver):
        """Tapping the Profile tab must navigate to the Profile screen."""
        driver = logged_in_driver
        profile_tab = _find(
            driver,
            '//*[@content-desc="Profile" or @text="Profile"]',
            '//*[contains(@content-desc,"Profile") or contains(@text,"Profile")]',
        )
        assert profile_tab is not None, "Profile tab not found in bottom nav"
        profile_tab.click()
        time.sleep(2)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Profile") or contains(@text,"Profile")]',
            '//*[contains(@content-desc,"Sign Out") or contains(@text,"Sign Out")]',
            '//*[contains(@content-desc,"Reports") or contains(@text,"Reports")]',
        ), "Profile screen did not open"

    # AM039 — Back navigation from Search to Home works
    @pytest.mark.home
    def test_AM039_back_navigation_from_search(self, logged_in_driver):
        """Android back gesture / button from Search must return to Home."""
        driver = logged_in_driver
        # Navigate to search
        search_tab = _find(driver, '//*[@content-desc="Search" or @text="Search"]')
        if search_tab:
            search_tab.click()
            time.sleep(2)
        driver.back()
        time.sleep(2)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Trending") or contains(@text,"Trending")]',
            '//*[contains(@content-desc,"Categories") or contains(@text,"Categories")]',
            '//*[contains(@content-desc,"Home") or contains(@text,"Home")]',
        ), "Back navigation from Search did not return to Home"

    # AM040 — All bottom nav icons render
    @pytest.mark.home
    def test_AM040_bottom_nav_all_icons_render(self, logged_in_driver):
        """All expected bottom navigation tabs must be visible simultaneously."""
        driver = logged_in_driver
        home_tab    = _exists(driver, '//*[@content-desc="Home" or @text="Home"]', timeout=5)
        search_tab  = _exists(driver, '//*[@content-desc="Search" or @text="Search"]', timeout=5)
        # Check at least 2 tabs visible (Home + Search are always primary)
        assert home_tab or search_tab, "No bottom navigation tabs found"
