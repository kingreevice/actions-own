import json,time
from datetime import datetime

# 获取当前时间
now = datetime.now()




data = {
    "name": "GitHub Actions",
    "description":now
}
print(data)
with open("output.json", "w") as f:
    json.dump(data, f, indent=4)
