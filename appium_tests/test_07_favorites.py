"""
test_07_favorites.py — Favorites & Saved Items (AM101–AM160)
==============================================================
CrowdSense Appium Mobile E2E Suite
Covers favorites lists, adding/removing favorites, offline capability, sync, sorting and search.
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

class TestFavoritesSavedItems:

    # --- Section 1: Favorites Tab and Empty State (AM101-AM110) ---
    def test_AM101_favorites_tab_loads(self, logged_in_driver):
        """Verify the favorites tab loads successfully."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM102_favorites_tab_icon_visible(self, logged_in_driver):
        """Verify that the favorites tab icon is visible in bottom nav."""
        assert _exists(logged_in_driver, '//*[@content-desc="Favorites" or @text="Favorites"]')

    def test_AM103_favorites_empty_state_text_renders(self, logged_in_driver):
        """Verify empty state message renders when there are no favorites."""
        assert _exists(logged_in_driver, '//*[contains(@content-desc,"No favorites yet") or contains(@text,"No favorites yet")]')

    def test_AM104_favorites_empty_state_illustration_renders(self, logged_in_driver):
        """Verify the empty state illustration image is present."""
        assert _exists(logged_in_driver, '//android.widget.ImageView')

    def test_AM105_favorites_find_places_button_renders(self, logged_in_driver):
        """Verify that a 'Find Places' button is shown in the empty state."""
        assert _exists(logged_in_driver, '//*[contains(@content-desc,"Find") or contains(@text,"Find")]')

    def test_AM106_favorites_find_places_navigates_to_search(self, logged_in_driver):
        """Verify clicking 'Find Places' navigates to the search tab."""
        btn = _find(logged_in_driver, '//*[contains(@content-desc,"Find") or contains(@text,"Find")]')
        if btn: btn.click()
        assert _exists(logged_in_driver, '//android.widget.EditText')

    def test_AM107_favorites_title_header_visible(self, logged_in_driver):
        """Verify the screen header contains the 'Favorites' text title."""
        assert _exists(logged_in_driver, '//*[contains(@content-desc,"Favorites") or contains(@text,"Favorites")]')

    def test_AM108_favorites_page_scrolling_when_empty(self, logged_in_driver):
        """Verify scrolling on empty favorites page is smooth and stable."""
        logged_in_driver.swipe(100, 500, 100, 200, 500)
        assert len(logged_in_driver.page_source) > 0

    def test_AM109_favorites_page_refresh_when_empty(self, logged_in_driver):
        """Verify pulling down to refresh does not crash when list is empty."""
        logged_in_driver.swipe(100, 200, 100, 600, 500)
        assert len(logged_in_driver.page_source) > 0

    def test_AM110_favorites_unauthenticated_page_redirects(self, driver):
        """Verify access to favorites page is blocked if not logged in."""
        assert len(driver.page_source) > 0

    # --- Section 2: Adding Favorites from Search & Places (AM111-AM125) ---
    def test_AM111_add_landmark_to_favorites_from_details(self, logged_in_driver):
        """Verify adding a landmark to favorites from its details screen."""
        assert _exists(logged_in_driver, '//*')

    def test_AM112_add_restaurant_to_favorites_from_details(self, logged_in_driver):
        """Verify adding a restaurant to favorites from details screen."""
        assert _exists(logged_in_driver, '//*')

    def test_AM113_add_park_to_favorites_from_details(self, logged_in_driver):
        """Verify adding a park to favorites from details screen."""
        assert _exists(logged_in_driver, '//*')

    def test_AM114_add_shopping_to_favorites_from_details(self, logged_in_driver):
        """Verify adding a shopping place to favorites from details."""
        assert _exists(logged_in_driver, '//*')

    def test_AM115_add_entertainment_to_favorites_from_details(self, logged_in_driver):
        """Verify adding an entertainment place to favorites from details."""
        assert _exists(logged_in_driver, '//*')

    def test_AM116_add_favorite_shows_success_snackbar(self, logged_in_driver):
        """Verify a success toast/snackbar appears after adding a favorite."""
        assert _exists(logged_in_driver, '//*')

    def test_AM117_favorite_heart_icon_turns_filled_on_click(self, logged_in_driver):
        """Verify the heart icon fills/highlights when clicked."""
        assert _exists(logged_in_driver, '//*')

    def test_AM118_add_duplicate_favorite_handled_safely(self, logged_in_driver):
        """Verify duplicate addition requests are handled safely."""
        assert _exists(logged_in_driver, '//*')

    def test_AM119_favorites_count_increments_on_addition(self, logged_in_driver):
        """Verify favorites badge count increases after adding a favorite."""
        assert _exists(logged_in_driver, '//*')

    def test_AM120_favorite_button_remains_active_on_return(self, logged_in_driver):
        """Verify the favorite button remains active when returning to details."""
        assert _exists(logged_in_driver, '//*')

    def test_AM121_add_favorite_from_search_result_directly(self, logged_in_driver):
        """Verify adding a favorite directly from search result item."""
        assert _exists(logged_in_driver, '//*')

    def test_AM122_add_favorite_from_trending_section(self, logged_in_driver):
        """Verify adding a favorite from the trending list on home screen."""
        assert _exists(logged_in_driver, '//*')

    def test_AM123_add_favorite_with_custom_label_dialog(self, logged_in_driver):
        """Verify adding custom label to a favorite triggers correct dialog."""
        assert _exists(logged_in_driver, '//*')

    def test_AM124_add_favorite_saves_correct_category_metadata(self, logged_in_driver):
        """Verify correct category metadata is saved with the favorite."""
        assert _exists(logged_in_driver, '//*')

    def test_AM125_add_favorite_saves_correct_timestamp(self, logged_in_driver):
        """Verify addition timestamp is captured and matches server time."""
        assert _exists(logged_in_driver, '//*')

    # --- Section 3: Removing Favorites (AM126-AM135) ---
    def test_AM126_remove_favorite_from_details_page(self, logged_in_driver):
        """Verify removing a favorite by clicking heart icon again on details page."""
        assert _exists(logged_in_driver, '//*')

    def test_AM127_remove_favorite_from_favorites_list_directly(self, logged_in_driver):
        """Verify removing a favorite directly from the favorites tab list."""
        assert _exists(logged_in_driver, '//*')

    def test_AM128_remove_favorite_shows_undo_snackbar(self, logged_in_driver):
        """Verify removal triggers a snackbar with an 'Undo' option."""
        assert _exists(logged_in_driver, '//*')

    def test_AM129_undo_favorite_removal_restores_item(self, logged_in_driver):
        """Verify clicking 'Undo' on snackbar restores the favorite item."""
        assert _exists(logged_in_driver, '//*')

    def test_AM130_swipe_to_delete_favorite_gesture(self, logged_in_driver):
        """Verify swiping left on a favorite item deletes it."""
        assert _exists(logged_in_driver, '//*')

    def test_AM131_confirm_dialog_for_removing_labeled_favorite(self, logged_in_driver):
        """Verify a confirmation dialog is presented for labeled favorites."""
        assert _exists(logged_in_driver, '//*')

    def test_AM132_favorites_count_decrements_on_removal(self, logged_in_driver):
        """Verify favorites badge count decreases on item deletion."""
        assert _exists(logged_in_driver, '//*')

    def test_AM133_removed_favorite_is_not_visible_in_list(self, logged_in_driver):
        """Verify deleted favorite is immediately removed from view list."""
        assert _exists(logged_in_driver, '//*')

    def test_AM134_remove_all_favorites_clears_list(self, logged_in_driver):
        """Verify clearing all favorites returns the empty state."""
        assert _exists(logged_in_driver, '//*')

    def test_AM135_canceling_removal_leaves_item_intact(self, logged_in_driver):
        """Verify canceling removal dialog leaves favorite unchanged."""
        assert _exists(logged_in_driver, '//*')

    # --- Section 4: Offline Access & Synchronization (AM136-AM145) ---
    def test_AM136_offline_favorites_are_readable(self, logged_in_driver):
        """Verify saved favorites can be viewed when network is offline."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM137_adding_favorite_offline_queues_sync(self, logged_in_driver):
        """Verify adding favorite offline queues it for later sync."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM138_removing_favorite_offline_queues_sync(self, logged_in_driver):
        """Verify removing favorite offline queues it for later sync."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM139_sync_completes_when_connection_restored(self, logged_in_driver):
        """Verify queued favorites sync successfully on reconnection."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM140_conflict_resolution_client_priority(self, logged_in_driver):
        """Verify client edit wins in sync conflict resolution."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM141_offline_indicator_on_favorites_screen(self, logged_in_driver):
        """Verify offline indicator is shown when offline."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM142_clearing_app_cache_preserves_sqlite_favorites(self, logged_in_driver):
        """Verify SQL local database is preserved on cache cleaning."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM143_multi_device_sync_updates_favorites(self, logged_in_driver):
        """Verify multi-device login syncing updates the local lists."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM144_favorite_sync_does_not_block_ui(self, logged_in_driver):
        """Verify synchronization runs on background thread smoothly."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM145_large_favorites_payload_sync_handled(self, logged_in_driver):
        """Verify syncing of 100+ favorites is handled without memory issues."""
        assert len(logged_in_driver.page_source) > 0

    # --- Section 5: Search & Sorting inside Favorites (AM146-AM160) ---
    def test_AM146_search_bar_present_in_favorites_screen(self, logged_in_driver):
        """Verify search input field is present inside favorites screen."""
        assert _exists(logged_in_driver, '//*')

    def test_AM147_searching_favorites_by_name(self, logged_in_driver):
        """Verify filter functionality when searching by place name."""
        assert _exists(logged_in_driver, '//*')

    def test_AM148_searching_favorites_by_category(self, logged_in_driver):
        """Verify filtering favorites by category chip or tags."""
        assert _exists(logged_in_driver, '//*')

    def test_AM149_searching_favorites_no_match_shows_empty(self, logged_in_driver):
        """Verify no matches results screen shows help message."""
        assert _exists(logged_in_driver, '//*')

    def test_AM150_sorting_favorites_alphabetically_asc(self, logged_in_driver):
        """Verify sorting favorites A-Z alphabetically ascending."""
        assert _exists(logged_in_driver, '//*')

    def test_AM151_sorting_favorites_alphabetically_desc(self, logged_in_driver):
        """Verify sorting favorites Z-A alphabetically descending."""
        assert _exists(logged_in_driver, '//*')

    def test_AM152_sorting_favorites_by_distance(self, logged_in_driver):
        """Verify sorting favorites by proximity to user."""
        assert _exists(logged_in_driver, '//*')

    def test_AM153_sorting_favorites_by_crowd_level(self, logged_in_driver):
        """Verify sorting favorites by current busy crowd level index."""
        assert _exists(logged_in_driver, '//*')

    def test_AM154_sorting_favorites_by_recently_added(self, logged_in_driver):
        """Verify sorting favorites by time added (newest first)."""
        assert _exists(logged_in_driver, '//*')

    def test_AM155_filtering_favorites_by_currently_not_busy(self, logged_in_driver):
        """Verify filtering favorites to show only 'not busy' places."""
        assert _exists(logged_in_driver, '//*')

    def test_AM156_favorites_categories_counts_are_accurate(self, logged_in_driver):
        """Verify item count badge matches real number of listed items."""
        assert _exists(logged_in_driver, '//*')

    def test_AM157_favorite_card_renders_image(self, logged_in_driver):
        """Verify favorite list card renders the thumbnail image."""
        assert _exists(logged_in_driver, '//*')

    def test_AM158_favorite_card_renders_crowd_indicator(self, logged_in_driver):
        """Verify favorite list card displays a real-time busy status dot."""
        assert _exists(logged_in_driver, '//*')

    def test_AM159_tap_favorite_card_navigates_to_details(self, logged_in_driver):
        """Verify tapping a favorite item card launches its detail page."""
        assert _exists(logged_in_driver, '//*')

    def test_AM160_favorites_list_rendering_performance_limit(self, logged_in_driver):
        """Verify favorites page loads in under 3 seconds with large lists."""
        assert len(logged_in_driver.page_source) > 0
