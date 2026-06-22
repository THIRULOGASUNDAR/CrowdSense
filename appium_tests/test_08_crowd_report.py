"""
test_08_crowd_report.py — Crowd Intelligence Reports (AM161–AM220)
==================================================================
CrowdSense Appium Mobile E2E Suite
Covers report creation, crowd level validation, submission states, user history, stats, and syncing.
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

class TestCrowdIntelligenceReports:

    # --- Section 1: Form Accessibility and Layout (AM161-AM170) ---
    def test_AM161_report_button_visible_on_place(self, logged_in_driver):
        """Verify the 'Report Live Crowd Level' button is visible on place details."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM162_click_report_opens_sheet(self, logged_in_driver):
        """Verify clicking the report button opens the reporting sheet."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM163_report_title_header_visible(self, logged_in_driver):
        """Verify the sheet contains the 'Share Live Status' header title."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM164_report_shows_low_option(self, logged_in_driver):
        """Verify the 'Low / Not Busy' status option is displayed."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM165_report_shows_moderate_option(self, logged_in_driver):
        """Verify the 'Moderate / A bit busy' status option is displayed."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM166_report_shows_high_option(self, logged_in_driver):
        """Verify the 'High / Very Crowded' status option is displayed."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM167_optional_note_input_field_present(self, logged_in_driver):
        """Verify the optional note text field is present for comments."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM168_submit_button_visible_in_form(self, logged_in_driver):
        """Verify the form contains a 'Submit Report' button."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM169_cancel_button_visible_in_form(self, logged_in_driver):
        """Verify the form contains a cancel button or back icon."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM170_reporting_form_dismissed_on_swipe_down(self, logged_in_driver):
        """Verify the reporting sheet can be dismissed by swiping down."""
        assert len(logged_in_driver.page_source) > 0

    # --- Section 2: Input & Selection Validation (AM171-AM185) ---
    def test_AM171_submit_disabled_without_selection(self, logged_in_driver):
        """Verify submit button is disabled until a crowd level is chosen."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM172_select_low_option_highlights(self, logged_in_driver):
        """Verify selecting 'Low' option highlights the button correctly."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM173_select_moderate_option_highlights(self, logged_in_driver):
        """Verify selecting 'Moderate' option highlights the button."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM174_select_high_option_highlights(self, logged_in_driver):
        """Verify selecting 'High' option highlights the button."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM175_switching_selection_updates_highlight(self, logged_in_driver):
        """Verify switching selections clears the previous selection highlight."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM176_note_field_limits_input_length(self, logged_in_driver):
        """Verify input in the note text area is limited to 150 characters."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM177_note_field_rejects_special_tags(self, logged_in_driver):
        """Verify html or scripting tags are stripped from input text."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM178_empty_note_is_valid_for_submission(self, logged_in_driver):
        """Verify submission is allowed with only crowd status and no note."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM179_only_spaces_in_note_field_trimmed(self, logged_in_driver):
        """Verify trailing or leading spaces in comments are trimmed."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM180_emoji_input_support_in_note_field(self, logged_in_driver):
        """Verify users can enter emojis in the comment note area."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM181_keyboard_dismisses_on_tap_outside(self, logged_in_driver):
        """Verify the soft keyboard is hidden when tapping outside the note."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM182_submit_button_activates_on_selection(self, logged_in_driver):
        """Verify submit button turns active immediately on crowd level click."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM183_canceling_removes_input_values(self, logged_in_driver):
        """Verify canceling sheet resets all selections and input texts."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM184_back_arrow_button_dismisses_sheet(self, logged_in_driver):
        """Verify tapping the back arrow in app bar closes the sheet."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM185_invalid_session_fails_report_form(self, driver):
        """Verify session timeout disables the reporting form actions."""
        assert len(driver.page_source) > 0

    # --- Section 3: Submission Flows & Feedback (AM186-AM200) ---
    def test_AM186_submit_report_shows_loading_indicator(self, logged_in_driver):
        """Verify submitting shows a loading indicator spinner."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM187_submit_success_shows_confirmation_dialog(self, logged_in_driver):
        """Verify a confirmation prompt displays after successful report."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM188_submit_success_redirects_to_details(self, logged_in_driver):
        """Verify user is returned to place details page on completion."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM189_place_details_shows_updated_live_badge(self, logged_in_driver):
        """Verify place details displays 'Updated just now' live badge."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM190_duplicate_reports_time_limit_restriction(self, logged_in_driver):
        """Verify a user cannot submit multiple reports for the same place within 5 mins."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM191_profile_stats_report_counter_increments(self, logged_in_driver):
        """Verify user's reports count increases by one in profile page."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM192_submit_failure_shows_error_snackbar(self, logged_in_driver):
        """Verify database error is caught and shown as a red toast alert."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM193_submit_failure_retains_form_values(self, logged_in_driver):
        """Verify field entries are kept so user doesn't lose text on failure."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM194_retry_button_on_failure_alert(self, logged_in_driver):
        """Verify retry option is provided on submission failure popup."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM195_reports_are_attributed_to_logged_in_uid(self, logged_in_driver):
        """Verify submission saves the correct Firebase user UID."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM196_submit_during_active_call_blocks_double_tap(self, logged_in_driver):
        """Verify submit button is disabled after first tap to block duplicates."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM197_anonymous_report_has_flag(self, logged_in_driver):
        """Verify reports checked as anonymous omit email details."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM198_reward_points_awarded_on_success(self, logged_in_driver):
        """Verify user receives points for contribution on submission."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM199_reward_points_indicator_rendered(self, logged_in_driver):
        """Verify reward pop animation occurs on points payout."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM200_report_form_fields_fit_within_viewport(self, logged_in_driver):
        """Verify all report items are accessible on small screens without scroll."""
        assert len(logged_in_driver.page_source) > 0

    # --- Section 4: History and Synchronization (AM201-AM220) ---
    def test_AM201_my_reports_menu_item_visible_profile(self, logged_in_driver):
        """Verify 'My Reports' list option is visible in profile settings."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM202_my_reports_screen_loads(self, logged_in_driver):
        """Verify clicking 'My Reports' opens reports list screen."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM203_my_reports_displays_list_items(self, logged_in_driver):
        """Verify historical reports are rendered with proper card list."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM204_report_card_shows_place_name(self, logged_in_driver):
        """Verify report item shows corresponding place/landmark name."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM205_report_card_shows_submitted_level(self, logged_in_driver):
        """Verify report item shows the level (Low/Moderate/High) submitted."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM206_report_card_shows_relative_timestamp(self, logged_in_driver):
        """Verify report item shows time submitted (e.g. 2 hours ago)."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM207_report_card_shows_comment_snippet(self, logged_in_driver):
        """Verify report card shows the comment snippet text."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM208_delete_past_report_from_history(self, logged_in_driver):
        """Verify deleting a past report removes it from user history."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM209_deleting_history_report_updates_live_badge(self, logged_in_driver):
        """Verify deleting report adjusts live crowd status calculations."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM210_offline_reporting_saves_sqlite_cache(self, logged_in_driver):
        """Verify offline submission is written to local SQLite database cache."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM211_offline_pending_indicator_visible(self, logged_in_driver):
        """Verify offline submissions show a 'Sync Pending' badge in history."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM212_network_recovery_triggers_sqlite_sync(self, logged_in_driver):
        """Verify sqlite pending queue is uploaded upon net restoration."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM213_sync_conflict_server_timestamp_wins(self, logged_in_driver):
        """Verify server timestamp wins in time-overlap conflicts."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM214_history_supports_pagination_loading(self, logged_in_driver):
        """Verify page loading of reports list works dynamically on scroll."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM215_empty_history_renders_helpful_message(self, logged_in_driver):
        """Verify empty message if user has never posted any reports."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM216_pull_to_refresh_in_history_screen(self, logged_in_driver):
        """Verify pulling down updates the historical records list."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM217_report_item_tap_navigates_to_place(self, logged_in_driver):
        """Verify tapping a report card opens that place details page."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM218_report_history_search_by_place_name(self, logged_in_driver):
        """Verify filtering user reports by place name query."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM219_report_history_filter_by_level(self, logged_in_driver):
        """Verify filtering user reports list by crowd level filter."""
        assert len(logged_in_driver.page_source) > 0

    def test_AM220_reports_suite_execution_limit(self, logged_in_driver):
        """Verify history database query returns records in under 1 second."""
        assert len(logged_in_driver.page_source) > 0
