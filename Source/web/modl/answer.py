import jieba
import jieba.posseg
from modl.neo_models import neodb
import pandas as np
from modl.cilin import CiLin

class Answer:
    def __init__(self):
        # 初始化
        list_word = ["新冠肺炎", "确诊人数", "死亡人数", "治愈人数", "疫情", "防疫措施", "武汉肺炎"]  # 添加某些必要的词
        self.add_words(list_word)

        self.cilin = CiLin() #词林类，用来搜索近义词
        synset = set()
        for w, sset in self.cilin.synonymdict.items():
            synset.update(sset)
        
        self.add_words(synset)

        print('Loading database for nodes and properties...')
        self.zs_words = set(np.read_csv("static/data/out_nodes.csv")['nodename'])  # 获取数据库实体名列表
        #self.add_words(self.zs_words)  # 添加数据库的的实体名词

        cs = np.read_csv("static/data/out_nodes.csv")['propertytext']
        attributes = []
        for i in cs:
            try:
                j = i.split("”；")
                for x in j:
                    key, value = x.split(": “")
                    attributes.append(key)
            except:
                pass

        self.attributes = set(attributes)  # 实体属性列表
        self.add_words(self.attributes)

        self.key_words = ["确诊人数", "死亡人数", "治愈人数", "疫情", "防疫措施"]  # 疫情关键词列表

    def add_words(self, list_word):  # 添加词
        if type(list_word) is str:
            if len(list_word)<12:
                jieba.add_word(list_word,len(list_word)*100) #词频
        else:
            for word in list_word:
                if len(word)<12:
                    jieba.add_word(word,len(word)*100) #词频

    def get_key_words(self, txt):  # 提取文本中的疫情 关系 关键词
        words = []
        for word in jieba.cut(txt):
            if word in self.key_words:
                words.append(word)

        return words

    def get_zs_word(self, txt):  # 提取文本中的 实体 关键词
        words = []
        for w in jieba.cut(txt):
            if w in self.zs_words:
                words.append(w)
        
        if len(words)==0: #正向搜索失败，再开始反响搜索
            for w in self.zs_words:
                if w in txt:
                    words.append(w)

        return words

    def get_dm(self, text):  # 提取文本中的 地名
        city = ""
        for key, tag in jieba.posseg.cut(text):
            if tag == 'ns' or tag == 'nz' or tag == 'nt':
                city = key

        return city

    def get_node_attributes(self, text):  # 提取文本可能的属性值，如履历，性别，年龄这些，针对判别为实体的
        words = []
        for word in jieba.cut(text):
            if word in self.attributes:
                words.append(word)

        if len(words)==0: #正向搜索失败，再开始反响搜索
            for w in self.attributes:
                if w in txt:
                    words.append(w)

        return words

    def get_node_text(self, st_name):  # 从数据库查询该实体基本信息文本
        answer = neodb.match_item_by_name(st_name)
        properties = answer[0]['n']['properties']
        return properties

    def get_attribute(self, st_name, attribute_name):  # 提取数据库数据的实体属性值
        try:
            properties = self.get_node_text(st_name).split("”；")
            for i in properties:
                key, value = i.split(": “")
                if key == attribute_name:
                    return value
        except:
            pass

        return ""

    def get_num(self, city, index):  # 获取city地区的确诊人数， index 1为确诊， 2为治愈， 3为死亡
        cs = np.read_csv("static/map_csv/china.csv")
        for i in cs.values:
            if i[0] == city:
                return i[0+index]

        cs = np.read_csv("static/map_csv/china_city.csv")
        for i in cs.values:
            if i[1] == city:
                return i[1+index]

        cs = np.read_csv("static/map_csv/world.csv")
        for i in cs.values:
            if i[0] == city:
                return i[1+index]

    def yq_answer(self, text):  # 类型为疫情的操作
        words = self.get_key_words(text)
        ans = []
        num_dict = {
            1:['确诊人数','确诊病例','累计确诊','确诊数','确诊总数'],
            2:['治愈人数','出院人数','治愈病例','累计治愈','累计出院','出院病例','治愈数','出院数'],
            3:['死亡人数','死亡病例','死亡数','累计死亡'],
        }

        for key,words in num_dict.items():
            for w in words:
                if w in text:
                    city = self.get_dm(text)
                    num = self.get_num(city, key)
                    ans.append(words[0]+str(num))
                    break

        try:
            cypher = self.yq_cypher(text)
            print(cypher)
            data = neodb.graph.run(cypher).data()

            for i in data:
                ans.append(i['n2']['name']+":"+data[0]['n2']['properties'])
        except:
            pass

        return ans

    def zs_answer(self, text):  # 类型为知识的操作
        words = self.get_node_attributes(text)
        zs_words = self.get_zs_word(text)
        print(zs_words, words)
        ans = []
        for zs_word in zs_words:
            for word in words:
                value = self.get_attribute(zs_word, word)
                if value:
                    ans.append(word+": "+value)

        if not ans:
            res = self.get_node_text(zs_words[0])
            if res:
                ans.append("基本信息" + "：" + res)

        return ans

    def yq_cypher(self, text):
        words = self.get_key_words(text)
        city = self.get_dm(text)

        wh = "["
        if "疫情" in words:
            a = ""
            if len(wh)==1:
                a = "\"疫情\""
            else:
                a = ",\"疫情\""

            wh = wh+a

        if "防疫措施" in words:
            a = ""
            if len(wh) == 1:
                a = "\"防疫措施\""
            else:
                a = ",\"防疫措施\""

            wh = wh + a

        wh = wh+"]"
        cypher = "MATCH (n1:term{name:\""+city+"\"})-[r:rel]-(n2) WHERE r.relation IN " + wh + " RETURN n2"

        return cypher


answer = Answer()








