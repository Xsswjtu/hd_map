import os

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

ori_path = r"C:\Users\Xushan\Desktop\高精度地图\审图\腾讯"
check_path = r"C:\Users\Xushan\Desktop\高精度地图\审图\检查结果"
stand_path = r"C:\Users\Xushan\Desktop\高精度地图\审图\标准格式"

stand_df = pd.read_csv(os.path.join(stand_path, '腾讯-标准格式.csv'), header=0)

def Integrity_of_attributes(stand_df, check_df):
    # 图层完整
    file_s = stand_df["filename"].unique()
    file_c = check_df['filename'].unique()
    print("实际图层总数：", len(file_c))
    for i in file_s:
        if i in file_c:
            continue
        else:
            file_s = file_s[file_s != i]
            print('缺失图层：', i)

    # 属性完整
    for file in file_s:
        attr_s = stand_df[stand_df["filename"] == file]['attr'].values
        attr_c = check_df[check_df["filename"] == file]['attr'].values
        for i in attr_c:
            if i in attr_s:
                continue
            else:
                print('缺失属性：', file, i)

def attr_check(file_path):
    # 地物属性检查
    file = 'CSH.csv'
    df = pd.read_csv(os.path.join(file_path, file))
    # 横坡
    print("**横坡")
    seleva_min = -60
    seleve_max = 60
    attr = 'SELEVATION'
    attr_col = df[attr]
    attr_type = attr_col.dtypes
    if attr_type == np.int64:
        print("***已采用分级表达")
        print("***分级精度优于0.1")
    else:
        print("***未采用分级表达***")

    if max(attr_col) < seleve_max*10**1 and min(attr_col)>seleva_min*10**1:
        print("***横坡值在范围内")
    else:
        print("***横坡值不在范围内***")

    # 纵坡
    attr = 'SLOPE'
    print("**纵坡")
    slope_min = -60
    slope_max = 60
    attr_col = df[attr]
    attr_type = attr_col.dtypes
    if attr_type == np.int64:
        print("***已采用分级表达")
        print("***分级精度优于0.1")
    else:
        print("***未采用分级表达***")

    if max(attr_col) < slope_max*10**1 and min(attr_col)>slope_min*10**1:
        print("***纵坡值在范围内")
    else:
        print("***纵坡值不在范围内***")

    # 曲率
    attr = 'CURVATURE'
    print("**曲率")
    cur_min = -90
    cur_max = 90
    attr_col = df[attr]
    attr_type = attr_col.dtypes
    if attr_type == np.int64:
        print("***已采用分级表达")
        print("***分级精度优于10^-5")
    else:
        print("***未采用分级表达***")

    if max(attr_col) < cur_max*10**5 and min(attr_col) > cur_min*10**5:
        print("***曲率在范围内")
    else:
        print("***纵坡值不在范围内***")

for file in os.listdir(ori_path):
    print(f'*开始检查文件{file}')
    file_path = os.path.join(ori_path, file)

    print(f'**地物属性检查')
    attr_check(file_path)

    print(f'**数据结构检查')
    check_df = pd.DataFrame(columns=['filename', 'attr', 'attr type'])
    for filename in os.listdir(file_path):
        df = pd.read_csv(os.path.join(file_path, filename))
        for i in df.columns:
            type = df[i].dtypes
            check_df = check_df.append({'filename': filename.split('.')[0], 'attr': i, 'attr type': type}, ignore_index=True)
    integrity = Integrity_of_attributes(stand_df, check_df)
    print(f'*文件{file}检查完毕\n')





