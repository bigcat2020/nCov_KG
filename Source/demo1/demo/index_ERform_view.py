# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
 
import sys
sys.path.append("..")
from toolkit.pre_load import pre_load_thu,neo_con,predict_labels
from toolkit.NER import get_NE,temporaryok,get_explain,get_detail_explain

# 读取实体解析的文本
def ER_post(request):
	ctx ={}
	if request.POST:
		key = request.POST['user_text']
		thu1 = pre_load_thu  #提前加载好了
		# 使用thulac进行分词 TagList[i][0]代表第i个词
		# TagList[i][1]代表第i个词的词性
		key = key.strip()
		TagList = thu1.cut(key, text=False)
		text = ""
		NE_List = get_NE(key)  #获取实体列表
		
		for pair in NE_List:   #根据实体列表，显示各个实体
			if pair[1] == 0:
				text += pair[0]
				continue
			if temporaryok(pair[1]):
				text += "<a href='#'  data-original-title='" + get_explain(pair[1]) + "(暂无资料)'  data-placement='top' data-trigger='hover' data-content='"+get_detail_explain(pair[1])+"' class='popovers'>" + pair[0] + "</a>"
				continue
			
			text += "<a href='detail.html?title=" + pair[0] + "'  data-original-title='" + get_explain(pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='"+get_detail_explain(pair[1])+"' class='popovers'>" + pair[0] + "</a>"
		
		ctx['rlt'] = text
				
		seg_word = ""
		length = len(TagList)
		for t in TagList:   #测试打印词性序列
			seg_word += t[0]+" <strong><small>["+t[1]+"]</small></strong> "
		seg_word += ""
		ctx['seg_word'] = seg_word
		
		
		
		
	return render(request, "index.html", ctx)
	
