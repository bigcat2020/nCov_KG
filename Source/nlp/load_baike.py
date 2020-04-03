import csv
import re
import os
import jieba
import jieba.posseg as pseg

WORD_TYPE=['人物','省','国家','机构']
g_nodedict = dict() #实体字典
g_relationdict = dict() #关系字典


SYNONYM_WORDS = ['别名','别称','简称','又称']
#nr 人名
#nr1 汉语姓氏
#nr2 汉语名字
#nrj 日语人名
#nrf 音译人名
#ns 地名
#nsf 音译地名
#nt 机构团体名
def get_region_type(word):
    zt = word[len(word)-1:]
    if zt=='区':
        return '区'
    elif zt=='市':
        return '市'
    elif zt=='县':
        return '县'
    elif zt=='盟':
        return '盟'
    elif zt=='旗':
        return '旗'
    else:
        return '国家'

def guess_word_type(word,prop_dict):
    wpos =pseg.cut( word )
    for w in wpos:
        if word==w.word:
            if w.flag=='nr':
                return '人物'
            elif w.flag=='nt':
                return '机构'
            elif w.flag=='ns':
                return get_region_type(word)
    if '性别' in prop_dict:
        return '人物'
    if '行政类别' in prop_dict:
        return prop_dict['行政类别']
    else:
        return get_region_type(word)
    return ''

def clean_node(txt):
    txt = txt.replace('"','')
    txt = txt.strip()
    return txt

def clean_name(txt):
    txt = txt.replace('"','')
    txt = txt.replace('《','')
    txt = txt.replace('》','')
    txt = txt.replace(' ','')
    return txt

class KGNode():
    def __init__(self, nodename, nodeclass, nodedesc, propdict):
        self.node_id=''
        self.node_name = nodename
        self.node_class = nodeclass
        self.node_desc = nodedesc
        self.prop_dict = propdict

    def __init__(self, nodeid, nodename, nodeclass, nodedesc, propdict):
        self.node_id = nodeid
        self.node_name = nodename
        self.node_class = nodeclass
        self.node_desc = nodedesc
        self.prop_dict = propdict
    
    def get_synonyms(self):
        synset = [self.node_name]
        for k,v in self.prop_dict.items():
            if k in SYNONYM_WORDS:
                v = v.strip()
                v = v.replace('、',' ')
                v = v.replace('，',' ')
                v = v.replace('.','')
                v = v.replace('‘','')
                v = v.replace('’','')
                v = v.replace('（','')
                v = v.replace('）','')
                v = v.replace('“','')
                v = v.replace('”','')
                v = v.replace('。','')
                v = v.replace('等','')
                v = v.replace(',',' ')
                vlist = v.split()
                for x in vlist:
                    if x in synset:
                        continue
                    else:
                        synset.append(x)
        return synset

class KGRelation():
    def __init__(self, relation, node1, node2):
        self.relation=relation
        self.node1 = node1
        self.node2 = node2
        self.prop = ''

class KGManager():
    def __init__(self):
        self.baike_id=0
        self.node_dict = dict()
        self.synonym_dict = dict()
        self.baike_dict = dict()
        self.relation_dict = dict()

    def update_synonym(self, node):
        syns = node.get_synonyms()
        self.synonym_dict[node.node_name] = syns

    def add_baike_node(self, node ):
        self.update_synonym(node)
        #增加一个百科的id
        if node.node_name in self.node_dict:
            node1 = self.node_dict[node.node_name]
            node1.prop_dict = node.prop_dict
            self.node_dict[node.node_name] = node1
            return
        self.baike_id += 1
        node.node_id = 'baike/R{}'.format(self.baike_id)
        self.node_dict[node.node_name] = node

    def get_node_name( self, nodename ):
        if nodename in self.node_dict:
            return self.node_dict[nodename]
        else:
            return None
    
    def parse_proptext(self, ntype,prop):
        #读取属性，分解出属性名和属性值
        prop_dict = dict() 
        pr1 = prop.split('”；')
        for p in pr1:
            pr2 = p.split('：“')
            if len(pr2)==2:
                prop_dict[pr2[0]] = pr2[1].strip()
        return prop_dict

    def parse_node(self, item):
        if len(item)<4:
            return None
        node_id = clean_node(item[0])
        p = node_id.find('baike/R')
        if p>=0: #更新id
            id = int(node_id[p+7:])
            if self.baike_id<id:
                self.baike_id=id+1
        node_name = clean_name(item[1])
        node_class = clean_node(item[2])
        node_desc = clean_node(item[3])
        prop_dict = dict()
        return KGNode(node_id, node_name, node_class, node_desc, prop_dict)
    
    def load_node_csv( self, csvfile ):#id,nodename,nodeclass,propertytext
        with open(csvfile, 'r', encoding='utf8') as f:
            rows = csv.reader(f)
            i=0
            for item in rows:
                i+=1
                if i>1:
                    node = self.parse_node(item)
                    if node is not None:
                        self.update_synonym(node)
                        self.node_dict[node.node_name] = node

    def parse_baike(self, item):
        if len(item)<4:
            return None
        node_name = clean_name(item[0])
        node_class = clean_node(item[1])
        node_desc = clean_node(item[2])
        node_prop = clean_node(item[3])
        prop_dict = self.parse_proptext(node_class,node_prop)
        if node_class=='': 
            node_class = guess_word_type(node_name, prop_dict)
        if node_class=='': #如果没有类别名
            print(node_name,' ！！！')
        return KGNode('', node_name, node_class, node_desc, prop_dict)

    def save_synonym_txt(self,synfile):
        with open(synfile, 'a', encoding='utf8') as f:
            for k,values in self.synonym_dict.items():
                if len(values[0])<12: #文字太长的事件不保存
                    line = ','.join(values)
                    line +='\n'
                    f.write(line)

    def save_node_csv(self, csvfile):
        with open(csvfile, 'w', encoding='utf8') as f:
            f.write('id,nodename,nodeclass,propertytext\n')
            for k,node in self.node_dict.items():
                line = '"'+node.node_id+'","'+node.node_name+'","'+node.node_class+'","'+node.node_desc+'"\n'
                f.write(line)

    def save_relation_csv(self, csvfile):
        with open(csvfile, 'w', encoding='utf8') as f:
            f.write('relation,node1,node2\n')
            for k,rel in self.relation_dict.items():
                line = '"'+rel.relation+'","'+rel.node1+'","'+rel.node2+'"\n'
                f.write(line)

    def load_relation_csv(self, csvfile):
        with open(csvfile, 'r', encoding='utf8') as f:
            rows = csv.reader(f)
            i=0
            for rel in rows:
                i+=1
                if i>1:
                    rel[0] = clean_name(rel[0])
                    rel[1] = clean_node(rel[1])
                    rel[2] = clean_node(rel[2])
                    relation = KGRelation(rel[0],rel[1],rel[2])
                    self.relation_dict[rel[0]+','+rel[1]+','+rel[2]]=relation
    
    def add_baike_relation(self, rel):
        key = rel.relation+','+rel.node1+','+rel.node2
        if key in self.relation_dict:
            return
        else:
            self.relation_dict[key] = rel

    def search_relation( self, key, node1, value ):
        if value in self.synonym_dict:
            node2 = self.get_node_name(value)
            if node2 is None or node1.node_id==node2.node_id:
                return
            rel = KGRelation(key, node1.node_id, node2.node_id)
            #print(key, node1.node_id, node2.node_id)
            self.add_baike_relation(rel)
        else:
            for s, ls in self.synonym_dict.items():
                if value in ls:
                    node2 = self.get_node_name(s)
                    if node2 is None or node1.node_id==node2.node_id:
                        continue
                    rel = KGRelation(key, node1.node_id, node2.node_id)
                    #print(key, node1.node_id, node2.node_id)
                    self.add_baike_relation(rel)

    def parse_baike_relation(self):
        for word, node in self.node_dict.items():
            #print(node.prop_dict)
            for key, value in node.prop_dict.items():
                if not self.search_relation( key, node, value):
                    vals = jieba.cut(value) #结巴分词后查找
                    for v in vals:
                        self.search_relation( key, node, v )

    def load_baike_csv(self, csvfile):
        with open(csvfile, 'r', encoding='utf8') as f:
            rows = csv.reader(f) 
            i=0
            for line in rows:
                #print(i, line)
                i+=1
                if i>1:
                    node = self.parse_baike(line)
                    nn = node.node_name
                    if nn[len(nn)-1:] in ['镇','旗','盟','县','区']: #为简化信息，只处理市以上的信息
                        continue
                    self.baike_dict[node.node_name] = node
                    self.add_baike_node(node)
                    self.update_synonym(node)
    def save_node_relation_name( self, nodefile, relationfile ):
        lines = []
        with open(nodefile, 'w',encoding='utf8') as f:
            for w, _ in self.node_dict.items():
                lines.append(w+'\n')
            f.writelines(lines)
        lines = []
        reldict = dict()
        with open(relationfile, 'w',encoding='utf8') as f:
            for _, rel in self.relation_dict.items():
                if rel.relation in reldict:
                    continue
                else:
                    reldict[rel.relation] = 1
                    lines.append(rel.relation+'\n')
            f.writelines(lines)

    def _serach_property(self, node, propertyname):
        #print(node)
        #print(propertyname)
        if propertyname in node.prop_dict:
            return node.prop_dict[propertyname]
        else:
            for s, ls in self.synonym_dict.items():
                for l in ls:
                    if l in node.prop_dict:
                        return node.prop_dict[l]
        return ''

    def search_node_property(self, nodename, propertyname):
        if nodename in self.baike_dict:
            node = self.baike_dict[nodename]
            return self._serach_property(node, propertyname)
        else:
            for s, ls in self.synonym_dict.items():
                if nodename in ls:
                    for l in ls:
                        if l in self.baike_dict:
                            node = self.baike_dict[l]
                            return self._serach_property(node, propertyname)
        return ''

INPUT_NODE_FILE = '../../data/csv/out_nodes.csv'
INPUT_RELATION_FILE = '../../data/csv/out_relations.csv'
INPUT_BAIKE_FILE = '../../data/csv/baike.csv'
OUTPUT_NODE_FILE = '../../data/csv/out_nodes.csv'
OUTPUT_RELATION_FILE = '../../data/csv/out_relations.csv'
OUTPUT_SYNONYM_FILE = '../../data/csv/user_synonym.txt'
OUTPUT_NODE_TXT = '../../data/csv/nodes.txt'
OUTPUT_RELATION_TXT = '../../data/csv/relations.txt'
OUTPUT_PROPERTY_FILE = '../../data/csv/property.txt'
#print(len(synonym_dict))
kg = KGManager()
kg.load_node_csv(INPUT_NODE_FILE)
kg.load_relation_csv(INPUT_RELATION_FILE)
kg.load_baike_csv(INPUT_BAIKE_FILE)
#kg.parse_baike_relation()
#kg.save_node_property_csv(OUTPUT_PROPERTY_FILE)
#kg.save_node_csv(OUTPUT_NODE_FILE)
#kg.save_relation_csv(OUTPUT_RELATION_FILE)
#kg.save_synonym_txt(OUTPUT_SYNONYM_FILE)
#kg.save_node_relation_name(OUTPUT_NODE_TXT, OUTPUT_RELATION_TXT)
#print(len(kg.node_dict))
#print(len(kg.baike_dict))
#print(len(kg.relation_dict))
#print(len(kg.synonym_dict))
print( kg.search_node_property('钟南山','性别') )
print( kg.search_node_property('钟南山','民族') )
print( kg.search_node_property('意大利','国庆日') )
print( kg.search_node_property('美国','国庆日') )
print( kg.search_node_property('西班牙','国庆日') )
#ouput_synonyms(synonym_dict, './user_synonyms.txt')
#ouput_nodes(node_dict, './baikenodes.csv')