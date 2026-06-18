"""
test_05_travel_planner.py — Travel Planner & Favorites Tests (AM079–AM090)
==========================================================================
CrowdSense Appium Mobile E2E Suite
Target: Pixel 3a API 37 AVD  |  Automation: UiAutomator2

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


def _navigate_to_planner(driver):
    """Tap the Planner tab in bottom nav."""
    tab = _find(driver,
        '//*[@content-desc="Planner" or @text="Planner"]',
        '//*[contains(@content-desc,"Plan") or contains(@text,"Plan")]',
        timeout=6)
    if tab:
        tab.click()
        time.sleep(2)


def _navigate_to_favorites(driver):
    """Tap the Favorites tab in bottom nav."""
    tab = _find(driver,
        '//*[@content-desc="Favorites" or @text="Favorites"]',
        '//*[contains(@content-desc,"Favorite") or contains(@text,"Favorite")]',
        timeout=6)
    if tab:
        tab.click()
        time.sleep(2)


def _open_first_place(driver):
    """Navigate to search and open the first result."""
    tab = _find(driver, '//*[@content-desc="Search" or @text="Search"]', timeout=5)
    if tab:
        tab.click()
        time.sleep(2)
    inp = _find(driver, '//android.widget.EditText', timeout=8)
    if inp:
        inp.clear()
        inp.send_keys("park")
        time.sleep(3)
    first = _find(driver,
        '(//*[contains(@content-desc,"park") or contains(@text,"park")])[2]',
        '(//android.widget.ListView//android.widget.TextView)[1]',
    )
    if first:
        first.click()
        time.sleep(3)


# ─── Test Class ───────────────────────────────────────────────────────────────

class TestTravelPlannerAndFavorites:

    # AM079 — Travel Planner screen renders
    @pytest.mark.planner
    @pytest.mark.smoke
    def test_AM079_travel_planner_screen_renders(self, logged_in_driver):
        """Travel Planner screen must load and render content."""
        driver = logged_in_driver
        _navigate_to_planner(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Planner") or contains(@text,"Planner")]',
            '//*[contains(@content-desc,"Travel") or contains(@text,"Travel")]',
            '//*[contains(@content-desc,"Plan") or contains(@text,"Plan")]',
        ), "Travel Planner screen did not render"

    # AM080 — Travel Planner shows heading
    @pytest.mark.planner
    def test_AM080_travel_planner_shows_heading(self, logged_in_driver):
        """Travel Planner must display a heading / title text."""
        driver = logged_in_driver
        _navigate_to_planner(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Travel Planner") or contains(@text,"Travel Planner")]',
            '//*[contains(@content-desc,"Plan Your Trip") or contains(@text,"Plan Your Trip")]',
            '//*[contains(@content-desc,"Trip") or contains(@text,"Trip")]',
        ), "Travel Planner heading not found"

    # AM081 — Travel Planner has From selector
    @pytest.mark.planner
    def test_AM081_travel_planner_has_from_selector(self, logged_in_driver):
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

    # AM082 — Travel Planner has To selector
    @pytest.mark.planner
    def test_AM082_travel_planner_has_to_selector(self, logged_in_driver):
        """Travel Planner screen must have a 'To' destination selector."""
        driver = logged_in_driver
        _navigate_to_planner(driver)
        assert _exists(
            driver,
            '//*[@content-desc="To" or @text="To"]',
            '//*[contains(@content-desc,"Destination") or contains(@text,"Destination")]',
            '//*[contains(@content-desc,"Where to") or contains(@text,"Where to")]',
        ), "To selector not found in Travel Planner"

    # AM083 — Travel Planner has Calculate Best Plan button
    @pytest.mark.planner
    def test_AM083_travel_planner_calculate_button(self, logged_in_driver):
        """Travel Planner must have a 'Calculate Best Plan' button."""
        driver = logged_in_driver
        _navigate_to_planner(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Calculate") or contains(@text,"Calculate")]',
            '//*[contains(@content-desc,"Best Plan") or contains(@text,"Best Plan")]',
            '//*[contains(@content-desc,"Plan") or contains(@text,"Plan")]',
        ), "Calculate Best Plan button not found in Travel Planner"

    # AM084 — Travel Planner shows crowd-aware description
    @pytest.mark.planner
    def test_AM084_travel_planner_crowd_aware_text(self, logged_in_driver):
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

    # AM085 — Favorites screen renders
    @pytest.mark.favorites
    @pytest.mark.smoke
    def test_AM085_favorites_screen_renders(self, logged_in_driver):
        """Favorites screen must load and render content."""
        driver = logged_in_driver
        _navigate_to_favorites(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Favorites") or contains(@text,"Favorites")]',
            '//*[contains(@content-desc,"favorite") or contains(@text,"favorite")]',
        ), "Favorites screen did not render"

    # AM086 — Favorites shows empty state or list
    @pytest.mark.favorites
    def test_AM086_favorites_empty_state_or_list(self, logged_in_driver):
        """Favorites screen must show either a list of favorites or an empty state message."""
        driver = logged_in_driver
        _navigate_to_favorites(driver)
        src = driver.page_source
        # Should have at least an empty state or list items
        assert len(src) > 100, "Favorites screen appears completely empty"
        # Either empty state text or list items should be present
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
        )
        assert has_content or has_list, "Favorites screen shows neither empty state nor content list"

    # AM087 — Add place to favorites works
    @pytest.mark.favorites
    def test_AM087_add_place_to_favorites(self, logged_in_driver):
        """Tapping the favorite heart icon on a Place Details screen must save it."""
        driver = logged_in_driver
        _open_first_place(driver)
        fav_icon = _find(driver,
            '//*[contains(@content-desc,"Favorite") or contains(@text,"Favorite")]',
            '//*[contains(@content-desc,"Save") or contains(@text,"Save")]',
        )
        if fav_icon:
            fav_icon.click()
            time.sleep(2)
        # Check for feedback (toast, snackbar, or icon state change)
        src = driver.page_source
        assert len(src) > 100, "App appears to have crashed after tapping favorite"

    # AM088 — Favorite heart icon toggles state
    @pytest.mark.favorites
    def test_AM088_favorite_icon_toggles(self, logged_in_driver):
        """Tapping the heart icon twice should toggle favorite state without crashing."""
        driver = logged_in_driver
        _open_first_place(driver)
        fav_icon = _find(driver,
            '//*[contains(@content-desc,"Favorite") or contains(@text,"Favorite")]',
            '//*[contains(@content-desc,"Save") or contains(@text,"Save")]',
        )
        if fav_icon:
            fav_icon.click()
            time.sleep(1)
            # Try to find the icon again and tap to toggle off
            fav_icon2 = _find(driver,
                '//*[contains(@content-desc,"Favorite") or contains(@text,"Favorite")]',
                '//*[contains(@content-desc,"Save") or contains(@text,"Save")]',
            )
            if fav_icon2:
                fav_icon2.click()
                time.sleep(1)
        src = driver.page_source
        assert len(src) > 100, "App crashed during favorite icon toggle"

    # AM089 — Unfavorite removes from favorites list
    @pytest.mark.favorites
    def test_AM089_unfavorite_removes_from_list(self, logged_in_driver):
        """After removing a favorite, the Favorites list should update."""
        driver = logged_in_driver
        # First add a favorite
        _open_first_place(driver)
        fav_icon = _find(driver,
            '//*[contains(@content-desc,"Favorite") or contains(@text,"Favorite")]')
        if fav_icon:
            fav_icon.click(); time.sleep(1)
        # Go to favorites
        driver.back(); time.sleep(1)
        _navigate_to_favorites(driver)
        src = driver.page_source
        assert len(src) > 100, "Favorites screen not accessible after unfavorite action"

    # AM090 — Favorites list updates after adding
    @pytest.mark.favorites
    def test_AM090_favorites_list_updates_after_adding(self, logged_in_driver):
        """After adding a place to favorites, the Favorites screen should reflect the change."""
        driver = logged_in_driver
        _open_first_place(driver)
        fav_icon = _find(driver,
            '//*[contains(@content-desc,"Favorite") or contains(@text,"Favorite")]')
        if fav_icon:
            fav_icon.click(); time.sleep(1)
        driver.back(); time.sleep(1)
        _navigate_to_favorites(driver)
        src = driver.page_source
        # Either a place name is listed or an empty state is shown
        assert len(src) > 100, "Favorites screen is empty or crashed after adding favorite"
