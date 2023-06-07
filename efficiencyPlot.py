import ROOT
import tqdm
import os
import pc

ROOT.gStyle.SetOptStat(0)

run = input("Which Run?")
directory = "/hdfs/store/user/aloeliger/uGTComparisons/v_2/Run"+run+"/" 
chains = pc.prepChains(directory)
ratePlots = []

for i in tqdm(range(chains['anomalyChain'].GetEntries())):
    chains['anomalyChain'].GetEntry(i)
    a = chains['anomalyChain'].anomalyScore
    

