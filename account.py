from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from page import input_text_value


def log_in(account, tenant, url, driver):
    wait = WebDriverWait(driver, 420)
    driver.get(url['domain'] + url['main'])

    input_text_value(driver, "lims_userNameID", account["username"])
    input_text_value(driver, "lims_passwordID", account["password"])
    driver.find_element_by_id("lims_buttonID").click()

    driver.get(url['domain'] + url['login'])

    select_tenant = Select(driver.find_element_by_xpath("//select[@name='tenantSelect']"))
    select_tenant.select_by_visible_text(tenant)
    driver.find_element_by_xpath("//input[@name='submit'][@type='submit']").click()

    wait.until(EC.title_contains("PFS | Home"))

    return driver


def log_out(url, driver):
    wait = WebDriverWait(driver, 420)
    driver.get(url['domain'] + url['logout'])

    wait.until(EC.title_contains("PFS | Login"))

    return driver
