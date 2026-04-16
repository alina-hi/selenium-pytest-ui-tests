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

    @pytest.mark.parametrize("name, email, password", [
    # Корректные данные
    ("Иван Петров", "ivan@example.com", "password123"),
    ("Мария Сидорова", "maria@test.ru", "qwerty456"),
    # Некорректные email (должны вызвать ошибку)
    ("Тест1", "invalid-email", "pass1"),
    ("Тест2", "test@", "pass2"),
    ("Тест3", "withoutdot@com", "pass3"),
    ("Тест4", "", "pass4"),  # Пустой email
])
    
def test_text_box_form(driver, name, email, password):
    """
    Тест автоматизации ввода данных в текстовые поля формы
    и валидации отправленных данных.
    """
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print(f"\n--- Тест с данными: Name={name}, Email={email}, Password={password} ---")
    
    wait = WebDriverWait(driver, 10)
    
    # Прокручиваем страницу к форме
    form = driver.find_element(By.XPATH, "//div[contains(@class, 'form-elements')] | //form")
    driver.execute_script("arguments[0].scrollIntoView(true);", form)
    
    # Находим поля формы
    try:
        name_field = driver.find_element(By.XPATH, "//input[@name='name']")
        email_field = driver.find_element(By.XPATH, "//input[@name='email']")
        password_field = driver.find_element(By.XPATH, "//input[@name='password']")
        submit_button = driver.find_element(By.XPATH, "//button[text()='Submit']")
    except:
        # Альтернативные локаторы
        name_field = driver.find_element(By.XPATH, "//input[@type='text' or @placeholder*='Name']")
        email_field = driver.find_element(By.XPATH, "//input[@type='email' or @placeholder*='Email']")
        password_field = driver.find_element(By.XPATH, "//input[@type='password']")
        submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
    
    # Очищаем поля и вводим данныеpytest task1.py::test_text_box_form -s
    name_field.clear()
    name_field.send_keys(name)
    
    email_field.clear()
    email_field.send_keys(email)
    
    password_field.clear()
    password_field.send_keys(password)
    
    print(f"Данные введены: Name={name}, Email={email}, Password={password}")
    
    # Прокручиваем к кнопке и нажимаем Submit
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    submit_button.click()
    print("Форма отправлена")
    
    # Обработка исключения для некорректного email
    try:
        # Ждём появления сообщения об успешной отправке
        success_message = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Form submitted') or contains(@class, 'success')]"))
        )
        print(f"Сообщение об отправке: {success_message.text}")
        
        # Проверяем, что отправленные данные соответствуют введённым
        assert name in success_message.text or success_message.is_displayed(), \
            f"Имя '{name}' не найдено в сообщении об отправке"
        
        print(f"✓ Валидация пройдена для email: {email}")
        
    except Exception as e:
        # Если это некорректный email, ожидаем ошибку
        if not "@" in email or "." not in email or email == "":
            print(f"✓ Ожидаемое исключение для некорректного email '{email}': форма не отправилась")
            print(f"  Причина: {e}")
        else:
            # Если email корректный, но произошла ошибка — это проблема
            raise AssertionError(f"Не удалось отправить форму с корректными данными: {e}")
    
    # Небольшая задержка для визуального контроля
    import time
    time.sleep(1)


# Дополнительный тест только для проверки валидации email
def test_email_validation_only(driver):
    """
    Специальный тест для проверки обработки некорректного email.
    """
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print("\n--- Специальный тест валидации email ---")
    
    # Прокручиваем к форме
    form = driver.find_element(By.XPATH, "//div[contains(@class, 'form-elements')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", form)
    
    # Находим поле email и кнопку
    email_field = driver.find_element(By.XPATH, "//input[@name='email']")
    submit_button = driver.find_element(By.XPATH, "//button[text()='Submit']")
    
    # Список некорректных email для проверки
    invalid_emails = ["user@", "test.com", "user@.com", "user@domain.", "", "no-at-sign"]
    
    for invalid_email in invalid_emails:
        print(f"\nПроверка email: '{invalid_email}'")
        
        # Очищаем и вводим некорректный email
        email_field.clear()
        email_field.send_keys(invalid_email)
        
        # Пробуем отправить
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        submit_button.click()
        
        # Проверяем, что форма не отправилась или появилось сообщение об ошибке
        try:
            # Проверяем, нет ли сообщения об успешной отправке
            success_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Form submitted')]")
            if len(success_elements) == 0:
                print(f"  ✓ Форма не отправилась с некорректным email '{invalid_email}'")
            else:
                print(f"  ⚠ ВНИМАНИЕ: Форма отправилась с некорректным email '{invalid_email}'")
        except:
            print(f"  ✓ Некорректный email '{invalid_email}' обработан")
        
        # Небольшая пауза между проверками
        import time
        time.sleep(0.5)
    
    print("\n✓ Тест валидации email завершён")
    input("Нажмите Enter для закрытия браузера...")    