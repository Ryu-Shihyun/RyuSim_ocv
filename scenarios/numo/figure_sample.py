import sys
import csv
import pprint
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import math
import seaborn as sns

OVER_SIZE_LIMIT = 200_000_000

csv.field_size_limit(OVER_SIZE_LIMIT)

args = sys.argv
mode = "" # evaluation mode
option="" # label ex) option="test" => mode_test.png
ss = "./results/sps_smooth2_rri100.csv" #file 1
sd = "./results/ds_smooth2.csv" #file 2


if len(args)>=5:
    sd=args[4]
if len(args)>=4 :
    ss=args[3]
if len(args)>=3:
    option=args[2]
if len(args)>=2 :
    mode=args[1]
# command example
# python3 figure_sample.py mode option ss sd

# 柳くん方式
def transFroat (array):
    num_array=[]
    for a in array:
        num_array.append(float(a))
    return num_array

def transInt (array):
    num_array=[]
    for a in array:
        num_array.append(int(a))
    return num_array
    
if mode == "pdr_sample":
    # 例えば、pdrと車間距離の関係を調べる
    # これらは違うデータなのでそのままだとグラフが作れない
    # 
    # 対処方法１：宮田くん方式
    # 公式ドキュメントにやり方が書いてある。pandsを使うことでデータセットを作って操作する方法。
    # なれると楽だし、コードもスッキリするが、使いこなすのに手間がかかる
    # 
    # 対処方法２：柳くん方式
    # 無理やりグラフ用データを作る方法。配列、辞書、For文などプロ基礎の知識で作れる
    # データの作り方の工夫が必要なのと、コードが膨大になることが欠点
    # 例）tbDecodeとtxRxDestanceだが、timestampが一致している　＝＞　nodeそれぞれデータ作って組み合わせ{node:[tbDecode,txRxDistance]}を作ろう
    # 
    # とりあえず２つ作るので、どちらがいいかは選んでね
    pdrs=[] 
    pdrs2=[]
    pdrs_total=[]
    pdrs2_total=[]
    decodes = {}
    decodes2={}
    distances =[] # [0, 10, 20, 30,...500]
    for i in range(51):
        distances.append(i*10)
        pdrs.append(0)
        pdrs2.append(0)
        pdrs_total.append(0)
        pdrs2_total.append(0)

    # SPS
    with open(ss) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == "tbDecoded:vector":#信号受信した時、Decodeできたかどうか
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = transInt(re.split(" ",row[8]))
                if vehicle not in decodes:
                    decodes[vehicle] = [array,[]]
                else:
                    decodes[vehicle][0] = array
            elif row[1] == "vector" and row[3] == "txRxDistanceTB:vector":#送受信間の距離
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = transFroat(re.split(" ",row[8]))
                if vehicle not in decodes:
                    decodes[vehicle] = [[],array]
                else:
                    decodes[vehicle][1] = array
    for v in decodes.keys():
        decode = decodes[v][0]
        distance = decodes[v][1]
        for i in range(len(decode)):
            index = int(distance[i]//10)
            if index > 50:
                continue  
            pdrs[index] = 100*((pdrs[index] * pdrs_total[index]) + decode[i]) / (pdrs_total[index]+1)
            pdrs_total[index] += 1

    # DS
    with open(sd) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == "tbDecoded:vector":#信号受信した時、Decodeできたかどうか
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = transInt(re.split(" ",row[8]))
                if vehicle not in decodes2:
                    decodes2[vehicle] = [array,[]]
                else:
                    decodes2[vehicle][0] = array
            elif row[1] == "vector" and row[3] == "txRxDistanceTB:vector":#送受信間の距離
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = transFroat(re.split(" ",row[8]))
                if vehicle not in decodes2:
                    decodes2[vehicle] = [[],array]
                else:
                    decodes2[vehicle][1] = array
    for v in decodes2.keys():
        decode = decodes2[v][0]
        distance = decodes2[v][1]
        for i in range(len(decode)):
            index = int(distance[i]//10)
            if index > 50:
                continue 
            pdrs2[index] = 100*((pdrs2[index] * pdrs2_total[index]) + decode[i]) / (pdrs2_total[index]+1)
            pdrs2_total[index] += 1
    fig, ax = plt.subplots()
        

    ax.plot(distances, pdrs, label="sb-sps")
    ax.plot(distances, pdrs2, label="ds")
    


    yl="Packet Delivery Ratio %"
    ax.set(xlabel='Distance (m)', ylabel=yl)
    ax.legend(loc="lower left")
    ax.tick_params(direction='in')
    ax.set_xlim([0, (max(distances) + 1)])
    # ax.set_ylim([0, 101])
    plt.xticks(np.arange(0, (max(distances))+50, step=50))
    plt.yticks(np.arange(0, (101), step=10))



    plt.savefig(mode+"_"+option, dpi=300)
 
    


# 宮田くん方式
def parse_if_number(s):
    try: return float(s)
    except: return True if s=="true" else False if s=="false" else s if s else None

def parse_ndarray(s):
    return np.fromstring(s, sep=' ') if s else None

if mode == "pdr_sample2.py":
    save = mode
    ss ="results/intersection_0.05.sps.csv"
    sd = 'results/intersection_0.05.sps.csv'
    
    df = pd.read_csv(ss, converters = {
        'attrvalue': parse_if_number,
        'binedges': parse_ndarray,
        'binvalues': parse_ndarray,
        'vectime': parse_ndarray,
        'vecvalue': parse_ndarray})
    pdr_vector = 'tbDecoded:vector'
    l = "PDR"
    yl="Packet Delivery Ratio %"
    
    pdr_dist_vector = 'txRxDistanceTB:vector'

    distances = df[(df["name"] == pdr_dist_vector) & (df["vectime"].notnull())]
    decoded = df[(df["name"] == pdr_vector) & (df["vectime"].notnull())]
    distances = distances[["module", "vecvalue"]]
    distances.rename(columns={"vecvalue": "distance"}, inplace=True)
    decoded = decoded[["module", "vecvalue"]]
    decoded.rename(columns={"vecvalue": "decode"}, inplace=True)
    new_df = pd.merge(distances, decoded, on='module', how='inner')
    bins = []
    for i in range(50):
        bins.append({"count": 0, "success": 0})

    for row in new_df.itertuples():
        for i in range(len(row.distance)):
            if row.distance[i] < 300:
                # Ensures that we have everything in 10m chunks
                remainder = int(row.distance[i] // 10)
                if row.decode[i] >= 0:
                    # Only count TBs sent i.e. -1 will be ignored in result
                    bins[remainder]["count"] += 1
                    bins[remainder]["success"] += row.decode[i]

    pdrs = []
    distances = []
    distance = 0
    for dictionary in bins:
        try:
            pdrs.append((dictionary["success"] / dictionary["count"] * 100))
        except ZeroDivisionError:
            pdrs.append(0)
        distances.append(distance)
        distance += 10
    #ds
    df = pd.read_csv(sd, converters = {
        'attrvalue': parse_if_number,
        'binedges': parse_ndarray,
        'binvalues': parse_ndarray,
        'vectime': parse_ndarray,
        'vecvalue': parse_ndarray})
    if mode=="pdr":
        pdr_vector = 'tbDecoded:vector'
        l = "PDR"
        yl="Packet Delivery Ratio %"
    elif mode == "interference":
        pdr_vector = 'tbFailedDueToInterference:vector'
        l = "Interference"
        yl="Packet Loss Ratio %"
    elif mode=="halfDuplex":
        pdr_vector = 'tbFailedHalfDuplex:vector'
        l = "HalfDuplex"
        yl="HalfDuplex Ratio %"
    elif mode=="sci" :
        pdr_vector = 'tbFailedDueToInterferenceIgnoreSCI:vector'
        l = "SCI"
        yl="SCI Ignore Ratio %"

    pdr_dist_vector = 'txRxDistanceTB:vector'

    distances2 = df[(df["name"] == pdr_dist_vector) & (df["vectime"].notnull())]
    decoded = df[(df["name"] == pdr_vector) & (df["vectime"].notnull())]
    distances2 = distances2[["module", "vecvalue"]]
    distances2.rename(columns={"vecvalue": "distance"}, inplace=True)
    decoded = decoded[["module", "vecvalue"]]
    decoded.rename(columns={"vecvalue": "decode"}, inplace=True)
    new_df = pd.merge(distances2, decoded, on='module', how='inner')
    bins = []
    for i in range(50):
        bins.append({"count": 0, "success": 0})

    for row in new_df.itertuples():
        for i in range(len(row.distance)):
            if row.distance[i] < 500:
                # Ensures that we have everything in 10m chunks
                remainder = int(row.distance[i] // 10)
                if row.decode[i] >= 0:
                    # Only count TBs sent i.e. -1 will be ignored in result
                    bins[remainder]["count"] += 1
                    bins[remainder]["success"] += row.decode[i]

    pdrs2 = []
    for dictionary in bins:
        try:
            pdrs2.append((dictionary["success"] / dictionary["count"] * 100))
        except ZeroDivisionError:
            pdrs2.append(0)
    
    fig, ax = plt.subplots()
        

    ax.plot(distances, pdrs, label="sb-sps")
    ax.plot(distances, pdrs2, label="ds")
    



    ax.set(xlabel='Distance (m)', ylabel=yl)
    ax.legend(loc="lower left")
    ax.tick_params(direction='in')
    ax.set_xlim([0, (max(distances) + 1)])
    # ax.set_ylim([0, 101])
    plt.xticks(np.arange(0, (max(distances))+50, step=50))
    plt.yticks(np.arange(0, (101), step=10))



    plt.savefig(save+"_"+option, dpi=300)
 