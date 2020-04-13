# -*- coding: utf-8 -*-
import requests
from os.path import basename, isdir
from os import mkdir
from bs4 import BeautifulSoup
import re
class BaikeSpider:
    def __init__(self):
        self.url = r'http://www.baike.com/wiki/'
        self.content = {
            'nr': "",
            'information':{}
        }  # nr 基本介绍， information 基本信息
        self.headers = {
            "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:73.0)Gecko/20100101Firefox/73.0"
        }
  
    def search_word(self, word):
        self.word=word
        self.list_polysemy_word=[]
        self.__parse()
        return self.__get_content()

    def __get_soup(self, url, word):
        try:
            rq = requests.get(url+word, headers=self.headers)
            rq.encoding = rq.apparent_encoding
            soup = BeautifulSoup(rq.text, "lxml")
            return soup
        except:
            return None

    def _parse_tag( self, tag ):
        key = tag.select_one('strong')
        if key is not None:
            key = key.text
        else:
            return '',[]
        values=[]
        spans = tag.select('span')
        for v in spans:
            values.append(v.text)
        return key, values

    def __parse(self):
        soup = self.__get_soup(self.url, self.word)

        if soup == None:
            return
        else:
            qy = soup.select("#polysemyAll>li")
            if qy:
                list_qy = [i.text for i in qy]
                soup = self.__qy_parse(list_qy)

            for p in soup.select('#anchor>p'):
                self.content['nr'] = self.content.get('nr') + p.text

            for td_item in soup.select('#datamodule td'):
                key, values = self._parse_tag( td_item )
                if len(key)>0 and len(values)>0:
                    self.content['information'][key] = values

    def __qy_parse(self, list_qy):
        list_polysemy_word = self.list_polysemy_word  # 关键字匹配
        res = list_qy[0]
        for qy in list_qy:
            for word in list_polysemy_word:
                try:
                    qy.index(word)
                    res = qy
                except:
                    pass

        new_word = self.word+'['+res+']'

        return self.get_soup(self.url, new_word)

    def __clean_text( self, txt ):
        txt = txt.strip()
        txt = txt.replace(',','，')
        txt = txt.replace(':','')
        txt = txt.replace("'", " ")
        txt = txt.replace('"',' ')
        txt = txt.replace('(','（')
        txt = txt.replace(')','）')
        txt = txt.replace('\n','')
        txt = txt.replace('\t','')
        txt = txt.replace('\r','')
        return txt

    def __get_content(self):
        if self.content['nr'] == '':
            return ''
        descript = self.content['nr']
        descript = self.__clean_text(descript)
        ans = '"' + self.word + '",,"' + descript +'"'
        if len(self.content['information'])>0:
            ans = ans + ','
            prop = '"'
            for key, value in self.content['information'].items():
                key = self.__clean_text(key)
                key = key.replace(' ','') #关键词要去掉空格
                if key[-1]=='：' or key[-1]==':':
                    key = key[:-1]
                prop += key + '：“'
                for i in range(len(value)):
                    v = self.__clean_text(value[i])
                    if i<len(value)-1:
                        prop += v + '、'
                    else:
                        prop += v
                prop+='”；'
            prop = prop + '"' 
            ans = ans + prop
        else: #属性为空的情况
            ans = ans+','
        return ans
