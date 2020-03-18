import json
import csv
import numpy as np
import re

#cvoid_kg.py
#疫情知识图谱文件

#以event事件为例
# event/class/C0  '事件'
# event/class/C1  '公共卫生事件'
# event/class/C2  '新型冠状病毒事件'
# event/class/C3  '国家政策事件'

#命名空间：http://www.openkg.cn/2019-nCoV/character/
#属性定义：http://www.openkg.cn/2019-nCoV/character/{概念标识符}/property#{属性名称}
#概念定义：http://www.openkg.cn/2019-nCoV/ character /class/{概念标识符}
#实体定义：http://www.openkg.cn/2019-nCoV/ character /resource/{概念标识符}
#实体及概念标识符采用Base64编码，属性名称采用URL风格编码

#根节点
URL_ROOT = 'http://www.openkg.cn/COVID-19/'
URL_CHARACTER_ROOT = 'http://www.openkg.cn/COVID-19/character/'
URL_EVENT_ROOT = 'http://www.openkg.cn/COVID-19/event/'

KG_GRAPH_SCHEMA = '@graph'
KG_ID = '@id'
KG_TYPE = '@type'  #概念class, 实体resource, 属性Property
KG_LABEL = 'label' #可显示的名字，包括语言种类和标签值两个字段
KG_LABEL_LAN = '@language'
KG_LABEL_VAL = '@value'

KG_DOMAIN = 'domain' #定义实体或者属性属于哪个class
KG_RANGE = 'range' #实体或属性存储的数据类型（XMLSchema#string, XMLSchema#date等）
KG_SUB_CLASS_OF = 'subClassOf' #父概念，

KG_CONTEXT = '@context'

RET_INVALID_ID = 'Invalid id.'

#判断一个字符串是否为合法的id
def is_object_id( str ):
    return str.find(URL_ROOT)>=0 and re.match('/http(s)?:\/\/[\w.]+[\w\/]*[\w.]*\??[\w=&\+\%]*/is', str)!=None

#打印日志
PRINT_LOG = True
def print_log( str, module='Common' ):
    if PRINT_LOG:
        print( '['+module+']:'+str )

class KGObject():
    def __init__( self, root_url=URL_ROOT ):
        self.root = root_url
        self.kgdict = dict()

    def from_dict( self, kgdict ):
        self.kgdict = kgdict
        #print('From dict:',self.kgdict[KG_ID])
        #print( self.kgdict ) 

    def from_json_str( self, str, encoding='utf-8' ):
        self.kgdict = json.loads( str, encoding = encoding )
    
    def to_json_str( self ):
        return json.dumps( self.kgdict )
    
    def is_null( self ):
        return KG_ID in self.kgdict
    
    def get_id( self ):
        if KG_ID in self.kgdict:
            return self.kgdict[KG_ID]
        else:
            return ''

    def get_type( self ):
        if KG_TYPE in self.kgdict:
            return self.kgdict[KG_TYPE]
        else:
            return ''

    def get_label_language( self ):
        if KG_LABEL in self.kgdict and KG_LABEL_LAN in self.kgdict[KG_LABEL]:
            return self.kgdict[KG_LABEL][KG_LABEL_LAN]
        else:
            return ''

    def get_label_value( self ):
        if KG_LABEL in self.kgdict and KG_LABEL_VAL in self.kgdict[KG_LABEL]:
            return self.kgdict[KG_LABEL][KG_LABEL_VAL]
        else:
            return ''

    def __str__( self ):
        return self.get_label_value()

    def get_domain( self ):
        if KG_DOMAIN in self.kgdict:
            return self.kgdict[KG_DOMAIN]
        else:
            return ''

    def get_parent_class( self ):
        if KG_SUB_CLASS_OF in self.kgdict:
            return self.kgdict[KG_SUB_CLASS_OF]
        else:
            return ''
    
    def get_item( self, item ):
        if item in self.kgdict:
            return self.kgdict[item]
        else:
            return ''

class KGClass(KGObject):
    def __init__(self, rooturl=''):
        super().__init__(rooturl)
        self.parentclassid = list()
        self.childclassid = list()
    
    def from_obj( self, kgobj ):
        self.kgdict = kgobj.kgdict
        pc = self.get_parent_class()
        if len(pc)>=0:
            self.parentclassid.append(pc)

    def from_dict( self, kgdict ):
        self.kgdict = kgdict
        pc = self.get_parent_class()
        if len(pc)>=0:
            self.parentclassid.append(pc)

    def add_parent( self, parentid ):
        if not parentid in self.parentclassid:
            self.parentclassid.append(parentid)

    def has_parent(self, parentid ):
        return parentid in self.parentclassid

    def get_child_list(self):
        return self.childclassid
    
    def add_child( self, childid ):
        if not childid in self.childclassid:
            self.childclassid.append(childid)

    def has_child(self, childid):
        return childid in self.childclassid

#实体类
class KGNode(KGObject):
    def __init__(self, rooturl=''):
        super().__init__(rooturl)
        self.propertydict = dict() #每个属性可能有多个,所以内部是tuple形式("P20","abc")
        self.classid = list()
    
    def has_property( self, prop_id ):
        return prop_id in self.propertydict

    #增加一个属性，注意prop_values可能是str也可能是list
    def add_property( self, prop_id, prop_values ):
        if not self.has_property( prop_id ):
            self.propertydict[prop_id] = prop_values
    
    def is_class_of( self, class_id ):
        return class_id in self.classid

    def set_class( self, class_id ):
        if not self.is_class_of( class_id ):
            self.classid.append( class_id )

class KGRelation():
    def __init__( self, id_node1, id_node2, id_relation ):
        self.node1 = id_node1
        self.node2 = id_node2
        self.relation = id_relation
    
    def to_str( self ):
        return '['+ self.relation+','+self.node1+','+self.node2+']'

INT_TYPE_NULL = -1
INT_TYPE_CLASS = 0
INT_TYPE_NODE = 1
INT_TYPE_PROPERTY = 2

#知识图谱类
class CKnowledgeGraph():
    def __init__(self):
        self.kgnodes = dict()
        self.kgclass = dict()
        self.kgproperties = dict()
        self.kgrelations = dict()
        self.property_id_dict = dict()
        pass

    def clear_all( self ):
        self.kgnodes = dict()
        self.kgclass = dict()
        self.kgproperties = dict()
        self.kgrelations = dict()
        self.property_id_dict = dict()

    def get_class_label( self, id ):
        if id in self.kgclass:
            return self.kgclass[id].get_label_value()
        else:
            return RET_INVALID_ID

    def get_node_label( self, id ):
        if id in self.kgnodes:
            return self.kgnodes[id].get_label_value()
        else:
            return RET_INVALID_ID

    def get_property_label( self, id ):
        if id in self.kgproperties:
            return self.kgproperties[id].get_label_value()
        else:
            return RET_INVALID_ID

    def check_str_type( self, str ):
        if len(str)<10 and re.match( r'P[0-9]+', str )!=None:
            return INT_TYPE_PROPERTY
        type_label = ['/class/','/resource/','/property/']
        for i in range(len(type_label)):
            if str.find( type_label[i] )>=0:
                return i
        return INT_TYPE_NULL

    def check_item_type( self, item ):
        tstr = item.get_id()
        if len(tstr)<10:
            tstr = item.get_type()
            if len(tstr)<10:
                return INT_TYPE_NULL
            if tstr.find('#Property')>=0: #属性
                return INT_TYPE_PROPERTY

        type_label = ['/class/','/resource/','/property/']
        for i in range(len(type_label)):
            if tstr.find( type_label[i] )>=0:
                return i
        return INT_TYPE_NULL
    
    def add_class( self, item ):
        self.kgclass[item.get_id()] = KGClass()
        self.kgclass[item.get_id()].kgdict = item.kgdict
        obj = self.kgclass[item.get_id()]

        parentid = item.get_item(KG_SUB_CLASS_OF)
        if type(parentid) is str:
            #这里只完成父节点的添加，加完class后再遍历搜索子节点
            self.kgclass[item.get_id()].add_parent(parentid)
        elif type(parentid) is list:
            for id in parentid:
                self.kgclass[item.get_id()].add_parent(id)

    
    def get_property_id( self, id ):
        if id in self.property_id_dict:
            return self.property_id_dict[id]
        else:
            return id

    def add_node( self, item ):
        self.kgnodes[item.get_id()] = KGNode()
        self.kgnodes[item.get_id()].kgdict = item.kgdict
        obj = self.kgnodes[item.get_id()]
        #搜索property
        #print( "Add node ", obj )
        for id, val in item.kgdict.items():
            if re.match( r'P[0-9]+', id )!=None:
                #搜索类似'P41', 'P1', 'P2:0'，但是替换为context里面的长id
                #print( 'Add prop ', self.get_property_id( id ) )
                self.kgnodes[item.get_id()].add_property( self.get_property_id( id ), val )

    #增加一个属性，注意要用context里面的长id替换短id
    def add_property( self, item ):
        id = item.kgdict[KG_ID]
        id1 = self.get_property_id( id )
        #print('prop  ',id, id1)
        self.kgproperties[id1] = KGObject(URL_CHARACTER_ROOT)
        self.kgproperties[id1].kgdict = item.kgdict
        self.kgproperties[id1].kgdict[KG_ID] = id1

    def add_item( self, item ):
        nodetype = self.check_item_type(item)
        if nodetype==INT_TYPE_NULL:
            #print_log('Invalid item' + item.get_id() )
            return

        if nodetype==INT_TYPE_CLASS: #添加类
            self.add_class( item )
        elif nodetype==INT_TYPE_NODE: #节点 
            self.add_node( item )
        elif nodetype==INT_TYPE_PROPERTY: #属性
            self.add_property( item )

    def get_item_label( self, id ):
        typeid = self.check_str_type(id)
        if typeid==INT_TYPE_CLASS:
            return self.get_class_label( id )
        elif typeid==INT_TYPE_NODE:
            return self.get_node_label( id )
        elif typeid==INT_TYPE_PROPERTY:
            return self.get_property_label( id )
        else:
            return ''

    def print_property( self, id, val ):
        type_label = ['class','resource','property']
        if type(val) is str:
            typeid = self.check_str_type(val)
            if typeid!=INT_TYPE_NULL: #是对象id
                print('    Prop id['+id+'], label['+ self.get_item_label(id)+'], type['+type_label[typeid]+'] prop value['+ self.get_item_label(val) +']')
            else: #直接打印字符串
                if is_object_id( val ):
                    print('    Prop id['+id+'], label['+ self.get_item_label(id)+'], type['+type_label[typeid]+'] prop value['+ self.get_item_label(val) +']')
                else:
                    print('    Prop id['+id+'], label['+ self.get_item_label(id)+'], type['+type_label[typeid]+'] prop value['+ val +']')
        elif type(val) is list:
            for v in val:
                typeid = self.check_str_type(v)
                if typeid!=INT_TYPE_NULL: #是对象id
                    print('    Prop id['+id+'], label['+ self.get_item_label( id)+'], type['+type_label[typeid]+'] prop value['+ self.get_item_label(v) +']')
                else: #直接打印字符串
                    if is_object_id( v ):
                        print('    Prop id['+id+'], label['+ self.get_item_label(id)+'], type['+type_label[typeid]+'] prop value['+ self.get_item_label(v) +']')
                    else:
                        print('    Prop id['+id+'], label['+ self.get_item_label(2, id)+'], type['+type_label[typeid]+'] prop value['+ v +']')

    def list_nodes( self ):
        for id, nodeobj in self.kgnodes.items():
            if len(id)>0:
                print('Nodes id['+id+'] label['+nodeobj.get_label_value()+']')
                print('    type['+nodeobj.get_type()+']')
                for id, val in nodeobj.propertydict.items():
                    self.print_property( id, val )

    def list_properties( self ):
        for id, prop in self.kgproperties.items():
            if len(id)>0:
                print('Property id['+id+'] label['+prop.get_label_value()+']')
                domain = prop.get_domain()
                print('    domain label['+self.get_item_label(domain)+']')

    def list_class( self ):
        #print( self.kgclass )
        for id, classobj in self.kgclass.items():
            if len(id)>0:
                print('class id['+id+'] label['+classobj.get_label_value()+']')
                for id in classobj.parentclassid:
                    if id in self.kgclass:
                        print('    Parent class Id['+id +'] label[' + self.kgclass[id].get_label_value() + ']')
                for id in classobj.childclassid:
                    if id in self.kgclass:
                        print('    Child class Id['+id +'] label[' + self.kgclass[id].get_label_value() + ']')

    def search_child_class(self):
        for id, obj in self.kgclass.items():
            for pid in obj.parentclassid:
                if pid in self.kgclass:
                    self.kgclass[pid].add_child( id )

    #增加一个关系
    def add_relation( self, id1, id2, relation ):
        rel = KGRelation(id1, id2, relation)
        #print( 'Add relation= ', rel )
        #print( str(rel) )
        self.kgrelations[rel.to_str()] = rel

    def search_relations(self):
        #先搜索实体与实体之间的关系
        for id1, node in self.kgnodes.items(): #节点id1
            #print( 'Search node['+id1+']')
            for rel, val in node.propertydict.items():
                if type(val) is str:
                    val = [val]
                for v in val:
                    typeid = self.check_str_type(v)
                    if typeid==INT_TYPE_NODE:
                        id2 = self.kgnodes[v].get_id()
                        self.add_relation( id1, id2, rel )

    def list_relations(self):
        for id, rel in self.kgrelations.items():
            print( 'Relation='+id)
            self.print_relation(rel)
    
    def find_id(self, nodename ):
        itemlist = list()
        for id, node in self.kgclass.items(): #节点id1
            if node.get_label_value() == nodename:
                itemlist.append( ('class', id) )
        for id, node in self.kgnodes.items(): #节点id1
            if node.get_label_value() == nodename:
                itemlist.append( ('node', id) )
        for id, node in self.kgproperties.items(): #节点id1
            if node.get_label_value() == nodename:
                itemlist.append( ('property', id) )
        return itemlist
    
    def print_relation( self, rel ):
        label_node1 = self.kgnodes[rel.node1].get_label_value()
        label_node2 = self.kgnodes[rel.node2].get_label_value()
        if rel.relation in self.kgproperties:
            label_rel = self.kgproperties[rel.relation].get_label_value()
            print( '    relation['+label_node1+'],['+label_rel+'],['+label_node2+']')
        else:
            print( '    relation['+label_node1+'],[Null],['+label_node2+']')

    def find_relation(self, nodename ):
        itemlist = self.find_id( nodename )
        #print(itemtype, ', ', id)
        for item in itemlist:
        #if len(id)>0 and itemtype=='node':
            if item[0]=='node':
                id = item[1]
                nodeobj = self.kgnodes[id]
                print('Nodes id['+id+'] label['+nodeobj.get_label_value()+']')
                print('    type['+nodeobj.get_type()+']')
                for id, val in nodeobj.propertydict.items():
                    self.print_property( id, val )

            itemtype = item[0]
            itemid = item[1]
            #print( 'Found node=', nodename )# self.kgnodes[id].get_label_value())
            for id_rel, rel in self.kgrelations.items():
                if rel.node1==itemid or rel.node2==itemid:
                    #print( '    relation=', id_rel )
                    self.print_relation(rel)

    def load_context(self, kgcontext):
        print( '处理Context')
        for id, item in kgcontext.items():
            if self.check_str_type(id)==INT_TYPE_PROPERTY:
                    id1 = item[KG_ID]
                    self.property_id_dict[id] = id1
                    #print( 'context ['+id+'] = ['+id1+']')

    #修改event节点
    def modify_event_nodes( self ):
        p1 = 'http://www.openkg.cn/2019-nCoV/event/property/P1'
        p18 = 'http://www.openkg.cn/2019-nCoV/event/property/P18'
        for id, node in self.kgnodes.items():
            nlabel = node.get_label_value()
            if id.find('/event/resource'): #修改事件节点
                if p1 in node.propertydict:
                    val = node.propertydict[p1]
                    print( 'Modify ['+val+'], ['+nlabel+']' )                
                    node.kgdict[KG_LABEL][KG_LABEL_VAL] = val
                    del node.propertydict[p1]

    def load_json( self, jsonfile ):
        with open( jsonfile, 'r', encoding='utf-8' ) as f:
            kgroot = json.load( f )

            if type(kgroot) is list:
                for item in kgroot:
                    obj = KGObject( URL_CHARACTER_ROOT )
                    obj.from_dict( item )
                    self.add_item( obj )
                    self.search_child_class()
                    #搜索关系
                    self.search_relations()
            elif type(kgroot) is dict:
                #先加载id映射表
                if KG_CONTEXT in kgroot:
                    #kgcontext = kgroot[KG_CONTEXT]
                    self.load_context(kgroot[KG_CONTEXT])

                if KG_GRAPH_SCHEMA in kgroot:
                    kggraph = kgroot[KG_GRAPH_SCHEMA]
                    for item in kggraph:
                        obj = KGObject( URL_CHARACTER_ROOT )
                        obj.from_dict( item )
                        self.add_item( obj )
                    self.search_child_class()
                    #搜索关系
                    self.search_relations()
                    self.modify_event_nodes()
                return True
            else:
                return False

    def get_short_id( self, id ):
        idprefix = ['2019-nCoV', 'COVID-19']
        for i in range(len(idprefix)):
            idx = id.find( idprefix[i] )
            if idx>0:
                ll = len(idprefix[i])
                return id[idx+ll+1:]
        return id

    #关系对象保存到relations.csv 
    #数据结构为：
    #     relationname：关系名，默认为中文
    #     node1：实体1的id
    #     node2：实体2的id
    def save_relations_csv(self, relfile):
        p16='http://www.openkg.cn/2019-nCoV/event/property/P16'
        with open( relfile, 'w', encoding='utf-8' ) as f:
            lines = ['relation,node1,node2\n']
            for id, rel in self.kgrelations.items():
                if rel.node1 in self.kgnodes and \
                   rel.node2 in self.kgnodes and \
                   rel.relation in self.kgproperties:
                   relation = self.kgproperties[rel.relation].get_label_value()
                   if rel.relation==p16:
                       print( 'relation 并发症==',self.kgproperties[rel.relation] )
                       relation = '后续事件'
                   relation = self.clean_text( relation )
                   l = '"' + self.get_short_id(relation) + '","' + \
                       self.get_short_id(rel.node1) + '","' + \
                       self.get_short_id(rel.node2) + '"\n'
                   lines.append(l)
                else:
                    print( "Wrong ",rel )
            f.writelines( lines )

    def clean_text( self, txt ):
        txt = txt.strip()
        txt = txt.replace(',','，')
        txt = txt.replace(':','：')
        txt = txt.replace("'", " ")
        txt = txt.replace('"',' ')
        txt = txt.replace('(','（')
        txt = txt.replace(')','）')
        return txt

    #保存到csv文件，逗号分隔，utf-8编码
    #实体对象保存到nodes.csv 
    #数据结构为: 
    #    id：字符串，符合OWL标准
    #    nodename：节点名，默认为中文
    #    nodeclass: 节点类型，默认为中文
    #    parentclass: 节点父类型，默认为中文，暂时不用
    #    propertytext：把所有文本属性集合为一段字符，例如："籍贯：福建厦门； 性别：男； 民族：汉"，默认为中文
    #neo4j加载的cypher语句为：
    # LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS line CREATE()
    # 实体对象要解决去重的问题，名称/class都相同，则识别为重复的节点
    def save_nodes_csv(self, nodefile):
        with open( nodefile, 'w', encoding='utf-8' ) as f:
            lines = ['id,nodename,nodeclass,propertytext\n']
            for id, node in self.kgnodes.items():
                nodename = node.get_label_value()
                cid = node.get_type()
                nodeclass = '节点'
                if cid in self.kgclass:
                    nodeclass = self.kgclass[cid].get_label_value()
                propertytext = ''
                for pid, val in node.propertydict.items():
                    plabel = self.kgproperties[pid].get_label_value() + ': “'#属性值用中文左右引号分隔
                    if type(val) is str:
                        val = [val]
                    typeid = self.check_str_type(pid)
                    if typeid==INT_TYPE_PROPERTY:
                        i=0
                        for v in val:
                            vtype = self.check_str_type(v)
                            if INT_TYPE_NODE == vtype:
                                v = self.kgnodes[v].get_label_value()
                            plabel += self.clean_text(v)
                            i += 1
                            if i<len(val):
                                plabel +='、' #两个属性之间用中文顿号隔开
                    propertytext += plabel + '”；'#属性值用中文左右引号分隔
                nodename = self.clean_text( nodename )
                #propertytext = self.clean_text( propertytext )
                nodeclass = self.clean_text( nodeclass )
                l = '"' + self.get_short_id(id) +'","' + nodename + '","' + \
                    nodeclass + '","' + propertytext + '"\n'
                lines.append(l)
            f.writelines(lines)

    def save_csv( self, path ):
        relfile = path + 'nodes.csv'
        self.save_nodes_csv(relfile)
        relfile = path + 'relations.csv'
        self.save_relations_csv(relfile)
        return

#kgmng.load_json('d:/character-covid-19-v0.21.json')

#json_list = ['goods-v0.1.json',\
#    'medical-covid-19-v0.2.json',\
#    'openkg-covid-19-prevention-3-10.json',\
#json_list=[ 'xinguan_schema_list.json',\
#    'wiki-covid-19-v0.2.json']
#json_list=[ 'character-covid-19-v0.21.json']#,'event-covid-19-v0.2.json']
#json_list=['event-covid-19-v0.2.json']
#json_list=['xinguan_schema_list.json']

def clear_node( txt ):
    txt = txt.strip()
    txt = txt.replace('《','')
    txt = txt.replace('》','')
    txt = txt.replace('、','')
    txt = txt.replace('，','')
    txt = txt.replace('：','')
    txt = txt.replace('。','')
    txt = txt.replace('“','')
    txt = txt.replace('”','')
    txt = txt.replace(' ','')
    return txt

def load_nodes( csvfile ):
    nodes = list()
    with open(csvfile, 'r', encoding='utf8') as f:
        rows = csv.reader(f)
        for line in rows:
            nodename = clear_node(line[1])
            nodes.append( nodename+'\n' )
    if(len(nodes)>0):
        with open('nodes.csv', 'w', encoding='utf8') as f:
            f.writelines(nodes)

#load_nodes('../../data/csv/nodes.csv')
#exit(0)

json_list=['character-covid-19-v0.21.json','event-covid-19-v0.2.json','medical-covid-19-v0.2.json']

PATH_NAME = '../../data/json/'

import time
kgmng = CKnowledgeGraph()
for i in range(len(json_list)):
    start = time.time()
    kgmng.load_json( PATH_NAME + str(json_list[i]) )

#kgmng.list_class()
#kgmng.list_properties()
#kgmng.list_nodes()
#kgmng.list_relations()
print( 'class numbers=', len(kgmng.kgclass))
print( 'nodes numbers=', len(kgmng.kgnodes))
print( 'properties numbers=', len(kgmng.kgproperties))
print( 'relations numbers=', len(kgmng.kgrelations))
    #kgmng.find_relation('钟南山')
    #kgmng.find_relation('李兰娟')
kgmng.save_csv('../../data/csv/')
kgmng.clear_all()

print( 'Time cost=', time.time() - start)

