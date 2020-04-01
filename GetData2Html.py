#!coding:utf-8
# pyhton 3.0

import requests
import json
import re
from pyecharts.charts import Map
from pyecharts import options

result = requests.get('https://interface.sina.cn/news/wap/fymap2020_data.d.json?1580097300739&&callback=sinajp_1580097300873005379567841634181')
json_str = re.search("\(+([^)]*)\)+", result.text).group(1)
html = f"{json_str}"
table = json.loads(f"{html}")

#print(table['data'])
#print(table['data']['list'])
#print(table['data']['otherlist'])

print(table['data']['times'],"(",table['data']['mtime'],"--",table['data']['cachetime'],")")
print("中国大陆","确诊病例:",table['data']['gntotal']," | ","死亡病例:",table['data']['deathtotal']," | ","治愈病例:",table['data']['curetotal']," | ","疑似病例:",table['data']['sustotal'])
for country in table['data']['otherlist']:
    print(country['name'], "确诊病例:", country['value'], " | ", "死亡病例:", country['deathNum'], " | ", "治愈病例:",
          country['cureNum'], " | ", "疑似病例:", country['susNum'])
print("-----------------------------------中国大陆各省份详细情况--------------------------------------------------------")

for pro in table['data']['list']:
    print(pro['name'], "确诊病例:", pro['value'], " | ", "死亡病例:", pro['deathNum'], " | ", "治愈病例:",
          pro['cureNum'], " | ", "疑似病例:", pro['susNum'])


province_data = []
#循环获取省份名称和对应的确诊数据
for province in table['data']['list']:
    #将省份数据添加到列表中去
    province_data.append((province['name'], province['value']))

    city_data = []
    #循环获取城市名称和对应的确诊数据
    for city in province['city']:
        #这里要注意对应上地图的名字需要使用mapName这个字段
        city_data.append((city['mapName'], city['conNum']))

    #使用Map，创建省份地图
    map_province = Map()
    #设置地图上的标题和数据标记，添加省份和确诊人数
    #自定义数据范围和对应的颜色，这里我是取色工具获取的颜色值，不容易呀。
    #设置是否为分段显示
    map_province.set_global_opts(title_opts=options.TitleOpts(title=province['name'] + "实时疫情图-确诊人数：" + province['value']), visualmap_opts=options.VisualMapOpts(is_piecewise=True,
        pieces=[
                    {"min": 1000, "label": '>1000人', "color": "#6F171F"},
                    {"min": 500, "max": 1000, "label": '500-1000人', "color": "#C92C34"},
                    {"min": 100, "max": 499, "label": '100-499人', "color": "#E35B52"},
                    {"min": 10, "max": 99, "label": '10-99人', "color": "#F39E86"},
                    {"min": 1, "max": 9, "label": '1-9人', "color": "#FDEBD0"}]))
    #将数据添加进去，生成省份地图，所以maptype要对应省份。
    map_province.add("确诊", city_data, maptype = province['name'])
    #一切完成，那么生成一个省份的html网页文件，取上对应省份的名字。
    map_province.render(province['name'] + ".html")

#创建国家地图
map_country = Map()
#设置地图上的标题和数据标记，添加确诊人数
map_country.set_global_opts(title_opts=options.TitleOpts(title="中国实时疫情图-确诊人数：" + table['data']["gntotal"]), visualmap_opts=options.VisualMapOpts(is_piecewise=True,#设置是否为分段显示
                #自定义数据范围和对应的颜色，这里我是取色工具获取的颜色值，不容易呀。
                pieces=[
                    {"min": 1000, "label": '>1000人', "color": "#6F171F"}, # 不指定 max，表示 max 为无限大（Infinity）。
                    {"min": 500, "max": 1000, "label": '500-1000人', "color": "#C92C34"},
                    {"min": 100, "max": 499, "label": '100-499人', "color": "#E35B52"},
                    {"min": 10, "max": 99, "label": '10-99人', "color": "#F39E86"},
                    {"min": 1, "max": 9, "label": '1-9人', "color": "#FDEBD0"}]))
#将数据添加进去，生成中国地图，所以maptype要对应china。
map_country.add("确诊", province_data, maptype="china")
#一切完成，那么生成一个html网页文件。
map_country.render("country.html")

