import ddddocr
from util import *

ocr = ddddocr.DdddOcr()

with open("./a.jpg", 'rb') as f:
    image = f.read()

res = ocr.classification(image)
print(res)


driver = get_web_driver()
driver.get("https://www.91tvg.com")
