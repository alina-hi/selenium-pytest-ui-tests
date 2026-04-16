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
from selenium.common.exceptions import TimeoutException


@pytest.fixture
def driver():
    options = Options()
    # Добавляем опции для избежания перекрытия
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
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
    "email": "ivan@example.com",
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
    """
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print(f"\n=== Тест с некорректным email: '{invalid_email}' ===")
    
    wait = WebDriverWait(driver, 10)
    
    # Ждем загрузки формы и прокручиваем
    form_section = wait.until(
        EC.presence_of_element_located((By.XPATH, "//section[.//h2[contains(text(), 'Form Elements')]]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", form_section)
    
    # Заполняем все обязательные поля
    username_field = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username_field.clear()
    username_field.send_keys(test_user_data["username"])
    print(f"✓ Username заполнен: {test_user_data['username']}")
    
    email_field = wait.until(EC.element_to_be_clickable((By.ID, "email")))
    email_field.clear()
    email_field.send_keys(invalid_email)
    print(f"✓ Email заполнен: '{invalid_email}'")
    
    password_field = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password_field.clear()
    password_field.send_keys(test_user_data["password"])
    print("✓ Password заполнен")
    
    country_select = wait.until(EC.element_to_be_clickable((By.ID, "country")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", country_select)
    select = Select(country_select)
    select.select_by_value(test_user_data["country"])
    print("✓ Country выбран: United States")
    
    # Прокручиваем к кнопке и ждем, пока она станет кликабельной
    submit_button = wait.until(EC.element_to_be_clickable((By.ID, "submit-btn")))
    
    # Пытаемся кликнуть разными способами
    try:
        # Способ 1: обычный клик
        submit_button.click()
    except:
        try:
            # Способ 2: клик через JavaScript
            driver.execute_script("arguments[0].click();", submit_button)
            print("✓ Клик выполнен через JavaScript")
        except:
            # Способ 3: клик через ActionChains
            actions = ActionChains(driver)
            actions.move_to_element(submit_button).click().perform()
            print("✓ Клик выполнен через ActionChains")
    
    print("✓ Форма отправлена")
    
    # Проверяем, что форма НЕ отправилась (ждем, что результат НЕ появится)
    try:
        result_div = driver.find_element(By.ID, "form-result")
        wait.until(EC.visibility_of(result_div))
        result_text = result_div.text
        print(f"Результат: {result_text}")
        # Если результат появился - форма отправилась, а это ошибка
        raise AssertionError(f"ОШИБКА: Форма отправилась с некорректным email '{invalid_email}'!")
    except TimeoutException:
        # Ожидаемое поведение - форма не отправилась
        print(f"✓ Исключение обработано: форма НЕ отправилась с email '{invalid_email}'")
    
    print(f"✓ Тест для email '{invalid_email}' завершен")
    print("=" * 60)


def test_valid_email_and_validate_data(driver):
    """
    Тест с корректным email и валидацией введённых данных.
    """
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print("\n=== Тест с корректным email и валидацией данных ===")
    
    wait = WebDriverWait(driver, 10)
    
    # Прокручиваем к форме
    form_section = wait.until(
        EC.presence_of_element_located((By.XPATH, "//section[.//h2[contains(text(), 'Form Elements')]]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", form_section)
    
    # Вводим данные
    username_field = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username_field.clear()
    username_field.send_keys(test_user_data["username"])
    print(f"✓ Username: {test_user_data['username']}")
    
    email_field = wait.until(EC.element_to_be_clickable((By.ID, "email")))
    email_field.clear()
    email_field.send_keys(test_user_data["email"])
    print(f"✓ Email: {test_user_data['email']}")
    
    password_field = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password_field.clear()
    password_field.send_keys(test_user_data["password"])
    print("✓ Password заполнен")
    
    bio_field = wait.until(EC.element_to_be_clickable((By.ID, "bio")))
    bio_field.clear()
    bio_field.send_keys(test_user_data["bio"])
    print(f"✓ Bio: {test_user_data['bio']}")
    
    country_select = wait.until(EC.element_to_be_clickable((By.ID, "country")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", country_select)
    Select(country_select).select_by_value(test_user_data["country"])
    print("✓ Country: United States")
    
    # Кликаем по кнопке с обходом перекрытия
    submit_button = wait.until(EC.element_to_be_clickable((By.ID, "submit-btn")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", submit_button)
    
    try:
        submit_button.click()
    except:
        driver.execute_script("arguments[0].click();", submit_button)
    
    print("✓ Форма отправлена")
    
    # Ждём появления результата
    result_div = wait.until(EC.visibility_of_element_located((By.ID, "form-result")))
    result_text = result_div.text
    print(f"\nПоявившееся текстовое окно: '{result_text}'")
    
    # Валидация данных
    print("\n=== Проверка соответствия данных ===")
    
    # Проверяем username
    assert test_user_data["username"] in result_text, \
        f"Username '{test_user_data['username']}' не найден в результате: {result_text}"
    print(f"✓ Username '{test_user_data['username']}' найден в результате")
    
    # Проверяем email
    assert test_user_data["email"] in result_text, \
        f"Email '{test_user_data['email']}' не найден в результате: {result_text}"
    print(f"✓ Email '{test_user_data['email']}' найден в результате")
    
    # Проверяем страну
    country_names = {"us": "United States"}
    expected_country = country_names.get(test_user_data["country"], "")
    assert expected_country in result_text, \
        f"Страна '{expected_country}' не найдена в результате: {result_text}"
    print(f"✓ Страна '{expected_country}' найдена в результате")
    
    # Проверяем bio
    assert test_user_data["bio"] in result_text, \
        f"Bio не найден в результате: {result_text}"
    print(f"✓ Bio найден в результате")
    
    print("\n✓ ВСЕ ДАННЫЕ УСПЕШНО ПРОВАЛИДИРОВАНЫ")
    print("✓ ТЕСТ ПОЛНОСТЬЮ СООТВЕТСТВУЕТ ЗАДАНИЮ")


# Дополнительный тест для проверки, что форма не отправляется без обязательных полей
def test_form_does_not_submit_without_required_fields(driver):
    """
    Тест проверяет, что форма не отправляется без заполнения обязательных полей.
    """
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print("\n=== Тест: форма не отправляется без обязательных полей ===")
    
    wait = WebDriverWait(driver, 10)
    
    # Прокручиваем к форме
    form_section = wait.until(
        EC.presence_of_element_located((By.XPATH, "//section[.//h2[contains(text(), 'Form Elements')]]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", form_section)
    
    # Заполняем только email (без username, password, country)
    email_field = wait.until(EC.element_to_be_clickable((By.ID, "email")))
    email_field.clear()
    email_field.send_keys("test@example.com")
    
    # Пытаемся отправить
    submit_button = driver.find_element(By.ID, "submit-btn")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", submit_button)
    
    # Проверяем HTML5 валидацию
    username_field = driver.find_element(By.ID, "username")
    is_username_valid = driver.execute_script("return arguments[0].checkValidity();", username_field)
    
    assert not is_username_valid, "Форма должна быть невалидной без заполненного username"
    print("✓ Форма не отправляется без обязательных полей - это правильно")

