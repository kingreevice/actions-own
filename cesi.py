from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import ddddocr
import os

# 设置Chrome WebDriver为无头模式
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
# 初始化WebDriver
driver = webdriver.Chrome(options=options)

try:
    # 打开Google首页
    driver.get("https://i.nosec.org/login?locale=zh-CN&service=https://fofa.info/f_login")

    # 打印当前页面标题
    print("Page title: {}".format(driver.title))

     # 等待验证码图片元素出现
    captcha_image = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="captcha_image"]'))
    )

    # 截取验证码图片
   
    screenshot = captcha_image.screenshot_as_png
    # 使用Pillow保存图片
    with open("abj.png", 'wb') as f:
        f.write(screenshot)

finally:
    # 关闭WebDriver
    driver.quit()

ocr = ddddocr.DdddOcr()

with open("abj.png", 'rb') as f:
    image = f.read()

res = ocr.classification(image)
print(res)


