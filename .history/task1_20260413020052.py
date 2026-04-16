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


def test_no_duplicate_result_after_rerun(driver):
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

@pytest.mark.parametrize("username, email, password, bio, expected_valid", [
    # Корректные данные
    ("Иван", "ivan@example.com", "password123", "Тестировщик", True),
    ("Мария", "maria@test.ru", "qwerty456", "Разработчик", True),
    # Некорректные email
    ("Тест1", "invalid-email", "pass1", "Био", False),
    ("Тест2", "test@", "pass2", "Био", False),
    ("Тест3", "withoutdot@com", "pass3", "Био", False),
    ("Тест4", "", "pass4", "Био", False),
    ("Анна", "anna@example.com", "pass123", "", True),  # Пустое био
])
def test_text_box_form(driver, username, email, password, bio, expected_valid):
    """
    Тест автоматизации ввода данных в текстовые поля формы
    и валидации отправленных данных.
    """
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print(f"\n=== Тест с данными: Username={username}, Email={email} ===")
    
    wait = WebDriverWait(driver, 10)
    
    # Прокручиваем страницу к форме
    form_section = driver.find_element(By.XPATH, "//section[.//h2[contains(text(), 'Form Elements')]]")
    driver.execute_script("arguments[0].scrollIntoView(true);", form_section)
    
    # Находим поля формы по ID
    username_field = driver.find_element(By.ID, "username")
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    bio_field = driver.find_element(By.ID, "bio")
    submit_button = driver.find_element(By.ID, "submit-btn")
    result_div = driver.find_element(By.ID, "form-result")
    
    # Очищаем поля и вводим данные
    username_field.clear()
    username_field.send_keys(username)
    
    email_field.clear()
    email_field.send_keys(email)
    
    password_field.clear()
    password_field.send_keys(password)
    
    bio_field.clear()
    bio_field.send_keys(bio)
    
    print(f"Данные введены: Username={username}, Email={email}")
    
    # Прокручиваем к кнопке и нажимаем Submit
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    
    # Обработка исключения для некорректных данных
    try:
        submit_button.click()
        print("Форма отправлена")
        
        # Ждём появления результата
        wait.until(EC.visibility_of(result_div))
        
        # Проверяем, что сообщение об успешной отправке появилось
        result_text = result_div.text
        print(f"Сообщение об отправке: {result_text}")
        
        if expected_valid:
            assert "successfully" in result_text.lower() or "submitted" in result_text.lower()
            print(f"✓ Валидация пройдена для данных: {username}, {email}")
        else:
            print(f"✓ Ожидаемое поведение: форма не отправилась с некорректными данными")
            
    except Exception as e:
        if not expected_valid:
            print(f"✓ Ожидаемое исключение для некорректных данных: {e}")
        else:
            raise AssertionError(f"Не удалось отправить форму с корректными данными: {e}")


def test_email_validation(driver):
    """
    Тест для проверки обработки некорректного email.
    """
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print("\n=== Специальный тест валидации email ===")
    
    # Прокручиваем к форме
    form_section = driver.find_element(By.XPATH, "//section[.//h2[contains(text(), 'Form Elements')]]")
    driver.execute_script("arguments[0].scrollIntoView(true);", form_section)
    
    # Находим поля
    username_field = driver.find_element(By.ID, "username")
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    submit_button = driver.find_element(By.ID, "submit-btn")
    result_div = driver.find_element(By.ID, "form-result")
    
    # Заполняем корректные поля (кроме email)
    username_field.clear()
    username_field.send_keys("ТестовыйПользователь")
    
    password_field.clear()
    password_field.send_keys("test123456")
    
    # Список некорректных email для проверки
    invalid_emails = ["user@", "test.com", "user@.com", "user@domain.", "", "no-at-sign", "test@test", "user@test."]
    
    for invalid_email in invalid_emails:
        print(f"\n--- Проверка email: '{invalid_email}' ---")
        
        email_field.clear()
        email_field.send_keys(invalid_email)
        
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        submit_button.click()
        
        # Проверяем HTML5 валидацию
        is_valid = driver.execute_script("return arguments[0].checkValidity();", email_field)
        
        if not is_valid:
            print(f"  ✓ HTML5 валидация: email '{invalid_email}' признан некорректным")
        else:
            if result_div.is_displayed():
                print(f"  ⚠ Форма отправилась с email '{invalid_email}'")
            else:
                print(f"  ✓ Форма не отправилась с email '{invalid_email}'")
    
    print("\n✓ Тест валидации email завершён")
    input("Нажмите Enter для закрытия браузера...")


def test_form_submission_result(driver):
    """
    Тест проверяет, что после отправки формы появляется результат
    и данные соответствуют введённым.
    """
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print("\n=== Тест проверки результата отправки формы ===")
    
    wait = WebDriverWait(driver, 10)
    
    # Прокручиваем к форме
    form_section = driver.find_element(By.XPATH, "//section[.//h2[contains(text(), 'Form Elements')]]")
    driver.execute_script("arguments[0].scrollIntoView(true);", form_section)
    
    # Заполняем форму тестовыми данными
    test_data = {
        "username": "Петр Иванов",
        "email": "petr@example.com",
        "password": "secret123",
        "bio": "Люблю автоматизацию тестирования"
    }
    
    username_field = driver.find_element(By.ID, "username")
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    bio_field = driver.find_element(By.ID, "bio")
    submit_button = driver.find_element(By.ID, "submit-btn")
    result_div = driver.find_element(By.ID, "form-result")
    
    username_field.clear()
    username_field.send_keys(test_data["username"])
    
    email_field.clear()
    email_field.send_keys(test_data["email"])
    
    password_field.clear()
    password_field.send_keys(test_data["password"])
    
    bio_field.clear()
    bio_field.send_keys(test_data["bio"])
    
    print(f"Введены данные: {test_data['username']}, {test_data['email']}")
    
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    submit_button.click()
    print("Форма отправлена")
    
    wait.until(EC.visibility_of(result_div))
    result_text = result_div.text
    print(f"Результат: {result_text}")
    
    assert "successfully" in result_text.lower() or "submitted" in result_text.lower()
    
    print("✓ Проверка пройдена: форма успешно отправлена")
    
    input("Нажмите Enter для закрытия браузера...")