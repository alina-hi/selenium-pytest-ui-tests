import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    service = Service(executable_path=os.path.join(os.getcwd(), "chromedriver-win64", "chromedriver.exe"))
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_select_menu(driver):
    driver.get("https://demoqa.com/select-menu")
    wait = WebDriverWait(driver, timeout=10, poll_frequency=1)
    
    # 1. SELECT VALUE - используем CSS_SELECTOR (РАБОТАЛО)
    select_container = (By.CSS_SELECTOR, "#withOptGroup .css-13cymwt-control")
    driver.find_element(*select_container).click()
    
    option_to_select = (By.XPATH, '//div[text()="Group 2, option 1"]')
    wait.until(EC.element_to_be_clickable(option_to_select))
    driver.find_element(*option_to_select).click()
    
    selected_value = (By.CSS_SELECTOR, "#withOptGroup .css-1dimb5e-singleValue")
    selected_text = driver.find_element(*selected_value).text
    assert selected_text == "Group 2, option 1"
    print(f"✓ Select Value: {selected_text}")
    
    # 2. SELECT ONE - тоже CSS_SELECTOR
    select_one_container = (By.CSS_SELECTOR, "#selectOne .css-13cymwt-control")
    driver.find_element(*select_one_container).click()
    
    option_one = (By.XPATH, '//div[text()="Other"]')
    wait.until(EC.element_to_be_clickable(option_one))
    driver.find_element(*option_one).click()
    
    selected_one = (By.CSS_SELECTOR, "#selectOne .css-1dimb5e-singleValue")
    selected_one_text = driver.find_element(*selected_one).text
    print(f"✓ Select One: {selected_one_text}")