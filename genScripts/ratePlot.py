import ROOT
import os
import numpy as np
from tqdm import tqdm

ROOT.gStyle.SetOptStat(0)

# Running which plot for all 4 runs
selectPlot = int(input("Please select the type of plot desired (1: CICADA, 2: CICADA/SNAIL, 3: CICADA/SNAIL**2) : "))
listofPlots = {"1": "CICADA", "2": "CICADA/SNAIL", "3": "CICADA/SNAIL**2"}
b = np.asarray(list(listofPlots.keys())).astype(int)
while not (selectPlot in b):
    selectPlot = int(input("Please select the type of plot desired (1: CICADA, 2: CICADA/SNAIL, 3: CICADA/SNAIL**2) : "))

o = "/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genScripts/"
# newhistFiles/
a = ''
if selectPlot == 1:
    a = 'histCICADA_run'
elif selectPlot == 2:
    a = 'histCS_run'
elif selectPlot == 3:
    a = 'histCS2_run'

# Running the histograms
runs = ["A","C", "D"]
flist = [o+a+runs[0]+'.root', o+a+runs[1]+'.root', o+a+runs[2]+'.root']
openfiles = []
hists = []
eHists = []

lineColors = np.asarray([46, 30, 38, 40])
black = 1
canvas = ROOT.TCanvas('canvas', '', 500, 500)
canvas.SetLogx()
canvas.SetLogy()
leg = ROOT.TLegend(0.13, 0.15, 0.30, 0.27)
leg.SetBorderSize(1)
leg.SetFillColor(0)
leg.SetFillStyle(2)
leg.SetTextFont(40)
for i in tqdm(range(3)):
    # Resolving ROOTs memory issues by making sure both the file and the histogram is saved somewhere.
    f = ROOT.TFile.Open(flist[i], 'READ')
    openfiles.append(f)
    hist = f.Get(a+runs[i])
    hists.append(hist)

    nBins = hists[i].GetNbinsX() # 100

    # Create Efficiency Histogram
    if selectPlot == 1:
        efficiencyHist = ROOT.TH1F("Run "+runs[i]+" Efficiency", "Run "+runs[i]+" Efficiency", nBins, 0.1, 10.0)
    else:
        efficiencyHist = ROOT.TH1F("Run "+runs[i]+" Efficiency", "Run "+runs[i]+" Efficiency", nBins, 0.01, 1.0)
    
    # Iterate through X Bins for each histogram
    zeroBiasRate = 28609 # in kHz
    for j in tqdm(range(nBins)):
        e = hists[i].GetBinContent(j)
        total = hists[i].Integral()
        above_t= hists[i].Integral(nBins-j, nBins)
        perc = above_t/total * zeroBiasRate
        efficiencyHist.SetBinContent(nBins-j, perc)
    efficiencyHist.SetLineColor(int(lineColors[i]))
    efficiencyHist.SetMarkerColor(int(lineColors[i]))
    efficiencyHist.SetTitle("")
    efficiencyHist.GetXaxis().SetTitle(listofPlots[str(selectPlot)]+" Threshold")
    efficiencyHist.GetYaxis().SetTitle("L1 Trigger Rate (kHz)")
    efficiencyHist.SetMarkerStyle(8)
    efficiencyHist.SetMarkerSize(0.5)
    efficiencyHist.GetXaxis().SetTitleSize(0.035)
    efficiencyHist.GetXaxis().SetTitleOffset(1.2)
    efficiencyHist.GetYaxis().SetTitleSize(0.035)
    efficiencyHist.GetYaxis().SetTitleOffset(1.2)
    #xMax = hist.GetXaxis().GetXmax() * 1.75
    yMax = efficiencyHist.GetMaximum() * 1.25
    eHists.append(efficiencyHist)
    efficiencyHist.SetMaximum(yMax)
    if i == 0:
        print("First Histogram")
        eHists[i].Draw("HIST")
    else:
        print("Duplicate Histograms")
        eHists[i].Draw("SAME HIST")
    leg.AddEntry(eHists[i], "Run " + runs[i], "l")

leg.Draw()
canvas.Draw()
canvas.SaveAs('INCI'+a+'rate.png')

