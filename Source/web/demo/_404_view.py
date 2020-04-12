# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf

def _404_(request):  # 404页面
	context = {}
	return render(request, '404.html', context)
	