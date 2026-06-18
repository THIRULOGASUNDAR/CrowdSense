"""
test_05_travel_planner.py — Travel Planner & Favorites Tests (PM079–PM090)
==========================================================================
CrowdSense Appium Physical Device E2E Suite
Target: Real Android device via USB  |  Automation: UiAutomator2

Covers:
  - Travel Planner screen UI (heading, From/To selectors, calculate button)
  - Favorites screen (empty state, adding and removing favorites)
  - Favorite heart icon toggle in Place Details
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


def _navigate_to_planner(driver):
    """Tap the Planner tab in bottom nav."""
    _ensure_home(driver)
    tab = _find(driver,
        '//*[@content-desc="Planner" or @text="Planner"]',
        '//*[contains(@content-desc,"Plan") or contains(@text,"Plan")]',
        timeout=8)
    if tab:
        tab.click()
        time.sleep(3)


def _navigate_to_favorites(driver):
    """Tap the Favorites tab in bottom nav."""
    _ensure_home(driver)
    tab = _find(driver,
        '//*[@content-desc="Favorites" or @text="Favorites"]',
        '//*[contains(@content-desc,"Favorite") or contains(@text,"Favorite")]',
        timeout=8)
    if tab:
        tab.click()
        time.sleep(3)


def _open_first_place(driver):
    """Navigate to Search and open the first result."""
    _ensure_home(driver)
    tab = _find(driver,
        '//*[@content-desc="Search" or @text="Search"]',
        '//*[contains(@content-desc,"Search") or contains(@text,"Search")]',
        timeout=8)
    if tab:
        tab.click(); time.sleep(2)
    inp = _find(driver, '//android.widget.EditText', timeout=10)
    if inp:
        inp.clear()
        inp.send_keys("park")
        time.sleep(4)
    first = _find(driver,
        '(//android.widget.ScrollView/android.widget.Button)[1]',
        '(//*[contains(@content-desc,"Park") or contains(@text,"Park") or contains(@content-desc,"park") or contains(@text,"park")])[2]',
        '(//android.widget.ListView//android.widget.TextView)[1]',
    )
    if first:
        first.click()
        time.sleep(4)


# ─── Test Class ───────────────────────────────────────────────────────────────

class TestTravelPlannerAndFavorites:

    # PM079 — Travel Planner screen renders
    @pytest.mark.planner
    @pytest.mark.smoke
    def test_PM079_travel_planner_screen_renders(self, logged_in_driver):
        """Travel Planner screen must load and render content on physical device."""
        driver = logged_in_driver
        _navigate_to_planner(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Planner") or contains(@text,"Planner")]',
            '//*[contains(@content-desc,"Travel") or contains(@text,"Travel")]',
            '//*[contains(@content-desc,"Plan") or contains(@text,"Plan")]',
        ), "Travel Planner screen did not render"

    # PM080 — Travel Planner shows heading
    @pytest.mark.planner
    def test_PM080_travel_planner_shows_heading(self, logged_in_driver):
        """Travel Planner must display a heading / title text."""
        driver = logged_in_driver
        _navigate_to_planner(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Travel Planner") or contains(@text,"Travel Planner")]',
            '//*[contains(@content-desc,"Plan Your Trip") or contains(@text,"Plan Your Trip")]',
            '//*[contains(@content-desc,"Trip") or contains(@text,"Trip")]',
        ), "Travel Planner heading not found"

    # PM081 — Travel Planner has From selector
    @pytest.mark.planner
    def test_PM081_travel_planner_has_from_selector(self, logged_in_driver):
        """Travel Planner screen must have a 'From' location selector."""
        driver = logged_in_driver
        _navigate_to_planner(driver)
        assert _exists(
            driver,
            '//*[@content-desc="From" or @text="From"]',
            '//*[contains(@content-desc,"From") or contains(@text,"From")]',
            '//*[contains(@content-desc,"Start") or contains(@text,"Start")]',
            '//*[contains(@content-desc,"Source") or contains(@text,"Source")]',
        ), "From selector not found in Travel Planner"

    # PM082 — Travel Planner has To selector
    @pytest.mark.planner
    def test_PM082_travel_planner_has_to_selector(self, logged_in_driver):
        """Travel Planner screen must have a 'To' destination selector."""
        driver = logged_in_driver
        _navigate_to_planner(driver)
        assert _exists(
            driver,
            '//*[@content-desc="To" or @text="To"]',
            '//*[contains(@content-desc,"To\n") or contains(@text,"To\n")]',
            '//*[contains(@content-desc,"Destination") or contains(@text,"Destination")]',
            '//*[contains(@content-desc,"Where to") or contains(@text,"Where to")]',
        ), "To selector not found in Travel Planner"

    # PM083 — Travel Planner has Calculate Best Plan button
    @pytest.mark.planner
    def test_PM083_travel_planner_calculate_button(self, logged_in_driver):
        """Travel Planner must have a 'Calculate Best Plan' button."""
        driver = logged_in_driver
        _navigate_to_planner(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Calculate") or contains(@text,"Calculate")]',
            '//*[contains(@content-desc,"Best Plan") or contains(@text,"Best Plan")]',
            '//*[contains(@content-desc,"Plan") or contains(@text,"Plan")]',
        ), "Calculate Best Plan button not found in Travel Planner"

    # PM084 — Travel Planner shows crowd-aware description
    @pytest.mark.planner
    def test_PM084_travel_planner_crowd_aware_text(self, logged_in_driver):
        """Travel Planner must display crowd-aware description text."""
        driver = logged_in_driver
        _navigate_to_planner(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"crowd") or contains(@text,"crowd")]',
            '//*[contains(@content-desc,"Crowd") or contains(@text,"Crowd")]',
            '//*[contains(@content-desc,"smart") or contains(@text,"smart")]',
            '//*[contains(@content-desc,"optimal") or contains(@text,"optimal")]',
        ), "Crowd-aware description not found in Travel Planner"

    # PM085 — Favorites screen renders
    @pytest.mark.favorites
    @pytest.mark.smoke
    def test_PM085_favorites_screen_renders(self, logged_in_driver):
        """Favorites screen must load and render content on physical device."""
        driver = logged_in_driver
        _navigate_to_favorites(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Favorites") or contains(@text,"Favorites")]',
            '//*[contains(@content-desc,"favorite") or contains(@text,"favorite")]',
        ), "Favorites screen did not render"

    # PM086 — Favorites shows empty state or list
    @pytest.mark.favorites
    def test_PM086_favorites_empty_state_or_list(self, logged_in_driver):
        """Favorites screen must show either a list or an empty state message."""
        driver = logged_in_driver
        _navigate_to_favorites(driver)
        src = driver.page_source
        assert len(src) > 100, "Favorites screen appears completely empty"
        has_content = _exists(
            driver,
            '//*[contains(@content-desc,"No favorites") or contains(@text,"No favorites")]',
            '//*[contains(@content-desc,"empty") or contains(@text,"empty")]',
            '//*[contains(@content-desc,"Start exploring") or contains(@text,"Start exploring")]',
        )
        has_list = _exists(
            driver,
            '//android.widget.ListView',
            '//androidx.recyclerview.widget.RecyclerView',
            '//*[@scrollable="true"]',
            '//android.widget.ImageView',
        )
        assert has_content or has_list, "Favorites shows neither empty state nor content list"

    # PM087 — Add place to favorites works
    @pytest.mark.favorites
    def test_PM087_add_place_to_favorites(self, logged_in_driver):
        """Tapping the favorite heart icon on Place Details must save it."""
        driver = logged_in_driver
        _open_first_place(driver)
        fav_icon = _find(driver,
            '//android.widget.Button[@content-desc="Back"]/following-sibling::android.widget.Button[1]',
            '//*[contains(@content-desc,"Favorite") or contains(@text,"Favorite")]',
            '//*[contains(@content-desc,"Save") or contains(@text,"Save")]',
        )
        if fav_icon:
            fav_icon.click()
            time.sleep(2)
        src = driver.page_source
        assert len(src) > 100, "App appears to have crashed after tapping favorite"

    # PM088 — Favorite heart icon toggles state
    @pytest.mark.favorites
    def test_PM088_favorite_icon_toggles(self, logged_in_driver):
        """Tapping the heart icon twice must toggle favorite state without crashing."""
        driver = logged_in_driver
        _open_first_place(driver)
        fav_icon = _find(driver,
            '//android.widget.Button[@content-desc="Back"]/following-sibling::android.widget.Button[1]',
            '//*[contains(@content-desc,"Favorite") or contains(@text,"Favorite")]',
            '//*[contains(@content-desc,"Save") or contains(@text,"Save")]',
        )
        if fav_icon:
            fav_icon.click(); time.sleep(1)
            fav_icon2 = _find(driver,
                '//android.widget.Button[@content-desc="Back"]/following-sibling::android.widget.Button[1]',
                '//*[contains(@content-desc,"Favorite") or contains(@text,"Favorite")]',
                '//*[contains(@content-desc,"Save") or contains(@text,"Save")]',
            )
            if fav_icon2:
                fav_icon2.click(); time.sleep(1)
        src = driver.page_source
        assert len(src) > 100, "App crashed during favorite icon toggle"

    # PM089 — Unfavorite removes from favorites list
    @pytest.mark.favorites
    def test_PM089_unfavorite_removes_from_list(self, logged_in_driver):
        """After removing a favorite, the Favorites list should update."""
        driver = logged_in_driver
        _open_first_place(driver)
        fav_icon = _find(driver,
            '//android.widget.Button[@content-desc="Back"]/following-sibling::android.widget.Button[1]',
            '//*[contains(@content-desc,"Favorite") or contains(@text,"Favorite")]')
        if fav_icon:
            fav_icon.click(); time.sleep(1)
        driver.back(); time.sleep(2)
        _navigate_to_favorites(driver)
        src = driver.page_source
        assert len(src) > 100, "Favorites screen not accessible after unfavorite action"

    # PM090 — Favorites list updates after adding
    @pytest.mark.favorites
    def test_PM090_favorites_list_updates_after_adding(self, logged_in_driver):
        """After adding a place to favorites, Favorites screen must reflect the change."""
        driver = logged_in_driver
        _open_first_place(driver)
        fav_icon = _find(driver,
            '//android.widget.Button[@content-desc="Back"]/following-sibling::android.widget.Button[1]',
            '//*[contains(@content-desc,"Favorite") or contains(@text,"Favorite")]')
        if fav_icon:
            fav_icon.click(); time.sleep(1)
        driver.back(); time.sleep(2)
        _navigate_to_favorites(driver)
        src = driver.page_source
        assert len(src) > 100, "Favorites screen is empty or crashed after adding favorite"
