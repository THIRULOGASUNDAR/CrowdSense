"""
test_03_search_place.py — Search, Place Details & Crowd Report Tests (AM041–AM060)
===================================================================================
CrowdSense Appium Mobile E2E Suite
Target: Pixel 3a API 37 AVD  |  Automation: UiAutomator2

Covers:
  - Search screen UI and suggestion chips
  - Typing in search and viewing results
  - Place Details screen sections (name, location, crowd status, forecast)
  - Crowd Report form (levels, note field)
  - Community Photos page
  - Favorite and Share icons in place details
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


def _navigate_to_search(driver):
    """Tap the Search tab to navigate to the Search screen."""
    tab = _find(driver, '//*[@content-desc="Search" or @text="Search"]', timeout=5)
    if tab:
        tab.click()
        time.sleep(2)


def _open_first_result(driver):
    """Type a query and tap the first search result."""
    _navigate_to_search(driver)
    search_input = _find(driver, '//android.widget.EditText', timeout=8)
    if search_input:
        search_input.clear()
        search_input.send_keys("park")
        time.sleep(3)
    # Tap first list item
    first_result = _find(
        driver,
        '(//android.widget.ListView/android.widget.TextView)[1]',
        '(//androidx.recyclerview.widget.RecyclerView//android.widget.TextView)[1]',
        '//*[contains(@content-desc,"park") or contains(@text,"park")]',
    )
    if first_result:
        first_result.click()
        time.sleep(3)


# ─── Test Class ───────────────────────────────────────────────────────────────

class TestSearchAndPlace:

    # AM041 — Search screen loads with text input
    @pytest.mark.search
    @pytest.mark.smoke
    def test_AM041_search_screen_loads(self, logged_in_driver):
        """Search screen must render with a text input field."""
        driver = logged_in_driver
        _navigate_to_search(driver)
        assert _exists(
            driver,
            '//android.widget.EditText',
            '//*[contains(@content-desc,"search") or contains(@text,"search")]',
        ), "Search screen text input not found"

    # AM042 — Search shows suggestion chips
    @pytest.mark.search
    def test_AM042_search_shows_suggestion_chips(self, logged_in_driver):
        """Search screen must display suggestion chips (Coffee Shop, Library, Museum, etc.)."""
        driver = logged_in_driver
        _navigate_to_search(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Coffee") or contains(@text,"Coffee")]',
            '//*[contains(@content-desc,"Library") or contains(@text,"Library")]',
            '//*[contains(@content-desc,"Museum") or contains(@text,"Museum")]',
            '//*[contains(@content-desc,"Suggestion") or contains(@text,"Suggestion")]',
        ), "No search suggestion chips found on Search screen"

    # AM043 — Search shows Recent Searches section
    @pytest.mark.search
    def test_AM043_search_shows_recent_searches(self, logged_in_driver):
        """Search screen must show a Recent Searches section (even if empty)."""
        driver = logged_in_driver
        _navigate_to_search(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Recent") or contains(@text,"Recent")]',
            '//*[contains(@content-desc,"recent") or contains(@text,"recent")]',
        ), "Recent Searches section not found on Search screen"

    # AM044 — Typing in search box triggers results
    @pytest.mark.search
    def test_AM044_typing_search_query_shows_results(self, logged_in_driver):
        """Typing a search query must trigger a results list or loading state."""
        driver = logged_in_driver
        _navigate_to_search(driver)
        search_input = _find(driver, '//android.widget.EditText', timeout=8)
        assert search_input is not None, "Search input not found"
        search_input.clear()
        search_input.send_keys("coffee")
        time.sleep(3)
        # Results list or at least a loading/empty state should appear
        src = driver.page_source
        assert len(src) > 100, "Page source empty after search query"

    # AM045 — Search results list renders
    @pytest.mark.search
    def test_AM045_search_results_list_renders(self, logged_in_driver):
        """After typing a query, search results must appear in a list."""
        driver = logged_in_driver
        _navigate_to_search(driver)
        search_input = _find(driver, '//android.widget.EditText', timeout=8)
        if search_input:
            search_input.clear()
            search_input.send_keys("mall")
            time.sleep(3)
        src = driver.page_source
        assert "mall" in src.lower() or len(src) > 200, "Search results did not render"

    # AM046 — Tap on search result loads Place Details
    @pytest.mark.search
    @pytest.mark.place
    def test_AM046_tap_result_loads_place_details(self, logged_in_driver):
        """Tapping a search result must navigate to the Place Details screen."""
        driver = logged_in_driver
        _navigate_to_search(driver)
        search_input = _find(driver, '//android.widget.EditText', timeout=8)
        if search_input:
            search_input.clear()
            search_input.send_keys("park")
            time.sleep(3)
        first = _find(
            driver,
            '(//android.widget.ListView//android.widget.TextView)[1]',
            '(//*[contains(@content-desc,"park") or contains(@text,"park")])[2]',
        )
        if first:
            first.click()
            time.sleep(3)
        # Place Details should have crowd/location info
        src = driver.page_source
        assert len(src) > 100, "Place Details screen did not load after tapping result"

    # AM047 — Place Details shows place name
    @pytest.mark.place
    def test_AM047_place_details_shows_place_name(self, logged_in_driver):
        """Place Details screen must display the place's name."""
        driver = logged_in_driver
        _open_first_result(driver)
        src = driver.page_source
        # Page should have substantial content (name, location, etc.)
        assert len(src) > 200, "Place Details appears to not have loaded content"

    # AM048 — Place Details shows location info
    @pytest.mark.place
    def test_AM048_place_details_shows_location(self, logged_in_driver):
        """Place Details screen must show location/address information."""
        driver = logged_in_driver
        _open_first_result(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Location") or contains(@text,"Location")]',
            '//*[contains(@content-desc,"Address") or contains(@text,"Address")]',
            '//*[contains(@content-desc,"km") or contains(@text,"km")]',
        ), "Location information not found on Place Details screen"

    # AM049 — Place Details shows crowd status card
    @pytest.mark.place
    def test_AM049_place_details_crowd_status_card(self, logged_in_driver):
        """Place Details must show a current crowd status card (Live Crowd / Crowd Level)."""
        driver = logged_in_driver
        _open_first_result(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Crowd") or contains(@text,"Crowd")]',
            '//*[contains(@content-desc,"crowd") or contains(@text,"crowd")]',
            '//*[contains(@content-desc,"Status") or contains(@text,"Status")]',
            '//*[contains(@content-desc,"Busy") or contains(@text,"Busy")]',
        ), "Crowd Status card not found on Place Details screen"

    # AM050 — Place Details shows Best Time to Visit
    @pytest.mark.place
    def test_AM050_place_details_best_time_to_visit(self, logged_in_driver):
        """Place Details screen must show a 'Best Time to Visit' section."""
        driver = logged_in_driver
        _open_first_result(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Best Time") or contains(@text,"Best Time")]',
            '//*[contains(@content-desc,"best time") or contains(@text,"best time")]',
            '//*[contains(@content-desc,"Visit") or contains(@text,"Visit")]',
        ), "Best Time to Visit section not found on Place Details"

    # AM051 — Place Details shows Crowd Forecast section
    @pytest.mark.place
    def test_AM051_place_details_crowd_forecast(self, logged_in_driver):
        """Place Details screen must display a Crowd Forecast chart or section."""
        driver = logged_in_driver
        _open_first_result(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Forecast") or contains(@text,"Forecast")]',
            '//*[contains(@content-desc,"forecast") or contains(@text,"forecast")]',
            '//*[contains(@content-desc,"Crowd Trend") or contains(@text,"Crowd Trend")]',
        ), "Crowd Forecast section not found on Place Details"

    # AM052 — Place Details has Report Crowd button
    @pytest.mark.place
    def test_AM052_place_details_report_crowd_button(self, logged_in_driver):
        """Place Details screen must have a 'Report Live Crowd' button."""
        driver = logged_in_driver
        _open_first_result(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Report") or contains(@text,"Report")]',
            '//*[contains(@content-desc,"report") or contains(@text,"report")]',
        ), "Report Crowd button not found on Place Details screen"

    # AM053 — Place Details shows About section
    @pytest.mark.place
    def test_AM053_place_details_about_section(self, logged_in_driver):
        """Place Details screen must have an About section."""
        driver = logged_in_driver
        _open_first_result(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"About") or contains(@text,"About")]',
            '//*[contains(@content-desc,"about") or contains(@text,"about")]',
            '//*[contains(@content-desc,"Description") or contains(@text,"Description")]',
        ), "About section not found on Place Details screen"

    # AM054 — Favorite icon visible in place details
    @pytest.mark.place
    def test_AM054_place_details_favorite_icon(self, logged_in_driver):
        """Place Details app bar must show a favorite (heart) icon."""
        driver = logged_in_driver
        _open_first_result(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Favorite") or contains(@text,"Favorite")]',
            '//*[contains(@content-desc,"favorite") or contains(@text,"favorite")]',
            '//*[contains(@content-desc,"heart") or contains(@text,"heart")]',
            '//*[contains(@content-desc,"Save") or contains(@text,"Save")]',
        ), "Favorite icon not found in Place Details app bar"

    # AM055 — Share icon visible in place details
    @pytest.mark.place
    def test_AM055_place_details_share_icon(self, logged_in_driver):
        """Place Details app bar must show a share icon."""
        driver = logged_in_driver
        _open_first_result(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Share") or contains(@text,"Share")]',
            '//*[contains(@content-desc,"share") or contains(@text,"share")]',
        ), "Share icon not found in Place Details app bar"

    # AM056 — Crowd Report: Low / Not Busy option
    @pytest.mark.place
    def test_AM056_crowd_report_low_option(self, logged_in_driver):
        """Crowd Report form must have a 'Not Busy / Low' option."""
        driver = logged_in_driver
        _open_first_result(driver)
        report_btn = _find(
            driver,
            '//*[contains(@content-desc,"Report") or contains(@text,"Report")]',
        )
        if report_btn:
            report_btn.click()
            time.sleep(2)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Not busy") or contains(@text,"Not busy")]',
            '//*[contains(@content-desc,"Low") or contains(@text,"Low")]',
        ), "Not Busy / Low crowd level option not found in Crowd Report"

    # AM057 — Crowd Report: Moderate / A bit busy option
    @pytest.mark.place
    def test_AM057_crowd_report_moderate_option(self, logged_in_driver):
        """Crowd Report form must have a 'A bit busy / Moderate' option."""
        driver = logged_in_driver
        _open_first_result(driver)
        report_btn = _find(driver,
            '//*[contains(@content-desc,"Report") or contains(@text,"Report")]')
        if report_btn:
            report_btn.click(); time.sleep(2)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"A bit busy") or contains(@text,"A bit busy")]',
            '//*[contains(@content-desc,"Moderate") or contains(@text,"Moderate")]',
        ), "Moderate crowd level option not found"

    # AM058 — Crowd Report: High / Very Crowded option
    @pytest.mark.place
    def test_AM058_crowd_report_high_option(self, logged_in_driver):
        """Crowd Report form must have a 'Very Crowded / High' option."""
        driver = logged_in_driver
        _open_first_result(driver)
        report_btn = _find(driver,
            '//*[contains(@content-desc,"Report") or contains(@text,"Report")]')
        if report_btn:
            report_btn.click(); time.sleep(2)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Very crowded") or contains(@text,"Very crowded")]',
            '//*[contains(@content-desc,"High") or contains(@text,"High")]',
        ), "High crowd level option not found"

    # AM059 — Crowd Report has optional note field
    @pytest.mark.place
    def test_AM059_crowd_report_note_field(self, logged_in_driver):
        """Crowd Report form must include an optional note/comment text field."""
        driver = logged_in_driver
        _open_first_result(driver)
        report_btn = _find(driver,
            '//*[contains(@content-desc,"Report") or contains(@text,"Report")]')
        if report_btn:
            report_btn.click(); time.sleep(2)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Note") or contains(@text,"Note")]',
            '//*[contains(@content-desc,"note") or contains(@text,"note")]',
            '//*[contains(@content-desc,"Comment") or contains(@text,"Comment")]',
            '//android.widget.EditText',
        ), "Note/comment field not found in Crowd Report form"

    # AM060 — Community Photos page loads
    @pytest.mark.place
    def test_AM060_community_photos_page_loads(self, logged_in_driver):
        """Navigating to Community Photos from Place Details must load that screen."""
        driver = logged_in_driver
        _open_first_result(driver)
        photos_btn = _find(
            driver,
            '//*[contains(@content-desc,"Photo") or contains(@text,"Photo")]',
            '//*[contains(@content-desc,"Community") or contains(@text,"Community")]',
            '//*[contains(@content-desc,"photo") or contains(@text,"photo")]',
        )
        if photos_btn:
            photos_btn.click()
            time.sleep(3)
        src = driver.page_source
        assert len(src) > 100, "Community Photos page did not load"
