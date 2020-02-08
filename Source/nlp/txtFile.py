#文本文档处理模块
import os

#目录搜索类
class pathSearch:
    #判断文件名是否符合条件
    #参数：
    #   fName，要判断的文件名
    #   keyWord，关键词
    #   profix，文件后缀
    #返回值：
    #    True，符合条件
    #    False，不符合条件
    def matchFileName( self, fName, keyWord, profix ):
        print( 'Match in' + fName + ' , ' + keyWord.len + ' , ' + profix.len )
        if keyWord.length>0:
            if not keyWord in fName:
                print('不符合 ' + keyWord + '  ' + fName )
                return False
        if profix.length>0:
            if fName.length<=profix.length:
                return False
            print( profix + '   ' + fName + ' :: ' + fName[:profix.length] + '::' +  fName[fName.length-profix.length-1])
            if profix.length!=fName[:length(profix)] or fName[fName.length-profix.length-1]!='.':
                pass # do nothing
            else:
                return F
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
                            fileList.append(subDir)
                else:
                    print( 'Match out' + f + ' , ' + keyWord.length + ' , ' + profix.length )
                    if self.matchFileName( f, keyWord, profix ):
                        print('matched ' + f)
                        fileList.append( fPath )
        except:
            return []
        return fileList


#测试代码
ps = pathSearch()
csvFiles = ps.searchFile( 'd:\\data', '', 'csv', True )
txtFiles = ps.searchFile( 'd:\\data', '', 'txt', True )
WeiboFiles = ps.searchFile( 'd:\\data', '微博', '', True )
print( csvFiles)
print('-------------------------')
print( txtFiles)
print('-------------------------')
print( WeiboFiles)
