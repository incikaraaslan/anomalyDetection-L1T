import ROOT
from tqdm import tqdm
import os
import prepChains as pc
import numpy as np
import math

ROOT.gStyle.SetOptStat(0)

m_dir = "/hdfs/store/user/aloelige/TT_TuneCP5_13p6TeV_powheg-pythia8/CICADA_2022_TT_07Jul2023/"
# "/hdfs/store/user/aloelige/ZeroBias/CICADA_2018Run"+run+"_ZB_07Jul2023"
# "/hdfs/store/user/aloelige/ZeroBias/CICADA_Ztoee_wMINIAOD_RAW_Run"+run+"_08Jun2023/"

# There's probably a better way to do this ngl - Run Differentiation
add = [f.path for f in os.scandir(m_dir) if f.is_dir()]
run_list = [a.path for a in os.scandir(add[0]) if a.is_dir()]

# Prepping Chains
for i in range(len(run_list)):
    chains = pc.prepChains(run_list[i])

