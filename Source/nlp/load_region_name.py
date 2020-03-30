import json

NODE_DICT_NAME = 'name'
NODE_DICT_LEVEL = 'level'
NODE_DICT_CENTER = 'center'
NODE_DICT_DISTRICTS = 'districts'

g_nodeset = list()
def search_district(nodedict, parent):
    if NODE_DICT_DISTRICTS in nodedict and len(nodedict[NODE_DICT_DISTRICTS])>0:
        #迭代
        #print('开始迭代',nodedict['name'])
        for node in nodedict[NODE_DICT_DISTRICTS]:
            #print(node)
            search_district(node, nodedict[NODE_DICT_NAME])
    #node = dict()
    if NODE_DICT_NAME in nodedict and NODE_DICT_LEVEL in nodedict:
        g_nodeset.append( [nodedict[NODE_DICT_NAME], nodedict[NODE_DICT_LEVEL], parent] )
        #node[NODE_DICT_NAME] = nodedict[NODE_DICT_NAME]
    #else:
    #    print(nodedict)
    #    return
    #if NODE_DICT_LEVEL in nodedict:
    #    node[NODE_DICT_LEVEL] = nodedict[NODE_DICT_LEVEL]
    #g_nodeset.update(node)
    return
    

with open('../../data/region.json', 'r', encoding='utf-8') as f:
    root = json.load( f )
    node = set()
    search_district(root,'中国')
    print(g_nodeset)

with open('../../data/regions.csv','w', encoding='utf-8') as f:
    lines = list()
    for node in g_nodeset:
        line = node[0] + ',' + node[1] + ','+node[2]+'\n'
        lines.append(line)
    f.writelines(lines)

with open('../../data/regionname.txt','w', encoding='utf-8') as f:
    lines = list()
    for node in g_nodeset:
        line = node[0]+'\n'
        lines.append(line)
    f.writelines(lines)