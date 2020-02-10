# -*- coding:utf-8 -*-
#导入模块
import os
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from goto import with_goto

#定义类
class downloader():
	def __init__(self):
		self.server = 'ynswsjkw.yn.gov.cn' #网站域名
		self.main_url = 'http://ynswsjkw.yn.gov.cn' #文章网站的前缀url 会因网站不同而不同
		self.list_url = ['http://ynswsjkw.yn.gov.cn/wjwWebsite/web/col?id=UU157976428326282067&cn=xxgzbd&pcn=ztlm&pid=UU145102906505319731',\
		'http://ynswsjkw.yn.gov.cn/wjwWebsite/web/col?id=UU157976428326282067&pId=UU145102906505319731&cn=xxgzbd&pcn=ztlm&pid=UU145102906505319731&page=2',\
		'http://ynswsjkw.yn.gov.cn/wjwWebsite/web/col?id=UU157976428326282067&pId=UU145102906505319731&cn=xxgzbd&pcn=ztlm&pid=UU145102906505319731&page=3',\
		'http://ynswsjkw.yn.gov.cn/wjwWebsite/web/col?id=UU157976428326282067&pId=UU145102906505319731&cn=xxgzbd&pcn=ztlm&pid=UU145102906505319731&page=4',\
		'http://ynswsjkw.yn.gov.cn/wjwWebsite/web/col?id=UU157976428326282067&pId=UU145102906505319731&cn=xxgzbd&pcn=ztlm&pid=UU145102906505319731&page=5'
		] #疫情发布的列表主页，用它来获取文章
							#如'http://wst.hainan.gov.cn/swjw/rdzt/yqfk/index.html' ,会因页码不同而不同，还未想到方法（因为每个站点个结构不一样）
		self.articles_url = [] #存放文章的链接
		self.articles_date = [] #存放文章的时间
		self.articles_name = []
		self.browser = webdriver.Firefox(executable_path = "D:\webdriver\geckodriver") #webDriver路径

	#定义获取文章url，title，及发布日期的方法
	def get_artcles_url(self):
		for i in self.list_url:
			self.browser.get(i) #使用浏览器打开页面
			sleep(2) #等待网页加载完成
			request = self.browser.execute_script("return document.documentElement.outerHTML") #将网页所有内容存入requset
			div_bf = BeautifulSoup(request,'lxml')
			div = div_bf.find_all('div',class_='theSimilar')
			a_bf = BeautifulSoup(str(div),'lxml')
			a = a_bf.find_all('a')
			for x in a:
				print(x.get('href'),x.text)
				self.articles_url.append(self.main_url + x.get('href'))
				self.articles_name.append(x.text)
			date_bf = BeautifulSoup(str(div),'lxml')
			date = date_bf.find_all('span')
			for z in date:
				print(z.text)
				self.articles_date.append(z.text)
		print(len(self.articles_url),len(self.articles_name),len(self.articles_date))


	#定义下载文章并写入的方法
	def writer(self):
		path = self.server
		if not os.path.exists(path): #监测文件夹是否存在，否者创建
			os.mkdir(path)
		url_count = len(self.articles_url) #计算url数量以确定循环次数
		for i in range(url_count):
			try:
				self.browser.get(self.articles_url[i])
			except Exception:
				print("url error\n")
				continue
			sleep(2)
			fileName = str(self.articles_date[i]) + str(self.articles_name[i])
			print("filename:",fileName)
			request = self.browser.execute_script("return document.documentElement.outerHTML")
			div_bf = BeautifulSoup(request,'lxml')
			div = div_bf.find_all('div',id='content') #获取div标签
			inner = ""
			for j in div:
				inner += '\n' + j.text
			try:
				with open(path + '\\' + fileName + '.txt','a',encoding='utf-8') as file:
					file.write(inner)
			except Exception:
				print("fileName Error as \"",fileName,"\"\n")
				continue

		print('write Complete')

if __name__ == '__main__':
	dl = downloader()
	dl.get_artcles_url()
	dl.writer()
	print('All Complete')
				



