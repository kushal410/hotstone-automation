import os
import sys
import time
import logging
from typing import Dict, List, Tuple, Optional

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.common import AppiumOptions

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


# ------------------- Logging -------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("HOTSTONE_LT_FINAL")


# ------------------- CONFIG -------------------
LT_USERNAME = os.getenv("LT_USERNAME", "kushal181722")
LT_ACCESS_KEY = os.getenv("LT_ACCESS_KEY", "YOUR_ACCESS_KEY")

# ✅ YOUR UPLOADED APP
APP_URL = "lt://APP10160431111777012323728482"

LT_HUB = "https://mobile-hub.lambdatest.com/wd/hub"

DEFAULT_WAIT = 20


# ------------------- DEVICE (SAFE SINGLE DEVICE FIRST) -------------------
ANDROID_DEVICE_MATRIX = [
    {
        "deviceName": "Galaxy S21",
        "platformVersion": "12"
    }
]


# ------------------- LOCATORS -------------------
EMAIL_XPATH = '//android.widget.EditText[1]'
PASSWORD_XPATH = '//android.widget.EditText[2]'
LOGIN_BTN_XPATH = '//android.view.View[@content-desc="Login"]'

HOME = (AppiumBy.ACCESSIBILITY_ID, "Home")
ABOUT = (AppiumBy.ACCESSIBILITY_ID, "About us")
PROFILE = (AppiumBy.ACCESSIBILITY_ID, "Profile")


# ------------------- DRIVER -------------------
def create_driver(device: Dict[str, str], run_index: int):
    options = AppiumOptions()

    capabilities = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",

        # ✅ YOUR LAMBDA TEST APP
        "appium:app": APP_URL,

        "appium:deviceName": device["deviceName"],
        "appium:platformVersion": device["platformVersion"],

        # 🔥 SAFE CONFIG (IMPORTANT)
        "appium:autoGrantPermissions": True,
        "appium:noReset": True,

        "lt:options": {
            "username": LT_USERNAME,
            "accessKey": LT_ACCESS_KEY,
            "project": "Hotstone Loyalty",
            "build": f"Hotstone Build #{run_index}",
            "name": "Smoke Test",
            "w3c": True
        }
    }

    options.load_capabilities(capabilities)

    try:
        return webdriver.Remote(LT_HUB, options=options)
    except WebDriverException as e:
        raise RuntimeError(f"LambdaTest session failed: {e}")


# ------------------- TEST CLASS -------------------
class HotstoneTest:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_WAIT)

    def click(self, locator: Tuple[str, str]):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, xpath: str, text: str):
        el = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
        el.click()
        el.clear()
        el.send_keys(text)

    # ------------------- LOGIN -------------------
    def login(self):
        logger.info("🔐 Logging in...")

        self.type(EMAIL_XPATH, "test@example.com")
        self.type(PASSWORD_XPATH, "password123")

        self.driver.find_element(AppiumBy.XPATH, LOGIN_BTN_XPATH).click()
        time.sleep(5)

        logger.info("✅ Login attempted")

    # ------------------- NAVIGATION -------------------
    def run_flow(self):
        logger.info("🏠 Home")
        self.click(HOME)

        time.sleep(2)

        logger.info("ℹ️ About")
        self.click(ABOUT)

        time.sleep(2)

        logger.info("👤 Profile")
        self.click(PROFILE)

        logger.info("🎉 Flow complete")


# ------------------- RUNNER -------------------
def run_once(device, run_index):
    driver = None

    try:
        logger.info(f"🚀 Starting {device['deviceName']}")

        driver = create_driver(device, run_index)
        test = HotstoneTest(driver)

        test.login()
        test.run_flow()

        logger.info("✅ Test Passed")

    except Exception as e:
        logger.exception("❌ Test Failed")
        raise

    finally:
        if driver:
            driver.quit()


def main():
    for i in range(1):
        for device in ANDROID_DEVICE_MATRIX:
            run_once(device, i + 1)

    logger.info("🎉 All runs complete")


if __name__ == "__main__":
    main()
