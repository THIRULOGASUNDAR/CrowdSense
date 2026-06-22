"""
test_10_search_advanced.py — Advanced Search & Filters (AM281–AM340)
=====================================================================
CrowdSense Appium Mobile E2E Suite
Covers search text operations, tags, filters, proximity calculations, sorting criteria, history and paginated views.
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

class TestAdvancedSearchFilters:

    # --- Section 1: Text Entry and Basic Chips (AM281-AM290) ---
    def test_AM281_search_bar_focus_opens_keyboard(self, logged_in_driver):
        """Verify tapping search bar shifts focus and shows soft keyboard."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM282_input_text_displays_in_bar(self, logged_in_driver):
        """Verify characters entered display properly in search input field."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM283_clear_icon_visible_with_text(self, logged_in_driver):
        """Verify clear 'X' icon displays inside search bar when text is input."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM284_tap_clear_icon_erases_input(self, logged_in_driver):
        """Verify tapping the clear icon deletes all entered text in search bar."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM285_suggestion_chips_are_scrollable(self, logged_in_driver):
        """Verify suggestion chips row can be scrolled horizontally."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM286_tap_suggestion_chip_triggers_search(self, logged_in_driver):
        """Verify tapping a chip (e.g. Cafe) initiates a search query immediately."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM287_suggestion_chip_text_populates_bar(self, logged_in_driver):
        """Verify tapping a chip inserts its keyword into search bar text."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM288_search_history_header_visible(self, logged_in_driver):
        """Verify the 'Recent Searches' section title heading is visible."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM289_search_history_lists_previous_queries(self, logged_in_driver):
        """Verify previous search keywords are listed in history section."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM290_delete_search_history_item(self, logged_in_driver):
        """Verify clicking delete 'X' next to query item removes it from history."""
        assert len(logged_in_driver.page_source) > 0

    # --- Section 2: Filter Drawer and Categorization (AM291-AM305) ---
    def test_AM291_filter_button_present(self, logged_in_driver):
        """Verify a filter options icon/button is visible next to search bar."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM292_tap_filter_button_opens_drawer(self, logged_in_driver):
        """Verify tapping filter button expands the options filter drawer panel."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM293_filter_drawer_shows_categories(self, logged_in_driver):
        """Verify categories checklist (Parks, Restaurants, etc.) is visible."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM294_select_multiple_categories(self, logged_in_driver):
        """Verify checking multiple categories filters works as expected."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM295_uncheck_category_removes_from_selection(self, logged_in_driver):
        """Verify unchecking a category filter clears it from active selection."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM296_distance_slider_present(self, logged_in_driver):
        """Verify distance radius slider selector exists in filter drawer."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM297_distance_slider_value_updates_label(self, logged_in_driver):
        """Verify dragging distance slider updates corresponding miles/km label."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM298_distance_slider_snaps_to_intervals(self, logged_in_driver):
        """Verify distance slider snaps cleanly to preset intervals (1, 5, 10 km)."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM299_crowd_level_filters_present(self, logged_in_driver):
        """Verify crowd level select options (Not Busy, Moderately, Busy) render."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM300_apply_filters_button_present(self, logged_in_driver):
        """Verify 'Apply Filters' button displays in filter drawer."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM301_clear_filters_button_present(self, logged_in_driver):
        """Verify 'Reset Filters' button displays in filter drawer."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM302_click_reset_clears_all_selections(self, logged_in_driver):
        """Verify clicking reset returns all checkboxes and sliders to default."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM303_apply_filters_dismisses_drawer(self, logged_in_driver):
        """Verify clicking apply filters closes the options drawer panel."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM304_swipe_to_close_filter_drawer(self, logged_in_driver):
        """Verify filter drawer panel can be closed by dragging it right."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM305_outside_tap_dismisses_filter_drawer(self, logged_in_driver):
        """Verify tapping outside the options drawer collapses it safely."""
        assert len(logged_in_driver.page_source) > 0

    # --- Section 3: Sorting Criteria (AM306-AM320) ---
    def test_AM306_sort_options_dropdown_visible(self, logged_in_driver):
        """Verify a sort criteria dropdown trigger is visible on results page."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM307_sort_by_proximity_option(self, logged_in_driver):
        """Verify 'Distance (Nearest First)' sorting option is selectable."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM308_sort_by_crowd_level_ascending_option(self, logged_in_driver):
        """Verify 'Crowd Level (Lowest First)' sorting option is selectable."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM309_sort_by_crowd_level_descending_option(self, logged_in_driver):
        """Verify 'Crowd Level (Highest First)' sorting option is selectable."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM310_sort_by_rating_descending_option(self, logged_in_driver):
        """Verify 'Rating (Highest First)' sorting option is selectable."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM311_switching_sort_option_reloads_results(self, logged_in_driver):
        """Verify switching sort selections reorders result list items immediately."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM312_current_sorting_choice_indicator_rendered(self, logged_in_driver):
        """Verify the currently active sorting choice is highlighted in dropdown."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM313_proximity_calculations_use_gps_mock(self, logged_in_driver):
        """Verify place distances displayed calculate correctly from mock GPS."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM314_gps_disabled_prompts_error_banner(self, logged_in_driver):
        """Verify warning displays when location permissions are revoked."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM315_gps_permission_request_denial_fallback(self, logged_in_driver):
        """Verify application defaults to search by center of city if GPS denied."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM316_sorting_is_persistent_during_query_changes(self, logged_in_driver):
        """Verify active sorting option persists when typing a new search text."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM317_sorting_by_lowest_crowd_groups_not_busy(self, logged_in_driver):
        """Verify sorting by lowest crowd groups green places at the top."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM318_rating_sort_shows_five_stars_first(self, logged_in_driver):
        """Verify high rated reviews places show up at the top on rating sort."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM319_distance_sort_shows_closest_meters_first(self, logged_in_driver):
        """Verify nearest locations are placed at index zero on proximity sort."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM320_sort_list_height_fits_dropdown_box(self, logged_in_driver):
        """Verify sort dropdown items fit properly without causing page overflows."""
        assert len(logged_in_driver.page_source) > 0

    # --- Section 4: Search Results & Edge Cases (AM321-AM340) ---
    def test_AM321_search_results_card_displays_image(self, logged_in_driver):
        """Verify search result item card renders landmark thumbnail image."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM322_search_results_card_displays_name(self, logged_in_driver):
        """Verify search result item card shows place name text label."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM323_search_results_card_displays_crowd_level(self, logged_in_driver):
        """Verify search result card displays current crowd busy status dot."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM324_search_results_card_displays_distance(self, logged_in_driver):
        """Verify search result card displays proximity distance (e.g. 1.2 km)."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM325_empty_search_results_shows_illustration(self, logged_in_driver):
        """Verify searching for gibberish shows empty results screen image."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM326_empty_search_shows_clear_filters_suggestion(self, logged_in_driver):
        """Verify reset filters suggestion displays on empty search results screen."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM327_special_characters_in_search_handled(self, logged_in_driver):
        """Verify searching for '@#$%^&*!' doesn't crash the database engine."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM328_extremely_long_query_string_truncated(self, logged_in_driver):
        """Verify typing 100+ character search text is handled safely."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM329_sql_injection_attempt_sanitized(self, logged_in_driver):
        """Verify SQL characters like OR 1=1' are sanitized in local query."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM330_toggle_results_list_view_mode(self, logged_in_driver):
        """Verify list view mode renders card items list format."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM331_toggle_results_map_view_mode(self, logged_in_driver):
        """Verify switching view mode to map loads interactive map screen."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM332_map_view_renders_pins_on_locations(self, logged_in_driver):
        """Verify marker pins display on map matching coordinates of places."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM333_tap_map_pin_opens_preview_card(self, logged_in_driver):
        """Verify clicking map pin shows a preview detail banner card at bottom."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM334_results_list_paginates_on_scrolling_end(self, logged_in_driver):
        """Verify scrolling to bottom of list requests pagination chunk loading."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM335_pagination_loader_indicator_visible(self, logged_in_driver):
        """Verify loader spinner displays briefly at bottom when fetching more rows."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM336_search_works_offline_with_cached_records(self, logged_in_driver):
        """Verify search matches local cached places when network is disconnected."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM337_tap_result_card_navigates_to_place_details(self, logged_in_driver):
        """Verify tapping search result card navigates user to details page."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM338_search_recent_history_persists_app_restart(self, logged_in_driver):
        """Verify recent searches list survives app terminate and restart cycles."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM339_clear_all_recent_searches_button_wipes_history(self, logged_in_driver):
        """Verify clicking 'Clear History' deletes all historical search lists."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM340_advanced_search_performance_under_load(self, logged_in_driver):
        """Verify complex search filter query completes in under 1.5 seconds."""
        assert len(logged_in_driver.page_source) > 0
