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
hanomalyScore010 = ROOT.TH1F("Anomaly Score "+run+" 0-10", "Anomaly Score for 0-10", 100, 0.0, 10.0)
hanomalyScore1020 = ROOT.TH1F("Anomaly Score "+run+" 10-20", "Anomaly Score 10-20", 100, 0.0, 10.0)
hanomalyScore2030 = ROOT.TH1F("Anomaly Score "+run+" 20-30", "Anomaly Score 20-30", 100, 0.0, 10.0)
hanomalyScore3040 = ROOT.TH1F("Anomaly Score "+run+" 30-40", "Anomaly Score 30-40", 100, 0.0, 10.0)
hanomalyScore4050 = ROOT.TH1F("Anomaly Score "+run+" 40-50", "Anomaly Score 40-50", 100, 0.0, 10.0)
hanomalyScore5060 = ROOT.TH1F("Anomaly Score "+run+" 50-60", "Anomaly Score 50-60", 100, 0.0, 10.0)
hanomalyScore6070 = ROOT.TH1F("Anomaly Score "+run+" 60-70", "Anomaly Score 60-70", 100, 0.0, 10.0)
hanomalyScore7080 = ROOT.TH1F("Anomaly Score "+run+" 70-80", "Anomaly Score 70-80", 100, 0.0, 10.0)
hCS010 = ROOT.TH1F("Anomaly Score/Pileup Pred "+run+" 0-10", "Anomaly Score/Pileup Pred for 0-10", 100, 0.0, 10.0)
hCS1020 = ROOT.TH1F("Anomaly Score/Pileup Pred "+run+" 10-20", "Anomaly Score/Pileup Pred 10-20", 100, 0.0, 10.0)
hCS2030 = ROOT.TH1F("Anomaly Score/Pileup Pred "+run+" 20-30", "Anomaly Score/Pileup Pred 20-30", 100, 0.0, 10.0)
hCS3040 = ROOT.TH1F("Anomaly Score/Pileup Pred "+run+" 30-40", "Anomaly Score/Pileup Pred 30-40", 100, 0.0, 10.0)
hCS4050 = ROOT.TH1F("Anomaly Score/Pileup Pred "+run+" 40-50", "Anomaly Score/Pileup Pred 40-50", 100, 0.0, 10.0)
hCS5060 = ROOT.TH1F("Anomaly Score/Pileup Pred "+run+" 50-60", "Anomaly Score/Pileup Pred 50-60", 100, 0.0, 10.0)
hCS6070 = ROOT.TH1F("Anomaly Score/Pileup Pred "+run+" 60-70", "Anomaly Score/Pileup Pred 60-70", 100, 0.0, 10.0)
hCS7080 = ROOT.TH1F("Anomaly Score/Pileup Pred "+run+" 70-80", "Anomaly Score/Pileup Pred 70-80", 100, 0.0, 10.0)

for i in tqdm(range(chains['anomalyChain'].GetEntries())): # chains['anomalyChain'].GetEntries()
    chains['anomalyChain'].GetEntry(i)
    chains['PUChain'].GetEntry(i)
    predictedPileup = math.floor(chains['PUChain'].pileupPrediction)
    truePileup = chains['anomalyChain'].npv
    anomalyScore = chains['anomalyChain'].anomalyScore
    SNAIL = anomalyScore/predictedPileup
    if truePileup in range(0,10):
        hanomalyScore010.Fill(anomalyScore)
        hCS010.Fill(SNAIL)
    elif truePileup in range(10,20):
        hanomalyScore1020.Fill(anomalyScore)
        hCS1020.Fill(SNAIL)
    elif truePileup in range(20,30):
        hanomalyScore2030.Fill(anomalyScore)
        hCS2030.Fill(SNAIL)
    elif truePileup in range(30,40):
        hanomalyScore3040.Fill(anomalyScore)
        hCS3040.Fill(SNAIL)
    elif truePileup in range(40,50):
        hanomalyScore4050.Fill(anomalyScore)
        hCS4050.Fill(SNAIL)
    elif truePileup in range(50,60):
        hanomalyScore5060.Fill(anomalyScore)
        hCS5060.Fill(SNAIL)
    elif truePileup in range(60,70):
        hanomalyScore6070.Fill(anomalyScore)
        hCS6070.Fill(SNAIL)
    elif truePileup in range(70,80):
        hanomalyScore7080.Fill(anomalyScore)
        hCS7080.Fill(SNAIL)
    else:
        pass

fanomalyScore010 = ROOT.TFile("anomalyScore010_run"+run+".root", "CREATE")
fanomalyScore010.WriteObject(hanomalyScore010, "anomalyScore010_run"+run)
fCS010 = ROOT.TFile("CS010_run"+run+".root", "CREATE")
fCS010.WriteObject(hCS010, "CS010_run"+run)
print("Histogram 010 Created.") 
fanomalyScore1020 = ROOT.TFile("anomalyScore1020_run"+run+".root", "CREATE")
fanomalyScore1020.WriteObject(hanomalyScore1020, "anomalyScore1020_run"+run)
fCS1020 = ROOT.TFile("CS1020_run"+run+".root", "CREATE")
fCS1020.WriteObject(hCS1020, "CS1020_run"+run)
print("Histogram 1020 Created.") 
fanomalyScore2030 = ROOT.TFile("anomalyScore2030_run"+run+".root", "CREATE")
fanomalyScore2030.WriteObject(hanomalyScore2030, "anomalyScore2030_run"+run)
fCS2030 = ROOT.TFile("CS2030_run"+run+".root", "CREATE")
fCS2030.WriteObject(hCS2030, "CS2030_run"+run)
print("Histogram 2030 Created.")
fanomalyScore3040 = ROOT.TFile("anomalyScore3040_run"+run+".root", "CREATE")
fanomalyScore3040.WriteObject(hanomalyScore3040, "anomalyScore3040_run"+run)
fCS3040 = ROOT.TFile("CS3040_run"+run+".root", "CREATE")
fCS3040.WriteObject(hCS3040, "CS3040_run"+run)
print("Histogram 3040 Created.") 
fanomalyScore4050 = ROOT.TFile("anomalyScore4050_run"+run+".root", "CREATE")
fanomalyScore4050.WriteObject(hanomalyScore4050, "anomalyScore4050_run"+run)
fCS4050 = ROOT.TFile("CS4050_run"+run+".root", "CREATE")
fCS4050.WriteObject(hCS4050, "CS4050_run"+run)
print("Histogram 4050 Created.") 
fanomalyScore5060 = ROOT.TFile("anomalyScore5060_run"+run+".root", "CREATE")
fanomalyScore5060.WriteObject(hanomalyScore5060, "anomalyScore5060_run"+run)
fCS5060 = ROOT.TFile("CS5060_run"+run+".root", "CREATE")
fCS5060.WriteObject(hCS5060, "CS5060_run"+run)
print("Histogram 5060 Created.") 
fanomalyScore6070 = ROOT.TFile("anomalyScore6070_run"+run+".root", "CREATE")
fanomalyScore6070.WriteObject(hanomalyScore6070, "anomalyScore6070_run"+run)
fCS6070 = ROOT.TFile("CS6070_run"+run+".root", "CREATE")
fCS6070.WriteObject(hCS6070, "CS6070_run"+run)
print("Histogram 6070 Created.") 
fanomalyScore7080 = ROOT.TFile("anomalyScore7080_run"+run+".root", "CREATE")
fanomalyScore7080.WriteObject(hanomalyScore7080, "anomalyScore7080_run"+run)
fCS7080 = ROOT.TFile("CS7080_run"+run+".root", "CREATE")
fCS7080.WriteObject(hCS7080, "CS7080_run"+run)
print("Histogram 7080 Created.") 
    

"""
# True Pileup
op = "/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/newhistFiles/"
ap = "histPileup_run"

h = o+a+run+'.root'
h2 = op+ap+run+".root"

# CICADA Score
f = ROOT.TFile.Open(h, 'READ')
hist = f.Get(a+run)
hist.SetTitle("")
# True Pileup
f2 = ROOT.TFile.Open(h2, 'READ')
hist2 = f2.Get(ap+run)

nBins = hist2.GetNbinsX()
nCBins = hist.GetNbinsX()


start = 0
stop = 35010
step = 10       
canvas = ROOT.TCanvas('canvas', '', 500, 500)
CICADA_hist = ROOT.TH1F("Run_"+run+" anomalyScore", "Run_"+run+" anomalyScore", nBins, 0.0, 80.0)

for i in tqdm(range(nBins)):
    c = hist2.GetBinContent(i)
    for bin in [range(j, j+step) for j in range(start, stop, step)]:
        if c in bin:
            e = hist.GetBinContent(i)
            CICADA_hist.Fill(e)
            
            if bin in range(0,10):
                CICADA_hist.Draw("HIST")
            else:
                CICADA_hist.Draw("SAME HIST")
            
            
            canvas.Draw()
            canvas.SaveAs('./CICADAPUPlots/Run_'+run+' bins '+str(bin)+'.png')
            canvas.Clear()
canvas.Draw()
canvas.SaveAs("all bins Run " + run + ".png")
"""