import os
import pytest
from selenium.webdriver.chrome.webdriver import ChromiumDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


@pytest.fixture
def driver():
    options = Options()
    service = Service(executable_path=os.path.join(os.getcwd(), "chromedriver-win64", "chromedriver.exe"))
    driver = ChromiumDriver(browser_name="Chrome", vendor_prefix="Google", options=options, service=service)
    driver.maximize_window()
    yield driver
    # driver.quit()  # Закомментировано, браузер не закрывается


def test_python_lab_and_code_checker(driver):
    # Часть 1: Переход в Python Code Checker через меню
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print("Страница открыта")
    
    python_lab = driver.find_element(By.XPATH, "//li[@id='menu-item-23405']/a")
    driver.execute_script("arguments[0].scrollIntoView(true);", python_lab)
    
    actions = ActionChains(driver)
    actions.move_to_element(python_lab).perform()
    
    menu_item = driver.find_element(By.XPATH, "//li[@id='menu-item-23407']/a")
    menu_item.click()
    print("Выбран 'Python Code Checker'")
    
    # Часть 2: Проверка дублирования результата
    wait = WebDriverWait(driver, 10)
    check_button = driver.find_element(By.ID, "checkCodeButton")
    
    check_button.click()
    print("Код запущен первый раз")
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='output' or contains(@class, 'result')]")))
    
    check_button.click()
    print("Код запущен второй раз")
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='output' or contains(@class, 'result')]")))
    
    result_elements = driver.find_elements(By.XPATH, "//div[@class='output' or contains(@class, 'result')]")
    print(f"Количество блоков с результатом: {len(result_elements)}")
    assert len(result_elements) == 1, "Есть дублирование результата!"
    
    print("✓ Все проверки пройдены")
    
    input("Нажмите Enter для закрытия браузера...")