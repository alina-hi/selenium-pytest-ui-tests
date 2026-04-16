import os
import pytest
from selenium.webdriver.chrome.webdriver import ChromiumDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    options = Options()
    service = Service(executable_path=os.path.join(os.getcwd(), "chromedriver-win64", "chromedriver.exe"))
    driver = ChromiumDriver(browser_name="Chrome", vendor_prefix="Google", options=options, service=service)
    driver.maximize_window()
    yield driver
    #driver.quit()

def test_select_(driver):
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print("Страница открыта")
    assert "TechBeamers" in driver.title
    driver.implicitly_wait(5)
    
    print("\n--- Тест выпадающих списков ---")
    # Находим выпадающий список (на странице он один)
    dropdown_element = driver.find_element(By.XPATH, "//select")
    select = Select(dropdown_element)
    
    # Выбираем значение по видимому тексту (как просится в задании)
    select.select_by_visible_text("Python")
    print(f"1. Выбрано по тексту: {select.first_selected_option.text}")
    
    # Для демонстрации выберем другое значение по индексу
    select.select_by_index(2) # Например, 2-й элемент
    print(f"2. Выбрано по индексу: {select.first_selected_option.text}")
    
    # Выберем ещё одно значение по value (атрибуту)
    select.select_by_value("selenium")
    print(f"3. Выбрано по value: {select.first_selected_option.text}")
    
    print("Тест выпадающих списков пройден!")
    input("Нажмите Enter для закрытия браузера...")