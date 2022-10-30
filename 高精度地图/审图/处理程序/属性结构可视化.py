import os

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

ori_path = r"C:\Users\Xushan\Desktop\高精度地图\审图\腾讯"
check_path = r"C:\Users\Xushan\Desktop\高精度地图\审图\检查结果"
stand_path = r"C:\Users\Xushan\Desktop\高精度地图\审图\标准格式"
stand_df = pd.read_csv(os.path.join(stand_path, '腾讯-标准格式.csv'), header=0)
stand_dict = {'道路': ['Road','RoadNode','RoadAttribute','Name', 'NameRelation', 'JunctionArea'],
              '车道': ['Lane','LaneAttribute','LaneMarking','LaneMarkingAttribute'],
              'CSH': ['CSH'],
              '限制信息': ['RestrictionGroup','RestrictionLine','RestrictionPoint'],
              '特征点': ['FeaturePoint'],
              'Object': ['RoadMark', 'Facility', 'Pole', 'SubTrafficSign','StopLine','TrafficLight','TrafficSign'],
              '拓扑关系': ['RoadConnectivity','LaneConnectivity','ObjectRelation','TrafficControl'],
              '来源': ['SourceInfo']
              }

with open(os.path.join(stand_path, '腾讯-标准格式-思维导图.txt'), 'w', encoding='utf-8') as f:
    f.write('腾讯高级辅助驾驶地图\n')
    for s_class in stand_dict.keys():
        f.write(f"\t{s_class}\n")
        for i in stand_dict[s_class]:
            f.write(f"\t\t{i}\n")
            for attr in stand_df[stand_df['filename']==i]['attr'].values:
                f.write(f"\t\t\t{attr}\n")
