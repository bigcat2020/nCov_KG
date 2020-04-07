from django.shortcuts import render
from django.views.decorators import csrf
from django.shortcuts import HttpResponse
from modl.nlpltp import pltobj
from modl.neo_models import neodb
import json


def nlp_fc(request):
	if request.GET:
		text = request.GET['text']
		words = pltobj.segment(text)  # 分词
		cx = pltobj.postag(words)

		nlp_fc = ''

		for i, j in zip(words, cx):
			nlp_fc = nlp_fc + i + " <strong><small>[" + j + "]</small></strong> "



		st = pltobj.get_keywords(text)

		nlp_st = ""
		for word in words:
			if word in st:
				data = neodb.match_item_by_name(word)
				if data:
					title = data[0]['n']['nodeclass']

					nlp_st = nlp_st + "<a href='/data_st?name=" + word + "' title='" + title + "' data-placement='top' " + " class='popovers'>" + word + "</a>"
					continue
				nlp_st = nlp_st + "<a href='#" + "' title='暂无资料'" + "  data-placement='top'  " + "class='popovers'>" + word + "</a>"
				continue
			else:
				nlp_st = nlp_st+word

		data = {
			'nlp_fc': nlp_fc,
			'nlp_st': nlp_st,
		}

		return HttpResponse(json.dumps(data), content_type='application/json')