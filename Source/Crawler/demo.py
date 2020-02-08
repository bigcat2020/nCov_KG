# -*- coding:utf-8 -*-
"""
	program：国家卫建委疫情防控工作网络爬虫
	author：Kisssss
"""

import os
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from goto import with_goto  #要杜绝goto语句 -yemao


class Downloader():
	"""docstring for Downloader"""
	def __init__(self):
		self.server = 'www.nhc.gov.cn'
		self.main_url = 'http://www.nhc.gov.cn'
		self.model_target = '/xcs/xxgzbd/gzbd_index.shtml'
		self.model_name = []
		self.model_url =[]
		self.article_name = []
		self.article_url = []
		self.article_time = []
	
	def find_model(self):

		#1.创建Chrome浏览器对象，这会在电脑上在打开一个浏览器窗口
		browser = webdriver.Firefox(executable_path = "D:\webdriver\geckodriver")  #程序路径可作为命令行参数输入，这样不同的电脑上都能用 -yemao
		#2.通过浏览器向服务器发送URL请求
		browser.get(self.main_url + self.model_target)
		sleep(2) #sleep时间也不要硬编码，定义为一个常量，便于成语维护 -yemao
		request = browser.execute_script("return document.documentElement.outerHTML")
		h3_bf = BeautifulSoup(request,'lxml')
		h3 = h3_bf.find_all('h3',class_='jkxdtit')
		a_bf = BeautifulSoup(str(h3),'lxml')
		a = a_bf.find_all('a')
		for i in range(1,len(a),2):
			self.model_name.append(a[i].string.replace('\t',''))
			self.model_url.append(self.main_url + a[i].get('href').replace('\t','').replace(" ",""))
		print("get model complete")

	@with_goto
	def find_article_url(self):
		browser = webdriver.Firefox(executable_path = "D:\webdriver\geckodriver")
		for i in self.model_url:
			label .start
			url = str(i)
			print("url:",url)
			browser.get(i)
			sleep(5)
			request = browser.execute_script("return document.documentElement.outerHTML")
			ul_bf = BeautifulSoup(request,'lxml')
			ul = ul_bf.find_all('ul',class_='zxxx_list')
			a_bf = BeautifulSoup(str(ul),'lxml')
			a = a_bf.find_all('a')
			time_bf = BeautifulSoup(str(ul),'lxml')
			time = time_bf.find_all('span')
			for i in a:
				self.article_url.append(i.get('href').replace('\t','').replace(" ",""))
				self.article_name.append(i.get('title').replace('\t','').replace(" ",""))
			for i in time:
				self.article_time.append(i.string)
			next_url_bf = BeautifulSoup(request,'lxml')
			next_url_str = str(next_url_bf.find_all('div',class_='pagediv'))
			if '下一页' in next_url_str:
				next_a = next_url_bf.find_all('a',string='下一页')
				next_url = next_a[0].get('href')
				#next_url = '/' + str(next_url)
				url = str(url).split('/')
				for i in range(len(url)):
					url[i] += '/'
				url[-1] = next_url;
				i = str(url).replace('[','').replace(']','').replace('\'','').replace(' ','').replace(',','').replace('\"','')
				#i = "".join(url)
				print(i,end = '\n')
				goto .start
			print(self.article_url[0])
			self.article_url.append('#')
			self.article_name.append('#')
			self.article_time.append('#')
		print("get article_url complete")

	def get_content(self):
		browser = webdriver.Firefox(executable_path = "D:\webdriver\geckodriver")
		titleNum = 0;
		artlen = len(self.article_url)
		if not os.path.exists(str(self.model_name[titleNum]).replace('\n','')):
			os.mkdir(str(self.model_name[titleNum]).replace('\n',''))
		folderPath = './' + str(self.model_name[titleNum]).replace('\n','')
		for i in range(artlen):
			print("当前:",i,"总共:",artlen)
			if self.article_url[i] == '#':
				titleNum += 1
				if not os.path.exists(str(self.model_name[titleNum]).replace('\n','')):
					os.mkdir(str(self.model_name[titleNum]).replace('\n',''))
				folderPath = './' + str(self.model_name[titleNum]).replace('\n','')
			if(self.article_url[i] != '#'):
				url = self.main_url + str(self.article_url[i])
				print("get url =",url)
				browser.get(url)
				sleep(10)
				request = browser.execute_script("return document.documentElement.outerHTML")
				content_bf = BeautifulSoup(request,'lxml')
				content = content_bf.find_all('p')
				inner = content[0].text
				try:
					with open(folderPath+'\\'+self.article_time[i] + self.article_name[i] +'.txt','a',encoding='utf-8') as file:
						file.write(inner)
				except OSError:
					print("file's name error")
					continue
		print("get_content complete")

if __name__ == '__main__':
	dl = Downloader()
	dl.find_model()
	dl.find_article_url()
	dl.get_content()
	print("complete")