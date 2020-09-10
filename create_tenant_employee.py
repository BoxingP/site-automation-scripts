import json
from datetime import datetime

from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

time_started = datetime.utcnow()

NEED_CREATE_TENANT = True
NEED_CREATE_EMPLOYEE = True
chrome_driver = webdriver.Chrome()


def input_text_value(driver, select, info):
    textbox = driver.find_element_by_xpath("//*[@id='" + select + "']")
    textbox.send_keys(Keys.CONTROL + "a")
    textbox.send_keys(Keys.BACK_SPACE)
    textbox.send_keys(info)


def select_option(driver, select, info):
    for option in info:
        Select(driver.find_element_by_xpath("//select[@id='" + select + "']")).select_by_visible_text(option)


def get_file_info(path):
    file = open(path, 'r', encoding='UTF-8')
    data = json.load(file)
    file.close()
    return data


def log_in_tenant(account, tenant, url, driver):
    wait = WebDriverWait(driver, 420)
    driver.get(url + "corelims")

    input_text_value(driver, "lims_userNameID", account["username"])
    input_text_value(driver, "lims_passwordID", account["password"])
    driver.find_element_by_id("lims_buttonID").click()

    driver.get(url + "login")

    select_tenant = Select(driver.find_element_by_xpath("//select[@name='tenantSelect']"))
    select_tenant.select_by_visible_text(tenant)
    driver.find_element_by_xpath("//input[@name='submit'][@type='submit']").click()

    wait.until(EC.title_contains("PFS | Home"))

    return driver


def log_out(url, driver):
    wait = WebDriverWait(driver, 420)
    driver.get(url + "login?cmd=logout&entityType=LIMS")

    wait.until(EC.title_contains("PFS | Login"))

    return driver


def create_tenant(tenant, info, url, driver):
    wait = WebDriverWait(driver, 420)

    driver.get(url + "708646210/corelims?cmd=clone&entityType=PLATFORM%20ACCOUNT&entityId=17437965")

    input_text_value(driver, "name", tenant)
    input_text_value(driver, "17429591", info['base-account-barcode'])
    input_text_value(driver, "17429593", tenant)
    select_option(driver, "associatedEntityIdentifier|17429833", info['tomcat-service'])

    if NEED_CREATE_TENANT:
        driver.find_element_by_xpath("//input[@type='button'][@value='Save']").click()
        wait.until(EC.title_contains("PFS | PLATFORM ACCOUNT Details"))
    else:
        driver.get(url + "708646210/corelims?cmd=getall&entityType=PLATFORM%20ACCOUNT")
        wait.until(EC.presence_of_element_located((By.ID, "gridview-1050-body")))

    return driver


def create_employee(tenant, index, info, url, driver):
    wait = WebDriverWait(driver, 420)

    driver.get(url + tenant + "/corelims?cmd=new&entityType=EMPLOYEE&superType=EMPLOYEE")
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

    if NEED_CREATE_EMPLOYEE:
        driver.find_element_by_xpath("//input[@id='overrideControlledSubmit']").click()
        wait.until(EC.title_contains("PFS | EMPLOYEE Details"))
    else:
        driver.get(url + tenant + "/corelims?cmd=getall&entityType=EMPLOYEE")
        wait.until(EC.presence_of_element_located((By.ID, "gridview-1060-body")))

    return driver


def create_tenants(account, info, driver):
    url = info['url']
    tenant = info['tenant']
    driver = log_in_tenant(account, "PLATFORM ADMIN", url, driver)
    tenant_index = tenant['start-point']
    tenant_index_limit = tenant_index + tenant['number']

    while tenant_index < tenant_index_limit:
        tenant_name = "CLX" + str(tenant_index)
        driver = create_tenant(tenant_name, tenant, url, driver)
        tenant_index += 1

    driver = log_out(url, driver)

    return driver


def create_employees(account, info, driver):
    url = info['url']
    tenant_info = info['tenant']
    tenant_index = tenant_info['start-point']
    tenant_index_limit = tenant_index + tenant_info['number']
    employee_info = info['employee']
    employee_index = employee_info['start-point']
    employee_amount = employee_info['number-each-tenant']
    i = 0

    while tenant_index < tenant_index_limit:
        tenant_name = "CLX" + str(tenant_index)
        driver = log_in_tenant(account, tenant_name, url, driver)
        while i < employee_amount:
            employee_index = employee_index + i
            driver = create_employee(tenant_name, employee_index, employee_info, url, driver)
            i += 1
        driver = log_out(url, driver)
        i = 0
        tenant_index += 1
        employee_index += 1

    return driver


admin_account = get_file_info("./account.json")['account']['admin']
creation_info = get_file_info("./creation.json")['creation']
chrome_driver = create_tenants(admin_account, creation_info, chrome_driver)
chrome_driver = create_employees(admin_account, creation_info, chrome_driver)
chrome_driver.close()

time_ended = datetime.utcnow()
total_time = (time_ended - time_started).total_seconds()
print('Total time is %ss.' % round(total_time))
