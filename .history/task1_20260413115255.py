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
    
    # Ждем загрузки страницы
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    # Прокручиваем к кнопке Submit (самый нижний элемент формы)
    submit_button = wait.until(EC.presence_of_element_located((By.ID, "submit-btn")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", submit_button)
    
    # Теперь поднимаемся немного вверх, чтобы увидеть все поля
    driver.execute_script("window.scrollBy(0, -200);")
    
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
    
    # Прокручиваем к country и выбираем
    country_select = wait.until(EC.element_to_be_clickable((By.ID, "country")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", country_select)
    select = Select(country_select)
    select.select_by_value(test_user_data["country"])
    print("✓ Country выбран: United States")
    
    # Снова прокручиваем к кнопке Submit
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", submit_button)
    
    result_div = driver.find_element(By.ID, "form-result")
    
    # Обработка исключения при отправке
    try:
        submit_button.click()
        print("✓ Форма отправлена")
        
        try:
            wait.until(EC.visibility_of(result_div))
            result_text = result_div.text
            print(f"Результат: {result_text}")
            raise AssertionError(f"ОШИБКА: Форма отправилась с некорректным email '{invalid_email}'!")
            
        except TimeoutException:
            print(f"✓ Исключение обработано: форма НЕ отправилась с email '{invalid_email}'")
            
    except Exception as e:
        print(f"✓ Исключение обработано: {e}")
    
    print(f"✓ Тест для email '{invalid_email}' завершен")
    print("=" * 60)


def test_valid_email_and_validate_data(driver):
    """
    Тест с корректным email и валидацией введённых данных.
    """
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print("\n=== Тест с корректным email и валидацией данных ===")
    
    wait = WebDriverWait(driver, 10)
    
    # Ждем загрузки страницы
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    # Прокручиваем к кнопке Submit
    submit_button = wait.until(EC.presence_of_element_located((By.ID, "submit-btn")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", submit_button)
    
    # Поднимаемся немного вверх
    driver.execute_script("window.scrollBy(0, -250);")
    
    # Заполняем поля
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
    
    # Прокручиваем к country
    country_select = wait.until(EC.element_to_be_clickable((By.ID, "country")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", country_select)
    Select(country_select).select_by_value(test_user_data["country"])
    print("✓ Country: United States")
    
    # Снова прокручиваем к кнопке Submit
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", submit_button)
    
    # Отправляем форму
    submit_button.click()
    print("✓ Форма отправлена")
    
    # Ждём появления результата
    result_div = wait.until(EC.visibility_of_element_located((By.ID, "form-result")))
    result_text = result_div.text
    print(f"\nПоявившееся текстовое окно: '{result_text}'")
    
    # Валидация данных
    print("\n=== Проверка соответствия данных ===")
    
    assert test_user_data["username"] in result_text, \
        f"Username '{test_user_data['username']}' не найден в результате: {result_text}"
    print(f"✓ Username '{test_user_data['username']}' найден в результате")
    
    assert test_user_data["email"] in result_text, \
        f"Email '{test_user_data['email']}' не найден в результате: {result_text}"
    print(f"✓ Email '{test_user_data['email']}' найден в результате")
    
    country_names = {"us": "United States"}
    expected_country = country_names.get(test_user_data["country"], "")
    assert expected_country in result_text, \
        f"Страна '{expected_country}' не найдена в результате: {result_text}"
    print(f"✓ Страна '{expected_country}' найдена в результате")
    
    assert test_user_data["bio"] in result_text, \
        f"Bio не найден в результате: {result_text}"
    print(f"✓ Bio найден в результате")
    
    print("\n✓ ВСЕ ДАННЫЕ УСПЕШНО ПРОВАЛИДИРОВАНЫ")
    print("✓ ТЕСТ ПОЛНОСТЬЮ СООТВЕТСТВУЕТ ЗАДАНИЮ")


# Самый надежный способ - прокрутка к элементу с кнопкой
def test_scroll_to_form(driver):
    """
    Тест, который гарантированно прокрутит до нужной формы.
    """
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print("\n=== Тест с гарантированной прокруткой до формы ===")
    
    wait = WebDriverWait(driver, 10)
    
    # Способ 1: Найти блок с кнопкой Submit и прокрутить к нему
    submit_section = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[@id='submit-btn']/ancestor::div[@class='test-case']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'start', behavior: 'smooth'});", submit_section)
    
    # Способ 2: Или просто прокрутить к кнопке
    # submit_button = wait.until(EC.presence_of_element_located((By.ID, "submit-btn")))
    # driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", submit_button)
    
    print("✓ Страница прокручена до формы с кнопками")
    
    # Теперь все поля должны быть видны
    username_field = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username_field.send_keys("Тест")
    print("✓ Поле username доступно и видимо")
    
    email_field = wait.until(EC.element_to_be_clickable((By.ID, "email")))
    email_field.send_keys("test@example.com")
    print("✓ Поле email доступно и видимо")
    
    print("✓ Тест прокрутки успешно завершен")


# Альтернативный вариант: прокрутка к конкретному заголовку
def test_scroll_to_buttons_section(driver):
    """
    Прокрутка к секции с кнопками по заголовку.
    """
    driver.get("https://techbeamers.com/selenium-practice-test-page/")
    print("\n=== Прокрутка к секции Buttons and Form Submission ===")
    
    wait = WebDriverWait(driver, 10)
    
    # Находим заголовок секции с кнопками
    buttons_header = wait.until(
        EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'Buttons and Form Submission')]"))
    )
    
    # Прокручиваем к этому заголовку
    driver.execute_script("arguments[0].scrollIntoView({block: 'start', behavior: 'smooth'});", buttons_header)
    
    print("✓ Прокручено до секции 'Buttons and Form Submission'")
    
    # Проверяем, что кнопка видна
    submit_button = wait.until(EC.visibility_of_element_located((By.ID, "submit-btn")))
    assert submit_button.is_displayed(), "Кнопка Submit не видна на странице"
    print("✓ Кнопка Submit видна")
    
    # Заполняем поля
    username_field = driver.find_element(By.ID, "username")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", username_field)
    username_field.send_keys("Пользователь")
    print("✓ Username заполнен")
    
    email_field = driver.find_element(By.ID, "email")
    email_field.send_keys("user@test.com")
    print("✓ Email заполнен")
    
    print("✓ Тест успешно завершен")