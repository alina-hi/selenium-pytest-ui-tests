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
    actions = ActionChains(driver)
    actions.move_to_element(python_lab).perform()
    menu_item = driver.find_element(By.XPATH, "//li[@id='menu-item-23407']/a")  # Python Code Checker
    menu_item.click()
    
    print("Выбран 'Python Code Checker'")
    
    input("Нажмите Enter для закрытия браузера...")


def test_no_double_output(driver):
    driver.get("https://techbeamers.com/python-code-checker/")
    print("Страница Python Code Checker открыта")
    
    wait = WebDriverWait(driver, 10)
    check_button = driver.find_element(By.ID, "checkCodeButton")
    check_button.click()
    print("Код запущен первый раз")

    wait.until(EC.presence_of_element_located((By.XPATH, "//pre[@class='output-format success-message']")))
    print("Результат первого запуска отобразился")
    check_button.click()

    print("Код запущен второй раз")
    wait.until(EC.presence_of_element_located((By.XPATH, "//pre[@class='output-format success-message']")))
    print("Результат второго запуска отобразился")
    
    result_blocks = driver.find_elements(By.XPATH, "//pre[@class='output-format success-message']")
    
    print(f"Найдено блоков с результатом: {len(result_blocks)}")
    
    assert len(result_blocks) == 1, (
        f"Ошибка: обнаружено дублирование результата! "
        f"Найдено {len(result_blocks)} блоков с результатом, ожидался 1 блок."
    )
    
    print("✓ Проверка пройдена: дублирование результата отсутствует")

    input("Нажмите Enter для закрытия браузера...")

def test_form_with_only_required_fields(driver):
    """
    Тест отправки формы только с обязательными полями
    """
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print("\n=== Тест: только обязательные поля ===")
    
    wait = WebDriverWait(driver, 10)
    
    # Прокрутка к форме
    form = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//section[.//h2[contains(text(), 'Form Elements')]]")
    ))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", form)
    
    # Заполняем ТОЛЬКО обязательные поля
    driver.find_element(By.ID, "username").send_keys("TestUser")
    driver.find_element(By.ID, "email").send_keys("test@example.com")
    driver.find_element(By.ID, "password").send_keys("password123")
    Select(driver.find_element(By.ID, "country")).select_by_value("us")
    
    # Отправляем
    submit_btn = driver.find_element(By.ID, "submit-btn")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
    submit_btn.click()
    
    # Проверяем успешную отправку
    result = wait.until(EC.visibility_of_element_located((By.ID, "form-result")))
    assert "successfully" in result.text.lower()
    print("✓ Форма успешно отправлена только с обязательными полями")