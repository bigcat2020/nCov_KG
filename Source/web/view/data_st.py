from django.shortcuts import render
from modl.neo_models import neodb


def data_st(request):
    if request.GET:
        name = request.GET['name']
        data = neodb.match_item_by_name(name)[0]['n']
        name = data['name']
        node_class = data['nodeclass']
        properties = data['properties'].split("”；")
        ppts = {}

        if len(properties) > 1:

            for i in properties:
                dt = i.split(": “")
                print(dt)
                if not dt[0]:
                    continue

                if len(dt) > 1:
                    ppts[dt[0]] = dt[1]
                    print(dt[0], dt[1])
                else:
                    ppts['简介'] = dt[0]

        elif len(properties) == 1:
            ppts = {'简介': data['properties']}

        return render(request, 'data_st.html', {'name': name, 'node_class': node_class, 'properties': ppts})
