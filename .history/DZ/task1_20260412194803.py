import os
import pytest
from selenium.webdriver.chrome.webdriver import ChromiumDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
 
@pytest.fixture
def driver():
    options = Options()
    options.binary_location = os.path.join(os.getcwd(), "chrome-win64", "chrome.exe")
    service = Service(executable_path=os.path.join(os.getcwd(), "chromedriver-win64", "chromedriver.exe"))
    driver = ChromiumDriver(browser_name="Chrome", vendor_prefix="Google", options=options, service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_select_menu(driver):
    driver.get("https://demoqa.com/select-menu")
    wait = WebDriverWait(driver, timeout=10, poll_frequency=1)
    select_container = (By.CSS_SELECTOR, "#withOptGroup .css-13cymwt-control")
    driver.find_element(*select_container).click()
    # Для чётного студента: Group 2, option 1
    option_to_select = (By.XPATH, '//div[text() = ]')
    select_value_container = (By.XPATH, '//')



