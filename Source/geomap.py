import os
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Geo,Map
from pyecharts.globals import ChartType, SymbolType
from pyecharts.globals import ThemeType
import json

# city_names = list()
# with open( 'd:\\data\\cities.json','r',encoding='utf-8' ) as f:
#     citydict = json.load( f )
#     cities = citydict['PINYIN_MAP']
#     for (city, pinyin) in cities.items():
#         city_names.append(city)

# data = pd.read_csv('d:\\data\\data.csv')
# with open( 'd:\\data\\data1.csv', 'w', encoding='utf-8') as f:
#     lines = ['城市,确诊人数\n']
#     for index, row in data.iterrows():
#         if str(row['城市']) in city_names:
#             lines.append( str(row['城市']) +',' + str(row['确诊人数'])+'\n' )
#     f.writelines(lines)
#     print( lines )
# exit()

Result=pd.DataFrame()
Result1=pd.DataFrame()
data = pd.read_csv('d:\\data\\data.csv')

data_City=data["城市"]
data_Numbers=data["确诊人数"]
Result1=pd.concat([data_City,data_Numbers], axis=1)
Result=pd.concat([Result, Result1])

data=[]
for i in range(len(Result)):
    turple=(Result.iat[i,0],int(Result.iat[i,1]))
    data.append(turple)
print(data)
def geo_virus() -> Geo:
    c = (
        Geo(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_schema(maptype="china")
        .add("",data,ChartType.EFFECT_SCATTER,#选择地图类型
        is_selected = True,symbol = None,symbol_size= 6,color="red",is_large=True,)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(visualmap_opts=opts.VisualMapOpts(is_piecewise=True,max_=30000,),
                         title_opts=opts.TitleOpts(title="全国各城市新型冠状病毒感染分布图",
                         pos_left="100", pos_right='100')
        )
    )
    return c

g=geo_virus()#调用一下这个定义的函数
g.render('全国新型冠状病毒感染分布图.html')