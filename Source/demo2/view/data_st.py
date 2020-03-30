from django.shortcuts import HttpResponse, render
from modl.nlpltp import pltobj
from modl.neo_models import neodb
import json


def data_st(request):
    if request.GET:
        name = request.GET['name']
        data = neodb.match_item_by_name(name)[0]['n']
        name = data['name']
        node_class = data['nodeclass']
        properties = data['properties'].split("”；")
        if len(properties)>1:
            ppts = {}
            print(data['properties'])
            print(properties)
            for i in properties:
                dt = i.split(": “")
                print(dt)
                if not dt[0]:
                    continue
                print(dt)
                if len(dt)>1:
                    ppts[dt[0]] = dt[1]
                    print(dt[0], dt[1])
                else:
                    ppts['简介']=dt[0]
            print(ppts)
        elif len(properties)==1:
            ppts = {'简介':data['properties']}

        # ppts = {'name': "钟南山",
        #         '性别': "男",
        #         '籍贯': '福建厦门',
        #         '参与事件': '2020年1月18日，钟南山从广州赶往武汉。、2020年1月20日晚，钟南山院士接受了白岩松采访，提出“它是肯定有人传人的”，拉响全国防控警报。'
        #      }

        return render(request, 'data_st.html', {'name': name, 'node_class': node_class, 'properties': ppts})
