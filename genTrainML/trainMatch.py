import ROOT
from tqdm import tqdm
import os
import prepChains as pc
import numpy as np
import math
from time import perf_counter

ROOT.gStyle.SetOptStat(0)

run = input("Log in the Run A, C, D:")
if run == "A":
    m_dir = "/store/user/aloelige/ZeroBias/SNAIL_2018Run"+run+"_ZB_08Sep2023"
elif run == "D":
    m_dir = "/store/user/aloelige/ZeroBias/SNAIL_2018Run"+run+"_ZB_09Sep2023"
# "/hdfs/store/user/aloelige/ZeroBias/CICADA_2018Run"+run+"_ZB_07Jul2023"

# Run Differentiation
add = [f.path for f in os.scandir(m_dir) if f.is_dir()]
run_list = [a.path for a in os.scandir(add[0]) if a.is_dir()]

# Prepping Chains
for i in range(len(run_list)):
    chains = pc.prepChains(run_list[i])


