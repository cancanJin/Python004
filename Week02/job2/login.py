from selenium import webdriver
import time
try:
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get("https://shimo.im")
    time.sleep(5)
    login_button = browser.find_element_by_xpath("//button[@class=\"login-button btn_hover_style_8\"]")
    login_button.click()
    all_window = browser.window_handles
    print(all_window)
    now_window = browser.current_window_handle
    print(now_window)
    #新打开窗口的时候根据下标选择窗口
    #browser.switch_to.window(browser.window_handles[0])
    browser.find_element_by_xpath("//input[@name=\"mobileOrEmail\"]").send_keys("admin")
    time.sleep(1)
    browser.find_element_by_xpath("//input[@name=\"password\"]").send_keys("admin123")
    time.sleep(1)
    browser.find_element_by_xpath("//button[@class=\"sm-button submit sc-1n784rm-0 bcuuIb\"]").click()
    time.sleep(1)
except Exception as e:
    print(e)
finally:
    browser.close()