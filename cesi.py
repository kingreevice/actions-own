# from PIL import Image
import ddddocr
import numpy as np
from retrying import retry
from selenium import webdriver
import os, sys, time, requests
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox') # 解决DevToolsActivePort文件不存在的报错
chrome_options.add_argument('window-size=1920x1080') # 指定浏览器分辨率
chrome_options.add_argument('--disable-gpu') # 谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--headless') # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败

chromedriver = "/usr/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)
driver.implicitly_wait(10) # 所有的操作都可以最长等待10s



img_path = os.getcwd() + "/1.png"

ocr = ddddocr.DdddOcr()

with open("./a.jpg", 'rb') as f:
    image = f.read()

res = ocr.classification(image)
print(res)


driver = get_web_driver()
driver.get("https://fofa.info/")
# 获取网页标题
page_title = driver.title

print("Page Title:", page_title)

driver.find_element_by_xpath('//*[@id="captcha_image"]').screenshot("/cooc.png")

time.sleep(5)

# 关闭浏览器
driver.quit()
