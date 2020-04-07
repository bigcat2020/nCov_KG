from django.shortcuts import HttpResponse, render
import pandas as np


def china_findall():
    cs = np.read_csv("/static/map_csv/china.csv")
    return cs.values


def world_findall():
    cs = np.read_csv("/static/map_csv/world.csv")
    return cs.values


def china_map(request):

    return render(request, "china_ajax.html")


def world_map(request):
    return render(request, "world_ajax.html")

