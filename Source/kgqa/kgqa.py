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
