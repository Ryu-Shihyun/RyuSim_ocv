# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import re

#文字列を数字、True, False, Noneのいずれかに変換する関数
def parse_if_number(s):
    try: return float(s)
    except: return True if s=="true" else False if s=="false" else s if s else None

# 数値に変換する関数
def parse_ndarray(s):
    return np.fromstring(s, sep=' ') if s else None

args = sys.argv
df1 = pd.read_csv(args[1], converters = {
    'attrvalue': parse_if_number,
    'binedges': parse_ndarray,
    'binvalues': parse_ndarray,
    'vectime': parse_ndarray,
    'vecvalue': parse_ndarray})

df2 = pd.read_csv(args[2], converters = {
    'attrvalue': parse_if_number,
    'binedges': parse_ndarray,
    'binvalues': parse_ndarray,
    'vectime': parse_ndarray,
    'vecvalue': parse_ndarray})

df3 = pd.read_csv(args[3], converters = {
    'attrvalue': parse_if_number,
    'binedges': parse_ndarray,
    'binvalues': parse_ndarray,
    'vectime': parse_ndarray,
    'vecvalue': parse_ndarray})

def getAoi(df):
    aoi_vector = 'aoi:vector' 
    aoi_dist_vector = 'perceptedObjectDistance:vector'

    # name='objectPerception:vector'で、vectimeの値がnullでないものを取り出す 
    aoi = df[(df["name"] == aoi_vector) & (df["vectime"].notnull())]
    # name='objectDistance:vector'で、vectimeの値がnullでないものを取り出す
    distances = df[(df["name"] == aoi_dist_vector) & (df["vectime"].notnull())]

    #データから、"module"と"vecvalue"のカラムのみ取り出す
    aois = aoi[["module", "vecvalue", "vectime"]] #各ノードの他ノードへの認識(1 or 0)
    aois.rename(columns={"vecvalue": "aoi"}, inplace=True)
    aois.rename(columns={"vectime": "time"}, inplace=True)

    distances = distances[["module", "vecvalue"]] #各ノードの他ノードとの距離(m)
    distances.rename(columns={"vecvalue": "distance"}, inplace=True) 

    # 'module'をキーとしてdistancesとperceptionsを結合
    new_df = pd.merge(distances, aois, on='module', how='inner')
    
    bins = {"aoi": [], "distance": []}
    for i in range(6):
        bins["aoi"].append([])
    for row in new_df.itertuples():
        # 手動運転車なら無視
        # if re.match("World.node\[[5-9]\d\]", row.module):
        #     continue
        # print(row.module)
        for i in range(len(row.distance)):
            if row.distance[i] < 300:
                # Ensures that we have everything in 50m chunks
                remainder = int(row.distance[i] // 50)
                bins["aoi"][remainder].append(row.aoi[i])
    distance = 50
    for dictionary in bins["aoi"]:
        bins["distance"].append(str(distance))
        distance += 50

    return bins

aois1 = getAoi(df1)
aois2 = getAoi(df2)
aois3 = getAoi(df3)

aois = [aois1, aois2, aois3]
labels = ["100 veh/km^2 ", "200 veh/km^2", "300 veh/km^2"]
colors = ["blue", "orange", "green"]

# 最大AoIが入るようにグラフを描画
fig, ax = plt.subplots()

# binsに距離と車両密度ごとに分けたaoiを格納
bins = []
for dist_i in range(len(aois1['distance'])):
    for veh_i in range(len(aois) + 1):
        if veh_i == len(aois):
            bins.append([])
        else:
            bins.append(aois[veh_i]["aoi"][dist_i])

bp = ax.boxplot(bins, 
                patch_artist=True, 
                whis=1e100, 
                medianprops=dict(color='black', linewidth=1))

# boxを塗りつぶす
for dist_i in range(len(aois1['distance'])):
    for veh_i in range(len(aois)):
        i = veh_i + dist_i * (len(aois) + 1)
        bp["boxes"][i].set_facecolor(colors[veh_i])
        bp["boxes"][i].set(color=colors[veh_i], linewidth=1)

# レジェンドの設定
legends = []
for veh_i in range(len(aois)):
    plot, = plt.plot([1, 1], colors[veh_i], linewidth=10)
    legends.append(plot)
plt.legend(legends, labels)

# x軸の設定
xtricklabels = []
for dist_i in range(len(aois1['distance'])):
    for veh_i in range(len(aois) + 1):
        if veh_i == 1:
            xtricklabels.append(aois[veh_i]["distance"][dist_i])        
        else:
            xtricklabels.append('')
ax.set_xticklabels(xtricklabels)

ax.set(xlabel='Distance (m)', ylabel="Age of Information [s]")
ax.tick_params(direction='in')
ax.set_xlim([0, len(aois1["distance"]) * (len(aois) + 1) + 1])
ax.set_ylim([0, 1.5])

plt.savefig("AOI_density.png", dpi=300)
# plt.show()
plt.close(fig)
