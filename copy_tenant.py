import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


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


def input_text_value(driver, select, info):
    textbox = driver.find_element_by_xpath("//*[@id='" + select + "']")
    textbox.send_keys(Keys.CONTROL + "a")
    textbox.send_keys(Keys.BACK_SPACE)
    textbox.send_keys(info)


def select_option(driver, select, info):
    for option in info:
        Select(driver.find_element_by_xpath("//select[@id='" + select + "']")).select_by_visible_text(option)


def log_out(url, driver):
    wait = WebDriverWait(driver, 420)
    driver.get(url + "login?cmd=logout&entityType=LIMS")

    wait.until(EC.title_contains("PFS | Login"))

    return driver


def copy_tenant(url, base, tenant, driver, need_create_tenant=False):
    wait = WebDriverWait(driver, 480)
    driver.get(url + "708646210/corelims?cmd=clone&entityType=PLATFORM%20ACCOUNT&entityId=17437965")

    tenant_name = tenant['name'] + base['flag']
    barcode = tenant['code'] + base['base-account-barcode']

    input_text_value(driver, "name", tenant_name)
    input_text_value(driver, "17429590", base['named-users'])
    input_text_value(driver, "17429591", barcode)
    input_text_value(driver, "17429593", tenant_name)
    select_option(driver, "associatedEntityIdentifier|17429833", base['tomcat-service'])

    if need_create_tenant:
        driver.find_element_by_xpath("//input[@type='button'][@value='Save']").click()
        wait.until(EC.title_contains("PFS | PLATFORM ACCOUNT Details"))
    else:
        driver.get(url + "708646210/corelims?cmd=getall&entityType=PLATFORM%20ACCOUNT")
        wait.until(EC.presence_of_element_located((By.ID, "gridview-1050-body")))

    return driver


chrome_driver = webdriver.Chrome()
admin_account = get_file_info("./account.json")['account']['admin']
copy_info = get_file_info("./copy.json")['copy']
site_url = copy_info['url']
for item in copy_info['tenants']:
    chrome_driver = log_in_tenant(admin_account, "PLATFORM ADMIN", site_url, chrome_driver)
    chrome_driver = copy_tenant(site_url, copy_info['base'], item, chrome_driver, True)
    chrome_driver = log_out(site_url, chrome_driver)
chrome_driver.close()
