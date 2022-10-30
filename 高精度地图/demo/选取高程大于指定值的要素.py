import os

import geopandas as gpd
import pandas as pd

ori_path = r"C:\Users\PC\Desktop\高精度地图\84XY-20221014\84XY-20221014\1"

for filename in os.listdir(ori_path):
    if filename.split('.')[-1] =='shp':
        new_gdf_up = None
        new_gdf_down = None
        path = os.path.join(ori_path, filename)
        gdf = gpd.read_file(path, encodings='utf-8')
        geom_col = gdf.geometry
        if geom_col.geom_type[0] == 'Polygon':
            continue
        z_avg = []
        for geom in geom_col:
            coord = geom.wkt.split('(')[1].replace(')', '').split(', ')
            sum = 0
            for c in coord:
                sum += float(c.split(' ')[-1])
            z_avg.append(sum/len(coord))
            if sum / len(coord) > 9:
                tmp_gdf = gdf[gdf["geometry"] == geom]
                if new_gdf_up is None:
                    new_gdf_up = tmp_gdf
                else:
                    new_gdf_up = new_gdf_up.append(tmp_gdf)
            else:
                tmp_gdf = gdf[gdf["geometry"] == geom]
                if new_gdf_down is None:
                    new_gdf_down = tmp_gdf
                else:
                    new_gdf_down = new_gdf_down.append(tmp_gdf)

        save_path = r"C:\Users\PC\Desktop\高精度地图\84XY-20221014\84XY-20221014\1\上下分层\\"
        gdf["avg_h"] = z_avg
        gdf.to_file(save_path + filename.split('.')[0] + '_h.shp')
        # if new_gdf_up is not None:
        #     new_gdf_up.to_file(save_path+'上\\'+filename.split('.')[0] + '_up.shp')
        # if new_gdf_down is not None:
        #     new_gdf_down.to_file(save_path+'下\\'+filename.split('.')[0] + '_down.shp')
