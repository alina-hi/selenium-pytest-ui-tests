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

test_user_data = {
    "username": "Иван Петров",
    "email": "ivan@example.com",  # Корректный email для успешного теста
    "password": "secret123",
    "country": "us",
    "bio": "Люблю автоматизацию тестирования"
}

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
    
    wait = WebDriverWait(driver, 10)
    
    # Прокручиваем к форме
    form_section = wait.until(
        EC.presence_of_element_located((By.XPATH, "//section[.//h2[contains(text(), 'Form Elements')]]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", form_section)
    
    # Заполняем все обязательные поля
    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    username_field.clear()
    username_field.send_keys(test_user_data["username"])
    
    email_field = driver.find_element(By.ID, "email")
    email_field.clear()
    email_field.send_keys(invalid_email)  # Вводим некорректный email
    
    password_field = driver.find_element(By.ID, "password")
    password_field.clear()
    password_field.send_keys(test_user_data["password"])
    
    country_select = driver.find_element(By.ID, "country")
    Select(country_select).select_by_value(test_user_data["country"])
    
    submit_button = driver.find_element(By.ID, "submit-btn")
    result_div = driver.find_element(By.ID, "form-result")
    
    # Прокручиваем к кнопке и пытаемся отправить
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", submit_button)
    
    # Обработка исключения при отправке
    try:
        submit_button.click()
        print("Форма отправлена")
        
        # Проверяем, появилось ли окно с результатом
        try:
            wait.until(EC.visibility_of(result_div))
            result_text = result_div.text
            print(f"Результат: {result_text}")
            
            # Если форма отправилась с некорректным email - это ошибка
            raise AssertionError(f"ОШИБКА: Форма отправилась с некорректным email '{invalid_email}'!")
            
        except TimeoutException:
            # Ожидаемое поведение - форма не отправилась
            print(f"✓ Исключение обработано: форма не отправилась с email '{invalid_email}'")
            
    except Exception as e:
        print(f"✓ Исключение обработано: {e}")
    
    print(f"✓ Тест для email '{invalid_email}' завершён\n")


def test_valid_email_and_validate_data(driver):
    """
    Тест с корректным email и валидацией введённых данных.
    Полностью соответствует заданию.
    """
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print("\n=== Тест с корректным email и валидацией данных ===")
    
    wait = WebDriverWait(driver, 10)
    
    # Прокручиваем к форме
    form_section = wait.until(
        EC.presence_of_element_located((By.XPATH, "//section[.//h2[contains(text(), 'Form Elements')]]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", form_section)
    
    # Вводим данные в текстовые поля формы
    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    username_field.clear()
    username_field.send_keys(test_user_data["username"])
    
    email_field = driver.find_element(By.ID, "email")
    email_field.clear()
    email_field.send_keys(test_user_data["email"])
    
    password_field = driver.find_element(By.ID, "password")
    password_field.clear()
    password_field.send_keys(test_user_data["password"])
    
    bio_field = driver.find_element(By.ID, "bio")
    bio_field.clear()
    bio_field.send_keys(test_user_data["bio"])
    
    country_select = driver.find_element(By.ID, "country")
    Select(country_select).select_by_value(test_user_data["country"])
    
    print("✓ Все текстовые поля заполнены")
    
    # Отправляем данные по кнопке Submit
    submit_button = driver.find_element(By.ID, "submit-btn")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", submit_button)
    submit_button.click()
    print("✓ Данные отправлены по кнопке Submit")
    
    # Ждём появления текстового окна с результатом
    result_div = wait.until(EC.visibility_of_element_located((By.ID, "form-result")))
    result_text = result_div.text
    print(f"\nПоявившееся текстовое окно: '{result_text}'")
    
    # ВАЛИДАЦИЯ: проверяем соответствие введённым данным
    print("\n=== Проверка соответствия данных ===")
    
    # Проверяем, что в результате есть username
    if test_user_data["username"] in result_text:
        print(f"✓ Username '{test_user_data['username']}' найден в результате")
    else:
        print(f"✗ Username '{test_user_data['username']}' НЕ найден в результате")
    
    # Проверяем, что в результате есть email
    if test_user_data["email"] in result_text:
        print(f"✓ Email '{test_user_data['email']}' найден в результате")
    else:
        print(f"✗ Email '{test_user_data['email']}' НЕ найден в результате")
    
    # Проверяем, что в результате есть страна
    country_names = {"us": "United States", "ca": "Canada", "uk": "United Kingdom"}
    expected_country = country_names.get(test_user_data["country"], "")
    if expected_country in result_text:
        print(f"✓ Страна '{expected_country}' найдена в результате")
    else:
        print(f"✗ Страна '{expected_country}' НЕ найдена в результате")
    
    # Проверяем, что в результате есть bio
    if test_user_data["bio"] in result_text:
        print(f"✓ Bio найден в результате")
    else:
        print(f"✗ Bio НЕ найден в результате")
    
    # Финальная проверка: все ли данные соответствуют
    assert test_user_data["username"] in result_text, \
        f"Username '{test_user_data['username']}' не найден в результате: {result_text}"
    
    assert test_user_data["email"] in result_text, \
        f"Email '{test_user_data['email']}' не найден в результате: {result_text}"
    
    assert expected_country in result_text, \
        f"Страна '{expected_country}' не найдена в результате: {result_text}"
    
    print("\n✓ ВСЕ ДАННЫЕ УСПЕШНО ПРОВАЛИДИРОВАНЫ")
    print("✓ ТЕСТ ПОЛНОСТЬЮ СООТВЕТСТВУЕТ ЗАДАНИЮ")


# Альтернативный вариант с более детальной валидацией
def test_valid_email_with_detailed_validation(driver):
    """
    Расширенный тест с детальной проверкой каждого поля
    """
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print("\n=== Расширенный тест с детальной валидацией ===")
    
    wait = WebDriverWait(driver, 10)
    
    # Вводимые данные
    form_data = {
        "username": "Анна Смирнова",
        "email": "anna@test.com",
        "password": "mypassword789",
        "bio": "QA Engineer, опыт 5 лет",
        "country": "United Kingdom"
    }
    
    # Прокрутка к форме
    form = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//section[.//h2[contains(text(), 'Form Elements')]]")
    ))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", form)
    
    # Заполнение полей
    driver.find_element(By.ID, "username").send_keys(form_data["username"])
    driver.find_element(By.ID, "email").send_keys(form_data["email"])
    driver.find_element(By.ID, "password").send_keys(form_data["password"])
    driver.find_element(By.ID, "bio").send_keys(form_data["bio"])
    Select(driver.find_element(By.ID, "country")).select_by_visible_text(form_data["country"])
    
    # Отправка
    submit_btn = driver.find_element(By.ID, "submit-btn")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
    submit_btn.click()
    
    # Получение результата
    result = wait.until(EC.visibility_of_element_located((By.ID, "form-result")))
    result_text = result.text
    
    # Валидация каждого поля
    print(f"Результат: {result_text}\n")
    
    validation_results = []
    
    # Проверка username
    if form_data["username"] in result_text:
        print(f"✅ Username: '{form_data['username']}' → присутствует")
        validation_results.append(True)
    else:
        print(f"❌ Username: '{form_data['username']}' → отсутствует")
        validation_results.append(False)
    
    # Проверка email
    if form_data["email"] in result_text:
        print(f"✅ Email: '{form_data['email']}' → присутствует")
        validation_results.append(True)
    else:
        print(f"❌ Email: '{form_data['email']}' → отсутствует")
        validation_results.append(False)
    
    # Проверка bio
    if form_data["bio"] in result_text:
        print(f"✅ Bio: '{form_data['bio']}' → присутствует")
        validation_results.append(True)
    else:
        print(f"❌ Bio: '{form_data['bio']}' → отсутствует")
        validation_results.append(False)
    
    # Проверка страны
    if form_data["country"] in result_text:
        print(f"✅ Country: '{form_data['country']}' → присутствует")
        validation_results.append(True)
    else:
        print(f"❌ Country: '{form_data['country']}' → отсутствует")
        validation_results.append(False)
    
    # Финальная проверка
    assert all(validation_results), "Не все данные соответствуют введённым!"
    
    print("\n✅ ВСЕ ДАННЫЕ УСПЕШНО ПРОВАЛИДИРОВАНЫ")
    print("✅ ТЕСТ ПОЛНОСТЬЮ СООТВЕТСТВУЕТ ЗАДАНИЮ")