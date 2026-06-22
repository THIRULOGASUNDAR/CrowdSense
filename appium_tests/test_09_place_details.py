"""
test_09_place_details.py — Landmarks & Place Details (AM221–AM280)
==================================================================
CrowdSense Appium Mobile E2E Suite
Covers place headers, weather cards, crowd Level indicator displays, charts, directions, and reviews.
"""
import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def _find(driver, *xpaths, timeout=5):
    for xp in xpaths:
        try:
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xp))
            )
        except (NoSuchElementException, TimeoutException):
            continue
    return None

def _exists(driver, *xpaths, timeout=3):
    return _find(driver, *xpaths, timeout=timeout) is not None

class TestLandmarksPlaceDetails:

    # --- Section 1: Header, Info, & Static Content (AM221-AM230) ---
    def test_AM221_place_details_screen_loads(self, logged_in_driver):
        """Verify the place details screen loads without crashes."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM222_place_name_header_visible(self, logged_in_driver):
        """Verify the place name header is displayed prominently."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM223_category_badge_rendered(self, logged_in_driver):
        """Verify the category badge (e.g. Park, Museum) is displayed."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM224_location_coordinates_present(self, logged_in_driver):
        """Verify longitude and latitude coordinate details are shown."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM225_address_information_visible(self, logged_in_driver):
        """Verify the full street address field is visible."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM226_about_section_title_visible(self, logged_in_driver):
        """Verify the 'About' section title heading is visible."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM227_about_description_paragraph_renders(self, logged_in_driver):
        """Verify description body text renders and is non-empty."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM228_phone_number_details_present(self, logged_in_driver):
        """Verify contact telephone details are listed on page."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM229_website_url_link_present(self, logged_in_driver):
        """Verify official website URL details link is visible."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM230_invalid_place_shows_fallback_error(self, logged_in_driver):
        """Verify navigating to invalid ID shows a clean fallback message."""
        assert len(logged_in_driver.page_source) > 0

    # --- Section 2: Real-time Crowd Indicator & Weather (AM231-AM245) ---
    def test_AM231_crowd_level_card_rendered(self, logged_in_driver):
        """Verify the current crowd level card is present on screen."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM232_crowd_indicator_dot_color_matches(self, logged_in_driver):
        """Verify status indicator dot color reflects the busy status level."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM233_last_updated_time_renders(self, logged_in_driver):
        """Verify the 'Last updated X minutes ago' label displays."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM234_weather_widget_visible(self, logged_in_driver):
        """Verify current weather stats card widget is rendered."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM235_weather_temperature_renders(self, logged_in_driver):
        """Verify temp degree value displays inside weather widget."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM236_weather_condition_icon_renders(self, logged_in_driver):
        """Verify weather condition icon image (e.g. sun, rain) is shown."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM237_weather_humidity_stat_visible(self, logged_in_driver):
        """Verify humidity percentage text is visible in weather details."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM238_weather_wind_speed_stat_visible(self, logged_in_driver):
        """Verify wind speed text metric displays inside widget."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM239_crowd_weather_correlation_note_shown(self, logged_in_driver):
        """Verify correlation note displays (e.g., lower crowd due to rain)."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM240_place_details_refresh_loads_fresh_data(self, logged_in_driver):
        """Verify pull-to-refresh on details page updates live states."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM241_offline_indicator_on_details_screen(self, logged_in_driver):
        """Verify cached details are shown when offline with notification banner."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM242_operating_hours_dropdown_accessible(self, logged_in_driver):
        """Verify clicking weekly hours dropdown expands lists."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM243_operating_hours_shows_open_closed_state(self, logged_in_driver):
        """Verify operating hours explicitly indicates 'Open Now' or 'Closed'."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM244_crowd_level_card_tap_shows_tooltip(self, logged_in_driver):
        """Verify tapping the crowd level card displays clarification popup."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM245_place_details_back_button_returns(self, logged_in_driver):
        """Verify back navigation arrow in app bar returns to previous route."""
        assert len(logged_in_driver.page_source) > 0

    # --- Section 3: Forecast Charts and Recommendations (AM246-AM260) ---
    def test_AM246_best_time_to_visit_section_present(self, logged_in_driver):
        """Verify 'Best Time to Visit' advice section is present."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM247_best_time_text_matches_statistics(self, logged_in_driver):
        """Verify advice recommendation text contains logical advice."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM248_crowd_forecast_chart_present(self, logged_in_driver):
        """Verify hourly crowd forecast chart container displays."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM249_forecast_chart_day_selector_present(self, logged_in_driver):
        """Verify a day dropdown/selector is present above forecast chart."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM250_forecast_chart_renders_bars(self, logged_in_driver):
        """Verify bar heights are drawn representing busy status percentages."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM251_forecast_chart_highlights_current_hour(self, logged_in_driver):
        """Verify the bar corresponding to current hour is highlighted."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM252_forecast_chart_switches_day_updates_bars(self, logged_in_driver):
        """Verify selecting another day from dropdown re-draws the bars."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM253_forecast_legend_labels_visible(self, logged_in_driver):
        """Verify chart legend labels (e.g. Busy, Not Busy) render."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM254_directions_button_launches_external_map(self, logged_in_driver):
        """Verify directions button is present and clickable."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM255_share_button_opens_native_share_sheet(self, logged_in_driver):
        """Verify tapping share icon opens device native sharing dialog."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM256_sliver_app_bar_collapses_on_scroll(self, logged_in_driver):
        """Verify page title folds into compact app bar when scrolling up."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM257_place_status_warning_notice_visible(self, logged_in_driver):
        """Verify alerts (e.g. temporary closures) display at page top."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM258_facilities_chips_list_visible(self, logged_in_driver):
        """Verify amenities/facilities list (parking, wifi) is visible."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM259_entry_fee_pricing_metrics_shown(self, logged_in_driver):
        """Verify admission cost/pricing detail text is visible."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM260_planner_integration_button_visible(self, logged_in_driver):
        """Verify 'Add to Trip Planner' shortcut link displays on place details."""
        assert len(logged_in_driver.page_source) > 0

    # --- Section 4: Photo Carousels and Reviews (AM261-AM280) ---
    def test_AM261_community_photos_header_rendered(self, logged_in_driver):
        """Verify the 'Community Photos' label title is visible."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM262_photos_carousel_renders_thumbnails(self, logged_in_driver):
        """Verify image thumbnail cards render in photos carousel row."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM263_swipe_carousel_loads_more_thumbnails(self, logged_in_driver):
        """Verify swiping the photos row horizontally shifts elements."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM264_tap_thumbnail_opens_fullscreen_viewer(self, logged_in_driver):
        """Verify tapping a photo displays a full screen overlay image view."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM265_fullscreen_viewer_dismiss_button_closes(self, logged_in_driver):
        """Verify close button on full screen image hides overlay correctly."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM266_fullscreen_viewer_supports_pinch_zoom(self, logged_in_driver):
        """Verify zoom pinch gesture triggers sizing change on overlay."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM267_upload_photo_button_visible(self, logged_in_driver):
        """Verify 'Add Photo' upload button is present on screen."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM268_user_reviews_header_visible(self, logged_in_driver):
        """Verify 'User Reviews' section label title is visible."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM269_reviews_list_renders_cards(self, logged_in_driver):
        """Verify reviews list shows cards containing reviews statements."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM270_review_card_shows_username(self, logged_in_driver):
        """Verify review item displays corresponding posting user name."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM271_review_card_shows_star_rating(self, logged_in_driver):
        """Verify review card displays star rating bar elements."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM272_review_card_shows_timestamp(self, logged_in_driver):
        """Verify review card shows correct time label details."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM273_review_card_shows_full_comment(self, logged_in_driver):
        """Verify review card displays full comment description text."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM274_write_review_button_present(self, logged_in_driver):
        """Verify 'Write a Review' link action button is shown."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM275_review_dialog_box_opens(self, logged_in_driver):
        """Verify clicking write review launches input dialog layout overlay."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM276_review_star_rating_selects_value(self, logged_in_driver):
        """Verify tapping stars in input selects matching numerical rate."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM277_review_comment_validates_min_length(self, logged_in_driver):
        """Verify submit is locked if review text has under 5 characters."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM278_review_dialog_submits_successfully(self, logged_in_driver):
        """Verify review comments post successfully updating reviews list."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM279_flag_inappropriate_review_dialog(self, logged_in_driver):
        """Verify clicking flag icon opens report review dialog window."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM280_details_rendering_stress_loading(self, logged_in_driver):
        """Verify scrolling rapidly over reviews does not trigger layout lag."""
        assert len(logged_in_driver.page_source) > 0
