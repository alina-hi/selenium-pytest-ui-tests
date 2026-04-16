import os
from selenium.webdriver.chrome.webdriver import ChromiumDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.
options = Options()
# options.binary_location = os.path.join(os.getcwd(), "chrome-win64", "chrome.exe")
service = Service(executable_path=os.path.join(os.getcwd(), "chromedriver-win64", "chromedriver.exe"))
driver = ChromiumDriver(browser_name = "Chrome", vendor_prefix = "Google" , options = options, service = service)
driver.get("https://www.red-soft.ru/ru")
driver.quit()

