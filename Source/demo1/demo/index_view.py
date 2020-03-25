# -*- coding: utf-8 -*-
#from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators import csrf
import nlpltp

pltobj = nlpltp.NlpLtp()
def index(request):  # index页面需要一开始就加载的内容写在这里
	# context = {
	# 	text:"杨源斌蒟蒻",
	# 	res:obj.get_keywords(text)
	# }
	text = ""
	try:
		text = request.POST['user_text']
	except Exception:
		pass
	res = ""
	if text != "":
		res = str(pltobj.get_keywords(text))
	return render(request, 'index.html', {"text":text,"res":res})