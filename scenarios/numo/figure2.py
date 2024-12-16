import sys
import csv
import pprint
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import math

OVER_SIZE_LIMIT = 200_000_000

VEHICLE_DATA = {
250493:[1268632557, 1940],
266134:[1212534319, 2287],
269288:[506959639, 2388],
270927:[76810012, 2442],
273261:[159999213, 2487],
278171:[903633726, 2638],
280942:[783175739, 2700],
224968:[1204868098, 1496],
232596:[1967632854, 1649],
236142:[1594769883, 1690],
241865:[366831742, 1785],
244755:[1041356631, 1839],
252205:[2057337242, 1966],
258230:[1943679781, 2106],
258547:[278608944, 2116],
259677:[71185160, 2139],
260595:[1480708313, 2156],
261664:[596727699, 2176],
262434:[353511414, 2192],
262795:[1211270210, 2198],
264411:[568637651, 2244],
266291:[1401943880, 2290],
268286:[1622838287, 2354],
269573:[431315644, 2399],
269612:[1178835412, 2401],
270878:[1259480129, 2440],
270929:[2047140186, 2443],
272766:[1138259617, 2479],
272936:[1469543483, 2481],
273027:[545343058, 2482],
274079:[486006071, 2508],
278859:[969069027, 2649],
279073:[739068399, 2655],
213042:[257675105, 665],
230094:[575705360, 1618],
235209:[1999337836, 1679],
236281:[209473567, 1692],
238094:[1374631287, 1726],
238515:[1953534826, 1730],
239471:[1183912267, 1746],
241224:[1815983044, 1773],
242455:[1064651899, 1792],
242705:[429363923, 1800],
248901:[1166437685, 1909],
249833:[859310840, 1929],
250492:[916768482, 1939],
254508:[427778693, 2018],
256852:[2123987799, 2076],
257179:[1072190528, 2083],
257408:[954296984, 2090],
258461:[26416758, 2114],
258911:[1656951142, 2124],
259073:[1069774565, 2127],
262590:[320062251, 2196],
263254:[1110980456, 2212],
264905:[189409560, 2259],
266999:[127340947, 2314],
267014:[1554430207, 2315],
268354:[1617869388, 2355],
268419:[1927454328, 2356],
268631:[2095802345, 2363],
270705:[1943410399, 2434],
271784:[891528784, 2459],
272045:[158535326, 2463],
276084:[1609446676, 2572],
281101:[73831160, 2707],
281397:[1863967037, 2715],
285115:[147775927, ],
222407:[1531585205, 1278],
227837:[62299853, 1591],
239013:[258219170, 1737],
251330:[106242869, 1953],
257824:[1654435776, 2094],
263810:[981512505, 2226],
265442:[560413640, 2270],
268859:[2016747294, 2372],
270367:[682900658, 2421],
215182:[1520982030, 775],
219496:[1931706506, 1051],
224432:[928682751, 1450],
234779:[340563072, 1672],
252777:[1602182790, 1976],
263831:[1836997946, 2227],
264173:[363159161, 2236],
268948:[1578037126, 2378],
277043:[589130772, 2603],
234950:[1776088411, 1675],
234968:[217852623, 1676],
251313:[1454580282, 1951],
253904:[184794536, 2000]
}

csv.field_size_limit(OVER_SIZE_LIMIT)

args = sys.argv
mode = ""
option=""

if len(args)>=3:
    option=args[2]
if len(args)>=2 :
    mode=args[1]

def id_match(target_name,s):
    target_id = 0
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[3] == target_name:
                target_id = row[1]
                break
    return target_id


#一台ごとの車の軌跡
if mode in {"vehicle_trajectory", "vehicle_pos", "vehicle_pos3D"}:
    #入力：camTimeStamp.csvのrow[3], row[4], row[0], posx, posy
    #出力：分類[上下左右から右折、左折、直進、停止]
    interjunction_pos=[9475.0,9615.0,13985.0,14125.0] #left up,left down, right up, right down
    street_pos=[9670.0,10270.0,14670.0,14750.0] #left up,left down, right up, right down
    target_name = "1"
    
    if len(args)>= 4:
        target_name = args[3]
    s = "./data/camTimeStamp_sps2_2.csv"
    s2 = "./data/stationIdList_sps2_2.csv"
    timeStamp = []
    count = 0
    y_count = []
    target_id = id_match(target_name,s2)
    print(target_name)
    print(target_id)
    poses_x = []
    poses_y=[]
    first_pos = [0.0,0.0]
    isFirst = True
    velocity = []
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == target_id:
                y_count.append(count)
                count += 1
                timeStamp.append(float(row[0]))
                if isFirst:
                    isFirst = False
                    poses_x.append(0.0)
                    poses_y.append(0.0)
                    first_pos = [float(row[3]),float(row[4])]
                else:
                    poses_x.append(float(row[3])-first_pos[0])
                    poses_y.append(float(row[4])-first_pos[1])
                velocity.append(float(row[6])*3600/1000)
                
    # print(timeStamp)
    y_time = []      
    post_timeStamp=0.0
    
    isFirst = True

    for i in range(len(timeStamp)):
        if isFirst:
            # y_time.append(0.0)
            isFirst=False
        else:
            y_time.append(timeStamp[i]-post_timeStamp)
            # x_v=(poses_x[i]-poses_x[i-1])/(timeStamp[i]-post_timeStamp)
            # y_v=(poses_y[i]-poses_y[i-1])/(timeStamp[i]-post_timeStamp)
            # velocity.append(math.sqrt(x_v**2 + y_v**2))
        
        post_timeStamp = timeStamp[i]
        
    # print(y_count)

    s = "./data/headingDelta_sps2_2.csv" #Red
    s1 = "./data/positionDelta_sps2_2.csv" #Blue
    s2 = "./data/speedDelta_sps2_2.csv" #Green

    triggers = {}

    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == target_id:
                triggers[float(row[0])] = "r"
    with open(s1) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == target_id:
                triggers[float(row[0])] = "b"
    with open(s2) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == target_id:
                triggers[float(row[0])] = "g"
    # print(triggers)
    colors = []
    for t in timeStamp:
        if t in triggers.keys():
            colors.append(triggers[t])
        else:
            colors.append("k")

    fig = plt.figure()
    if mode == "vehicle_trajectory":
        
        # cam log
        ax = fig.add_subplot(111)
        ax.set_ylim(0,1.0)
        ax.plot(timeStamp[1:],y_time,zorder=0)
        ax.scatter(timeStamp[1:],y_time,s=50,c=colors[1:],zorder=1,marker="^")
        ax.grid(axis="y")
        ax.set_xlabel("time[s]")
        ax.set_ylabel("interval[s]")
        
        ax2 = ax.twinx()
        ax2.plot(timeStamp[1:],velocity[1:],"o-",c="orange")
        ax2.set_ylabel("speed")
        ax2.set_ylim(0,120)
        # 凡例用に空のデータをlabel付でプロットする（実際はなにもプロットしてない）
        plt.scatter([], [], c="r", s=50, marker="^",label="head")
        plt.scatter([], [], c="b", s=50, marker="^",label="position")
        plt.scatter([], [], c="g", s=50, marker="^",label="speed")
        plt.scatter([], [], c="k", s=50, marker="^",label="T_GenCam")
        plt.legend()
    elif mode == "vehicle_pos":
        # pos log
        # plt.ylim(400,-400)
        # plt.xlim(-400,400)
        plt.plot(poses_x,poses_y,"-^")
        plt.grid(axis="y")
        plt.grid(axis="x")

        plt.xlabel("x")
        plt.ylabel("y")
    elif mode == "vehicle_pos3D":
        # pos log
        ax = fig.add_subplot(projection='3d')
        # plt.ylim(400,-400)
        # plt.xlim(-400,400)
        ax.plot(poses_x,poses_y,timeStamp,"-^")
        plt.grid(axis="y")
        plt.grid(axis="x")

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("time [s]")

    if args[3] in ["250493","266134","269288","270927","273261","278171","280942"] :
        fig.savefig("./vehicleCamData/accel/"+mode+"_"+option)
    elif args[3] in ["224968","232596","236142","241865","244755","252205","258230","258547","259677","260595","261664","262434","262795","264411","266291","268286","269573","269612","270878","270929","272766","272936","273027","274079","278859","279073"]:
        fig.savefig("./vehicleCamData/brake/"+mode+"_"+option)
    elif args[3] in ["213042","230094","235209","236281","238094","238515","239471","241224","242455","242705","248901","249833","250492","254508","256852","257179","257408","258461","258911","259073","262590","263254","264905","266999","267014","268354","268419","268631","270705","271784","272045","276084","281101","281397","285115"]:
        fig.savefig("./vehicleCamData/direct/"+mode+"_"+option)
    elif args[3] in ["222407","227837","239013","251330","257824","263810","265442","268859","270367"]:
        fig.savefig("./vehicleCamData/left/"+mode+"_"+option)
    elif args[3] in ["215182","219496","224432","234779","252777","263831","264173","268948","277043"]:
        fig.savefig("./vehicleCamData/right/"+mode+"_"+option)
    else:
        fig.savefig("./vehicleCamData/"+mode+"_"+option)
    
    

def module_match(nodes,s_c,s_d,s_r):
    modules = []
    ids = {}
    node_pos ={}
    module_pos={}
    for n in nodes:
        ids[id_match(n,s_d)]=[n,""]
    # print(ids)
    # with open(s_c) as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         if float(row[0]) < 28800.0:
    #             continue
    #         if row[1] not in node_pos and row[1] in ids:
    #             node_pos[row[1]] = [float(row[3]),float(row[4])]
    print('1654435776' in ids)
    with open(s_r) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == 'vector'and row[3] == "camVehicleId:vector":
                id = re.split(" ",row[8])
                print(id[0])
                if id[0] in ids:
                    nodeStr = re.split("[\[\]]",row[2])
                    # print(nodeStr)
                    nodeID = nodeStr[1]
                    ids[id[0]][1] = nodeID

    # print(node_pos)
    # for m,p_m in module_pos.items():
    #     min_d = 10000
    #     target_node = ""
    #     for n,p_n in node_pos.items():
    #         d = math.sqrt((p_m[0]-p_n[0])**2 + (p_m[1]-p_n[1])**2)
    #         if min_d > d:
    #             min_d = d
    #             target_node = n
    #     if target_node == "":
    #         print(str(m))
    #     else:
    #         modules[m] = [ids[target_node],target_node,min_d]

    return ids
    
    
if mode == "module_match":
    nodes = ["250493","266134","269288","270927","273261","278171","280942","224968","232596","236142","241865","244755","252205","258230","258547","259677","260595","261664","262434","262795","264411","266291","268286","269573","269612","270878","270929","272766","272936","273027","274079","278859","279073","213042","230094","235209","236281","238094","238515","239471","241224","242455","242705","248901","249833","250492","254508","256852","257179","257408","258461","258911","259073","262590","263254","264905","266999","267014","268354","268419","268631","270705","271784","272045","276084","281101","281397","285115","222407","227837","239013","251330","257824","263810","265442","268859","270367","215182","219496","224432","234779","252777","263831","264173","268948","277043","234950","234968","251313","253904"]

    s_r = "./results/stationID.csv"
    s = "./data/camTimeStamp_ds2.csv"
    s2 = "./data/stationIdList_ds2.csv"
    # modules = module_match(nodes,s,s2,s_r)
    # print(modules)
    # print("len:"+str(len(modules)))
    ans=[]
    # for n in nodes:
        # print(str(n)+", "+str(id_match(n,s2)))
    modules = module_match(nodes,s,s2,s_r)
    for k in  modules.keys():
        print(modules[k][0]+":["+ k + ", " + modules[k][1]+"],")

if mode in ["pdr_speed_gb","delay_each_vehicle"]:
    s="./results/sps_1015.csv"
    s2 ="./results/ds_1015.csv"
    s_c = "./data/camTimeStamp_sps2_2.csv"
    s_id = "./data/stationIdList_sps2_2.csv"

    isDelay = (mode=="delay_each_vehicle") 
    if isDelay:
        s="./results/sps_1015_interPacketDelay.csv"
        s2="./results/ds_1015_interPacketDelay.csv"
    

    data=VEHICLE_DATA

    target_name= ""
    
    if len(args)>=4:
        target_name = args[3] 

    timeStamp_v=[]
    velocity =[]

    target_id = id_match(target_name,s_id)

    tp={}
    # velocity
    with open(s_c) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == target_id:
                if float(row[0]) >= 28800.0:
                    timeStamp_v.append(float(row[0])-28800.0)
                    velocity.append(float(row[6])*3600/1000)

    #pdr 累積グラフ　デコード数／総数
    node = data[int(target_name)][1]
    #sps
    pdr_devide=[0.0,0.0,0.0,0.0,0.0,0.0]
    timeStamp_pdr=["[0,5)","[5,10)","[10,15)","[15,20)","[20,25)","[25,30)",]
    with open(s) as f:
        reader = csv.reader(f)
        nameTarget="tbDecoded:vector"
        if isDelay: nameTarget="interPacketDelay:vector"
        for row in reader:

            if row[1] == "vector" and row[3] == nameTarget and row[2]=="Mode4World.node["+str(node)+"].lteNic.phy":
                ts = re.split(" ",row[7])
                pdrs = re.split(" ",row[8])
                decodes=[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
                for t_i in range(len(ts)):
                    index = int(int(float(ts[t_i])-28800.0)/5)
                    # print(index)
                    if index >= 6:
                        index = 5
                    decodes[index][0] += float(pdrs[t_i])
                    decodes[index][1] += 1
                for i in range(len(pdr_devide)):
                    if decodes[i][1] != 0:
                        pdr_devide[i]=decodes[i][0]/decodes[i][1]*1.0
                    else :
                        pdr_devide[i]=decodes[i][0]/1*1.0
    
    tp["sps"] = pdr_devide
    
    #ds
    pdr_devide2=[0.0,0.0,0.0,0.0,0.0,0.0]
    # timeStamp_pdr=["[0,5)","[5,10)","[10,15)","[15,20)","[20,25)","[25,30)",]
    with open(s) as f:
        reader = csv.reader(f)
        nameTarget="tbDecoded:vector"
        if isDelay: nameTarget="interPacketDelay:vector"
        for row in reader:
            if row[1] == "vector" and row[3] == nameTarget and row[2]=="Mode4World.node["+str(node)+"].lteNic.phy":
                ts = re.split(" ",row[7])
                pdrs = re.split(" ",row[8])
                decodes=[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
                for t_i in range(len(ts)):
                    index = int(int(float(ts[t_i])-28800.0)/5)
                    # print(index)
                    if index >= 6:
                        index = 5
                    decodes[index][0] += float(pdrs[t_i])
                    decodes[index][1] += 1
                for i in range(len(pdr_devide2)):
                    if decodes[i][1] != 0:
                        pdr_devide2[i]=decodes[i][0]/decodes[i][1]*1.0
                    else :
                        pdr_devide2[i]=decodes[i][0]/1*1.0
    
    tp["ds"] = pdr_devide2

    fig = plt.figure()
    #pdr
    ax = fig.add_subplot(111)
    # ax.set_ylim(0.0,100.0)
    df = pd.DataFrame(tp,timeStamp_pdr)
    #sps
    # ax.bar(timeStamp_pdr,pdr_devide)
    # ax.bar(timeStamp_pdr,pdr_devide2,color="orange")
    df.plot.bar(ax=ax)
    ax.grid(axis="y")
    ax.set_xlabel("Time [s]")
    ylabel = "Packet Delivery Ratio [%]"
    if isDelay: ylabel="Average Packet Delay[s]"
    ax.set_ylabel(ylabel)
    # #speed
    # ax2 = ax.twinx()
    # ax2.plot(timeStamp_v,velocity,"o-",c="green")
    # ax2.set_ylabel("speed")
    # ax2.set_ylim(0,120)

    if args[3] in ["250493","266134","269288","270927","273261","278171","280942"] :
        fig.savefig("./vehicleCamData/accel/"+mode+"_"+option)
    elif args[3] in ["224968","232596","236142","241865","244755","252205","258230","258547","259677","260595","261664","262434","262795","264411","266291","268286","269573","269612","270878","270929","272766","272936","273027","274079","278859","279073"]:
        fig.savefig("./vehicleCamData/brake/"+mode+"_"+option)
    elif args[3] in ["213042","230094","235209","236281","238094","238515","239471","241224","242455","242705","248901","249833","250492","254508","256852","257179","257408","258461","258911","259073","262590","263254","264905","266999","267014","268354","268419","268631","270705","271784","272045","276084","281101","281397","285115"]:
        fig.savefig("./vehicleCamData/direct/"+mode+"_"+option)
    elif args[3] in ["222407","227837","239013","251330","257824","263810","265442","268859","270367"]:
        fig.savefig("./vehicleCamData/left/"+mode+"_"+option)
    elif args[3] in ["215182","219496","224432","234779","252777","263831","264173","268948","277043"]:
        fig.savefig("./vehicleCamData/right/"+mode+"_"+option)
    else:
        fig.savefig("./vehicleCamData/"+mode+"_"+option)


if mode == "delay":
    fig, ax= plt.subplots()
    ax.get_xticklabels()
    ss = "./results/sps_1015_interPacketDelay.csv"
    sd = "./results/ds_1015_interPacketDelay.csv"
    tp = {}
    left = ["[0,0.2)","[0.2,0.4)","[0.4,0.6)","[0.6,0.8)","[0.8,1.0)","[1.0,1.2)","[1.2,1.4)","[1.4,1.6)","[1.6,1.8)","[1.8,2.0)","[2.0,∞]"]
    accel=[]
    brake=[]
    direct=[]
    left = []
    right = []
    for v in ["250493","266134","269288","270927","273261","278171","280942"]:
        accel.append(VEHICLE_DATA[int(v)][1])
    for v in ["224968","232596","236142","241865","244755","252205","258230","258547","259677","260595","261664","262434","262795","264411","266291","268286","269573","269612","270878","270929","272766","272936","273027","274079","278859","279073"]:
        brake.append(VEHICLE_DATA[int(v)][1])
    for v in ["213042","230094","235209","236281","238094","238515","239471","241224","242455","242705","248901","249833","250492","254508","256852","257179","257408","258461","258911","259073","262590","263254","264905","266999","267014","268354","268419","268631","270705","271784","272045","276084","281101","281397","285115"]:
        direct.append(VEHICLE_DATA[int(v)][1])
    for v in ["222407","227837","239013","251330","257824","263810","265442","268859","270367"]:
        left.append(VEHICLE_DATA[int(v)][1])
    for v in ["215182","219496","224432","234779","252777","263831","264173","268948","277043"]:
        right.append(VEHICLE_DATA[int(v)][1])
    
        
    
    
    data_accel = [0,0,0,0,0,0,0,0,0,0,0]
    data_brake = [0,0,0,0,0,0,0,0,0,0,0]
    data_direct = [0,0,0,0,0,0,0,0,0,0,0]
    data_left = [0,0,0,0,0,0,0,0,0,0,0]
    data_right = [0,0,0,0,0,0,0,0,0,0,0]
    
    #sps
    with open(ss) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == "interPacketDelay:vector":
                array = re.split(" ",row[8])
                for a in array:
                    try:
                        index = int(float(a)*10/2)
                        if index > 9 :
                            index=10
                        node = re.split("[]",row[2])
                        if node[1] in accel:
                            data_accel[index] += 1
                        elif node[1] in brake:
                            data_brake[index]+=1
                        elif node[1] in direct:
                            data_direct[index]+=1
                        elif node[1] in left:
                            data_left[index]+=1
                        elif node[1] in right:
                            data_right[index]+=1
                        
                    except IndexError:
                        print(index)

    tp["sps_a"] = data
    
    data_accel = [0,0,0,0,0,0,0,0,0,0,0]
    data_brake = [0,0,0,0,0,0,0,0,0,0,0]
    data_direct = [0,0,0,0,0,0,0,0,0,0,0]
    data_left = [0,0,0,0,0,0,0,0,0,0,0]
    data_right = [0,0,0,0,0,0,0,0,0,0,0]
    #ds
    with open(sd) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == "interPacketDelay:vector":
                array = re.split(" ",row[8])
                for a in array:
                    try:
                        index = int(float(a)*10/2)
                        if index > 9 :
                            index=10
                        node = re.split("[]",row[2])
                        if node[1] in accel:
                            data_accel[index] += 1
                        elif node[1] in brake:
                            data_brake[index]+=1
                        elif node[1] in direct:
                            data_direct[index]+=1
                        elif node[1] in left:
                            data_left[index]+=1
                        elif node[1] in right:
                            data_right[index]+=1
                    except IndexError:
                        print(index)
    tp["ds"] = data

    df = pd.DataFrame(tp,left)
    # ax.set_xticks(sendinterval)
    ax.set_xticklabels(left)
    plt.xlabel("Inter-Packet Delay [s]")
    plt.ylabel("Number of CAM")
    df.plot.bar(ax=ax)
    # plt.setp(left, rotation=45, fontsize=9)
    plt.xticks(fontsize=9)
    plt.xticks(rotation=45)
    save = "delay"
    fig.savefig(save+"_"+option)