
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

# Running which plot for all 4 runs
selectPlot = int(input("Please select the type of plot desired (1: CICADA, 2: CICADA/SNAIL, 3: CICADA/SNAIL**2) : "))
listofPlots = {"1": "CICADA", "2": "CICADA/SNAIL", "3": "CICADA/SNAIL**2"}
b = np.asarray(list(listofPlots.keys())).astype(int)
while not (selectPlot in b):
    selectPlot = int(input("Please select the type of plot desired (1: CICADA, 2: CICADA/SNAIL, 3: CICADA/SNAIL**2) : "))

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
runs = ["A","B","C", "D"]
lineColors = np.asarray([46, 30, 38, 40])
black = 1
canvas = ROOT.TCanvas('canvas', '', 500, 500)
ROOT.gStyle.SetOptStat(False)
 
flist = [o+a+runs[0]+'.root', o+a+runs[1]+'.root', o+a+runs[2]+'.root', o+a+runs[3]+'.root']
hstack = ROOT.THStack("stack", "")

leg = ROOT.TLegend(0.7, 0.75, 0.87, 0.87)
leg.SetBorderSize(1)
leg.SetFillColor(0)
leg.SetFillStyle(2)
leg.SetTextFont(40)

# Loop over to draw the histograms:
for i in tqdm(range(4)):
    f = ROOT.TFile.Open(flist[i], 'READ')
    hist = f.Get(a+runs[i])

    hist.SetLineColor(int(lineColors[i]))
    hist.SetMarkerColor(int(lineColors[i]))
    hist.SetTitle("")
    hist.GetXaxis().SetTitle(listofPlots[str(selectPlot)]) 
    hist.GetXaxis().SetTitleSize(0.045)  
    hist.GetXaxis().SetTitleOffset(0.9)                                   
    hist.GetYaxis().SetTitleSize(0.045)
    hist.GetYaxis().SetTitleOffset(0.9)      
    yMax = hist.GetMaximum() * 1.25                 
    hist.SetMaximum(yMax)                                               
    hist.SetMinimum(0.01) 
    if selectPlot == 1:
        hist.GetXaxis().SetRangeUser(0.0,10.0)     
    else:
        hist.GetXaxis().SetRangeUser(0.0,1.0)
    ROOT.gROOT.cd() 
    hnew = hist.Clone()
    
    leg.AddEntry(hist, "Run " + runs[i], "l")
    hstack.Add(hnew)

hstack.Draw("nostack")
leg.Draw()
canvas.SaveAs("histN_run.png")

# Error Bars Here
"""histErr = f.Get(a+runs[0])
ROOT.gStyle.SetEndErrorSize(3)
histErr.SetLineColor(black)
histErr.Draw("E1")
canvas.Update()

hist2Err= f2.Get(a+runs[1])
hist2Err.SetLineColor(black)
hist2Err.Draw("E1")"""
# Legend Here
"""leg = ROOT.TLegend(0.7, 0.75, 0.87, 0.87)
leg.SetBorderSize(1)
leg.SetFillColor(0)
leg.SetFillStyle(2)
leg.SetTextFont(40)
leg.SetTextSize(0.035)
leg.AddEntry(hist, "Run " + runs[0], "l")
leg.AddEntry(hist2, "Run " + runs[1], "l")
leg.Draw()"""



"""
for i in tqdm(range(1)):
    i += 1
    f = ROOT.TFile.Open(o+a+runs[i]+'.root', 'READ')
    hist2 = f.Get(a+runs[i])
    # Draw the Histogram
    hist2.Draw("SAME")
    if selectPlot == 1:
        hist2.GetXaxis().SetRangeUser(0.0,10.0)
    else:
        hist2.GetXaxis().SetRangeUser(0.0,1.0)
    # Plot the Error Bars
    if i == 0:
        hist.Draw("E1")
    else:
        hist.Draw("SAME E1")
    
    legend = ROOT.TLegend(0.1,0.7,0.48,0.9)
    legend.AddEntry("Run " + runs[i])

canvas.Draw()
canvas.SaveAs('histt_run.png')"""
