from setting import *
import geopandas as gpd
from shapely.geometry import Point, LineString


def compute_avgheight(gdf):
    z_avg = []
    geom_col = gdf.geometry
    for geom in geom_col:
        coord = geom.wkt.split('(')[1].replace(')', '').split(', ')
        sum = 0
        for c in coord:
            sum += float(c.split(' ')[-1])
        z_avg.append(sum / len(coord))

    # min_z = min(z_avg)
    # if min_z <= 0:
    #     z_avg = [z_avg[i] + abs(min_z) for i in range(len(z_avg))]
    # else:
    #     z_avg = [z_avg[i] - abs(min_z) for i in range(len(z_avg))]

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

def rename_column(df):
    columns = df.columns
    rename_dict = {}
    for col in columns:
        rename_dict[col] = col.lower()
    df.rename(columns=rename_dict, inplace=True)
    return df

def import_shp(gdf, table_name):
    gdf = rename_column(gdf)
    geom_col = gdf.geometry

    new_geometry = []
    z = []

    if geom_col.geom_type[0] == 'LineString':
        for geom in geom_col:
            coord = geom.wkt.split('(')[1].replace(')', '').split(', ')
            geom_z = []
            new_geom = []
            for c in coord:
                p_coord = (c.split(' '))
                geom_z.append(float(p_coord[-1]))
                new_geom.append(Point(float(p_coord[0]), float(p_coord[1])))
            new_geometry.append(LineString(new_geom))
            z.append(geom_z)
    elif geom_col.geom_type[0] == 'Point':
        z = geom_col.z
        for i in range(len(gdf)):
            p = Point(gdf.geometry.x[i], gdf.geometry.y[i])
            new_geometry.append(p)

    gdf["geometry"] = new_geometry
    gdf["z_value"] = z
    init_crs = gdf.crs
    gdf = gdf.set_crs(init_crs)
    gdf.to_crs(f"EPSG:{SRID}", inplace=True)
    gdf.to_postgis(table_name, engine, if_exists="replace")
    print("import", table_name)

def import_data(zht_ori_path, ch_ori_path, date_num):
    # 中海庭
    zht_file_dict = {
        'efd_road_vector.shp': f'd{date_num}_road_vector',
        'efd_road_node.shp': f'd{date_num}_road_node',
        'efd_lane_node.shp': f'd{date_num}_lane_node',
        'efd_ld_chg_pt.shp': f'd{date_num}_ld_chg_pt',
        'efd_lane_vector.shp': f'd{date_num}_lane_vector',
        'efd_lane_divider.shp': f'd{date_num}_lane_divider',
        'efd_lane_divider_marking.shp': f'd{date_num}_lane_divider_marking',
    }
    for file in zht_file_dict:
        gdf = gpd.read_file(zht_ori_path + file)
        gdf["avg_h"] = compute_avgheight(gdf)
        gdf["slope"] = compute_slope(gdf)
        import_shp(gdf, zht_file_dict[file])

    # 测绘院
    ch_file_dict = {
        'TrafficInfo_L.shp': f'd{date_num}_traffic_info'
    }
    for file in ch_file_dict:
        gdf = gpd.read_file(ch_ori_path + file)
        gdf["featutename"] = compute_featurename(gdf)
        gdf["color"] = comput_color(gdf)
        gdf["solid"] = comput_solid(gdf)
        gdf["avg_h"] = compute_avgheight(gdf)
        gdf["slope"] = compute_slope(gdf)
        import_shp(gdf, ch_file_dict[file])

def output_attr(zht_ori_path, ch_ori_path, date_num):
    # 中海庭
    zht_file_dict = {
        'efd_road_vector.shp': f'd{date_num}_road_vector',
        'efd_road_node.shp': f'd{date_num}_road_node',
        'efd_lane_node.shp': f'd{date_num}_lane_node',
        'efd_ld_chg_pt.shp': f'd{date_num}_ld_chg_pt',
        'efd_lane_vector.shp': f'd{date_num}_lane_vector',
        'efd_lane_divider.shp': f'd{date_num}_lane_divider',
        'efd_lane_divider_marking.shp': f'd{date_num}_lane_divider_marking',
    }
    for file in zht_file_dict:
        gdf = gpd.read_file(zht_ori_path + file)
        columns = gdf.columns


    # 测绘院
    ch_file_dict = {
        'TrafficInfo_L.shp': f'd{date_num}_traffic_info'
    }
    for file in ch_file_dict:
        gdf = gpd.read_file(ch_ori_path + file)
        gdf["featutename"] = compute_featurename(gdf)
        gdf["color"] = comput_color(gdf)
        gdf["solid"] = comput_solid(gdf)
        gdf["avg_h"] = compute_avgheight(gdf)
        gdf["slope"] = compute_slope(gdf)
        import_shp(gdf, ch_file_dict[file])


if __name__ == '__main__':
    # 中环路
    zht_ori_path = r"C:\Users\PC\Desktop\高精度地图\国家十四五专项_上海中环路5x5_20220802_1\国家十四五专项_上海中环路5x5_20220802_1\shp" \
               r"\efd_guojiashisiwu_shanghaizhonghuanlu5x5_20220802_1\public\\"
    ch_ori_path = r"C:\Users\PC\Desktop\高精度地图\84BL-1018\84BL-1018\3\\"
    import_data(zht_ori_path, ch_ori_path, 3)



