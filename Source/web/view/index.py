from django.shortcuts import render


def search(request):
	context = {}
	return render(request, 'search_st.html', context)