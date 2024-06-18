import re
import logging
import os
import sys
from typing import Optional, List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.CRITICAL)


def setup_driver() -> WebDriver:
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Using new headless mode to avoid detection
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    # Set user-agent to mimic a real browser
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Suppress DevTools listening messages
    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Restore stdout
    sys.stdout = original_stdout
    return driver


def search_vessel(driver: WebDriver, vessel_name: str):
    vessel_name = vessel_name.replace(" ", "+").lower()

    url = f"https://www.google.com/search?q=vessel+name%3A+{vessel_name}+vessel+imo"
    driver.get(url)


def get_vessel_info(driver: WebDriver, imo: str) -> str:
    url = f"https://www.marinetraffic.com/en/ais/details/ships/imo:{imo}"
    driver.get(url)
    return driver.page_source


def find_top_result(driver: WebDriver, class_names: List[str]) -> Optional[WebElement]:
    for class_name in class_names:
        try:
            element = driver.find_element(By.CLASS_NAME, class_name)
            if element:
                return element
        except NoSuchElementException as e:
            logging.debug(f"Class name '{class_name}' not found: {e}")
    return


def extract_imo(text: str) -> Optional[str]:
    seven_digits = re.search(r"(\d{7})", text)
    return seven_digits.group() if seven_digits else None


def get_information_from_chrome_search(vessel_name: str) -> Optional[str]:
    class_names = ["hgKElc", "IZ6rdc", "ztXv9"]

    with setup_driver() as driver:

        # Set properties to mimic a real browser
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        });
                    """
        })
        sys.stdout = sys.__stdout__

        search_vessel(driver, vessel_name)
        top_result = find_top_result(driver, class_names)
        if not top_result:
            logging.info("Vessel IMO not found.")
            return

        imo = extract_imo(top_result.text)
        if not imo:
            logging.info("IMO number not found in the search results.")
            return

        print(f"Vessel {vessel_name.upper()} found.")

        html_source = get_vessel_info(driver, imo)
        if not html_source:
            logging.info("No html source data found in url.")

    return html_source
