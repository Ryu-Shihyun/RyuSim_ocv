# from omnetpp.scave import results, chart, utils
import sys
import csv
import pprint
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re

OVER_SIZE_LIMIT = 200_000_000

csv.field_size_limit(OVER_SIZE_LIMIT)

args = sys.argv
camTransmitTimestamps = []
camsSize = []
numCollision=0 #mode 4 でリソース割当てる時の衝突数
numGen=0#mode 4でリソース割当
collisionRateSps=[] #spsでの衝突率
collisionRateDs=[]  #dsでの衝突率
mode = ""
option=""

def add_value_label(x_list, y_list):
    # y_dash_list = []
    # for j in range(0,len(y_list))
    #     y_dash_list.append(round(y_list[j]))
    for i in range(0, len(x_list)):
        plt.annotate(round(y_list[i],2), (i, y_list[i]))

# def parse_if_number(s):
#     try: return float(s)
#     except: return True if s=="true" else False if s=="false" else s if s else None
# def parse_ndarray(s):
#     return np.fromstring(s, sep=' ') if s else None
# file = ""
# if len(args) < 2: 
#     file = 'test.csv'
# else:
#     file = args[1]
if len(args)>=3:
    option=args[2]
if len(args)>=2 :
    mode=args[1]



#CAM送信のtimestamp取得 
# with open(file) as f:
#     reader = csv.reader(f)
#     for row in reader:
#         if row[1] == 'vector' and row[3]=='numberTransmittedPackets:vector':
#             timestamp = row[15]
#             camTransmitTimestamps.append(timestamp.split(' '))


#CAMの衝突回数/CAMの生成数 vs車の通行率================================================
if mode=="collision" :
    left = [1,2,3,4,5,6,7,8,9,10]
    fig = plt.figure()
    # sps
    for i in range(1,11):
        numCollision=0 #mode 4 でリソース割当てる時の衝突数
        numGen=0#mode 4でリソース割当
        s = "results/sps_exp("+str(i)+")_highway.csv"
        with open(s) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] == 'statistic' and row[3]=="packetCollisionMode4:stats":
                    numCollision = numCollision + int(row[7])
                elif row[1] == 'statistic' and row[3]=="numberCAMSGenerated:stats":
                    numGen =numGen + int (row[7])
        collisionRateSps.append(numCollision*1.0/numGen)


    # ds
    for i in range(1,11):
        numCollision=0 #mode 4 でリソース割当てる時の衝突数
        numGen=0#mode 4でリソース割当
        s = "results/ds_exp("+str(i)+")_highway.csv"
        with open(s) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] == 'statistic' and row[3]=="packetCollisionMode4:stats":
                    numCollision = numCollision + int(row[7])
                elif row[1] == 'statistic' and row[3]=="numberCAMSGenerated:stats":
                    numGen = numGen +  int (row[7])
        collisionRateDs.append(numCollision*1.0/numGen)

    print(collisionRateSps)
    print(collisionRateDs)
    plt.plot(left,collisionRateSps)
    plt.plot(left,collisionRateDs)
    plt.xlabel("Vehicle transit rate [veh/s]")
    plt.ylabel("Packet Collision Rate")
    save = "packetCollision"
    fig.savefig(save+"_"+option)

# ========================================================================

#送信間隔　Vs 個数 ===========================================================
elif mode == "interval" :
    # sps
    left = ["100","200", "300", "400", "500", "600", "700", "800", "900", "1000"]
    tp = {}
    plt.rcParams['figure.subplot.bottom'] = 0.2
    vehicles={}
    fig, ax= plt.subplots()
    ax.get_xticklabels()
    # plt.xticks(fontsize=9)
    # plt.xticks(rotation=45)
    # tp[index]= ["[100,200)", "[200,300)", "[300,400)", "[400,500)", "[500,600)", "[600,700)"]
    for i in range(0,1):
        s = "data/camTimeStamp_ds.csv"
        sendinterval=[0,0,0,0,0,0,0,0,0,0]# [100,200), [200,300), [300,400), [400,500), [500,600), [600,700), [700,800), (800,900], (900,1000], 
        # fig, ax= plt.subplots()
        
        with open(s) as f:
            reader = csv.reader(f)
            # id : [time, time, ....]
            for row in reader:
                id = row[1]
                time = float(row[0])
                if id in vehicles:
                    vehicles[id].append(time)
                else:
                    vehicles[id]=[time]
        #time diff => sendinterval
        for v in vehicles.values():
            isFirst=True
            post=0.0
            for t in v:
                if isFirst:
                    post=t
                    isFirst=False
                else:
                    value = round((float(t)-post)*10)
                    # print(str(t)+" "+str(post)+" "+str(value))
                    sendinterval[value-1] = sendinterval[value-1] + 1
                    post=float(t)
        print(sendinterval)
        key = str(i*500)
        tp[key] = sendinterval
            # plt.bar(left,height,width=1.0,edgecolor="black",linewidth=1)
    
    df = pd.DataFrame(tp,left)
            # plt.grid()
    
    ax.set_xticks(sendinterval)
    # ax.set_xticklabels(left)
    plt.xlabel("Generation Intaerval [ms]")
    plt.ylabel("Number of CAM")
    df.plot.bar(ax=ax)
    # plt.setp(left, rotation=45, fontsize=9)
    plt.xticks(fontsize=9)
    plt.xticks(rotation=45)
    save = "interval"
    fig.savefig(save+"_"+option)

#リソース衝突回数/割当総数 vs車の通行率================================================
# subchannels =[[t_index,[f_index,..]],



def add_use(arr1,arr2):
    min=int(arr1[0]) #最初のサブチャネルのインデックス
    max=int(arr1[len(arr1)-1]) #最後のサブチャネルのインデックス
    for i in range(min,max+1):
        arr2[i] = arr2[i]+1


def regist_subchannels(data,subs):
    isFound = False
    for el in subs:
        if data[0]==el[0] : #時間が同じ
            isFound = True
            add_use(data[1],el[1]) #subsのサブチャネルとdataのサブチャネルでかぶっているところを探し、カウントする
            break
    if isFound==False:
        newEl = [0]*21 #サブチャネルの数を多めにした。インデックスi番目がかぶると、i番目の値にかぶった分カウントされる
        # print(data[1])
        add_use(data[1],newEl)
        subs.append([data[0],newEl])


def count_overlap(arr):
    count=0
    for i in arr:
        for j in i[1]:
            if(j>1):
                count = count+1
                break     
    
    return count
            
                


if mode=="resource" :
    # left = [500,1000,1500,2000,2500,3000,3500]
    left = ["intersection a","intersection b", "street c", "street d"]
    # fig = plt.figure()
    plt.rcParams['figure.subplot.bottom'] = 0.14
    fig, ax= plt.subplots()
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, fontsize=9)
   
    tp = {}
    # sps
    
    numCollision=0 #mode 4 でリソース割当てる時の衝突数
    numGen=0#mode 4でリソース割当
    s = "data/resourcesAllocation_sps2.csv" 
    subchannels=[]
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            data=[]
            data.append(row[0])
            array = row[1].split(' ') + row[2].split(' ')
            data.append(array)
            regist_subchannels(data,subchannels)
    numGen=len(subchannels)
    numCollision=count_overlap(subchannels)
    print("numCollision:"+str(numCollision))
    print("numGen:"+str(numGen))
    # collisionRateSps.append(numCollision*100.0/numGen)
    key="a"
    tp[key]=numCollision*100.0/numGen


    numCollision=0 #mode 4 でリソース割当てる時の衝突数
    numGen=0#mode 4でリソース割当
    s = "data/resourcesAllocation_sps2.csv" 
    subchannels=[]
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            data=[]
            data.append(row[0])
            array = row[1].split(' ') + row[2].split(' ')
            data.append(array)
            regist_subchannels(data,subchannels)
    numGen=len(subchannels)
    numCollision=count_overlap(subchannels)
    print("numCollision:"+str(numCollision))
    print("numGen:"+str(numGen))
    collisionRateSps.append(numCollision*100.0/numGen)
    key="a"
    tp[key]=collisionRateSps

    # ds

    for i in range(1,2):
        numCollision=0 #mode 4 でリソース割当てる時の衝突数
        numGen=0#mode 4でリソース割当
        s = "data/resourcesAllocation_ds.csv" 
        subchannels=[]
        with open(s) as f:
            reader = csv.reader(f)
            for row in reader:
                data=[]
                data.append(row[0])
                array = row[1].split(' ') + row[2].split(' ')
                data.append(array)
                regist_subchannels(data,subchannels)
        numGen=len(subchannels)
        numCollision=count_overlap(subchannels)
        print("numCollision:"+str(numCollision))
        print("numGen:"+str(numGen))
        collisionRateDs.append(numCollision*100.0/numGen)
    key="DS"
    tp[key]=collisionRateDs

    print(collisionRateSps)
    print(collisionRateDs)
    df = pd.DataFrame(tp,left)
    # plt.bar(left,collisionRateSps,width=5,edgecolor="black",linewidth=1)
    # plt.bar(left,collisionRateDs,width=5,edgecolor="black",linewidth=1)
    # plt.plot(left,collisionRateSps)
    # plt.plot(left,collisionRateDs)
    plt.xlabel("Vehicle transit rate [veh/h]")
    plt.ylabel("Resource Collision Rate [%]")
    
    df.plot.bar(ax=ax)
    # add_value_label(left,collisionRateSps)
    # add_value_label(left,collisionRateDs)
    plt.xticks(rotation=0)
    save = "resourceCollision"
    fig.savefig(save+"_"+option)


# Packet Delivery Ratio ===================================
def parse_if_number(s):
    try: return float(s)
    except: return True if s=="true" else False if s=="false" else s if s else None

def parse_ndarray(s):
    return np.fromstring(s, sep=' ') if s else None

if mode in ["pdr", "interference", "halfDuplex","sci"]:
    save = mode
    l =""
    yl = ""
    csv_s ="results/intersection_0.05.sps.csv"
    csv_d = 'results/intersection_0.05.sps.csv'
    if len(args)>=4:
        csv_s= args[3]
    if len(args)>=5:
        csv_d = args[4]
    df = pd.read_csv(csv_s, converters = {
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
    df = pd.read_csv(csv_d, converters = {
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
            if row.distance[i] < 300:
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
    
# ========================================================================

#CAM送信のsize取得
# with open(file) as f:
#     reader = csv.reader(f)
#     for row in reader:
#         if row[1] == 'vector' and row[3]=='dataPDUSizeTransmitted:vector':
#             size = row[16]
#             camsSize.append(size.split(' '))
# print(camsSize)0

#========================================================================
# positionを考慮したPDR

if mode=="posPDR":
    node_pos = {}
    interjunction_pdr={}
    interjunction_dist={}
    interjunction_node=[]
    interjunction_pos=[9475.0,9725.0,14575.0,14825.0] #left up,left down, right up, right down
    street_pdr={}
    street_dist={}
    street_node=[]
    street_pos=[9500.0,9600.0,14160.0,14510.0] #left up,left down, right up, right down
    fig, ax = plt.subplots()
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, fontsize=9)
    # bar graph
    tp = {}
    left = ["interjunction","street"]
    for i in range(0,1):
        #sps
        s = "./results/sps-high.csv"
        marginX = 0
        marginY=0
        with open(s) as f:
            reader = csv.reader(f)
            posX_mean = 'posX:vector'
            for row in  reader:
                if row[1] == 'vector'and row[3] == posX_mean:
                    nodeStr = re.split("[\[\]]",row[2])
                    # print(nodeStr)
                    nodeID = int(nodeStr[1])
                    posx = re.split(" ",row[8])
                    node_pos[nodeID] = []
                    # print(posx)
                    for x  in posx:
                        node_pos[nodeID].append([float(x),0.0])
                    # for x in posx:
                    #     if float(x) >= interjunction_pos[0][0]-marginX and float(x) >= interjunction_pos[1][0]-marginX and float(x) <= interjunction_pos[2][0]+marginX and float(x) <= interjunction_pos[3][0]+marginX :
                    #         interjunction_node.append(nodeID)
                    #         break
                    #     elif float(x) >= street_pos[0][0]-marginX and float(x) >= street_pos[1][0]-marginX and float(x) <= street_pos[2][0]+marginX and float(x) <= street_pos[3][0]+marginX :
                    #         street_node.append(nodeID)
                    #         break
        # print(node_pos)   
        with open(s) as f:
            reader = csv.reader(f)
            posY_mean = 'posY:vector'
            for row in  reader:
                if row[1] == 'vector'and row[3] == posY_mean:
                    nodeStr = re.split("[\[\]]",row[2])
                    nodeID = int(nodeStr[1])
                    posy = re.split(" ",row[8])
                    # print(posy)
                    for i in range(0,len(posy)):
                        node_pos[nodeID][i][1]= float(posy[i])
                    # for y in posy:
                    #     if nodeID in interjunction_node:    
                    #         if not (float(y) >= interjunction_pos[0][1]+marginY and float(y) >= interjunction_pos[1][1]-marginY and float(y) <= interjunction_pos[2][1]+marginY and float(y) <= interjunction_pos[3][1]-marginY) :
                    #             interjunction_node.remove(nodeID)
                    #     elif nodeID in street_node:
                    #         if not (float(y) >= street_pos[0][1]+marginY and float(y) >= street_pos[1][1]-marginY and float(y) <= street_pos[2][1]+marginY and float(y) <= street_pos[3][1]-marginY) :
                    #             street_node.remove(nodeID)
            
        # print(len(node_pos))
        # print(node_pos[0])  
# # 交差点か直線道路に所属しているかどうかを判断し、分類。重複の場合、両方に分類
        for id in node_pos.keys():
            isIncludeI = False
            isIncludeS = False
            isIncludeI2 = False
            isIncludeS2 = False
            for i in range(0,len(node_pos[id])):
                if node_pos[id][i][0] >= interjunction_pos[0]-marginX and node_pos[id][i][1] >= interjunction_pos[2]-marginY and node_pos[id][i][0] <= interjunction_pos[1]+marginX and node_pos[id][i][1] <= interjunction_pos[3]+marginY:
                    isIncludeI=True
                if isIncludeI:
                    interjunction_node.append(id)
                    break
            for i in range(0,len(node_pos[id])):
                if  node_pos[id][i][0] >= street_pos[0]-marginX and node_pos[id][i][1] >= street_pos[2]-marginY and node_pos[id][i][0] <= street_pos[1]+marginX and node_pos[id][i][1] <= street_pos[3]+marginY:
                    isIncludeS=True
                if isIncludeS:
                    street_node.append(id)
                    break
        #     for i in range(0,len(node_pos[id])):
        #         if node_pos[id][i][0] >= interjunction2_pos[0]-marginX and node_pos[id][i][1] >= interjunction2_pos[2]-marginY and node_pos[id][i][0] <= interjunction2_pos[1]+marginX and node_pos[id][i][1] <= interjunction2_pos[3]+marginY:
        #             isIncludeI2=True
        #         if isIncludeI2:
        #             interjunction2_node.append(id)
        #             break
        #     for i in range(0,len(node_pos[id])):
        #         if  node_pos[id][i][0] >= street2_pos[0]-marginX and node_pos[id][i][1] >= street2_pos[2]-marginY and node_pos[id][i][0] <= street2_pos[1]+marginX and node_pos[id][i][1] <= street2_pos[3]+marginY:
        #             isIncludeS2=True
        #         if isIncludeS2:
        #             street2_node.append(id)
        #             break
        print(interjunction_node)
        print(street_node)
        with open(s) as f:
            reader = csv.reader(f)    
            pdr_vector = 'tbDecoded:vector'
            # pdr_vector ='tbFailedDueToInterference:vector'
            
            pdr_dist_vector = 'txRxDistanceTB:vector'
            for row in reader:
                if row[1] == 'vector'and row[3] == pdr_vector:
                    nodeStr = re.split("[\[\]]",row[2])
                    nodeID = int(nodeStr[1])
                    timearr = re.split(" ",row[7])
                    arr = re.split(" ",row[8])
                    if nodeID in interjunction_node:
                        interjunction_pdr[nodeID] = [timearr,arr]
                    if nodeID in street_node:
                        street_pdr[nodeID] = [timearr,arr]
                elif row[1] == 'vector'and row[3] == pdr_dist_vector:
                    nodeStr = re.split("[\[\]]",row[2])
                    nodeID = int(nodeStr[1])
                    timearr = re.split(" ",row[7])
                    isf_i=False
                    isf_s=False
                    if nodeID in interjunction_node:
                        interjunction_dist[nodeID] = [timearr,arr]
                    if nodeID in street_node:
                        street_dist[nodeID] = [timearr,arr]
    #10mごとのsuccess / count
    # interjunction_pdr_sorted= sorted(interjunction_pdr.items(), key=lambda x:x[0])
    # interjunction_dist_sorted=sorted(interjunction_dist.items(), key=lambda x:x[0])
    # street_pdr_sorted= sorted(street_pdr.items(), key=lambda x:x[0])
    # street_dist_sorted= sorted(street_dist.items(), key=lambda x:x[0])
    bins_i = []
    bins_s = []
    count_i = 0
    success_i=0
    count_s = 0
    success_s=0
    for i in range(50):
        bins_i.append({"count": 0, "success": 0})
        bins_s.append({"count": 0, "success": 0})
    # print(len(interjunction_pdr))
    for key in interjunction_pdr.keys() :
        # print(len(interjunction_pdr[key][1]))
        # print(len(interjunction_dist[key][1]))
        for i in range(len(interjunction_pdr[key][1])):
            dist_i = interjunction_dist[key][0].index(interjunction_pdr[key][0][i])
            # print(dist_i)
            if dist_i >= len(interjunction_dist[key][1]):
                break
            if float(interjunction_dist[key][1][dist_i]) <= 10:
                remainder = int(float(interjunction_dist[key][1][dist_i]) // 0.2)
                if int(interjunction_pdr[key][1][i]) >= 0:
                    # Only count TBs sent i.e. -1 will be ignored in result
                    bins_i[remainder]["count"] += 1
                    bins_i[remainder]["success"] += int(interjunction_pdr[key][1][i])
                    count_i += 1
                    success_i += int(interjunction_pdr[key][1][i])
    for key in  street_pdr.keys() :
        for i in range(len(street_pdr[key][1])):
            dist_i = street_dist[key][0].index(street_pdr[key][0][i])
            if dist_i >= len(street_dist[key][1]):
                break
            if float(street_dist[key][1][dist_i]) <= 10:
                remainder = int(float(street_dist[key][1][dist_i]) // 0.2)
                if int(street_pdr[key][1][i]) >= 0:
                    # Only count TBs sent i.e. -1 will be ignored in result
                    bins_s[remainder]["count"] += 1
                    bins_s[remainder]["success"] += int(street_pdr[key][1][i])
                    count_s += 1
                    success_s += int(street_pdr[key][1][i])
    
    tp["sb-sps"]=[success_i/count_i*100.0, success_s/count_s*100.0]

    l_i = "interjunction_sps"
    l_s = "street_sps"
    # yl="Packet Delivery Ratio %"
    pdrs_i = []
    pdrs_s = []
    distances = []
    distance = 0
    for dictionary in bins_i:
        if dictionary["count"]>0 :
            pdrs_i.append((dictionary["success"] / dictionary["count"] * 100))
        else:
            pdrs_i.append(0.0)
        distances.append(distance)
        distance += 10
    for dictionary in bins_s:
        if dictionary["count"]>0 :
            pdrs_s.append((dictionary["success"] / dictionary["count"] * 100))
        else:
            pdrs_s.append(0.0)
    # ax.plot(distances, pdrs_i, label=l_i)
    # ax.plot(distances, pdrs_s, label=l_s)


    ##DS=========================
    node_pos = {}
    interjunction_pdr={}
    interjunction_dist={}
    interjunction_node=[]
    street_pdr={}
    street_dist={}
    street_node=[]

    for i in range(0,1):
        s = "./results/ds_high.csv"
        marginX = 800
        marginY=800
        with open(s) as f:
            reader = csv.reader(f)
            posX_mean = 'posX:vector'
            for row in  reader:
                if row[1] == 'vector'and row[3] == posX_mean:
                    nodeStr = re.split("[\[\]]",row[2])
                    # print(nodeStr)
                    nodeID = int(nodeStr[1])
                    posx = re.split(" ",row[8])
                    node_pos[nodeID] = []
                    # print(posx)
                    for x  in posx:
                        node_pos[nodeID].append([float(x),0.0])
                    # for x in posx:
                    #     if float(x) >= interjunction_pos[0][0]-marginX and float(x) >= interjunction_pos[1][0]-marginX and float(x) <= interjunction_pos[2][0]+marginX and float(x) <= interjunction_pos[3][0]+marginX :
                    #         interjunction_node.append(nodeID)
                    #         break
                    #     elif float(x) >= street_pos[0][0]-marginX and float(x) >= street_pos[1][0]-marginX and float(x) <= street_pos[2][0]+marginX and float(x) <= street_pos[3][0]+marginX :
                    #         street_node.append(nodeID)
                    #         break
        # print(node_pos)   
        with open(s) as f:
            reader = csv.reader(f)
            posY_mean = 'posY:vector'
            for row in  reader:
                if row[1] == 'vector'and row[3] == posY_mean:
                    nodeStr = re.split("[\[\]]",row[2])
                    nodeID = int(nodeStr[1])
                    posy = re.split(" ",row[8])
                    # print(posy)
                    for i in range(0,len(posy)):
                        node_pos[nodeID][i][1]= float(posy[i])
                    # for y in posy:
                    #     if nodeID in interjunction_node:    
                    #         if not (float(y) >= interjunction_pos[0][1]+marginY and float(y) >= interjunction_pos[1][1]-marginY and float(y) <= interjunction_pos[2][1]+marginY and float(y) <= interjunction_pos[3][1]-marginY) :
                    #             interjunction_node.remove(nodeID)
                    #     elif nodeID in street_node:
                    #         if not (float(y) >= street_pos[0][1]+marginY and float(y) >= street_pos[1][1]-marginY and float(y) <= street_pos[2][1]+marginY and float(y) <= street_pos[3][1]-marginY) :
                    #             street_node.remove(nodeID)
            
        # print(len(node_pos))
        # print(node_pos[0])  
        for id in node_pos.keys():
            isIncludeI = False
            isIncludeS = False
            for i in range(0,len(node_pos[id])):
                if node_pos[id][i][0] >= interjunction_pos[0]-marginX and node_pos[id][i][1] >= interjunction_pos[3]-marginY and node_pos[id][i][0] <= interjunction_pos[1]+marginX and node_pos[id][i][1] <= interjunction_pos[2]+marginY:
                    isIncludeI=True
                elif  node_pos[id][i][0] >= street_pos[0]-marginX and node_pos[id][i][1] >= street_pos[3]-marginY and node_pos[id][i][0] <= street_pos[1]+marginX and node_pos[id][i][1] <= street_pos[2]+marginY:
                    isIncludeS=True
                if isIncludeI:
                    interjunction_node.append(id)
                    break
                if isIncludeS:
                    street_node.append(id)
                    break
        print(interjunction_node)
        print(street_node)
        with open(s) as f:
            reader = csv.reader(f)    
            pdr_vector = 'tbDecoded:vector'
            # pdr_vector = 'tbFailedDueToInterference:vector'
            pdr_dist_vector = 'txRxDistanceTB:vector'
            for row in reader:
                if row[1] == 'vector'and row[3] == pdr_vector:
                    nodeStr = re.split("[\[\]]",row[2])
                    nodeID = int(nodeStr[1])
                    timearr = re.split(" ",row[7])
                    arr = re.split(" ",row[8])
                    if nodeID in interjunction_node:
                        interjunction_pdr[nodeID] = [timearr,arr]
                    if nodeID in street_node:
                        street_pdr[nodeID] = [timearr,arr]
                elif row[1] == 'vector'and row[3] == pdr_dist_vector:
                    nodeStr = re.split("[\[\]]",row[2])
                    nodeID = int(nodeStr[1])
                    timearr = re.split(" ",row[7])
                    isf_i=False
                    isf_s=False
                    if nodeID in interjunction_node:
                        interjunction_dist[nodeID] = [timearr,arr]
                    if nodeID in street_node:
                        street_dist[nodeID] = [timearr,arr]
    #10mごとのsuccess / count
    # interjunction_pdr_sorted= sorted(interjunction_pdr.items(), key=lambda x:x[0])
    # interjunction_dist_sorted=sorted(interjunction_dist.items(), key=lambda x:x[0])
    # street_pdr_sorted= sorted(street_pdr.items(), key=lambda x:x[0])
    # street_dist_sorted= sorted(street_dist.items(), key=lambda x:x[0])
    bins_i = []
    bins_s = []
    count_i = 0
    success_i=0
    count_s = 0
    success_s=0
    for i in range(50):
        bins_i.append({"count": 0, "success": 0})
        bins_s.append({"count": 0, "success": 0})
    # print(len(interjunction_pdr))
    for key in interjunction_pdr.keys() :
        # print(len(interjunction_pdr[key][1]))
        # print(len(interjunction_dist[key][1]))
        for i in range(len(interjunction_pdr[key][1])):
            dist_i = interjunction_dist[key][0].index(interjunction_pdr[key][0][i])
            # print(dist_i)
            if dist_i >= len(interjunction_dist[key][1]):
                break
            if float(interjunction_dist[key][1][dist_i]) <= 10:
                remainder = int(float(interjunction_dist[key][1][dist_i]) // 0.2)
                if int(interjunction_pdr[key][1][i]) >= 0:
                    # Only count TBs sent i.e. -1 will be ignored in result
                    bins_i[remainder]["count"] += 1
                    bins_i[remainder]["success"] += int(interjunction_pdr[key][1][i])
                    count_i += 1
                    success_i += int(interjunction_pdr[key][1][i])
    for key in  street_pdr.keys() :
        for i in range(len(street_pdr[key][1])):
            dist_i = street_dist[key][0].index(street_pdr[key][0][i])
            if dist_i >= len(street_dist[key][1]):
                break
            if float(street_dist[key][1][dist_i]) <= 10:
                remainder = int(float(street_dist[key][1][dist_i]) // 0.2)
                if int(street_pdr[key][1][i]) >= 0:
                    # Only count TBs sent i.e. -1 will be ignored in result
                    bins_s[remainder]["count"] += 1
                    bins_s[remainder]["success"] += int(street_pdr[key][1][i])
                    count_s += 1
                    success_s += int(street_pdr[key][1][i])
    
    tp["ds"]=[success_i/count_i*100.0, success_s/count_s*100.0]

    l_i = "interjunction_ds"
    l_s = "street_ds"
    yl="Packet Delivery Ratio %"
    pdrs_i = []
    pdrs_s = []
    distances = []
    distance = 0
    for dictionary in bins_i:
        if dictionary["count"]>0 :
            pdrs_i.append((dictionary["success"] / dictionary["count"] * 100))
        else:
            pdrs_i.append(0.0)
        distances.append(distance)
        distance += 10
    for dictionary in bins_s:
        if dictionary["count"]>0 :
            pdrs_s.append((dictionary["success"] / dictionary["count"] * 100))
        else:
            pdrs_s.append(0.0)
        
    # ax.plot(distances, pdrs_i, label=l_i)
    # ax.plot(distances, pdrs_s, label=l_s)
    
    # ax.set(xlabel='Distance (m)', ylabel=yl)
    # ax.legend(loc="lower left")
    # ax.tick_params(direction='in')
    # ax.set_xlim([0, (max(distances) + 1)])
    # ax.set_xlim([0, (max(distances) + 1)])
    # ax.set_ylim([0, 101])
    # plt.xticks(np.arange(0, 11, step=1))
    # plt.yticks(np.arange(0, (31), step=5))
    # plt.savefig(mode+"_"+option, dpi=300)
    print(tp)
    df = pd.DataFrame(tp,left)
    # plt.xlabel("")
    plt.ylabel(yl)
    
    df.plot.bar(ax=ax)
    plt.xticks(rotation=0)
    save = mode + "_bar"
    fig.savefig(save+"_"+option)


if mode == "resourceMap":
    s = "data/resourcesAllocation_sps_high.csv" 
    subchannels=[]
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            data=[]
            data.append(row[0])
            array = row[1].split(' ') + row[2].split(' ')
            data.append(array)
            regist_subchannels(data,subchannels)
    numGen=len(subchannels)
    numCollision=count_overlap(subchannels)
    print("high traffic")
    print("sps")
    print(subchannels)
    print("numCollision:"+str(numCollision))
    print("numGen:"+str(numGen))
    print("collision rate:"+str(numCollision/numGen*1.0))

    s = "data/resourcesAllocation_ds_high.csv" 
    subchannels=[]
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            data=[]
            data.append(row[0])
            array = row[1].split(' ') + row[2].split(' ')
            data.append(array)
            regist_subchannels(data,subchannels)
    numGen=len(subchannels)
    numCollision=count_overlap(subchannels)
    print("ds")
    print("numCollision:"+str(numCollision))
    print("numGen:"+str(numGen))
    print("collision rate:"+str(numCollision/numGen*1.0))

    s = "data/resourcesAllocation_test.csv" 
    subchannels=[]
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            data=[]
            data.append(row[0])
            array = row[1].split(' ') + row[2].split(' ')
            data.append(array)
            regist_subchannels(data,subchannels)
    numGen=len(subchannels)
    numCollision=count_overlap(subchannels)
    print("low traffic")
    print("sps")
    print("numCollision:"+str(numCollision))
    print("numGen:"+str(numGen))
    print("collision rate:"+str(numCollision/numGen*1.0))

    s = "data/resourcesAllocation_ds.csv" 
    subchannels=[]
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            data=[]
            data.append(row[0])
            array = row[1].split(' ') + row[2].split(' ')
            data.append(array)
            regist_subchannels(data,subchannels)
    numGen=len(subchannels)
    numCollision=count_overlap(subchannels)
    print("ds")
    print("numCollision:"+str(numCollision))
    print("numGen:"+str(numGen))
    print("collision rate:"+str(numCollision/numGen*1.0))


#=============================================================
if mode=="pos_confirm" :
    s1 ="data/stationIdList_sps_high.csv"
    s2 = "data/camTimeStamp_sps_high.csv"
    v_s = []
    v_m = []
    maxX_s = 0
    minX_s = 0
    maxY_s = 0
    minY_s = 0
    maxX_m = 0
    minX_m = 0
    maxY_m = 0
    minY_m = 0
    so = ["281030","274406","239013","272045","224232","274406","281397","266134","278171","268631","241023","274079","263254","263831","262590","281101","259677","269573","262434","251313","241865","270878","258547","268286","269288","259073","257408","262795","268859","260595","258911","258230","257824","251330","270367","257179","258461","252777","278859","271784","264173","248901","268419","257160","263810","277504","253904","255434","252205","219808","219496","266134","268948"]
    mitsu = ["270927","236281","270929","270705","249833","268354","230094","234366","250493","227837","234779","242455","236142","235209","276084","222407","224968","216925","242705","266999","241224","234950","273261","269612","264411","233515","234968","238094","239471","242471","215182","280942","261664","277043","272766","273027","266291","270223","256852","232596","282277","219218","279073","212405","254511","262093","274495"]
    with open(s1) as f:
        reader = csv.reader(f)
        for row in  reader:
            if row[3] in so:
                v_s.append(row[1])
            elif row[3] in mitsu:
                v_m.append(row[1])
    with open(s2) as f:
        reader = csv.reader(f)
        for row in  reader:
            if row[1] in v_s:
                if minX_s <=0 or minX_s > float(row[3]):
                    minX_s = float(row[3])
                if maxX_s <=0 or maxX_s < float(row[3]):
                    maxX_s = float(row[3])
                if minY_s <= 0 or minY_s > float(row[4]):
                    minY_s = float(row[4])
                if maxY_s <= 0 or maxY_s < float(row[4]):
                    maxY_s = float(row[4])
            elif row[1] in v_m:
                if minX_m <=0 or minX_m > float(row[3]):
                    minX_m = float(row[3])
                if maxX_m <=0 or maxX_m < float(row[3]):
                    maxX_m = float(row[3])
                if minY_m <= 0 or minY_m > float(row[4]):
                    minY_m = float(row[4])
                if maxY_m <= 0 or maxY_m < float(row[4]):
                    maxY_m = float(row[4])
    print("so_x:" + str(minX_s)+ "~" + str(maxX_s) + ", span:" + str(maxX_s-minX_s))
    print("so_y:" + str(minY_s)+ "~" + str(maxY_s) + ", span:" + str(maxY_s-minY_s))
    print("mitsu_x:" + str(minX_m)+ "~" + str(maxX_m) + ", span:" + str(maxX_m-minX_m))
    print("mitsu_y:" + str(minY_m)+ "~" + str(maxY_m) + ", span:" + str(maxY_m-minY_m))
    
if mode == "cam_pos":
    # numo
    # x: sumo - artery = 310
    # y: sumo + artery = 30940

    # intersection b : [9475.0,9615.0,13985.0,14125.0]
    # intersection a : [9475.0,9725.0,14575.0,14825.0]
    # street c : [9500.0,9600.0,14160.0,14510.0]
    # street d : [9670.0,10270.0,14670.0,14750.0]
    # intersection_pos = [9475.0,9725.0,14575.0,14825.0]#a
    intersection_pos = [9475.0,9615.0,13985.0,14125.0]#b
    # intersection_pos = [0.0,1000.0,0.0,1000.0]
    
    # street_pos = [0.0,1000.0,0.0,1000.0]
    street_pos = [9500.0,9600.0,14160.0,14510.0]#c
    #street_pos = [9670.0,10270.0,14670.0,14750.0] #d
    s = "results/sps_smooth2_rri100.csv"
    s_i = "results/intersection_b_test.csv"
    s_s= "results/street_c_test.csv"
    csv_i =[]
    csv_s = []
    poses_i={}
    poses_s={}
    count_i = 0
    count_s = 0
    cam_i = {}
    cam_s = {}
    v_i=[]
    v_s=[]
    node_i=[]
    node_s=[]
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            # position x
            if row[1] == "vector" and row[3] == "camSentPositionX:vector":
                
                vehicle = re.split("[\[\]]",row[2])[1]
                v_poses = re.split(" ",row[8])
                times = re.split(" ",row[7])
                for i in range(len(v_poses)):
                    if float(v_poses[i]) >= intersection_pos[0] and float(v_poses[i]) <= intersection_pos[1]:
                        count_i += 1
                        # intersectionにいる間のCAMの受信率とか調べられたらいいよね
                        key = "node_" + vehicle + "_" + times[i]
                        if key in poses_i:
                            poses_i[key][0] = float(v_poses[i])
                            poses_i[key][2] = True
                        else:
                            poses_i[key] = [float(v_poses[i]),0.0,False,0.0,0]
            
                    if float(v_poses[i]) >= street_pos[0] and float(v_poses[i]) <= street_pos[1]:
                        count_s += 1
                        key = "node_" + vehicle + "_" + times[i]
                        if key in poses_s:
                            poses_s[key][0] = float(v_poses[i])
                            poses_s[key][2] = True
                        else:
                            poses_s[key] = [float(v_poses[i]),0.0,False,0.0,0]
            # position y
            elif row[1] == "vector" and row[3] == "camSentPositionY:vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                v_poses = re.split(" ",row[8])
                times = re.split(" ",row[7])
                for i in range(len(v_poses)):
                    if float(v_poses[i]) >= intersection_pos[2] and float(v_poses[i]) <= intersection_pos[3]:
                        count_i += 1
                        # intersectionにいる間のCAMの受信率とか調べられたらいいよね
                        key = "node_" + vehicle + "_" + times[i]
                        if key in poses_i:
                            poses_i[key][1] = float(v_poses[i])
                            poses_i[key][2] = True
                        else:
                            poses_i[key] = [0.0,float(v_poses[i]),False,0.0,0]
                    
                    if float(v_poses[i]) >= street_pos[2] and float(v_poses[i]) <= street_pos[3]:
                        count_s += 1
                        key = "node_" + vehicle + "_" + times[i]
                        if key in poses_s:
                            poses_s[key][1] = float(v_poses[i])
                            poses_s[key][2] = True
                        else:
                            poses_s[key] = [0.0,float(v_poses[i]),False,0.0,0]
    
    


                        
                        
    # print(poses_i)
    # 道路に存在する車のIDを取得する
    # v_i, v_sに入れる
    # csv = [nodeID, vehicle, time, x, y, speed, trigger]
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3]== "camVehicleId:vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                nodeID = re.split(" ",row[8])[0]
                target = "node_" + vehicle+"_"
                filter_poses_i = dict(filter(lambda vh:target in vh[0],poses_i.items()))
                filter_poses_s = dict(filter(lambda vh:target in vh[0],poses_s.items()))
                for k in filter_poses_i.keys():
                    if filter_poses_i[k][2]:
                        if nodeID not in v_i: 
                            v_i.append(nodeID)
                            node_i.append([vehicle,nodeID])
                        # print("find_i")
                        time = re.split("_",k)[2]
                        csv_i.append([nodeID,vehicle,time,filter_poses_i[k][0],filter_poses_i[k][1],filter_poses_i[k][3],filter_poses_i[k][4]])
                for k in filter_poses_s.keys():
                    if filter_poses_s[k][2]:
                        if nodeID not in v_s:
                            v_s.append(nodeID)
                            node_s.append([vehicle,nodeID])
                        # print("find_s")
                        time = re.split("_",k)[2]
                        csv_s.append([nodeID,vehicle,time,filter_poses_s[k][0],filter_poses_s[k][1],filter_poses_s[k][3],filter_poses_s[k][4]])
    
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            # speed
            if row[1] == "vector" and row[3] == "camSentSpeed:vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                v_speed = re.split(" ",row[8])
                times = re.split(" ",row[7])
                for i in range(len(v_speed)):
                    
                    for c in csv_i:
                        if vehicle == c[1] and times[i] == c[2] : c[5] = v_speed[i]
                    for c in csv_s:
                        if vehicle == c[1] and times[i] == c[2] : c[5] = v_speed[i]
                    
            elif row[1] == "vector" and row[3] in ["camTriggerPosition:vector", "camTriggerHead:vector", "camTriggerSpeed:vector"]:
                vehicle = re.split("[\[\]]",row[2])[1]
                el = re.split(" ",row[8])
                times = re.split(" ",row[7])
                
                for i in range(len(el)):
                   
                    for c in csv_i:
                        if vehicle == c[1] and times[i] == c[2] :
                            if row[3] == "camTriggerHead:vector":
                                c[6] = 1
                            elif row[3] == "camTriggerPosition:vector":
                                c[6] = 2
                            elif row[3] == "camTriggerSpeed:vector":
                                c[6] = 3

                    for c in csv_s:
                        if vehicle == c[1] and times[i] == c[2] :
                            if row[3] == "camTriggerHead:vector":
                                c[6] = 1
                            elif row[3] == "camTriggerPosition:vector":
                                c[6] = 2
                            elif row[3] == "camTriggerSpeed:vector":
                                c[6] = 3

            
                    
    print("intersection\nCAM:" + str(count_i)+", vehicle:" + str(len(v_i))+", /veh:" + str(count_i/len(v_i)*1.0)+", " + str(node_i))
    print("street\nCAM:" + str(count_s)+", vehicle:" + str(len(v_s))+", /veh:" + str(count_s/len(v_s)*1.0)+"%, " + str(node_s))

    with open(s_i,"w") as f:
        writer  = csv.writer(f)
        writer.writerows(csv_i)
    with open(s_s,"w") as f:
        writer = csv.writer(f)
        writer.writerows(csv_s)
    print("csv ok\nfinish!")
        
    # fh = open("data/headingDelta_ds2.csv")
    # fp = open("data/positionDelta_ds2.csv")
    # fs = open("data/speedDelta_ds2.csv")
    
    # reader_h = csv.reader(fh)
    # reader_p = csv.reader(fp)
    # reader_s = csv.reader(fs)

    # nHeadi = 0
    # nHeads = 0
    # nPosi  = 0
    # nPoss =0
    # nSpeedi =0
    # nSpeeds = 0

    # for row in reader_h:
    #     if row[1] in v_i:
    #         if row[0] in cam_i[row[1]]:
    #             nHeadi += 1
    #     elif row[1] in v_s:
    #         if row[0] in cam_s[row[1]]:
    #             nHeads += 1
    # for row in reader_p:
    #     if row[1] in v_i:
    #         if row[0] in cam_i[row[1]]:
    #             nPosi += 1
    #     elif row[1] in v_s:
    #         if row[0] in cam_s[row[1]]:
    #             nPoss += 1
    # for row in reader_s:
    #     if row[1] in v_i:
    #         if row[0] in cam_i[row[1]]:
    #             nSpeedi += 1
    #     elif row[1] in v_s:
    #         if row[0] in cam_s[row[1]]:
    #             nSpeeds += 1
    
    # print("intersection: head = " + str(nHeadi/(nHeadi+nPosi+nSpeedi)*100.0) + "%, position = "  + str(nPosi/(nHeadi+nPosi+nSpeedi)*100.0) + "%, speed = " + str(nSpeedi/(nHeadi+nPosi+nSpeedi)*100.0)) 
    # print("street: head = " + str(nHeads/(nHeads+nPoss+nSpeeds)*100.0) + "%, position = "  + str(nPoss/(nHeads+nPoss+nSpeeds)*100.0) + "%, speed = " + str(nSpeeds/(nHeads+nPoss+nSpeeds)*100.0)) 
    


if mode == "posPDR_new":
    node_pos = {}
    interjunction_pdr={}
    interjunction_dist={}
    interjunction_node=[]
    interjunction_pos=[9475.0,9725.0,14575.0,14825.0] #intersection a
    interjunction2_pdr={}
    interjunction2_dist={}
    interjunction2_node=[]
    interjunction2_pos=[9475.0,9615.0,13985.0,14125.0] #intersection b
    street_pdr={}
    street_dist={}
    street_node=[]
    street_pos=[9500.0,9600.0,14160.0,14510.0] #street c
    street2_pdr={}
    street2_dist={}
    street2_node=[]
    street2_pos=[9670.0,10270.0,14670.0,14750.0] #street d
    INTERSECTION_A_NODE = {'430':'552910253','294':'2025187190','1196':'962980710','950':'1287726651','1920':'1921376925','985':'2135019593','1035':'2078107280','412':'1329132133','1788':'1945891638','466':'1144522535','1754':'204428608','572':'1376035217','903':'219544266','1403':'922587542','912':'1671735990','834':'670752506','1220':'1690492373','1023':'610486506','1444':'1221389873','1555':'1565306616','395':'114723506','494':'1402961682','456':'559301039','502':'1941690360','543':'318561886','1517':'703955951','350':'1253207672','1931':'995097051','951':'146533149','332':'1797073940','1991':'517408978','864':'1370973813','1879':'346502533','1588':'578187134','1961':'138700754','835':'2025554010','1418':'1069117832','352':'1414647625','895':'1669475776','918':'1875641892','1186':'1587992726','1268':'1947691087','1314':'1569115921','1965':'237140292','1594':'87522686','1222':'1984498433','1924':'1320634492','1435':'419914800','1582':'263043320','817':'1487053959','1832':'2026478004','1636':'940472515','797':'1581539848','1816':'1386214636','1120':'318322042','926':'1267889618','426':'739273303','1221':'1111800030','1276':'1390598089','1948':'1680687005','935':'772634225','1182':'1926411641','1258':'692981712','1562':'354367395','1294':'1256273378','512':'1184214677','1433':'1989200801','1674':'1438865740','2081':'1758204253'}
    INTERSECTION_B_NODE = {'315':'1469262009','1935':'2070707654','929':'1663080928','774':'628966950','254':'1308044878','1912':'132629780','1833':'1659239833','356':'1896306640','128':'1610120709','100':'1036140795','1090':'1607774548','967':'413360099','1005':'12548159','83':'1889947178','1117':'1903409954','1241':'415675634','1043':'1143195511','1475':'116423768','1411':'858829294','1269':'245240853','431':'1671294892','652':'1543324176','585':'1647149314','1604':'819827984','1590':'1578716908','187':'1626276121','1208':'1107096180','668':'1965421244','1313':'750679664','1129':'242474976'}
    STREET_C_NODE = {'430':'552910253','1035':'2078107280','412':'1329132133','1403':'922587542','1968':'339335164','1444':'1221389873','1183':'1812718902','1912':'132629780','1844':'438485374','1186':'1587992726','1222':'1984498433','1727':'1992232983','1522':'33713861','426':'739273303','1674':'1438865740'}
    STREET_D_NODE = {'1196':'962980710','1754':'204428608','903':'219544266','912':'1671735990','1526':'777635325','1555':'1565306616','1521':'599529154','1235':'359147515','1427':'1727952741','1406':'1209379174','543':'318561886','350':'1253207672','951':'146533149','933':'370917955','1991':'517408978','864':'1370973813','975':'1736491298','1588':'578187134','1961':'138700754','352':'1414647625','1646':'1391927494','895':'1669475776','918':'1875641892','1965':'237140292','618':'1388391521','1497':'219994425','817':'1487053959','1832':'2026478004','1417':'1101533292','797':'1581539848','926':'1267889618','1276':'1390598089','1948':'1680687005','1913':'1744161708','1600':'934618834','527':'1630634994','976':'1396918184','800':'207026272','1706':'65785292','195':'1605894428','512':'1184214677','875':'209359415','836':'1649709016','1000':'981914693','1830':'421101832','1060':'878273679','927':'1326247643'}


    # bar graph
    # tp = {}
    # left = ["interjunction","street"]
    for i in range(0,1):
        #sps
        s = "./results/pro1.1_smooth2_rri100.csv"
        marginX = 0
        marginY=0
        # 位置情報をnodeIDごとにまとめる
        # with open(s) as f:
        #     reader = csv.reader(f)
        #     posX_mean = 'posX:vector'
        #     for row in  reader:
        #         if row[1] == 'vector'and row[3] == posX_mean:
        #             nodeStr = re.split("[\[\]]",row[2])
        #             # print(nodeStr)
        #             nodeID = int(nodeStr[1])
        #             posx = re.split(" ",row[8])
        #             node_pos[nodeID] = []
        #             # print(posx)
        #             for x  in posx:
        #                 node_pos[nodeID].append([float(x),0.0])
        # # print(node_pos)   
        # with open(s) as f:
        #     reader = csv.reader(f)
        #     posY_mean = 'posY:vector'
        #     for row in  reader:
        #         if row[1] == 'vector'and row[3] == posY_mean:
        #             nodeStr = re.split("[\[\]]",row[2])
        #             nodeID = int(nodeStr[1])
        #             posy = re.split(" ",row[8])
        #             # print(posy)
        #             for i in range(0,len(posy)):
        #                 node_pos[nodeID][i][1]= float(posy[i])
        # # 交差点か直線道路に所属しているかどうかを判断し、分類。重複の場合、両方に分類
        # for id in node_pos.keys():
        #     isIncludeI = False
        #     isIncludeS = False
        #     isIncludeI2 = False
        #     isIncludeS2 = False
        #     for i in range(0,len(node_pos[id])):
        #         if node_pos[id][i][0] >= interjunction_pos[0]-marginX and node_pos[id][i][1] >= interjunction_pos[2]-marginY and node_pos[id][i][0] <= interjunction_pos[1]+marginX and node_pos[id][i][1] <= interjunction_pos[3]+marginY:
        #             isIncludeI=True
        #         if isIncludeI:
        #             interjunction_node.append(id)
        #             break
        #     for i in range(0,len(node_pos[id])):
        #         if  node_pos[id][i][0] >= street_pos[0]-marginX and node_pos[id][i][1] >= street_pos[2]-marginY and node_pos[id][i][0] <= street_pos[1]+marginX and node_pos[id][i][1] <= street_pos[3]+marginY:
        #             isIncludeS=True
        #         if isIncludeS:
        #             street_node.append(id)
        #             break
        #     for i in range(0,len(node_pos[id])):
        #         if node_pos[id][i][0] >= interjunction2_pos[0]-marginX and node_pos[id][i][1] >= interjunction2_pos[2]-marginY and node_pos[id][i][0] <= interjunction2_pos[1]+marginX and node_pos[id][i][1] <= interjunction2_pos[3]+marginY:
        #             isIncludeI2=True
        #         if isIncludeI2:
        #             interjunction2_node.append(id)
        #             break
        #     for i in range(0,len(node_pos[id])):
        #         if  node_pos[id][i][0] >= street2_pos[0]-marginX and node_pos[id][i][1] >= street2_pos[2]-marginY and node_pos[id][i][0] <= street2_pos[1]+marginX and node_pos[id][i][1] <= street2_pos[3]+marginY:
        #             isIncludeS2=True
        #         if isIncludeS2:
        #             street2_node.append(id)
        #             break
        interjunction_node = INTERSECTION_A_NODE.keys()
        interjunction2_node = INTERSECTION_B_NODE.keys()
        street_node = STREET_C_NODE.keys()
        street2_node = STREET_D_NODE.keys()


        # print(interjunction_node)
        # print(street_node) 
        # print(interjunction2_node)
        # print(street2_node)
        df = pd.read_csv(s, converters = {
        'attrvalue': parse_if_number,
        'binedges': parse_ndarray,
        'binvalues': parse_ndarray,
        'vectime': parse_ndarray,
        'vecvalue': parse_ndarray})
        pdr_vector = 'tbDecoded:vector'
        l = "PDR"
        yl="Packet Delivery Ratio %"
        pdr_dist_vector = 'txRxDistanceTB:vector'

        node_label_i = []
        node_label_s = []
        node_label_i2 = []
        node_label_s2 = []
        for node in interjunction_node:
            node_label_i.append("Mode4World.node["+str(node)+"].lteNic.phy")

        for node in street_node:
            node_label_s.append("Mode4World.node["+str(node)+"].lteNic.phy")
        
        for node in interjunction2_node:
            node_label_i2.append("Mode4World.node["+str(node)+"].lteNic.phy")

        for node in street2_node:
            node_label_s2.append("Mode4World.node["+str(node)+"].lteNic.phy")

        df_i  = df.query('module in @node_label_i')
        df_s = df.query("module in @node_label_s")
        distances = df_i[(df_i["name"] == pdr_dist_vector) & (df_i["vectime"].notnull())]
        decoded = df_i[(df_i["name"] == pdr_vector) & (df_i["vectime"].notnull())]
        distances = distances[["module", "vecvalue"]]
        distances.rename(columns={"vecvalue": "distance"}, inplace=True)
        decoded = decoded[["module", "vecvalue"]]
        decoded.rename(columns={"vecvalue": "decode"}, inplace=True)
        new_df = pd.merge(distances, decoded, on='module', how='inner')
        
        distances2 = df_s[(df_s["name"] == pdr_dist_vector) & (df_s["vectime"].notnull())]
        decoded2 = df_s[(df_s["name"] == pdr_vector) & (df_s["vectime"].notnull())]
        distances2 = distances2[["module", "vecvalue"]]
        distances2.rename(columns={"vecvalue": "distance"}, inplace=True)
        decoded2 = decoded2[["module", "vecvalue"]]
        decoded2.rename(columns={"vecvalue": "decode"}, inplace=True)
        new_df2 = pd.merge(distances2, decoded2, on='module', how='inner')
        
        
        
        
        df_i2  = df.query('module in @node_label_i2')
        df_s2 = df.query("module in @node_label_s2")
        distancesI2 = df_i2[(df_i2["name"] == pdr_dist_vector) & (df_i2["vectime"].notnull())]
        decodedI2 = df_i2[(df_i2["name"] == pdr_vector) & (df_i2["vectime"].notnull())]
        distancesI2 = distancesI2[["module", "vecvalue"]]
        distancesI2.rename(columns={"vecvalue": "distance"}, inplace=True)
        decodedI2 = decodedI2[["module", "vecvalue"]]
        decodedI2.rename(columns={"vecvalue": "decode"}, inplace=True)
        new_dfI2 = pd.merge(distancesI2, decodedI2, on='module', how='inner')
        
        distancesS2 = df_s2[(df_s2["name"] == pdr_dist_vector) & (df_s2["vectime"].notnull())]
        decodedS2 = df_s2[(df_s2["name"] == pdr_vector) & (df_s2["vectime"].notnull())]
        distancesS2 = distancesS2[["module", "vecvalue"]]
        distancesS2.rename(columns={"vecvalue": "distance"}, inplace=True)
        decodedS2 = decodedS2[["module", "vecvalue"]]
        decodedS2.rename(columns={"vecvalue": "decode"}, inplace=True)
        new_dfS2 = pd.merge(distancesS2, decodedS2, on='module', how='inner')
        
        count_i = 0
        count_s = 0
        success_i = 0
        success_s = 0
        bins_i = []
        bins_s=[]

        count_i2 = 0
        count_s2 = 0
        success_i2 = 0
        success_s2 = 0
        bins_i2 = []
        bins_s2=[]

        for i in range(80):
            bins_i.append({"count": 0, "success": 0})
            bins_s.append({"count": 0, "success": 0})
            bins_i2.append({"count": 0, "success": 0})
            bins_s2.append({"count": 0, "success": 0})

        for row in new_df.itertuples():
            for i in range(len(row.distance)):
                if row.distance[i] < 800:
                    # Ensures that we have everything in 10m chunks
                    remainder = int(row.distance[i] // 10)
                    if row.decode[i] >= 0:
                        # Only count TBs sent i.e. -1 will be ignored in result
                        count_i+= 1
                        success_i += row.decode[i]
                        bins_i[remainder]["count"] +=1
                        bins_i[remainder]["success"] += row.decode[i]
        
        for row in new_df2.itertuples():
            for i in range(len(row.distance)):
                if row.distance[i] < 800:
                    # Ensures that we have everything in 10m chunks
                    remainder = int(row.distance[i] // 10)
                    if row.decode[i] >= 0:
                        # Only count TBs sent i.e. -1 will be ignored in result
                        count_s+= 1
                        success_s += row.decode[i]
                        bins_s[remainder]["count"] +=1
                        bins_s[remainder]["success"] += row.decode[i]
        for row in new_dfI2.itertuples():
            for i in range(len(row.distance)):
                if row.distance[i] < 800:
                    # Ensures that we have everything in 10m chunks
                    remainder = int(row.distance[i] // 10)
                    if row.decode[i] >= 0:
                        # Only count TBs sent i.e. -1 will be ignored in result
                        count_i2+= 1
                        success_i2 += row.decode[i]
                        bins_i2[remainder]["count"] +=1
                        bins_i2[remainder]["success"] += row.decode[i]
        
        for row in new_dfS2.itertuples():
            for i in range(len(row.distance)):
                if row.distance[i] < 800:
                    # Ensures that we have everything in 10m chunks
                    remainder = int(row.distance[i] // 10)
                    if row.decode[i] >= 0:
                        # Only count TBs sent i.e. -1 will be ignored in result
                        count_s2+= 1
                        success_s2 += row.decode[i]
                        bins_s2[remainder]["count"] +=1
                        bins_s2[remainder]["success"] += row.decode[i]
        print("count_i:" + str(count_i) + ", rate:" + str(success_i/count_i*100))
        print("count_s:" + str(count_s) + ", rate:" + str(success_s/count_s*100.0))
        print("count_i2:" + str(count_i2) + ", rate:" + str(success_i2/count_i2*100))
        print("count_s2:" + str(count_s2) + ", rate:" + str(success_s2/count_s2*100.0))

        pdrs_i = []
        distances_i = []
        distance_i = 0
        for dictionary in bins_i:
            pdrs_i.append((dictionary["success"] / dictionary["count"] * 100))
            distances_i.append(distance_i)
            distance_i += 10        
        pdrs_s = []
        distances_s = []
        distance_s = 0
        for dictionary in bins_s:
            pdrs_s.append((dictionary["success"] / dictionary["count"] * 100))
            distances_s.append(distance_s)
            distance_s += 10
        
        pdrs_i2 = []
        for dictionary in bins_i2:
            pdrs_i2.append((dictionary["success"] / dictionary["count"] * 100))

        pdrs_s2 = []
        for dictionary in bins_s2:
            pdrs_s2.append((dictionary["success"] / dictionary["count"] * 100))
            
        
        #ds
        s = "./results/sps_smooth2_rri100.csv"
        marginX = 0
        marginY=0
        node_pos={}
        interjunction_node=[]
        street_node=[]
        interjunction2_node=[]
        street2_node=[]
        # with open(s) as f:
        #     reader = csv.reader(f)
        #     posX_mean = 'posX:vector'
        #     for row in  reader:
        #         if row[1] == 'vector'and row[3] == posX_mean:
        #             nodeStr = re.split("[\[\]]",row[2])
        #             # print(nodeStr)
        #             nodeID = int(nodeStr[1])
        #             posx = re.split(" ",row[8])
        #             node_pos[nodeID] = []
        #             # print(posx)
        #             for x  in posx:
        #                 node_pos[nodeID].append([float(x),0.0])
                    
        # # print(node_pos)   
        # with open(s) as f:
        #     reader = csv.reader(f)
        #     posY_mean = 'posY:vector'
        #     for row in  reader:
        #         if row[1] == 'vector'and row[3] == posY_mean:
        #             nodeStr = re.split("[\[\]]",row[2])
        #             nodeID = int(nodeStr[1])
        #             posy = re.split(" ",row[8])
        #             # print(posy)
        #             for i in range(0,len(posy)):
        #                 node_pos[nodeID][i][1]= float(posy[i])
                    
        # # print(len(node_pos))
        # # print(node_pos[0])  
        # for id in node_pos.keys():
        #     isIncludeI = False
        #     isIncludeS = False
        #     isIncludeI2 = False
        #     isIncludeS2 = False
        #     for i in range(0,len(node_pos[id])):
        #         if node_pos[id][i][0] >= interjunction_pos[0]-marginX and node_pos[id][i][1] >= interjunction_pos[2]-marginY and node_pos[id][i][0] <= interjunction_pos[1]+marginX and node_pos[id][i][1] <= interjunction_pos[3]+marginY:
        #             isIncludeI=True
        #         if isIncludeI:
        #             interjunction_node.append(id)
        #             break
        #     for i in range(0,len(node_pos[id])):
        #         if  node_pos[id][i][0] >= street_pos[0]-marginX and node_pos[id][i][1] >= street_pos[2]-marginY and node_pos[id][i][0] <= street_pos[1]+marginX and node_pos[id][i][1] <= street_pos[3]+marginY:
        #             isIncludeS=True
        #         if isIncludeS:
        #             street_node.append(id)
        #             break
        #     for i in range(0,len(node_pos[id])):
        #         if node_pos[id][i][0] >= interjunction2_pos[0]-marginX and node_pos[id][i][1] >= interjunction2_pos[2]-marginY and node_pos[id][i][0] <= interjunction2_pos[1]+marginX and node_pos[id][i][1] <= interjunction2_pos[3]+marginY:
        #             isIncludeI2=True
        #         if isIncludeI2:
        #             interjunction2_node.append(id)
        #             break
        #     for i in range(0,len(node_pos[id])):
        #         if  node_pos[id][i][0] >= street2_pos[0]-marginX and node_pos[id][i][1] >= street2_pos[2]-marginY and node_pos[id][i][0] <= street2_pos[1]+marginX and node_pos[id][i][1] <= street2_pos[3]+marginY:
        #             isIncludeS2=True
        #         if isIncludeS2:
        #             street2_node.append(id)
        #             break
        interjunction_node = INTERSECTION_A_NODE.keys()
        interjunction2_node = INTERSECTION_B_NODE.keys()
        street_node = STREET_C_NODE.keys()
        street2_node = STREET_D_NODE.keys()

        # print(interjunction_node)
        # print(street_node)
        # print(interjunction2_node)
        # print(street2_node)
        df = pd.read_csv(s, converters = {
        'attrvalue': parse_if_number,
        'binedges': parse_ndarray,
        'binvalues': parse_ndarray,
        'vectime': parse_ndarray,
        'vecvalue': parse_ndarray})
        pdr_vector = 'tbDecoded:vector'
        l = "PDR"
        yl="Packet Delivery Ratio %"
        pdr_dist_vector = 'txRxDistanceTB:vector'

        node_label_i = []
        node_label_s = []
        node_label_i2 = []
        node_label_s2 = []
        for node in interjunction_node:
            node_label_i.append("Mode4World.node["+str(node)+"].lteNic.phy")

        for node in street_node:
            node_label_s.append("Mode4World.node["+str(node)+"].lteNic.phy")
        
        for node in interjunction2_node:
            node_label_i2.append("Mode4World.node["+str(node)+"].lteNic.phy")

        for node in street2_node:
            node_label_s2.append("Mode4World.node["+str(node)+"].lteNic.phy")

        df_i  = df.query('module in @node_label_i')
        df_s = df.query("module in @node_label_s")
        distances = df_i[(df_i["name"] == pdr_dist_vector) & (df_i["vectime"].notnull())]
        decoded = df_i[(df_i["name"] == pdr_vector) & (df_i["vectime"].notnull())]
        distances = distances[["module", "vecvalue"]]
        distances.rename(columns={"vecvalue": "distance"}, inplace=True)
        decoded = decoded[["module", "vecvalue"]]
        decoded.rename(columns={"vecvalue": "decode"}, inplace=True)
        new_df = pd.merge(distances, decoded, on='module', how='inner')
        
        distances2 = df_s[(df_s["name"] == pdr_dist_vector) & (df_s["vectime"].notnull())]
        decoded2 = df_s[(df_s["name"] == pdr_vector) & (df_s["vectime"].notnull())]
        distances2 = distances2[["module", "vecvalue"]]
        distances2.rename(columns={"vecvalue": "distance"}, inplace=True)
        decoded2 = decoded2[["module", "vecvalue"]]
        decoded2.rename(columns={"vecvalue": "decode"}, inplace=True)
        new_df2 = pd.merge(distances2, decoded2, on='module', how='inner')
        
        
        df_i2  = df.query('module in @node_label_i2')
        df_s2 = df.query("module in @node_label_s2")
        distancesI2 = df_i2[(df_i2["name"] == pdr_dist_vector) & (df_i2["vectime"].notnull())]
        decodedI2 = df_i2[(df_i2["name"] == pdr_vector) & (df_i2["vectime"].notnull())]
        distancesI2 = distancesI2[["module", "vecvalue"]]
        distancesI2.rename(columns={"vecvalue": "distance"}, inplace=True)
        decodedI2 = decodedI2[["module", "vecvalue"]]
        decodedI2.rename(columns={"vecvalue": "decode"}, inplace=True)
        new_dfI2 = pd.merge(distancesI2, decodedI2, on='module', how='inner')
        
        distancesS2 = df_s2[(df_s2["name"] == pdr_dist_vector) & (df_s2["vectime"].notnull())]
        decodedS2 = df_s2[(df_s2["name"] == pdr_vector) & (df_s2["vectime"].notnull())]
        distancesS2 = distancesS2[["module", "vecvalue"]]
        distancesS2.rename(columns={"vecvalue": "distance"}, inplace=True)
        decodedS2 = decodedS2[["module", "vecvalue"]]
        decodedS2.rename(columns={"vecvalue": "decode"}, inplace=True)
        new_dfS2 = pd.merge(distancesS2, decodedS2, on='module', how='inner')
        
        count_i = 0
        count_s = 0
        success_i = 0
        success_s = 0
        bins_i = []
        bins_s=[]
        
        count_i2 = 0
        count_s2 = 0
        success_i2 = 0
        success_s2 = 0
        bins_i2 = []
        bins_s2=[]

        for i in range(80):
            bins_i.append({"count": 0, "success": 0})
            bins_s.append({"count": 0, "success": 0})
            bins_i2.append({"count": 0, "success": 0})
            bins_s2.append({"count": 0, "success": 0})

        for row in new_df.itertuples():
            for i in range(len(row.distance)):
                if row.distance[i] < 800:
                    # Ensures that we have everything in 10m chunks
                    remainder = int(row.distance[i] // 10)
                    if row.decode[i] >= 0:
                        # Only count TBs sent i.e. -1 will be ignored in result
                        count_i+= 1
                        success_i += row.decode[i]
                        bins_i[remainder]["count"] +=1
                        bins_i[remainder]["success"] += row.decode[i]
        
        for row in new_df2.itertuples():
            for i in range(len(row.distance)):
                if row.distance[i] < 800:
                    # Ensures that we have everything in 10m chunks
                    remainder = int(row.distance[i] // 10)
                    if row.decode[i] >= 0:
                        # Only count TBs sent i.e. -1 will be ignored in result
                        count_s+= 1
                        success_s += row.decode[i]
                        bins_s[remainder]["count"] +=1
                        bins_s[remainder]["success"] += row.decode[i]
        for row in new_dfI2.itertuples():
            for i in range(len(row.distance)):
                if row.distance[i] < 800:
                    # Ensures that we have everything in 10m chunks
                    remainder = int(row.distance[i] // 10)
                    if row.decode[i] >= 0:
                        # Only count TBs sent i.e. -1 will be ignored in result
                        count_i2+= 1
                        success_i2 += row.decode[i]
                        bins_i2[remainder]["count"] +=1
                        bins_i2[remainder]["success"] += row.decode[i]
        
        for row in new_dfS2.itertuples():
            for i in range(len(row.distance)):
                if row.distance[i] < 800:
                    # Ensures that we have everything in 10m chunks
                    remainder = int(row.distance[i] // 10)
                    if row.decode[i] >= 0:
                        # Only count TBs sent i.e. -1 will be ignored in result
                        count_s2+= 1
                        success_s2 += row.decode[i]
                        bins_s2[remainder]["count"] +=1
                        bins_s2[remainder]["success"] += row.decode[i]
        print("count_i:" + str(count_i) + ", rate:" + str(success_i/count_i*100.0))
        print("count_s:" + str(count_s) + ", rate:" + str(success_s/count_s*100.0))
        print("count_i2:" + str(count_i2) + ", rate:" + str(success_i2/count_i2*100.0))
        print("count_s2:" + str(count_s2) + ", rate:" + str(success_s2/count_s2*100.0))

        pdrs2_i = []
        distances = []
        distance = 0
        for dictionary in bins_i:
            pdrs2_i.append((dictionary["success"] / dictionary["count"] * 100))
            distances.append(distance)
            distance += 10
        pdrs2_s = []
        for dictionary in bins_s:
            pdrs2_s.append((dictionary["success"] / dictionary["count"] * 100))
        pdrs2_i2 = []
        for dictionary in bins_i2:
            pdrs2_i2.append((dictionary["success"] / dictionary["count"] * 100))
        pdrs2_s2 = []
        for dictionary in bins_s2:
            pdrs2_s2.append((dictionary["success"] / dictionary["count"] * 100))
          
            
        
        fig, ax = plt.subplots()
        

        ax.plot(distances, pdrs_i, label="proposal,intersection a", color="blue")
        ax.plot(distances, pdrs_i2, label="proposal,intersection b",color="green")
        ax.plot(distances, pdrs_s, label="proposal,street c",color="orange")
        ax.plot(distances, pdrs_s2, label="proposal,street d",color="red")
        ax.plot(distances, pdrs2_i,":", label="sps,intersection a",color="blue")
        ax.plot(distances, pdrs2_i2,":", label="sps,intersection b",color="green")
        ax.plot(distances, pdrs2_s,":", label="sps,street c",color="orange")
        ax.plot(distances, pdrs2_s2,":", label="sps,street d",color="red")
        



        ax.set(xlabel='Distance (m)', ylabel=yl)
        ax.legend(loc="lower left")
        ax.tick_params(direction='in')
        ax.set_xlim([0, (max(distances) + 1)])
        # ax.set_ylim([0, 101])
        plt.xticks(np.arange(0, (max(distances))+50, step=50))
        plt.yticks(np.arange(0, (101), step=10))



        plt.savefig(mode+"_"+option, dpi=300)


if mode == "posResourceMap":
    node_pos = {}
    interjunction_pdr={}
    interjunction_dist={}
    interjunction_node=[]
    interjunction_pos=[9475.0,9615.0,13985.0,14125.0] #left up,left down, right up, right down
    street_pdr={}
    street_dist={}
    street_node=[]
    street_pos=[9670.0,10270.0,14670.0,14750.0] #left up,left down, right up, right down
    fig, ax = plt.subplots()
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, fontsize=9)
    # bar graph
    tp = {}
    left = ["interjunction","street"]
    for i in range(0,1):
        #sps
        s = "./results/sps-high.csv"
        marginX = 500
        marginY=500
        with open(s) as f:
            reader = csv.reader(f)
            posX_mean = 'posX:vector'
            for row in  reader:
                if row[1] == 'vector'and row[3] == posX_mean:
                    nodeStr = re.split("[\[\]]",row[2])
                    # print(nodeStr)
                    nodeID = int(nodeStr[1])
                    posx = re.split(" ",row[8])
                    node_pos[nodeID] = []
                    # print(posx)
                    for x  in posx:
                        node_pos[nodeID].append([float(x),0.0])
                    # for x in posx:
                    #     if float(x) >= interjunction_pos[0]-marginX and float(x) <= interjunction_pos[1]+marginX  :
                    #         interjunction_node.append(nodeID)
                    #         break
                    #     elif float(x) >= street_pos[0]-marginX and float(x) <= street_pos[1]+marginX :
                    #         street_node.append(nodeID)
                    #         break
        # print(node_pos)   
        with open(s) as f:
            reader = csv.reader(f)
            posY_mean = 'posY:vector'
            for row in  reader:
                if row[1] == 'vector'and row[3] == posY_mean:
                    nodeStr = re.split("[\[\]]",row[2])
                    nodeID = int(nodeStr[1])
                    posy = re.split(" ",row[8])
                    print(posy)
                    for i in range(0,len(posy)):
                        node_pos[nodeID][i][1]= float(posy[i])
                    # for y in posy:
                    #     if nodeID in interjunction_node:    
                    #         if not (float(y) >= interjunction_pos[2]-marginY and float(y) <= interjunction_pos[3]+marginY) :
                    #             interjunction_node.remove(nodeID)
                    #     elif nodeID in street_node:
                    #         if not (float(y) >= street_pos[2]-marginY and float(y) <= street_pos[3]+marginY) :
                    #             street_node.remove(nodeID)
            
        # print(len(node_pos))
        # print(node_pos[0])  
        for id in node_pos.keys():
            isIncludeI = False
            isIncludeS = False
            for i in range(0,len(node_pos[id])):
                if node_pos[id][i][0] >= interjunction_pos[0]-marginX and node_pos[id][i][1] >= interjunction_pos[3]-marginY and node_pos[id][i][0] <= interjunction_pos[1]+marginX and node_pos[id][i][1] <= interjunction_pos[2]+marginY:
                    isIncludeI=True
                elif  node_pos[id][i][0] >= street_pos[0]-marginX and node_pos[id][i][1] >= street_pos[3]-marginY and node_pos[id][i][0] <= street_pos[1]+marginX and node_pos[id][i][1] <= street_pos[2]+marginY:
                    isIncludeS=True
                if isIncludeI:
                    interjunction_node.append(id)
                    break
                if isIncludeS:
                    street_node.append(id)
                    break
        s = "data/resourcesAllocation_sps2.csv" 
        subchannels_i=[]
        subchannels_s=[]
        with open(s) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] in interjunction_node:
                    data=[]
                    data.append(row[1])
                    array = row[2].split(' ') + row[3].split(' ')
                    data.append(array)
                    regist_subchannels(data,subchannels_i)
                if row[0] in street_node:
                    data=[]
                    data.append(row[1])
                    array = row[2].split(' ') + row[3].split(' ')
                    data.append(array)
                    regist_subchannels(data,subchannels_s)
        numGen=len(subchannels_i)
        numCollision=count_overlap(subchannels_i)
        
        print("sps")
        print("intersection")
        # print(subchannels)
        print("numCollision:"+str(numCollision))
        print("numGen:"+str(numGen))
        print("collision rate:"+str(numCollision/numGen*1.0))
        numGen=len(subchannels_s)
        numCollision=count_overlap(subchannels_s)
        
        print("street")
        # print(subchannels)
        print("numCollision:"+str(numCollision))
        print("numGen:"+str(numGen))
        print("collision rate:"+str(numCollision/numGen*1.0))
        
        
    for i in range(0,1):
        #ds
        s = "./results/ds_high.csv"
        marginX = 500
        marginY=500
        with open(s) as f:
            reader = csv.reader(f)
            posX_mean = 'posX:vector'
            for row in  reader:
                if row[1] == 'vector'and row[3] == posX_mean:
                    nodeStr = re.split("[\[\]]",row[2])
                    # print(nodeStr)
                    nodeID = int(nodeStr[1])
                    posx = re.split(" ",row[8])
                    node_pos[nodeID] = []
                    # print(posx)
                    for x  in posx:
                        node_pos[nodeID].append([float(x),0.0])
                    # for x in posx:
                    #     if float(x) >= interjunction_pos[0]-marginX and float(x) <= interjunction_pos[1]+marginX  :
                    #         interjunction_node.append(nodeID)
                    #         break
                    #     elif float(x) >= street_pos[0]-marginX and float(x) <= street_pos[1]+marginX :
                    #         street_node.append(nodeID)
                    #         break
        # print(node_pos)   
        with open(s) as f:
            reader = csv.reader(f)
            posY_mean = 'posY:vector'
            for row in  reader:
                if row[1] == 'vector'and row[3] == posY_mean:
                    nodeStr = re.split("[\[\]]",row[2])
                    nodeID = int(nodeStr[1])
                    posy = re.split(" ",row[8])
                    # print(posy)
                    for i in range(0,len(posy)):
                        node_pos[nodeID][i][1]= float(posy[i])
                    # for y in posy:
                    #     if nodeID in interjunction_node:    
                    #         if not (float(y) >= interjunction_pos[2]-marginY and float(y) <= interjunction_pos[3]+marginY) :
                    #             interjunction_node.remove(nodeID)
                    #     elif nodeID in street_node:
                    #         if not (float(y) >= street_pos[2]-marginY and float(y) <= street_pos[3]+marginY) :
                    #             street_node.remove(nodeID)
                
        # print(len(node_pos))
        # print(node_pos[0])  
        for id in node_pos.keys():
            isIncludeI = False
            isIncludeS = False
            for i in range(0,len(node_pos[id])):
                if node_pos[id][i][0] >= interjunction_pos[0]-marginX and node_pos[id][i][1] >= interjunction_pos[3]-marginY and node_pos[id][i][0] <= interjunction_pos[1]+marginX and node_pos[id][i][1] <= interjunction_pos[2]+marginY:
                    isIncludeI=True
                elif  node_pos[id][i][0] >= street_pos[0]-marginX and node_pos[id][i][1] >= street_pos[3]-marginY and node_pos[id][i][0] <= street_pos[1]+marginX and node_pos[id][i][1] <= street_pos[2]+marginY:
                    isIncludeS=True
                if isIncludeI:
                    interjunction_node.append(id)
                    break
                if isIncludeS:
                    street_node.append(id)
                    break
        s = "data/resourcesAllocation_ds2.csv" 
        subchannels_i=[]
        subchannels_s=[]
        with open(s) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] in interjunction_node:
                    data=[]
                    data.append(row[1])
                    array = row[2].split(' ') + row[3].split(' ')
                    data.append(array)
                    regist_subchannels(data,subchannels_i)
                if row[0] in street_node:
                    data=[]
                    data.append(row[1])
                    array = row[2].split(' ') + row[3].split(' ')
                    data.append(array)
                    regist_subchannels(data,subchannels_s)
        numGen=len(subchannels_i)
        numCollision=count_overlap(subchannels_i)
        
        print("ds")
        print("intersection")
        print("numCollision:"+str(numCollision))
        print("numGen:"+str(numGen))
        print("collision rate:"+str(numCollision/numGen*1.0))
        numGen=len(subchannels_s)
        numCollision=count_overlap(subchannels_s)
        
        print("street")
        print("numCollision:"+str(numCollision))
        print("numGen:"+str(numGen))
        print("collision rate:"+str(numCollision/numGen*1.0))

        