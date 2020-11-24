from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from page import input_text_value, select_option


def create_tenant(tenant, url, driver, need_create_tenant=False):
    wait = WebDriverWait(driver, 420)

    driver.get(url['domain'] + url['create-tenant'])

    input_text_value(driver, "name", tenant['name'])
    input_text_value(driver, "17429590", tenant['named-users'])
    input_text_value(driver, "17429591", tenant['barcode'])
    input_text_value(driver, "17429593", tenant['name'])
    select_option(driver, "associatedEntityIdentifier|17429833", tenant['tomcat-service'])

    print(tenant['name'])

    if need_create_tenant:
        driver.find_element_by_xpath("//input[@type='button'][@value='Save']").click()
        wait.until(EC.title_contains("PFS | PLATFORM ACCOUNT Details"))
    else:
        driver.get(url['domain'] + url['list-tenant'])
        wait.until(EC.presence_of_element_located((By.ID, "gridview-1050-body")))

    return driver


def generate_tenant_info(tenant, info):
    tenant['name'] = tenant['name'] + info['flag']
    tenant['named-users'] = info['named-users']
    tenant['barcode'] = tenant['source_schema'] + info['base-account-barcode']
    tenant['tomcat-service'] = info['tomcat-service']
    return tenant
