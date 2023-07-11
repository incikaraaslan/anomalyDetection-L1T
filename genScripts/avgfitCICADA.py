import ROOT
from tqdm import tqdm
import os
import prepChains as pc
import numpy as np
import math
import matplotlib.pyplot as plt

ROOT.gStyle.SetOptStat(0)

run = input("Which Run?")
m_dir = "/hdfs/store/user/aloelige/ZeroBias/CICADA_Ztoee_wMINIAOD_RAW_Run"+run+"_08Jun2023/"

# There's probably a better way to do this ngl - Run Differentiation
add = [f.path for f in os.scandir(m_dir) if f.is_dir()]
run_list = [a.path for a in os.scandir(add[0]) if a.is_dir()]

# Prepping Chains
for i in range(len(run_list)):
    chains = pc.prepChains(run_list[i])

# Creating the Histograms
canvas = ROOT.TCanvas()
hanompileup = ROOT.TH2F("AnomalyNPileup"+run, "Pileup v. Anomaly Score", 100, 0.0, 10.0, 10, 0.0, 100.0)
sumo = []
sum010 = 0
sum1020 = 0
sum2030 = 0
sum3040 = 0
sum4050 = 0
sum5060 = 0
sum6070 = 0
sum7080 = 0
sum8090 = 0
sum90100 = 0

a = []

for i in tqdm(range(chains['anomalyChain'].GetEntries())): # chains['anomalyChain'].GetEntries()
    chains['anomalyChain'].GetEntry(i)
    chains['PUChain'].GetEntry(i)
    predictedPileup = math.floor(chains['PUChain'].pileupPrediction)
    truePileup = chains['anomalyChain'].npv
    anomalyScore = chains['anomalyChain'].anomalyScore
    SNAIL = anomalyScore/predictedPileup
    nBinsy = hanompileup.GetNbinsY()

    for j in range(nBinsy):
        a.append(hanompileup.GetBinContent(j+1))

    print(a)

    if truePileup in range(0,10):
        sum010 += anomalyScore
    elif truePileup in range(10,20):
        sum1020 += anomalyScore
    elif truePileup in range(20,30):
        sum2030 += anomalyScore
    elif truePileup in range(30,40):
        sum3040 += anomalyScore
    elif truePileup in range(40,50):
        sum4050 += anomalyScore
    elif truePileup in range(50,60):
        sum5060 += anomalyScore
    elif truePileup in range(60,70):
        sum6070 += anomalyScore
    elif truePileup in range(70,80):
        sum7080 += anomalyScore
    elif truePileup in range(80,90):
        sum8090 += anomalyScore
    elif truePileup in range(90,100):
        sum90100 += anomalyScore
    else:
        pass
    
    """
    nBins = hanompileup.GetNbinsX() # 100
    nBinsy = hanompileup.GetNbinsY() # 10
    # print(nBins, nBinsy)

    for j in range(nBinsy):
        pileupC = hanompileup.GetYaxis().GetBinCenter(j+1)    
        print(pileupC, cicadaC)
        centarrCy.append(pileupC)
        centarrC.append(cicadaC)
    """
sumo.extend((sum010, sum1020, sum2030, sum3040, sum4050, sum5060, sum6070, sum7080, sum8090, sum90100))
print(sumo)
avgarr = []

for i in range(10):
    avgarr.append(sumo[i]/a[i])

print(avgarr)
