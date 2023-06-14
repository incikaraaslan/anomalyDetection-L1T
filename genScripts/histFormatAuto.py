
#include "TCanvas.h"
#include "TStyle.h"
#include "TH1.h"
#include "TGaxis.h"
#include "TRandom.h"

import ROOT
import os
import numpy as np
from tqdm import tqdm

ROOT.gStyle.SetOptStat(0)

# Running which plot for all 3 runs
selectPlot = int(input("Please select the type of plot desired (1: CICADA, 2: CICADA/SNAIL, 3: CICADA/SNAIL**2) : "))
listofPlots = {"1": "CICADA", "2": "CICADA/SNAIL", "3": "CICADA/SNAIL**2"}
b = np.asarray(list(listofPlots.keys())).astype(int)
while not (selectPlot in b):
    selectPlot = int(input("Please select the type of plot desired (1: CICADA, 2: CICADA/SNAIL, 3: CICADA/SNAIL**2, 4: SNAIL v. Pileup) : "))

o = "/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genScripts/newhistFiles/"
# newhistFiles/
a = ''
if selectPlot == 1:
    a = 'histCICADA_run'
elif selectPlot == 2:
    a = 'histCS_run'
elif selectPlot == 3:
    a = 'histCS2_run'

# Running the histograms
runs = ["A", "B", "C", "D"] # 'B' whenever I have that for pileup lol
lineColors = np.asarray([46, 30, 38, 40])
black = 1
canvas = ROOT.TCanvas('canvas', '', 500, 500)
# canvas.SetLogy()
# canvas.SetLogx()
ROOT.gStyle.SetOptStat(False)
 
flist = [o+a+runs[0]+'.root', o+a+runs[1]+'.root', o+a+runs[2]+'.root', o+a+runs[3]+'.root']
openfiles = []
hists = []

leg = ROOT.TLegend(0.7, 0.75, 0.87, 0.87)
leg.SetBorderSize(1)
leg.SetFillColor(0)
leg.SetFillStyle(2)
leg.SetTextFont(40)

for i in tqdm(range(4)):
    f = ROOT.TFile.Open(flist[i], 'READ')
    openfiles.append(f)
    hist = f.Get(a+runs[i])
    hist.SetLineColor(int(lineColors[i]))
    hist.SetMarkerColor(int(lineColors[i]))
    hist.SetMarkerStyle(8)
    hist.SetMarkerSize(0.5)
    hist.SetTitle("")
    hist.GetXaxis().SetTitle(listofPlots[str(selectPlot)])
    hist.GetXaxis().SetTitleSize(0.045)
    hist.GetXaxis().SetTitleOffset(0.9)
    hist.GetYaxis().SetTitleSize(0.045)
    hist.GetYaxis().SetTitleOffset(0.9)
    #xMax = hist.GetXaxis().GetXmax() * 1.75
    yMax = hist.GetMaximum() * 1.25
    hist.SetMaximum(yMax)
    #hist.GetXaxis().SetLimits(1, xMax)
    hist.SetMinimum(0.1)
    hists.append(hist)
    if selectPlot == 1:
        hists[i].GetXaxis().SetRangeUser(0.1,10.0)
    else:
        hists[i].GetXaxis().SetRangeUser(0.01,1.0)
    if i == 0:
        print("First Histogram")
        hists[i].Draw("E1")
    else:
        print("Duplicate Histograms")
        hists[i].Draw("SAME E1")
    leg.AddEntry(hists[i], "Run " + runs[i], "l")

leg.Draw()
canvas.Draw()
canvas.SaveAs(a+'.png')
