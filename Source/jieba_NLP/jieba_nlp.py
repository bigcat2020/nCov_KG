import jieba.posseg as posg
import os
import csv

"""
功能：

主目录：
    四川：
        。。。.txt
    广西:
        。。。.txt
给定主目录路径/自动将主目录下所有目录里的txt文件解析生成txt和csv文件。
    

"""


class Nlp:
    def __init__(self, path):  # path,主目录的路径
        self.path = path
        self.list_mkdir = os.listdir(path)  # 将主目录下的目录列表保存下来
        print(self.list_mkdir)

    def get_list_txt(self, mkdir_name):
        """
        获取次目录下的txt文件
        :param mkdir_name:
        :return:
        """
        res = []
        list_a = os.listdir(self.path+mkdir_name)  # 次目录里的所有文件
        # print(list_a)
        for i in list_a:
            if i[len(i)-3::] == "txt":
                res.append(i)
        return res

    def cut_write(self, filename):
        """
        文本分词及词性解析
        :param filename:
        :return:
        """
        filename = self.path+filename
        with open(filename, "rb") as f:
            result = list(posg.cut(f.read()))  # 取一次就没了
            # txt
            with open(filename[:-4:]+"nlp.txt", "ab") as outtxt:
                temp = ""
                for i, j in result:
                    print(i + "\t" + j)
                    if j == "m" and temp != "x":
                        outtxt.write((i + '\t' + "q" + '\n').encode("utf-8"))
                    else:
                        outtxt.write((i + '\t' + j + '\n').encode("utf-8"))
                    temp = j
            print("-"*100)
            # csv
            with open(filename[:-4:]+"nlp.csv", "w", encoding="utf-8", newline='') as outcsv:
                csv_write = csv.writer(outcsv)
                temp = ""
                for i, j in result:
                    print(i + "," + j)
                    if j == "m" and temp != "x":
                        csv_write.writerow([i, "q"])
                    else:
                        csv_write.writerow([i, j])
                    temp = j


    def run_nlp(self):
        """
        遍历所有的txt文件，并执行解析操作
        :return:
        """
        for i in self.list_mkdir:
            list_txt = self.get_list_txt(i)
            for j in list_txt:
                self.cut_write(i+"/"+j)


def main():
    nlp = Nlp("C:/Users/lenovo/Desktop/微博信息提取汇总/")
    nlp.run_nlp()


if __name__ =="__main__":
    main()

