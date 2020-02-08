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
			li_bf = BeautifulSoup(request,'lxml') #转换为bs4类型
			li = li_bf.find_all('li') #文章的url都是存储在li标签中，将所有标签都导出到li
			a_bf = BeautifulSoup(str(li),'lxml')
			a = a_bf.find_all('a') #进一步将a标签提取出来
			voice_bf = BeautifulSoup(str(a),'lxml')
			voice = voice_bf.find_all('voice')
			for j in a:
				self.articles_url.append(self.main_url + str(j.get('href')).strip('.')) #获取a标签中的url
				#self.articles_name.append(str(j.get('title'))) #获取a标签的title作为文章名
			for z in voice:
				self.articles_name.append(self.main_url + str(z.text))
			span_bf = BeautifulSoup(str(li),'lxml')
			span = span_bf.find_all('span') #发布日期存放在li->span中
			for k in span:
				self.articles_date.append(k.text)
		print(self.articles_url)
		print('get_artcles_url as Complete')
		print("\n\n\n",len(self.articles_date),len(self.articles_url),len(self.articles_name),"\n\n\n")
		#sleep(600)

	#定义下载文章并写入的方法
	def writer(self):
		path = self.server
		if not os.path.exists(path): #监测文件夹是否存在，否者创建
			os.mkdir(path)

		index = -1
		url_count = len(self.articles_url) #计算url数量以确定循环次数
		print("urlCount=",url_count,end='\n')
		for i in range(url_count):
			index += 1
			print("i=%d,index=%d,urlcount=%d"%(i,index,url_count))
			if index >= url_count:
				break
			if str(self.articles_name[index]) == 'None':
				self.articles_name.pop(0)
				self.articles_url.pop(0)
				index = index - 1
				continue
			print("url = ",self.articles_url[index],end="\n")
			self.browser.get(self.articles_url[index])
			sleep(5)

			fileName = str(self.articles_date[index]) + str(self.articles_name[index])
			request = self.browser.execute_script("return document.documentElement.outerHTML")
			p_bf = BeautifulSoup(request,'lxml')
			p = p_bf.find_all('p') #获取p标签
			inner = ""
			for l in p:
				inner += l.text
			print("self.articles_name[index] = ",self.articles_name[index])
			print("inner = ",inner,end="\n")
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
				



