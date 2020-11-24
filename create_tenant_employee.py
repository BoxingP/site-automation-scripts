from datetime import datetime

from selenium import webdriver

from account import log_in, log_out
from employee import create_employee
from info import load_config
from tenant import create_tenant, generate_tenant_info


def create_tenants(account, info, driver, need_create_tenant=False):
    url = info['url']
    tenant = info['tenant']
    tenant_name = tenant['name']
    driver = log_in(account, "PLATFORM ADMIN", url, driver)
    tenant_index = tenant['start-point']
    tenant_index_limit = tenant_index + tenant['number']

    while tenant_index < tenant_index_limit:
        tenant['name'] = tenant_name + str(tenant_index)
        tenant = generate_tenant_info(tenant, info['base'])
        driver = create_tenant(tenant, url, driver, need_create_tenant)
        tenant_index += 1

    driver = log_out(url, driver)

    return driver


def create_employees(account, info, driver, need_create_employee=False):
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
        driver = log_in(account, tenant_name, url, driver)
        while i < employee_amount:
            employee_index = employee_index + i
            driver = create_employee(tenant_name, employee_index, employee_info, url, driver, need_create_employee)
            i += 1
        driver = log_out(url, driver)
        i = 0
        tenant_index += 1
        employee_index += 1

    return driver


time_started = datetime.utcnow()

chrome_driver = webdriver.Chrome()
admin_account = load_config("./account.json")['account']['admin']
creation_info = load_config("./creation.json")['creation']
chrome_driver = create_tenants(admin_account, creation_info, chrome_driver, True)
chrome_driver = create_employees(admin_account, creation_info, chrome_driver, True)
chrome_driver.close()

time_ended = datetime.utcnow()
total_time = (time_ended - time_started).total_seconds()
print('Total time is %ss.' % round(total_time))
