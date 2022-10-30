import os
import geopandas as gpd
import pandas as pd

xml_path = r'C:\Users\Xushan\Desktop\高精度地图\欧阳剑需求_上海指定图幅_20220713_1\欧阳剑需求_上海指定图幅_20220713_1\ouyangjianxuqiu_shanghaizhidingtufu_20220713_2\public\\'

f = open("test.txt", "w", encoding='utf-8')

for file_name in os.listdir(xml_path):
    if file_name.split('.')[-1] == 'shp':
        print(file_name.split('.')[0].lower())
        f.write(file_name.split('.')[0].lower())
        # f.write('\n' + '属性')
        # gdf = gpd.read_file(xml_path+file_name)
        # print(gdf.columns.values)
        # for i in gdf.columns.values:
        #     f.write(str(i)+',')
        f.write('\n')