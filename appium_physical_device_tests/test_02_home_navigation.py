"""
test_02_home_navigation.py — Home Screen & Navigation Tests (PM023–PM040)
=========================================================================
CrowdSense Appium Physical Device E2E Suite
Target: Real Android device via USB  |  Automation: UiAutomator2

Covers:
  - Home screen UI sections (search bar, trending, categories, recent searches)
  - Bottom navigation bar tabs
  - Inter-screen navigation (Home → Search → Planner → Favorites → Profile)
  - Back navigation behaviour on physical device
"""
import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# ─── Helper utilities ─────────────────────────────────────────────────────────

def _find(driver, *xpaths, timeout=12):
    if not xpaths:
        return None
    combined_xpath = " | ".join(xpaths)
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((AppiumBy.XPATH, combined_xpath))
        )
    except (NoSuchElementException, TimeoutException):
        return None


def _exists(driver, *xpaths, timeout=10):
    return _find(driver, *xpaths, timeout=timeout) is not None


def _ensure_home(driver):
    # Check if already home
    if _exists(driver, '//*[contains(@content-desc,"Trending") or contains(@text,"Trending")]', timeout=2):
        return True
    # Try tapping Home tab
    try:
        home_tab = driver.find_element(AppiumBy.XPATH, '//*[contains(@content-desc,"Home") or contains(@text,"Home")]')
        if home_tab:
            home_tab.click()
            time.sleep(2)
            if _exists(driver, '//*[contains(@content-desc,"Trending") or contains(@text,"Trending")]', timeout=3):
                return True
    except Exception:
        pass
    # Fallback to back button
    for _ in range(3):
        if _exists(driver, '//*[contains(@content-desc,"Trending") or contains(@text,"Trending")]', timeout=2):
            return True
        try:
            driver.back()
            time.sleep(1.5)
        except Exception:
            break
    # Last resort: restart app
    try:
        driver.terminate_app("com.example.crowdsense")
        time.sleep(1.5)
        driver.activate_app("com.example.crowdsense")
        time.sleep(6)
        if _exists(driver, '//*[contains(@content-desc,"Trending") or contains(@text,"Trending")]', timeout=5):
            return True
    except Exception:
        pass
    return False


def _scroll_right(driver):
    try:
        scroll_views = driver.find_elements(AppiumBy.CLASS_NAME, 'android.widget.HorizontalScrollView')
        if len(scroll_views) >= 2:
            rect = scroll_views[1].rect
            y = int(rect['y'] + rect['height'] / 2)
            start_x = int(rect['x'] + rect['width'] * 0.85)
            end_x = int(rect['x'] + rect['width'] * 0.15)
            driver.swipe(start_x, y, end_x, y, 600)
        else:
            # Fallback to coordinate-based swipe at 70% of screen height
            size = driver.get_window_size()
            driver.swipe(
                int(size['width'] * 0.85),
                int(size['height'] * 0.70),
                int(size['width'] * 0.15),
                int(size['height'] * 0.70),
                600
            )
        time.sleep(1.5)
    except Exception:
        pass



# ─── Test Class ───────────────────────────────────────────────────────────────

class TestHomeNavigation:

    # PM023 — Home screen loads after login
    @pytest.mark.home
    @pytest.mark.smoke
    def test_PM023_home_screen_loads(self, logged_in_driver):
        """Home screen must load successfully after login."""
        driver = logged_in_driver
        time.sleep(3)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Search") or contains(@text,"Search")]',
            '//*[contains(@content-desc,"Trending") or contains(@text,"Trending")]',
            '//*[contains(@content-desc,"Home") or contains(@text,"Home")]',
        ), "Home screen did not load after login"

    # PM024 — Home shows search bar
    @pytest.mark.home
    def test_PM024_home_shows_search_bar(self, logged_in_driver):
        """Home screen must display a search bar or search hint text."""
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Search") or contains(@text,"Search")]',
            '//*[contains(@content-desc,"search") or contains(@text,"search")]',
        ), "Search bar not visible on Home screen"

    # PM025 — Home shows greeting
    @pytest.mark.home
    def test_PM025_home_shows_greeting(self, logged_in_driver):
        """Home screen must display a greeting or welcome text."""
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Hello") or contains(@text,"Hello")]',
            '//*[contains(@content-desc,"Welcome") or contains(@text,"Welcome")]',
            '//*[contains(@content-desc,"Good") or contains(@text,"Good")]',
            '//*[contains(@content-desc,"Hi") or contains(@text,"Hi")]',
        ), "Greeting text not found on Home screen"

    # PM026 — Home shows Trending Now section
    @pytest.mark.home
    def test_PM026_home_shows_trending_section(self, logged_in_driver):
        """Home screen must display a 'Trending Now' section."""
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Trending") or contains(@text,"Trending")]',
            '//*[contains(@content-desc,"trending") or contains(@text,"trending")]',
        ), "Trending Now section not found on Home screen"

    # PM027 — Home shows Popular Categories section
    @pytest.mark.skip(reason="Popular Categories removed")
    @pytest.mark.home
    def test_PM027_home_shows_categories_section(self, logged_in_driver):
        """Home screen must display a Popular Categories section."""
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Categories") or contains(@text,"Categories")]',
            '//*[contains(@content-desc,"Popular") or contains(@text,"Popular")]',
        ), "Popular Categories section not found on Home screen"

    # PM028 — Landmarks category chip visible
    @pytest.mark.skip(reason="Popular Categories removed")
    @pytest.mark.home
    def test_PM028_landmarks_category_chip(self, logged_in_driver):
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[@content-desc="Landmarks" or @text="Landmarks"]',
            '//*[contains(@content-desc,"Landmark") or contains(@text,"Landmark")]',
        ), "Landmarks category chip not found"

    # PM029 — Restaurants category chip visible
    @pytest.mark.skip(reason="Popular Categories removed")
    @pytest.mark.home
    def test_PM029_restaurants_category_chip(self, logged_in_driver):
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[@content-desc="Restaurants" or @text="Restaurants"]',
            '//*[contains(@content-desc,"Restaurant") or contains(@text,"Restaurant")]',
        ), "Restaurants category chip not found"

    # PM030 — Parks category chip visible
    @pytest.mark.skip(reason="Popular Categories removed")
    @pytest.mark.home
    def test_PM030_parks_category_chip(self, logged_in_driver):
        driver = logged_in_driver
        assert _exists(
            driver,
            '//*[@content-desc="Parks" or @text="Parks"]',
            '//*[contains(@content-desc,"Park") or contains(@text,"Park")]',
        ), "Parks category chip not found"

    # PM031 — Shopping category chip visible
    @pytest.mark.skip(reason="Popular Categories removed")
    @pytest.mark.home
    def test_PM031_shopping_category_chip(self, logged_in_driver):
        driver = logged_in_driver
        _ensure_home(driver)
        _scroll_right(driver)
        assert _exists(
            driver,
            '//*[@content-desc="Shopping" or @text="Shopping"]',
            '//*[contains(@content-desc,"Shop") or contains(@text,"Shop")]',
        ), "Shopping category chip not found"

    # PM032 — Entertainment category chip visible
    @pytest.mark.skip(reason="Popular Categories removed")
    @pytest.mark.home
    def test_PM032_entertainment_category_chip(self, logged_in_driver):
        driver = logged_in_driver
        _ensure_home(driver)
        _scroll_right(driver)
        assert _exists(
            driver,
            '//*[@content-desc="Entertainment" or @text="Entertainment"]',
            '//*[contains(@content-desc,"Entertain") or contains(@text,"Entertain")]',
        ), "Entertainment category chip not found"

    # PM033 — Home shows Recent Searches section
    @pytest.mark.home
    def test_PM033_home_shows_recent_searches(self, logged_in_driver):
        driver = logged_in_driver
        _ensure_home(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Recent") or contains(@text,"Recent")]',
            '//*[contains(@content-desc,"recent") or contains(@text,"recent")]',
        ), "Recent Searches section not visible on Home screen"

    # PM034 — Bottom navigation bar visible
    @pytest.mark.home
    @pytest.mark.smoke
    def test_PM034_bottom_nav_bar_visible(self, logged_in_driver):
        """The bottom navigation bar must be rendered on Home screen."""
        driver = logged_in_driver
        _ensure_home(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Home") or contains(@text,"Home")]',
            '//*[contains(@content-desc,"Search") or contains(@text,"Search")]',
            '//android.widget.BottomNavigationView',
            '//androidx.compose.ui.platform.ComposeView',
        ), "Bottom navigation bar not found"

    # PM035 — Tap Search tab navigates to Search screen
    @pytest.mark.home
    def test_PM035_tap_search_tab_navigates(self, logged_in_driver):
        driver = logged_in_driver
        _ensure_home(driver)
        search_tab = _find(driver,
            '//*[@content-desc="Search" or @text="Search"]',
            '//*[contains(@content-desc,"Search") or contains(@text,"Search")]',
        )
        assert search_tab is not None, "Search tab not found in bottom nav"
        search_tab.click()
        time.sleep(3)
        assert _exists(
            driver,
            '//android.widget.EditText',
            '//*[contains(@content-desc,"search") or contains(@text,"search")]',
            '//*[contains(@content-desc,"Search places") or contains(@text,"Search places")]',
        ), "Search screen did not open after tapping Search tab"

    # PM036 — Tap Planner tab navigates to Travel Planner
    @pytest.mark.home
    def test_PM036_tap_planner_tab_navigates(self, logged_in_driver):
        driver = logged_in_driver
        _ensure_home(driver)
        planner_tab = _find(
            driver,
            '//*[@content-desc="Planner" or @text="Planner"]',
            '//*[contains(@content-desc,"Plan") or contains(@text,"Plan")]',
        )
        assert planner_tab is not None, "Planner tab not found in bottom nav"
        planner_tab.click()
        time.sleep(3)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Planner") or contains(@text,"Planner")]',
            '//*[contains(@content-desc,"Travel") or contains(@text,"Travel")]',
        ), "Travel Planner screen did not open"

    # PM037 — Tap Favorites tab navigates to Favorites
    @pytest.mark.home
    def test_PM037_tap_favorites_tab_navigates(self, logged_in_driver):
        driver = logged_in_driver
        _ensure_home(driver)
        fav_tab = _find(
            driver,
            '//*[@content-desc="Favorites" or @text="Favorites"]',
            '//*[contains(@content-desc,"Favorite") or contains(@text,"Favorite")]',
        )
        assert fav_tab is not None, "Favorites tab not found in bottom nav"
        fav_tab.click()
        time.sleep(3)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Favorites") or contains(@text,"Favorites")]',
        ), "Favorites screen did not open"

    # PM038 — Tap Profile tab navigates to Profile screen
    @pytest.mark.home
    def test_PM038_tap_profile_tab_navigates(self, logged_in_driver):
        driver = logged_in_driver
        _ensure_home(driver)
        profile_tab = _find(
            driver,
            '//*[@content-desc="Profile" or @text="Profile"]',
            '//*[contains(@content-desc,"Profile") or contains(@text,"Profile")]',
        )
        assert profile_tab is not None, "Profile tab not found in bottom nav"
        profile_tab.click()
        time.sleep(3)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Profile") or contains(@text,"Profile")]',
            '//*[contains(@content-desc,"Sign Out") or contains(@text,"Sign Out")]',
            '//*[contains(@content-desc,"Reports") or contains(@text,"Reports")]',
        ), "Profile screen did not open"

    # PM039 — Back navigation from Search to Home works
    @pytest.mark.home
    def test_PM039_back_navigation_from_search(self, logged_in_driver):
        """Android back button from Search must return to Home on real device."""
        driver = logged_in_driver
        _ensure_home(driver)
        search_tab = _find(driver,
            '//*[@content-desc="Search" or @text="Search"]',
            '//*[contains(@content-desc,"Search") or contains(@text,"Search")]',
        )
        if search_tab:
            search_tab.click(); time.sleep(2)
        driver.back()
        time.sleep(3)   # real device back animation
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Trending") or contains(@text,"Trending")]',
            '//*[contains(@content-desc,"Categories") or contains(@text,"Categories")]',
            '//*[contains(@content-desc,"Home") or contains(@text,"Home")]',
        ), "Back navigation from Search did not return to Home"

    # PM040 — All bottom nav icons render simultaneously
    @pytest.mark.home
    def test_PM040_bottom_nav_all_icons_render(self, logged_in_driver):
        """All expected bottom navigation tabs must be visible at the same time."""
        driver = logged_in_driver
        _ensure_home(driver)
        home_tab   = _exists(driver, '//*[contains(@content-desc,"Home") or contains(@text,"Home")]', timeout=8)
        search_tab = _exists(driver, '//*[contains(@content-desc,"Search") or contains(@text,"Search")]', timeout=8)
        planner_tab = _exists(driver, '//*[contains(@content-desc,"Planner") or contains(@text,"Planner")]', timeout=8)
        fav_tab = _exists(driver, '//*[contains(@content-desc,"Favorites") or contains(@text,"Favorites")]', timeout=8)
        profile_tab = _exists(driver, '//*[contains(@content-desc,"Profile") or contains(@text,"Profile")]', timeout=8)
        assert home_tab and search_tab and planner_tab and fav_tab and profile_tab, "Not all 5 bottom navigation tabs found on physical device"
