import math
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy
import jenkspy

from setting import  *

def compute_avgheight(gdf):
    z_avg = []
    geom_col = gdf.geometry
    for geom in geom_col:
        coord = geom.wkt.split('(')[1].replace(')', '').split(', ')
        sum = 0
        for c in coord:
            sum += float(c.split(' ')[-1])
        z_avg.append(sum / len(coord))

    min_z = min(z_avg)
    if min_z <= 0:
        z_avg = [z_avg[i] + abs(min_z) for i in range(len(z_avg))]
    else:
        z_avg = [z_avg[i] - abs(min_z) for i in range(len(z_avg))]

    return z_avg

def comput_color(gdf):
    color_list = []
    color_col = gdf["FEATURECOD"].values
    for i in color_col:
        attr = CEHUI_DICT[i]
        if attr.find('白色') > 0:
            color = 'white'
        elif attr.find('黄色') > 0:
            color = 'yellow'
        else:
            color = 'unknown'
        color_list.append(color)
    return color_list

def comput_solid(gdf):
    solid_list = []
    solid_col = gdf["FEATURECOD"].values
    for i in solid_col:
        attr = CEHUI_DICT[i]
        if attr.find("实线") > 0:
            solid = "solid"
        elif attr.find("虚线") > 0:
            solid = 'dot'
        else:
            solid = 'unknown'
        solid_list.append(solid)
    return solid_list

def compute_featurename(gdf):
    name_list = []
    color_col = gdf["FEATURECOD"].values
    for i in color_col:
        attr = CEHUI_DICT[i]
        name_list.append(attr)
    return name_list

def compute_slope(gdf):
    slope_list = []
    geom_col = gdf.geometry
    for geom in geom_col:
        length = geom.length
        coord = geom.wkt.split('(')[1].replace(')', '').split(', ')
        start = coord[0].split(' ')[-1]
        end = coord[-1].split(' ')[-1]
        slope = 0.01 * abs(float(start) - float(end)) / (length+(0.1)**10)
        slope_list.append(slope)

    return slope_list


def main():
    ori_path = r'C:\Users\PC\Desktop\高精度地图\84BL-1018\84BL-1018\3\\'
    shp_name = 'TrafficInfo_L.shp'
    path = ori_path + shp_name
    gdf = gpd.read_file(path)
    gdf["featutename"] = compute_featurename(gdf)
    gdf["color"] = comput_color(gdf)
    gdf["solid"] = comput_solid(gdf)
    gdf["avg_h"] = compute_avgheight(gdf)
    gdf["slope"] = compute_slope(gdf)

    ava_list = []
    for i in range(len(gdf)):
        h = gdf["avg_h"][i]
        if h > 10:
            tmp = 3
        elif h < 0:
            tmp = 4
        else:
            tmp = 1
        if gdf["FEATURECOD"][i] in [401113, 401122, 401142, 41211]:
            tmp = -1

        ava_list.append(tmp)

    gdf["available"] = ava_list

    gdf.to_file(ori_path + '\\预处理\\' + shp_name, encodings='utf-8')

def zhonghaiting_main():
    ori_path = r'C:\Users\PC\Desktop\高精度地图\国家十四五专项_上海中环路5x5_20220802_1\国家十四五专项_上海中环路5x5_20220802_1\shp\efd_guojiashisiwu_shanghaizhonghuanlu5x5_20220802_1\public\\'
    # shp_name = 'TrafficInfo_L.shp'
    shp_name = 'efd_lane_divider_marking.shp'
    path = ori_path + shp_name
    gdf = gpd.read_file(path)
    gdf["avg_h"] = compute_avgheight(gdf)
    gdf["slope"] = compute_slope(gdf)

    gdf.to_file(ori_path + '\\预处理\\' + shp_name, encodings='utf-8')

if __name__ == '__main__':
    main()