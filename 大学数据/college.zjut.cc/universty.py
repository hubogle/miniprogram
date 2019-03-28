import requests
import json
from lxml import etree
start_url = "https://college.zjut.cc/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
}
response = requests.get(start_url, headers=headers)
html = etree.HTML(response.text)
result = html.xpath("//ul[@class='list-unstyled row']//li[@class='col-md-4']/a/text()")
result = sorted(result)
# print(result)
with open("data.json", "w", encoding="utf-8") as fileobject:
    fileobject.write(json.dumps(result, indent=2, ensure_ascii=False))
# print(len(result))
