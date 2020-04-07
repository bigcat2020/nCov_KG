# -*- coding: utf-8 -*-
import os
import time
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
#from pyltp import Parser
#from pyltp import SementicRoleLabeller
from pyltp import NamedEntityRecognizer
    
    
LTP_DATA_DIR = '../../data/ltp_model'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
print(cws_model_path)
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`ner.model`
#par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
#srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl_win.model')  # 语义角色标注模型
user_dict_seg = os.path.join(LTP_DATA_DIR, 'user_seg.txt')
user_dict_pos = os.path.join(LTP_DATA_DIR, 'user_pos.txt')

#省缩略词
PROVINCE_NAME = ['京', '沪', '津', '渝', '黑', '吉', '辽', '蒙','冀','新','甘','青','陕','宁','豫','晋','皖','鄂','湘','苏','川','黔','滇','桂','藏','浙','赣','粤','闽','台','琼','港','澳']
#NOUN_TYPE={'n':'一般名词','nh':'人名','ni':'机构名','ns':'地名','nt':'时间','ws':'外文名词'}
NOUN_LIST=['nh','ni','ns','ws','nt','nz']

class NlpLtp():
    def __init__(self):
        print('Load pyplt models...')
        start = time.time()
        self.segmentor = Segmentor()  # 初始化实例
        self.segmentor.load_with_lexicon(cws_model_path, user_dict_seg)  # 加载模型
        self.postagger=Postagger()
        self.postagger.load_with_lexicon(pos_model_path, user_dict_pos)
         
        #self.parser = Parser() # 初始化实例
        #self.parser.load(par_model_path)  # 加载模型
        #self.labeller = SementicRoleLabeller() # 初始化实例
        #self.labeller.load(srl_model_path)  # 加载模型
        self.recognizer = NamedEntityRecognizer() # 初始化实例
        self.recognizer.load(ner_model_path)
        self.nerdict = dict()
        elapsed = time.time() - start
        print('Load pyplt models finished in ', elapsed)
        
    # 释放模型
    def __del__(self):
        print('Release pyplt models...')
        self.segmentor.release()
        self.postagger.release()
        self.recognizer.release()
        #self.parser.release()
        #self.labeller.release()
        print('Release pyplt models finished.')
        
    def sentence(self, content):
        return SentenceSplitter.split(content)

    def segment(self, text):
        return self.segmentor.segment(text) 

    def postag(self, wordlist):
        return self.postagger.postag(wordlist)

    #def parse(self, wordlist, postags):
    #    return self.parser.parse(wordlist, postags)

    #def role_label(self, wordlist, postags, arcs):
    #    return self.labeller.label(wordlist, postags, arcs)
    def get_keywords(self, txt):
        words = pltobj.segment( txt )
        postags = pltobj.postag( words )
        ners = pltobj.ner( words, postags )
        keywords = list()
        for k, val in ners.items():
            keywords.append(k)
        return keywords
            
    def add_entity(self, word, tag):
        if word in self.nerdict:
            count = self.nerdict[word][1]
        else:
            count = 0
        self.nerdict[word] = [tag, count+1]

    #命名实体结果如下，ltp命名实体类型为：人名（Nh），地名（NS），机构名（Ni）；
    #ltp采用BIESO标注体系。
    #B表示实体开始词，I表示实体中间词，E表示实体结束词，S表示单独成实体，O表示不构成实体。
    def ner(self, wordlist, postags):
        ners = self.recognizer.recognize(wordlist, postags)
        for i in range(0,len(ners)):
            #print( wordlist[i], postags[i], ners[i] )
            if postags[i] in NOUN_LIST:
                word = wordlist[i].strip()
                if len(word)>1:
                    self.add_entity(word, postags[i])

            if ners[i]=='S-Ns' or ners[i]=='S-Nh' or ners[i]=='S-Ni':
                word = wordlist[i].strip()
                if len(word)>1 or word in PROVINCE_NAME: #实体名长度大于1，保存词性
                    self.add_entity(word, postags[i])
        return self.nerdict
    
    def clean_ner(self):
        self.nerdict = dict()

    def get_ner(self):
        return self.nerdict




pltobj = NlpLtp()

if __name__ == '__main__':

    def tes_plt( pltobj, s ):
        words = pltobj.segment( s )
        postags = pltobj.postag( words )
        print(len(words), len(postags))
        ners = pltobj.ner( words, postags )

        ll = pltobj.get_keywords(s)
        print( '实体识别结果：', ll )
        print(ners)
        #return
        arcs = pltobj.ner(words, postags)


        print('分词结果----------------\n')
        print( ' '.join(words) )
        print('词性标注----------------\n')
        print( ' '.join(postags) )
        print('句法分析----------------\n')
        # 打印结果
        print( ''.join(arcs) )
        print( len(arcs), type(arcs) )

        #arc.head 表示依存弧的父节点词的索引。ROOT节点的索引是0，第一个词开始的索引依次为1、2、3…
        #arc.relation 表示依存弧的关系。
        #print('语法角色标注----------------\n')
        #words = ['元芳', '你', '怎么', '看']
        #postags = ['nh', 'r', 'r', 'v']
        #4:SBV       4:SBV   4:ADV   0:HED
        #3 A0:(0,0)A0:(1,1)ADV:(2,2)
        #第一个词开始的索引依次为0、1、2…
        #返回结果 roles 是关于多个谓词的语义角色分析的结果。由于一句话中可能不含有语义角色，所以结果可能为空。
        #role.index 代表谓词的索引， role.arguments 代表关于该谓词的若干语义角色。
        #arg.name 表示语义角色类型，arg.range.start 表示该语义角色起始词位置的索引，arg.range.end 表示该语义角色结束词位置的索引。
        #例如上面的例子，由于结果输出一行，所以“元芳你怎么看”有一组语义角色。 其谓词索引为3，即“看”。这个谓词有三个语义角色，范围分别是(0,0)即“元芳”，(1,1)即“你”，(2,2)即“怎么”，类型分别是A0、A0、ADV。
        #arg.name 表示语义角色关系，arg.range.start 表示起始词位置，arg.range.end 表示结束位置。
        #print( len(roles), type(roles) )
        #for role in roles:
        #    print(role.index, "".join(["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))


    pltobj = NlpLtp()
    start = time.time()


    tes_plt(pltobj, '塞内加尔出现首例输入性新冠肺炎患者，该病患是一名常住塞内加尔首都达喀尔市阿勒马蒂区的法国人。' )
    #test_plt( plt, '元芳你怎么看' )
    tes_plt(pltobj, '李兰娟院士赞扬陕西省援助湖北医疗队。' )
    #test_plt( plt, '据俄罗斯卫星通讯社3日消息，世卫组织在伊朗的一名工作人员被确诊感染新型冠状病毒，病情目前处于中等程度。')


    elapsed = time.time() - start
    print('程序运行总耗时', elapsed)
