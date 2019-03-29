import requests
import json
from lxml import etree
from collections import defaultdict


start_url = "https://college.zjut.cc/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
}
universitys = defaultdict(list)
loca_uni_page = {}


def get_index():
    response = requests.get(url=start_url, headers=headers)
    html = etree.HTML(response.text)
    location = html.xpath("//div[@class='row']/div[6]//a/text()")
    university = html.xpath("//div[@class='row']/div[6]//a/@href")
    for i in range(len(location)):
        loca_uni_page[location[i]] = university[i]
    return loca_uni_page


def get_next_url(kwargs):
    for i in kwargs:
        yield i, kwargs[i]


def get_university(url, province):
        response = requests.get(url=url, headers=headers)
        html = etree.HTML(response.text)
        u = html.xpath("//h4[@class='media-heading']/a/text()")
        universitys[province].extend(u)
        port_url = html.xpath("//a[@class='nxt']/@href")
        if port_url:
            for i in port_url:
                next_url = "https:" + i
                get_university(next_url, province)



def save_as_json(data):
    with open("data.json", "w", encoding="utf-8") as fileobject:
        fileobject.write(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    x = get_index()
    for i in get_next_url(x):
        get_university(i[1], i[0])
        # print(universitys)
    save_as_json(universitys)
        

if __name__ == '__main__':
    main()