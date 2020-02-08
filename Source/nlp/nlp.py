#NLP自然语言处理模块
#模块功能
#1.读取指定目录所有文本文件
#2.文本预处理（去除
#3.文件标题及文本进行分词处理（分词、词性）
#4.识别句子，实体，关系
#5.输出三元组
#创建文件 2020-2-8，叶茂

from txtFile import pathSearch, txtFile, csvFile

#知识图谱自然语言处理库
class ChineseNLP:
    __txtPath=''
    
    #构造函数
    #参数: txtPath, 文本文件目录
    def __init__(self, txtPath):
        __txtPath = txtPath
    
    #读取一个文本文件
    def readTxtFile( txtFile ):
        return
    
    #读取目录下所有文本文件
    def loadPath( txtPath ):
        return

    #文本预处理
    def cleanTxt( txt ):
        return
    
    #从一段文本中分出句子列表
    def getSentense( txt ):
        return
    


    


