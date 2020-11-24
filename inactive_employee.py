from selenium import webdriver

from account import log_in, log_out
from employee import inactive_employee
from info import load_config

chrome_driver = webdriver.Chrome()
admin_account = load_config("./account.json")['account']['admin']
employee_info = load_config("./employee.json")['employees']
url = load_config("./url.json")['url']
for employee in employee_info:
    chrome_driver = log_in(admin_account, employee['tenant'], url, chrome_driver)
    chrome_driver = inactive_employee(employee, url, chrome_driver, True)
    chrome_driver = log_out(url, chrome_driver)
chrome_driver.close()
