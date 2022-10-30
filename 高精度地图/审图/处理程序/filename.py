import os

path = r"C:\Users\Xushan\Desktop\高精度地图\四平路（赤峰路-国权路）\四平路（赤峰路-国权路）\84blh\\"

for filename in os.listdir(path):
    if filename.split('.')[1] == 'shp':
        print(filename.split('.')[0])