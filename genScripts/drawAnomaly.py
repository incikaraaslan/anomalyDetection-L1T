import ROOT
import os
import numpy as np
from tqdm import tqdm

ROOT.gStyle.SetOptStat(0)

o = "/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genScripts/CICADAPUPlots/"
b = "anomalyScore"
# newhistFiles/
a = ["010_run", "1020_run", "2030_run", "3040_run", "4050_run", "5060_run", "6070_run", "7080_run"]
flist = []
# Running the histograms
runs = ["A","C","D"]
names = []

for i in range(3):
    for j in range(8):
        flist.append(o+b+str(a[j])+str(runs[i])+'.root')
        names.append(b+str(a[j])+str(runs[i]))

openfiles = []
hists = []

lineColors = np.asarray([46, 30, 38, 40])
black = 1
canvas = ROOT.TCanvas('canvas', '', 500, 500)
#canvas.SetLogx()
"""
leg = ROOT.TLegend(0.7, 0.75, 0.87, 0.87)
leg.SetBorderSize(1)
leg.SetFillColor(0)
leg.SetFillStyle(2)
leg.SetTextFont(40)
"""
for i in tqdm(range(24)):
    f = ROOT.TFile.Open(flist[i], 'READ')
    openfiles.append(f)
    hist = f.Get(names[i])
    hist.SetLineColor(int(lineColors[0]))
    hist.SetMarkerColor(int(lineColors[0]))
    hist.SetMarkerStyle(8)
    hist.SetMarkerSize(0.5)
    hist.SetTitle("")
    hist.GetXaxis().SetTitle("CICADA Score")
    hist.GetXaxis().SetTitleSize(0.045)
    hist.GetXaxis().SetTitleOffset(0.9)
    hist.GetYaxis().SetTitleSize(0.045)
    hist.GetYaxis().SetTitleOffset(0.9)
    #xMax = hist.GetXaxis().GetXmax() * 1.75
    yMax = hist.GetMaximum() * 1.25
    hist.SetMaximum(yMax)
    if i in range(i, i+8):
        hist.GetXaxis().SetLimits(, xMax)
    hists.append(hist)
    hists[i].Draw("E1")
    canvas.Draw()
    canvas.SaveAs("./CICADAPUPlots/"+names[i]+'.png')