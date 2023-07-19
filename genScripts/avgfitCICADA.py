import ROOT
from tqdm import tqdm
import os
import prepChains as pc
import numpy as np
import math
import matplotlib.pyplot as plt
from array import array

ROOT.gStyle.SetOptStat(0)

run = input("Which Run?")
m_dir = "/hdfs/store/user/aloelige/ZeroBias/CICADA_2018Run"+run+"_ZB_07Jul2023"
#"/hdfs/store/user/aloelige/ZeroBias/CICADA_Ztoee_wMINIAOD_RAW_Run"+run+"_08Jun2023/"

# There's probably a better way to do this ngl - Run Differentiation
add = [f.path for f in os.scandir(m_dir) if f.is_dir()]
run_list = [a.path for a in os.scandir(add[0]) if a.is_dir()]

# Prepping Chains
for i in range(len(run_list)):
    chains = pc.prepChains(run_list[i])

# Creating the Histograms
canvas = ROOT.TCanvas()
hanompileup = ROOT.TH2F("AnomalyNPileup"+run, "Pileup v. Anomaly Score", 100, 0.0, 10.0, 10, 0.0, 100.0)
xval = []
yval = []
xbins = 100
ybins = 10
zbins = 1

# NEW DATA
for i in tqdm(range(chains['cicadaChain'].GetEntries())): # chains['anomalyChain'].GetEntries()
    chains['cicadaChain'].GetEntry(i)
    chains['newPUChain'].GetEntry(i)
    chains['pileupInfo'].GetEntry(i)
    predictedPileup = math.floor(chains['PUChain'].pileupPrediction)
    truePileup = chains['pileupInfo'].npv
    anomalyScore = chains['cicadaChain'].anomalyScore
    if predictedPileup == 0:
        SNAIL: anomalyScore
    else:
        SNAIL = anomalyScore/predictedPileup
    # count = 0
    hanompileup.Fill(anomalyScore,truePileup)
"""
OLD DATA
for i in tqdm(range(chains['anomalyChain'].GetEntries())): # chains['anomalyChain'].GetEntries()
    chains['anomalyChain'].GetEntry(i)
    chains['PUChain'].GetEntry(i)
    predictedPileup = math.floor(chains['PUChain'].pileupPrediction)
    truePileup = chains['anomalyChain'].npv
    anomalyScore = chains['anomalyChain'].anomalyScore
    SNAIL = anomalyScore/predictedPileup
    # count = 0
    hanompileup.Fill(anomalyScore,truePileup)
"""

# Loop over x values for all y values
for j in range(ybins):
    zmax = None
    maxbin = 0
    for k in range(xbins):
        # count += 1
        pileupC = hanompileup.GetYaxis().GetBinCenter(j+1)
        if zmax is None:
            zmax = hanompileup.GetBinContent(k+1, j+1)
        
        elif hanompileup.GetBinContent(k+1, j+1) > zmax:
            zmax = hanompileup.GetBinContent(k+1, j+1)
            maxbin = k+1
        print(maxbin)

        """if k == 0:
            zmax = hanompileup.GetBinContent(k+1, j+1)
            maxbin = 1
        else:
            zmax = max(zmax, hanompileup.GetBinContent(k+1, j+1))
            if zmax == hanompileup.GetBinContent(k+1, j+1):
                maxbin = k+1"""
    if maxbin > 0.1: # FOR RUND ONLY
        xval.append(hanompileup.GetXaxis().GetBinCenter(maxbin))
        yval.append(pileupC)
    else:
        pass

print(xval, yval)
anomscores = array('d', xval)
truepileup = array('d', yval)
avgforEachP = ROOT.TGraph(len(anomscores), anomscores, truepileup)

avgfit = ROOT.TFile("INCImaxforEachP_run"+run+".root", "CREATE")
avgfit.WriteObject(hanompileup, "AnomalyNPileup"+run)
avgfit.WriteObject(avgforEachP, "INCImaxforEachP_run"+run)
print("Histogram and Graph Created.")

"""maxbin = hanompileup.GetMaximum()
        e = hanompileup.GetZaxis().GetBinCenter(1)"""
        # = hanompileup.GetBinXYZ(maxbin, ROOT.Long(k), ROOT.Long(j), ROOT.Long(1))
        # e = hanompileup.GetBinContent(k,j)
        # print("Event Bin: " + str(e))
        # sumo += e
"""
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
avgforEachP.Draw("CP")


canvas.Draw()

canvas.SaveAs("anomnormpileupWG_run"+run+'.png')

"""

