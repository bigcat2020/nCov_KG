import requests
from lxml import etree
from bs4 import BeautifulSoup
import time
import re
import pandas as pd


class getContents():
    def __init__(self):
        print("开始获取所有的链接")
        self.UserAgent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
        self.starturl = "http://www.moe.gov.cn/was5/web/search?channelid=239993&searchword=&lx=&page="
        self.page = [1, 2]  # 链接分布在两个页面中.....
        self.listurl = []  # 存放所有获取到的url
        self.htmlContent = ""  # 每一个url获取到的网页文本
        self.text = ""  # 存放每一个url的正文
        self.title = ""  # 存放每一个url的标题
        self.time = ""  # 存放每一个url的时间

        # """这里先将标题行写入"""
        self.content = [["标题", "url", "时间", "正文"]]
        file = pd.DataFrame(self.content)
        file.to_csv('out.csv', index=False, header=False, mode='a+', encoding="utf-8")

        # """获取到每一个新闻页面的链接"""
        for i in self.page:
            newstart = self.starturl + str(i)
            htmlContent = requests.get(newstart, headers=self.UserAgent)
            htmlContent = htmlContent.content.decode('utf-8')
            htmlContentXpath = etree.HTML(htmlContent, parser=etree.HTMLParser(encoding='utf-8'))
            self.listurl = self.listurl + htmlContentXpath.xpath('//div[@class="scy_lbsj-right-nr"]/ul/li/a/@href')
            '''
                    可以先读取已经爬取的url存放在一个列表
                    然后与当前获取到的url作对比
                    如果已经有了 则不将当前的url放入listurl中
            '''
        print("获取链接成功,总共",len(self.listurl),"个")

    def getHtmlcontent(self):
        k = 1
        for url in self.listurl:
            print("正在获取第", k, "个网页")
            try:
                r = requests.get(url, headers=self.UserAgent)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                self.htmlContent = r.text
            except:
                print("HTML获取失败")
                while (True):
                    if self.htmlContent == "":
                        print("等待5秒后重新获取~~~~~")
                        time.sleep(5)
                        r = requests.get(url, headers=self.UserAgent)
                        r.encoding = r.apparent_encoding
                        self.htmlContent = r.text
                    else:
                        break
            soup = BeautifulSoup(self.htmlContent, 'html.parser')
            cnn = soup.find_all("p")
            if len(cnn) == 0:
                cnn = soup.find_all("span")
                if len(cnn) == 0:
                    cnn = soup.find_all("div")
            s = ""
            for i in cnn:
                if i.text == None or i.text == "":
                    continue
                s = s + i.text

            # 去除正文中乱七八糟的符号
            s = s.replace("\n", "")
            s = s.replace("\t", "")
            s = s.replace("\u3000", "")
            s = s.replace("\xa0", "")


            self.text = s
            times = re.findall(r'\d{4}-\d{1,2}-\d{1,2}', self.htmlContent)
            try:
                if len(times) == 0:
                    # 如果没有找到上面格式的日期,就用下面这一招
                    times = re.findall(r'\d{4}年\d{1,2}月\d{1,2}日', self.htmlContent)
                    self.time = times[0]
                else:
                    self.time = times[1]
            except:
                # 如果两种日期都没找到,那就是未知了.....
                self.time = "未知"
            # 通过H1标签找到标题
            self.title = soup.find_all("h1")[0].text
            # 将获得的标题 链接 时间 正文 组成列表写入csv
            self.content = [[self.title, url, self.time, self.text]]
            file = pd.DataFrame(self.content)
            file.to_csv('out.csv', index=False, header=False, mode='a+', encoding="utf-8")
            print("第", k, "个网页写入成功")
            k= k + 1


if __name__ == '__main__':
    a = getContents()
    a.getHtmlcontent()


