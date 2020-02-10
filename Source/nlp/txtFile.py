#文本文档处理模块
import os

#目录搜索类
class pathSearch:
    #判断文件名是否符合条件
    #参数：
    #  fName，要判断的文件名
    #  keyWord，关键词
    #  profix，文件后缀
    #返回值：
    #  True，文件名匹配
    #  False，文件名不匹配
    def matchFileName( self, fName, keyWord, profix ):
        if len(keyWord)>0:
            if not keyWord in fName:
                return False
        if len(profix)>0:
            if len(fName)<=len(profix):
                return False
            if profix!=fName[-len(profix)-1:]!='.'+profix:
                return False
        return True

    #搜索目录下的文件
    #参数：
    #  workPath，str，路径名，不能为空，最后不用加'\'
    #  keyWord, str，文件名包含的关键词，为空则返回所有文件
    #  profix，str，文件类型，为空则返回所有文件，不用加'.'
    #  isSubDir，boolean，是否搜索子目录，默认为true
    #例如 searchFile( 'd:\\data', '中国', 'csv', True )
    #返回值：
    #  返回符合条件的文件名list
    def searchFile( self, workPath, keyWord, profix, isSubDir ):
        if len(workPath)==0:
            return null
        
        fileList = []
        try:
            dirs = os.listdir( workPath ) 
            for f in dirs:
                fPath = workPath + '\\' + f
                if os.path.isdir( fPath ):
                    if isSubDir:
                        subDir = self.searchFile( fPath, keyWord, profix, isSubDir )
                        if subDir!=[]:
                            fileList = fileList + subDir
                else:
                    if self.matchFileName( f, keyWord, profix ):
                        fileList.append(fPath)
        except:
            return []
        return fileList

#纯文本文件处理类
class txtFile:
    content = ''
    #加载一个文本文件
    def load( fName ):
        with f=open(fName, 'r', encoding='utf-8'):
            content = f.read()
        return null
    
    #清理
    def clean( stopwords ):
        return

#csv文件处理类
class csvFile:
    def load( fName ):
        return
    
    def clean( stopwords ):
        return

#测试代码
# ps = pathSearch()
# csvFiles = ps.searchFile( 'd:\\data', '', 'csv', True )
# txtFiles = ps.searchFile( 'd:\\data', '', 'txt', True )
# WeiboFiles = ps.searchFile( 'd:\\data', '广东', 'txt', True )
# print('CSV file ', len(csvFiles), '-------------------------')
# print( csvFiles)
# print('txt file ', len(txtFiles), '-------------------------')
# print( txtFiles)
# print('keyword 广东', len(WeiboFiles), '-------------------------')
# print( WeiboFiles)
