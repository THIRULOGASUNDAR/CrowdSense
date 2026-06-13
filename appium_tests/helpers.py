import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def element_exists(driver, by, value, timeout=3) -> bool:
    try:
        wait_for_element(driver, by, value, timeout)
        return True
    except Exception:
        return False

def text_contains_exists(driver, text: str, timeout=3) -> bool:
    xpath = f"//*[contains(@text, '{text}') or contains(@content-desc, '{text}')]"
    return element_exists(driver, AppiumBy.XPATH, xpath, timeout)

def click_text(driver, text: str, timeout=3):
    xpath = f"//*[contains(@text, '{text}') or contains(@content-desc, '{text}')]"
    elem = wait_for_element(driver, AppiumBy.XPATH, xpath, timeout)
    elem.click()

def enter_text(driver, hint_text: str, input_text: str):
    xpath = f"//*[contains(@text, '{hint_text}') or contains(@content-desc, '{hint_text}')]"
    elem = wait_for_element(driver, AppiumBy.XPATH, xpath, 5)
    elem.click()
    time.sleep(0.5)
    elem.send_keys(input_text)
    try:
        driver.hide_keyboard()
    except Exception:
        pass

def count_text_views(driver) -> int:
    try:
        views = driver.find_elements(AppiumBy.CLASS_NAME, "android.view.View")
        text_views = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        return len(views) + len(text_views)
    except Exception:
        return 0
