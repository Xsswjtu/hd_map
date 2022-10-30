import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

from setting import *

road_vector_id = pd.read_sql(f"select id from d3_road_vector", conn)
for rvid in road_vector_id:
    rv_gdf = gpd.read_postgis(f"select * from d3_road_vector where id == {rvid}", conn)
    lv_gdf = gpd.read_postgis(f"select * from d3_lane_divider where rvid == {rvid}", conn)
    fig, ax = plt.subplots(1, 1)
    rv_gdf.plot(ax=ax)
    lv_gdf.plot(ax=ax)
    plt.show()

    for ldid in lv_gdf["ID"]:
        fig1, ax1 = plt.subplots(1, 1)
        lv_gdf = gpd.read_postgis(f"select * from d3_lane_divider where id == {ldid}", conn)
        lvm_gdf = gpd.read_postgis(f"select * from d3_lane_divider_marking where ldid == {ldid}", conn)
        lv_gdf.plot(ax=ax)
        lvm_gdf.plot(ax=ax)
        plt.show()


