#命名实体识别模块 Named Entity Recognition 
import jieba
import jieba.analyse
import pandas as pd

#从文档中提取关键词
class KeyWordExtract:
    __df_clean_content = null
    __df_content = null
    #从多行文本中清除stop words
    def dropStopWords( self, content, stopWords ):
        clean_content=[]
        all_words=[]
        for ct in content:
            line_clean = []
            for line in content:
                if line in stopWrods:
                    continue
                line_clean.append(line)
                all_words.append(line)
            clean_content.append(line_clean)
    
        return clean_content, all_words
    
    #从一段文字中获取top n关键词
    def getKeyWords( self, content, topK ):
        if content.length==0 or topK<1:
            return ''
        
        content_txt=''
        for ct in self.__df_content:
            content_word = ''.join(self.__clean_content)
            content_txt = ' '.join( jieba.analyse.extract_tags(content, topK ,withWeight=False) )
        return content_txt