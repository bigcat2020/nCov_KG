from neo_models import KGneo4j
from nlpltp import NlpLtp
import pandas as pd

LTP_DATA_DIR = '../../data/ltp_model'  # ltp模型目录的路径

class KGQA_Parser():
    QUESTION_KEY_WORDS = { #根据关键词来对问题分类 #'如何','怎么','怎样','情况',
        '疫情':['防控','防疫','疫情','措施','政策','策略','监管','确诊','住院','治愈','治好','出院','死亡','去世','逝世','多少人','多少','人数'],
        '实体':['是谁','哪位','什么','哪里','地方','什么是'],
        '知识':['新冠','新型冠状','来源','药物','特效药','治疗','药','疫苗','症状','预防','防护','设备'],
        '未知':[]}
    QUESTION_TYPE = {'疫情','实体','知识','未知'}
    QT_CONDITION = 0
    QT_ENTITY = 1
    QT_KNOWLEDGE = 2
    QT_UNKNOWN = 3
    def __init__(self):
        self.ltp = NlpLtp()
        self.node_frame = pd.read_csv('../../data/csv/out_nodes.csv')
        self.relation_frame = pd.read_csv('../../data/csv/out_relations.csv')
        self.nodes = self.node_frame['nodename'].drop_duplicates() #去掉重复关系名
        self.relations = self.relation_frame['relation'].drop_duplicates() #去掉重复关系名

    def _search_entity( self, words, sentence ): #在句子中找到存在的实体和关系
        found = list()
        for n in self.nodes:
            if sentence.find(n)>=0:
                found.append(n)
        for n in self.relations:
            if sentence.find(n)>=0:
                found.append(n)
        return found

    def get_question_type( self, question):
        #搜索问句中的实体和关系
        found_node = self._search_entity( self.nodes, question)
        found_rel = self._search_entity( self.relations, question)
        #print(question)
        #print('-'*80)
        scores = dict()
        for key,words in self.QUESTION_KEY_WORDS.items():
            for w in words:
                if question.find(w)>=0:
                    if key in scores: #找到一个关键词加1分
                        scores[key] +=1
                    else:
                        scores[key] = 1
                if key in scores and (len(found_node)>0 or len(found_rel)>0):
                    scores[key] +=1 #如果句子中有现存的实体或者关系，是加分项
        #返回score中最大的key，就是问题最可能的类型
        #print(scores)
        max_score = 0
        max_key = '未知'
        for k,s in scores.items():
            if max_score<s:
                max_score = s
                max_key = k
        return max_key

    def parse_question( self, question ):
        #self.search_entity(question)
        seg_array = self.ltp.segment(question)
        pos_array = self.ltp.postag(seg_array)
        q_type = self.get_question_type( question )
        return q_type

    def get_answer( self, array):
        #print(array)
        data_array=[]
        for i in range(len(array)-2):
            if i==0:
                name=array[0]
            else:
                name=data_array[-1]['p.Name']
            print( similar_words[array[i]] )
            print( similar_words[array[i+1]] )
            print( name )
            sql = "match(p)-[r:%s{relation: '%s'}]->(n:Person{Name:'%s'}) return  p.Name,n.Name,r.relation,p.cate,n.cate" % (similar_words[array[i]], similar_words[array[i+1]], name)
            print(sql)

question_samples=[ #    QUESTION_TYPE = {'疫情','实体','知识','未知'}
    '广元的疫情情况如何？', #疫情
    '美国疫情如何？', #疫情
    '四川有哪些防控措施？', #疫情
    '四川信息职业技术学院有哪些防控措施？', #疫情
    '四川信息职业技术学院的防疫政策？', #疫情
    '钟南山是谁？', #实体
    '美国是什么？', #实体
    '尼日利亚是哪里？', #实体
    '新冠肺炎来源？', #知识
    '新冠肺炎是什么？', #知识
    '怎么预防新型冠状肺炎？', #知识
    '哪些药物可以治新冠肺炎？', #知识
    '新冠肺炎有特效药吗？', #知识
    '新冠肺炎有什么药？', #知识
    '新冠病毒有疫苗吗？', #知识
]

parser = KGQA_Parser()
for q in question_samples:
    qp = parser.parse_question(q)
    print(qp)
while True:
    question = input('请输入问题（exit结束）：')
    if question=='exit':
        break
    qp = parser.parse_question(question) #获取问题模板
    print('问题类型是：', qp)
    #get_KGQA_answer(get_target_array(question))
    #answer = get_KGQA_answer(get_target_array(question))
    #print(answer)

"""
n 名词
nr 人名
nr1 汉语姓氏
nr2 汉语名字
nrj 日语人名
nrf 音译人名
ns 地名
nsf 音译地名
nt 机构团体名
nz 其它专名
nl 名词性惯用语
ng 名词性语素
2. 时间词(1个一类，1个二类)
t 时间词
tg 时间词性语素
3. 处所词(1个一类)
s 处所词
4. 方位词(1个一类)
f 方位词
5. 动词(1个一类，9个二类)
v 动词
vd 副动词
vn 名动词
vshi 动词“是”
vyou 动词“有”
vf 趋向动词
vx 形式动词
vi 不及物动词（内动词）
vl 动词性惯用语
vg 动词性语素
6. 形容词(1个一类，4个二类)
a 形容词
ad 副形词
an 名形词
ag 形容词性语素
al 形容词性惯用语
7. 区别词(1个一类，2个二类)
b 区别词
bl 区别词性惯用语
8. 状态词(1个一类)
z 状态词
9. 代词(1个一类，4个二类，6个三类)
r 代词
rr 人称代词
rz 指示代词
rzt 时间指示代词
rzs 处所指示代词
rzv 谓词性指示代词
ry 疑问代词
ryt 时间疑问代词
rys 处所疑问代词
ryv 谓词性疑问代词
rg 代词性语素
10. 数词(1个一类，1个二类)
m 数词
mq 数量词
11. 量词(1个一类，2个二类)
q 量词
qv 动量词
qt 时量词
12. 副词(1个一类)
d 副词
13. 介词(1个一类，2个二类)
p 介词
pba 介词“把”
pbei 介词“被”
14. 连词(1个一类，1个二类)
c 连词
cc 并列连词
15. 助词(1个一类，15个二类)
u 助词
uzhe 着
ule 了 喽
uguo 过
ude1 的 底
ude2 地
ude3 得
usuo 所
udeng 等 等等 云云
uyy 一样 一般 似的 般
udh 的话
uls 来讲 来说 而言 说来
uzhi 之
ulian 连 （“连小学生都会”）
16. 叹词(1个一类)
e 叹词
17. 语气词(1个一类)
y 语气词(delete yg)
18. 拟声词(1个一类)
o 拟声词
19. 前缀(1个一类)
h 前缀
20. 后缀(1个一类)
k 后缀
21. 字符串(1个一类，2个二类)
x 字符串
xx 非语素字
xu 网址URL
22. 标点符号(1个一类，16个二类)
w 标点符号
wkz 左括号，全角：（ 〔 ［ ｛ 《 【 〖 〈 半角：( [ { <
wky 右括号，全角：） 〕 ］ ｝ 》 】 〗 〉 半角： ) ] { >
wyz 左引号，全角：“ ‘ 『
wyy 右引号，全角：” ’ 』
wj 句号，全角：。
ww 问号，全角：？ 半角：?
wt 叹号，全角：！ 半角：!
wd 逗号，全角：， 半角：,
wf 分号，全角：； 半角： ;
wn 顿号，全角：、
wm 冒号，全角：： 半角： :
ws 省略号，全角：…… …
wp 破折号，全角：—— －－ ——－ 半角：--- ----
wb 百分号千分号，全角：％ ‰ 半角：%
wh 单位符号，全角：￥ ＄ ￡ ° ℃ 半角：$
"""