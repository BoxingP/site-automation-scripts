from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


def input_text_value(driver, select, info):
    textbox = driver.find_element_by_xpath("//*[@id='" + select + "']")
    textbox.send_keys(Keys.CONTROL + "a")
    textbox.send_keys(Keys.BACK_SPACE)
    textbox.send_keys(info)


def select_option(driver, select, info):
    for option in info:
        Select(driver.find_element_by_xpath("//select[@id='" + select + "']")).select_by_visible_text(option)
