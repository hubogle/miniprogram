#!/usr/bin/env python
import requests
from lxml import etree
import csv
import time
import logging
"""
中学学校采集地址：http://school.zhongkao.com
目前只采集了，省份，市区，学校名称两种信息。
"""

class HighSchool:
	def __init__(self):
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
		}
		self.index_url = 'http://school.zhongkao.com/'
		logging.basicConfig(level=logging.DEBUG, filename='school.log', filemode='a')		

	# 首先获取省份
	def get_province(self) -> None:
		try:
			response = requests.get(url = self.index_url, headers = self.headers)
			if response.status_code == 200:
				HTML = etree.HTML(response.text)
				nodes = HTML.xpath("//div[@class='inbox fl']//a[position() > 1]")
				for node in nodes:
					name = node.xpath("./text()")[0]
					url = node.xpath("./@href")[0]
					self.get_city(name, url)
		except Exception as e:
			logging.warning(e)

	# 获取市区
	def get_city(self, province_name:str, province_url:str) -> None:
		try:
			response = requests.get(url = province_url, headers = self.headers)
			if response.status_code == 200:
				HTML = etree.HTML(response.text)
				nodes = HTML.xpath("//p[@class='tm10'][1]/a[position() > 1]")
				for node in nodes:
					name = node.xpath("./text()")[0]
					url = node.xpath("./@href")[0]
					self.get_school_name(province_name, name, url)
		except Exception as e:
			logging.warning(e)

	# 获取学校名称
	def get_school_name(self, province_name:str, city_name:str, city_url:str):
		try:
			response = requests.get(url = city_url, headers=self.headers)
			if response.status_code == 200:
				HTML= etree.HTML(response.text)
				nodes = HTML.xpath("//section[@class='w725 fl']/article")
				for node in nodes:
					name = node.xpath("./dl//h3/a/text()")[0]
					infos = [province_name, city_name, name]
					self.save_file(infos)
					print(','.join(infos) + '：保存成功')
				time.sleep(1)
				next_url = HTML.xpath("//section[@class='w725 fl']/nav/a[last()]/@href")
				if next_url:
					self.get_school_name(province_name, city_name, next_url[0])
		except Exception as e:
			logging.warning(e)
	
	def save_file(self, infos):
		with open('./data/high_school.csv', 'a', encoding='utf-8') as fp:
			f = csv.writer(fp)
			f.writerow(infos)

	def run(self):
		self.get_province()

if __name__ == "__main__":
	school = HighSchool()
	school.run()
