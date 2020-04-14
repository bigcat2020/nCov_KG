from django.shortcuts import HttpResponse, render
from modl.neo_models import neodb
import json


def search_st(request):
    if request.GET:
        name = request.GET['name']
        list_data = neodb.match_item_by_name(name, True)
        if len(list_data) > 0:
            ul = ""
            for i in list_data:
                name = i['n']['name']
                node_class = i['n']['nodeclass']
                ul = ul+'<p class="st_li" >实体名称：<a href="/data_st?name='+name+'">'+name+'</a> <span>实体类别：'+node_class+'</span></p>'
                print(name, node_class, )

            ul = ul+""

            data = {
                'list_st': ul,
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {
                'list_st': '<p style="font-size: 20px; ">抱歉，数据库中没有该实体</p>'
            }
            return HttpResponse(json.dumps(data), content_type='application/json')


def search_relation(request):
    ctx = {}
    if request.GET:
        db = neodb
        entity1 = request.GET['entity1_text']
        relation = request.GET['relation_name_text']
        entity2 = request.GET['entity2_text']

        relation = relation.lower()

        # 若只输入entity1,则输出与entity1有直接关系的实体和关系
        if len(entity1) != 0 and len(relation) == 0 and len(entity2) == 0:

            searchResult = db.find_relation_by_node_one(entity1)
            if len(searchResult) > 0:
                return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})

        # 若只输入entity2则,则输出与entity2有直接关系的实体和关系
        if len(entity2) != 0 and len(relation) == 0 and len(entity1) == 0:
            searchResult = db.find_relation_by_node_two(entity2)
            if len(searchResult) > 0:
                return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})
        # 若输入entity1和relation，则输出与entity1具有relation关系的其他实体
        if len(entity1) != 0 and len(relation) != 0 and len(entity2) == 0:
            searchResult = db.find_other_node1(entity1, relation)
            if (len(searchResult) > 0):
                return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})
        # 若输入entity2和relation，则输出与entity2具有relation关系的其他实体
        if len(entity2) != 0 and len(relation) != 0 and len(entity1) == 0:
            searchResult = db.find_other_node2(entity2, relation)
            if (len(searchResult) > 0):
                return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})

        # 若输入entity1和entity2,则输出entity1和entity2之间的最短路径
        if len(entity1) != 0 and len(relation) == 0 and len(entity2) != 0:
            searchResult = db.find_node1_node2(entity1, entity2)
            if len(searchResult) > 0:
                return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})

        # 若输入entity1,entity2和relation,则输出entity1、entity2是否具有相应的关系
        if len(entity1) != 0 and len(entity2) != 0 and len(relation) != 0:
            searchResult = db.find_entity_relation(entity1, relation, entity2)
            if len(searchResult) > 0:
                return render(request, 'relation.html', {'searchResult': json.dumps(searchResult, ensure_ascii=False)})
        # 全为空
        if len(entity1) != 0 and len(relation) != 0 and len(entity2) != 0:
            pass

        ctx = {'title': '<h1>暂未找到相应的匹配</h1>'}
        return render(request, 'relation.html', {'ctx': ctx})

    return render(request, 'relation.html', {'ctx': ctx})
