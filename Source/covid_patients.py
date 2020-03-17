import pandas as pd
import numpy as np
import re
import time

#从csv文件中读取确诊、出院、死亡人数，提供查询功能

def day2int( day ):
    ret = re.findall('^\d{1,2}|\d{1,2}', day)
    if len(ret)==2:
        return int(ret[0])*100 + int(ret[1])
    else:
        return 0

#根据地区、国家、城市进行过滤
def filter_by_local( pdata, localname=''):
    if localname!='': #根据国家查询
        if localname in pdata['国家'].values:
            pdata = pdata[pdata['国家']==localname]
        elif localname in pdata['地区'].values:
            pdata = pdata[pdata['地区']==localname]
        elif localname in pdata['城市'].values:
            pdata = pdata[pdata['城市']==localname]
        else:
            return None
    return pdata

#根据时间过滤
def filter_by_date( pdata, date ):
    if date!='':
        lastday = day2int(date)
        return pdata[pdata['报道时间']<=lastday]
    return pdata

def get_patients( pdata, localname='', lastday='' ):
    pdata = filter_by_date( pdata, lastday )
    if pdata is None:
        return 0
    pdata = filter_by_local( pdata, localname=localname )
    if pdata is None:
        return 0
    pp = pd.pivot_table(pdata,index=['报道时间','国家','地区','城市'],values=['新增确诊','新增出院','新增死亡'],aggfunc='sum')
    #numbers = [int(pp['新增确诊'].sum()), int(pp['新增出院'].sum()), int(pp['新增死亡'].sum())]
    return pp

def fill_none_data( up ):
    up['新增确诊'] = up['新增确诊'].fillna(value=0)
    up['新增出院'] = up['新增出院'].fillna(value=0)
    up['新增死亡'] = up['新增死亡'].fillna(value=0)
    up['城市'] = up['城市'].fillna(value='')
    return up

up = pd.read_csv('../data/covid_data.csv',encoding='utf8')
up = fill_none_data(up)
#'报道时间', '国家', '地区', '城市', '新增确诊', '新增出院', '新增死亡', '消息来源'

#日期值替换为整数，便于搜索
reg = re.compile('^\d{1,2}|\d{1,2}')
up['报道时间'] = up['报道时间'].map(lambda x: int(re.findall(reg,x)[0])*100+int(re.findall(reg,x)[1]))

country = up.groupby(['报道时间','国家']).sum()
print(country)

print(get_patients(up, localname='广元市', lastday='3月5日'))
print(get_patients(up, localname='四川', lastday='3月5日'))
ret = get_patients(up, localname='中国', lastday='3月15日')
num = ret['新增确诊'] - ret['新增出院'] - ret['新增死亡']
print(num[:].sum())

