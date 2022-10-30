import geopandas as gpd
import matplotlib.pyplot as plt

path = r"C:\Users\PC\Desktop\高精度地图\84XY-20221014\84XY-20221014\4\TrafficInfo_L.shp"
traffic_shp = gpd.read_file(path)

fig, ax = plt.subplots(1, 1)
for i in traffic_shp.index:
    new_gdf = gpd.GeoDataFrame({"index":[0], "geometry": [traffic_shp.iloc[i].geometry]}, geometry="geometry")
    new_gdf.plot(ax=ax)

plt.show()

