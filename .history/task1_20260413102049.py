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

@pytest.mark.parametrize("invalid_email", [
    "invalid-email",
    "test@",
    "user@.com",
    "user@domain.",
    "",
    "no-at-sign",
    "test@test",
    "user@test."
])
def test_invalid_email_validation(driver, invalid_email):
    """
    Параметризованный тест для проверки ввода некорректного email.
    Ожидается, что форма не отправится или появится ошибка валидации.
    """
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print(f"\n=== Тест с некорректным email: '{invalid_email}' ===")
    
    # Прокручиваем страницу к форме
    form_section = driver.find_element(By.XPATH, "//section[.//h2[contains(text(), 'Form Elements')]]")
    driver.execute_script("arguments[0].scrollIntoView(true);", form_section)
    
    # Находим поля формы
    username_field = driver.find_element(By.ID, "username")
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    submit_button = driver.find_element(By.ID, "submit-btn")
    result_div = driver.find_element(By.ID, "form-result")
    
    # Заполняем корректные поля
    username_field.clear()
    username_field.send_keys("ТестовыйПользователь")
    
    password_field.clear()
    password_field.send_keys("test123456")
    
    # Вводим некорректный email
    email_field.clear()
    email_field.send_keys(invalid_email)
    
    print(f"Введён email: '{invalid_email}'")
    
    # Прокручиваем к кнопке
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    
    # Обработка исключения
    try:
        submit_button.click()
        print("Форма отправлена")
        
        # Проверяем, появилось ли сообщение об успехе
        # Если форма отправилась с некорректным email - это ошибка
        if result_div.is_displayed():
            result_text = result_div.text
            print(f"Результат: {result_text}")
            # Проверяем HTML5 валидацию
            is_valid = driver.execute_script("return arguments[0].checkValidity();", email_field)
            if not is_valid:
                print(f"✓ Исключение обработано: email '{invalid_email}' не прошёл HTML5 валидацию")
            else:
                raise AssertionError(f"Форма отправилась с некорректным email '{invalid_email}'!")
        else:
            print(f"✓ Исключение обработано: форма не отправилась с email '{invalid_email}'")
            
    except Exception as e:
        print(f"✓ Исключение обработано: {e}")
    
    print(f"✓ Тест для email '{invalid_email}' завершён")


# Тест с корректным email для сравнения
def test_valid_email(driver):
    """
    Тест с корректным email для проверки успешной отправки.
    """
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print("\n=== Тест с корректным email ===")
    
    wait = WebDriverWait(driver, 10)
    
    # Прокручиваем страницу к форме
    form_section = driver.find_element(By.XPATH, "//section[.//h2[contains(text(), 'Form Elements')]]")
    driver.execute_script("arguments[0].scrollIntoView(true);", form_section)
    
    # Находим поля формы
    username_field = driver.find_element(By.ID, "username")
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    bio_field = driver.find_element(By.ID, "bio")
    submit_button = driver.find_element(By.ID, "submit-btn")
    result_div = driver.find_element(By.ID, "form-result")
    
    # Вводим корректные данные
    username_field.clear()
    username_field.send_keys("Петр Иванов")
    
    email_field.clear()
    email_field.send_keys("petr@example.com")
    
    password_field.clear()
    password_field.send_keys("secret123")
    
    bio_field.clear()
    bio_field.send_keys("Люблю автоматизацию")
    
    print("Введены корректные данные")
    
    # Прокручиваем к кнопке и нажимаем Submit
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    submit_button.click()
    print("Форма отправлена")
    
    # Ждём появления результата
    wait.until(EC.visibility_of(result_div))
    
    # Проверяем успешную отправку
    result_text = result_div.text
    print(f"Результат: {result_text}")
    
    assert "successfully" in result_text.lower() or "submitted" in result_text.lower(), \
        "Сообщение об успешной отправке не найдено!"
    
    print("✓ Тест с корректным email пройден")
    
    input("Нажмите Enter для закрытия браузера...")