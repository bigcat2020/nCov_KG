from django.shortcuts import render
from django.views.decorators import csrf
from django.shortcuts import HttpResponse


def index(request):  # index页面需要一开始就加载的内容写在这里
	context = {}

	return render(request, 'index1.html', context)


def search(request):
	context = {}
	print("我是自己写的")
	return render(request, 'search_st.html', context)