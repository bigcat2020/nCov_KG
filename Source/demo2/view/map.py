from django.shortcuts import HttpResponse, render
from modl.nlpltp import pltobj
from modl.neo_models import neodb
import json


def china_map(request):

    return render(request, "china_ajax.html")


def world_map(request):
    return render(request, "world_ajax.html")

