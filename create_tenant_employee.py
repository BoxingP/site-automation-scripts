from datetime import datetime

import numpy as np
import pandas as pd
from selenium import webdriver

from account import log_in, log_out
from employee import create_employee
from info import load_config
from tenant import create_tenant, generate_tenant_info


def create_tenants(account, info, url, driver, result, need_create_tenant=False):
    tenant = info['tenant']
    tenant_name_prefix = tenant['name']
    driver = log_in(account, account['tenant'], url, driver)
    tenant_index = tenant['start-point']
    tenant_index_limit = tenant_index + tenant['number']

    while tenant_index < tenant_index_limit:
        current_tenant = {'name': tenant_name_prefix + str(tenant_index), 'source_schema': tenant['source_schema']}
        tenant = generate_tenant_info(current_tenant, info['base'])
        driver, result = create_tenant(tenant, url, driver, result, need_create_tenant)
        tenant_index += 1

    driver = log_out(url, driver)

    return driver, result


def create_employees(account, info, url, driver, result, need_create_employee=False):
    tenant_info = info['tenant']
    tenant_name_prefix = tenant_info['name']
    tenant_index = tenant_info['start-point']
    tenant_index_limit = tenant_index + tenant_info['number']
    employee_info = info['employee']
    employee_index = employee_info['start-point']
    employee_amount = employee_info['number-each-tenant']
    i = 0

    while tenant_index < tenant_index_limit:
        tenant_name = tenant_name_prefix + str(tenant_index)
        driver = log_in(account, tenant_name, url, driver)
        while i < employee_amount:
            employee_index = employee_index + i
            driver, result = create_employee(tenant_name, employee_index, employee_info, url, driver, result,
                                             need_create_employee)
            i += 1
        driver = log_out(url, driver)
        i = 0
        tenant_index += 1
        employee_index += 1

    return driver, result


time_started = datetime.utcnow()

creation_result = pd.DataFrame(columns=['tenant', 'barcode', 'employee', 'password'])
chrome_driver = webdriver.Chrome()
admin_account = load_config("./account.json")['account']['admin']
creation_info = load_config("./creation.json")['creation']
site_url = load_config("./url.json")['url']
chrome_driver, creation_result = create_tenants(admin_account, creation_info, site_url, chrome_driver, creation_result,
                                                True)
chrome_driver, creation_result = create_employees(admin_account, creation_info, site_url, chrome_driver,
                                                  creation_result, True)
chrome_driver.close()
creation_result = creation_result.set_index(['tenant', 'barcode']).apply(lambda x: x.str.split(',').explode()).reset_index()
creation_result.index = np.arange(1, len(creation_result) + 1)
with pd.ExcelWriter('creation_result.xlsx', mode='w') as writer:
    creation_result.to_excel(writer, sheet_name='creation_results')

time_ended = datetime.utcnow()
total_time = (time_ended - time_started).total_seconds()
print('Total time is %ss.' % round(total_time))
