# from PIL import Image
import ddddocr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time


#chromedriver.exe 要与chrome 版本号从左到右尽量对应
#chromedriver.exe 要与chrom浏览器放一起
chrome_path = "/usr/bin/chromedriver"
 
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
 
service = Service(executable_path=chrome_path)

driver = webdriver.Chrome(service=service, options=options)

 # 将浏览器窗口设置为全屏
driver.maximize_window()

driver.get("https://i.nosec.org/login?locale=zh-CN&service=https://fofa.info/f_login")

print("程序运行成功")
# 获取网页标题
page_title = driver.title

print("Page Title:", page_title)



img_path = os.getcwd() + "/1.png"

ocr = ddddocr.DdddOcr()

with open("./ggg.png", 'rb') as f:
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
