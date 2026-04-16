import os
import pytest
import time
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

def test_select_from_python_lab_menu_v2(driver):
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print("Страница открыта")
    
    # Находим и наводим на Python Lab
    python_lab = driver.find_element(By.XPATH, "//li[@id='menu-item-23405']/a")
    
    driver.execute_script("arguments[0].scrollIntoView(true);", python_lab)
    
    # Наводим курсор
    from selenium.webdriver.common.action_chains import ActionChains
    actions = ActionChains(driver)
    actions.move_to_element(python_lab).perform()
    # Выбираем нужный пункт
    menu_item = driver.find_element(By.XPATH, "//li[@id='menu-item-23407']/a")  # Python Code Checker
    menu_item.click()
    
    print("Выбран 'Python Code Checker'")
    
    input("Нажмите Enter для закрытия браузера...")
def test_no_duplicate_result_after_clear_and_rerun(driver):
    driver.get("https://techbeamers.com/python-code-checker/")
    print("Страница открыта")
    
    wait = WebDriverWait(driver, 10)
    
    # Находим кнопки
    check_button = driver.find_element(By.ID, "checkCodeButton")
    clear_button = driver.find_element(By.ID, "clearButton")
    
    # Находим поле для ввода кода (CodeMirror)
    code_area = driver.find_element(By.XPATH, "//div[@class='CodeMirror-code' and @contenteditable='true']")
    
    # 1. Вводим код через JS (надёжнее)
    driver.execute_script("""
        var cm = document.querySelector('.CodeMirror').CodeMirror;
        cm.setValue("print('Hello')");
    """)
    
    # 2. Запускаем проверку
    check_button.click()
    print("Код запущен первый раз")
    
    # Ждём появления результата
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='output' or contains(@class, 'result')]")))
    
    # 3. Очищаем поле
    clear_button.click()
    print("Поле очищено")
    
    # 4. Вводим тот же код снова
    driver.execute_script("""
        var cm = document.querySelector('.CodeMirror').CodeMirror;
        cm.setValue("print('Hello')");
    """)
    
    # 5. Запускаем снова
    check_button.click()
    print("Код запущен второй раз")
    
    # 6. Ждём обновления результата
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='output' or contains(@class, 'result')]")))
    
    # 7. ПРОВЕРКА: ищем все блоки с результатом
    result_elements = driver.find_elements(By.XPATH, "//div[@class='output' or contains(@class, 'result')]")
    
    print(f"Количество блоков с результатом: {len(result_elements)}")
    
    # Проверяем, что результат только один (нет дублирования)
    assert len(result_elements) == 1, "Есть дублирование результата!"
    
    print("✓ Проверка пройдена: дублирование отсутствует")
    
    input("Нажмите Enter для закрытия...")