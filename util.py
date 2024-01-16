# from PIL import Image
# import cv2, ddddocr
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

def get_web_driver():
    chromedriver = "/usr/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)
    driver.implicitly_wait(10) # 所有的操作都可以最长等待10s
    return driver

# 一直等待某元素可见，默认超时10秒（此函数暂时没有使用）
def is_visible(driver, locator, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, locator)))
        return element
    except TimeoutException:
        return False


