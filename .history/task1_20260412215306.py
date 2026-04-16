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
    
    # dropdown = driver.find_element(By.XPATH, "//select[@id='country']")
    
    # Прокручиваем к элементу
    driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
    time.sleep(0.5)

    # Работаем через Select (это не требует клика для раскрытия)
    select = Select(dropdown)
    select.select_by_value("ca")  # Выбираем Canada
    print(f"Выбрана страна: {select.first_selected_option.text}")
    
    input("Нажмите Enter для закрытия браузера...")