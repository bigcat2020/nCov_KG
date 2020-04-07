# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd
import time
import threading

class getDatas():
    def __init__(self):
        pass

    def china(self):
        url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
        try:
            reponse = requests.get(url=url).json()
            data = json.loads(reponse['data'])  # 返回数据字典
            areaTree = data['areaTree']
            china_data = areaTree[0]['children']  # childrenl里面包含了国内数据
            # 下面这个存每一个城市的数据
            china_list = [{'省份': '省份', '城市': '城市', '累计确诊': '累计确诊', '累计治愈': '累计治愈', '累计死亡': '累计死亡'}]
            # 下面这个存每一个省份的数据
            china_pro_list = [{'省份': '省份', '累计确诊': '累计确诊', '累计治愈': '累计治愈', '累计死亡': '累计死亡'}]
            for i in range(len(china_data)):
                province = china_data[i]['name']  # 各个省份

                pro_num = china_data[i]['total']['confirm']  # 各个省份数量
                pro_dead = china_data[i]['total']['dead']
                pro_heal = china_data[i]['total']['heal']
                china_pro_dict = {}
                china_pro_dict['省份'] = province
                china_pro_dict['累计确诊'] = pro_num
                china_pro_dict['累计治愈'] = pro_heal
                china_pro_dict['累计死亡'] = pro_dead
                china_pro_list.append(china_pro_dict)
                province_list = china_data[i]['children']  # 各个省的城市
                for j in range(len(province_list)):
                    city = province_list[j]['name']
                    confirm = province_list[j]['total']['confirm']  # 累计确诊人数
                    heal = province_list[j]['total']['heal']  # 累计治愈人数
                    dead = province_list[j]['total']['dead']  # 累计死亡人数
                    china_dict = {}
                    china_dict['省份'] = province
                    china_dict['城市'] = city
                    china_dict['累计确诊'] = confirm
                    china_dict['累计治愈'] = heal
                    china_dict['累计死亡'] = dead

                    china_list.append(china_dict)
            china_pro_data= pd.DataFrame(china_pro_list)
            china_pro_data.to_csv("static/map_csv/china.csv", index=False, header=False, encoding="utf-8")
            china_data = pd.DataFrame(china_list)
            china_data.to_csv("static/map_csv/china_city.csv", index=False, header=False, encoding="utf-8")
            print("中国疫情数据获取成功")
        except:
            print("中国疫情数据获取失败")

    def world(self):
        url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'
        try:
            reponse = requests.post(url=url).json()
            data = reponse['data']
            # 存每一个国家的数据
            world_list = [{'名称': '名称', '累计确诊': '累计确诊', '累计治愈': '累计治愈', '累计死亡': '累计死亡'}]
            for item in data:
                world_dict = {}
                world_dict['名称'] = item['name']
                world_dict['累计确诊'] = item['confirm']
                world_dict['累计治愈'] = item['heal']
                world_dict['累计死亡'] = item['dead']
                world_list.append(world_dict)

            world_data = pd.DataFrame(world_list)
            world_data.to_csv("static/map_csv/world.csv", index=False, header=False, encoding="utf-8")
            print("世界疫情数据获取成功!")

        except:
            print("世界疫情数据获取失败!")


def main():
    while True:
        test = getDatas()
        test.china()
        test.world()
        time.sleep(3600) #每隔一小时更新一次数据

try:
    x = threading.Thread(target=main)
    print("地图数据更新线程开启成功")
    x.start()
except:
    print("Error: 刷新地图数据线程开启失败")
