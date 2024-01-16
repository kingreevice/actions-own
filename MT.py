import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
from time import sleep
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)


driver.get("https://bbs.binmt.cc/")

print("程序运行成功")
# 获取网页标题
page_title = driver.title

print("Page Title:", page_title)


driver.quit()
