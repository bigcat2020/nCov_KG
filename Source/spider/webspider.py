import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time

OUTPUT_FILE = '..\\..\\data\\webOutput.csv'
URL_UPDATE = '..\\..\\data\\inputurls.csv'
URL_FILE = '..\\..\\data\\readurls.txt'
BLACK_LIST = '..\\..\\data\\blacklist.txt'

class WebSpider():
    def __init__(self, filename):
        self.filename = filename
        self.urls = pd.read_csv(self.filename, usecols=['来源链接1'], encoding='utf-8', index_col=0, header=0)
        self.urls.drop_duplicates(subset=['colA', 'colB'], keep='first')
        #self.data2 = pd.read_csv(self.filename, usecols=['消息来源'], encoding='utf-8', index_col=0, header=0)
        #读取已爬过的URL，创建一个字典
        self.urldict = {}
        try:
            with open( URL_FILE, 'r', encoding='utf-8' ) as f:
                for l in f.readlines():
                    self.urldict[l.replace('\n','')] = 1 
        except:
            with open( URL_FILE, 'w', encoding='utf-8' ) as urlfile:
                urlfile.write('\n')
                urlfile.close()
        
        with open(BLACK_LIST, 'r', encoding='utf-8') as f_stop:
            self.stoplist = f_stop.read().split('\n')

        self.htmltxt = ''
        self.sanyuan = []
        self.laiyuan = ''
        self.times = ''

    #从正文中提取时间
    def get_time(self, txt):
        tt = re.findall(r'\d{4}-\d{1,2}-\d{1,2}', txt)
        if len(tt) == 0:
            tt = re.findall(r'\d{4}年\d{1,2}月\d{1,2}日', txt)
            if len(tt) == 0:
                tt = re.findall(r'\{1,2}月\d{1,2}日', txt)
        if len(tt)>0:
            self.times = tt[0]
        else:
            self.times = '未知'
        return self.times
    
    def clean_black_words(self, txt):
        for w in self.stoplist:
            txt = txt.replace( w, '' )
        return txt
    
    def clean_text(self, txt ):
        txt = txt.strip()
        txt = txt.replace('\n', '')
        txt = txt.replace('\r', '')
        txt = txt.replace('\t', '')
        txt = self.clean_black_words( txt )
        return txt

    def spider_url(self, url ):
        try:
            kv = {'user-agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=kv)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            self.htmltxt = r.text
        except:
            print("HTML获取失败")
        retry = 0
        while (True):
            if retry>5:
                break
            retry = retry + 1
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
        return self.clean_text(s)

    #获取内容三元组并保存到csv文件中
    def get_connent(self, outputfile):
        #print(self.urls.shape[0])
        for i in range(1, self.urls.shape[0]):
            url = self.urls.index[i-1]
            if pd.isnull( url ):
                continue
            url = url.strip()
            #已读取的url
            if url in self.urldict:
                print( url + ' 已读取过')
                continue
            self.urldict[url] = 1
            self.laiyuan = url

            #爬取url，获得正文文本
            s = self.spider_url( url )
            if len(s)==0:
                continue

            times = self.get_time( self.htmltxt )
            self.sanyuan = [[[self.laiyuan], [self.times], s]]
            print( self.laiyuan, self.times )
            urlline = pd.DataFrame([[url]])
            urlline.to_csv( URL_FILE, index=False, header=False, mode='a+' )
            file = pd.DataFrame(self.sanyuan)
            file.to_csv( outputfile, index=False, header=False, mode='a+' )
        return '处理完成'


if __name__ == '__main__':
    address = WebSpider(URL_UPDATE)
    print(address.get_connent(OUTPUT_FILE))