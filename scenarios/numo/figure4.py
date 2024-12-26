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
ss = "./results/sps_smooth.csv"
sd = "./results/ds_smooth.csv"


if len(args)>=5:
    sd=args[4]
if len(args)>=4 :
    ss=args[3]
if len(args)>=3:
    option=args[2]
if len(args)>=2 :
    mode=args[1]
INTERSECTION_A_NODE = {'430':'552910253','294':'2025187190','1196':'962980710','950':'1287726651','1920':'1921376925','985':'2135019593','1035':'2078107280','412':'1329132133','1788':'1945891638','466':'1144522535','1754':'204428608','572':'1376035217','903':'219544266','1403':'922587542','912':'1671735990','834':'670752506','1220':'1690492373','1023':'610486506','1444':'1221389873','1555':'1565306616','395':'114723506','494':'1402961682','456':'559301039','502':'1941690360','543':'318561886','1517':'703955951','350':'1253207672','1931':'995097051','951':'146533149','332':'1797073940','1991':'517408978','864':'1370973813','1879':'346502533','1588':'578187134','1961':'138700754','835':'2025554010','1418':'1069117832','352':'1414647625','895':'1669475776','918':'1875641892','1186':'1587992726','1268':'1947691087','1314':'1569115921','1965':'237140292','1594':'87522686','1222':'1984498433','1924':'1320634492','1435':'419914800','1582':'263043320','817':'1487053959','1832':'2026478004','1636':'940472515','797':'1581539848','1816':'1386214636','1120':'318322042','926':'1267889618','426':'739273303','1221':'1111800030','1276':'1390598089','1948':'1680687005','935':'772634225','1182':'1926411641','1258':'692981712','1562':'354367395','1294':'1256273378','512':'1184214677','1433':'1989200801','1674':'1438865740','2081':'1758204253'}
INTERSECTION_B_NODE = {'315':'1469262009','1935':'2070707654','929':'1663080928','774':'628966950','254':'1308044878','1912':'132629780','1833':'1659239833','356':'1896306640','128':'1610120709','100':'1036140795','1090':'1607774548','967':'413360099','1005':'12548159','83':'1889947178','1117':'1903409954','1241':'415675634','1043':'1143195511','1475':'116423768','1411':'858829294','1269':'245240853','431':'1671294892','652':'1543324176','585':'1647149314','1604':'819827984','1590':'1578716908','187':'1626276121','1208':'1107096180','668':'1965421244','1313':'750679664','1129':'242474976'}
STREET_C_NODE = {'430':'552910253','1035':'2078107280','412':'1329132133','1403':'922587542','1968':'339335164','1444':'1221389873','1183':'1812718902','1912':'132629780','1844':'438485374','1186':'1587992726','1222':'1984498433','1727':'1992232983','1522':'33713861','426':'739273303','1674':'1438865740'}
STREET_D_NODE = {'1196':'962980710','1754':'204428608','903':'219544266','912':'1671735990','1526':'777635325','1555':'1565306616','1521':'599529154','1235':'359147515','1427':'1727952741','1406':'1209379174','543':'318561886','350':'1253207672','951':'146533149','933':'370917955','1991':'517408978','864':'1370973813','975':'1736491298','1588':'578187134','1961':'138700754','352':'1414647625','1646':'1391927494','895':'1669475776','918':'1875641892','1965':'237140292','618':'1388391521','1497':'219994425','817':'1487053959','1832':'2026478004','1417':'1101533292','797':'1581539848','926':'1267889618','1276':'1390598089','1948':'1680687005','1913':'1744161708','1600':'934618834','527':'1630634994','976':'1396918184','800':'207026272','1706':'65785292','195':'1605894428','512':'1184214677','875':'209359415','836':'1649709016','1000':'981914693','1830':'421101832','1060':'878273679','927':'1326247643'}

if mode=="pdr":
    pdr_data_s = []
    pdr_data_d = []
    pdr_ms_data_s = []
    pdr_ms_data_d = []
    pdr_ps_data_s = []
    pdr_ps_data_d = []
    pdr_mr_data_s = []
    pdr_mr_data_d = []
    pdr_pr_data_s = []
    pdr_pr_data_d = []
    pdr_data_s2 = []
    pdr_data_d2 = []
    pdr_ms_data_s2 = []
    pdr_ms_data_d2 = []
    pdr_ps_data_s2 = []
    pdr_ps_data_d2 = []
    pdr_mr_data_s2 = []
    pdr_mr_data_d2 = []
    pdr_pr_data_s2 = []
    pdr_pr_data_d2 = []
    traffic_data = []
    for s in ["1.0","0.5","0.2","0.1","0.05","0.02"]:
        ss = f'results/one2one_{s}.rri100.sps.csv'
        ss2 = f'results/one2one_{s}.sps.csv'
        sd = f'results/one2one_{s}.rri100.ds.csv'
        sd2 = f'results/one2one_{s}.rri500.sps.csv'
        
        traffic_data.append(190*8/float(s)/1000000 * 2)
        genNum = 0
        receiveNum = 0
        macSendSuccessNum =0
        phySendSuccessNum = 0
        macReceiveSuccessNum =0
        phyReceiveSuccessNum=0
        with open(ss) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] != "vector":continue
                if row[1] == "vector" and row[3] == "camSentHead:vector":
                    array = re.split(" ",row[8])
                    genNum += len(array)
                elif re.split("\.",row[2])[3] == "mac" and row[3] == "sentPacketToLowerLayer:vector(packetBytes)":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 100:
                            macSendSuccessNum += 1
                elif re.split("\.",row[2])[3] == "phy" and row[3] == "tbSent:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            phySendSuccessNum += int(a)
                elif re.split("\.",row[2])[3] == "phy" and row[3] == "tbDecoded:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            phyReceiveSuccessNum += int(a)
                elif re.split("\.",row[2])[3] == "mac" and row[3] == "sentPacketToUpperLayer:vector(packetBytes)":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 100:
                            macReceiveSuccessNum += 1           
                elif row[1] == "vector" and row[3] == "CamReceived:vector":
                    array = re.split(" ",row[8])
                    receiveNum += len(array)
        pdr_data_s.append(100*receiveNum/genNum)
        pdr_ms_data_s.append(100*macSendSuccessNum/genNum)
        pdr_ps_data_s.append(100*phySendSuccessNum/genNum)
        pdr_mr_data_s.append(100*macReceiveSuccessNum/genNum)
        pdr_pr_data_s.append(100*phyReceiveSuccessNum/genNum)
        print("late:" + s )
        print("SPS_100ms, Send app:" + str(genNum) + ", mac:" + str(macSendSuccessNum) + ", phy:" + str(phySendSuccessNum)+ ", Receive app:" + str(receiveNum) + ", mac:" + str(macReceiveSuccessNum) + ", phy:" + str(phyReceiveSuccessNum))
        
        genNum = 0
        receiveNum = 0
        macSendSuccessNum =0
        phySendSuccessNum = 0
        macReceiveSuccessNum =0
        phyReceiveSuccessNum=0
        with open(sd) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] != "vector":continue
                if row[1] == "vector" and row[3] == "camSentHead:vector":
                    array = re.split(" ",row[8])
                    genNum += len(array)
                elif re.split("\.",row[2])[3] == "mac" and row[3] == "sentPacketToLowerLayer:vector(packetBytes)":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 100:
                            macSendSuccessNum += 1
                elif re.split("\.",row[2])[3] == "phy" and row[3] == "tbSent:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            phySendSuccessNum += int(a)
                elif re.split("\.",row[2])[3] == "phy" and row[3] == "tbDecoded:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            phyReceiveSuccessNum += int(a)
                elif re.split("\.",row[2])[3] == "mac" and row[3] == "sentPacketToUpperLayer:vector(packetBytes)":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 100:
                            macReceiveSuccessNum += 1           
                elif row[1] == "vector" and row[3] == "CamReceived:vector":
                    array = re.split(" ",row[8])
                    receiveNum += len(array)
        pdr_data_d.append(100*receiveNum/genNum)
        pdr_ms_data_d.append(100*macSendSuccessNum/genNum)
        pdr_ps_data_d.append(100*phySendSuccessNum/genNum)
        pdr_mr_data_d.append(100*macReceiveSuccessNum/genNum)
        pdr_pr_data_d.append(100*phyReceiveSuccessNum/genNum)
        print("DS_100ms, Send app:" + str(genNum) + ", mac:" + str(macSendSuccessNum) + ", phy:" + str(phySendSuccessNum)+ ", Receive app:" + str(receiveNum) + ", mac:" + str(macReceiveSuccessNum) + ", phy:" + str(phyReceiveSuccessNum))
        genNum = 0
        receiveNum = 0
        macSendSuccessNum =0
        phySendSuccessNum = 0
        macReceiveSuccessNum =0
        phyReceiveSuccessNum=0
        with open(ss2) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] != "vector":continue
                if row[1] == "vector" and row[3] == "camSentHead:vector":
                    array = re.split(" ",row[8])
                    genNum += len(array)
                elif re.split("\.",row[2])[3] == "mac" and row[3] == "sentPacketToLowerLayer:vector(packetBytes)":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 100:
                            macSendSuccessNum += 1
                elif re.split("\.",row[2])[3] == "phy" and row[3] == "tbSent:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            phySendSuccessNum += int(a)
                elif re.split("\.",row[2])[3] == "phy" and row[3] == "tbDecoded:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            phyReceiveSuccessNum += int(a)
                elif re.split("\.",row[2])[3] == "mac" and row[3] == "sentPacketToUpperLayer:vector(packetBytes)":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 100:
                            macReceiveSuccessNum += 1           
                elif row[1] == "vector" and row[3] == "CamReceived:vector":
                    array = re.split(" ",row[8])
                    receiveNum += len(array)
        pdr_data_s2.append(100*receiveNum/genNum)
        pdr_ms_data_s2.append(100*macSendSuccessNum/genNum)
        pdr_ps_data_s2.append(100*phySendSuccessNum/genNum)
        pdr_mr_data_s2.append(100*macReceiveSuccessNum/genNum)
        pdr_pr_data_s2.append(100*phyReceiveSuccessNum/genNum)
        print("SPS_rri10ms, Send app:" + str(genNum) + ", mac:" + str(macSendSuccessNum) + ", phy:" + str(phySendSuccessNum)+ ", Receive app:" + str(receiveNum) + ", mac:" + str(macReceiveSuccessNum) + ", phy:" + str(phyReceiveSuccessNum))
        
        genNum = 0
        receiveNum = 0
        macSendSuccessNum =0
        phySendSuccessNum = 0
        macReceiveSuccessNum =0
        phyReceiveSuccessNum=0
        with open(sd2) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] != "vector":continue
                if row[1] == "vector" and row[3] == "camSentHead:vector":
                    array = re.split(" ",row[8])
                    genNum += len(array)
                elif re.split("\.",row[2])[3] == "mac" and row[3] == "sentPacketToLowerLayer:vector(packetBytes)":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 100:
                            macSendSuccessNum += 1
                elif re.split("\.",row[2])[3] == "phy" and row[3] == "tbSent:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            phySendSuccessNum += int(a)
                elif re.split("\.",row[2])[3] == "phy" and row[3] == "tbDecoded:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            phyReceiveSuccessNum += int(a)
                elif re.split("\.",row[2])[3] == "mac" and row[3] == "sentPacketToUpperLayer:vector(packetBytes)":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 100:
                            macReceiveSuccessNum += 1           
                elif row[1] == "vector" and row[3] == "CamReceived:vector":
                    array = re.split(" ",row[8])
                    receiveNum += len(array)
        pdr_data_d2.append(100*receiveNum/genNum)
        pdr_ms_data_d2.append(100*macSendSuccessNum/genNum)
        pdr_ps_data_d2.append(100*phySendSuccessNum/genNum)
        pdr_mr_data_d2.append(100*macReceiveSuccessNum/genNum)
        pdr_pr_data_d2.append(100*phyReceiveSuccessNum/genNum)
        print("DS_10ms, Send app:" + str(genNum) + ", mac:" + str(macSendSuccessNum) + ", phy:" + str(phySendSuccessNum)+ ", Receive app:" + str(receiveNum) + ", mac:" + str(macReceiveSuccessNum) + ", phy:" + str(phyReceiveSuccessNum))

    # ==================================
    fig, ax= plt.subplots()
    ax.get_xticklabels()
    ax.plot(traffic_data,pdr_data_s,"o-",c="blue",label="sps_rri100ms")
    ax.plot(traffic_data,pdr_ps_data_s,"+:",c="blue",label="sps_rri100ms-phy")
    ax.plot(traffic_data,pdr_data_d,"o-",c="orange",label="ds_rri100ms")
    ax.plot(traffic_data,pdr_ps_data_d,"+:",c="orange",label="ds_rri100ms-phy")
    ax.plot(traffic_data,pdr_data_s2,"o-",c="aqua",label="sps_rri10ms")
    ax.plot(traffic_data,pdr_ps_data_s2,"+:",c="aqua",label="sps_rri10ms-phy")
    ax.plot(traffic_data,pdr_data_d2,"o-",c="navy",label="sps_rri500ms")
    ax.plot(traffic_data,pdr_ps_data_d2,"+:",c="navy",label="sps_rri500ms-phy")
    plt.legend()

    plt.xlabel("Traffic amount [Mbps]")
    plt.ylabel("Packet Delivery Ratio [%]")
    plt.xticks(fontsize=9)
    plt.xticks(rotation=45)
    plt.ylim(0,101)
    save = mode + "One2one"
    fig.savefig(save+"_"+option)

if mode in ["pdrIntersection","interferenceIntersection"]:
    pdr_data_s = []
    pdr_data_s2 = []
    pdr_data_s3 = []
    pdr_data_d = []
    pdr_ms_data_s = []
    pdr_ms_data_s2 = []
    pdr_ms_data_s3 = []
    pdr_ms_data_d = []
    pdr_ps_data_s = []
    pdr_ps_data_s2 = []
    pdr_ps_data_s3 = []
    pdr_ps_data_d = []
    pdr_mr_data_s = []
    pdr_mr_data_s2 = []
    pdr_mr_data_s3 = []
    pdr_mr_data_d = []
    pdr_pr_data_s = []
    pdr_pr_data_s2 = []
    pdr_pr_data_s3 = []
    pdr_pr_data_d = []
    interference_data_s = []
    interference_data_s2 = []
    interference_data_s3 = []
    interference_data_d = []
    traffic_data = []
    for s in ["1.0","0.5","0.2","0.1","0.05","0.02"]:
        ss = f'results/intersection_{s}.rri100.sps2.csv'
        ss2 = f'results/intersection_{s}.rri100.sps.csv'
        ss3 = f'results/intersection_{s}.rri500.sps.csv'
        sd = f'results/intersection_{s}.ds.csv'
        traffic_data.append(190*8/float(s)/1000000 * 79)
        genNum = 0
        receiveNum = 0
        macSendSuccessNum =0
        phySendSuccessNum = 0
        macReceiveSuccessNum =0
        phyReceiveSuccessNum=0
        interferenceNum=0
        phyReceiveNum =0
        with open(ss) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] != "vector":continue
                if row[1] == "vector" and row[3] == "camSentHead:vector":
                    array = re.split(" ",row[8])
                    genNum += len(array)
                elif re.split("\.",row[2])[3] == "mac" and row[3] == "sentPacketToLowerLayer:vector(packetBytes)":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 100:
                            macSendSuccessNum += 1
                elif re.split("\.",row[2])[3] == "phy" and row[3] == "tbSent:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            phySendSuccessNum += int(a)
                elif re.split("\.",row[2])[3] == "phy" and row[3] == "tbDecoded:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            phyReceiveSuccessNum += int(a)
                        phyReceiveNum += 1
                            
                elif re.split("\.",row[2])[3] == "mac" and row[3] == "sentPacketToUpperLayer:vector(packetBytes)":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 100:
                            macReceiveSuccessNum += 1           
                elif row[1] == "vector" and row[3] == "CamReceived:vector":
                    array = re.split(" ",row[8])
                    receiveNum += len(array)
                elif row[1] == "vector" and row[3] == "tbFailedDueToInterferenceIgnoreSCI:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            interferenceNum += int(a)

        pdr_data_s.append(100*receiveNum/genNum/79)
        pdr_ms_data_s.append(100*macSendSuccessNum/genNum)
        pdr_ps_data_s.append(100*phySendSuccessNum/genNum)
        pdr_mr_data_s.append(100*macReceiveSuccessNum/genNum/79)
        pdr_pr_data_s.append(100*phyReceiveSuccessNum/genNum/79)
        interference_data_s.append(100*interferenceNum/phyReceiveNum)
        print("late:" + s )
        if mode == "pdrIntersection":
            print("SPS_rri100ms, Send app:" + str(genNum) + ", mac:" + str(macSendSuccessNum) + ", phy:" + str(phySendSuccessNum)+ ", Receive app:" + str(receiveNum) + ", mac:" + str(macReceiveSuccessNum) + ", phy:" + str(phyReceiveSuccessNum))
        elif mode == "interferenceIntersection":
            print("SPS_rri100ms, interference:" + str(interferenceNum) + ", total receive tb:"+str(phyReceiveNum))
        genNum = 0
        receiveNum = 0
        macSendSuccessNum =0
        phySendSuccessNum = 0
        macReceiveSuccessNum =0
        phyReceiveSuccessNum=0
        interferenceNum=0
        phyReceiveNum =0
        with open(ss2) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] != "vector":continue
                if row[1] == "vector" and row[3] == "camSentHead:vector":
                    array = re.split(" ",row[8])
                    genNum += len(array)
                elif re.split("\.",row[2])[3] == "mac" and row[3] == "sentPacketToLowerLayer:vector(packetBytes)":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 100:
                            macSendSuccessNum += 1
                elif re.split("\.",row[2])[3] == "phy" and row[3] == "tbSent:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            phySendSuccessNum += int(a)
                elif re.split("\.",row[2])[3] == "phy" and row[3] == "tbDecoded:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            phyReceiveSuccessNum += int(a)
                        phyReceiveNum += 1
                elif re.split("\.",row[2])[3] == "mac" and row[3] == "sentPacketToUpperLayer:vector(packetBytes)":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 100:
                            macReceiveSuccessNum += 1           
                elif row[1] == "vector" and row[3] == "CamReceived:vector":
                    array = re.split(" ",row[8])
                    receiveNum += len(array)
                elif row[1] == "vector" and row[3] == "tbFailedDueToInterferenceIgnoreSCI:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            interferenceNum += int(a)

        pdr_data_s2.append(100*receiveNum/genNum/79)
        pdr_ms_data_s2.append(100*macSendSuccessNum/genNum)
        pdr_ps_data_s2.append(100*phySendSuccessNum/genNum)
        pdr_mr_data_s2.append(100*macReceiveSuccessNum/genNum/79)
        pdr_pr_data_s2.append(100*phyReceiveSuccessNum/genNum/79)
        interference_data_s2.append(100*interferenceNum/phyReceiveNum)
        # print("late:" + s )
        if mode == "pdrIntersection":
            print("SPS_rri10ms, Send app:" + str(genNum) + ", mac:" + str(macSendSuccessNum) + ", phy:" + str(phySendSuccessNum)+ ", Receive app:" + str(receiveNum) + ", mac:" + str(macReceiveSuccessNum) + ", phy:" + str(phyReceiveSuccessNum))
        elif mode == "interferenceIntersection":
            print("SPS_rri10ms, interference:" + str(interferenceNum) + ", total receive tb:"+str(phyReceiveNum))
        genNum = 0
        receiveNum = 0
        macSendSuccessNum =0
        phySendSuccessNum = 0
        macReceiveSuccessNum =0
        phyReceiveSuccessNum=0
        interferenceNum=0
        phyReceiveNum =0
        with open(ss3) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] != "vector":continue
                if row[1] == "vector" and row[3] == "camSentHead:vector":
                    array = re.split(" ",row[8])
                    genNum += len(array)
                elif re.split("\.",row[2])[3] == "mac" and row[3] == "sentPacketToLowerLayer:vector(packetBytes)":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 100:
                            macSendSuccessNum += 1
                elif re.split("\.",row[2])[3] == "phy" and row[3] == "tbSent:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            phySendSuccessNum += int(a)
                elif re.split("\.",row[2])[3] == "phy" and row[3] == "tbDecoded:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            phyReceiveSuccessNum += int(a)
                        phyReceiveNum += 1
                elif re.split("\.",row[2])[3] == "mac" and row[3] == "sentPacketToUpperLayer:vector(packetBytes)":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 100:
                            macReceiveSuccessNum += 1
                elif row[1] == "vector" and row[3] == "CamReceived:vector":
                    array = re.split(" ",row[8])
                    receiveNum += len(array)    
                elif row[1] == "vector" and row[3] == "tbFailedDueToInterferenceIgnoreSCI:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            interferenceNum += int(a)

        pdr_data_s3.append(100*receiveNum/genNum/79)
        pdr_ms_data_s3.append(100*macSendSuccessNum/genNum)
        pdr_ps_data_s3.append(100*phySendSuccessNum/genNum)
        pdr_mr_data_s3.append(100*macReceiveSuccessNum/genNum/79)
        pdr_pr_data_s3.append(100*phyReceiveSuccessNum/genNum/79)
        interference_data_s3.append(100*interferenceNum/phyReceiveNum)
        # print("late:" + s )
        if mode == "pdrIntersection":
            print("SPS_rri50ms, Send app:" + str(genNum) + ", mac:" + str(macSendSuccessNum) + ", phy:" + str(phySendSuccessNum)+ ", Receive app:" + str(receiveNum) + ", mac:" + str(macReceiveSuccessNum) + ", phy:" + str(phyReceiveSuccessNum))
        elif mode == "interferenceIntersection":
            print("SPS_rri50ms, interference:" + str(interferenceNum) + ", total receive tb:"+str(phyReceiveNum))
        
        genNum = 0
        receiveNum = 0
        macSendSuccessNum =0
        phySendSuccessNum = 0
        macReceiveSuccessNum =0
        phyReceiveSuccessNum=0
        interferenceNum=0
        phyReceiveNum =0
        with open(sd) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] != "vector":continue
                if row[1] == "vector" and row[3] == "camSentHead:vector":
                    array = re.split(" ",row[8])
                    genNum += len(array)
                elif re.split("\.",row[2])[3] == "mac" and row[3] == "sentPacketToLowerLayer:vector(packetBytes)":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 100:
                            macSendSuccessNum += 1
                elif re.split("\.",row[2])[3] == "phy" and row[3] == "tbSent:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            phySendSuccessNum += int(a)
                elif re.split("\.",row[2])[3] == "phy" and row[3] == "tbDecoded:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            phyReceiveSuccessNum += int(a)
                        phyReceiveNum += 1
                elif re.split("\.",row[2])[3] == "mac" and row[3] == "sentPacketToUpperLayer:vector(packetBytes)":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 100:
                            macReceiveSuccessNum += 1           
                elif row[1] == "vector" and row[3] == "CamReceived:vector":
                    array = re.split(" ",row[8])
                    receiveNum += len(array)
                elif row[1] == "vector" and row[3] == "tbFailedDueToInterferenceIgnoreSCI:vector":
                    array = re.split(" ",row[8])
                    for a in array:
                        if int(a) > 0:
                            interferenceNum += int(a)

        pdr_data_d.append(100*receiveNum/genNum/79)
        pdr_ms_data_d.append(100*macSendSuccessNum/genNum)
        pdr_ps_data_d.append(100*phySendSuccessNum/genNum)
        pdr_mr_data_d.append(100*macReceiveSuccessNum/genNum/79)
        pdr_pr_data_d.append(100*phyReceiveSuccessNum/genNum/79)
        interference_data_d.append(100*interferenceNum/phyReceiveNum)
        # print("late:" + s )
        if mode == "pdrIntersection":
            print("DS, Send app:" + str(genNum) + ", mac:" + str(macSendSuccessNum) + ", phy:" + str(phySendSuccessNum)+ ", Receive app:" + str(receiveNum) + ", mac:" + str(macReceiveSuccessNum) + ", phy:" + str(phyReceiveSuccessNum))
        elif mode == "interferenceIntersection":
            print("DS, interference:" + str(interferenceNum) + ", total receive tb:"+str(phyReceiveNum))
        
    # ==================================
    # pdr_data = []
    # pdr_ms_data = []
    # pdr_ps_data = []
    # pdr_mr_data = []
    # pdr_pr_data = []
    # interference_data = []
    # traffic_data2=[]
    # for s in ["0.05.rri500.seed1","0.05.rri500.up0.01","0.06.rri500","0.04.rri500","0.05.rri200","0.05.rri600"] :
    #     genNum = 0
    #     receiveNum = 0
    #     macSendSuccessNum =0
    #     phySendSuccessNum = 0
    #     macReceiveSuccessNum =0
    #     phyReceiveSuccessNum=0
    #     interferenceNum=0
    #     phyReceiveNum =0
    #     if s in ["0.05.rri500.seed1","0.05.rri500.up0.01","0.05.rri200","0.05.rri600"]:
    #         traffic_data2.append(190*8/0.05/1000000 * 79)
    #     elif s == "0.06.rri500":
    #         traffic_data2.append(190*8/0.06/1000000 * 79)
    #     elif s== "0.04.rri500":
    #         traffic_data2.append(190*8/0.04/1000000 * 79)
            
    #     sd=f'results/intersection_{s}.csv'
    #     with open(sd) as f:
    #         reader = csv.reader(f)
    #         for row in reader:
    #             if row[1] != "vector":continue
    #             if row[1] == "vector" and row[3] == "camSentHead:vector":
    #                 array = re.split(" ",row[8])
    #                 genNum += len(array)
    #             elif re.split("\.",row[2])[3] == "mac" and row[3] == "sentPacketToLowerLayer:vector(packetBytes)":
    #                 array = re.split(" ",row[8])
    #                 for a in array:
    #                     if int(a) > 100:
    #                         macSendSuccessNum += 1
    #             elif re.split("\.",row[2])[3] == "phy" and row[3] == "tbSent:vector":
    #                 array = re.split(" ",row[8])
    #                 for a in array:
    #                     if int(a) > 0:
    #                         phySendSuccessNum += int(a)
    #             elif re.split("\.",row[2])[3] == "phy" and row[3] == "tbDecoded:vector":
    #                 array = re.split(" ",row[8])
    #                 for a in array:
    #                     if int(a) > 0:
    #                         phyReceiveSuccessNum += int(a)
    #                     phyReceiveNum += 1
    #             elif re.split("\.",row[2])[3] == "mac" and row[3] == "sentPacketToUpperLayer:vector(packetBytes)":
    #                 array = re.split(" ",row[8])
    #                 for a in array:
    #                     if int(a) > 100:
    #                         macReceiveSuccessNum += 1           
    #             elif row[1] == "vector" and row[3] == "CamReceived:vector":
    #                 array = re.split(" ",row[8])
    #                 receiveNum += len(array)
    #             elif row[1] == "vector" and row[3] == "tbFailedDueToInterferenceIgnoreSCI:vector":
    #                 array = re.split(" ",row[8])
    #                 for a in array:
    #                     if int(a) > 0:
    #                         interferenceNum += int(a)

    #     pdr_data.append(100*receiveNum/genNum/79)
    #     pdr_ms_data.append(100*macSendSuccessNum/genNum)
    #     pdr_ps_data.append(100*phySendSuccessNum/genNum)
    #     pdr_mr_data.append(100*macReceiveSuccessNum/genNum/79)
    #     pdr_pr_data.append(100*phyReceiveSuccessNum/genNum/79)
    #     interference_data.append(100*interferenceNum/phyReceiveNum)
    #     # print("late:" + s )
    #     if mode == "pdrIntersection":
    #         print("DS, Send app:" + str(genNum) + ", mac:" + str(macSendSuccessNum) + ", phy:" + str(phySendSuccessNum)+ ", Receive app:" + str(receiveNum) + ", mac:" + str(macReceiveSuccessNum) + ", phy:" + str(phyReceiveSuccessNum))
    #     elif mode == "interferenceIntersection":
    #         print("DS, interference:" + str(interferenceNum) + ", total receive tb:"+str(phyReceiveNum))
    # print(len(pdr_data))
    # print(len(pdr_ps_data))
    # print(len(traffic_data))
    #=====================================
    fig, ax= plt.subplots()
    ax.get_xticklabels()
    if mode == "pdrIntersection":
        ax.plot(traffic_data,pdr_data_s,"o-",c="aqua",label="sps-100ms")
        ax.plot(traffic_data,pdr_ps_data_s,":",c="aqua",label="sps-100ms-phy")
        ax.plot(traffic_data,pdr_data_s2,"o-",c="blue",label="sps-10ms")
        ax.plot(traffic_data,pdr_ps_data_s2,":",c="blue",label="sps-10ms-phy")
        ax.plot(traffic_data,pdr_data_s3,"o-",c="navy",label="sps-50ms")
        ax.plot(traffic_data,pdr_ps_data_s3,":",c="navy",label="sps-50ms-phy")
        ax.plot(traffic_data,pdr_data_d,"o-",c="orange",label="ds")
        ax.plot(traffic_data,pdr_ps_data_d,":",c="orange",label="ds-phy")
        # ax2 = ax.twinx().twiny()
        # ax.scatter(traffic_data2,pdr_data,marker="^") #
        # ax.scatter(traffic_data2,pdr_ps_data,marker="^")
    elif mode == "interferenceIntersection":
        ax.plot(traffic_data,interference_data_s,"o-",c="aqua",label="sps-100ms")
        ax.plot(traffic_data,interference_data_s2,"o-",c="blue",label="sps-10ms")
        ax.plot(traffic_data,interference_data_s3,"o-",c="navy",label="sps-50ms")
        ax.plot(traffic_data,interference_data_d,"o-",c="orange",label="ds")
        # ax2 = ax.twinx().twiny()
        # ax.scatter(traffic_data2,interference_data,marker="^")
    plt.legend()
    plt.xlabel("Traffic amount [Mbps]")
    if mode == "pdrIntersection":
        plt.ylabel("Packet Delivery Ratio [%]")
    elif mode == "interferenceIntersection":
        plt.ylabel("Packet Collision Ratio [%]")
    
    plt.xticks(fontsize=9)
    plt.xticks(rotation=45)
    plt.ylim(0,101)
    save = mode
    fig.savefig(save+"_"+option)


if mode=="grantRequest":
    count = 0
    count2 = 0
    count_1 = 0
    count2_1 = 0
    count_2 = 0
    count2_2 = 0
    count_3 = 0
    count2_3 = 0
    
    with open(ss) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "scalar" and row[3]=="tbFailedDueToInterference:sum":
                count += int(row[6])
            if row[1] == "scalar" and row[3]=="tbFailedDueToInterference:sum":
                count += int(row[6])
            if row[1] == "scalar" and row[3]=="tbFailedDueToInterference:sum":
                count += int(row[6])
        
    with open(sd) as f:      
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "scalar" and row[3]=="tbFailedDueToInterference:sum":
                count2 += int(row[6])
    print("count:" + str(count) + ", count2:" + str(count2))       
                

# Packet Delivery Ratio ===================================
def parse_if_number(s):
    try: return float(s)
    except: return True if s=="true" else False if s=="false" else s if s else None

def parse_ndarray(s):
    return np.fromstring(s, sep=' ') if s else None

Pdr_Distance_Distances = []

def make_pdrs(csv_s, pdr_vector, isDistances):
    pdrs = []
    df = pd.read_csv(csv_s, converters = {
        'attrvalue': parse_if_number,
        'binedges': parse_ndarray,
        'binvalues': parse_ndarray,
        'vectime': parse_ndarray,
        'vecvalue': parse_ndarray})

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
    distance = 0
    for dictionary in bins:
        try:
            pdrs.append((dictionary["success"] / dictionary["count"] * 100))
        except ZeroDivisionError:
            pdrs.append(0)
        if(isDistances):
            Pdr_Distance_Distances.append(distance)
            distance += 10
    return pdrs


if mode in ["pdrDistance", "0", "1","2"]:
    save = mode
    l =""
    yl = ""
    csv_s10 ="results/intersection_sps_rri100.csv"
    csv_s50 ="results/intersection_pro_rri100.csv"
    csv_s100 ="results/intersection_pro1.1_rri100.csv"
    csv_d = 'results/intersection_0.2.ds.csv'
    pdr_vector = ""
    if mode=="pdrDistance":
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
    pdr10=make_pdrs(csv_s10,pdr_vector,True)
    pdr50=make_pdrs(csv_s50,pdr_vector,False)
    pdr100=make_pdrs(csv_s100,pdr_vector,False)
    pdrD=make_pdrs(csv_d,pdr_vector,False)
    
    
    fig, ax = plt.subplots()
        

    ax.plot(Pdr_Distance_Distances, pdr10,"o-", label="sps,rri=300ms",c="blue")
    ax.plot(Pdr_Distance_Distances, pdr50,"o-", label="pro1",c="navy")
    ax.plot(Pdr_Distance_Distances, pdr100,"o-", label="pro1.1",c="aqua")
    # ax.plot(Pdr_Distance_Distances, pdrD,"o-", label="ds",c="orange")
    



    ax.set(xlabel='Distance (m)', ylabel=yl)
    ax.legend(loc="lower left")
    ax.tick_params(direction='in')
    ax.set_xlim([0, (max(Pdr_Distance_Distances) + 1)])
    # ax.set_ylim([0, 101])
    plt.xticks(np.arange(0, (max(Pdr_Distance_Distances))+50, step=50))
    plt.yticks(np.arange(0, (101), step=10))



    plt.savefig(save+"_"+option, dpi=300)
     
