from django.shortcuts import render, HttpResponse
import pandas as np
import json


def china_findall():
    cs = np.read_csv("static/map_csv/china.csv")
    ans = []
    for name, value in zip(cs["省份"], cs['累计确诊']):
        t = [name, value]
        ans.append(t)

    return ans


def world_findall():
    cs = np.read_csv("static/map_csv/world.csv")
    ans = []
    for name, value in zip(cs["名称"], cs['累计确诊']):
        t = [name, value]
        ans.append(t)
    return ans


def ajax_china(request):
    dt = china_findall()

    data = {
        "ans": dt
    }

    return HttpResponse(json.dumps(data), content_type='application/json')


def ajax_world(request):
    dt = world_findall()

    data = {
        "ans": dt
    }

    return HttpResponse(json.dumps(data), content_type='application/json')





def china_map(request):

    return render(request, "china_ajax.html")


def world_map(request):
    return render(request, "world_ajax.html")

