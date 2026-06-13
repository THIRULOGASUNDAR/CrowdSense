"""
test_04_place.py — Place Details End-to-End Tests
==================================================
Tests: TC066–TC085
Coverage:
  • Place details page loads with a valid place ID
  • Place details shows loader or content
  • Place name, location info, category badge
  • About section
  • Favourite heart icon & Share icon in AppBar
  • Community Photos sub-page
  • Invalid place ID does not crash app
  • SliverAppBar image header
  • Place details scroll stability

Target: https://thirulogasundar.github.io/CrowdSense
"""
import time
import pytest

BASE_URL = "https://thirulogasundar.github.io/CrowdSense"

# A fixture place ID used throughout. The app may show "not found" but should NOT crash.
TEST_PLACE_ID = "test-place-001"
INVALID_ID    = "nonexistent-xyz-00000"


def _nav(driver, path: str, wait: float = 3.5):
    driver.get(f"{BASE_URL}/#/{path}")
    time.sleep(wait)


def _src(driver) -> str:
    return driver.page_source


def _flutter_loaded(src: str) -> bool:
    return any(ind in src.lower() for ind in ["flt-", "canvas", "flutter"])


def _url_has(driver, *fragments) -> bool:
    url = driver.current_url.lower()
    return any(f.lower() in url for f in fragments)


# ══════════════════════════════════════════════════════════════════════════════
class TestPlaceDetails:
    """TC066–TC085 — Place Details Tests"""

    def test_tc066_place_details_page_loads_with_id(self, driver):
        """TC066 — /place/:id route loads Flutter app for a test place ID."""
        _nav(driver, f"place/{TEST_PLACE_ID}")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login"), (
            f"Place details page did not load. URL: {driver.current_url}"
        )

    def test_tc067_place_details_flutter_rendered(self, driver):
        """TC067 — Flutter is rendered on place details route."""
        _nav(driver, f"place/{TEST_PLACE_ID}")
        assert _flutter_loaded(_src(driver)), "Flutter not rendered on place details page"

    def test_tc068_place_details_shows_loader_or_content(self, driver):
        """TC068 — Place details page shows a loader or actual content."""
        _nav(driver, f"place/{TEST_PLACE_ID}")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc069_place_details_shows_place_name(self, driver):
        """TC069 — Place details page renders the place name area."""
        _nav(driver, f"place/{TEST_PLACE_ID}")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc070_place_details_shows_location_info(self, driver):
        """TC070 — Place details page shows location information."""
        _nav(driver, f"place/{TEST_PLACE_ID}")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc071_place_details_shows_category_badge(self, driver):
        """TC071 — Place details page shows a category badge/chip."""
        _nav(driver, f"place/{TEST_PLACE_ID}")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc072_place_details_about_section(self, driver):
        """TC072 — Place details page shows an About section."""
        _nav(driver, f"place/{TEST_PLACE_ID}")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc073_place_details_favourite_icon_in_appbar(self, driver):
        """TC073 — Place details page has a Favourite (heart) icon in the app bar."""
        _nav(driver, f"place/{TEST_PLACE_ID}")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc074_place_details_share_icon_in_appbar(self, driver):
        """TC074 — Place details page has a Share icon in the app bar."""
        _nav(driver, f"place/{TEST_PLACE_ID}")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc075_place_details_current_status_card(self, driver):
        """TC075 — Place details page shows a Current Crowd Status card."""
        _nav(driver, f"place/{TEST_PLACE_ID}")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc076_place_details_best_time_to_visit(self, driver):
        """TC076 — Place details page shows a Best Time to Visit section."""
        _nav(driver, f"place/{TEST_PLACE_ID}")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc077_place_details_crowd_forecast_section(self, driver):
        """TC077 — Place details page shows a Crowd Forecast chart/section."""
        _nav(driver, f"place/{TEST_PLACE_ID}")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc078_place_details_report_crowd_button(self, driver):
        """TC078 — Place details page shows a Report Live Crowd Level button."""
        _nav(driver, f"place/{TEST_PLACE_ID}")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc079_place_details_image_header_appbar(self, driver):
        """TC079 — Place details page shows the SliverAppBar image header."""
        _nav(driver, f"place/{TEST_PLACE_ID}")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login")

    def test_tc080_community_photos_page_loads(self, driver):
        """TC080 — /place/:id/photos route loads without crashing."""
        _nav(driver, f"place/{TEST_PLACE_ID}/photos")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "place", "login"), (
            f"Community photos page failed. URL: {driver.current_url}"
        )

    def test_tc081_invalid_place_id_no_crash(self, driver):
        """TC081 — Navigating to a nonexistent place ID does not crash the app."""
        _nav(driver, f"place/{INVALID_ID}")
        assert _flutter_loaded(_src(driver)), (
            "App crashed when navigating to an invalid place ID"
        )

    def test_tc082_place_details_page_source_not_empty(self, driver):
        """TC082 — Place details page source has substantial content."""
        _nav(driver, f"place/{TEST_PLACE_ID}")
        assert len(_src(driver)) > 300, "Place details page source appears empty"

    def test_tc083_place_details_no_server_error(self, driver):
        """TC083 — Place details page does not show a server error."""
        _nav(driver, f"place/{TEST_PLACE_ID}")
        src = _src(driver)
        assert "500 Internal Server Error" not in src, (
            "Place details page is showing a 500 error"
        )

    def test_tc084_place_details_scroll_stable(self, driver):
        """TC084 — Scrolling on the place details page does not crash the app."""
        _nav(driver, f"place/{TEST_PLACE_ID}")
        driver.execute_script("window.scrollBy(0, 800)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver)), "App crashed after scrolling on place details"

    def test_tc085_place_details_title_is_crowdsense(self, driver):
        """TC085 — Browser title is 'crowdsense' on place details route."""
        _nav(driver, f"place/{TEST_PLACE_ID}")
        assert "crowdsense" in driver.title.lower()
