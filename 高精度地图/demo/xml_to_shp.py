import time
from xml.etree import ElementTree
import geopandas
import pandas as pd
from shapely.geometry import Point, LineString
import os

file_dict = {
    "Confidence": [],
    "LineString": {
                    "lane_linestring": ['x', 'y', 'z', 'yaw', 'width'],
                    "curb_linestring": ['x', 'y', 'z'],
                    "POSE_t_x_y_z_vx_vy_vz_roll_pitch_yaw_status": ['t', 'x', 'y', 'z', 'vx', 'vy', 'vz', 'roll', 'pitch', 'yaw', 'status'],
                    },
    "Point_lon_lat_alt_height": ['x', 'y', 'z', 'height'],
    "ObserPOSE_t_x_y_z_yaw_speed": ['t', 'x', 'y', 'z', 'vx', 'vy', 'vz']}

def new_shp(attr, last_tag, tag, text):
    text = [i.split(',') for i in text]
    df = []
    gdf = []
    if last_tag == 'LineString':
        if tag == 'POSE_t_x_y_z_vx_vy_vz_roll_pitch_yaw_status':
            df = pd.DataFrame(text, columns=file_dict["LineString"]["POSE_t_x_y_z_vx_vy_vz_roll_pitch_yaw_status"])
        elif attr["name"].find("Lane")==0:
            df = pd.DataFrame(text, columns=file_dict["LineString"]["lane_linestring"])
        elif attr["name"].find("Curb")==0:
            df = pd.DataFrame(text, columns=file_dict["LineString"]["curb_linestring"])
        df = df.dropna()
        geom = LineString([(float(x), float(y), float(z)) for x, y, z in list(df[['x', 'y', 'z']].values)])
        gdf = geopandas.GeoDataFrame({"name": [attr["name"]]}, geometry=[geom], crs="EPSG:4326", index=[0])
    elif last_tag == 'Point_lon_lat_alt_height':
        df = pd.DataFrame(text, columns=file_dict["Point_lon_lat_alt_height"])
        df = df.dropna()
        geom = [Point(float(x), float(y), float(z)) for x, y, z in list(df[['x', 'y', 'z']].values)]
        gdf = geopandas.GeoDataFrame(df, geometry=geom, crs="EPSG:4326")
    return gdf

def save_gdf(new_dict, save_path, ori_file_name, file_count):
    gdf = new_dict["shp"]
    file_name = new_dict['name'] + '_' + ori_file_name.split('.')[0][-3:] + '_' + str(file_count)
    print(file_name)
    if 'position' in new_dict:
        file_name = file_name + new_dict['position']
    gdf.to_file(save_path + file_name + '.shp')
    return file_count + 1


xml_path = r'C:\Users\Xushan\Desktop\高精度地图\HSD同济数据\\'
ori_save_path = r'C:\Users\Xushan\Desktop\高精度地图\HSD同济数据矢量化\\'

for file_name in os.listdir(xml_path):
    if file_name.split('.')[1] == 'xml':
        save_path = ori_save_path
        tree = ElementTree.parse(xml_path+file_name)
        root = tree.getroot()

        file_count = 0
        for child in root:
            if child.tag == 'Placemark':
                attr_dict = dict()
                new_dict = dict()
                count = 0
                flag = 0
                for i in child:
                    if i.tag in file_dict.keys():
                        if i.tag == 'Confidence':
                            new_dict['Confidence'] = i.text
                        elif i.tag == 'ObserPOSE_t_x_y_z_yaw_speed':
                            new_dict['ObserPOSE_t_x_y_z_yaw_speed'] = i.text
                            flag = 1
                            print(new_dict)
                            file_count = save_gdf(new_dict, save_path+str(count), file_name, file_count)
                        for j in i:
                            count = count + 1
                            gdf = new_shp(attr_dict, i.tag, j.tag, j.text.split(' '))
                            new_dict = attr_dict.copy()
                            new_dict['shp'] = gdf
                    else:
                        attr_dict[i.tag] = i.text

                if count == 1 and flag == 0:
                    print('1', new_dict)
                    file_count = save_gdf(new_dict, save_path, file_name, file_count)



