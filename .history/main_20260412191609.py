import os
import pytest
from selenium.webdriver.chrome.webdriver import ChromiumDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

@pytest.fixture
def driver():
    options = Options()
    # options.binary_location = os.path.join(os.getcwd(), "chrome-win64", "chrome.exe")
    service = Service(executable_path=os.path.join(os.getcwd(), "chromedriver-win64", "chromedriver.exe"))
    driver = ChromiumDriver(browser_name = "Chrome", vendor_prefix = "Google" , options = options, service = service)
    driver.maximize_window()
    yield
    driver.quit()

def    
driver.get("https://redvrm.red-soft.ru/")

driver.implicitly_wait(5)
driver.set_window_size(1920, 1080)
driver.maximize_window()
element_locator = (By.XPATH , '//div[contains(.,"Клиент РЕД ВРМ") and @data-tab = "tab2"]')
element = driver.find_element(*element_locator)
driver.execute_script("arguments[0].scrollIntoView(true);", element)
wait = WebDriverWait(driver, timeout = 60, poll_frequency = 15)
wait.until(EC.visibility_of_all_elements_located(element_locator))

#driver = driver.execute_script("arguments[0].scrollIntoView(true);", element)
#action = ActionChains(driver)
#action.scroll_to_element(element)
#action.perform()
element.click()
driver = driver.find_element((By.XPATH, '//p[text() = "Выбор периферии"]'))
element.click =()


