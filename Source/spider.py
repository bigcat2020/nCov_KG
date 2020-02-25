import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time


class getContents():
    def __init__(self, filename):
        self.filename = filename
        self.urls = pd.read_csv(self.filename, usecols=['来源链接1'], encoding='utf-8', index_col=0, header=0)
        #self.data2 = pd.read_csv(self.filename, usecols=['消息来源'], encoding='utf-8', index_col=0, header=0)
        self.readurls = list()
        try:
            with open('..\\data\\readurls.txt', 'r', encoding='utf-8') as f:
                self.readurls = f.readlines()
        except:
            urlfile = open('..\\data\\readurls.txt', 'w', encoding='utf-8')
            urlfile.write(' ')
            urlfile.close()

        self.htmltxt = ''
        self.sanyuan = []
        self.laiyuan = ''
        self.times = ''

    def getConn(self):
        for i in range(1, self.urls.shape[0]):
            url = self.urls.index[i-1]
            if pd.isnull( url ):
                continue
            url = url.strip()
            #已读取的url
            if url in self.readurls:
                continue
            self.readurls.append(url)
            self.laiyuan = url
            try:
                kv = {'user-agent': 'Mozilla/5.0'}
                r = requests.get(url, headers=kv)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                self.htmltxt = r.text
            except:
                print("HTML获取失败")
            while (True):
                if self.htmltxt == "":
                    print("等待中....")
                    time.sleep(5)
                    kv = {'user-agent': 'Mozilla/5.0'}
                    r = requests.get(url, headers=kv)
                    r.raise_for_status()
                    r.encoding = r.apparent_encoding
                    self.htmltxt = r.text
                else:
                    break
            soup = BeautifulSoup(self.htmltxt, 'html.parser')
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
            s = s.replace("\n", "")
            s = s.replace("\t", "")
            s = s.replace("\xa0", "")
            times = re.findall(r'\d{4}-\d{1,2}-\d{1,2}', self.htmltxt)
            try:
                if len(times) == 0:
                    times = re.findall(r'\d{4}年\d{1,2}月\d{1,2}日', self.htmltxt)
                    self.times = times[0]
                else:
                    self.times = times[0]
            except:
                self.times = "未知"
            self.sanyuan = [[[self.laiyuan], [self.times], [s]]]
            print( self.laiyuan, self.times )
            urlline = pd.DataFrame([[url]])
            urlline.to_csv('..\\data\\readurls.txt', index=False, header=False, mode='a+')
            file = pd.DataFrame(self.sanyuan)
            file.to_csv('..\\data\\webOutput.csv', index=False, header=False, mode='a+')


if __name__ == '__main__':
    address = getContents('..\\data\\Updates_NC.csv')
    print(address.getConn())