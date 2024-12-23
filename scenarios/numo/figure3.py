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
mode = ""
option=""

if len(args)>=3:
    option=args[2]
if len(args)>=2 :
    mode=args[1]
INTERSECTION_A_NODE = {'430':'552910253','294':'2025187190','1196':'962980710','950':'1287726651','1920':'1921376925','985':'2135019593','1035':'2078107280','412':'1329132133','1788':'1945891638','466':'1144522535','1754':'204428608','572':'1376035217','903':'219544266','1403':'922587542','912':'1671735990','834':'670752506','1220':'1690492373','1023':'610486506','1444':'1221389873','1555':'1565306616','395':'114723506','494':'1402961682','456':'559301039','502':'1941690360','543':'318561886','1517':'703955951','350':'1253207672','1931':'995097051','951':'146533149','332':'1797073940','1991':'517408978','864':'1370973813','1879':'346502533','1588':'578187134','1961':'138700754','835':'2025554010','1418':'1069117832','352':'1414647625','895':'1669475776','918':'1875641892','1186':'1587992726','1268':'1947691087','1314':'1569115921','1965':'237140292','1594':'87522686','1222':'1984498433','1924':'1320634492','1435':'419914800','1582':'263043320','817':'1487053959','1832':'2026478004','1636':'940472515','797':'1581539848','1816':'1386214636','1120':'318322042','926':'1267889618','426':'739273303','1221':'1111800030','1276':'1390598089','1948':'1680687005','935':'772634225','1182':'1926411641','1258':'692981712','1562':'354367395','1294':'1256273378','512':'1184214677','1433':'1989200801','1674':'1438865740','2081':'1758204253'}
INTERSECTION_B_NODE = {'315':'1469262009','1935':'2070707654','929':'1663080928','774':'628966950','254':'1308044878','1912':'132629780','1833':'1659239833','356':'1896306640','128':'1610120709','100':'1036140795','1090':'1607774548','967':'413360099','1005':'12548159','83':'1889947178','1117':'1903409954','1241':'415675634','1043':'1143195511','1475':'116423768','1411':'858829294','1269':'245240853','431':'1671294892','652':'1543324176','585':'1647149314','1604':'819827984','1590':'1578716908','187':'1626276121','1208':'1107096180','668':'1965421244','1313':'750679664','1129':'242474976'}
STREET_C_NODE = {'430':'552910253','1035':'2078107280','412':'1329132133','1403':'922587542','1968':'339335164','1444':'1221389873','1183':'1812718902','1912':'132629780','1844':'438485374','1186':'1587992726','1222':'1984498433','1727':'1992232983','1522':'33713861','426':'739273303','1674':'1438865740'}
STREET_D_NODE = {'1196':'962980710','1754':'204428608','903':'219544266','912':'1671735990','1526':'777635325','1555':'1565306616','1521':'599529154','1235':'359147515','1427':'1727952741','1406':'1209379174','543':'318561886','350':'1253207672','951':'146533149','933':'370917955','1991':'517408978','864':'1370973813','975':'1736491298','1588':'578187134','1961':'138700754','352':'1414647625','1646':'1391927494','895':'1669475776','918':'1875641892','1965':'237140292','618':'1388391521','1497':'219994425','817':'1487053959','1832':'2026478004','1417':'1101533292','797':'1581539848','926':'1267889618','1276':'1390598089','1948':'1680687005','1913':'1744161708','1600':'934618834','527':'1630634994','976':'1396918184','800':'207026272','1706':'65785292','195':'1605894428','512':'1184214677','875':'209359415','836':'1649709016','1000':'981914693','1830':'421101832','1060':'878273679','927':'1326247643'}


def make_timeRange(s):
    timeRange= {}
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            node = str(row[1])
            if node in timeRange:
                if timeRange[node][1] < round(float(row[2]),1):
                    timeRange[node][1] = round(float(row[2]),1)
            else:
                timeRange[node] = [math.floor(float(row[2])*10)/10,round(float(row[2]),1)]
    return timeRange

if mode == "delay":
    fig, ax= plt.subplots()
    ax.get_xticklabels()
    ss = "./results/sps_1026_high.csv"
    sd = "./results/ds_1026_high.csv"
    tp = {}
    left = ["[0,0.02)","[0.02,0.04)","[0.04,0.06)","[0.06,0.08)","[0.08,0.10)","[0.10,0.12)","[0.12,0.14)","[0.14,0.16)","[0.16,0.18)","[0.18,0.2)","[0.2,∞]"]
    data = [0,0,0,0,0,0,0,0,0,0,0]
    #sps
    with open(ss) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == "CamReceived:vector":
                array = re.split(" ",row[8])
                for a in array:
                    try:
                        index = int(float(a)*100/2)
                        if index > 9 :
                            index=10
                        data[index] += 1
                    except IndexError:
                        print(index)

    print("sps")
    print(data)
    print("total:"+str(data[0]+data[1]+data[2]+data[3]+data[4]+data[5]+data[6]+data[7]+data[8]+data[9]+data[10]))
    tp["sps"] = data
    data = [0,0,0,0,0,0,0,0,0,0,0]
    #ds
    with open(sd) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == "CamReceived:vector":
                array = re.split(" ",row[8])
                for a in array:
                    try:
                        index = int(float(a)*100/2)
                        if index > 9 :
                            index=10
                        data[index] += 1
                    except IndexError:
                        print(index)
    print("ds")
    print(data)
    print("total:"+str(data[0]+data[1]+data[2]+data[3]+data[4]+data[5]+data[6]+data[7]+data[8]+data[9]+data[10]))
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


if mode == "cbr":
    fig, ax= plt.subplots()
    ax.get_xticklabels()
    ss = "./results/sps_smooth.csv"
    sd = "./results/ds_smooth.csv"
    tp = {}
    # left = ["[0,10)","[0.1,0.2)","[0.2,0.3)","[0.3,0.08)","[0.08,0.10)","[0.10,0.12)","[0.12,0.14)","[0.14,0.16)","[0.16,0.18)","[0.18,0.2)","[0.2,∞]"]
    # data = [0,0,0,0,0,0,0,0,0,0,0]
    y_data_a =[]
    y_data2_a =[]
    x_data=[]
    y_data_b =[]
    y_data2_b =[]
    
    y_data_c =[]
    y_data2_c =[]
    
    y_data_d =[]
    y_data2_d =[]
   
    startTime = 28800.0
    for i in range(0,301):
        x_data.append(i*0.1)
        y_data_a.append(0.0)
        y_data2_a.append(0.0)
      
        y_data_b.append(0.0)
        y_data2_b.append(0.0)
        
        y_data_c.append(0.0)
        y_data2_c.append(0.0)
       
        y_data_d.append(0.0)
        y_data2_d.append(0.0)
        

    timeRange_a={}
    timeRange_b={}
    timeRange_c={}
    timeRange_d={}
    s_c_a = "./results/intersection_a_sps.csv"
    s_c_b = "./results/intersection_b_sps.csv"
    s_c_c = "./results/street_c_sps.csv"
    s_c_d = "./results/street_d_sps.csv"

    # with open(s_c_a) as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         node = str(row[1])
    #         if node in timeRange_a:
    #             if timeRange_a[node][1] < round(float(row[2]),1):
    #                 timeRange_a[node][1] = round(float(row[2]),1)
    #         else:
    #             timeRange_a[node] = [math.floor(float(row[2])*10)/10,round(float(row[2]),1)]
    # with open(s_c_b) as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         node = str(row[1])
    #         if node in timeRange_b:
    #             if timeRange_b[node][1] < round(float(row[2]),1):
    #                 timeRange_b[node][1] = round(float(row[2]),1)
    #         else:
    #             timeRange_b[node] = [math.floor(float(row[2])*10)/10,round(float(row[2]),1)]
    # with open(s_c_c) as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         node = str(row[1])
    #         if node in timeRange_c:
    #             if timeRange_c[node][1] < round(float(row[2]),1):
    #                 timeRange_c[node][1] = round(float(row[2]),1)
    #         else:
    #             timeRange_c[node] = [math.floor(float(row[2])*10)/10,round(float(row[2]),1)]
    # with open(s_c_d) as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         node = str(row[1])
    #         if node in timeRange_d:
    #             if timeRange_d[node][1] < round(float(row[2]),1):
    #                 timeRange_d[node][1] = round(float(row[2]),1)
    #         else:
    #             timeRange_d[node] = [math.floor(float(row[2])*10)/10,round(float(row[2]),1)]
    timeRange_a = make_timeRange(s_c_a)  
    timeRange_b = make_timeRange(s_c_b)  
    timeRange_c = make_timeRange(s_c_c)  
    timeRange_d = make_timeRange(s_c_d)  
    #sps
    with open(ss) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == "cbr:vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(array)):
                    try:
                        if vehicle in INTERSECTION_A_NODE.keys() and float(times[j]) >= timeRange_a[vehicle][0] and float(times[j]) <= timeRange_a[vehicle][1]+0.2:
                            y_data_a[int((float(times[j])-startTime)*10)] = (y_data_a[int((float(times[j])-startTime)*10)] * len(y_data_a) + float(array[j])) / (len(y_data_a)+1)
                        if vehicle in INTERSECTION_B_NODE.keys() and float(times[j]) >= timeRange_b[vehicle][0] and float(times[j]) <= timeRange_b[vehicle][1]+0.2:
                            y_data_b[int((float(times[j])-startTime)*10)] = (y_data_b[int((float(times[j])-startTime)*10)] * len(y_data_b) + float(array[j])) / (len(y_data_b)+1)
                        if vehicle in STREET_C_NODE.keys() and float(times[j]) >= timeRange_c[vehicle][0] and float(times[j]) <= timeRange_c[vehicle][1]+0.2:
                            y_data_c[int((float(times[j])-startTime)*10)] = (y_data_c[int((float(times[j])-startTime)*10)] * len(y_data_c) + float(array[j])) / (len(y_data_c)+1)
                        if vehicle in STREET_D_NODE.keys() and float(times[j]) >= timeRange_d[vehicle][0] and float(times[j]) <= timeRange_d[vehicle][1]+0.2:
                            y_data_d[int((float(times[j])-startTime)*10)] = (y_data_d[int((float(times[j])-startTime)*10)] * len(y_data_d) + float(array[j])) / (len(y_data_d)+1)
                    except IndexError:
                        print(int((float(times[j])-startTime)*10))
                        exit()


    
    #ds
    with open(sd) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == "cbr:vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(array)):
                    try:
                        if vehicle in INTERSECTION_A_NODE.keys() and float(times[j]) >= timeRange_a[vehicle][0] and float(times[j]) <= timeRange_a[vehicle][1]+0.2:
                            y_data2_a[int((float(times[j])-startTime)*10)] = (y_data2_a[int((float(times[j])-startTime)*10)] * len(y_data2_a) + float(array[j])) / (len(y_data2_a)+1)
                        if vehicle in INTERSECTION_B_NODE.keys() and float(times[j]) >= timeRange_b[vehicle][0] and float(times[j]) <= timeRange_b[vehicle][1]+0.2:
                            y_data2_b[int((float(times[j])-startTime)*10)] = (y_data2_b[int((float(times[j])-startTime)*10)] * len(y_data2_b) + float(array[j])) / (len(y_data2_b)+1)
                        if vehicle in STREET_C_NODE.keys() and float(times[j]) >= timeRange_c[vehicle][0] and float(times[j]) <= timeRange_c[vehicle][1]+0.2:
                            y_data2_c[int((float(times[j])-startTime)*10)] = (y_data2_c[int((float(times[j])-startTime)*10)] * len(y_data2_c) + float(array[j])) / (len(y_data2_c)+1)
                        if vehicle in STREET_D_NODE.keys() and float(times[j]) >= timeRange_d[vehicle][0] and float(times[j]) <= timeRange_d[vehicle][1]+0.2:
                            y_data2_d[int((float(times[j])-startTime)*10)] = (y_data2_d[int((float(times[j])-startTime)*10)] * len(y_data2_d) + float(array[j])) / (len(y_data2_d)+1)
                    except IndexError:
                        print(int((float(times[j])-startTime)*10))
                        exit()

                    
    ax.plot(x_data,y_data_a,"o-",c="blue",label="sps_a")
    ax.plot(x_data,y_data2_a,"o-",c="aqua",label="ds_a")
    ax.plot(x_data,y_data_b,"o-",c="red",label="sps_b")
    ax.plot(x_data,y_data2_b,"o-",c="violet",label="ds_b")
    ax.plot(x_data,y_data_c,"o-",c="orange",label="sps_c")
    ax.plot(x_data,y_data2_c,"o-",c="yellow",label="ds_c")
    ax.plot(x_data,y_data_d,"o-",c="green",label="sps_d")
    ax.plot(x_data,y_data2_d,"o-",c="palegreen",label="ds_d")
    plt.legend()

    plt.xlabel("Simulation Time [s]")
    plt.ylabel("Average CBR")
    # plt.setp(left, rotation=45, fontsize=9)
    plt.xticks(fontsize=9)
    plt.xticks(rotation=45)
    save = "cbr"
    fig.savefig(save+"_"+option)



if mode in ["traffic_pdr","traffic_delay","box_traffic_pdr","box_traffic_delay"]:
    # traffic_pdr :
    # x:count of tbSent * 190byte * 8 /0.5s  
    # y:count of tbDecoded=1/total of tbDecoded  for each 0.5s
    #
    # traffic_delay:
    # x:count of tbSent * 190byte * 8 /0.5s
    # y:average of latency for each 0.5s
    span = 5.0
    ss = "./results/sps_smooth2_rri300.csv"
    sd = "./results/ds_smooth2.csv"
    if len(args) >= 4:
        ss = args[3]
    if len(args) >= 5:
        sd = args[4]
    if len(args) >= 6:
        span = float(args[5])
    
    tp = {}
    # span = 5.0
    box_span = 50000
    startTime = 28800.0
    simTime = 30
    #sps
    x_data_a = {}
    x_data_a_app = {}
    y_decode_data_a = []
    y_total_data_a=[]
    x_data_b = {}
    x_data_b_app = {}
    y_decode_data_b = []
    y_total_data_b=[]
    x_data_c = {}
    x_data_c_app = {}
    y_decode_data_c = []
    y_total_data_c=[]
    x_data_d = {}
    x_data_d_app = {}
    y_decode_data_d = []
    y_total_data_d=[]

    timeRange_a={}
    timeRange_b={}
    timeRange_c={}
    timeRange_d={}
    s_c_a = "./results/intersection_a_sps.csv"
    s_c_b = "./results/intersection_b_sps.csv"
    s_c_c = "./results/street_c_sps.csv"
    s_c_d = "./results/street_d_sps.csv"



# txrxDistance => senderID 11/26
    senderID = {}
    senderID2= {}
    
    with open(ss) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == "senderID:vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                senderID[vehicle] = {}
                for i in range(len(array)):
                    senderID[vehicle][times[i]]=str(int(array[i])-1025)
    with open(sd) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == "senderID:vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                senderID2[vehicle] = {}
                for i in range(len(array)):
                    senderID2[vehicle][times[i]]=str(int(array[i])-1025)
    
   # txrxDistance
    distance_a = {}
    distance_b = {}
    distance_c = {}
    distance_d = {}
    
    
    # with open(ss) as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         if row[1] == "vector" and row[3] == 'txRxDistanceTB:vector':
    #             vehicle = re.split("[\[\]]",row[2])[1]
    #             times = re.split(" ",row[7])
    #             array = re.split(" ",row[8])
    #             distance[vehicle] = {}
    #             for i in range(len(array)):
    #                 distance[vehicle][times[i]]=float(array[i])
    # with open(sd) as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         if row[1] == "vector" and row[3] == 'txRxDistanceTB:vector':
    #             vehicle = re.split("[\[\]]",row[2])[1]
    #             times = re.split(" ",row[7])
    #             array = re.split(" ",row[8])
    #             distance2[vehicle] = {}
    #             for i in range(len(array)):
    #                 distance2[vehicle][times[i]]=float(array[i])
    
            

    # print(senderID)
    if mode in ["traffic_pdr","traffic_delay","box_traffic_pdr","box_traffic_delay"]:
        for i in range(int(simTime/span)+1) :   
            x_data_a[i] = 0.0
            x_data_a_app[i] = 0.0
            y_decode_data_a.append(0.0)
            y_total_data_a.append(0)
            x_data_b[i] = 0.0
            x_data_b_app[i] = 0.0
            y_decode_data_b.append(0.0)
            y_total_data_b.append(0)
            x_data_c[i] = 0.0
            x_data_c_app[i] = 0.0
            y_decode_data_c.append(0.0)
            y_total_data_c.append(0)
            x_data_d[i] = 0.0
            x_data_d_app[i] = 0.0
            y_decode_data_d.append(0.0)
            y_total_data_d.append(0)


    with open(s_c_a) as f:
        reader = csv.reader(f)
        for row in reader:
            node = str(row[1])
            if node in timeRange_a:
                if timeRange_a[node][1] < float(row[2]):
                    timeRange_a[node][1] = float(row[2])
            else:
                timeRange_a[node] = [float(row[2]),float(row[2])]
            x_data_a_app[int((float(row[2])-startTime)/span)] += 190 * 8
    with open(s_c_b) as f:
        reader = csv.reader(f)
        for row in reader:
            node = str(row[1])
            if node in timeRange_b:
                if timeRange_b[node][1] < float(row[2]):
                    timeRange_b[node][1] = float(row[2])
            else:
                timeRange_b[node] = [float(row[2]),float(row[2])]
            x_data_b_app[int((float(row[2])-startTime)/span)] += 190 * 8
    with open(s_c_c) as f:
        reader = csv.reader(f)
        for row in reader:
            node = str(row[1])
            if node in timeRange_c:
                if timeRange_c[node][1] < float(row[2]):
                    timeRange_c[node][1] = float(row[2])
            else:
                timeRange_c[node] = [float(row[2]),float(row[2])]
            x_data_c_app[int((float(row[2])-startTime)/span)] += 190 * 8
    with open(s_c_d) as f:
        reader = csv.reader(f)
        for row in reader:
            node = str(row[1])
            if node in timeRange_d:
                if timeRange_d[node][1] < float(row[2]):
                    timeRange_d[node][1] = float(row[2])
            else:
                timeRange_d[node] = [float(row[2]),float(row[2])]
            x_data_d_app[int((float(row[2])-startTime)/span)] += 190 * 8
      
        
    
    #((x+y)/2 * 2 +z)/3 = 
    
    # elif mode in ["pdr"]:
    #     for i in range(int(500/50)+1):
    #         distance_a[i] = 0


    with open(ss) as f:
        reader = csv.reader(f)
        for row in reader:
            #対象外の車はcontinue
            if row[1] == "vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                if vehicle not in INTERSECTION_A_NODE.keys() and vehicle not in INTERSECTION_B_NODE.keys() and vehicle not in STREET_C_NODE.keys() and vehicle not in STREET_D_NODE.keys():
                    continue
            if row[1] == "vector" and row[3] == "tbSent:vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    # 時間内のものだけを入れる
                    if (vehicle in INTERSECTION_A_NODE.keys() 
                        and float(times[j]) >= timeRange_a[vehicle][0] 
                        and float(times[j]) <= timeRange_a[vehicle][1] + 0.2):
                        x_data_a[int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

                    if (vehicle in INTERSECTION_B_NODE.keys() 
                        and float(times[j]) >= timeRange_b[vehicle][0] 
                        and float(times[j]) <= timeRange_b[vehicle][1] + 0.2):
                        x_data_b[int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

                    if (vehicle in STREET_C_NODE.keys() 
                        and float(times[j]) >= timeRange_c[vehicle][0] 
                        and float(times[j]) <= timeRange_c[vehicle][1] + 0.2):
                        x_data_c[int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

                    if (vehicle in STREET_D_NODE.keys() 
                        and float(times[j]) >= timeRange_d[vehicle][0] 
                        and float(times[j]) <= timeRange_d[vehicle][1] + 0.2):
                        x_data_d[int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])
            # if row[1] == "vector" and row[3] == "txRxDistanceTB:vector":
            #     vehicle = re.split("[\[\]]",row[2])[1]
            #     times = re.split(" ",row[7])
            #     array = re.split(" ",row[8])
            #     for j in range(len(times)):
            #         # 時間内のものだけを入れる
            #         if (vehicle in INTERSECTION_A_NODE.keys() 
            #             and float(times[j]) >= timeRange_a[vehicle][0] 
            #             and float(times[j]) <= timeRange_a[vehicle][1] + 0.2
            #             and senderID[vehicle][times[j]] in INTERSECTION_A_NODE.keys()):
            #             x_data_a[int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

            #         if (vehicle in INTERSECTION_B_NODE.keys() 
            #             and float(times[j]) >= timeRange_b[vehicle][0] 
            #             and float(times[j]) <= timeRange_b[vehicle][1] + 0.2
            #             and senderID[vehicle][times[j]] in INTERSECTION_B_NODE.keys()):
            #             x_data_b[int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

            #         if (vehicle in STREET_C_NODE.keys() 
            #             and float(times[j]) >= timeRange_c[vehicle][0] 
            #             and float(times[j]) <= timeRange_c[vehicle][1] + 0.2
            #             and senderID[vehicle][times[j]] in STREET_C_NODE.keys()):
            #             x_data_c[int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

            #         if (vehicle in STREET_D_NODE.keys() 
            #             and float(times[j]) >= timeRange_d[vehicle][0] 
            #             and float(times[j]) <= timeRange_d[vehicle][1] + 0.2
            #             and senderID[vehicle][times[j]] in STREET_D_NODE.keys()):
            #             x_data_d[int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])
            if row[1] == "vector" and row[3] == "tbDecoded:vector" and mode in ["traffic_pdr","box_traffic_pdr"]:
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    # 時間内のものだけを入れる
                    # index = int((float(times[j])-startTime)/span)
                    # try:
                    #     y_decode_data[index] = (y_decode_data[index]*y_total_data[index] + int(float(array[j])))/(y_total_data[index]+1)
                    #     y_total_data[index] += 1
                    # except IndexError:
                    #     print("index:" + str(index))
                    #     print("j:" + str(j))
                    index = 0
                    if vehicle in INTERSECTION_A_NODE.keys() and float(times[j]) >= timeRange_a[vehicle][0] and float(times[j]) <= timeRange_a[vehicle][1]+0.2 and senderID[vehicle][times[j]] in INTERSECTION_A_NODE.keys():
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data_a[index] = (y_decode_data_a[index]*y_total_data_a[index] + int(float(array[j])))/(y_total_data_a[index]+1)
                        y_total_data_a[index] += 1
                    if vehicle in INTERSECTION_B_NODE.keys() and float(times[j]) >= timeRange_b[vehicle][0] and float(times[j]) <= timeRange_b[vehicle][1]+0.2 and senderID[vehicle][times[j]] in INTERSECTION_B_NODE.keys():
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data_b[index] = (y_decode_data_b[index]*y_total_data_b[index] + int(float(array[j])))/(y_total_data_b[index]+1)
                        y_total_data_b[index] += 1
                    if vehicle in STREET_C_NODE.keys() and float(times[j]) >= timeRange_c[vehicle][0] and float(times[j]) <= timeRange_c[vehicle][1]+0.2 and senderID[vehicle][times[j]] in STREET_C_NODE.keys():
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data_c[index] = (y_decode_data_c[index]*y_total_data_c[index] + int(float(array[j])))/(y_total_data_c[index]+1)
                        y_total_data_c[index] += 1
                    if vehicle in STREET_D_NODE.keys() and float(times[j]) >= timeRange_d[vehicle][0] and float(times[j]) <= timeRange_d[vehicle][1]+0.2 and senderID[vehicle][times[j]] in STREET_D_NODE.keys():
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data_d[index] = (y_decode_data_d[index]*y_total_data_d[index] + int(float(array[j])))/(y_total_data_d[index]+1)
                        y_total_data_d[index] += 1
                    
            if row[1] == "vector" and row[3] == "CamReceived:vector" and mode in ["traffic_delay","box_traffic_delay"]:
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    # 時間内のものだけを入れる
                    index = 0
                    if vehicle in INTERSECTION_A_NODE.keys() and float(times[j]) >= timeRange_a[vehicle][0] and float(times[j]) <= timeRange_a[vehicle][1]+0.2:
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data_a[index] = (y_decode_data_a[index]*y_total_data_a[index] + float(array[j]))/(y_total_data_a[index]+1)
                        y_total_data_a[index] += 1
                    if vehicle in INTERSECTION_B_NODE.keys() and float(times[j]) >= timeRange_b[vehicle][0] and float(times[j]) <= timeRange_b[vehicle][1]+0.2:
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data_b[index] = (y_decode_data_b[index]*y_total_data_b[index] + float(array[j]))/(y_total_data_b[index]+1)
                        y_total_data_b[index] += 1
                    if vehicle in STREET_C_NODE.keys() and float(times[j]) >= timeRange_c[vehicle][0] and float(times[j]) <= timeRange_c[vehicle][1]+0.2:
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data_c[index] = (y_decode_data_c[index]*y_total_data_c[index] + float(array[j]))/(y_total_data_c[index]+1)
                        y_total_data_c[index] += 1
                    if vehicle in STREET_D_NODE.keys() and float(times[j]) >= timeRange_d[vehicle][0] and float(times[j]) <= timeRange_d[vehicle][1]+0.2:
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data_d[index] = (y_decode_data_d[index]*y_total_data_d[index] + float(array[j]))/(y_total_data_d[index]+1)
                        y_total_data_d[index] += 1
            
    sorted_items_by_value_a = sorted(x_data_a.items(), key=lambda item: item[1])
    x_sorted_a = {k: v for k, v in sorted_items_by_value_a}
    sorted_items_by_value_a = sorted(x_data_a.items(), key=lambda item: item[1])
    x_sorted_a = {k: v for k, v in sorted_items_by_value_a}
    # print(x_sorted_)
    y_data_a =[]
    sorted_items_by_value_b = sorted(x_data_b.items(), key=lambda item: item[1])
    x_sorted_b = {k: v for k, v in sorted_items_by_value_b}
    # print(x_sorted_)
    y_data_b=[]
    sorted_items_by_value_c = sorted(x_data_c.items(), key=lambda item: item[1])
    x_sorted_c = {k: v for k, v in sorted_items_by_value_c}
    # print(x_sorted_)
    y_data_c =[]
    sorted_items_by_value_d = sorted(x_data_d.items(), key=lambda item: item[1])
    x_sorted_d = {k: v for k, v in sorted_items_by_value_d}
    # print(x_sorted_)
    y_data_d =[]
    print("sps\na:")
    for k in x_sorted_a.keys():
        if mode in ["traffic_pdr","box_traffic_pdr"]:
            y_data_a.append(y_decode_data_a[k]*100.0)
            print("decode rate:"+str(y_decode_data_a[k]*100.0)+", total receive:" + str(y_total_data_a[k]))
        elif mode in ["traffic_delay","box_traffic_delay"]:
            y_data_a.append(y_decode_data_a[k]*1000.0)
            print("average delay time:"+str(y_decode_data_a[k]*100.0)+", total receive:" + str(y_total_data_a[k]))
    print("分散:" + str(np.var(y_data_a)))
    print("b:")
    for k in x_sorted_b.keys():
        if mode in ["traffic_pdr","box_traffic_pdr"]:
            y_data_b.append(y_decode_data_b[k]*100.0)
            print("decode rate:"+str(y_decode_data_b[k]*100.0)+", total receive:" + str(y_total_data_b[k]))
        elif mode in ["traffic_delay","box_traffic_delay"]:
            y_data_b.append(y_decode_data_b[k]*1000.0)
            print("average delay time:"+str(y_decode_data_b[k]*100.0)+", total receive:" + str(y_total_data_b[k]))
    print("分散:" + str(np.var(y_data_b)))
    print("c:")
    for k in x_sorted_c.keys():
        if mode in ["traffic_pdr","box_traffic_pdr"]:
            y_data_c.append(y_decode_data_c[k]*100.0)
            print("decode rate:"+str(y_decode_data_c[k]*100.0)+", total receive:" + str(y_total_data_c[k]))
        elif mode in ["traffic_delay","box_traffic_delay"]:
            y_data_c.append(y_decode_data_c[k]*1000.0)
            print("average delay time:"+str(y_decode_data_c[k]*100.0)+", total receive:" + str(y_total_data_c[k]))
    print("分散:" + str(np.var(y_data_c)))
    print("d:")
    for k in x_sorted_d.keys():
        if mode in ["traffic_pdr","box_traffic_pdr"]:
            y_data_d.append(y_decode_data_d[k]*100.0)
            print("decode rate:"+str(y_decode_data_d[k]*100.0)+", total receive:" + str(y_total_data_d[k]))
        elif mode in ["traffic_delay","box_traffic_delay"]:
            y_data_d.append(y_decode_data_d[k]*1000.0)
            print("average delay time:"+str(y_decode_data_d[k]*100.0)+", total receive:" + str(y_total_data_d[k]))
    print("分散:" + str(np.var(y_data_d)))
    # x_value = float(x_sorted.values())
    x_value_a=[]
    for k, v in x_sorted_a.items():
        x_value_a.append(float(v))
    x_value_b=[]
    for k, v in x_sorted_b.items():
        x_value_b.append(float(v))
    x_value_c=[]
    for k, v in x_sorted_c.items():
        x_value_c.append(float(v))
    x_value_d=[]
    for k, v in x_sorted_d.items():
        x_value_d.append(float(v))
    
    
    #ds
    x_data2_a = {}
    y_decode_data2_a = []
    y_total_data2_a =[]
    x_data2_b = {}
    y_decode_data2_b = []
    y_total_data2_b =[]
    x_data2_c = {}
    y_decode_data2_c = []
    y_total_data2_c =[]
    x_data2_d = {}
    y_decode_data2_d = []
    y_total_data2_d =[]

    for i in range(int(simTime/span)+1) :   
        x_data2_a[i] = 0.0
        y_decode_data2_a.append(0.0)
        y_total_data2_a.append(0)
        x_data2_b[i] = 0.0
        y_decode_data2_b.append(0.0)
        y_total_data2_b.append(0)
        x_data2_c[i] = 0.0
        y_decode_data2_c.append(0.0)
        y_total_data2_c.append(0)
        x_data2_d[i] = 0.0
        y_decode_data2_d.append(0.0)
        y_total_data2_d.append(0)

    with open(sd) as f:
        reader = csv.reader(f)
        for row in reader:
            #対象外の車はcontinue
            if row[1] == "vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                if vehicle not in INTERSECTION_A_NODE.keys() and vehicle not in INTERSECTION_B_NODE.keys() and vehicle not in STREET_C_NODE.keys() and vehicle not in STREET_D_NODE.keys():
                    continue
            if row[1] == "vector" and row[3] == "tbSent:vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    # 時間内のものだけを入れる
                    if (vehicle in INTERSECTION_A_NODE.keys()
                        and float(times[j]) >= timeRange_a[vehicle][0]
                        and float(times[j]) <= timeRange_a[vehicle][1] + 0.2):
                        x_data2_a[int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

                    if (vehicle in INTERSECTION_B_NODE.keys()
                        and float(times[j]) >= timeRange_b[vehicle][0]
                        and float(times[j]) <= timeRange_b[vehicle][1] + 0.2):
                        x_data2_b[int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

                    if (vehicle in STREET_C_NODE.keys()
                        and float(times[j]) >= timeRange_c[vehicle][0]
                        and float(times[j]) <= timeRange_c[vehicle][1] + 0.2):
                        x_data2_c[int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

                    if (vehicle in STREET_D_NODE.keys()
                        and float(times[j]) >= timeRange_d[vehicle][0]
                        and float(times[j]) <= timeRange_d[vehicle][1] + 0.2):
                        x_data2_d[int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

            if row[1] == "vector" and row[3] == "tbDecoded:vector" and mode in ["traffic_pdr","box_traffic_pdr"]:
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    # 時間内のものだけを入れる
                    # index = int((float(times[j])-startTime)/span)
                    # try:
                    #     y_decode_data2[index] = (y_decode_data2[index]*y_total_data2[index] + int(float(array[j])))/(y_total_data2[index]+1)
                    #     y_total_data2[index] += 1
                    # except IndexError:
                    #     print("index:" + str(index))
                    #     print("j:" + str(j))
                    index = 0
                    if vehicle in INTERSECTION_A_NODE.keys() and float(times[j]) >= timeRange_a[vehicle][0] and float(times[j]) <= timeRange_a[vehicle][1]+0.2 and senderID2[vehicle][times[j]] in INTERSECTION_A_NODE.keys():
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data2_a[index] = (y_decode_data2_a[index]*y_total_data2_a[index] + int(float(array[j])))/(y_total_data2_a[index]+1)
                        y_total_data2_a[index] += 1
                    if vehicle in INTERSECTION_B_NODE.keys() and float(times[j]) >= timeRange_b[vehicle][0] and float(times[j]) <= timeRange_b[vehicle][1]+0.2 and senderID2[vehicle][times[j]] in INTERSECTION_B_NODE.keys():
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data2_b[index] = (y_decode_data2_b[index]*y_total_data2_b[index] + int(float(array[j])))/(y_total_data2_b[index]+1)
                        y_total_data2_b[index] += 1
                    if vehicle in STREET_C_NODE.keys() and float(times[j]) >= timeRange_c[vehicle][0] and float(times[j]) <= timeRange_c[vehicle][1]+0.2 and senderID2[vehicle][times[j]] in STREET_C_NODE.keys():
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data2_c[index] = (y_decode_data2_c[index]*y_total_data2_c[index] + int(float(array[j])))/(y_total_data2_c[index]+1)
                        y_total_data2_c[index] += 1
                    if vehicle in STREET_D_NODE.keys() and float(times[j]) >= timeRange_d[vehicle][0] and float(times[j]) <= timeRange_d[vehicle][1]+0.2 and senderID2[vehicle][times[j]] in STREET_D_NODE.keys():
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data2_d[index] = (y_decode_data2_d[index]*y_total_data2_d[index] + int(float(array[j])))/(y_total_data2_d[index]+1)
                        y_total_data2_d[index] += 1
                    
            if row[1] == "vector" and row[3] == "CamReceived:vector" and mode in ["traffic_delay","box_traffic_delay"]:
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    # 時間内のものだけを入れる
                    index = 0
                    if (vehicle in INTERSECTION_A_NODE.keys()
                        and float(times[j]) >= timeRange_a[vehicle][0]
                        and float(times[j]) <= timeRange_a[vehicle][1] + 0.2):
                        index = int((float(times[j]) - startTime) / span)
                        y_decode_data2_a[index] = (y_decode_data2_a[index] * y_total_data2_a[index] + float(array[j])) / (y_total_data2_a[index] + 1)
                        y_total_data2_a[index] += 1

                    if (vehicle in INTERSECTION_B_NODE.keys()
                        and float(times[j]) >= timeRange_b[vehicle][0]
                        and float(times[j]) <= timeRange_b[vehicle][1] + 0.2):
                        index = int((float(times[j]) - startTime) / span)
                        y_decode_data2_b[index] = (y_decode_data2_b[index] * y_total_data2_b[index] + float(array[j])) / (y_total_data2_b[index] + 1)
                        y_total_data2_b[index] += 1

                    if (vehicle in STREET_C_NODE.keys()
                        and float(times[j]) >= timeRange_c[vehicle][0]
                        and float(times[j]) <= timeRange_c[vehicle][1] + 0.2):
                        index = int((float(times[j]) - startTime) / span)
                        y_decode_data2_c[index] = (y_decode_data2_c[index] * y_total_data2_c[index] + float(array[j])) / (y_total_data2_c[index] + 1)
                        y_total_data2_c[index] += 1

                    if (vehicle in STREET_D_NODE.keys()
                        and float(times[j]) >= timeRange_d[vehicle][0]
                        and float(times[j]) <= timeRange_d[vehicle][1] + 0.2):
                        index = int((float(times[j]) - startTime) / span)
                        y_decode_data2_d[index] = (y_decode_data2_d[index] * y_total_data2_d[index] + float(array[j])) / (y_total_data2_d[index] + 1)
                        y_total_data2_d[index] += 1
                                
    sorted_items_by_value_a = sorted(x_data2_a.items(), key=lambda item: item[1])
    x_sorted_a = {k: v for k, v in sorted_items_by_value_a}
    # print(x_sorted_)
    y_data2_a =[]
    sorted_items_by_value_b = sorted(x_data2_b.items(), key=lambda item: item[1])
    x_sorted_b = {k: v for k, v in sorted_items_by_value_b}
    # print(x_sorted_)
    y_data2_b=[]
    sorted_items_by_value_c = sorted(x_data2_c.items(), key=lambda item: item[1])
    x_sorted_c = {k: v for k, v in sorted_items_by_value_c}
    # print(x_sorted_)
    y_data2_c =[]
    sorted_items_by_value_d = sorted(x_data2_d.items(), key=lambda item: item[1])
    x_sorted_d = {k: v for k, v in sorted_items_by_value_d}
    # print(x_sorted_)
    y_data2_d =[]
    print("ds\na:")
    for k in x_sorted_a.keys():
        if mode in ["traffic_pdr","box_traffic_pdr"]:
            y_data2_a.append(y_decode_data2_a[k]*100.0)
            print("decode rate:"+str(y_decode_data2_a[k]*100)+", total receive:" + str(y_total_data2_a[k]))
        elif mode in ["traffic_delay","box_traffic_delay"]:
            y_data2_a.append(y_decode_data2_a[k]*1000.0)
            print("average delay time:"+str(y_decode_data2_a[k]*100)+", total receive:" + str(y_total_data2_a[k]))
    print("分散:" + str(np.var(y_data2_a)))
    print("b:")
    for k in x_sorted_b.keys():
        if mode in ["traffic_pdr","box_traffic_pdr"]:
            y_data2_b.append(y_decode_data2_b[k]*100.0)
            print("decode rate:"+str(y_decode_data2_b[k]*100)+", total receive:" + str(y_total_data2_b[k]))
        elif mode in ["traffic_delay","box_traffic_delay"]:
            y_data2_b.append(y_decode_data2_b[k]*1000.0)
            print("average delay time:"+str(y_decode_data2_b[k]*100)+", total receive:" + str(y_total_data2_b[k]))
    print("分散:" + str(np.var(y_data2_b)))
    print("c:")
    for k in x_sorted_c.keys():
        if mode in ["traffic_pdr","box_traffic_pdr"]:
            y_data2_c.append(y_decode_data2_c[k]*100.0)
            print("decode rate:"+str(y_decode_data2_c[k]*100)+", total receive:" + str(y_total_data2_c[k]))
        elif mode in ["traffic_delay","box_traffic_delay"]:
            y_data2_c.append(y_decode_data2_c[k]*1000.0)
            print("average delay time:"+str(y_decode_data2_c[k]*100)+", total receive:" + str(y_total_data2_c[k]))
    print("分散:" + str(np.var(y_data2_c)))
    print("d:")
    for k in x_sorted_d.keys():
        if mode in ["traffic_pdr","box_traffic_pdr"]:
            y_data2_d.append(y_decode_data2_d[k]*100.0)
            print("decode rate:"+str(y_decode_data2_d[k]*100)+", total receive:" + str(y_total_data2_d[k]))
        elif mode in ["traffic_delay","box_traffic_delay"]:
            y_data2_d.append(y_decode_data2_d[k]*1000.0)
            print("average delay time:"+str(y_decode_data2_d[k]*100)+", total receive:" + str(y_total_data2_d[k]))
    print("分散:" + str(np.var(y_data2_d)))
    # x_value = float(x_sorted.values())
    x_value2_a=[]
    for k, v in x_sorted_a.items():
        x_value2_a.append(float(v))
    x_value2_b=[]
    for k, v in x_sorted_b.items():
        x_value2_b.append(float(v))
    x_value2_c=[]
    for k, v in x_sorted_c.items():
        x_value2_c.append(float(v))
    x_value2_d=[]
    for k, v in x_sorted_d.items():
        x_value2_d.append(float(v))
    #sps=100
    ss2 = "./results/sps_smooth2_rri100.csv"
    senderID3 = {}
    with open(ss2) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == "senderID:vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                senderID3[vehicle] = {}
                for i in range(len(array)):
                    senderID3[vehicle][times[i]]=str(int(array[i])-1025)
    x_data3_a = {}
    y_decode_data3_a = []
    y_total_data3_a =[]
    x_data3_b = {}
    y_decode_data3_b = []
    y_total_data3_b =[]
    x_data3_c = {}
    y_decode_data3_c = []
    y_total_data3_c =[]
    x_data3_d = {}
    y_decode_data3_d = []
    y_total_data3_d =[]

    for i in range(int(simTime/span)+1) :   
        x_data3_a[i] = 0.0
        y_decode_data3_a.append(0.0)
        y_total_data3_a.append(0)
        x_data3_b[i] = 0.0
        y_decode_data3_b.append(0.0)
        y_total_data3_b.append(0)
        x_data3_c[i] = 0.0
        y_decode_data3_c.append(0.0)
        y_total_data3_c.append(0)
        x_data3_d[i] = 0.0
        y_decode_data3_d.append(0.0)
        y_total_data3_d.append(0)

    with open(ss2) as f:
        reader = csv.reader(f)
        for row in reader:
            #対象外の車はcontinue
            if row[1] == "vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                if vehicle not in INTERSECTION_A_NODE.keys() and vehicle not in INTERSECTION_B_NODE.keys() and vehicle not in STREET_C_NODE.keys() and vehicle not in STREET_D_NODE.keys():
                    continue
            if row[1] == "vector" and row[3] == "tbSent:vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    # 時間内のものだけを入れる
                    if (vehicle in INTERSECTION_A_NODE.keys()
                        and float(times[j]) >= timeRange_a[vehicle][0]
                        and float(times[j]) <= timeRange_a[vehicle][1] + 0.2):
                        x_data3_a[int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

                    if (vehicle in INTERSECTION_B_NODE.keys()
                        and float(times[j]) >= timeRange_b[vehicle][0]
                        and float(times[j]) <= timeRange_b[vehicle][1] + 0.2):
                        x_data3_b[int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

                    if (vehicle in STREET_C_NODE.keys()
                        and float(times[j]) >= timeRange_c[vehicle][0]
                        and float(times[j]) <= timeRange_c[vehicle][1] + 0.2):
                        x_data3_c[int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

                    if (vehicle in STREET_D_NODE.keys()
                        and float(times[j]) >= timeRange_d[vehicle][0]
                        and float(times[j]) <= timeRange_d[vehicle][1] + 0.2):
                        x_data3_d[int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

            if row[1] == "vector" and row[3] == "tbDecoded:vector" and mode in ["traffic_pdr","box_traffic_pdr"]:
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    # 時間内のものだけを入れる
                    # index = int((float(times[j])-startTime)/span)
                    # try:
                    #     y_decode_data3[index] = (y_decode_data3[index]*y_total_data3[index] + int(float(array[j])))/(y_total_data3[index]+1)
                    #     y_total_data3[index] += 1
                    # except IndexError:
                    #     print("index:" + str(index))
                    #     print("j:" + str(j))
                    index = 0
                    if vehicle in INTERSECTION_A_NODE.keys() and float(times[j]) >= timeRange_a[vehicle][0] and float(times[j]) <= timeRange_a[vehicle][1]+0.2 and senderID3[vehicle][times[j]] in INTERSECTION_A_NODE.keys():
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data3_a[index] = (y_decode_data3_a[index]*y_total_data3_a[index] + int(float(array[j])))/(y_total_data3_a[index]+1)
                        y_total_data3_a[index] += 1
                    if vehicle in INTERSECTION_B_NODE.keys() and float(times[j]) >= timeRange_b[vehicle][0] and float(times[j]) <= timeRange_b[vehicle][1]+0.2 and senderID3[vehicle][times[j]] in INTERSECTION_B_NODE.keys():
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data3_b[index] = (y_decode_data3_b[index]*y_total_data3_b[index] + int(float(array[j])))/(y_total_data3_b[index]+1)
                        y_total_data3_b[index] += 1
                    if vehicle in STREET_C_NODE.keys() and float(times[j]) >= timeRange_c[vehicle][0] and float(times[j]) <= timeRange_c[vehicle][1]+0.2 and senderID3[vehicle][times[j]] in STREET_C_NODE.keys():
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data3_c[index] = (y_decode_data3_c[index]*y_total_data3_c[index] + int(float(array[j])))/(y_total_data3_c[index]+1)
                        y_total_data3_c[index] += 1
                    if vehicle in STREET_D_NODE.keys() and float(times[j]) >= timeRange_d[vehicle][0] and float(times[j]) <= timeRange_d[vehicle][1]+0.2 and senderID3[vehicle][times[j]] in STREET_D_NODE.keys():
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data3_d[index] = (y_decode_data3_d[index]*y_total_data3_d[index] + int(float(array[j])))/(y_total_data3_d[index]+1)
                        y_total_data3_d[index] += 1
                    
            if row[1] == "vector" and row[3] == "CamReceived:vector" and mode in ["traffic_delay","box_traffic_delay"]:
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    # 時間内のものだけを入れる
                    index = 0
                    if (vehicle in INTERSECTION_A_NODE.keys()
                        and float(times[j]) >= timeRange_a[vehicle][0]
                        and float(times[j]) <= timeRange_a[vehicle][1] + 0.2):
                        index = int((float(times[j]) - startTime) / span)
                        y_decode_data3_a[index] = (y_decode_data3_a[index] * y_total_data3_a[index] + float(array[j])) / (y_total_data3_a[index] + 1)
                        y_total_data3_a[index] += 1

                    if (vehicle in INTERSECTION_B_NODE.keys()
                        and float(times[j]) >= timeRange_b[vehicle][0]
                        and float(times[j]) <= timeRange_b[vehicle][1] + 0.2):
                        index = int((float(times[j]) - startTime) / span)
                        y_decode_data3_b[index] = (y_decode_data3_b[index] * y_total_data3_b[index] + float(array[j])) / (y_total_data3_b[index] + 1)
                        y_total_data3_b[index] += 1

                    if (vehicle in STREET_C_NODE.keys()
                        and float(times[j]) >= timeRange_c[vehicle][0]
                        and float(times[j]) <= timeRange_c[vehicle][1] + 0.2):
                        index = int((float(times[j]) - startTime) / span)
                        y_decode_data3_c[index] = (y_decode_data3_c[index] * y_total_data3_c[index] + float(array[j])) / (y_total_data3_c[index] + 1)
                        y_total_data3_c[index] += 1

                    if (vehicle in STREET_D_NODE.keys()
                        and float(times[j]) >= timeRange_d[vehicle][0]
                        and float(times[j]) <= timeRange_d[vehicle][1] + 0.2):
                        index = int((float(times[j]) - startTime) / span)
                        y_decode_data3_d[index] = (y_decode_data3_d[index] * y_total_data3_d[index] + float(array[j])) / (y_total_data3_d[index] + 1)
                        y_total_data3_d[index] += 1
                                
    sorted_items_by_value_a = sorted(x_data3_a.items(), key=lambda item: item[1])
    x_sorted_a = {k: v for k, v in sorted_items_by_value_a}
    # print(x_sorted_)
    y_data3_a =[]
    sorted_items_by_value_b = sorted(x_data3_b.items(), key=lambda item: item[1])
    x_sorted_b = {k: v for k, v in sorted_items_by_value_b}
    # print(x_sorted_)
    y_data3_b=[]
    sorted_items_by_value_c = sorted(x_data3_c.items(), key=lambda item: item[1])
    x_sorted_c = {k: v for k, v in sorted_items_by_value_c}
    # print(x_sorted_)
    y_data3_c =[]
    sorted_items_by_value_d = sorted(x_data3_d.items(), key=lambda item: item[1])
    x_sorted_d = {k: v for k, v in sorted_items_by_value_d}
    # print(x_sorted_)
    y_data3_d =[]
    print("ds\na:")
    for k in x_sorted_a.keys():
        if mode in ["traffic_pdr","box_traffic_pdr"]:
            y_data3_a.append(y_decode_data3_a[k]*100.0)
            print("decode rate:"+str(y_decode_data3_a[k]*100)+", total receive:" + str(y_total_data3_a[k]))
        elif mode in ["traffic_delay","box_traffic_delay"]:
            y_data3_a.append(y_decode_data3_a[k]*1000.0)
            print("average delay time:"+str(y_decode_data3_a[k]*100)+", total receive:" + str(y_total_data3_a[k]))
    print("分散:" + str(np.var(y_data3_a)))
    print("b:")
    for k in x_sorted_b.keys():
        if mode in ["traffic_pdr","box_traffic_pdr"]:
            y_data3_b.append(y_decode_data3_b[k]*100.0)
            print("decode rate:"+str(y_decode_data3_b[k]*100)+", total receive:" + str(y_total_data3_b[k]))
        elif mode in ["traffic_delay","box_traffic_delay"]:
            y_data3_b.append(y_decode_data3_b[k]*1000.0)
            print("average delay time:"+str(y_decode_data3_b[k]*100)+", total receive:" + str(y_total_data3_b[k]))
    print("分散:" + str(np.var(y_data3_b)))
    print("c:")
    for k in x_sorted_c.keys():
        if mode in ["traffic_pdr","box_traffic_pdr"]:
            y_data3_c.append(y_decode_data3_c[k]*100.0)
            print("decode rate:"+str(y_decode_data3_c[k]*100)+", total receive:" + str(y_total_data3_c[k]))
        elif mode in ["traffic_delay","box_traffic_delay"]:
            y_data3_c.append(y_decode_data3_c[k]*1000.0)
            print("average delay time:"+str(y_decode_data3_c[k]*100)+", total receive:" + str(y_total_data3_c[k]))
    print("分散:" + str(np.var(y_data3_c)))
    print("d:")
    for k in x_sorted_d.keys():
        if mode in ["traffic_pdr","box_traffic_pdr"]:
            y_data3_d.append(y_decode_data3_d[k]*100.0)
            print("decode rate:"+str(y_decode_data3_d[k]*100)+", total receive:" + str(y_total_data3_d[k]))
        elif mode in ["traffic_delay","box_traffic_delay"]:
            y_data3_d.append(y_decode_data3_d[k]*1000.0)
            print("average delay time:"+str(y_decode_data3_d[k]*100)+", total receive:" + str(y_total_data3_d[k]))
    print("分散:" + str(np.var(y_data3_d)))
    # x_value = float(x_sorted.values())
    x_value3_a=[]
    for k, v in x_sorted_a.items():
        x_value3_a.append(float(v))
    x_value3_b=[]
    for k, v in x_sorted_b.items():
        x_value3_b.append(float(v))
    x_value3_c=[]
    for k, v in x_sorted_c.items():
        x_value3_c.append(float(v))
    x_value3_d=[]
    for k, v in x_sorted_d.items():
        x_value3_d.append(float(v))
    
    fig, ax = plt.subplots()
    
    if mode in ["traffic_pdr","traffic_delay"]:
        ax.scatter(x_value3_a[1:], y_data3_a[1:], marker="o", c="blue",label="sps_rri100_a")
        ax.scatter(x_value_a[1:], y_data_a[1:], marker="^", c="blue",label="sps_rri1_a")
        ax.scatter(x_value2_a[1:], y_data2_a[1:],marker="x", c="aqua",label="ds_a")
        ax.scatter(x_value3_b[1:], y_data3_b[1:], marker="o", c="green",label="sps_rri100_b")
        ax.scatter(x_value_b[1:], y_data_b[1:], marker="^", c="green",label="sps_rri1_b")
        ax.scatter(x_value2_b[1:], y_data2_b[1:],marker="x", c="palegreen",label="ds_b")
        ax.scatter(x_value3_c[1:], y_data3_c[1:], marker="o", c="red",label="sps_rri100_c")
        ax.scatter(x_value_c[1:], y_data_c[1:], marker="^", c="red",label="sps_rri1_c")
        ax.scatter(x_value2_c[1:], y_data2_c[1:],marker="x", c="violet",label="ds_c")
        ax.scatter(x_value3_d[1:], y_data3_d[1:], marker="o", c="orange",label="sps_rri100_d")
        ax.scatter(x_value_d[1:], y_data_d[1:], marker="^", c="orange",label="sps_rri1_d")
        ax.scatter(x_value2_d[1:], y_data2_d[1:],marker="x", c="yellow",label="ds_d")
        ax.plot(x_value3_a[1:], np.poly1d(np.polyfit(x_value3_a[1:], y_data3_a[1:], 1))(x_value3_a[1:]),c="blue")
        ax.plot(x_value_a[1:], np.poly1d(np.polyfit(x_value_a[1:], y_data_a[1:], 1))(x_value_a[1:]),":",c="blue")
        ax.plot(x_value2_a[1:], np.poly1d(np.polyfit(x_value2_a[1:], y_data2_a[1:], 1))(x_value2_a[1:]),c="aqua")
        ax.plot(x_value3_b[1:], np.poly1d(np.polyfit(x_value3_b[1:], y_data3_b[1:], 1))(x_value3_b[1:]),c="green")
        ax.plot(x_value_b[1:], np.poly1d(np.polyfit(x_value_b[1:], y_data_b[1:], 1))(x_value_b[1:]),":",c="green")
        ax.plot(x_value2_b[1:], np.poly1d(np.polyfit(x_value2_b[1:], y_data2_b[1:], 1))(x_value2_b[1:]),c="palegreen")
        ax.plot(x_value3_c[1:], np.poly1d(np.polyfit(x_value3_c[1:], y_data3_c[1:], 1))(x_value3_c[1:]),c="red")
        ax.plot(x_value_c[1:], np.poly1d(np.polyfit(x_value_c[1:], y_data_c[1:], 1))(x_value_c[1:]),":",c="red")
        ax.plot(x_value2_c[1:], np.poly1d(np.polyfit(x_value2_c[1:], y_data2_c[1:], 1))(x_value2_c[1:]),c="violet")
        ax.plot(x_value3_d[1:], np.poly1d(np.polyfit(x_value3_d[1:], y_data3_d[1:], 1))(x_value3_d[1:]),c="orange")
        ax.plot(x_value_d[1:], np.poly1d(np.polyfit(x_value_d[1:], y_data_d[1:], 1))(x_value_d[1:]),":",c="orange")
        ax.plot(x_value2_d[1:], np.poly1d(np.polyfit(x_value2_d[1:], y_data2_d[1:], 1))(x_value2_d[1:]),c="yellow")
        
        ax.set_ylim(0,101)

        # リストをps.Seriesに変換
        s1_a=pd.Series(x_value_a[1:])
        s2_a=pd.Series(y_data_a[1:])
        s3_a=pd.Series(x_value2_a[1:])
        s4_a=pd.Series(y_data2_a[1:])
        s1_b=pd.Series(x_value_b[1:])
        s2_b=pd.Series(y_data_b[1:])
        s3_b=pd.Series(x_value2_b[1:])
        s4_b=pd.Series(y_data2_b[1:])
        s1_c=pd.Series(x_value_c[1:])
        s2_c=pd.Series(y_data_c[1:])
        s3_c=pd.Series(x_value2_c[1:])
        s4_c=pd.Series(y_data2_c[1:])
        s1_d=pd.Series(x_value_d[1:])
        s2_d=pd.Series(y_data_d[1:])
        s3_d=pd.Series(x_value2_d[1:])
        s4_d=pd.Series(y_data2_d[1:])
        

        # pandasを使用してPearson's rを計算
        # res=s1.corr(s2)   # numpy.float64 に格納される
        # res2 = s3.corr(s4)
    elif mode in ["box_traffic_pdr","box_traffic_delay"]:
        labels =[]
        minX_a=int(x_value_a[1])//box_span * box_span
        # maxX = int(x_value[len(x_value)-1])//box_span * box_span
        minX2_a=int(x_value2_a[1])//box_span * box_span
        # maxX2 = int(x_value2[len(x_value)-1])//box_span * box_span
        minX_b=int(x_value_b[1])//box_span * box_span
        # maxX = int(x_value[len(x_value)-1])//box_span * box_span
        minX2_b=int(x_value2_b[1])//box_span * box_span
        # maxX2 = int(x_value2[len(x_value)-1])//box_span * box_span
        minX_c=int(x_value_c[1])//box_span * box_span
        # maxX = int(x_value[len(x_value)-1])//box_span * box_span
        minX2_c=int(x_value2_c[1])//box_span * box_span
        # maxX2 = int(x_value2[len(x_value)-1])//box_span * box_span
        minX_d=int(x_value_d[1])//box_span * box_span
        # maxX = int(x_value[len(x_value)-1])//box_span * box_span
        minX2_d=int(x_value2_d[1])//box_span * box_span
        # maxX2 = int(x_value2[len(x_value)-1])//box_span * box_span
        
        label_now=""
        point_a ={}
        point2_a = {}
        point_b ={}
        point2_b = {}
        point_c ={}
        point2_c = {}
        point_d ={}
        point2_d = {}
        x_box_data_a = []
        x_box_data2_a = []
        x_box_data_b = []
        x_box_data2_b = []
        x_box_data_c = []
        x_box_data2_c = []
        x_box_data_d = []
        x_box_data2_d = []
        # n x y method
        level = minX_a
        for i in range(1,len(x_value_a)) :
            if x_value_a[i] >= level:
                level += box_span
            s = "["+str((level-box_span)//1000)+","+str(level//1000) + ")"
            x_box_data_a.append(s)

        level = minX2_a
        for i in range(1,len(x_value2_a)) :
            if x_value2_a[i] >= level:
                level += box_span
            s = "["+str((level-box_span)//1000)+","+str(level//1000) + ")"
            x_box_data2_a.append(s)
        level = minX_b
        for i in range(1,len(x_value_b)) :
            if x_value_b[i] >= level:
                level += box_span
            s = "["+str((level-box_span)//1000)+","+str(level//1000) + ")"
            x_box_data_b.append(s)

        level = minX2_b
        for i in range(1,len(x_value2_b)) :
            if x_value2_b[i] >= level:
                level += box_span
            s = "["+str((level-box_span)//1000)+","+str(level//1000) + ")"
            x_box_data2_b.append(s)
        level = minX_c
        for i in range(1,len(x_value_c)) :
            if x_value_c[i] >= level:
                level += box_span
            s = "["+str((level-box_span)//1000)+","+str(level//1000) + ")"
            x_box_data_c.append(s)

        level = minX2_c
        for i in range(1,len(x_value2_c)) :
            if x_value2_c[i] >= level:
                level += box_span
            s = "["+str((level-box_span)//1000)+","+str(level//1000) + ")"
            x_box_data2_c.append(s)
        
        level = minX_d
        for i in range(1,len(x_value_d)) :
            if x_value_d[i] >= level:
                level += box_span
            s = "["+str((level-box_span)//1000)+","+str(level//1000) + ")"
            x_box_data_d.append(s)

        level = minX2_d
        for i in range(1,len(x_value2_d)) :
            if x_value2_d[i] >= level:
                level += box_span
            s = "["+str((level-box_span)//1000)+","+str(level//1000) + ")"
            x_box_data2_d.append(s)
        
        dict1_a = dict(x=x_box_data_a,y=y_data_a[1:])
        dict2_a = dict(x=x_box_data2_a,y=y_data2_a[1:])
        dict1_b = dict(x=x_box_data_b,y=y_data_b[1:])
        dict2_b = dict(x=x_box_data2_b,y=y_data2_b[1:])
        dict1_c = dict(x=x_box_data_c,y=y_data_c[1:])
        dict2_c = dict(x=x_box_data2_c,y=y_data2_c[1:])
        dict1_d = dict(x=x_box_data_d,y=y_data_d[1:])
        dict2_d = dict(x=x_box_data2_d,y=y_data2_d[1:])
        df1_a =pd.DataFrame(data=dict1_a)
        df2_a = pd.DataFrame(data=dict2_a)
        df1_b =pd.DataFrame(data=dict1_b)
        df2_b = pd.DataFrame(data=dict2_b)
        df1_c =pd.DataFrame(data=dict1_c)
        df2_c = pd.DataFrame(data=dict2_c)
        df1_d =pd.DataFrame(data=dict1_d)
        df2_d = pd.DataFrame(data=dict2_d)
        print(df1_a.head())
        print(df2_a.head())
        # df1_a =pd.DataFrame(point_a,columns=labels)
        # df2_a = pd.DataFrame(point2_a,columns=labels)
        # df1_b =pd.DataFrame(point_b,columns=labels)
        # df2_b = pd.DataFrame(point2_b,columns=labels)
        # df1_c =pd.DataFrame(point_c,columns=labels)
        # df2_c = pd.DataFrame(point2_c,columns=labels)
        # df1_d =pd.DataFrame(point_d,columns=labels)
        # df2_d = pd.DataFrame(point2_d,columns=labels)
        df1_a["method"] = "sps_a"
        df2_a["method"] = "ds_a"
        df1_b["method"] = "sps_b"
        df2_b["method"] = "ds_b"
        df1_c["method"] = "sps_c"
        df2_c["method"] = "ds_c"
        df1_d["method"] = "sps_d"
        df2_d["method"] = "ds_d"
        df = pd.concat([df1_a,df2_a,df1_b,df2_b,df1_c,df2_c,df1_d,df2_d],axis=0)
        print(df.head())
        myColors = {"sps_a":"blue","ds_a":"aqua","sps_b":"green","ds_b":"palegreen","sps_c":"red","ds_c":"violet","sps_d":"orange","ds_d":"yellow"}
        sns.boxplot(x='x', y='y', data=df, hue='method',ax=ax, palette=myColors, showmeans=True,meanprops={"marker":"x","markeredgecolor":"k"})
        

        

    if mode =="traffic_pdr":
        # exp
        # ax.set_xlim(300000,)
        # ax.set_ylim(60,)

        #trigger
        # ax.set_xlim(50000,)
        ax.set_ylim(0,101)

        ax.set(xlabel='Traffic amount [bps]', ylabel="PDR [%]")
    elif mode =="box_traffic_pdr":
        # exp
        # ax.set_xlim(300000,)
        # ax.set_ylim(60,)

        #trigger
        # ax.set_xlim(50000,)
        # ax.set_ylim(60,)

        ax.set(xlabel='Traffic amount [Kbps]', ylabel="PDR [%]")
    elif mode=="traffic_delay":
        # exp
        # ax.set_xlim(300000,)
        # ax.set_ylim(50,)

        #trigger
        # ax.set_xlim(50000,)
        ax.set_ylim(50,)
        ax.set(xlabel='Traffic amount [bps]', ylabel="Average Delay [ms]")
    elif mode=="box_traffic_delay":
        # exp
        # ax.set_xlim(300000,)
        # ax.set_ylim(50,)

        #trigger
        # ax.set_xlim(50000,)
        ax.set_ylim(50,)
        ax.set(xlabel='Traffic amount [Kbps]', ylabel="Average Delay [ms]")
        
    ax.legend(loc="lower left")

    save = mode
    if mode in ["traffic_pdr","traffic_delay"]:
        # fig.savefig(save+"_"+option+"_span"+str(int(span*1000))+"ms_spsCorr"+str(round(res,2))+"_dsCoor"+str(round(res2,2))+".png")
        fig.savefig(save+"_"+option+"_span"+str(int(span*1000))+"ms.png")
    
    elif mode in ["box_traffic_pdr","box_traffic_delay"]:
        fig.savefig(save+"_"+option+"_span"+str(int(span*1000))+"ms_boxSpan"+str(box_span)+".png")
        
    

# 1. 道路ごとのPDRと遅延 vs traffic
# 2.  ;;        PDR vs txrxDistance
# 3. ;;       camのトリガー


#一台ごとの車の軌跡
if mode in {"vehicle_trajectory", "vehicle_pos", "vehicle_pos3D"}:
    s_c_a = "./results/intersection_a_sps.csv"
    s_c_b = "./results/intersection_b_sps.csv"
    s_c_c = "./results/street_c_sps.csv"
    s_c_d = "./results/street_d_sps.csv"
    startTime = 0.0


    target_name= ""
    
    if len(args)>=4:
        target_name = args[3] 

    timeStamp_v=[]
    velocity =[]
    poses_x =[]
    poses_y = []
    target_id = ""
    target_csv = ""
    target_folder = ""
    print(target_name)

    
    if "_a" in option:
        target_id = INTERSECTION_A_NODE[target_name]
        target_csv = s_c_a
        target_folder = "./vehicleCamData/a/"
    elif "_b" in option:
        target_id = INTERSECTION_B_NODE[target_name]
        target_csv = s_c_b
        target_folder = "./vehicleCamData/b/"
    elif "_c" in option:
        target_id = STREET_C_NODE[target_name]
        target_csv = s_c_c
        target_folder = "./vehicleCamData/c/"
    elif "_d" in option:
        target_id = STREET_D_NODE[target_name]
        target_csv = s_c_d
        target_folder = "./vehicleCamData/d/"
    else:
        exit()
    print(target_folder)
    tp={}
    isFirst = True
    first_pos=[]
    colors = []
    post_timeStamp = 0.0
    y_time = []
    with open(target_csv) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == target_id:
                
                if isFirst:
                    isFirst = False
                    poses_x.append(0.0)
                    poses_y.append(0.0)
                    first_pos = [float(row[3]),float(row[4])]
                    startTime = float(row[2])
                    
                else:
                    poses_x.append(float(row[3])-first_pos[0])
                    poses_y.append(float(row[4])-first_pos[1])
                    y_time.append(float(row[2])-post_timeStamp)
                
                timeStamp_v.append(float(row[2])-startTime)
                velocity.append(float(row[5])*3600/1000)
                post_timeStamp = float(row[2])
                print(post_timeStamp)
                #trigger
                #head : red
                #position: blue
                #speed : green
                if int(row[6]) == 1:
                    colors.append("r")
                elif int(row[6])==2:
                    colors.append("b")
                elif int(row[6])==3:
                    colors.append("g")
                else:
                    colors.append("k")
        
    # print(y_count)
    print(y_time)
    print(colors)
    print(velocity)
    print(timeStamp_v)

    
    fig = plt.figure()
    if mode == "vehicle_trajectory":
        
        # cam log
        ax = fig.add_subplot(111)
        ax.set_ylim(0,1.0)
        ax.plot(timeStamp_v[1:],y_time,zorder=0)
        ax.scatter(timeStamp_v[1:],y_time,s=50,c=colors[1:],zorder=1,marker="^")
        ax.grid(axis="y")
        ax.set_xlabel("time[s]")
        ax.set_ylabel("interval[s]")
        
        ax2 = ax.twinx()
        ax2.plot(timeStamp_v[1:],velocity[1:],"o-",c="orange")
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
        ax.plot(poses_x,poses_y,timeStamp_v,"-^")
        plt.grid(axis="y")
        plt.grid(axis="x")

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("time [s]")

    
    fig.savefig(target_folder+mode+"_"+option)


if mode in ["myenv_traffic_pdr","myenv_traffic_delay","myenv_box_traffic_pdr","myenv_box_traffic_delay"]:
    # traffic_pdr :
    # x:count of tbSent * 190byte * 8 /0.5s  
    # y:count of tbDecoded=1/total of tbDecoded  for each 0.5s
    #
    # traffic_delay:
    # x:count of tbSent * 190byte * 8 /0.5s
    # y:average of latency for each 0.5s
    ss = "./results/intersection_0.1.sps.csv"
    sd = "./results/intersection_0.1.ds.csv"
    tp = {}
    span = 1
    box_span = 50000
    startTime = 200.0
    simTime = 100
    #sps
    x_data = {}
    y_decode_data = []
    y_total_data=[]

    colors =[]

    for i in range(int(simTime/span)+1) :   
        x_data[i] = 0.0
        y_decode_data.append(0.0)
        y_total_data.append(0)
        if i <= int(simTime/span/3*1):
            colors.append("aqua")
        elif i <= int(simTime/span/3*2):
            colors.append("blue")
        else:
            colors.append("navy")
    with open(ss) as f:
        reader = csv.reader(f)
        for row in reader:
            
            if row[1] == "vector" and row[3] == "tbSent:vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    x_data[int((float(times[j])-startTime)/span)] += 190*8/span * int(array[j])
                    
            if row[1] == "vector" and row[3] == "tbDecoded:vector" and mode in ["myenv_traffic_pdr","myenv_box_traffic_pdr"]:
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    index = 0
                    index = int((float(times[j])-startTime)/span)
                    y_decode_data[index] = (y_decode_data[index]*y_total_data[index] + int(float(array[j])))/(y_total_data[index]+1)
                    y_total_data[index] += 1
                    
            if row[1] == "vector" and row[3] == "CamReceived:vector" and mode in ["myenv_traffic_delay","myenv_box_traffic_delay"]:
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    index = 0
                    index = int((float(times[j])-startTime)/span)
                    y_decode_data[index] = (y_decode_data[index]*y_total_data[index] + float(array[j]))/(y_total_data[index]+1)
                    y_total_data[index] += 1
                    
    sorted_items_by_value = sorted(x_data.items(), key=lambda item: item[1])
    x_sorted = {k: v for k, v in sorted_items_by_value}
    # x_sorted = x_data
    y_data =[]
    colors_data=[]
    for k in x_sorted.keys():
        if mode in ["myenv_traffic_pdr","myenv_box_traffic_pdr"]:
            y_data.append(y_decode_data[k]*100.0)
            colors_data.append(colors[k])
        elif mode in ["myenv_traffic_delay","myenv_box_traffic_delay"]:
            y_data.append(y_decode_data[k]*1000.0)
    x_value=[]
    for k, v in x_sorted.items():
        x_value.append(float(v))
    
    
    #ds
    x_data2 = {}
    y_decode_data2 = []
    y_total_data2 =[]
    colors2 = []
    for i in range(int(simTime/span)+1) :   
        x_data2[i] = 0.0
        y_decode_data2.append(0.0)
        y_total_data2.append(0)
        if i <= int(simTime/span/3*1):
            colors2.append("yellow")
        elif i <= int(simTime/span/3*2):
            colors2.append("orange")
        else:
            colors2.append("chocolate")
       
    with open(sd) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == "tbSent:vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    x_data2[int((float(times[j])-startTime)/span)] += 190*8/span * int(array[j])
                    
            if row[1] == "vector" and row[3] == "tbDecoded:vector" and mode in ["myenv_traffic_pdr","myenv_box_traffic_pdr"]:
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    index = 0
                    index = int((float(times[j])-startTime)/span)
                    y_decode_data2[index] = (y_decode_data2[index]*y_total_data2[index] + int(float(array[j])))/(y_total_data2[index]+1)
                    y_total_data2[index] += 1
                    
            if row[1] == "vector" and row[3] == "CamReceived:vector" and mode in ["myenv_traffic_delay","myenv_box_traffic_delay"]:
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    index = 0
                    index = int((float(times[j])-startTime)/span)
                    y_decode_data2[index] = (y_decode_data2[index]*y_total_data2[index] + float(array[j]))/(y_total_data2[index]+1)
                    y_total_data2[index] += 1
                   
    sorted_items_by_value = sorted(x_data2.items(), key=lambda item: item[1])
    x_sorted = {k: v for k, v in sorted_items_by_value}
    # x_sorted = x_data2
    y_data2 =[]
    colors2_data = []
    for k in x_sorted.keys():
        if mode in ["myenv_traffic_pdr","myenv_box_traffic_pdr"]:
            y_data2.append(y_decode_data2[k]*100.0)
            colors2_data.append(colors2[k])
        elif mode in ["myenv_traffic_delay","myenv_box_traffic_delay"]:
            y_data2.append(y_decode_data2[k]*1000.0)
    x_value2=[]
    for k, v in x_sorted.items():
        x_value2.append(float(v))
     
    fig, ax = plt.subplots()
    
    if mode in ["myenv_traffic_pdr","myenv_traffic_delay"]:
        ax.scatter(x_value[1:], y_data[1:], marker="o", c="blue",label="sps")
        ax.scatter(x_value2[1:], y_data2[1:],marker="x", c="orange",label="ds")
        ax.plot(x_value[1:], np.poly1d(np.polyfit(x_value[1:], y_data[1:], 1))(x_value[1:]),c="blue")
        ax.plot(x_value2[1:], np.poly1d(np.polyfit(x_value2[1:], y_data2[1:], 1))(x_value2[1:]),c="orange")
        # s1=pd.Series(x_value[1:])
        # s2=pd.Series(y_data[1:])
        # 
        # pandasを使用してPearson's rを計算
        # res=s1.corr(s2)   # numpy.float64 に格納される
        # res2 = s3.corr(s4)
        res=np.var(x_value[1:])
        res1=np.var(y_data[1:])
        res2=np.var(x_value2[1:])
        res3=np.var(y_data2[1:])
        
    elif mode in ["myenv_box_traffic_pdr","myenv_box_traffic_delay"]:
        labels =[]
        minX=int(x_value[1])//box_span * box_span
        minX2=int(x_value2[1])//box_span * box_span
        abel_now=""
        point ={}
        x_box_data = []
        x_box_data2 = []
        
        level = minX
        for i in range(1,len(x_value)) :
            if x_value[i] >= level:
                level += box_span
            s = "["+str((level-box_span)//1000)+","+str(level//1000) + ")"
            x_box_data.append(s)

        level = minX2
        for i in range(1,len(x_value2)) :
            if x_value2[i] >= level:
                level += box_span
            s = "["+str((level-box_span)//1000)+","+str(level//1000) + ")"
            x_box_data2.append(s)
        
        dict1 = dict(x=x_box_data,y=y_data[1:])
        dict2 = dict(x=x_box_data2,y=y_data2[1:])
        df1 =pd.DataFrame(data=dict1)
        df2 = pd.DataFrame(data=dict2)
        df1["method"] = "sps"
        df2["method"] = "ds"
        df = pd.concat([df1,df2],axis=0)
        print(df.head())
        myColors = {"sps":"blue","ds":"orange"}
        sns.boxplot(x='x', y='y', data=df, hue='method',ax=ax, palette=myColors, showmeans=True,meanprops={"marker":"x","markeredgecolor":"k"})

    if mode =="myenv_traffic_pdr":
        # exp
        # ax.set_xlim(300000,)
        # ax.set_ylim(60,)

        #trigger
        # ax.set_xlim(50000,)
        # ax.set_ylim(10,35)

        ax.set(xlabel='Traffic amount [bps]', ylabel="PDR [%]")
    elif mode =="myenv_box_traffic_pdr":
        # exp
        # ax.set_xlim(300000,)
        # ax.set_ylim(60,)

        #trigger
        # ax.set_xlim(50000,)
        # ax.set_ylim(60,)

        ax.set(xlabel='Traffic amount [Kbps]', ylabel="PDR [%]")
    elif mode=="myenv_traffic_delay":
        # exp
        # ax.set_xlim(300000,)
        # ax.set_ylim(50,)

        #trigger
        # ax.set_xlim(50000,)
        # ax.set_ylim(50,)
        ax.set(xlabel='Traffic amount [bps]', ylabel="Average Delay [ms]")
    elif mode=="myenv_box_traffic_delay":
        # exp
        # ax.set_xlim(300000,)
        # ax.set_ylim(50,)

        #trigger
        # ax.set_xlim(50000,)
        # ax.set_ylim(40,)
        ax.set(xlabel='Traffic amount [Kbps]', ylabel="Average Delay [ms]")
        
    ax.legend(loc="lower left")

    save = mode
    if mode in ["myenv_traffic_pdr","myenv_traffic_delay"]:
        # fig.savefig(save+"_"+option+"_span"+str(int(span*1000))+"ms_spsCorr"+str(round(res,2))+"_dsCoor"+str(round(res2,2))+".png")
        fig.savefig(save+"_"+option+"_span"+str(int(span*1000))+"ms.png")
    
    elif mode in ["myenv_box_traffic_pdr","myenv_box_traffic_delay"]:
        fig.savefig(save+"_"+option+"_span"+str(int(span*1000))+"ms_boxSpan"+str(box_span)+".png")
        
# Packet Delivery Ratio ===================================
def parse_if_number(s):
    try: return float(s)
    except: return True if s=="true" else False if s=="false" else s if s else None

def parse_ndarray(s):
    return np.fromstring(s, sep=' ') if s else None

def filter_vectime_and_vecvalue(vectime, vecvalue, module,condition_func):
    if vectime is None or vecvalue is None:  # None の場合はそのまま返す
        return vectime, vecvalue,module
    print(module)
    vehicle = re.split("[\[\]]",module)
    filtered_indices = [i for i, x in enumerate(vectime) if condition_func(x,vehicle)]
    return vectime[filtered_indices], vecvalue[filtered_indices],module
def co(x,m,IDs,nodes):
    if m not in IDs:
        return False
    if str(x) in IDs[m]:
        return IDs[m][str(x)] in nodes
    return False

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
    senderID = {}
    senderID2= {}
    senderID3={}
    interjunction_node = INTERSECTION_A_NODE.keys()

    interjunction2_node = INTERSECTION_B_NODE.keys()

    street_node = STREET_C_NODE.keys()

    street2_node = STREET_D_NODE.keys()
    for i in range(0,1):
        #sps rri=1ms
        s = "./results/sps_smooth2.csv"
        with open(s) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] == "vector" and row[3] == "senderID:vector":
                    vehicle = re.split("[\[\]]",row[2])[1]
                    times = re.split(" ",row[7])
                    array = re.split(" ",row[8])
                    senderID[vehicle] = {}
                    for i in range(len(array)):
                        senderID[vehicle][times[i]]=str(int(array[i])-1025)
        
        marginX = 0
        marginY=0
       
        # interjunction_node = INTERSECTION_A_NODE.keys()

        # interjunction2_node = INTERSECTION_B_NODE.keys()

        # street_node = STREET_C_NODE.keys()

        # street2_node = STREET_D_NODE.keys()


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

        # 条件: 例えば、vectime の値が 0.2 以上の場合のみ残す
        condition_a = lambda x,m: co(x,m,senderID,interjunction_node)
        condition_b = lambda x,m: co(x,m,senderID,interjunction2_node) 
        condition_c = lambda x,m: co(x,m,senderID,street_node) 
        condition_d = lambda x,m: co(x,m,senderID,street2_node)
        

        # vectime と vecvalue を更新
        df_i[['vectime', 'vecvalue','module']] = df.apply(
            lambda row: filter_vectime_and_vecvalue(row['vectime'], row['vecvalue'], row['module'],condition_a),
            axis=1,
            result_type='expand'
        )
        df_s[['vectime', 'vecvalue','module']] = df.apply(
            lambda row: filter_vectime_and_vecvalue(row['vectime'], row['vecvalue'], row['module'],condition_c),
            axis=1,
            result_type='expand'
        )
        
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
        # vectime と vecvalue を更新
        df_i2[['vectime', 'vecvalue','module']] = df.apply(
            lambda row: filter_vectime_and_vecvalue(row['vectime'], row['vecvalue'], row['module'],condition_b),
            axis=1,
            result_type='expand'
        )
        df_s2[['vectime', 'vecvalue','module']] = df.apply(
            lambda row: filter_vectime_and_vecvalue(row['vectime'], row['vecvalue'], row['module'],condition_d),
            axis=1,
            result_type='expand'
        )
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
        s = "./results/ds_smooth2.csv"
        with open(s) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] == "vector" and row[3] == "senderID:vector":
                    vehicle = re.split("[\[\]]",row[2])[1]
                    times = re.split(" ",row[7])
                    array = re.split(" ",row[8])
                    senderID2[vehicle] = {}
                    for i in range(len(array)):
                        senderID2[vehicle][times[i]]=str(int(array[i])-1025)
            marginX = 0
        marginY=0
        node_pos={}
        # interjunction_node=[]
        # street_node=[]
        # interjunction2_node=[]
        # street2_node=[]
        
        # interjunction_node = INTERSECTION_A_NODE.keys()

        # interjunction2_node = INTERSECTION_B_NODE.keys()

        # street_node = STREET_C_NODE.keys()

        # street2_node = STREET_D_NODE.keys()

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

        # 条件: 例えば、vectime の値が 0.2 以上の場合のみ残す
        condition_a = lambda x,m: co(x,m,senderID2,interjunction_node) 
        condition_b = lambda x,m: co(x,m,senderID2,interjunction2_node) 
        condition_c = lambda x,m: co(x,m,senderID2,street_node)
        condition_d = lambda x,m: co(x,m,senderID2,street2_node)
        
        df_i  = df.query('module in @node_label_i')
        df_s = df.query("module in @node_label_s")
        df_i[['vectime', 'vecvalue','module']] = df.apply(
            lambda row: filter_vectime_and_vecvalue(row['vectime'], row['vecvalue'], row['module'],condition_a),
            axis=1,
            result_type='expand'
        )
        df_s[['vectime', 'vecvalue','module']] = df.apply(
            lambda row: filter_vectime_and_vecvalue(row['vectime'], row['vecvalue'], row['module'],condition_c),
            axis=1,
            result_type='expand'
        )

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
        # vectime と vecvalue を更新
        df_i2[['vectime', 'vecvalue','module']] = df.apply(
            lambda row: filter_vectime_and_vecvalue(row['vectime'], row['vecvalue'], row['module'],condition_b),
            axis=1,
            result_type='expand'
        )
        df_s2[['vectime', 'vecvalue','module']] = df.apply(
            lambda row: filter_vectime_and_vecvalue(row['vectime'], row['vecvalue'], row['module'],condition_d),
            axis=1,
            result_type='expand'
        )
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
          
        #sps=100ms
        s = "./results/sps_smooth2_rri100.csv"
        with open(s) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] == "vector" and row[3] == "senderID:vector":
                    vehicle = re.split("[\[\]]",row[2])[1]
                    times = re.split(" ",row[7])
                    array = re.split(" ",row[8])
                    senderID3[vehicle] = {}
                    for i in range(len(array)):
                        senderID3[vehicle][times[i]]=str(int(array[i])-1025)
        marginX = 0
        marginY=0
        node_pos={}
        # interjunction_node=[]
        # street_node=[]
        # interjunction2_node=[]
        # street2_node=[]
        
        # interjunction_node = INTERSECTION_A_NODE.keys()

        # interjunction2_node = INTERSECTION_B_NODE.keys()

        # street_node = STREET_C_NODE.keys()

        # street2_node = STREET_D_NODE.keys()

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

        # 条件: 例えば、vectime の値が 0.2 以上の場合のみ残す
        condition_a = lambda x,m: co(x,m,senderID3,interjunction_node) 
        condition_b = lambda x,m: co(x,m,senderID3,interjunction2_node) 
        condition_c = lambda x,m: co(x,m,senderID3,street_node)
        condition_d = lambda x,m: co(x,m,senderID3,street2_node)
        
        df_i  = df.query('module in @node_label_i')
        df_s = df.query("module in @node_label_s")
        df_i[['vectime', 'vecvalue','module']] = df.apply(
            lambda row: filter_vectime_and_vecvalue(row['vectime'], row['vecvalue'], row['module'],condition_a),
            axis=1,
            result_type='expand'
        )
        df_s[['vectime', 'vecvalue','module']] = df.apply(
            lambda row: filter_vectime_and_vecvalue(row['vectime'], row['vecvalue'], row['module'],condition_c),
            axis=1,
            result_type='expand'
        )

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
        # vectime と vecvalue を更新
        df_i2[['vectime', 'vecvalue','module']] = df.apply(
            lambda row: filter_vectime_and_vecvalue(row['vectime'], row['vecvalue'], row['module'],condition_b),
            axis=1,
            result_type='expand'
        )
        df_s2[['vectime', 'vecvalue','module']] = df.apply(
            lambda row: filter_vectime_and_vecvalue(row['vectime'], row['vecvalue'], row['module'],condition_d),
            axis=1,
            result_type='expand'
        )
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

        pdrs3_i = []
        distances = []
        distance = 0
        for dictionary in bins_i:
            pdrs3_i.append((dictionary["success"] / dictionary["count"] * 100))
            distances.append(distance)
            distance += 10
        pdrs3_s = []
        for dictionary in bins_s:
            pdrs3_s.append((dictionary["success"] / dictionary["count"] * 100))
        pdrs3_i2 = []
        for dictionary in bins_i2:
            pdrs3_i2.append((dictionary["success"] / dictionary["count"] * 100))
        pdrs3_s2 = []
        for dictionary in bins_s2:
            pdrs3_s2.append((dictionary["success"] / dictionary["count"] * 100))
          
            
        
        fig, ax = plt.subplots()
        

        ax.plot(distances, pdrs3_i,"o-", label="sps-100ms inter a", color="blue")
        ax.plot(distances, pdrs3_i2,"o-", label="sps-100ms,inter b",color="green")
        ax.plot(distances, pdrs3_s,"o-", label="sps-100ms,str c",color="red")
        ax.plot(distances, pdrs3_s2,"o-", label="sps-100ms,str d",color="orange")
        ax.plot(distances, pdrs_i,"+;", label="sps-1ms inter a", color="blue")
        ax.plot(distances, pdrs_i2,"+;", label="sps-1ms,inter b",color="green")
        ax.plot(distances, pdrs_s,"+;", label="sps-1ms,str c",color="red")
        ax.plot(distances, pdrs_s2,"+;", label="sps-1ms,str d",color="orange")
        ax.plot(distances, pdrs2_i,"^:", label="ds,inter a",color="blue")
        ax.plot(distances, pdrs2_i2,"^:", label="ds,inter b",color="green")
        ax.plot(distances, pdrs2_s,"^:", label="ds,str c",color="red")
        ax.plot(distances, pdrs2_s2,"^:", label="ds,str d",color="orange")
        



        ax.set(xlabel='Distance (m)', ylabel=yl)
        ax.legend(loc="lower left")
        ax.tick_params(direction='in')
        ax.set_xlim([0, (max(distances) + 1)])
        # ax.set_ylim([0, 101])
        plt.xticks(np.arange(0, (max(distances))+50, step=50))
        plt.yticks(np.arange(0, (101), step=10))



        plt.savefig(mode+"_"+option, dpi=300)

if mode == "grantBreakCount":
    ss="./results/sps_smooth2.csv"
    sd="./results/ds_smooth2.csv"

    timeRange_a={}
    timeRange_b={}
    timeRange_c={}
    timeRange_d={}
    s_c_a = "./results/intersection_a_sps.csv"
    s_c_b = "./results/intersection_b_sps.csv"
    s_c_c = "./results/street_c_sps.csv"
    s_c_d = "./results/street_d_sps.csv"
    timeRange_a = make_timeRange(s_c_a)  
    timeRange_b = make_timeRange(s_c_b)  
    timeRange_c = make_timeRange(s_c_c)  
    timeRange_d = make_timeRange(s_c_d)

    count_i=0
    count_i2=0
    count_s=0
    count_s2=0
    with open(ss) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == "grantBreakTiming:vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(times):
                    if (vehicle in INTERSECTION_A_NODE.keys()
                            ):
                        count_i += array[j]
                    if (vehicle in INTERSECTION_B_NODE.keys()
                            ):
                        count_i2 += array[j]
                    if (vehicle in STREET_C_NODE.keys()
                            ):
                        count_s += array[j]
                    if (vehicle in STREET_D_NODE.keys()
                            ):
                        count_s2 += array[j]
    
    print("sps: count i:" + str(count_i) + ", count i2:" + str(count_i2) + ", count s:" + str(count_s) + ", count s2:" + str(count_s2))
    count_i=0
    count_i2=0
    count_s=0
    count_s2=0
    with open(sd) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == "grantBreakTiming:vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(times):
                    if (vehicle in INTERSECTION_A_NODE.keys()
                            ):
                        count_i += array[j]
                    if (vehicle in INTERSECTION_B_NODE.keys()
                            ):
                        count_i2 += array[j]
                    if (vehicle in STREET_C_NODE.keys()
                            ):
                        count_s += array[j]
                    if (vehicle in STREET_D_NODE.keys()
                            ):
                        count_s2 += array[j]
    
    print("ds: count i:" + str(count_i) + ", count i2:" + str(count_i2) + ", count s:" + str(count_s) + ", count s2:" + str(count_s2))

if mode=="interval":
    fig = plt.figure()
    left = ["intersection a","intersection b","street c","street d"]
    data = [0,0,0,0]
    countChange_a = 0
    countChange_b = 0
    countChange_c = 0
    countChange_d = 0

    s_c_a = "./results/intersection_a_sps.csv"
    s_c_b = "./results/intersection_b_sps.csv"
    s_c_c = "./results/street_c_sps.csv"
    s_c_d = "./results/street_d_sps.csv"
    with open(s_c_a) as f:
        reader = csv.reader(f)
        target_node = ""
        prev_time = 0
        prev_diff = 0
        isSecond = True
        for row in reader:
            node = str(row[1])
            if node != target_node:
                target_node = node
                isSecond = True
            elif isSecond:
                prev_diff = float(row[2]) - prev_time
                isSecond = False
            else:
                if prev_diff - (float(row[2]) - prev_time) >= 0.1:
                    data[0] += 1
                    print("prev_time:"+str(prev_time)+",carrent:"+row[2])
                prev_diff = float(row[2]) - prev_time
            prev_time = float(row[2])
                
                

    with open(s_c_b) as f:
        reader = csv.reader(f)
        target_node = ""
        prev_time = 0
        prev_diff = 0
        isSecond = True
        for row in reader:
            node = str(row[1])
            if node != target_node:
                target_node = node
                isSecond = True
            elif isSecond:
                prev_diff = float(row[2]) - prev_time
                isSecond = False
            else:
                if prev_diff - (float(row[2]) - prev_time) >= 0.1:
                    data[1] += 1
                prev_diff = float(row[2]) - prev_time
            prev_time = float(row[2])

    with open(s_c_c) as f:
        reader = csv.reader(f)
        target_node = ""
        prev_time = 0
        prev_diff = 0
        isSecond = True
        for row in reader:
            node = str(row[1])
            if node != target_node:
                target_node = node
                isSecond = True
            elif isSecond:
                prev_diff = float(row[2]) - prev_time
                isSecond = False
            else:
                if prev_diff - (float(row[2]) - prev_time) >= 0.1:
                    data[2] += 1
                prev_diff = float(row[2]) - prev_time
            prev_time = float(row[2])
    with open(s_c_d) as f:
        reader = csv.reader(f)
        target_node = ""
        prev_time = 0
        prev_diff = 0
        isSecond = True
        for row in reader:
            node = str(row[1])
            if node != target_node:
                target_node = node
                isSecond = True
            elif isSecond:
                prev_diff = float(row[2]) - prev_time
                isSecond = False
            else:
                if prev_diff - (float(row[2]) - prev_time) >= 0.1:
                    data[3] += 1
                prev_diff = float(row[2]) - prev_time
            prev_time = float(row[2])
    print(data)
    colors = ["blue","green","red","orange"]
    plt.bar(left,data,color=colors)
    plt.xlabel("Traffic model")
    plt.ylabel("Number of Message")
    # plt.setp(left, rotation=45, fontsize=9)
    # plt.xticks(fontsize=9)
    # plt.xticks(rotation=45)
    save = mode
    fig.savefig(save+"_"+option)


if mode  == "resourceCollision" :
    ss = "./results/sps_smooth2_rri100.csv"
    sd ="./results/ds_smooth2.csv"

    timeRange_a = {}
    timeRange_b = {}
    timeRange_c = {}
    timeRange_d = {}

    s_c_a = "./results/intersection_a_sps.csv"
    s_c_b = "./results/intersection_b_sps.csv"
    s_c_c = "./results/street_c_sps.csv"
    s_c_d = "./results/street_d_sps.csv"
    timeRange_a = make_timeRange(s_c_a)  
    timeRange_b = make_timeRange(s_c_b)  
    timeRange_c = make_timeRange(s_c_c)  
    timeRange_d = make_timeRange(s_c_d)

    simStart = 28800
    simEnd = 28830

    resourceUsed_s_a = {} # {time:[subchannel,num of access]}
    resourceUsed_s_b = {} # {time:[subchannel,num of access]}
    resourceUsed_s_c = {} # {time:[subchannel,num of access]}
    resourceUsed_s_d = {} # {time:[subchannel,num of access]}
    resourceUsed_d_a = {} # {time:[subchannel,num of access]}
    resourceUsed_d_b = {} # {time:[subchannel,num of access]}   
    resourceUsed_d_c = {} # {time:[subchannel,num of access]}
    resourceUsed_d_d = {} # {time:[subchannel,num of access]}

    for n in range(0,2):
        s =""
        if n==0:
            s = ss
        else:
            s=sd
        with open(s) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] == "vector" and row[3] == "subchannelSent:vector":
                    vehicle = re.split("[\[\]]",row[2])[1]
                    times = re.split(" ",row[7])
                    array = re.split(" ",row[8])
                    for j in range(len(times)):
                        # 時間内のものだけを入れる
                        if (vehicle in INTERSECTION_A_NODE.keys()
                            and float(times[j]) >= timeRange_a[vehicle][0]
                            and float(times[j]) <= timeRange_a[vehicle][1] + 0.2):
                            if s == ss:
                                if float(times[j]) not in resourceUsed_s_a:
                                    resourceUsed_s_a[float(times[j])]= [0,0,0]
                                resourceUsed_s_a[float(times[j])][int(array[j])] += 1
                            else:
                                if float(times[j]) not in resourceUsed_d_a:
                                    resourceUsed_d_a[float(times[j])]= [0,0,0]
                                resourceUsed_d_a[float(times[j])][int(array[j])] += 1
                                

                        if (vehicle in INTERSECTION_B_NODE.keys()
                            and float(times[j]) >= timeRange_b[vehicle][0]
                            and float(times[j]) <= timeRange_b[vehicle][1] + 0.2):
                            if s == ss:
                                if float(times[j]) not in resourceUsed_s_b:
                                    resourceUsed_s_b[float(times[j])]= [0,0,0]
                                resourceUsed_s_b[float(times[j])][int(array[j])] += 1
                            else:
                                if float(times[j]) not in resourceUsed_d_b:
                                    resourceUsed_d_b[float(times[j])]= [0,0,0]
                                resourceUsed_d_b[float(times[j])][int(array[j])] += 1

                        if (vehicle in STREET_C_NODE.keys()
                            and float(times[j]) >= timeRange_c[vehicle][0]
                            and float(times[j]) <= timeRange_c[vehicle][1] + 0.2):
                            if s == ss:
                                if float(times[j]) not in resourceUsed_s_c:
                                    resourceUsed_s_c[float(times[j])]= [0,0,0]
                                resourceUsed_s_c[float(times[j])][int(array[j])] += 1
                            else:
                                if float(times[j]) not in resourceUsed_d_c:
                                    resourceUsed_d_c[float(times[j])]= [0,0,0]
                                resourceUsed_d_c[float(times[j])][int(array[j])] += 1

                        if (vehicle in STREET_D_NODE.keys()
                            and float(times[j]) >= timeRange_d[vehicle][0]
                            and float(times[j]) <= timeRange_d[vehicle][1] + 0.2):
                            if s == ss:
                                if float(times[j]) not in resourceUsed_s_d:
                                    resourceUsed_s_d[float(times[j])]= [0,0,0]
                                resourceUsed_s_d[float(times[j])][int(array[j])] += 1
                            else:
                                if float(times[j]) not in resourceUsed_d_d:
                                    resourceUsed_d_d[float(times[j])]= [0,0,0]
                                resourceUsed_d_d[float(times[j])][int(array[j])] += 1
                            
    userNums = ['2','3']
    counts_s_a =[0,0,0,0,0,0,0]
    counts_s_b =[0,0,0,0,0,0,0]
    counts_s_c =[0,0,0,0,0,0,0]
    counts_s_d =[0,0,0,0,0,0,0]
    counts_d_a =[0,0,0,0,0,0,0]
    counts_d_b =[0,0,0,0,0,0,0]
    counts_d_c =[0,0,0,0,0,0,0]
    counts_d_d =[0,0,0,0,0,0,0]

    for k in resourceUsed_s_a:
        for c in resourceUsed_s_a[k]:
            if c > 6:
                counts_s_a[6] +=1
            elif c>5:
                counts_s_a[5] +=1
            elif c>4:
                counts_s_a[4] +=1
            elif c>3:
                counts_s_a[3] +=1
            elif c>2:
                counts_s_a[2] +=1
            elif c>1:
                counts_s_a[1] +=1
            elif c>0:
                counts_s_a[0] +=1
    for k in resourceUsed_s_b:
        for c in resourceUsed_s_b[k]:
            if c > 6:
                counts_s_b[6] +=1
            elif c>5:
                counts_s_b[5] +=1
            elif c>4:
                counts_s_b[4] +=1
            elif c>3:
                counts_s_b[3] +=1
            elif c>2:
                counts_s_b[2] +=1
            elif c>1:
                counts_s_b[1] +=1
            elif c>0:
                counts_s_b[0] +=1
    for k in resourceUsed_s_c:
        for c in resourceUsed_s_c[k]:
            if c > 6:
                counts_s_c[6] +=1
            elif c>5:
                counts_s_c[5] +=1
            elif c>4:
                counts_s_c[4] +=1
            elif c>3:
                counts_s_c[3] +=1
            elif c>2:
                counts_s_c[2] +=1
            elif c>1:
                counts_s_c[1] +=1
            elif c>0:
                counts_s_c[0] +=1
    for k in resourceUsed_s_d:
        for c in resourceUsed_s_d[k]:
            if c > 6:
                counts_s_d[6] +=1
            elif c>5:
                counts_s_d[5] +=1
            elif c>4:
                counts_s_d[4] +=1
            elif c>3:
                counts_s_d[3] +=1
            elif c>2:
                counts_s_d[2] +=1
            elif c>1:
                counts_s_d[1] +=1
            elif c>0:
                counts_s_d[0] +=1
    for k in resourceUsed_d_a:
        for c in resourceUsed_d_a[k]:
            if c > 6:
                counts_d_a[6] +=1
            elif c>5:
                counts_d_a[5] +=1
            elif c>4:
                counts_d_a[4] +=1
            elif c>3:
                counts_d_a[3] +=1
            elif c>2:
                counts_d_a[2] +=1
            elif c>1:
                counts_d_a[1] +=1
            elif c>0:
                counts_d_a[0] +=1
    for k in resourceUsed_d_b:
        for c in resourceUsed_d_b[k]:
            if c > 6:
                counts_d_b[6] +=1
            elif c>5:
                counts_d_b[5] +=1
            elif c>4:
                counts_d_b[4] +=1
            elif c>3:
                counts_d_b[3] +=1
            elif c>2:
                counts_d_b[2] +=1
            elif c>1:
                counts_d_b[1] +=1
            elif c>0:
                counts_d_b[0] +=1
    for k in resourceUsed_d_c:
        for c in resourceUsed_d_c[k]:
            if c > 6:
                counts_d_c[6] +=1
            elif c>5:
                counts_d_c[5] +=1
            elif c>4:
                counts_d_c[4] +=1
            elif c>3:
                counts_d_c[3] +=1
            elif c>2:
                counts_d_c[2] +=1
            elif c>1:
                counts_d_c[1] +=1
            elif c>0:
                counts_d_c[0] +=1
    for k in resourceUsed_d_d:
        for c in resourceUsed_d_d[k]:
            if c > 6:
                counts_d_d[6] +=1
            elif c>5:
                counts_d_d[5] +=1
            elif c>4:
                counts_d_d[4] +=1
            elif c>3:
                counts_d_d[3] +=1
            elif c>2:
                counts_d_d[2] +=1
            elif c>1:
                counts_d_d[1] +=1
            elif c>0:
                counts_d_d[0] +=1
    tp={'sps-a':counts_s_a[1:3],'sps-b':counts_s_b[1:3],'sps-c':counts_s_c[1:3],'sps-d':counts_s_d[1:3],'ds-a':counts_d_a[1:3],'ds-b':counts_d_b[1:3],'ds-c':counts_d_c[1:3],'ds-d':counts_d_d[1:3]}
    fig, ax = plt.subplots()
    df = pd.DataFrame(tp,userNums)
    # plt.bar(left,collisionRateSps,width=5,edgecolor="black",linewidth=1)
    # plt.bar(left,collisionRateDs,width=5,edgecolor="black",linewidth=1)
    # plt.plot(left,collisionRateSps)
    # plt.plot(left,collisionRateDs)
    plt.xlabel("Number of Users Using Resources")
    plt.ylabel("Count")
    
    df.plot.bar(ax=ax)
    plt.xticks(rotation=0)
    save = mode
    fig.savefig(save+"_"+option)   

            
                            
