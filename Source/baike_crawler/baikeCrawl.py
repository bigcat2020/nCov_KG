import os
import re
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup

class webCrawl(object):
	def __init__(self,keyword):
		self.polysemy_key_wrod = ['医学','症状']
		self.driver = webdriver.Firefox(executable_path = "./webdriver/geckodriver")
		self.driver.get('http://www.baike.com/')
		self.key_word = []
		self.load_key_word(keyword)
		self.get()


	def check_polysemy(self,html):
		polysemy_bf = html.find_all('ul',id='polysemyAll')
		temp = BeautifulSoup(str(polysemy_bf),'lxml')
		polysemy = temp.find_all('li')
		for j in polysemy:
			print(j.get('class'),j.text)
			for i in self.polysemy_key_wrod:
				if i in j.text and j.get('class') and j.get('class')[0] == 'current':
					return None
				elif i in j.text:
					a = j.find('a')
					url = a.get('href')
					return 'http:'+ url;

	def load_key_word(self,keyword):
		with open(keyword,'r',encoding='utf-8') as file:
			temp = file.read();
		self.key_word = temp.split('\n')

	def get(self):
		for i in self.key_word:
			summary = ""
			jbxx = "基本信息：\n"
			url = 'http://www.baike.com/wiki/' + i;
			print(url)
			self.driver.get(url)
			request = self.driver.execute_script("return document.documentElement.outerHTML")
			html = BeautifulSoup(request,'lxml')
			if html.find('ul',id='polysemyAll'):
				url = self.check_polysemy(html)
				if url:
					self.driver.get(url)
					request = self.driver.execute_script("return document.documentElement.outerHTML")
					html = BeautifulSoup(request,'lxml')
			summary = html.find('div',class_='summary')
			if summary:
				summary = summary.text
			print(summary)
			infor_bf = html.find('div',id='datamodule')
			if infor_bf:
				infor = BeautifulSoup(str(infor_bf),'lxml')
				name  = infor.find_all('strong')
				value = infor.find_all('span')
				for j in range(len(name)):
					print(name[j].text,value[j].text)
					jbxx += name[j].text + value[j].text + '\n'
			if summary:
				summary = str(summary).replace('编辑摘要','')
				print(summary)
				self.write(i,str(summary),str(jbxx))

	def write(self, filename, summary, jbxx):
		with open('./data/'+filename+'.txt', 'w',encoding='utf-8') as file:
			file.write(summary)
			file.write(jbxx)


if __name__ == '__main__':
	crawl = webCrawl('./userdict.txt')

