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
hPileup = ROOT.TH1F("Pileup "+run, "True Pileup", 80, 0.0, 80.0)
hanomalyScore010 = ROOT.TH1F("Anomaly Score "+run+" 0-10", "Anomaly Score for 0-10", 80, 0.0, 80.0)
hanomalyScore1020 = ROOT.TH1F("Anomaly Score "+run+" 10-20", "Anomaly Score 10-20", 80, 0.0, 80.0)
hanomalyScore2030 = ROOT.TH1F("Anomaly Score "+run+" 20-30", "Anomaly Score 20-30", 80, 0.0, 80.0)
hanomalyScore3040 = ROOT.TH1F("Anomaly Score "+run+" 30-40", "Anomaly Score 30-40", 80, 0.0, 80.0)
hanomalyScore4050 = ROOT.TH1F("Anomaly Score "+run+" 40-50", "Anomaly Score 40-50", 80, 0.0, 80.0)
hanomalyScore5060 = ROOT.TH1F("Anomaly Score "+run+" 50-60", "Anomaly Score 50-60", 80, 0.0, 80.0)
hanomalyScore6070 = ROOT.TH1F("Anomaly Score "+run+" 60-70", "Anomaly Score 60-70", 80, 0.0, 80.0)
hanomalyScore7080 = ROOT.TH1F("Anomaly Score "+run+" 70-80", "Anomaly Score 70-80", 80, 0.0, 80.0)

for i in tqdm(range(chains['anomalyChain'].GetEntries())):
    chains['anomalyChain'].GetEntry(i)
    chains['PUChain'].GetEntry(i)
    truePileup = chains['anomalyChain'].npv
    anomalyScore = truePileup = chains['anomalyChain'].anomalyScore
    if truePileup in range(0,10):
        hanomalyScore010.Fill(anomalyScore)
    elif truePileup in range(10,20):
        hanomalyScore1020.Fill(anomalyScore)
    elif truePileup in range(20,30):
        hanomalyScore2030.Fill(anomalyScore)
    elif truePileup in range(30,40):
        hanomalyScore3040.Fill(anomalyScore)
    elif truePileup in range(40,50):
        hanomalyScore4050.Fill(anomalyScore)
    elif truePileup in range(50,60):
        hanomalyScore5060.Fill(anomalyScore)
    elif truePileup in range(60,70):
        hanomalyScore6070.Fill(anomalyScore)
    elif truePileup in range(70,80):
        hanomalyScore7080.Fill(anomalyScore)

fanomalyScore010 = ROOT.TFile("anomalyScore010_run"+run+".root", "CREATE")
fanomalyScore010.WriteObject(hanomalyScore010, "anomalyScore010_run"+run)
print("Histogram 010 Created.") 
fanomalyScore1020 = ROOT.TFile("anomalyScore1020_run"+run+".root", "CREATE")
fanomalyScore1020.WriteObject(hanomalyScore1020, "anomalyScore1020_run"+run)
print("Histogram 1020 Created.") 
fanomalyScore2030 = ROOT.TFile("anomalyScore2030_run"+run+".root", "CREATE")
fanomalyScore2030.WriteObject(hanomalyScore2030, "anomalyScore2030_run"+run)
print("Histogram 2030 Created.")
fanomalyScore3040 = ROOT.TFile("anomalyScore3040_run"+run+".root", "CREATE")
fanomalyScore3040.WriteObject(hanomalyScore3040, "anomalyScore3040_run"+run)
print("Histogram 3040 Created.") 
fanomalyScore4050 = ROOT.TFile("anomalyScore4050_run"+run+".root", "CREATE")
fanomalyScore4050.WriteObject(hanomalyScore4050, "anomalyScore4050_run"+run)
print("Histogram 4050 Created.") 
fanomalyScore5060 = ROOT.TFile("anomalyScore5060_run"+run+".root", "CREATE")
fanomalyScore5060.WriteObject(hanomalyScore5060, "anomalyScore5060_run"+run)
print("Histogram 5060 Created.") 
fanomalyScore6070 = ROOT.TFile("anomalyScore6070_run"+run+".root", "CREATE")
fanomalyScore6070.WriteObject(hanomalyScore6070, "anomalyScore6070_run"+run)
print("Histogram 6070 Created.") 
fanomalyScore7080 = ROOT.TFile("anomalyScore7080_run"+run+".root", "CREATE")
fanomalyScore7080.WriteObject(hanomalyScore7080, "anomalyScore7080_run"+run)
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