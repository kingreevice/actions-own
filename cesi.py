from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ddddocr
import os

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
    captcha_image.screenshot("/ggg.png")

finally:
    # 关闭WebDriver
    driver.quit()




img_path = os.getcwd() + "/ggg.png"

ocr = ddddocr.DdddOcr()

with open("./ggg.png", 'rb') as f:
    image = f.read()

res = ocr.classification(image)
print(res)


