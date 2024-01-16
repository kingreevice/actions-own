from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()

 # 将浏览器窗口设置为全屏
driver.maximize_window()

driver.get("https://bbs.binmt.cc/")

print("程序运行成功")
# 获取网页标题
page_title = driver.title

print("Page Title:", page_title)

# 等待登录窗口加载，可以根据实际情况调整等待时间  
driver.implicitly_wait(10)

#find_element_by_xpath() 不能使用
driver.find_element(By.XPATH,'//*[@id="comiis_nv"]/div/div/div/div[2]/a[1]').click()

driver.implicitly_wait(2)
#根据name定位
driver.find_element("name", "username").send_keys("andy_123")

driver.implicitly_wait(2)
#根据name定位
driver.find_element(By.NAME,"password").send_keys("andy12345678")


driver.implicitly_wait(2)
#根据name定位
driver.find_element(By.NAME,"loginsubmit").click()#登入

#//*[@id="pt"]/div[1]/a[1]
driver.implicitly_wait(2)
#根据文本定位
driver.find_element(By.LINK_TEXT,"签到").click()#签到


time.sleep(5)

# 关闭浏览器
driver.quit()
