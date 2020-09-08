from selenium import webdriver
from selenium.webdriver.common.by import By
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


def log_in_admin(account, driver):
    wait = WebDriverWait(driver, 420)
    driver.get("http://corelimslite.thermofisher.cn/")

    username_id = driver.find_element_by_id("lims_userNameID")
    username_id.clear()
    username_id.send_keys(account["username"])

    password_id = driver.find_element_by_id("lims_passwordID")
    password_id.clear()
    password_id.send_keys(account["password"])

    driver.find_element_by_id("lims_buttonID").click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='login']/form/div[@class='form-group']")))

    select_tenant = Select(driver.find_element_by_xpath("//select[@name='tenantSelect']"))
    select_tenant.select_by_visible_text("PLATFORM ADMIN")
    driver.find_element_by_xpath("//input[@name='submit'][@type='submit']").click()

    wait.until(EC.title_contains("PFS | Home"))

    return driver


def log_out(driver):
    wait = WebDriverWait(driver, 420)
    driver.get("http://corelimslite.thermofisher.cn/login?cmd=logout&entityType=LIMS")

    wait.until(EC.title_contains("PFS | Login"))

    return driver


def create_tenant(tenant, driver):
    wait = WebDriverWait(driver, 420)

    driver.get(
        "http://corelimslite.thermofisher.cn/708646210/corelims?cmd=clone&entityType=PLATFORM%20ACCOUNT&entityId=17437965")

    input_name = driver.find_element_by_id("name")
    input_name.send_keys(tenant)

    input_base_account_barcode = driver.find_element_by_id("17429591")
    input_base_account_barcode.send_keys(Keys.CONTROL + "a")
    input_base_account_barcode.send_keys(Keys.BACK_SPACE)
    input_base_account_barcode.send_keys("ACT3@CI_LOOPBACK")

    input_alias = driver.find_element_by_id("17429593")
    input_alias.send_keys(Keys.CONTROL + "a")
    input_alias.send_keys(Keys.BACK_SPACE)
    input_alias.send_keys(tenant)

    select_tomcat = Select(driver.find_element_by_id("associatedEntityIdentifier|17429833"))
    select_tomcat.select_by_value("17430067")
    driver.find_element_by_xpath("//input[@type='button'][@value='Save']").click()

    wait.until(EC.title_contains("PFS | PLATFORM ACCOUNT Details"))

    return driver


login_account = get_login_account("./account")
chrome_driver = log_in_admin(login_account, chrome_driver)

tenant_index = 173
while tenant_index < 177:
    tenant_name = "CLX" + str(tenant_index)
    chrome_driver = create_tenant(tenant_name, chrome_driver)
    tenant_index += 1

chrome_driver = log_out(chrome_driver)
chrome_driver.close()
