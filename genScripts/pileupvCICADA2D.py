import ROOT
from tqdm import tqdm
import os
import prepChains as pc
import numpy as np
import math

ROOT.gStyle.SetOptStat(0)

run = input("Which Run?")
m_dir = "/hdfs/store/user/aloelige/ZeroBias/CICADA_2018Run"+run+"_ZB_07Jul2023"
# "/hdfs/store/user/aloelige/ZeroBias/CICADA_2022Run"+run+"_ZeroBias_07Jul2023/"
#m_dir = "/hdfs/store/user/aloelige/ZeroBias/CICADA_Ztoee_wMINIAOD_RAW_Run"+run+"_08Jun2023/" # "/hdfs/store/user/aloelige/ZeroBias/CICADA_Ztoee_wMINIAOD_RAW_Run"+run+"_08Jun2023/"

# There's probably a better way to do this ngl - Run Differentiation
add = [f.path for f in os.scandir(m_dir) if f.is_dir()]
run_list = [a.path for a in os.scandir(add[0]) if a.is_dir()]

# Prepping Chains
for i in range(len(run_list)):
    chains = pc.prepChains(run_list[i])

# Creating the Histograms
canvas = ROOT.TCanvas()
hanompileup = ROOT.TH2F("AnomalyNPileup"+run, "Pileup v. Anomaly Score/Pileup Prediction", 100, 0.0, 1.0, 10, 0.0, 100.0)
sumo = []
tpileuparr = []
avgarr = []

count = 0

for i in tqdm(range(chains['cicadaChain'].GetEntries())): # chains['anomalyChain'].GetEntries()
    """chains['anomalyChain'].GetEntry(i)
    chains['PUChain'].GetEntry(i)"""
    chains['cicadaChain'].GetEntry(i)
    chains['newPUChain'].GetEntry(i)
    chains['pileupInfo'].GetEntry(i)
    predictedPileup = math.floor(chains['newPUChain'].pileupPrediction)
    truePileup = chains['pileupInfo'].npv
    tpileuparr.append(truePileup)
    anomalyScore = chains['cicadaChain'].anomalyScore
    if predictedPileup != 0:
        SNAIL = anomalyScore/predictedPileup
    else:
        SNAIL: anomalyScore
    
    """
    nBins = hanompileup.GetNbinsX() # 100
    nBinsy = hanompileup.GetNbinsY() # 10
   
    for j in range(nBins):
        e = hanompileup.GetBinContent(j)
        
        
        sumo.append(e)
        avgbin = np.average(np.asarray(sumo))
        avgarr.append(avgbin)
    """
    hanompileup.Fill(SNAIL,truePileup)

    # hanompileup.Fill(anomalyScore,truePileup)

"""tpileuparr = np.asarray(tpileuparr)
avgarr = np.asarray(avgbin)

def linfit(x, a, b):
    return a * x + b

def sqrtfit(x, a, b):
    return a * x**(1/2) + b"""


hanompileup.SetTitle("")
hanompileup.GetXaxis().SetTitle("Anomaly Score/Pileup Prediction")
hanompileup.GetYaxis().SetTitle("True Pileup")
hanompileup.SetMarkerStyle(8)
hanompileup.SetMarkerSize(0.4)
hanompileup.GetXaxis().SetTitleSize(0.035)
hanompileup.GetXaxis().SetTitleOffset(1.2)
hanompileup.GetYaxis().SetTitleSize(0.035)
hanompileup.GetYaxis().SetTitleOffset(1.2)
hanompileup.Draw("COLZ")
"""popt, pcov = curve_fit(linfit, avgarr, tpileuparr)
plt.plot(avgarr, linfit(avgarr, *popt), "r-")
plt.plot(avgarr, tpileuparr, "b")"""

canvas.Draw()
canvas.SaveAs("anomnormpileupNN_run"+run+'.png')

"""
fanompileup = ROOT.TFile("anompileup_run"+run+".root", "CREATE")
fanompileup.WriteObject(hanompileup, "anompileup_run"+run)
print("Histogram Created.")
"""
