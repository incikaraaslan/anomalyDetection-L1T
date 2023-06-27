import ROOT
from tqdm import tqdm
import os
import prepChains as pc
import numpy as np
import math

ROOT.gStyle.SetOptStat(0)

# Get CICADA Score and True Pileup
run = input("Which Run?")
# CICADA OR C/S
selectPlot = int(input("Please select the type of plot desired (1: CICADA, 2: CICADA/SNAIL) : "))
listofPlots = {"1": "CICADA", "2": "CICADA/SNAIL"}
b = np.asarray(list(listofPlots.keys())).astype(int)
while not (selectPlot in b):
    selectPlot = int(input("Please select the type of plot desired (1: CICADA, 2: CICADA/SNAIL) : "))

o = "/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/newhistFiles/"
a = ''
if selectPlot == 1:
    a = 'histCICADA_run'
elif selectPlot == 2:
    a = 'histCS_run'

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
            """
            if bin in range(0,10):
                CICADA_hist.Draw("HIST")
            else:
                CICADA_hist.Draw("SAME HIST")
            
            """
            canvas.Draw()
            canvas.SaveAs('./CICADAPUPlots/Run_'+run+' bins '+str(bin)+'.png')
            canvas.Clear()
"""canvas.Draw()
canvas.SaveAs("all bins Run " + run + ".png")"""
        


