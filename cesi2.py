from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# 设置Chrome WebDriver为无头模式
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# 初始化WebDriver
driver = webdriver.Chrome(options=options)

try:
    # 打开网页
    driver.get("https://i.nosec.org/login?locale=zh-CN&service=https://fofa.info/f_login")  # 替换成你的网页地址

    # 等待验证码图片元素出现
    captcha_image = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="captcha_image"]'))
    )

    # 截取验证码图片
    screenshot = captcha_image.screenshot_as_png

    # 确保目录存在
   image_path = os.path.join(os.path.dirname(__file__), "captcha.png")
   with open(image_path, 'wb') as f:
       f.write(screenshot)

print("验证码图片已保存到:", image_path)

finally:
    # 关闭WebDriver
    driver.quit()



