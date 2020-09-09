import json
from datetime import datetime

from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

time_started = datetime.utcnow()

chrome_driver = webdriver.Chrome()


def get_file_info(path):
    file = open(path, 'r', encoding='UTF-8')
    data = json.load(file)
    file.close()
    return data


def log_in_tenant(account, tenant, driver):
    wait = WebDriverWait(driver, 420)
    driver.get("http://corelimslite.thermofisher.cn/corelims")

    username_id = driver.find_element_by_id("lims_userNameID")
    username_id.clear()
    username_id.send_keys(account["username"])

    password_id = driver.find_element_by_id("lims_passwordID")
    password_id.clear()
    password_id.send_keys(account["password"])

    driver.find_element_by_id("lims_buttonID").click()

    driver.get("http://corelimslite.thermofisher.cn/login")

    select_tenant = Select(driver.find_element_by_xpath("//select[@name='tenantSelect']"))
    select_tenant.select_by_visible_text(tenant)
    driver.find_element_by_xpath("//input[@name='submit'][@type='submit']").click()

    wait.until(EC.title_contains("PFS | Home"))

    return driver


def log_out(driver):
    wait = WebDriverWait(driver, 420)
    driver.get("http://corelimslite.thermofisher.cn/login?cmd=logout&entityType=LIMS")

    wait.until(EC.title_contains("PFS | Login"))

    return driver


def create_tenant(tenant, info, driver):
    wait = WebDriverWait(driver, 420)

    driver.get(
        "http://corelimslite.thermofisher.cn/708646210/corelims?cmd=clone&entityType=PLATFORM%20ACCOUNT&entityId=17437965")

    input_name = driver.find_element_by_id("name")
    input_name.send_keys(tenant)

    input_base_account_barcode = driver.find_element_by_id("17429591")
    input_base_account_barcode.send_keys(Keys.CONTROL + "a")
    input_base_account_barcode.send_keys(Keys.BACK_SPACE)
    input_base_account_barcode.send_keys(info['base-account-barcode'])

    input_alias = driver.find_element_by_id("17429593")
    input_alias.send_keys(Keys.CONTROL + "a")
    input_alias.send_keys(Keys.BACK_SPACE)
    input_alias.send_keys(tenant)

    Select(driver.find_element_by_id("associatedEntityIdentifier|17429833")).select_by_visible_text(
        info['tomcat-service'])
    driver.find_element_by_xpath("//input[@type='button'][@value='Save']").click()

    wait.until(EC.title_contains("PFS | PLATFORM ACCOUNT Details"))

    return driver


def create_employee(tenant, index, info, driver):
    wait = WebDriverWait(driver, 420)

    driver.get(
        "http://corelimslite.thermofisher.cn/" +
        tenant + "/corelims?cmd=new&entityType=EMPLOYEE&superType=EMPLOYEE")
    wait.until(EC.title_contains("PFS | Create New EMPLOYEE"))

    user = 'user' + str(index)
    employee = tenant.lower()
    employee = employee[:3] + '60101' + employee[3:] + '_' + user

    first_name = driver.find_element_by_xpath("//input[@id='6130503']")
    first_name.send_keys(user)

    driver.find_element_by_xpath("//input[@id='6130505']").send_keys(info['last-name'])

    username = driver.find_element_by_xpath("//input[@id='6130509']")
    username.send_keys(employee)

    driver.find_element_by_xpath("//input[@id='password']").send_keys(info['password'])
    driver.find_element_by_xpath("//input[@id='password_confirm']").send_keys(info['password'])

    Select(driver.find_element_by_xpath("//select[@id='17322279']")).select_by_value(info['location'])
    Select(driver.find_element_by_xpath("//select[@id='17322280']")).select_by_value(info['role'])

    expire = driver.find_element_by_xpath("//input[@id='ts_17322281']")
    now = datetime.now() + relativedelta(months=+info['expire-month'])
    expire.send_keys(now.strftime("%m/%d/%Y"))

    for access_level in info['access-level']:
        select = driver.find_element_by_xpath(
            "//select[@id='associatedEntityIdentifier|5101124']/option[text()='" + access_level + "']")
        ActionChains(driver).key_down(Keys.CONTROL).click(select).key_up(Keys.CONTROL).perform()

    for application in info['applications']:
        select = driver.find_element_by_xpath(
            "//select[@id='associatedEntityIdentifier|6240792']/option[text()='" + application + "']")
        ActionChains(driver).key_down(Keys.CONTROL).click(select).key_up(Keys.CONTROL).perform()

    Select(driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240793']")).select_by_visible_text(
        info['default-application'])
    Select(driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|7234414']")).select_by_visible_text(
        info['home-dashboard'])

    print(employee)

    driver.find_element_by_xpath("//input[@id='overrideControlledSubmit']").click()

    wait.until(EC.title_contains("PFS | EMPLOYEE Details"))
    return driver


def create_tenants(account, info, driver):
    driver = log_in_tenant(account, "PLATFORM ADMIN", driver)

    tenant_index = info['start-point']
    tenant_index_limit = tenant_index + info['number']

    while tenant_index < tenant_index_limit:
        tenant_name = "CLX" + str(tenant_index)
        driver = create_tenant(tenant_name, info, driver)
        tenant_index += 1

    driver = log_out(driver)

    return driver


def create_employees(account, info, driver):
    tenant_index = info['creation']['tenant']['start-point']
    tenant_index_limit = tenant_index + info['creation']['tenant']['number']
    employee_index = info['creation']['employee']['start-point']
    employee_amount = info['creation']['employee']['number-each-tenant']
    i = 0

    while tenant_index < tenant_index_limit:
        tenant_name = "CLX" + str(tenant_index)
        driver = log_in_tenant(account, tenant_name, driver)
        while i < employee_amount:
            employee_index = employee_index + i
            driver = create_employee(tenant_name, employee_index, info['creation']['employee'], driver)
            i += 1
        driver = log_out(driver)
        i = 0
        tenant_index += 1
        employee_index += 1


login_account = get_file_info("./account.json")
creation_info = get_file_info("./creation.json")
chrome_driver = create_tenants(login_account['account']['admin'], creation_info['creation']['tenant'], chrome_driver)
create_employees(login_account['account']['admin'], creation_info, chrome_driver)
chrome_driver.close()

time_ended = datetime.utcnow()
total_time = (time_ended - time_started).total_seconds()
print('Total time is %ss.' % round(total_time))
