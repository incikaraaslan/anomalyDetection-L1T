import ROOT
from tqdm import tqdm
import os
import prepChains as pc
import numpy as np
import math

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

for i in tqdm(range(chains['anomalyChain'].GetEntries())): # chains['anomalyChain'].GetEntries()
    chains['anomalyChain'].GetEntry(i)
    chains['PUChain'].GetEntry(i)
    predictedPileup = math.floor(chains['PUChain'].pileupPrediction)
    truePileup = chains['anomalyChain'].npv
    anomalyScore = chains['anomalyChain'].anomalyScore
    SNAIL = anomalyScore/predictedPileup
    
    
    hanompileup.Fill(anomalyScore,truePileup)


hanompileup.SetTitle("")
hanompileup.GetXaxis().SetTitle("Anomaly Score")
hanompileup.GetYaxis().SetTitle("True Pileup")
hanompileup.SetMarkerStyle(8)
hanompileup.SetMarkerSize(0.4)
hanompileup.GetXaxis().SetTitleSize(0.035)
hanompileup.GetXaxis().SetTitleOffset(1.2)
hanompileup.GetYaxis().SetTitleSize(0.035)
hanompileup.GetYaxis().SetTitleOffset(1.2)
hanompileup.Draw("COLZ")
canvas.Draw()
canvas.SaveAs("anomnormpileup_run"+run+'.png')
"""
fanompileup = ROOT.TFile("anompileup_run"+run+".root", "CREATE")
fanompileup.WriteObject(hanompileup, "anompileup_run"+run)
print("Histogram Created.")
"""
