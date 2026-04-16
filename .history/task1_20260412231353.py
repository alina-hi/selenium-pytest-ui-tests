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
    # driver.quit()  


def test_python_lab_menu(driver):
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print("Страница открыта")
    
    python_lab = driver.find_element(By.XPATH, "//li[@id='menu-item-23405']/a")
    driver.execute_script("arguments[0].scrollIntoView(true);", python_lab)
    
    # Наводим курсор
    actions = ActionChains(driver)
    actions.move_to_element(python_lab).perform()
    
    # Выбираем нужный пункт
    menu_item = driver.find_element(By.XPATH, "//li[@id='menu-item-23407']/a")  # Python Code Checker
    menu_item.click()
    
    print("Выбран 'Python Code Checker'")
    
    input("Нажмите Enter для закрытия браузера...")


def test_no_duplicate_result_after_rerun(driver):
    driver.get("https://techbeamers.com/python-code-checker/")
    print("Страница открыта")
    
    wait = WebDriverWait(driver, 10)
    
    # Находим кнопку
    check_button = driver.find_element(By.ID, "checkCodeButton")
    
    # 1. Запускаем первый раз
    check_button.click()
    print("Код запущен первый раз")
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='output' or contains(@class, 'result')]")))
    
    # 2. Запускаем второй раз (без очистки)
    check_button.click()
    print("Код запущен второй раз")
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='output' or contains(@class, 'result')]")))
    
    # 3. Проверяем, что нет дублирования результата
    result_elements = driver.find_elements(By.XPATH, "//div[@class='output' or contains(@class, 'result')]")
    
    print(f"Количество блоков с результатом: {len(result_elements)}")
    assert len(result_elements) == 1, "Есть дублирование результата!"
    
    print("✓ Проверка пройдена")
    
    input("Нажмите Enter для закрытия...")