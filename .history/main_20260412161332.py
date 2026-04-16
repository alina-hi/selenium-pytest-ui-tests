import os
from selenium.webdriver.chrome.webdriver import ChromiumDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
options = Options()
# options.binary_location = os.path.join(os.getcwd(), "chrome-win64", "chrome.exe")
service = Service(executable_path=os.path.join(os.getcwd(), "chromedriver-win64", "chromedriver.exe"))
driver = ChromiumDriver(browser_name = "Chrome", vendor_prefix = "Google" , options = options, service = service)
driver.get("https://redvrm.red-soft.ru/")
driver.implicitly_wait(5)
driver.find_element(By.XPATH , '//div[contains(.,"Клиент РЕД ВРМ") and @data-tab = "tab2"]')
action = ActionChains()
action.scroll_to_element(element)
action.click()
action.perform()
driver = driver.find_element((By.XPATH, '//p'))
driver.quit()

