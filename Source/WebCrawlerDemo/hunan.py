# -*- coding:utf-8 -*-
#导入模块
import os
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
#from goto import with_goto

#定义类
class downloader():
	def __init__(self):
		self.server = 'wjw.hunan.gov.cn' #网站域名
		self.main_url = 'http://wjw.hunan.gov.cn' #文章网站的前缀url 会因网站不同而不同
		self.list_url = ['http://wjw.hunan.gov.cn/wjw/qwfb/yqfkgz_list.html'] #疫情发布的列表主页，用它来获取文章
							#如'http://wst.hainan.gov.cn/swjw/rdzt/yqfk/index.html' ,会因页码不同而不同，还未想到方法（因为每个站点个结构不一样）
		self.articles_url = [] #存放文章的链接
		self.articles_date = [] #存放文章的时间
		self.articles_name = []
		self.browser = webdriver.Firefox(executable_path = "D:\webdriver\geckodriver") #webDriver路径

	#定义获取文章url，title，及发布日期的方法
	def get_artcles_url(self):
		for i in self.list_url:
			self.browser.get(i) #使用浏览器打开页面
			sleep(5) #等待网页加载完成
			request = self.browser.execute_script("return document.documentElement.outerHTML") #将网页所有内容存入requset
			div_bf = BeautifulSoup(request,'lxml')
			div = div_bf.find_all('div',class_='bd_new bd_a80')
			span_bf = BeautifulSoup(str(div),'lxml')
			span = span_bf.find_all('span')
			date_bf = BeautifulSoup(str(span),'lxml')
			date = date_bf.find_all('voice')
			for j in date:
				self.articles_date.append(j.text)
			a_bf = BeautifulSoup(str(div),'lxml')
			a = a_bf.find_all('a')
			for k in a:
				self.articles_url.append(self.main_url+k.get('href'))
			voice_bf = BeautifulSoup(str(a),'lxml')
			voice = voice_bf.find_all('voice')
			for l in voice:
				self.articles_name.append(l.text)
			print(self.articles_name)
	#定义下载文章并写入的方法
	def writer(self):
		path = self.server
		if not os.path.exists(path): #监测文件夹是否存在，否者创建
			os.mkdir(path)
		url_count = len(self.articles_url) #计算url数量以确定循环次数
		for i in range(url_count):
			print("i=%d,urlcount=%d"%(i,url_count))
			print("url = ",self.articles_url[i],end="\n")
			self.browser.get(self.articles_url[i])
			sleep(5)

			fileName = str(self.articles_date[i]) + str(self.articles_name[i])
			request = self.browser.execute_script("return document.documentElement.outerHTML")
			p_bf = BeautifulSoup(request,'lxml')
			p = p_bf.find_all('div',id='j-show-body') #获取p标签
			inner = ""
			for x in p:
				inner += '\n' + x.text
			if not os.path.exists(path): #监测文件夹是否存在，否者创建
				os.mkdir(path)
			try:
				with open(path + '\\' + fileName +'.txt','a',encoding='utf-8') as file:
					file.write(inner)
			except Exception:
				print("fileName Error as \"",fileName,"\'\"\n")
				continue

		print('write Complete')

if __name__ == '__main__':
	dl = downloader()
	dl.get_artcles_url()
	dl.writer()
	print('All Complete')
				



