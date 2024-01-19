import ddddocr
from util import *
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
