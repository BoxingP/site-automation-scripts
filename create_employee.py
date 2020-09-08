
import time
from datetime import datetime

from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

chrome_driver = webdriver.Chrome()


def get_login_account(path):
    file = open(path, "r")
    lines = file.readlines()
    username = lines[0].rstrip()
    password = lines[1].rstrip()
    file.close()
    return {'username': username, 'password': password}


def log_in_tenant(account, tenant, driver):
    wait = WebDriverWait(driver, 420)

    driver.get("http://corelimslite.thermofisher.cn/")

    username_id = driver.find_element_by_id("lims_userNameID")
    username_id.clear()
    username_id.send_keys(account["username"])

    password_id = driver.find_element_by_id("lims_passwordID")
    password_id.clear()
    password_id.send_keys(account["password"])

    driver.find_element_by_id("lims_buttonID").click()

    time.sleep(2)

    select_tenant = Select(driver.find_element_by_xpath("//div[@id='login']/form/*/select[@name='tenantSelect']"))
    select_tenant.select_by_visible_text(tenant)
    driver.find_element_by_xpath("//input[@name='submit'][@type='submit']").click()

    wait.until(EC.title_contains("PFS | Home"))

    return driver


def log_out(driver):
    wait = WebDriverWait(driver, 420)
    driver.get("http://corelimslite.thermofisher.cn/login?cmd=logout&entityType=LIMS")

    wait.until(EC.title_contains("PFS | Login"))

    return driver


def create_employee(tenant, index, driver):
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

    last_name = driver.find_element_by_xpath("//input[@id='6130505']")
    last_name.send_keys("corelims")

    username = driver.find_element_by_xpath("//input[@id='6130509']")
    username.send_keys(employee)

    password = driver.find_element_by_xpath("//input[@id='password']")
    password.send_keys("abc123")

    password_confirm = driver.find_element_by_xpath("//input[@id='password_confirm']")
    password_confirm.send_keys("abc123")

    select_location = Select(driver.find_element_by_xpath("//select[@id='17322279']"))
    select_location.select_by_value("上海")

    select_role = Select(driver.find_element_by_xpath("//select[@id='17322280']"))
    select_role.select_by_value("系统管理员")

    expire = driver.find_element_by_xpath("//input[@id='ts_17322281']")
    now = datetime.now() + relativedelta(months=+3)
    expire.send_keys(now.strftime("%m/%d/%Y"))

    select_data_generator = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|5101124']/option[text()='DATA GENERATOR']")
    select_data_viewer = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|5101124']/option[text()='DATA VIEWER']")
    select_default = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|5101124']/option[text()='DEFAULT']")
    select_view_all = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|5101124']/option[text()='VIEW-ALL']")
    ActionChains(driver).key_down(Keys.CONTROL).click(select_data_generator).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_data_viewer).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_default).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_view_all).key_up(Keys.CONTROL).perform()

    select_1 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_batch_material_usage_query_application']")
    select_2 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_consumable_lowlimit_report_application']")
    select_3 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_consumable_management_application']")
    select_4 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_consumable_receive_management_application']")
    select_5 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_homepage']")
    select_6 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_inventory_check_application']")
    select_7 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_inventory_query_application']")
    select_8 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_location_management_application']")
    select_9 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_qa_review_mgmt_application']")
    select_10 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_sample_disposal_request_mgmt_application']")
    select_11 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_sample_disposal_request_review_application']")
    select_12 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_sample_receive_management_application']")
    select_13 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_sample_registration_mgmt_application']")
    select_14 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_sample_report_mgmt_application']")
    select_15 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_sample_source_mgmt_application']")
    select_16 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_samplebatch_usage_query_application']")
    select_17 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_stock_in_confirmation_management_application']")
    select_18 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_stock_in_request_review_application']")
    select_19 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_stock_in_request_submission_application']")
    select_20 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_stock_out_confirmation_management_application']")
    select_21 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_stock_out_request_review_application']")
    select_22 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_stock_out_request_submission_application']")
    select_23 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='bex_validity_period_management_application']")
    select_24 = driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240792']/option[text()='ci_app_eln']")
    ActionChains(driver).key_down(Keys.CONTROL).click(select_1).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_2).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_3).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_4).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_5).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_6).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_7).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_8).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_9).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_10).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_11).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_12).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_13).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_14).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_15).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_16).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_17).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_18).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_19).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_20).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_21).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_22).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_23).key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).click(select_24).key_up(Keys.CONTROL).perform()

    select_default_app = Select(driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|6240793']"))
    select_default_app.select_by_visible_text("bex_homepage")

    select_dashboard = Select(driver.find_element_by_xpath("//select[@id='associatedEntityIdentifier|7234414']"))
    select_dashboard.select_by_visible_text("bex_homepage_dashboard")

    print(employee)

    driver.find_element_by_xpath("//input[@id='overrideControlledSubmit']").click()

    wait.until(EC.title_contains("PFS | EMPLOYEE Details"))
    return driver


login_account = get_login_account("./account")
tenant_index = 168
employee_index = 335
tenant_name = "CLX" + str(tenant_index)
chrome_driver = log_in_tenant(login_account, tenant_name, chrome_driver)

i = 0
employee_amount = 2
while i < employee_amount:
    employee_index = employee_index + i
    chrome_driver = create_employee(tenant_name, employee_index, chrome_driver)
    i += 1

chrome_driver = log_out(chrome_driver)
chrome_driver.close()
