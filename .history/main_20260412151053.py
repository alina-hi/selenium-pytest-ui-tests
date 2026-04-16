import os
from selenium.webdriver.chrome.webdriver import ChroniumDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = os.path.join(os.getcwd(), "chrome-win64", "chrome.exe")
service = Service(executable_path=os.join(os.getcwd(), "chromedriver-win64", "chromedriver.exe"))
driver = 

