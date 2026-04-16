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

def test_select_country(driver):
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print("Страница открыта")
    
    # Находим выпадающий список по XPATH
    dropdown = driver.find_element(By.XPATH, "//select[@id='country']")
    dropdown.click()
    
    # Выбираем страну по XPATH
    dropdown = driver.find_element(By.XPATH, "//select[@id='country']")
    
    # Прокручиваем страницу к элементу
    driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
    
    # Небольшая пауза после прокрутки
    import time
    time.sleep(0.5)
    
    # Теперь кликаем
    dropdown.click()
    
    # Выбираем страну (например, Canada)
    country = driver.find_element(By.XPATH, "//option[@value='ca']")
    country.click()
    
    print(f"Выбрана страна: {country.text}")
    
    # Проверяем, что выбралось правильное значение
    selected = driver.find_element(By.XPATH, "//select[@id='country']/option[@selected]")
    assert selected.text == "Canada"
    print("Проверка пройдена!")
    
    input("Нажмите Enter для закрытия браузера...")