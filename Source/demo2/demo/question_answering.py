# -*- coding:utf-8 -*-
from django.shortcuts import render
from toolkit.pre_load import neo_con
import random
import re
import jieba
import jieba.posseg as pg

city_list = []

with open('label_data/city_list.txt','r',encoding='utf8') as fr:
	for city in fr.readlines():
		city_list.append(city.strip())


#thu_lac = pre_load_thu
db = neo_con

#找到对应天气适合种植的植物，随机取6个，如果植物里有科，那么找到这个科具体对应的植物，最多随机取6个,将答案和关系填在ret_dict中
def get_weather_plant(weather,ret_dict):
	plant = db.findOtherEntities(weather,"适合种植")

	#如果结果数大于6，则随机取6个
	selected_index = []
	if(len(plant) > 6 ):
		m = 6
		for i in range(len(plant)):
			rand = random.randint(0,len(plant) - i - 1)
			if(rand<m):
				m-=1
				selected_index.append(i)
	else:
		selected_index = [i for i in range(len(plant))]


	for i in selected_index:
		selected_plant = plant[i]['n2']['title']
		relation = plant[i]['rel']['type']
		if(selected_plant[-1] == "科"):
			concrete_plant_list = db.findOtherEntities2(selected_plant,"科")
			selected_concrete_index = []
			if(len(concrete_plant_list) >6 ):
				m = 6
				for j in range(len(concrete_plant_list)):
					rand = random.randint(0,len(concrete_plant_list) - j - 1)
					if(rand < m):
						m-=1
						selected_concrete_index.append(j)
			else:
				selected_concrete_index = [i for i in range(len(concrete_plant_list))]
			if(ret_dict.get('list') is None):
				ret_dict['list'] = []
			ret_dict['list'].append({"entity1":weather,"rel":"适合种植","entity2":selected_plant,"entity1_type":"气候","entity2_type":"植物"})
			for j in selected_concrete_index:
				concrete_plant = concrete_plant_list[j]['n1']['title']
				if(ret_dict.get('list') is None):
					ret_dict['list'] = []
				ret_dict['list'].append({"entity1":concrete_plant,"rel":"科","entity2":selected_plant,"entity1_type":"植物科","entity2_type":"植物"})

				if(ret_dict.get('answer') is None):
					ret_dict['answer'] = [concrete_plant]
				else:
					ret_dict['answer'].append(concrete_plant)


		else:
			if(ret_dict.get('list') is None):
				ret_dict['list'] = []
			ret_dict['list'].append({"entity1":weather,"rel":"适合种植","entity2":selected_plant,"entity1_type":"气候","entity2_type":"植物"})
			if (ret_dict.get('answer') is None):
				ret_dict['answer'] = [selected_plant]
			else:

				ret_dict['answer'].append(selected_plant)



	return ret_dict

def get_shi_weather(address,ret_dict):
	if (address in city_list):
		# 查看weather
		weather = get_city_weather(address)
		if (weather != 0):
			if(ret_dict.get('list') is None):
				ret_dict['list'] = []
			ret_dict['list'].append({'entity1': address, 'rel': '气候', 'entity2': weather,'entity1_type':'地点','entity2_type':'气候'})

			if(ret_dict.get('answer') is None):
				ret_dict['answer'] = [weather]
			else:
				ret_dict['answer'].append(weather)

	else:
		address_chinese_name = get_chinese_name(address)
		if (address_chinese_name in city_list):
			weather = get_city_weather(address_chinese_name)
			if (weather != 0):
				if(ret_dict.get('list') is None):
					ret_dict['list'] = []
				ret_dict['list'].append({'entity1': address, 'rel': '气候', 'entity2': weather,'entity1_type':'地点','entity2_type':'气候'})

				if (ret_dict.get('answer') is None):
					ret_dict['answer'] = [weather]
				else:
					ret_dict['answer'].append(weather)

	return ret_dict

def get_xian_plant(address,ret_dict):
	upper_address = get_shi_address(address)

	if (upper_address in city_list):
		ret_dict = get_shi_plant(upper_address, ret_dict)

	else:
		upper_address_chinese_name = get_chinese_name2(upper_address)
		if (upper_address_chinese_name == 0):
			upper_address_chinese_name = get_chinese_name(upper_address)

		ret_dict = get_shi_plant(upper_address_chinese_name, ret_dict)


	return ret_dict

def get_xian_weather(address,ret_dict):
	upper_address = get_shi_address(address)

	if (upper_address in city_list):
		ret_dict = get_shi_weather(upper_address, ret_dict)

	else:
		upper_address_chinese_name = get_chinese_name2(upper_address)
		if (upper_address_chinese_name == 0):
			upper_address_chinese_name = get_chinese_name(upper_address)

		ret_dict = get_shi_weather(upper_address_chinese_name, ret_dict)


	return ret_dict

def get_xian_address(address):
	upper_address = db.findOtherEntities2(address,"contains administrative territorial entity")
	if(len(upper_address) == 0):
		return 0
	return upper_address[0]['n1']['title']

#问答模板
#1、xx[地区、国家、省市、机构、人]的[疫情、防疫、情况、简介、介绍]（例：广元的疫情情况如何？ 美国疫情情况如何？） 关键词：地名
#2、新冠病毒（肺炎）的[来源、症状、预防、药物、治疗、防护]等？
#3、其他（答复：暂无回答）

def question_answering(request):  # index页面需要一开始就加载的内容写在这里
	context = {'ctx':''}
	if(request.GET):
		question = request.GET['question']
		cut_statement = thu_lac.cut(question,text=False)
		print(cut_statement)
		address_name = []
		weather_name = []
		question_name = ""
		ret_dict = {}

		pos = -1
		q_type  = -1
		for i in range(len(pattern)):
			for x in pattern[i]:
				index  =  re.search(x,question)
				if(index):
					pos = index.span()[0]
					q_type= i
					break
			if(pos!=-1):
				break

		print(pos)
		#匹配问题 xxx地方适合种什么
		if(q_type==0):
			index = 0
			for x in cut_statement:
				if(index>pos):
					break
				index += len(x)
				if (x[1] == 'ns' or (
						x[1] == 'n' and (x[0][-1] == '镇' or x[0][-1] == '区' or x[0][-1] == '县' or x[0][-1] == '市'))):
					address_name.append(x[0])
				elif (x[0] == '崇明'):
					address_name.append(x[0])

			for address in address_name:
				address = address.strip()
				##查看行政级别，如果没有行政级别这个属性，使用(address <- 中文名)再试一次，如果还没有行政级别这个属性，那么默认是镇
				xingzhengjibie = get_xinghzhengjibie(address)

				address_chinese_name = 0
				if(xingzhengjibie == 0):
					address_chinese_name = get_chinese_name2(address)
					if(address_chinese_name ==0):
						address_chinese_name = get_chinese_name(address)

				if(xingzhengjibie == 0 and address_chinese_name == 0):
					xingzhengjibie = '镇'
				elif(xingzhengjibie ==0 ):
					xingzhengjibie = get_xinghzhengjibie(address_chinese_name)
					if(xingzhengjibie == 0):
						xingzhengjibie = '镇'
				print(xingzhengjibie)
				#如果行政级别是市或者地级市，那么直接看该address是否在city_list中，如果不在，再看它的chinese_name在不在
				if(xingzhengjibie == "市" or xingzhengjibie == "地级市" or xingzhengjibie =='直辖市'):

					ret_dict  = get_shi_plant(address,ret_dict)

				elif(xingzhengjibie == "县" or xingzhengjibie == "市辖区"):
					if(len(ret_dict) == 0 or ret_dict==0):
						ret_dict = get_xian_plant(address,ret_dict)
					if (len(ret_dict) > 0):
						upper_address = get_shi_address(address)
						ret_dict['list'].append({'entity1': address, 'rel': '属于', 'entity2': upper_address,'entity1_type':'地点','entity2_type':'地点'})

				elif(xingzhengjibie == "镇"):
					upper_address = get_xian_address(address)
					if(len(ret_dict) == 0 and upper_address!=0):
						ret_dict = get_xian_plant(upper_address,ret_dict)
					if(len(ret_dict) >0 ):
						ret_dict['list'].append({'entity1':address,'rel':'属于','entity2':upper_address,'entity1_type':'地点','entity2_type':'地点'})

		##匹配问题：属于哪种气候
		if(q_type == 1):
			index  = 0
			flag = 0
			for x in cut_statement:
				if(index > pos):
					break

				index += len(x)

				if (x[1] == 'ns' or (x[1] == 'n' and (x[0][-1] == '镇' or x[0][-1] == '区' or x[0][-1] == '县' or x[0][-1] == '市'))):
					address_name.append(x[0])

				elif (x[0] == '崇明'):
					address_name.append(x[0])

				elif(x[0] == '首都' or x[0] == '首府'):
					flag = 1

			for address in address_name:
				print(flag)
				if(flag == 1):
					shoudu  = db.findOtherEntities(address, "首都")
					if(len(shoudu) >0):
						shoudu = shoudu[0]['n2']['title']
						if(ret_dict.get('list') is None):
							ret_dict['list'] =  [{'entity1':address,'rel':'首都','entity2':shoudu,'entity1_type':'地点','entity2_type':'地点'}]
							address = shoudu
				address = address.strip()
				print(address)
				##查看行政级别，如果没有行政级别这个属性，使用(address <- 中文名)再试一次，如果还没有行政级别这个属性，那么默认是镇
				xingzhengjibie = get_xinghzhengjibie(address)

				address_chinese_name = 0
				if (xingzhengjibie == 0):
					address_chinese_name = get_chinese_name2(address)
					if (address_chinese_name == 0):
						address_chinese_name = get_chinese_name(address)

				if (xingzhengjibie == 0 and address_chinese_name == 0):
					xingzhengjibie = '镇'
				elif (xingzhengjibie == 0):
					xingzhengjibie = get_xinghzhengjibie(address_chinese_name)
					if (xingzhengjibie == 0):
						xingzhengjibie = '镇'
				print(xingzhengjibie)
				# 如果行政级别是市或者地级市，那么直接看该address是否在city_list中，如果不在，再看它的chinese_name在不在
				if (xingzhengjibie == "市" or xingzhengjibie == "地级市" or xingzhengjibie == '直辖市'):

					ret_dict = get_shi_weather(address, ret_dict)
				elif (xingzhengjibie == "县" or xingzhengjibie == "市辖区"):
					if (len(ret_dict) == 0 or ret_dict ==0):
						ret_dict = get_xian_weather(address, ret_dict)
					if (len(ret_dict) > 0 and ret_dict!=0):
						upper_address = get_shi_address(address)
						ret_dict['list'].append(
							{'entity1': address, 'rel': '属于', 'entity2': upper_address, 'entity1_type': '地点',
							 'entity2_type': '地点'})

				elif (xingzhengjibie == "镇"):
					upper_address = get_xian_address(address)
					if (len(ret_dict) == 0 or ret_dict ==0):
						ret_dict = get_xian_weather(upper_address, ret_dict)
					if (len(ret_dict) > 0 and ret_dict!=0):
						ret_dict['list'].append(
							{'entity1': address, 'rel': '属于', 'entity2': upper_address, 'entity1_type': '地点',
							 'entity2_type': '地点'})

		#匹配问题，有什么营养元素
		zhuyu = ""
		if(q_type == 2):
			index = 0
			for x in cut_statement:
				if(index > pos):
					break
				index += len(x)
				if(x[1] == 'n'):
					zhuyu = zhuyu+x[0]

			if(len(zhuyu)>0):
				ret_dict = get_nutrition(zhuyu,ret_dict)

		#匹配问题，植物学知识
		zhuyu = ""
		if(q_type == 3):
			index = 0
			for x in cut_statement:
				if(index>pos):
					break
				index += len(x)
				if(x[1] == 'n'):
					zhuyu =  zhuyu+x[0]

			if(len(zhuyu)>0):
				ret_dict = get_plant_knowledge(zhuyu,ret_dict)

		print(ret_dict)

		if(len(ret_dict)!=0  and ret_dict!=0):
			return render(request,'question_answering.html',{'ret':ret_dict})
		print(context)
		return render(request, 'question_answering.html', {'ctx':'暂未找到答案'})
	return render(request, 'question_answering.html', context)