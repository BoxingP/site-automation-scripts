from selenium import webdriver

from account import log_in, log_out
from info import load_config
from tenant import create_tenant, generate_tenant_info

chrome_driver = webdriver.Chrome()
admin_account = load_config("./account.json")['account']['admin']
copy_info = load_config("./copy.json")['copy']
url = load_config("./url.json")['url']
for tenant in copy_info['tenants']:
    chrome_driver = log_in(admin_account, admin_account['tenant'], url, chrome_driver)
    tenant = generate_tenant_info(tenant, copy_info['base'])
    chrome_driver = create_tenant(tenant, url, chrome_driver, True)
    chrome_driver = log_out(url, chrome_driver)
chrome_driver.close()
