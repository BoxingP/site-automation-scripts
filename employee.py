from datetime import datetime

from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from page import input_text_value, select_option


def create_employee(tenant, index, info, url, driver, need_create_employee=False):
    wait = WebDriverWait(driver, 420)

    driver.get(url['domain'] + tenant + url['create-employee'])
    wait.until(EC.title_contains("PFS | Create New EMPLOYEE"))

    user = 'user' + str(index)
    input_text_value(driver, "6130503", user)
    input_text_value(driver, "6130505", info['last-name'])
    employee = tenant.lower()
    employee = employee[:3] + '60101' + employee[3:] + '_' + user
    input_text_value(driver, "6130509", employee)
    input_text_value(driver, "password", info['password'])
    input_text_value(driver, "password_confirm", info['password'])
    select_option(driver, "17322279", info['location'])
    select_option(driver, "17322280", info['role'])
    now = datetime.now() + relativedelta(months=+info['expire-month'])
    input_text_value(driver, "ts_17322281", now.strftime("%m/%d/%Y"))
    select_option(driver, "associatedEntityIdentifier|5101124", info['access-level'])
    select_option(driver, "associatedEntityIdentifier|6240792", info['applications'])
    select_option(driver, "associatedEntityIdentifier|6240793", info['default-application'])
    select_option(driver, "associatedEntityIdentifier|7234414", info['home-dashboard'])

    print(employee)

    if need_create_employee:
        driver.find_element_by_xpath("//input[@id='overrideControlledSubmit']").click()
        wait.until(EC.title_contains("PFS | EMPLOYEE Details"))
    else:
        driver.get(url['domain'] + tenant + url['list-employee'])
        wait.until(EC.presence_of_element_located((By.ID, "gridview-1060-body")))

    return driver
