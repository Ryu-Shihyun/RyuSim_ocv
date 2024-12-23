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

s = "./results/sps_smooth2_rri100.csv"

if len(args)>=2 :
    s=args[1]

with open(s) as f:
    reader = csv.reader(f)
    for row in reader:
        if row[1] =="vector" and row[3] == "camVehicleId:vector" :
            id = re.split(" ",row[8])[0]
            vehicle = re.split("[\[\]]",row[2])[1]
            print(vehicle + "," + id)

