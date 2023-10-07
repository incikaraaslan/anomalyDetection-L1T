import ROOT
from tqdm import tqdm
import os
import prepChains as pc
import numpy as np
import pandas as pd
import math
import random
from time import perf_counter
# import splitfolders

ROOT.gStyle.SetOptStat(0)

file_list = []
m_dir = ["/hdfs/store/user/aloelige/ZeroBias/SNAIL_2018RunA_ZB_08Sep2023/", 
"/hdfs/store/user/aloelige/ZeroBias/SNAIL_2018RunB_ZB_08Sep2023/", 
"/hdfs/store/user/aloelige/ZeroBias/SNAIL_2018RunC_ZB_08Sep2023/"]

for i in tqdm(range(3)):
    # Run Differentiation
    add = [f.path for f in os.scandir(m_dir[i]) if f.is_dir()]
    run_list = [a.path for a in os.scandir(add[0]) if a.is_dir()]
    for j in tqdm(range(len(run_list))):
        for k in tqdm(range(len(os.listdir(run_list[j])))):
            dir_list = os.listdir(run_list[j])
            file_list.append(str(run_list[j]) +"/" + str(dir_list[k]))

# Flatten if needed
"""def flatten(l):
    return [item for sublist in l for item in sublist]
file_list = flatten(file_list)"""
# Splitting Files
# Make sure to always shuffle with a fixed seed so that the split is reproducible

random.seed(230)
file_list.sort()
random.shuffle(file_list)

split = int(0.8 * len(file_list))
train_file = file_list[:split] # reshape(-1)
test_file = file_list[split:] #reshape(-1)

# Print
print("Training: ", train_file)
print("Test: ", test_file)

# Save Files
np.savetxt('output/train.txt', np.asarray(train_file), fmt='%s')
np.savetxt('output/test.txt', np.asarray(test_file), fmt='%s')