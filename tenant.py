from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from page import input_text_value, select_option


def get_tenant_barcode(driver):
    string = driver.find_element_by_xpath("//*[@id='ci_page_title']/a").text
    return string.split(' (')[0]


def create_tenant(tenant, url, driver, result, need_create_tenant=False):
    wait = WebDriverWait(driver, 540)

    driver.get(url['domain'] + url['create-tenant'])

    input_text_value(driver, "name", tenant['name'])
    input_text_value(driver, "17429590", tenant['named-users'])
    input_text_value(driver, "17429591", tenant['barcode'])
    input_text_value(driver, "17429593", tenant['name'])
    select_option(driver, "associatedEntityIdentifier|17429833", tenant['tomcat-service'])

    if need_create_tenant:
        driver.find_element_by_xpath("//input[@type='button'][@value='Save']").click()
        wait.until(EC.title_contains("PFS | PLATFORM ACCOUNT Details"))
        barcode = get_tenant_barcode(driver)
        result = result.append({"tenant": tenant['name'], "barcode": barcode}, ignore_index=True)
    else:
        driver.get(url['domain'] + url['list-tenant'])
        wait.until(EC.presence_of_element_located((By.ID, "gridview-1050-body")))

    return driver, result


def generate_tenant_info(tenant, info):
    tenant['name'] = tenant['name'] + info['flag']
    tenant['named-users'] = info['named-users']
    tenant['barcode'] = tenant['source_schema'] + info['base-account-barcode']
    tenant['tomcat-service'] = info['tomcat-service']
    return tenant
