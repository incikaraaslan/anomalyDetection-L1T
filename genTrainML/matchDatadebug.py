import ROOT
from tqdm import tqdm
import os
import prepChains as pc
import iEtaiPhiBinning
import numpy as np
import pandas as pd
import math
import random
from time import perf_counter
import h5py

tt = ["trainshuf"]# , "testshuf"]

counters = [0, 0, 0, 0, 0, 0]
chain_count = [0, 0]
for c in tqdm(range(len(tt))):
    print(tt[c])

    # Import Files from Data
    flist = open('output/'+tt[c]+'.txt', 'r')
    for x in flist:
        chains = pc.prepChains(x)
            
    print(chains['puppiJet'].GetEntries())
    
    """
    f = ROOT.TFile.Open(x, 'READ')
        openfiles.append(f)
        t = f.Get("puppiJetNtuplizer/PuppiJets").GetEntries()
        print(t)
        f.ROOT.TFile.Close()
    flist = open('output/'+tt[c]+'.txt', 'r')
    f = ROOT.TFile.Open(flist, 'READ')
    t = f.Get("puppiJetNtuplizer/PuppiJets").GetEntries()
    print(t)"""
        # chains = pc.prepChains(x)
        # counters[c] += 1
    
    # print(chains['puppiJet'].GetEntries())
    #print(chains['trigJet'].GetEntries())

    # Match Jet with PUPPI
    """for i in tqdm(range(chains['puppiJet'].GetEntries())):
        print(chains['puppiJet'].GetEntries())
        chains['puppiJet'].GetEntry(i)
        chains['trigJet'].GetEntry(i)
        chains['regionEt'].GetEntry(i)"""