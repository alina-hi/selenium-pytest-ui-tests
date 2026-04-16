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

"""
def test_python_lab_menu(driver):
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print("Страница открыта")
    
    python_lab = driver.find_element(By.XPATH, "//li[@id='menu-item-23405']/a")
    driver.execute_script("arguments[0].scrollIntoView(true);", python_lab)
    actions = ActionChains(driver)
    actions.move_to_element(python_lab).perform()
    menu_item = driver.find_element(By.XPATH, "//li[@id='menu-item-23407']/a")  # Python Code Checker
    menu_item.click()
    
    print("Выбран 'Python Code Checker'")
    
    input("Нажмите Enter для закрытия браузера...")
"""

def test_no_duplicate_result_after_rerun(driver):
    """
    Проверка отсутствия дублирования результата при повторном запуске кода.
    При повторном нажатии кнопки Check Code результат должен обновляться,
    а не создавать новый блок с результатом.
    """
    # Открываем страницу с проверкой кода
    driver.get("https://techbeamers.com/python-code-checker/")
    print("Страница Python Code Checker открыта")
    
    wait = WebDriverWait(driver, 10)
    
    # Находим кнопку "Check Code"
    check_button = driver.find_element(By.ID, "checkCodeButton")
    
    # Шаг 1: Первый запуск кода
    check_button.click()
    print("Код запущен первый раз")
    
    # Ожидаем появления результата выполнения
    wait.until(EC.presence_of_element_located((By.XPATH, "//pre[@class='output-format success-message']")))
    print("Результат первого запуска отобразился")
    
    # Шаг 2: Второй запуск кода (без очистки)
    check_button.click()
    print("Код запущен второй раз")
    
    # Ожидаем обновления результата
    wait.until(EC.presence_of_element_located((By.XPATH, "//pre[@class='output-format success-message']")))
    print("Результат второго запуска отобразился")
    
    # Шаг 3: Проверка отсутствия дублирования
    # Ищем все блоки с результатом выполнения
    result_blocks = driver.find_elements(By.XPATH, "//pre[@class='output-format success-message']")
    
    print(f"Найдено блоков с результатом: {len(result_blocks)}")
    
    # Ожидаемый результат: должен быть только ОДИН блок с результатом
    assert len(result_blocks) == 1, (
        f"Ошибка: обнаружено дублирование результата! "
        f"Найдено {len(result_blocks)} блоков с результатом, ожидался 1 блок."
    )
    
    print("✓ Проверка пройдена: дублирование результата отсутствует")
    
    # Задержка перед закрытием браузера
    input("Нажмите Enter для закрытия браузера...")