# from PIL import Image
import ddddocr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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

    # 找到搜索框元素并输入关键词
    search_box = driver.find_element("name", "q")
    search_box.send_keys("GitHub Actions with Selenium")
    search_box.send_keys(Keys.RETURN)

    # 等待一些时间以确保页面加载完全
    driver.implicitly_wait(5)

    # 打印当前页面标题
    print("Page title: {}".format(driver.title))

finally:
    # 关闭WebDriver
    driver.quit()




img_path = os.getcwd() + "/ggg.png"

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
