from selenium import webdriver

from account import log_in, log_out
from info import load_config
from tenant import create_tenant, generate_tenant_info

chrome_driver = webdriver.Chrome()
admin_account = load_config("./account.json")['account']['admin']
copy_info = load_config("./copy.json")['copy']
site_url = copy_info['url']
for tenant in copy_info['tenants']:
    chrome_driver = log_in(admin_account, "PLATFORM ADMIN", site_url, chrome_driver)
    tenant = generate_tenant_info(tenant, copy_info['base'])
    chrome_driver = create_tenant(tenant, site_url, chrome_driver, True)
    chrome_driver = log_out(site_url, chrome_driver)
chrome_driver.close()
