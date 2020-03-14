import csv
import re
path = '../../data/disease.csv'

#拆分 百日咳[疾病]，咳嗽[症状]
def splitlabel( txt ):
    end = len(txt)-1
    if end>1 and txt.find('[',1,end-1)>=0 and txt[end:]==']':
        lst = re.split( r"\[|\]", txt )
    # else:
    #     if end>1 and txt.find('(',1,end-1)>=0 and txt[end:]==')':
    #         lst = re.split( r"\(|\)", txt )
    else:
        lst = [txt,'']
    return lst[0],lst[1]

g_nodes=dict()

white_list = [
    '肺', '呼吸', '咳' 
]

g_relationdict=dict()

def check_node( node, label ):
    if len(node)<2 or len(label)<2:
        return False
    if node in g_nodes:
        g_nodes[node] += 1
        return False
    else:
        if label=='疾病':
            bwhitelist = False
            for w in white_list:
                if node.find(w)>=0:
                    bwhitelist = True
                    break
            if not bwhitelist:
                return False
        g_nodes[node] = 0
        return True

def check_multi_line( txt ):
    if txt[:1]=='"' and txt[len(txt)-1:]=='"':
        return txt
    else:
        #print('multi-line format ERR')
        #print(txt)
        txt = txt.replace('"','')
        return '"'+txt+'"'

def write_log( txt, log ):
    if log:
        print(txt)

def add_node( f_node, node, label ):
    if check_node(node, label):
        line = node+','+label+'\n'
        f_node.write(line)

def add_relation( f, r, n1, n2 ):
    if n1 in g_nodes and n2 in g_nodes:
        line = r+','+n1+','+n2+'\n'
        if not line in g_relationdict:
            g_relationdict[line]=0
            f.write(line)
        else:
            g_relationdict[line]+=1

def add_attr( f, node, attr, value ):
    if node in g_nodes and len(attr)>1 and len(value)>1:
        line = node+','+attr+','+value+'\n'
        f.write(line)

term_dict = {'可能疾病':'疾病',
    '就诊科室':'科室',
    '二级科室分类':'科室',
    '三级科室分类':'科室',
    '推荐药品':'药品',
    '常用药品':'药品',
    #'宜吃食物':'食品',
    #'忌吃食物':'食品',
    #'推荐食谱':'食品',
    '易感人群':'人群',
    '传染方式':'传染方式',
    '治疗方式':'治疗方式',
    '并发症':'症状',
    #'治疗周期':'治疗周期',
    #'治愈率':'治愈率',
    '症状':'症状'
    }

def save_row_to_file( row, f_node, f_rel, f_attr, log=False  ):
    assert(len(row)==3)

    relation = row[1]
    node, label1 = splitlabel(row[0])
    if row[2].find('\n',1,len(row[2])-2)>=0:
        #解决部分多行数据没有用双引号包裹的问题
        val = check_multi_line(row[2])
        label2 = ''
    else:
        #如果label2存在，则写入关系表
        val, label2 = splitlabel(row[2])

    if len(label2)>1:
        add_node( f_node, node, label1 )
        add_node( f_node, val, label2 )
        add_relation( f_rel, relation, node, val )
    else:
        add_node( f_node, node, label1 )
        #可以设置属性
        if len(val)>1:
            is_attr = True
            if relation in term_dict and node in g_nodes:
                ns = re.split( ' ', val)
                for n in ns:
                    add_node( f_node, n, term_dict[relation] )
                    add_relation( f_rel, relation, node, n )
                is_attr = False
            if is_attr:
                add_attr( f_attr, node, relation, val )


# delimiter:以逗号分隔  skiprows:跳过前1行
with open(path, 'r', encoding='utf-8') as f:
    lines = csv.reader(f)
    header = next(lines)
    
    f_node = open( '../../data/nodes.csv', 'w', encoding='utf8')
    f_node.write('nodename,labelname\n')
    f_rel = open( '../../data/relations.csv', 'w', encoding='utf8')
    f_rel.write('relname,node1,node2\n')
    f_attr = open( '../../data/attrs.csv', 'w', encoding='utf8')
    f_attr.write('nodename,attrname,attrvalue\n')
    
    i = 0
    for row in lines:
        save_row_to_file( row, f_node, f_rel, f_attr )
        i += 1
    print( i )
    
    f_node.close()
    f_rel.close()
    f_attr.close()

