import ROOT
from tqdm import tqdm
import os
import prepChains as pc
import numpy as np

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
hPileup = ROOT.TH1F("pRun_"+run, "True Pileup", 100, 0.0, 10.0)
hPrediction = ROOT.TH1F("ppredRun_"+run, "Prediction", 100, 0.0, 10.0)
hPileupvPrediction = ROOT.TH1F("pvpredRun_"+run, "Prediction/True Pileup", 100, 0.0, 10.0)

for i in tqdm(range(chains['anomalyChain'].GetEntries())):
    chains['anomalyChain'].GetEntry(i)
    chains['PUChain'].GetEntry(i)
    truePileup = chains['anomalyChain'].npv
    predictedPileup = chains['PUChain'].pileupPrediction
    hPileupvPrediction.Fill(predictedPileup/truePileup)
    hPileup.Fill(truePileup)
    hPrediction.Fill(predictedPileup)

fPileup = ROOT.TFile("histPileup_run"+run+".root", "CREATE")
fPileup.WriteObject(hPileup, "histPileup_run"+run)
print("Histogram 1 Created.") 
fPileupvPrediction = ROOT.TFile("histPredPileup_run"+run+".root", "CREATE")
fPileupvPrediction.WriteObject(hPileupvPrediction, "histPredPileup_run"+run)
print("Histogram 2 Created.") 
fPrediction = ROOT.TFile("histPred_run"+run+".root", "CREATE")
fPrediction.WriteObject(hPrediction, "histPred_run"+run)
print("Histogram 3 Created.")