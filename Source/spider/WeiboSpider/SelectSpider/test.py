import requests
from bs4 import BeautifulSoup
import json
import os
import time

"""
先获取登录的cookie写入config.json文件里
输入关键字，页数，即可开始爬取。
"""


class WeiSpider:
    def __init__(self, word="", page=10, config_filename="config.json"):
        self.headers = {}
        self.word = word
        self.page = page
        with open(config_filename, "r") as f:
            t = json.loads(f.read())
            self.headers["cookie"] = t["cookie"]
        if word != "":
            try:
                os.mkdir("select_text")
            except FileExistsError:
                pass
            with open("select_text/"+self.word+".txt", "w") as fp:
                pass

    def set_word(self, word):
        self.word = word
        with open("select_text/" + self.word + ".txt", "w") as fp:
            pass

    def set_page(self, num):
        self.page = num

    def get_soup(self, url):
        rq = requests.get(url, headers=self.headers)
        return BeautifulSoup(rq.text, "html.parser")

    def cookie(self):
        try:
            title = self.get_soup(("https://weibo.cn/search/mblog")).title.text
            if title !="搜索结果":
                print("cookie过期或者cookie错误")
                return False
            else:
                return True
        except:
            print("cookie错误")
            return False

    def run_spider(self):
        if self.cookie():
            try:
                os.mkdir("select_text")
            except FileExistsError:
                pass
            print("=" * 50 + "获取网页中" + "=" * 50 + "\n\n\n")
            for i in range(1, self.page + 1):
                print("正在获取关键字:" + self.word + "第" + str(i) + "页微博\n\n")
                url = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword=" + self.word + "&page=" + str(i) + "&sort=time"
                soup = self.get_soup(url)
                self.writer_soup(soup)
                time.sleep(1)

            print(str(self.page) + "个页面获取完成")
            print("=" * 100 + "\n\n\n")

    def writer_soup(self, soup):
        with open("select_text/" + self.word + ".txt", "ab") as fp:
            list_soup = soup.find_all(name='div', attrs={"class": "c"})
            for i in list_soup[6::]:
                try:
                    print("-" * 100 + "\n")
                    name = i.a.text
                    txt = i.find(name="span", attrs={"class": "ctt"}).text
                    fp.write(("用户名：" + name + "\n").encode("utf-8"))
                    fp.write((txt + "\n\n\n").encode("utf-8"))
                    print("用户名：" + name + "\n")
                    print(txt)
                    print("-" * 100 + "\n\n")
                except AttributeError:
                    pass


def main():
    word = input("请输入查询关键字：")
    page = input("请输入页数：")
    spider = WeiSpider(word, int(page))
    spider.run_spider()


if __name__ == '__main__':
    main()


