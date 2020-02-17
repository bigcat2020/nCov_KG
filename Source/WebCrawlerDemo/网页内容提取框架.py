import csv

import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import jieba


class getContents():
    # 获取html页面
    def getHTMLText(self, url):
        try:
            kv = {'user-agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=kv)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            return ""
    # 1获取标题
    def getTitle(self, str):
        try:
            soup = BeautifulSoup(str, 'html.parser')
            title = soup.find('title')
            return title.string
        except:
            return ""

    # 2获得来源
    def getSource(self):
        return '省卫健委'

    # 3获得发布时间
    def getTime(self, str):
        try:
            times = re.findall(r'\d{4}-\d{1,2}-\d{1,2}', str)
            if len(times) == 0:
                return "2020"
            else:
                return times[0]
        except:
            return '2020'
    # 4获取正文
    def getContent(self, str):
        try:
            soup = BeautifulSoup(str, 'html.parser')
            p = soup.find_all('p')
            if len(p) == 0:
                p = soup.find_all("span")
                if len(p) == 0:
                    p = soup.find_all("div")
            s = ""
            for i in p:
                if i.text == None or i.text == "":
                    continue
                s = s + i.text
            return s
        except:
            return "1"
    # 5进行分词
    def getParticiple(self, str):
        try:
            fenci = jieba.lcut(str)
            return fenci
        except:
            return ''
    # 写入内容


def main():
    with open("url.txt", 'r', encoding="utf-8") as f:
        url = f.read().split('\n')
        address = getContents()
        data = []
        for i in url:
            print(i)
            htmltxt = address.getHTMLText(i)
            while(True):
                if htmltxt == "":
                    print("等待中....")
                    time.sleep(5)
                    htmltxt = address.getHTMLText(i)
                else:
                    break
            title = address.getTitle(htmltxt)
            times = address.getTime(htmltxt)
            content = address.getContent(htmltxt)
            participle = address.getParticiple(content)
            data.append([title, "省卫健委", times, content, participle])
        try:
            file = pd.DataFrame(data)
            file.to_csv('out.csv',  index=False, header=False)
            print("成功")
        except:
            print("失败")
main()