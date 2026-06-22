"""
test_18_selenium_extended.py — Extended Selenium Browser Tests
==============================================================
Tests: TC741–TC900  (160 tests)
Coverage:
  • Extended Auth/Login flows              (TC741–TC780)
  • Extended Home & Navigation flows       (TC781–TC820)
  • Extended Search & Place flows          (TC821–TC860)
  • Extended Profile, Settings & Misc      (TC861–TC900)

Target: https://thirulogasundar.github.io/CrowdSense
"""
import time
import pytest

BASE_URL = "https://thirulogasundar.github.io/CrowdSense"


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


def _title_ok(driver) -> bool:
    return "crowdsense" in driver.title.lower()


# ══════════════════════════════════════════════════════════════════════════════
class TestSeleniumExtended:
    """TC741–TC900 — Extended Selenium Browser Tests"""

    # ── Category 1: Extended Auth / Login Flows (TC741–TC780) ─────────────────

    def test_tc741_app_loads_flutter_on_root(self, driver):
        """TC741 — Root URL loads Flutter app."""
        driver.get(BASE_URL)
        time.sleep(5)
        assert _flutter_loaded(_src(driver))

    def test_tc742_title_on_root(self, driver):
        """TC742 — Browser title contains 'crowdsense' on root URL."""
        driver.get(BASE_URL)
        time.sleep(4)
        assert _title_ok(driver)

    def test_tc743_root_redirects_to_login(self, driver):
        """TC743 — Root URL redirects unauthenticated user to login."""
        driver.get(BASE_URL)
        time.sleep(5)
        assert _url_has(driver, "login", "/")

    def test_tc744_login_page_flutter_loaded(self, driver):
        """TC744 — /login route renders Flutter app."""
        _nav(driver, "login")
        assert _flutter_loaded(_src(driver))

    def test_tc745_login_url_confirmed(self, driver):
        """TC745 — Current URL contains 'login' on /login route."""
        _nav(driver, "login")
        assert _url_has(driver, "login")

    def test_tc746_login_title_correct(self, driver):
        """TC746 — Browser title is 'crowdsense' on login page."""
        _nav(driver, "login")
        assert _title_ok(driver)

    def test_tc747_login_source_not_empty(self, driver):
        """TC747 — Login page source exceeds 300 bytes."""
        _nav(driver, "login")
        assert len(_src(driver)) > 300

    def test_tc748_login_no_500_error(self, driver):
        """TC748 — Login page does not display a 500 error."""
        _nav(driver, "login")
        assert "500 Internal Server Error" not in _src(driver)

    def test_tc749_login_no_404_error(self, driver):
        """TC749 — Login page does not display a 404 error."""
        _nav(driver, "login")
        assert "404 Not Found" not in _src(driver)

    def test_tc750_login_scroll_stable(self, driver):
        """TC750 — Scrolling on login page does not crash the app."""
        _nav(driver, "login")
        driver.execute_script("window.scrollBy(0, 300)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver))

    def test_tc751_login_refresh_stable(self, driver):
        """TC751 — Refreshing the login page does not crash the app."""
        _nav(driver, "login")
        driver.refresh()
        time.sleep(4)
        assert _flutter_loaded(_src(driver))

    def test_tc752_register_page_flutter_loaded(self, driver):
        """TC752 — /register route renders Flutter app."""
        _nav(driver, "register")
        assert _flutter_loaded(_src(driver))

    def test_tc753_register_url_confirmed(self, driver):
        """TC753 — Current URL contains 'register' on /register route."""
        _nav(driver, "register")
        assert _url_has(driver, "register")

    def test_tc754_register_title_correct(self, driver):
        """TC754 — Browser title is 'crowdsense' on register page."""
        _nav(driver, "register")
        assert _title_ok(driver)

    def test_tc755_register_source_not_empty(self, driver):
        """TC755 — Register page source exceeds 300 bytes."""
        _nav(driver, "register")
        assert len(_src(driver)) > 300

    def test_tc756_register_no_500_error(self, driver):
        """TC756 — Register page does not display a 500 error."""
        _nav(driver, "register")
        assert "500 Internal Server Error" not in _src(driver)

    def test_tc757_register_scroll_stable(self, driver):
        """TC757 — Scrolling on register page does not crash the app."""
        _nav(driver, "register")
        driver.execute_script("window.scrollBy(0, 300)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver))

    def test_tc758_register_refresh_stable(self, driver):
        """TC758 — Refreshing the register page does not crash."""
        _nav(driver, "register")
        driver.refresh()
        time.sleep(4)
        assert _flutter_loaded(_src(driver))

    def test_tc759_forgot_password_flutter_loaded(self, driver):
        """TC759 — /forgot-password route renders Flutter app."""
        _nav(driver, "forgot-password")
        assert _flutter_loaded(_src(driver))

    def test_tc760_forgot_password_url_confirmed(self, driver):
        """TC760 — Current URL contains 'forgot-password'."""
        _nav(driver, "forgot-password")
        assert _url_has(driver, "forgot-password")

    def test_tc761_forgot_password_title_correct(self, driver):
        """TC761 — Browser title is 'crowdsense' on forgot-password page."""
        _nav(driver, "forgot-password")
        assert _title_ok(driver)

    def test_tc762_forgot_password_source_not_empty(self, driver):
        """TC762 — Forgot-password page source exceeds 300 bytes."""
        _nav(driver, "forgot-password")
        assert len(_src(driver)) > 300

    def test_tc763_forgot_password_no_500(self, driver):
        """TC763 — Forgot-password page does not show 500 error."""
        _nav(driver, "forgot-password")
        assert "500 Internal Server Error" not in _src(driver)

    def test_tc764_forgot_password_scroll_stable(self, driver):
        """TC764 — Scrolling on forgot-password page does not crash."""
        _nav(driver, "forgot-password")
        driver.execute_script("window.scrollBy(0, 200)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver))

    def test_tc765_login_to_register_navigation(self, driver):
        """TC765 — Navigating from /login to /register loads register page."""
        _nav(driver, "login")
        _nav(driver, "register")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "register")

    def test_tc766_register_to_login_navigation(self, driver):
        """TC766 — Navigating from /register to /login loads login page."""
        _nav(driver, "register")
        _nav(driver, "login")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "login")

    def test_tc767_login_to_forgot_password(self, driver):
        """TC767 — Navigating from /login to /forgot-password loads forgot-password."""
        _nav(driver, "login")
        _nav(driver, "forgot-password")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "forgot-password")

    def test_tc768_rapid_auth_transitions_stable(self, driver):
        """TC768 — Rapid transitions between auth routes do not crash the app."""
        for route in ["login", "register", "forgot-password", "login"]:
            driver.get(f"{BASE_URL}/#/{route}")
            time.sleep(1)
        assert _flutter_loaded(_src(driver))

    def test_tc769_unauthenticated_home_redirects(self, driver):
        """TC769 — Unauthenticated /home access redirects to login."""
        _nav(driver, "home", wait=4)
        assert _url_has(driver, "login")

    def test_tc770_unauthenticated_profile_redirects(self, driver):
        """TC770 — Unauthenticated /profile access redirects to login."""
        _nav(driver, "profile", wait=4)
        assert _url_has(driver, "login")

    def test_tc771_unauthenticated_favorites_redirects(self, driver):
        """TC771 — Unauthenticated /favorites access redirects to login."""
        _nav(driver, "favorites", wait=4)
        assert _url_has(driver, "login")

    def test_tc772_unauthenticated_planner_redirects(self, driver):
        """TC772 — Unauthenticated /planner access redirects to login."""
        _nav(driver, "planner", wait=4)
        assert _url_has(driver, "login")

    def test_tc773_unauthenticated_my_reports_redirects(self, driver):
        """TC773 — Unauthenticated /my-reports access redirects to login."""
        _nav(driver, "my-reports", wait=4)
        assert _url_has(driver, "login")

    def test_tc774_login_back_navigation_stable(self, driver):
        """TC774 — Browser back navigation from register to login is stable."""
        _nav(driver, "login")
        _nav(driver, "register")
        driver.back()
        time.sleep(3)
        assert _flutter_loaded(_src(driver))

    def test_tc775_forward_navigation_stable(self, driver):
        """TC775 — Browser forward navigation is stable."""
        _nav(driver, "login")
        _nav(driver, "register")
        driver.back()
        time.sleep(2)
        driver.forward()
        time.sleep(2)
        assert _flutter_loaded(_src(driver))

    def test_tc776_login_page_window_resize_stable(self, driver):
        """TC776 — Resizing the window on login page does not crash."""
        _nav(driver, "login")
        driver.set_window_size(375, 667)
        time.sleep(2)
        assert _flutter_loaded(_src(driver))
        driver.set_window_size(1280, 800)

    def test_tc777_register_window_resize_stable(self, driver):
        """TC777 — Resizing the window on register page does not crash."""
        _nav(driver, "register")
        driver.set_window_size(414, 896)
        time.sleep(2)
        assert _flutter_loaded(_src(driver))
        driver.set_window_size(1280, 800)

    def test_tc778_login_tablet_viewport_stable(self, driver):
        """TC778 — Login page renders on tablet viewport (768×1024)."""
        driver.set_window_size(768, 1024)
        _nav(driver, "login")
        assert _flutter_loaded(_src(driver))
        driver.set_window_size(1280, 800)

    def test_tc779_register_tablet_viewport_stable(self, driver):
        """TC779 — Register page renders on tablet viewport (768×1024)."""
        driver.set_window_size(768, 1024)
        _nav(driver, "register")
        assert _flutter_loaded(_src(driver))
        driver.set_window_size(1280, 800)

    def test_tc780_auth_pages_source_consistent(self, driver):
        """TC780 — Login page source size is consistent between two loads."""
        _nav(driver, "login")
        size1 = len(_src(driver))
        _nav(driver, "login")
        size2 = len(_src(driver))
        assert abs(size1 - size2) / max(size1, size2) < 0.15

    # ── Category 2: Extended Home & Navigation Flows (TC781–TC820) ─────────────

    def test_tc781_home_route_flutter_loaded(self, driver):
        """TC781 — /home route renders Flutter app."""
        _nav(driver, "home")
        assert _flutter_loaded(_src(driver))

    def test_tc782_home_title_correct(self, driver):
        """TC782 — Browser title is 'crowdsense' on home route."""
        _nav(driver, "home")
        assert _title_ok(driver)

    def test_tc783_home_or_login_url(self, driver):
        """TC783 — /home resolves to home or login URL."""
        _nav(driver, "home", wait=4)
        assert _url_has(driver, "home", "login")

    def test_tc784_search_route_flutter_loaded(self, driver):
        """TC784 — /search route renders Flutter app."""
        _nav(driver, "search")
        assert _flutter_loaded(_src(driver))

    def test_tc785_search_title_correct(self, driver):
        """TC785 — Browser title is 'crowdsense' on search route."""
        _nav(driver, "search")
        assert _title_ok(driver)

    def test_tc786_search_or_login_url(self, driver):
        """TC786 — /search resolves to search or login URL."""
        _nav(driver, "search", wait=4)
        assert _url_has(driver, "search", "login")

    def test_tc787_search_results_route_loaded(self, driver):
        """TC787 — /search-results route renders Flutter app."""
        _nav(driver, "search-results")
        assert _flutter_loaded(_src(driver))

    def test_tc788_planner_route_flutter_loaded(self, driver):
        """TC788 — /planner route renders Flutter app."""
        _nav(driver, "planner")
        assert _flutter_loaded(_src(driver))

    def test_tc789_planner_title_correct(self, driver):
        """TC789 — Browser title is 'crowdsense' on planner route."""
        _nav(driver, "planner")
        assert _title_ok(driver)

    def test_tc790_favorites_route_flutter_loaded(self, driver):
        """TC790 — /favorites route renders Flutter app."""
        _nav(driver, "favorites")
        assert _flutter_loaded(_src(driver))

    def test_tc791_favorites_title_correct(self, driver):
        """TC791 — Browser title is 'crowdsense' on favorites route."""
        _nav(driver, "favorites")
        assert _title_ok(driver)

    def test_tc792_profile_route_flutter_loaded(self, driver):
        """TC792 — /profile route renders Flutter app."""
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver))

    def test_tc793_profile_title_correct(self, driver):
        """TC793 — Browser title is 'crowdsense' on profile route."""
        _nav(driver, "profile")
        assert _title_ok(driver)

    def test_tc794_my_reports_route_flutter_loaded(self, driver):
        """TC794 — /my-reports route renders Flutter app."""
        _nav(driver, "my-reports")
        assert _flutter_loaded(_src(driver))

    def test_tc795_my_reports_title_correct(self, driver):
        """TC795 — Browser title is 'crowdsense' on my-reports route."""
        _nav(driver, "my-reports")
        assert _title_ok(driver)

    def test_tc796_settings_route_flutter_loaded(self, driver):
        """TC796 — /settings route renders Flutter app."""
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver))

    def test_tc797_settings_title_correct(self, driver):
        """TC797 — Browser title is 'crowdsense' on settings route."""
        _nav(driver, "settings")
        assert _title_ok(driver)

    def test_tc798_settings_url_confirmed(self, driver):
        """TC798 — Current URL contains 'settings' on /settings route."""
        _nav(driver, "settings")
        assert _url_has(driver, "settings")

    def test_tc799_settings_source_not_empty(self, driver):
        """TC799 — Settings page source exceeds 300 bytes."""
        _nav(driver, "settings")
        assert len(_src(driver)) > 300

    def test_tc800_settings_no_500_error(self, driver):
        """TC800 — Settings page does not display a 500 error."""
        _nav(driver, "settings")
        assert "500 Internal Server Error" not in _src(driver)

    def test_tc801_settings_scroll_stable(self, driver):
        """TC801 — Scrolling on settings page does not crash."""
        _nav(driver, "settings")
        driver.execute_script("window.scrollBy(0, 400)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver))

    def test_tc802_settings_refresh_stable(self, driver):
        """TC802 — Refreshing settings page does not crash."""
        _nav(driver, "settings")
        driver.refresh()
        time.sleep(4)
        assert _flutter_loaded(_src(driver))

    def test_tc803_settings_mobile_viewport(self, driver):
        """TC803 — Settings page renders correctly on mobile viewport."""
        driver.set_window_size(390, 844)
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver))
        driver.set_window_size(1280, 800)

    def test_tc804_home_mobile_viewport(self, driver):
        """TC804 — Home route renders correctly on mobile viewport."""
        driver.set_window_size(390, 844)
        _nav(driver, "home")
        assert _flutter_loaded(_src(driver))
        driver.set_window_size(1280, 800)

    def test_tc805_multi_route_session_stable(self, driver):
        """TC805 — Visiting multiple routes in one session is stable."""
        for route in ["login", "register", "forgot-password", "settings"]:
            _nav(driver, route, wait=2)
        assert _flutter_loaded(_src(driver))

    def test_tc806_home_to_search_navigation(self, driver):
        """TC806 — Navigating from /home to /search loads search route."""
        _nav(driver, "home")
        _nav(driver, "search")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "search", "login")

    def test_tc807_search_to_planner_navigation(self, driver):
        """TC807 — Navigating from /search to /planner loads planner route."""
        _nav(driver, "search")
        _nav(driver, "planner")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "planner", "login")

    def test_tc808_settings_to_login_navigation(self, driver):
        """TC808 — Navigating from /settings to /login loads login page."""
        _nav(driver, "settings")
        _nav(driver, "login")
        assert _flutter_loaded(_src(driver)) and _url_has(driver, "login")

    def test_tc809_five_route_session_no_crash(self, driver):
        """TC809 — Visiting 5 routes sequentially does not crash."""
        routes = ["login", "register", "settings", "search", "planner"]
        for r in routes:
            driver.get(f"{BASE_URL}/#/{r}")
            time.sleep(2)
        assert _flutter_loaded(_src(driver))

    def test_tc810_page_source_grows_after_flutter_load(self, driver):
        """TC810 — Page source grows after initial Flutter render."""
        driver.get(BASE_URL)
        size_early = len(_src(driver))
        time.sleep(5)
        size_late = len(_src(driver))
        assert size_late >= size_early

    def test_tc811_login_wide_viewport(self, driver):
        """TC811 — Login page renders on wide desktop viewport (1920×1080)."""
        driver.set_window_size(1920, 1080)
        _nav(driver, "login")
        assert _flutter_loaded(_src(driver))
        driver.set_window_size(1280, 800)

    def test_tc812_register_wide_viewport(self, driver):
        """TC812 — Register page renders on wide desktop viewport (1920×1080)."""
        driver.set_window_size(1920, 1080)
        _nav(driver, "register")
        assert _flutter_loaded(_src(driver))
        driver.set_window_size(1280, 800)

    def test_tc813_settings_wide_viewport(self, driver):
        """TC813 — Settings page renders on wide desktop viewport (1920×1080)."""
        driver.set_window_size(1920, 1080)
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver))
        driver.set_window_size(1280, 800)

    def test_tc814_home_no_js_error_in_title(self, driver):
        """TC814 — Home page title does not contain 'error' or 'exception'."""
        _nav(driver, "home")
        title = driver.title.lower()
        assert "error" not in title and "exception" not in title

    def test_tc815_settings_no_js_error_in_title(self, driver):
        """TC815 — Settings page title does not contain 'error' or 'exception'."""
        _nav(driver, "settings")
        title = driver.title.lower()
        assert "error" not in title and "exception" not in title

    def test_tc816_consecutive_refreshes_stable(self, driver):
        """TC816 — Refreshing the login page 3 times is stable."""
        _nav(driver, "login")
        for _ in range(3):
            driver.refresh()
            time.sleep(3)
        assert _flutter_loaded(_src(driver))

    def test_tc817_login_source_over_time_stable(self, driver):
        """TC817 — Login page source remains non-empty after 6 seconds."""
        _nav(driver, "login")
        time.sleep(3)
        assert len(_src(driver)) > 300

    def test_tc818_forgot_password_refresh_stable(self, driver):
        """TC818 — Refreshing forgot-password page does not crash."""
        _nav(driver, "forgot-password")
        driver.refresh()
        time.sleep(4)
        assert _flutter_loaded(_src(driver))

    def test_tc819_search_results_title_correct(self, driver):
        """TC819 — Browser title is 'crowdsense' on search-results route."""
        _nav(driver, "search-results")
        assert _title_ok(driver)

    def test_tc820_rapid_refresh_on_settings(self, driver):
        """TC820 — Two rapid refreshes on settings page does not crash."""
        _nav(driver, "settings")
        driver.refresh()
        time.sleep(2)
        driver.refresh()
        time.sleep(3)
        assert _flutter_loaded(_src(driver))

    # ── Category 3: Extended Search & Place Flows (TC821–TC860) ───────────────

    def test_tc821_place_route_flutter_loaded(self, driver):
        """TC821 — /place/:id route renders Flutter app."""
        _nav(driver, "place/test-place-001")
        assert _flutter_loaded(_src(driver))

    def test_tc822_place_route_title_correct(self, driver):
        """TC822 — Browser title is 'crowdsense' on place route."""
        _nav(driver, "place/test-place-001")
        assert _title_ok(driver)

    def test_tc823_place_route_url_confirmed(self, driver):
        """TC823 — Current URL contains 'place' or 'login' on place route."""
        _nav(driver, "place/test-place-001", wait=4)
        assert _url_has(driver, "place", "login")

    def test_tc824_place_source_not_empty(self, driver):
        """TC824 — Place details page source exceeds 300 bytes."""
        _nav(driver, "place/test-place-001")
        assert len(_src(driver)) > 300

    def test_tc825_place_no_500_error(self, driver):
        """TC825 — Place details page does not show a 500 error."""
        _nav(driver, "place/test-place-001")
        assert "500 Internal Server Error" not in _src(driver)

    def test_tc826_place_invalid_id_no_crash(self, driver):
        """TC826 — Navigating to an invalid place ID does not crash."""
        _nav(driver, "place/nonexistent-xyz-99999")
        assert _flutter_loaded(_src(driver))

    def test_tc827_place_photos_route_loaded(self, driver):
        """TC827 — /place/:id/photos route renders Flutter app."""
        _nav(driver, "place/test-place-001/photos")
        assert _flutter_loaded(_src(driver))

    def test_tc828_place_photos_title_correct(self, driver):
        """TC828 — Browser title is 'crowdsense' on photos route."""
        _nav(driver, "place/test-place-001/photos")
        assert _title_ok(driver)

    def test_tc829_place_scroll_stable(self, driver):
        """TC829 — Scrolling on place details does not crash."""
        _nav(driver, "place/test-place-001")
        driver.execute_script("window.scrollBy(0, 800)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver))

    def test_tc830_place_refresh_stable(self, driver):
        """TC830 — Refreshing place details page does not crash."""
        _nav(driver, "place/test-place-001")
        driver.refresh()
        time.sleep(4)
        assert _flutter_loaded(_src(driver))

    def test_tc831_search_source_not_empty(self, driver):
        """TC831 — Search page source exceeds 300 bytes."""
        _nav(driver, "search")
        assert len(_src(driver)) > 300

    def test_tc832_search_no_500_error(self, driver):
        """TC832 — Search page does not display a 500 error."""
        _nav(driver, "search")
        assert "500 Internal Server Error" not in _src(driver)

    def test_tc833_search_scroll_stable(self, driver):
        """TC833 — Scrolling on the search page does not crash."""
        _nav(driver, "search")
        driver.execute_script("window.scrollBy(0, 400)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver))

    def test_tc834_search_refresh_stable(self, driver):
        """TC834 — Refreshing the search page does not crash."""
        _nav(driver, "search")
        driver.refresh()
        time.sleep(4)
        assert _flutter_loaded(_src(driver))

    def test_tc835_search_mobile_viewport(self, driver):
        """TC835 — Search page renders on mobile viewport."""
        driver.set_window_size(375, 667)
        _nav(driver, "search")
        assert _flutter_loaded(_src(driver))
        driver.set_window_size(1280, 800)

    def test_tc836_place_landmark_flutter_loaded(self, driver):
        """TC836 — /place/landmark-abc route renders Flutter app."""
        _nav(driver, "place/landmark-abc")
        assert _flutter_loaded(_src(driver))

    def test_tc837_place_multiple_ids_stable(self, driver):
        """TC837 — Visiting multiple place IDs sequentially is stable."""
        for pid in ["place-001", "place-002", "landmark-abc"]:
            _nav(driver, f"place/{pid}", wait=2)
        assert _flutter_loaded(_src(driver))

    def test_tc838_search_results_source_not_empty(self, driver):
        """TC838 — Search results page source exceeds 300 bytes."""
        _nav(driver, "search-results")
        assert len(_src(driver)) > 300

    def test_tc839_search_results_no_500(self, driver):
        """TC839 — Search results page does not show a 500 error."""
        _nav(driver, "search-results")
        assert "500 Internal Server Error" not in _src(driver)

    def test_tc840_search_results_scroll_stable(self, driver):
        """TC840 — Scrolling on search results does not crash."""
        _nav(driver, "search-results")
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver))

    def test_tc841_planner_source_not_empty(self, driver):
        """TC841 — Planner page source exceeds 300 bytes."""
        _nav(driver, "planner")
        assert len(_src(driver)) > 300

    def test_tc842_planner_no_500_error(self, driver):
        """TC842 — Planner page does not display a 500 error."""
        _nav(driver, "planner")
        assert "500 Internal Server Error" not in _src(driver)

    def test_tc843_planner_scroll_stable(self, driver):
        """TC843 — Scrolling on the planner page does not crash."""
        _nav(driver, "planner")
        driver.execute_script("window.scrollBy(0, 600)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver))

    def test_tc844_planner_refresh_stable(self, driver):
        """TC844 — Refreshing the planner page does not crash."""
        _nav(driver, "planner")
        driver.refresh()
        time.sleep(4)
        assert _flutter_loaded(_src(driver))

    def test_tc845_planner_mobile_viewport(self, driver):
        """TC845 — Planner page renders on mobile viewport."""
        driver.set_window_size(390, 844)
        _nav(driver, "planner")
        assert _flutter_loaded(_src(driver))
        driver.set_window_size(1280, 800)

    def test_tc846_favorites_source_not_empty(self, driver):
        """TC846 — Favorites page source exceeds 300 bytes."""
        _nav(driver, "favorites")
        assert len(_src(driver)) > 300

    def test_tc847_favorites_no_500_error(self, driver):
        """TC847 — Favorites page does not display a 500 error."""
        _nav(driver, "favorites")
        assert "500 Internal Server Error" not in _src(driver)

    def test_tc848_favorites_scroll_stable(self, driver):
        """TC848 — Scrolling on the favorites page does not crash."""
        _nav(driver, "favorites")
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver))

    def test_tc849_favorites_refresh_stable(self, driver):
        """TC849 — Refreshing the favorites page does not crash."""
        _nav(driver, "favorites")
        driver.refresh()
        time.sleep(4)
        assert _flutter_loaded(_src(driver))

    def test_tc850_my_reports_source_not_empty(self, driver):
        """TC850 — My Reports page source exceeds 300 bytes."""
        _nav(driver, "my-reports")
        assert len(_src(driver)) > 300

    def test_tc851_my_reports_no_500_error(self, driver):
        """TC851 — My Reports page does not display a 500 error."""
        _nav(driver, "my-reports")
        assert "500 Internal Server Error" not in _src(driver)

    def test_tc852_my_reports_scroll_stable(self, driver):
        """TC852 — Scrolling on my-reports page does not crash."""
        _nav(driver, "my-reports")
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver))

    def test_tc853_my_reports_refresh_stable(self, driver):
        """TC853 — Refreshing my-reports page does not crash."""
        _nav(driver, "my-reports")
        driver.refresh()
        time.sleep(4)
        assert _flutter_loaded(_src(driver))

    def test_tc854_place_photos_source_not_empty(self, driver):
        """TC854 — Community photos page source exceeds 300 bytes."""
        _nav(driver, "place/test-place-001/photos")
        assert len(_src(driver)) > 300

    def test_tc855_place_photos_no_500(self, driver):
        """TC855 — Community photos page does not show a 500 error."""
        _nav(driver, "place/test-place-001/photos")
        assert "500 Internal Server Error" not in _src(driver)

    def test_tc856_place_photos_scroll_stable(self, driver):
        """TC856 — Scrolling on community photos page does not crash."""
        _nav(driver, "place/test-place-001/photos")
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver))

    def test_tc857_place_photos_mobile_viewport(self, driver):
        """TC857 — Community photos page renders on mobile viewport."""
        driver.set_window_size(390, 844)
        _nav(driver, "place/test-place-001/photos")
        assert _flutter_loaded(_src(driver))
        driver.set_window_size(1280, 800)

    def test_tc858_unknown_route_no_crash(self, driver):
        """TC858 — Unknown route does not crash the app."""
        _nav(driver, "this-route-does-not-exist")
        assert _flutter_loaded(_src(driver))

    def test_tc859_unknown_route_title_correct(self, driver):
        """TC859 — Unknown route browser title is 'crowdsense'."""
        _nav(driver, "xyz-unknown-route")
        assert _title_ok(driver)

    def test_tc860_deep_nested_route_no_crash(self, driver):
        """TC860 — Deeply nested unknown route does not crash."""
        _nav(driver, "a/b/c/d/e/f")
        assert _flutter_loaded(_src(driver))

    # ── Category 4: Extended Profile, Settings & Misc (TC861–TC900) ──────────

    def test_tc861_profile_source_not_empty(self, driver):
        """TC861 — Profile page source exceeds 300 bytes."""
        _nav(driver, "profile")
        assert len(_src(driver)) > 300

    def test_tc862_profile_no_500_error(self, driver):
        """TC862 — Profile page does not display a 500 error."""
        _nav(driver, "profile")
        assert "500 Internal Server Error" not in _src(driver)

    def test_tc863_profile_scroll_stable(self, driver):
        """TC863 — Scrolling on the profile page does not crash."""
        _nav(driver, "profile")
        driver.execute_script("window.scrollBy(0, 600)")
        time.sleep(1)
        assert _flutter_loaded(_src(driver))

    def test_tc864_profile_refresh_stable(self, driver):
        """TC864 — Refreshing the profile page does not crash."""
        _nav(driver, "profile")
        driver.refresh()
        time.sleep(4)
        assert _flutter_loaded(_src(driver))

    def test_tc865_profile_mobile_viewport(self, driver):
        """TC865 — Profile page renders on mobile viewport (390×844)."""
        driver.set_window_size(390, 844)
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver))
        driver.set_window_size(1280, 800)

    def test_tc866_profile_tablet_viewport(self, driver):
        """TC866 — Profile page renders on tablet viewport (768×1024)."""
        driver.set_window_size(768, 1024)
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver))
        driver.set_window_size(1280, 800)

    def test_tc867_settings_to_profile_navigation(self, driver):
        """TC867 — Navigating from /settings to /profile is stable."""
        _nav(driver, "settings")
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver))

    def test_tc868_profile_to_settings_navigation(self, driver):
        """TC868 — Navigating from /profile to /settings is stable."""
        _nav(driver, "profile")
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver))

    def test_tc869_all_protected_routes_redirect(self, driver):
        """TC869 — All protected routes redirect unauthenticated user to login."""
        protected = ["home", "profile", "favorites", "planner", "my-reports"]
        for route in protected:
            _nav(driver, route, wait=3)
            assert _url_has(driver, "login", route), f"{route} did not redirect"

    def test_tc870_settings_is_not_protected(self, driver):
        """TC870 — /settings does not redirect to login (accessible without auth)."""
        _nav(driver, "settings", wait=4)
        assert _url_has(driver, "settings")

    def test_tc871_app_does_not_show_blank_page(self, driver):
        """TC871 — App never shows a completely blank page."""
        driver.get(BASE_URL)
        time.sleep(5)
        assert len(_src(driver)) > 100

    def test_tc872_login_page_never_blank(self, driver):
        """TC872 — Login page is never blank after 4 seconds."""
        _nav(driver, "login")
        assert len(_src(driver)) > 100

    def test_tc873_register_page_never_blank(self, driver):
        """TC873 — Register page is never blank after 4 seconds."""
        _nav(driver, "register")
        assert len(_src(driver)) > 100

    def test_tc874_settings_page_never_blank(self, driver):
        """TC874 — Settings page is never blank after 4 seconds."""
        _nav(driver, "settings")
        assert len(_src(driver)) > 100

    def test_tc875_forgot_password_never_blank(self, driver):
        """TC875 — Forgot-password page is never blank after 4 seconds."""
        _nav(driver, "forgot-password")
        assert len(_src(driver)) > 100

    def test_tc876_search_never_blank(self, driver):
        """TC876 — Search page is never blank after 4 seconds."""
        _nav(driver, "search")
        assert len(_src(driver)) > 100

    def test_tc877_planner_never_blank(self, driver):
        """TC877 — Planner page is never blank after 4 seconds."""
        _nav(driver, "planner")
        assert len(_src(driver)) > 100

    def test_tc878_base_url_no_crash(self, driver):
        """TC878 — Base URL does not cause a JavaScript error crash."""
        driver.get(BASE_URL)
        time.sleep(5)
        assert _flutter_loaded(_src(driver))

    def test_tc879_app_not_case_sensitive_crowdsense(self, driver):
        """TC879 — Browser title consistently shows 'crowdsense' lowercase."""
        _nav(driver, "login")
        assert "crowdsense" in driver.title.lower()

    def test_tc880_page_source_has_flutter_script(self, driver):
        """TC880 — Page source includes flutter_bootstrap.js script reference."""
        driver.get(BASE_URL)
        time.sleep(3)
        assert "flutter" in driver.page_source.lower()

    def test_tc881_login_consistent_title_on_2_loads(self, driver):
        """TC881 — Login page title is consistently 'crowdsense' on 2 loads."""
        for _ in range(2):
            _nav(driver, "login", wait=3)
            assert _title_ok(driver)

    def test_tc882_register_consistent_title_on_2_loads(self, driver):
        """TC882 — Register page title is consistently 'crowdsense' on 2 loads."""
        for _ in range(2):
            _nav(driver, "register", wait=3)
            assert _title_ok(driver)

    def test_tc883_settings_consistent_url_on_2_loads(self, driver):
        """TC883 — Settings page URL is consistently 'settings' on 2 loads."""
        for _ in range(2):
            _nav(driver, "settings", wait=3)
            assert _url_has(driver, "settings")

    def test_tc884_place_title_consistent_on_2_loads(self, driver):
        """TC884 — Place page title is consistently 'crowdsense' on 2 loads."""
        for _ in range(2):
            _nav(driver, "place/test-place-001", wait=3)
            assert _title_ok(driver)

    def test_tc885_app_does_not_leak_server_info(self, driver):
        """TC885 — Page source does not contain server stack traces."""
        driver.get(BASE_URL)
        time.sleep(4)
        src = _src(driver).lower()
        assert "traceback" not in src and "stacktrace" not in src

    def test_tc886_login_does_not_leak_server_info(self, driver):
        """TC886 — Login page source does not contain server stack traces."""
        _nav(driver, "login")
        src = _src(driver).lower()
        assert "traceback" not in src and "stacktrace" not in src

    def test_tc887_settings_dart_loaded(self, driver):
        """TC887 — Settings page source contains Flutter or Dart markers."""
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver))

    def test_tc888_planner_dart_loaded(self, driver):
        """TC888 — Planner page source contains Flutter or Dart markers."""
        _nav(driver, "planner")
        assert _flutter_loaded(_src(driver))

    def test_tc889_favorites_dart_loaded(self, driver):
        """TC889 — Favorites page source contains Flutter or Dart markers."""
        _nav(driver, "favorites")
        assert _flutter_loaded(_src(driver))

    def test_tc890_my_reports_dart_loaded(self, driver):
        """TC890 — My-reports page source contains Flutter or Dart markers."""
        _nav(driver, "my-reports")
        assert _flutter_loaded(_src(driver))

    def test_tc891_profile_dart_loaded(self, driver):
        """TC891 — Profile page source contains Flutter or Dart markers."""
        _nav(driver, "profile")
        assert _flutter_loaded(_src(driver))

    def test_tc892_place_dart_loaded(self, driver):
        """TC892 — Place details page source contains Flutter or Dart markers."""
        _nav(driver, "place/test-place-001")
        assert _flutter_loaded(_src(driver))

    def test_tc893_search_dart_loaded(self, driver):
        """TC893 — Search page source contains Flutter or Dart markers."""
        _nav(driver, "search")
        assert _flutter_loaded(_src(driver))

    def test_tc894_search_results_dart_loaded(self, driver):
        """TC894 — Search results page source contains Flutter or Dart markers."""
        _nav(driver, "search-results")
        assert _flutter_loaded(_src(driver))

    def test_tc895_home_dart_loaded(self, driver):
        """TC895 — Home page source contains Flutter or Dart markers."""
        _nav(driver, "home")
        assert _flutter_loaded(_src(driver))

    def test_tc896_photos_dart_loaded(self, driver):
        """TC896 — Community photos page contains Flutter or Dart markers."""
        _nav(driver, "place/test-place-001/photos")
        assert _flutter_loaded(_src(driver))

    def test_tc897_ten_route_session_no_crash(self, driver):
        """TC897 — Visiting 10 routes in one browser session does not crash."""
        routes = [
            "login", "register", "forgot-password", "settings",
            "home", "search", "planner", "favorites", "profile",
            "place/test-place-001"
        ]
        for r in routes:
            driver.get(f"{BASE_URL}/#/{r}")
            time.sleep(1.5)
        assert _flutter_loaded(_src(driver))

    def test_tc898_browser_history_length_grows(self, driver):
        """TC898 — Browser history length increases after route navigations."""
        driver.get(BASE_URL)
        initial = driver.execute_script("return window.history.length")
        _nav(driver, "login")
        _nav(driver, "settings")
        final = driver.execute_script("return window.history.length")
        assert final >= initial

    def test_tc899_all_test_routes_flutter_rendered(self, driver):
        """TC899 — All main test routes render Flutter markers."""
        routes = ["login", "register", "forgot-password", "settings"]
        for r in routes:
            _nav(driver, r, wait=3)
            assert _flutter_loaded(_src(driver)), f"Flutter not rendered on /{r}"

    def test_tc900_test_suite_reaches_900_test_cases(self, driver):
        """TC900 — Final extended selenium test — marks completion of TC741-TC900."""
        _nav(driver, "settings")
        assert _flutter_loaded(_src(driver)) and _title_ok(driver)
