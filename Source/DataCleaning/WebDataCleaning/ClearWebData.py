import os
from time import sleep
import re
"""
    1.获取目录地址
    2.获取文件名
    3.剔除不必要的信息
    4.存储
    是否使用双指针？中部数据较为重要，“正走反走”
"""
class MakeClear(object):
    def __init__(self,targetPath,storePath):
        self.filename = []
        self.inner_list = []
        self.inner = ""
        self.key = ['2020年','截至','报告','冠状','例','确诊','观察','患者']
        self.popList = []
        self.pathList = []
        self.targetPath = targetPath
        self.storePath = storePath

    def GetDirPath(self):
        if os.path.exists(self.targetPath):
            os.chdir(self.targetPath)
        else:
            os.mkdir(self.targetPath)
            os.chdir(self.targetPath)
        self.pathList = os.listdir(self.targetPath)
        print("GetDirPath Complete")


    def check(self):
        print('check')
        self.inner_list = []
        #self.inner_list = self.inner.split(',')
        self.inner_list = re.split(' |。|,|\\n|\\u3000',self.inner)#放弃使用str split，而采用re.split
        print(self.inner_list)
        self.popList = []
        for i in range(len(self.inner_list)):
            flag = 0
            for j in self.key:
                if j not in self.inner_list[i]:
                    flag += 1
                if flag == len(self.key):
                    self.popList.append(i)
            # if flag!=len(self.key):  """正反一遍放弃"""
            #     break

        # for i in range(len(self.inner_list)-1,-1,-1):
        #     flag = 0
        #     for j in self.key:
        #         if j not in self.inner_list[i]:
        #             flag += 1
        #         if flag == len(self.key):
        #             self.popList.append(i)
        #     if flag!=len(self.key):
        #         break
        self.popList = list(set(self.popList))
        self.popList.sort(reverse=True)
        print("popList",self.popList)
        for x in self.popList:
            self.inner_list.pop(x)
        self.inner = "".join(self.inner_list)
        print(self.inner)

    def getInner(self):
        print('1')
        for i in self.pathList:
            print('2')
            self.filename = []
            if os.path.isdir(i):
                self.filename = os.listdir(i)
                os.chdir(i)
            else:
                print(i,"not is a dir")
                continue
            for j in self.filename:
                self.inner = ""
                self.inner_list = []
                if '.txt' not in j:
                    print(j,"not is a .txt file")
                try:
                    with open(j,'r',encoding='utf-8') as file:
                        self.inner = file.read().replace('\t','\t，').replace(" ",' ，').replace('\u3000','\u3000，').replace('，','，,')

                except Exception:
                    print("can not open file ")
                    continue
                self.check()
                self.writer(i,j)
                os.chdir(self.targetPath+'\\'+i)
            os.chdir('../')


        # self.inner = ""
        # with open(self.filename[0],'r',encoding='utf-8') as file:
        #     self.inner = file.read().replace('\n','').replace('\t','').replace(" ",'').replace('\u3000','').replace('，','，,')

    def writer(self,levelTwoPath,filename):
        os.chdir(self.storePath)
        if not os.path.exists(levelTwoPath):
            os.mkdir(levelTwoPath)
        try:
            filename = self.storePath+'\\'+levelTwoPath+'\\'+filename
            print(filename)
            with open(filename,'a',encoding='utf-8') as file:
                print("entered")
                file.write(self.inner.replace('\n',',').replace('\t',',').replace(" ",'').replace('\u3000',',').replace('，',','))
        except Exception:
            print("Write has Error")

if __name__ == '__main__':
    mk = MakeClear('C:\\Users\\WORKSTATION\\Desktop\\nCovData\\网页信息汇总\\data','C:\\Users\\WORKSTATION\\Desktop\\nCovData\\网页信息汇总\\Scripts\\data')
    mk.GetDirPath()
    mk.getInner()
    print("All Complete")
        