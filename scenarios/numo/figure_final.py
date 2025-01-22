import sys
import csv
import pprint
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import math
import seaborn as sns
from matplotlib import rcParams
rcParams['pdf.fonttype'] = 42

OVER_SIZE_LIMIT = 200_000_000

csv.field_size_limit(OVER_SIZE_LIMIT)

args = sys.argv
mode = "" # evaluation mode
option="" # label ex) option="test" => mode_test.png
ss = "./results/sps_smooth2_rri100.csv" #file 1
sd = "./results/ds_smooth2.csv" #file 2
s_c_a = "./results/intersection_a_sps.csv"
s_c_b = "./results/intersection_b_sps.csv"
s_c_c = "./results/street_c_sps.csv"
s_c_d = "./results/street_d_sps.csv"
s_c_a2 = "./results/intersection_a_pro.csv"
s_c_b2 = "./results/intersection_b_pro.csv"
s_c_c2 = "./results/street_c_pro.csv"
s_c_d2 = "./results/street_d_pro.csv"
INTERSECTION_A_NODE = {'430':'552910253','294':'2025187190','1196':'962980710','950':'1287726651','1920':'1921376925','985':'2135019593','1035':'2078107280','412':'1329132133','1788':'1945891638','466':'1144522535','1754':'204428608','572':'1376035217','903':'219544266','1403':'922587542','912':'1671735990','834':'670752506','1220':'1690492373','1023':'610486506','1444':'1221389873','1555':'1565306616','395':'114723506','494':'1402961682','456':'559301039','502':'1941690360','543':'318561886','1517':'703955951','350':'1253207672','1931':'995097051','951':'146533149','332':'1797073940','1991':'517408978','864':'1370973813','1879':'346502533','1588':'578187134','1961':'138700754','835':'2025554010','1418':'1069117832','352':'1414647625','895':'1669475776','918':'1875641892','1186':'1587992726','1268':'1947691087','1314':'1569115921','1965':'237140292','1594':'87522686','1222':'1984498433','1924':'1320634492','1435':'419914800','1582':'263043320','817':'1487053959','1832':'2026478004','1636':'940472515','797':'1581539848','1816':'1386214636','1120':'318322042','926':'1267889618','426':'739273303','1221':'1111800030','1276':'1390598089','1948':'1680687005','935':'772634225','1182':'1926411641','1258':'692981712','1562':'354367395','1294':'1256273378','512':'1184214677','1433':'1989200801','1674':'1438865740','2081':'1758204253'}
INTERSECTION_B_NODE = {'315':'1469262009','1935':'2070707654','929':'1663080928','774':'628966950','254':'1308044878','1912':'132629780','1833':'1659239833','356':'1896306640','128':'1610120709','100':'1036140795','1090':'1607774548','967':'413360099','1005':'12548159','83':'1889947178','1117':'1903409954','1241':'415675634','1043':'1143195511','1475':'116423768','1411':'858829294','1269':'245240853','431':'1671294892','652':'1543324176','585':'1647149314','1604':'819827984','1590':'1578716908','187':'1626276121','1208':'1107096180','668':'1965421244','1313':'750679664','1129':'242474976'}
STREET_C_NODE = {'430':'552910253','1035':'2078107280','412':'1329132133','1403':'922587542','1968':'339335164','1444':'1221389873','1183':'1812718902','1912':'132629780','1844':'438485374','1186':'1587992726','1222':'1984498433','1727':'1992232983','1522':'33713861','426':'739273303','1674':'1438865740'}
STREET_D_NODE = {'1196':'962980710','1754':'204428608','903':'219544266','912':'1671735990','1526':'777635325','1555':'1565306616','1521':'599529154','1235':'359147515','1427':'1727952741','1406':'1209379174','543':'318561886','350':'1253207672','951':'146533149','933':'370917955','1991':'517408978','864':'1370973813','975':'1736491298','1588':'578187134','1961':'138700754','352':'1414647625','1646':'1391927494','895':'1669475776','918':'1875641892','1965':'237140292','618':'1388391521','1497':'219994425','817':'1487053959','1832':'2026478004','1417':'1101533292','797':'1581539848','926':'1267889618','1276':'1390598089','1948':'1680687005','1913':'1744161708','1600':'934618834','527':'1630634994','976':'1396918184','800':'207026272','1706':'65785292','195':'1605894428','512':'1184214677','875':'209359415','836':'1649709016','1000':'981914693','1830':'421101832','1060':'878273679','927':'1326247643'}

INTERSECTION_A_NODE_P = {'846': '11671338', '581': '1826620483', '962': '646755199', '1568': '1693485026', '335': '719346228', '400': '255789528', '1208': '1107096180', '937': '813274570', '297': '437116466', '914': '305197314', '1801': '547772603', '519': '1276673168', '1338': '763148569', '461': '1739000681', '1607': '1813511382', '1829': '1478705400', '1280': '573666704', '472': '777720504', '1034': '1289360871', '1892': '1443145325', '1845': '1798027458', '961': '1238498976', '1447': '2133584523', '1933': '20336956', '1649': '1967632854', '845': '931489114', '1234': '272312086', '1132': '1172063133', '356': '1896306640', '1445': '1173002606', '1530': '1073781763', '1937': '102194872', '828': '245798898', '1415': '192048860', '1575': '1793256508', '1767': '1815754673', '1046': '2058907361', '501': '1450956042', '1595': '1098193842', '1457': '1017565625', '1288': '703571522', '354': '1046741222', '929': '1663080928', '1233': '1698487330', '946': '856363827', '906': '428903682', '431': '1671294892', '923': '1745897490', '417': '212251746', '1326': '1219933931', '435': '474613996', '2054': '868563557', '808': '1603591171', '1974': '861746410', '1270': '100669', '1232': '1122551742', '1430': '1281944976', '509': '2002495425', '996': '1446648412', '1601': '2078480869', '1687': '978053418', '1961': '138700754', '1978': '2124149955', '875': '209359415', '1198': '649785905', '1306': '1286966948', '1944': '1889537797', '551': '1051858969', '1194': '461152493', '2094': '294402375'}
INTERSECTION_B_NODE_P = {'1129': '242474976', '436': '425245975', '677': '1959343768', '940': '699460008', '978': '376696776', '1617': '1917305981', '318': '1295166342', '785': '525829204', '1925': '1304438548', '1141': '773446912', '1220': '1690492373', '1102': '18400960', '101': '463480570', '594': '394633074', '360': '1197352298', '257': '705178736', '1846': '315813605', '1948': '1680687005', '129': '791698927', '1016': '737703662', '84': '1780695788', '1488': '493886463', '1603': '196095815', '1253': '1386510139', '189': '2130794395', '1054': '394709364', '1423': '627510635', '1325': '1987106312', '1281': '933596911', '661': '488663950'}
STREET_C_NODE_P = {'1195': '597010431', '1857': '701943705', '1535': '461851014', '1925': '1304438548', '1234': '272312086', '1981': '405341089', '1415': '192048860', '1046': '2058907361', '1457': '1017565625', '431': '1671294892', '417': '212251746', '435': '474613996', '1740': '1004011520', '1687': '978053418', '1198': '649785905'}
STREET_D_NODE_P = {'962': '646755199', '1568': '1693485026', '1208': '1107096180', '534': '1708302647', '937': '813274570', '914': '305197314', '519': '1276673168', '1539': '1773595097', '1926': '2042830296', '1534': '1457880381', '1845': '1798027458', '1510': '1175989877', '1659': '616716465', '356': '1896306640', '828': '245798898', '1767': '1815754673', '1247': '1456339643', '1288': '703571522', '1843': '37623446', '1071': '825726814', '354': '1046741222', '929': '1663080928', '906': '428903682', '938': '1390543437', '923': '1745897490', '1439': '457676440', '2054': '868563557', '987': '1434322197', '808': '1603591171', '1974': '861746410', '944': '1730418657', '1601': '2078480869', '1961': '138700754', '1418': '1069117832', '1978': '2124149955', '875': '209359415', '1011': '1402492972', '1429': '1364180570', '811': '2013725218', '847': '1395405989', '197': '1987231011', '1613': '1731563037', '627': '738393740', '551': '1051858969', '986': '1151297278', '886': '1078898506', '1719': '1322710936'}


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

def make_senderID(s,data):
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == "senderID:vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                data[vehicle] = {}
                for i in range(len(array)):
                    data[vehicle][times[i]]=str(int(array[i])-1025)
    
def make_timerange(sa,sb,sc,sd,data):
    index = 0
    for s in [sa,sb,sc,sd]:
        with open(s) as f:
            reader = csv.reader(f)
            for row in reader:
                node = str(row[1])
                if node in data[index]:
                    if data[index][node][1] < float(row[2]):
                        data[index][node][1] = float(row[2])
                else:
                    data[index][node] = [float(row[2]),float(row[2])]
        index += 1

def data_tbSent(row,x_data,NODE,timeRange,startTime,span):
    if row[1] == "vector" and row[3] == "tbSent:vector":
        vehicle = re.split("[\[\]]",row[2])[1]
        times = re.split(" ",row[7])
        array = re.split(" ",row[8])
        for j in range(len(times)):
            # 時間内のものだけを入れる
            if (vehicle in NODE[0].keys() 
                and float(times[j]) >= timeRange[0][vehicle][0] 
                and float(times[j]) <= timeRange[0][vehicle][1] + 0.2):
                x_data[0][int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

            if (vehicle in NODE[1].keys() 
                and float(times[j]) >= timeRange[1][vehicle][0] 
                and float(times[j]) <= timeRange[1][vehicle][1] + 0.2):
                x_data[1][int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

            if (vehicle in NODE[2].keys() 
                and float(times[j]) >= timeRange[2][vehicle][0] 
                and float(times[j]) <= timeRange[2][vehicle][1] + 0.2):
                x_data[2][int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

            if (vehicle in NODE[3].keys() 
                and float(times[j]) >= timeRange[3][vehicle][0] 
                and float(times[j]) <= timeRange[3][vehicle][1] + 0.2):
                x_data[3][int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])
    


def make_traffic_pdr(s,timeRange,y_decode_data,y_total_data,x_data,senderID,NODE,startTime,span):
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            #対象外の車はcontinue
            if row[1] == "vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                if vehicle not in NODE[0].keys() and vehicle not in NODE[1].keys() and vehicle not in NODE[2].keys() and vehicle not in NODE[3].keys():
                    continue
            # if row[1] == "vector" and row[3] == "tbSent:vector":
            #     vehicle = re.split("[\[\]]",row[2])[1]
            #     times = re.split(" ",row[7])
            #     array = re.split(" ",row[8])
            #     for j in range(len(times)):
            #         # 時間内のものだけを入れる
            #         if (vehicle in NODE[0].keys() 
            #             and float(times[j]) >= timeRange[0][vehicle][0] 
            #             and float(times[j]) <= timeRange[0][vehicle][1] + 0.2):
            #             x_data[0][int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

            #         if (vehicle in NODE[1].keys() 
            #             and float(times[j]) >= timeRange[1][vehicle][0] 
            #             and float(times[j]) <= timeRange[1][vehicle][1] + 0.2):
            #             x_data[1][int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

            #         if (vehicle in NODE[2].keys() 
            #             and float(times[j]) >= timeRange[2][vehicle][0] 
            #             and float(times[j]) <= timeRange[2][vehicle][1] + 0.2):
            #             x_data[2][int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])

            #         if (vehicle in NODE[3].keys() 
            #             and float(times[j]) >= timeRange[3][vehicle][0] 
            #             and float(times[j]) <= timeRange[3][vehicle][1] + 0.2):
            #             x_data[3][int((float(times[j]) - startTime) / span)] += 190 * 8 / span * int(array[j])
            data_tbSent(row,x_data,NODE,timeRange,startTime,span)
            if row[1] == "vector" and row[3] == "tbDecoded:vector":
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    # 時間内のものだけを入れる
                    
                    index = 0
                    if vehicle in NODE[0].keys() and float(times[j]) >= timeRange[0][vehicle][0] and float(times[j]) <= timeRange[0][vehicle][1]+0.2 and senderID[vehicle][times[j]] in NODE[0].keys():
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data[0][index] = (y_decode_data[0][index]*y_total_data[0][index] + int(float(array[j])))/(y_total_data[0][index]+1)
                        y_total_data[0][index] += 1
                    if vehicle in NODE[1].keys() and float(times[j]) >= timeRange[1][vehicle][0] and float(times[j]) <= timeRange[1][vehicle][1]+0.2 and senderID[vehicle][times[j]] in NODE[1].keys():
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data[1][index] = (y_decode_data[1][index]*y_total_data[1][index] + int(float(array[j])))/(y_total_data[1][index]+1)
                        y_total_data[1][index] += 1
                    if vehicle in NODE[2].keys() and float(times[j]) >= timeRange[2][vehicle][0] and float(times[j]) <= timeRange[2][vehicle][1]+0.2 and senderID[vehicle][times[j]] in NODE[2].keys():
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data[2][index] = (y_decode_data[2][index]*y_total_data[2][index] + int(float(array[j])))/(y_total_data[2][index]+1)
                        y_total_data[2][index] += 1
                    if vehicle in NODE[3].keys() and float(times[j]) >= timeRange[3][vehicle][0] and float(times[j]) <= timeRange[3][vehicle][1]+0.2 and senderID[vehicle][times[j]] in NODE[3].keys():
                        index = int((float(times[j])-startTime)/span)
                        y_decode_data[3][index] = (y_decode_data[3][index]*y_total_data[3][index] + int(float(array[j])))/(y_total_data[3][index]+1)
                        y_total_data[3][index] += 1
           

def make_data(x_data,x_value,y_decode_data,y_total_data,y_data):
    for i in range(4):
        sorted_items_by_value = sorted(x_data[i].items(), key=lambda item: item[1])
        x_sorted = {k: v for k, v in sorted_items_by_value}
        for k, v in x_sorted.items():
            x_value[i].append(float(v))
        for k in x_sorted.keys():
            y_data[i].append(y_decode_data[i][k]*100.0)
            print("decode rate:"+str(y_decode_data[i][k]*100.0)+", total receive:" + str(y_total_data[i][k]))
        print("分散:" + str(np.var(y_data[i])))

def count_el(s,target,timeRange,NODE):
    count_i=0
    count_i2=0
    count_s=0
    count_s2=0
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == target:
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    if (vehicle in NODE[0].keys()
                        and float(times[j]) >= timeRange[0][vehicle][0] 
                        and float(times[j]) <= timeRange[0][vehicle][1] + 0.2):
                        count_i += int(array[j])
                    if (vehicle in NODE[1].keys()
                        and float(times[j]) >= timeRange[1][vehicle][0] 
                        and float(times[j]) <= timeRange[1][vehicle][1] + 0.2):
                        count_i2 += int(array[j])
                    if (vehicle in NODE[2].keys()
                        and float(times[j]) >= timeRange[2][vehicle][0] 
                        and float(times[j]) <= timeRange[2][vehicle][1] + 0.2):
                        count_s += int(array[j])
                    if (vehicle in NODE[3].keys()
                        and float(times[j]) >= timeRange[3][vehicle][0] 
                        and float(times[j]) <= timeRange[3][vehicle][1] + 0.2):
                        count_s2 += int(array[j])
    print(s)
    print(f'target is {target}')
    print("count i:" + str(count_i) + ", count i2:" + str(count_i2) + ", count s:" + str(count_s) + ", count s2:" + str(count_s2))
    return [count_i,count_i2,count_s,count_s2]
def count_el_by_length(s,target,timeRange,NODE):
    count_i=0
    count_i2=0
    count_s=0
    count_s2=0
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == target:
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    if (vehicle in NODE[0].keys()
                        and float(times[j]) >= timeRange[0][vehicle][0] 
                        and float(times[j]) <= timeRange[0][vehicle][1] + 0.2):
                        count_i += 1
                        # if vehicle == '430':
                            # print("a,"+times[j] + "," + array[j])
                    if (vehicle in NODE[1].keys()
                        and float(times[j]) >= timeRange[1][vehicle][0] 
                        and float(times[j]) <= timeRange[1][vehicle][1] + 0.2):
                        count_i2 += 1
                        # if vehicle == '430':
                            # print("b,"+times[j] + "," + array[j])
                    if (vehicle in NODE[2].keys()
                        and float(times[j]) >= timeRange[2][vehicle][0] 
                        and float(times[j]) <= timeRange[2][vehicle][1] + 0.2):
                        count_s += 1
                        # if vehicle == '430':
                            # print("c,"+times[j] + "," + array[j])
                    if (vehicle in NODE[3].keys()
                        and float(times[j]) >= timeRange[3][vehicle][0] 
                        and float(times[j]) <= timeRange[3][vehicle][1] + 0.2):
                        count_s2 += 1
                        # if vehicle == '430':
                            # print("d,"+times[j] + "," + array[j])
    print(s)
    print(f'target is {target}')
    print("count i:" + str(count_i) + ", count i2:" + str(count_i2) + ", count s:" + str(count_s) + ", count s2:" + str(count_s2))
    return [count_i,count_i2,count_s,count_s2]
def count_el_and_total(s,target,timeRange,NODE):
    count_i=0
    count_i2=0
    count_s=0
    count_s2=0
    total=[0,0,0,0]
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == target:
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    if (vehicle in NODE[0].keys()
                        and float(times[j]) >= timeRange[0][vehicle][0] 
                        and float(times[j]) <= timeRange[0][vehicle][1] + 0.2):
                        count_i += int(array[j])
                        total[0] += 1
                    if (vehicle in NODE[1].keys()
                        and float(times[j]) >= timeRange[1][vehicle][0] 
                        and float(times[j]) <= timeRange[1][vehicle][1] + 0.2):
                        count_i2 += int(array[j])
                        total[1]+=1
                    if (vehicle in NODE[2].keys()
                        and float(times[j]) >= timeRange[2][vehicle][0] 
                        and float(times[j]) <= timeRange[2][vehicle][1] + 0.2):
                        count_s += int(array[j])
                        total[2]+=1
                    if (vehicle in NODE[3].keys()
                        and float(times[j]) >= timeRange[3][vehicle][0] 
                        and float(times[j]) <= timeRange[3][vehicle][1] + 0.2):
                        count_s2 += int(array[j])
                        total[3]+=1
    print(s)
    print(f'target is {target}')
    print("count i:" + str(count_i) + ", count i2:" + str(count_i2) + ", count s:" + str(count_s) + ", count s2:" + str(count_s2))
    print("total i:" + str(total[0]) + ", total i2:" + str(total[1]) + ", total s:" + str(total[2]) + ", total s2:" + str(total[3]))
    return [[count_i,total[0]],[count_i2,total[1]],[count_s,total[2]],[count_s2,total[3]]]
def count_el_and_total_d(s,target,timeRange,NODE,senderID):
    count_i=0
    count_i2=0
    count_s=0
    count_s2=0
    total=[0,0,0,0]
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == target:
                vehicle = re.split("[\[\]]",row[2])[1]
                times = re.split(" ",row[7])
                array = re.split(" ",row[8])
                for j in range(len(times)):
                    if (vehicle in NODE[0].keys()
                        and float(times[j]) >= timeRange[0][vehicle][0] 
                        and float(times[j]) <= timeRange[0][vehicle][1] + 0.2
                        and senderID[vehicle][times[j]] in NODE[0].keys()):
                        count_i += int(array[j])
                        total[0] += 1
                    if (vehicle in NODE[1].keys()
                        and float(times[j]) >= timeRange[1][vehicle][0] 
                        and float(times[j]) <= timeRange[1][vehicle][1] + 0.2
                        and senderID[vehicle][times[j]] in NODE[1].keys()):
                        count_i2 += int(array[j])
                        total[1]+=1
                    if (vehicle in NODE[2].keys()
                        and float(times[j]) >= timeRange[2][vehicle][0] 
                        and float(times[j]) <= timeRange[2][vehicle][1] + 0.2
                        and senderID[vehicle][times[j]] in NODE[2].keys()):
                        count_s += int(array[j])
                        total[2]+=1
                    if (vehicle in NODE[3].keys()
                        and float(times[j]) >= timeRange[3][vehicle][0] 
                        and float(times[j]) <= timeRange[3][vehicle][1] + 0.2
                        and senderID[vehicle][times[j]] in NODE[3].keys()):
                        count_s2 += int(array[j])
                        total[3]+=1
    print(s)
    print(f'target is {target}')
    print("count i:" + str(count_i) + ", count i2:" + str(count_i2) + ", count s:" + str(count_s) + ", count s2:" + str(count_s2))
    print("total i:" + str(total[0]) + ", total i2:" + str(total[1]) + ", total s:" + str(total[2]) + ", total s2:" + str(total[3]))
    return [[count_i,total[0]],[count_i2,total[1]],[count_s,total[2]],[count_s2,total[3]]]


def data_tbSent_node(row,x_data,NODE,timeRange):
    if row[1] == "vector" and row[3] == "tbSent:vector":
        vehicle = re.split("[\[\]]",row[2])[1]
        times = re.split(" ",row[7])
        array = re.split(" ",row[8])    
        for j in range(len(times)):
            # 時間内のものだけを入れる
            if (vehicle in NODE[0].keys() 
                and float(times[j]) >= timeRange[0][vehicle][0] 
                and float(times[j]) <= timeRange[0][vehicle][1] + 0.2):
                if vehicle not in x_data[0]:
                    x_data[0][vehicle] = []
                x_data[0][vehicle].append(float(times[j]))

            if (vehicle in NODE[1].keys() 
                and float(times[j]) >= timeRange[1][vehicle][0] 
                and float(times[j]) <= timeRange[1][vehicle][1] + 0.2):
                if vehicle not in x_data[1]:
                    x_data[1][vehicle] = []
                x_data[1][vehicle].append(float(times[j]))

            if (vehicle in NODE[2].keys() 
                and float(times[j]) >= timeRange[2][vehicle][0] 
                and float(times[j]) <= timeRange[2][vehicle][1] + 0.2):
                if vehicle not in x_data[2]:
                    x_data[2][vehicle] = []
                x_data[2][vehicle].append(float(times[j]))

            if (vehicle in NODE[3].keys() 
                and float(times[j]) >= timeRange[3][vehicle][0] 
                and float(times[j]) <= timeRange[3][vehicle][1] + 0.2):
                if vehicle not in x_data[3]:
                    x_data[3][vehicle] = []
                x_data[3][vehicle].append(float(times[j]))

def data_subchannel(row,x_data,NODE,timeRange):
    if row[1] == "vector" and row[3] == "subchannelSent:vector":
        vehicle = re.split("[\[\]]",row[2])[1]
        times = re.split(" ",row[7])
        array = re.split(" ",row[8])    
        for j in range(len(times)):
            # 時間内のものだけを入れる
            if (vehicle in NODE[0].keys() 
                and float(times[j]) >= timeRange[0][vehicle][0] 
                and float(times[j]) <= timeRange[0][vehicle][1] + 0.2):
                if vehicle not in x_data[0]:
                    x_data[0][vehicle] = []
                x_data[0][vehicle].append(int(array[j]))

            if (vehicle in NODE[1].keys() 
                and float(times[j]) >= timeRange[1][vehicle][0] 
                and float(times[j]) <= timeRange[1][vehicle][1] + 0.2):
                if vehicle not in x_data[1]:
                    x_data[1][vehicle] = []
                x_data[1][vehicle].append(int(array[j]))

            if (vehicle in NODE[2].keys() 
                and float(times[j]) >= timeRange[2][vehicle][0] 
                and float(times[j]) <= timeRange[2][vehicle][1] + 0.2):
                if vehicle not in x_data[2]:
                    x_data[2][vehicle] = []
                x_data[2][vehicle].append(int(array[j]))

            if (vehicle in NODE[3].keys() 
                and float(times[j]) >= timeRange[3][vehicle][0] 
                and float(times[j]) <= timeRange[3][vehicle][1] + 0.2):
                if vehicle not in x_data[3]:
                    x_data[3][vehicle] = []
                x_data[3][vehicle].append(int(array[j]))



def make_resourceMargin(x_data,y_data,NODE,timeRange,simTime,startTime):
    resource_data =[]
    resource_node_data=[]
    for i in range(3):
        resource_data.append([])
        resource_node_data.append([])
        for j in range(simTime*1000+1):
            resource_data[i].append(0)
            resource_node_data[i].append([])

    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            data_tbSent_node(row,x_data,NODE,timeRange)
            data_subchannel(row,y_data,NODE,timeRange)
    for road_i in range(len(x_data)):
        for v in x_data[road_i]:
            for i in range(len(x_data[road_i][v])):
                # print("check")
                # print(road_i)
                # print(v)
                # print(i)
                # print(x_data[road_i])
                # print(int((x_data[road_i][v][i]-startTime)*1000))
                
                resource_data[y_data[road_i][v][i]][int((x_data[road_i][v][i]-startTime)*1000)] += 1
                resource_node_data[y_data[road_i][v][i]][int((x_data[road_i][v][i]-startTime)*1000)].append(v)

    count_overlap = 0
    count_margin =0
    for i in range(3):
        for j in range(simTime*1000+1):
            if resource_data[i][j] ==0:
                count_margin +=1
            elif resource_data[i][j] >1:
                count_overlap += 1
    # for j in range(simTime*1000+1):
        # print(f'{resource_node_data[0][j]} \t {resource_node_data[1][j]} \t {resource_node_data[2][j]}')    

    print(f'\nTotal:{3*simTime*1000}, Overlap:{count_overlap}, Margin:{count_margin}')

def make_resourceMargin_simple(x_data,y_data,NODE,timeRange,simTime,startTime):
    resource_data =[]
    resource_node_data=[]
    for i in range(3):
        resource_data.append([])
        resource_node_data.append([])
        for j in range(simTime*1000+1):
            resource_data[i].append(0)
            resource_node_data[i].append([])

    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            data_tbSent_node(row,x_data,NODE,timeRange)
            data_subchannel(row,y_data,NODE,timeRange)
    # range is 1
    for road_i in range(1):
        for v in x_data[road_i]:
            for i in range(len(x_data[road_i][v])):
                # print("check")
                # print(road_i)
                # print(v)
                # print(i)
                # print(x_data[road_i])
                # print(int((x_data[road_i][v][i]-startTime)*1000))
                
                resource_data[y_data[road_i][v][i]][int((x_data[road_i][v][i]-startTime)*1000)] += 1
                resource_node_data[y_data[road_i][v][i]][int((x_data[road_i][v][i]-startTime)*1000)].append(v)

    count_overlap = 0
    count_margin =0
    for i in range(3):
        for j in range(simTime*1000+1):
            if resource_data[i][j] ==0:
                count_margin +=1
            elif resource_data[i][j] >1:
                count_overlap += 1
    for j in range(simTime*1000+1):
        print(f'{resource_node_data[0][j]} \t {resource_node_data[1][j]} \t {resource_node_data[2][j]}')    

    print(f'\nTotal:{3*simTime*1000}, Overlap:{count_overlap}, Margin:{count_margin}')


def makeNodes(s,NODE):
    with open(s) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == "camVehicleId:vector":
                id = re.split(" ",row[8])[0]
                vehicle = re.split("[\[\]]",row[2])[1]
                NODE[vehicle]=id


def show_index(current, previous):
    diff = (current - previous)*100
    return int(diff//100)-1

def make_interval_simple(x_data,y_data,s):
    with open(s) as f:
        reader=csv.reader(f)
        for row in reader:
            if row[1] == "vector" and row[3] == "camSentHead:vector":
                times = re.split(" ",row[7])
                previous = float(times[0])
                for i in range(1,len(times)):
                    y_data[show_index(float(times[i]),previous)] +=1
                    previous = float(times[i])   
                
        



if mode == "traffic_pdr":
    ss = "./results/pro3.0_smooth2.csv"
    ss2 = "./results/sps_smooth2_rri100.csv"
    span = 5
    if len(args)>=6:
        span = float(args[5])
    startTime = 28800.0
    simTime = 30
    senderID={}
    x_data={}
    y_decode_data={}
    y_total_data={}
    x_result={}
    y_result = {}
    NODE = {}
    timeRange={}
    fig, ax = plt.subplots()
    for s in [ss,ss2,sd]:
        senderID[s] = {}
        timeRange[s]=[{},{},{},{}]
        if "pro" in s:
            NODE[s]=[INTERSECTION_A_NODE_P,INTERSECTION_B_NODE_P,STREET_C_NODE_P,STREET_D_NODE_P]
            make_timerange(s_c_a2,s_c_b2,s_c_c2,s_c_d2,timeRange[s])
        else:
            NODE[s]=[INTERSECTION_A_NODE,INTERSECTION_B_NODE,STREET_C_NODE,STREET_D_NODE]
            make_timerange(s_c_a,s_c_b,s_c_c,s_c_d,timeRange[s])
        make_senderID(s,senderID[s])
        # print(senderID[s])
        x_data[s] = [{},{},{},{}]
        x_result[s]=[[],[],[],[]]
        y_decode_data[s]=[[],[],[],[]]
        y_total_data[s]=[[],[],[],[]]
        y_result[s]=[[],[],[],[]]

        for i in range(4) : 
            for j in range(int(simTime/span)+1):  
                x_data[s][i][j] = 0.0
                y_decode_data[s][i].append(0.0)
                y_total_data[s][i].append(0)
        
        make_traffic_pdr(s,timeRange[s],y_decode_data[s],y_total_data[s],x_data[s],senderID[s],NODE[s],startTime,span)
        print(s)
        make_data(x_data[s],x_result[s],y_decode_data[s],y_total_data[s],y_result[s])

    ax.scatter(x_result[ss][0][1:], y_result[ss][0][1:], marker="o", c="blue",label="Proposal_a")
    ax.scatter(x_result[ss2][0][1:], y_result[ss2][0][1:], marker="+", c="deepskyblue",label="SB-SPS_a")
    ax.scatter(x_result[sd][0][1:], y_result[sd][0][1:],marker="x", c="aqua",label="DS_a")
    ax.scatter(x_result[ss][1][1:], y_result[ss][1][1:], marker="o", c="green",label="Proposal_b")
    ax.scatter(x_result[ss2][1][1:], y_result[ss2][1][1:], marker="+", c="lawngreen",label="SB-SPS_b")
    ax.scatter(x_result[sd][1][1:], y_result[sd][1][1:],marker="x", c="palegreen",label="DS_b")
    ax.scatter(x_result[ss][2][1:], y_result[ss][2][1:], marker="o", c="red",label="Proposal_c")
    ax.scatter(x_result[ss2][2][1:], y_result[ss2][2][1:], marker="+", c="deeppink",label="SB-SPS_c")
    ax.scatter(x_result[sd][2][1:], y_result[sd][2][1:],marker="x", c="violet",label="DS_c")
    ax.scatter(x_result[ss][3][1:], y_result[ss][3][1:], marker="o", c="orange",label="Proposal_d")
    ax.scatter(x_result[ss2][3][1:], y_result[ss2][3][1:], marker="+", c="gold",label="SB-SPS_d")
    ax.scatter(x_result[sd][3][1:], y_result[sd][3][1:],marker="x", c="yellow",label="DS_d")
    ax.plot(x_result[ss][0][1:], np.poly1d(np.polyfit(x_result[ss][0][1:], y_result[ss][0][1:], 1))(x_result[ss][0][1:]),c="blue")
    ax.plot(x_result[ss2][0][1:], np.poly1d(np.polyfit(x_result[ss2][0][1:], y_result[ss2][0][1:], 1))(x_result[ss2][0][1:]),":",c="deepskyblue")
    ax.plot(x_result[sd][0][1:], np.poly1d(np.polyfit(x_result[sd][0][1:], y_result[sd][0][1:], 1))(x_result[sd][0][1:]),c="aqua")
    ax.plot(x_result[ss][1][1:], np.poly1d(np.polyfit(x_result[ss][1][1:], y_result[ss][1][1:], 1))(x_result[ss][1][1:]),c="green")
    ax.plot(x_result[ss2][1][1:], np.poly1d(np.polyfit(x_result[ss2][1][1:], y_result[ss2][1][1:], 1))(x_result[ss2][1][1:]),":",c="lawngreen")
    ax.plot(x_result[sd][1][1:], np.poly1d(np.polyfit(x_result[sd][1][1:], y_result[sd][1][1:], 1))(x_result[sd][1][1:]),c="palegreen")
    ax.plot(x_result[ss][2][1:], np.poly1d(np.polyfit(x_result[ss][2][1:], y_result[ss][2][1:], 1))(x_result[ss][2][1:]),c="red")
    ax.plot(x_result[ss2][2][1:], np.poly1d(np.polyfit(x_result[ss2][2][1:], y_result[ss2][2][1:], 1))(x_result[ss2][2][1:]),":",c="deeppink")
    ax.plot(x_result[sd][2][1:], np.poly1d(np.polyfit(x_result[sd][2][1:], y_result[sd][2][1:], 1))(x_result[sd][2][1:]),c="violet")
    ax.plot(x_result[ss][3][1:], np.poly1d(np.polyfit(x_result[ss][3][1:], y_result[ss][3][1:], 1))(x_result[ss][3][1:]),c="orange")
    ax.plot(x_result[ss2][3][1:], np.poly1d(np.polyfit(x_result[ss2][3][1:], y_result[ss2][3][1:], 1))(x_result[ss2][3][1:]),":",c="gold")
    ax.plot(x_result[sd][3][1:], np.poly1d(np.polyfit(x_result[sd][3][1:], y_result[sd][3][1:], 1))(x_result[sd][3][1:]),c="yellow")
    
    ax.set_ylim(0,101)
    ax.set_ylim(0,101)
    ax.set(xlabel='Traffic amount [bps]', ylabel="PDR [%]")
    ax.legend(loc="lower left")

    save = mode
    fig.savefig(save+"_"+option+"_span"+str(int(span*1000))+"ms.png")        
        

if mode == "decodeCount":
    ss="./results/pro1.1_smooth2_rri100.csv"
    ss3="./results/add_pro1.1_smooth2_rri100.csv"
    
    ss2="./results/sps_smooth2_rri100.csv"
    sd="./results/ds_smooth2.csv"

    senderID={}
    timeRange={}
    NODE = {}
    
    target= "tbSent:vector"
    target_d =["tbDecoded:vector","tbFailedDueToInterferenceIgnoreSCI:vector","tbFailedDueToPropIgnoreSCI:vector"]
    # target2="tbDecodedIgnoreSCI:vector"
    # target3 = "tbFailedHalfDuplex:vector"
    for s in [ss]:
        # count_el(s,target1,timeRange)
        # count_el_and_total(s,target2,timeRange)
        senderID[s]={}
        timeRange[s]=[{},{},{},{}]
        if "pro" in s:
            NODE[s]=[INTERSECTION_A_NODE_P,INTERSECTION_B_NODE_P,STREET_C_NODE_P,STREET_D_NODE_P]
            make_timerange(s_c_a2,s_c_b2,s_c_c2,s_c_d2,timeRange[s])
        else:
            NODE[s]=[INTERSECTION_A_NODE,INTERSECTION_B_NODE,STREET_C_NODE,STREET_D_NODE]
            make_timerange(s_c_a,s_c_b,s_c_c,s_c_d,timeRange[s])
        make_senderID(s,senderID[s])
        count_el(s,target,timeRange[s],NODE[s])
        for t in target_d:
            count_el_and_total_d(s,t,timeRange[s],NODE[s],senderID[s])
        

if mode == "resourceMargin":
    ss="./results/pro3.0_smooth2.csv"
    # ss2="./results/pro1.4_smooth2_rri100.csv"
    
    ss3="./results/sps_smooth2_rri100.csv"
    sd="./results/ds_smooth2.csv"
    timeRange={}
    simTime = 30
    startTime = 28800
    NODE = {}
    x_data={}
    y_data={}
    for s in [ss,ss3,sd]:
        timeRange[s]=[{},{},{},{}]
        x_data[s] = [{},{},{},{}]
        y_data[s] = [{},{},{},{}]
        if "pro" in s:
            NODE[s]=[INTERSECTION_A_NODE_P,INTERSECTION_B_NODE_P,STREET_C_NODE_P,STREET_D_NODE_P]
            make_timerange(s_c_a2,s_c_b2,s_c_c2,s_c_d2,timeRange[s])
        else:
            NODE[s]=[INTERSECTION_A_NODE,INTERSECTION_B_NODE,STREET_C_NODE,STREET_D_NODE]
            make_timerange(s_c_a,s_c_b,s_c_c,s_c_d,timeRange[s])
        print(s)
        make_resourceMargin(x_data[s],y_data[s],NODE[s],timeRange[s],simTime,startTime)

if mode == "parameter":
    NODE ={}
    makeNodes(ss,NODE)
    for n in NODE:
        print(str(n) + "," + NODE[n])

if mode == "myenv_resourceMargin":
    # csv_s10 ="results/test_0.3_sps.csv"
    # csv_s50 ="results/test_0.3_pro1.4.csv"
    # csv_s100 ="results/test_0.3_pro2.1.csv"
    # csv_d = 'results/test_0.3_ds.csv'
    csv_s10 ="results/intersection_sps_rri100.csv"
    csv_s50 ="results/intersection_pro1.1_rri100.csv"
    csv_s100 ="results/intersection_pro3.0.csv"
    csv_d = 'results/intersection_ds.csv'
    timeRange={}
    simTime = 100
    startTime = 200
    NODE = {}
    x_data={}
    y_data={}
    for s in [csv_s100]:
        timeRange[s]=[{},{},{},{}]
        nodes = {}
        makeNodes(s,nodes)
        x_data[s] = [{},{},{},{}]
        y_data[s] = [{},{},{},{}]
        NODE[s]=[nodes,nodes,nodes,nodes]
        for n in nodes:
            for i in range(len(timeRange[s])):
                timeRange[s][i][n]=[startTime,startTime+simTime]
        print(s)
        make_resourceMargin_simple(x_data[s],y_data[s],NODE[s],timeRange[s],simTime,startTime)

if mode == "sending_interval":
    ss = "results/intersection_sps_rri100.csv"
    ss2 = "results/intersection_pro1.4_rri100.csv"
    ss3 = "results/intersection_pro2.1_rri100.csv"
    ss4 = "results/intersection_pro3.0.csv"
    sd = "results/intersection_ds.csv"
    x_data = ["100","200","300","400","500","600","700","800","900","1000"]
    y_data={}
    tp={}
    labels=["sps","pro1.4","pro2.0","pro3.0","ds"]
    label_index =0
    for s in [ss,ss2,ss3,ss4,sd]:
        y_data[s] = []
        for i in range(len(x_data)):
            y_data[s].append(0)
        make_interval_simple(x_data,y_data[s],s)
        tp[labels[label_index]]=y_data[s]
        label_index += 1
    fig, ax = plt.subplots()
    df = pd.DataFrame(tp,x_data)
    # ax.set_xticks(sendinterval)
    # ax.set_xticklabels(left)
    plt.xlabel("Generation Intaerval [ms]")
    plt.ylabel("Number of CAM")
    df.plot.bar(ax=ax)
    # plt.setp(left, rotation=45, fontsize=9)
    plt.xticks(fontsize=9)
    plt.xticks(rotation=45)
    save = "interval"
    fig.savefig(save+"_"+option)


if mode == "missedTransmission":
    ss = "./results/pro3.0_smooth2.csv"
    ss2 = "./results/sps_smooth2_rri100.csv"
    startTime = 28800.0
    simTime = 30
    x_data=['Proposal_a','Proposal_b','Proposal_c','Proposal_d','SPS_a','SPS_b','SPS_c','SPS_d']
    y_data = []
    NODE = {}
    timeRange={}
    fig = plt.figure()
    
    colors=["blue","green","red","orange","deepskyblue","lawngreen","deeppink","gold"]
    
    for s in [ss,ss2]:
        timeRange[s]=[{},{},{},{}]
        if "pro" in s:
            NODE[s]=[INTERSECTION_A_NODE_P,INTERSECTION_B_NODE_P,STREET_C_NODE_P,STREET_D_NODE_P]
            make_timerange(s_c_a2,s_c_b2,s_c_c2,s_c_d2,timeRange[s])
        else:
            NODE[s]=[INTERSECTION_A_NODE,INTERSECTION_B_NODE,STREET_C_NODE,STREET_D_NODE]
            make_timerange(s_c_a,s_c_b,s_c_c,s_c_d,timeRange[s])
        for num in count_el(s,"grantBreakMissedTrans:vector",timeRange[s],NODE[s]):
            y_data.append(num)

    # 軸ラベルやタイトルを設定
    plt.bar(x_data,y_data,color=colors,edgecolor="black",linewidth=1)
    plt.xlabel('Traffic')
    plt.ylabel('Counts of Waste Resources')
    plt.xticks(rotation=45)
    plt.show()
    # plt.legend()

    # グラフを表示
    plt.show()
    fig.savefig(mode+"_"+option+".pdf")

if mode == "packetLoss":
    ss = "./results/pro3.0_smooth2.csv"
    ss2 = "./results/sps_smooth2_rri300.csv"
    startTime = 28800.0
    simTime = 30
    x_data=['Proposal_a','Proposal_b','Proposal_c','Proposal_d','SPS_a','SPS_b','SPS_c','SPS_d']
    y_data = []
    NODE = {}
    timeRange={}
    fig = plt.figure(figsize=(6,4))
    
    colors=["blue","green","red","orange","deepskyblue","lawngreen","deeppink","gold"]
    
    for s in [ss,ss2]:
        timeRange[s]=[{},{},{},{}]
        if "pro" in s:
            NODE[s]=[INTERSECTION_A_NODE_P,INTERSECTION_B_NODE_P,STREET_C_NODE_P,STREET_D_NODE_P]
            make_timerange(s_c_a2,s_c_b2,s_c_c2,s_c_d2,timeRange[s])
        else:
            NODE[s]=[INTERSECTION_A_NODE,INTERSECTION_B_NODE,STREET_C_NODE,STREET_D_NODE]
            make_timerange(s_c_a,s_c_b,s_c_c,s_c_d,timeRange[s])
        message_nums = count_el_by_length(s,"camSentPositionX:vector",timeRange[s],NODE[s])
        tbsent_nums = count_el(s,"tbSent:vector",timeRange[s],NODE[s])
        for i in range(len(message_nums)):
            y_data.append((message_nums[i] - tbsent_nums[i])/message_nums[i]*100)
        

    # 軸ラベルやタイトルを設定
    plt.bar(x_data,y_data,color=colors,edgecolor="black",linewidth=1)
    plt.ylim(0,31)
    plt.xlabel('Traffic')
    plt.ylabel('Packet Loss Rate [%]')
    plt.xticks(rotation=45)
    
    # plt.legend()

    # グラフを表示
    plt.show()
    fig.savefig(mode+"_"+option+".pdf")

if mode == "count":
    ss = "./results/pro3.0_smooth2.csv"
    ss2 = "./results/sps_smooth2_rri300.csv"
    startTime = 28800.0
    simTime = 30
    NODE = {}
    timeRange={}
    target = ""
    if len(args)>=4 :
        target=args[3]
    for s in [ss2]:
        timeRange[s]=[{},{},{},{}]
        if "pro" in s:
            NODE[s]=[INTERSECTION_A_NODE_P,INTERSECTION_B_NODE_P,STREET_C_NODE_P,STREET_D_NODE_P]
            make_timerange(s_c_a2,s_c_b2,s_c_c2,s_c_d2,timeRange[s])
        else:
            NODE[s]=[INTERSECTION_A_NODE,INTERSECTION_B_NODE,STREET_C_NODE,STREET_D_NODE]
            make_timerange(s_c_a,s_c_b,s_c_c,s_c_d,timeRange[s])
        count_el_by_length(s,target,timeRange[s],NODE[s])