import random
import string
from datetime import datetime
from time import sleep

from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from page import input_text_value, select_option


def generate_password(letters=string.ascii_letters, digits=string.digits,
                      punctuation=string.punctuation.replace(",", ""), N=16):
    letters = ''.join(random.choice(letters) for _ in range(N // 2))
    digits = ''.join(random.choice(digits) for _ in range(N - N // 2 - 2))
    punctuation = ''.join(random.choice(punctuation) for _ in range(2))
    password = list(letters + digits + punctuation)
    random.shuffle(password)
    return ''.join(password)


def update_employee_info(result, tenant, info, value):
    origin_value = result.loc[result['tenant'] == tenant, info].item()
    if origin_value != origin_value:
        value_list = ['', value]
    else:
        value_list = [origin_value, value]
    values = ','.join(filter(None, value_list))
    result.loc[(result['tenant'] == tenant), info] = values
    return result


def create_employee(tenant, index, info, url, driver, result, need_create_employee=False):
    wait = WebDriverWait(driver, 420)

    driver.get(url['domain'] + tenant + url['create-employee'])
    wait.until(EC.title_contains("PFS | Create New EMPLOYEE"))

    user = 'user' + str(index)
    input_text_value(driver, "6130503", user)
    input_text_value(driver, "6130505", info['last-name'])
    employee = tenant.lower()
    employee = employee[:3] + '60101' + employee[3:] + '_' + user
    input_text_value(driver, "6130509", employee)
    password = generate_password()
    input_text_value(driver, "password", password)
    input_text_value(driver, "password_confirm", password)
    select_option(driver, "17322279", info['location'])
    select_option(driver, "17322280", info['role'])
    now = datetime.now() + relativedelta(months=+info['expire-month'])
    input_text_value(driver, "ts_17322281", now.strftime("%m/%d/%Y"))
    select_option(driver, "associatedEntityIdentifier|5101124", info['access-level'])
    select_option(driver, "associatedEntityIdentifier|6240792", info['applications'])
    select_option(driver, "associatedEntityIdentifier|6240793", info['default-application'])
    select_option(driver, "associatedEntityIdentifier|7234414", info['home-dashboard'])

    print(employee)
    print(password)

    if need_create_employee:
        driver.find_element_by_xpath("//input[@id='overrideControlledSubmit']").click()
        wait.until(EC.title_contains("PFS | EMPLOYEE Details"))
        result = update_employee_info(result, tenant, 'employee', employee)
        result = update_employee_info(result, tenant, 'password', password)
    else:
        driver.get(url['domain'] + tenant + url['list-employee'])
        wait.until(EC.presence_of_element_located((By.ID, "gridview-1060-body")))

    return driver, result


def inactive_employee(employee, url, driver, need_inactive_employee=False):
    wait = WebDriverWait(driver, 420)

    driver.get(url['domain'] + employee['tenant'] + url['list-employee'])
    sleep(3)

    if employee['name'] in driver.page_source:
        record_id = driver.find_element_by_xpath(
            "//*[contains(text(), '" + employee['name'] + "')]").find_element_by_xpath(
            '..').find_element_by_xpath('..').get_attribute('data-recordid')
        driver.get(url['domain'] + employee['tenant'] + url['edit-employee'] + record_id)
        if driver.find_element_by_xpath("//input[@name='active'][@type='checkbox']").get_attribute('checked'):
            driver.find_element_by_xpath("//input[@name='active'][@type='checkbox']").click()
            if need_inactive_employee:
                driver.find_element_by_xpath("//input[@id='overrideControlledSubmit']").click()
                wait.until(EC.title_contains("PFS | EMPLOYEE Details"))
            else:
                print("Abandon to inactive: %s" % employee['name'])
                return driver
        else:
            print("%s is already inactive." % employee['name'])
            return driver
    else:
        print("%s doesn't exist!" % employee['name'])
        return driver

    return driver
