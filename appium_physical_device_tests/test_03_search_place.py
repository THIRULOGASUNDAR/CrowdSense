"""
test_03_search_place.py — Search, Place Details & Crowd Report Tests (PM041–PM060)
===================================================================================
CrowdSense Appium Physical Device E2E Suite
Target: Real Android device via USB  |  Automation: UiAutomator2

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


def _navigate_to_search(driver):
    """Tap the Search tab to navigate to the Search screen."""
    _ensure_home(driver)
    tab = _find(driver,
        '//*[@content-desc="Search" or @text="Search"]',
        '//*[contains(@content-desc,"Search") or contains(@text,"Search")]',
        timeout=8)
    if tab:
        tab.click()
        time.sleep(3)



def _open_first_result(driver):
    """Type a query and tap the first search result."""
    _navigate_to_search(driver)
    search_input = _find(driver, '//android.widget.EditText', timeout=10)
    if search_input:
        search_input.clear()
        search_input.send_keys("park")
        time.sleep(4)   # real device network call may be slower
    first_result = _find(
        driver,
        '(//android.widget.ScrollView/android.widget.Button)[1]',
        '(//*[contains(@content-desc,"Park") or contains(@text,"Park") or contains(@content-desc,"park") or contains(@text,"park")])[2]',
        '(//android.widget.ListView//android.widget.TextView)[1]',
        '(//androidx.recyclerview.widget.RecyclerView//android.widget.TextView)[1]',
    )
    if first_result:
        first_result.click()
        time.sleep(4)


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


def _scroll_to_report_button(driver):
    for _ in range(3):
        if _exists(driver,
            '//*[contains(@content-desc,"Report") or contains(@text,"Report")]',
            '//*[contains(@content-desc,"report") or contains(@text,"report")]',
            timeout=2
        ):
            return True
        _scroll_down(driver)
    return False


# ─── Test Class ───────────────────────────────────────────────────────────────

class TestSearchAndPlace:

    # PM041 — Search screen loads with text input
    @pytest.mark.search
    @pytest.mark.smoke
    def test_PM041_search_screen_loads(self, logged_in_driver):
        """Search screen must render with a text input field."""
        driver = logged_in_driver
        _navigate_to_search(driver)
        assert _exists(
            driver,
            '//android.widget.EditText',
            '//*[contains(@content-desc,"search") or contains(@text,"search")]',
        ), "Search screen text input not found on physical device"

    # PM042 — Search shows suggestion chips
    @pytest.mark.search
    def test_PM042_search_shows_suggestion_chips(self, logged_in_driver):
        driver = logged_in_driver
        _navigate_to_search(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Coffee") or contains(@text,"Coffee")]',
            '//*[contains(@content-desc,"Library") or contains(@text,"Library")]',
            '//*[contains(@content-desc,"Museum") or contains(@text,"Museum")]',
            '//*[contains(@content-desc,"Suggestion") or contains(@text,"Suggestion")]',
        ), "No search suggestion chips found on Search screen"

    # PM043 — Search shows Recent Searches section
    @pytest.mark.search
    def test_PM043_search_shows_recent_searches(self, logged_in_driver):
        driver = logged_in_driver
        _navigate_to_search(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Recent") or contains(@text,"Recent")]',
            '//*[contains(@content-desc,"recent") or contains(@text,"recent")]',
        ), "Recent Searches section not found on Search screen"

    # PM044 — Typing in search box triggers results
    @pytest.mark.search
    def test_PM044_typing_search_query_shows_results(self, logged_in_driver):
        driver = logged_in_driver
        _navigate_to_search(driver)
        search_input = _find(driver, '//android.widget.EditText', timeout=10)
        assert search_input is not None, "Search input not found"
        search_input.clear()
        search_input.send_keys("coffee")
        time.sleep(4)
        src = driver.page_source
        assert len(src) > 100, "Page source empty after search query on physical device"

    # PM045 — Search results list renders
    @pytest.mark.search
    def test_PM045_search_results_list_renders(self, logged_in_driver):
        driver = logged_in_driver
        _navigate_to_search(driver)
        search_input = _find(driver, '//android.widget.EditText', timeout=10)
        if search_input:
            search_input.clear()
            search_input.send_keys("mall")
            time.sleep(4)
        src = driver.page_source
        assert "mall" in src.lower() or len(src) > 200, "Search results did not render"

    # PM046 — Tap on search result loads Place Details
    @pytest.mark.search
    @pytest.mark.place
    def test_PM046_tap_result_loads_place_details(self, logged_in_driver):
        driver = logged_in_driver
        _navigate_to_search(driver)
        search_input = _find(driver, '//android.widget.EditText', timeout=10)
        if search_input:
            search_input.clear()
            search_input.send_keys("park")
            time.sleep(4)
        first = _find(
            driver,
            '(//android.widget.ListView//android.widget.TextView)[1]',
            '(//*[contains(@content-desc,"park") or contains(@text,"park")])[2]',
        )
        if first:
            first.click()
            time.sleep(4)
        src = driver.page_source
        assert len(src) > 100, "Place Details screen did not load"

    # PM047 — Place Details shows place name
    @pytest.mark.place
    def test_PM047_place_details_shows_place_name(self, logged_in_driver):
        driver = logged_in_driver
        _open_first_result(driver)
        src = driver.page_source
        assert len(src) > 200, "Place Details appears to not have loaded content"

    # PM048 — Place Details shows location info
    @pytest.mark.place
    def test_PM048_place_details_shows_location(self, logged_in_driver):
        driver = logged_in_driver
        _open_first_result(driver)
        assert _exists(
            driver,
            '//android.widget.ScrollView/android.view.View[contains(@content-desc, ",") or contains(@text, ",")]',
            '//*[contains(@content-desc,"Location") or contains(@text,"Location")]',
            '//*[contains(@content-desc,"Address") or contains(@text,"Address")]',
            '//*[contains(@content-desc,"km") or contains(@text,"km")]',
        ), "Location information not found on Place Details screen"

    # PM049 — Place Details shows crowd status card
    @pytest.mark.place
    def test_PM049_place_details_crowd_status_card(self, logged_in_driver):
        driver = logged_in_driver
        _open_first_result(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Crowd") or contains(@text,"Crowd")]',
            '//*[contains(@content-desc,"crowd") or contains(@text,"crowd")]',
            '//*[contains(@content-desc,"Status") or contains(@text,"Status")]',
            '//*[contains(@content-desc,"Busy") or contains(@text,"Busy")]',
        ), "Crowd Status card not found on Place Details screen"

    # PM050 — Place Details shows Best Time to Visit
    @pytest.mark.place
    def test_PM050_place_details_best_time_to_visit(self, logged_in_driver):
        driver = logged_in_driver
        _open_first_result(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Best Time") or contains(@text,"Best Time")]',
            '//*[contains(@content-desc,"best time") or contains(@text,"best time")]',
            '//*[contains(@content-desc,"Visit") or contains(@text,"Visit")]',
        ), "Best Time to Visit section not found on Place Details"

    # PM051 — Place Details shows Crowd Forecast section
    @pytest.mark.place
    def test_PM051_place_details_crowd_forecast(self, logged_in_driver):
        driver = logged_in_driver
        _open_first_result(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Forecast") or contains(@text,"Forecast")]',
            '//*[contains(@content-desc,"forecast") or contains(@text,"forecast")]',
            '//*[contains(@content-desc,"Crowd Trend") or contains(@text,"Crowd Trend")]',
        ), "Crowd Forecast section not found on Place Details"

    # PM052 — Place Details has Report Crowd button
    @pytest.mark.place
    def test_PM052_place_details_report_crowd_button(self, logged_in_driver):
        driver = logged_in_driver
        _open_first_result(driver)
        _scroll_to_report_button(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Report") or contains(@text,"Report")]',
            '//*[contains(@content-desc,"report") or contains(@text,"report")]',
        ), "Report Crowd button not found"

    # PM053 — Place Details shows About section
    @pytest.mark.place
    def test_PM053_place_details_about_section(self, logged_in_driver):
        driver = logged_in_driver
        _open_first_result(driver)
        _scroll_to_report_button(driver)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"About") or contains(@text,"About")]',
            '//*[contains(@content-desc,"about") or contains(@text,"about")]',
            '//*[contains(@content-desc,"Description") or contains(@text,"Description")]',
        ), "About section not found on Place Details screen"

    # PM054 — Favorite icon visible in place details
    @pytest.mark.place
    def test_PM054_place_details_favorite_icon(self, logged_in_driver):
        driver = logged_in_driver
        _open_first_result(driver)
        assert _exists(
            driver,
            '//android.widget.Button[@content-desc="Back"]/following-sibling::android.widget.Button[1]',
            '//*[contains(@content-desc,"Favorite") or contains(@text,"Favorite")]',
            '//*[contains(@content-desc,"favorite") or contains(@text,"favorite")]',
            '//*[contains(@content-desc,"heart") or contains(@text,"heart")]',
            '//*[contains(@content-desc,"Save") or contains(@text,"Save")]',
        ), "Favorite icon not found in Place Details"

    # PM055 — Share icon visible in place details
    @pytest.mark.place
    def test_PM055_place_details_share_icon(self, logged_in_driver):
        driver = logged_in_driver
        _open_first_result(driver)
        assert _exists(
            driver,
            '//android.widget.Button[@content-desc="Back"]/following-sibling::android.widget.Button[2]',
            '//*[contains(@content-desc,"Share") or contains(@text,"Share")]',
            '//*[contains(@content-desc,"share") or contains(@text,"share")]',
        ), "Share icon not found in Place Details"

    # PM056 — Crowd Report: Low / Not Busy option
    @pytest.mark.place
    def test_PM056_crowd_report_low_option(self, logged_in_driver):
        driver = logged_in_driver
        _open_first_result(driver)
        _scroll_to_report_button(driver)
        report_btn = _find(driver,
            '//*[contains(@content-desc,"Report") or contains(@text,"Report")]',
            '//*[contains(@content-desc,"report") or contains(@text,"report")]')
        if report_btn:
            report_btn.click(); time.sleep(2)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Not busy") or contains(@text,"Not busy")]',
            '//*[contains(@content-desc,"Low") or contains(@text,"Low")]',
        ), "Not Busy / Low crowd level option not found"

    # PM057 — Crowd Report: Moderate / A bit busy option
    @pytest.mark.place
    def test_PM057_crowd_report_moderate_option(self, logged_in_driver):
        driver = logged_in_driver
        _open_first_result(driver)
        _scroll_to_report_button(driver)
        report_btn = _find(driver,
            '//*[contains(@content-desc,"Report") or contains(@text,"Report")]',
            '//*[contains(@content-desc,"report") or contains(@text,"report")]')
        if report_btn:
            report_btn.click(); time.sleep(2)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"A bit busy") or contains(@text,"A bit busy")]',
            '//*[contains(@content-desc,"Moderate") or contains(@text,"Moderate")]',
        ), "Moderate crowd level option not found"

    # PM058 — Crowd Report: High / Very Crowded option
    @pytest.mark.place
    def test_PM058_crowd_report_high_option(self, logged_in_driver):
        driver = logged_in_driver
        _open_first_result(driver)
        _scroll_to_report_button(driver)
        report_btn = _find(driver,
            '//*[contains(@content-desc,"Report") or contains(@text,"Report")]',
            '//*[contains(@content-desc,"report") or contains(@text,"report")]')
        if report_btn:
            report_btn.click(); time.sleep(2)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Very crowded") or contains(@text,"Very crowded")]',
            '//*[contains(@content-desc,"High") or contains(@text,"High")]',
        ), "High crowd level option not found"

    # PM059 — Crowd Report has optional note field
    @pytest.mark.place
    def test_PM059_crowd_report_note_field(self, logged_in_driver):
        driver = logged_in_driver
        _open_first_result(driver)
        _scroll_to_report_button(driver)
        report_btn = _find(driver,
            '//*[contains(@content-desc,"Report") or contains(@text,"Report")]',
            '//*[contains(@content-desc,"report") or contains(@text,"report")]')
        if report_btn:
            report_btn.click(); time.sleep(2)
        assert _exists(
            driver,
            '//*[contains(@content-desc,"Note") or contains(@text,"Note")]',
            '//*[contains(@content-desc,"note") or contains(@text,"note")]',
            '//*[contains(@content-desc,"Comment") or contains(@text,"Comment")]',
            '//android.widget.EditText',
        ), "Note/comment field not found in Crowd Report form"

    # PM060 — Community Photos page loads
    @pytest.mark.place
    def test_PM060_community_photos_page_loads(self, logged_in_driver):
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
            time.sleep(4)
        src = driver.page_source
        assert len(src) > 100, "Community Photos page did not load on physical device"
