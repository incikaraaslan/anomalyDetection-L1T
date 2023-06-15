import ROOT
import os
import numpy as np
from tqdm import tqdm

ROOT.gStyle.SetOptStat(0)

runs = ["A", "C", "D"]
lineColors = np.asarray([46, 30, 38])
lineColors2 = np.asarray([45, 31, 37])
black = 1
canvas = ROOT.TCanvas('canvas', '', 500, 500)
ROOT.gStyle.SetOptStat(False)
 
o = "/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genScripts/"
a = "histPileup_run"
b = "histPileupPred_run"


"""
# print("Openıng fıle")
f1 = ROOT.TFile.Open(o+a+runs[0]+'.root', 'READ')
# print("File opened")
# f1.ls()
canvas1 = ROOT.TCanvas('canvas1', '', 500, 500)
# print("Getting histogram")
# print(f"histogram {a+runs[0]}")
hist1 = f1.Get(a+runs[0])
# print("Got histogram")
# print(type(hist1))
hist1.Draw()
canvas1.Draw()
canvas1.SaveAs("hpileupRun"+ runs[0] + ".png")
print("Image 1 Saved.")
"""
# print(o+a+runs[0]+'.root', o+b+runs[0]+'.root')

flist = [o+a+runs[0]+'.root', o+a+runs[1]+'.root', o+a+runs[2]+'.root']
flist2 = [o+b+runs[0]+'.root', o+b+runs[1]+'.root', o+b+runs[2]+'.root']
openfiles = []
openfiles2 = []
hists = []
hists2 = []

leg = ROOT.TLegend(0.7, 0.75, 0.87, 0.87)
leg.SetBorderSize(1)
leg.SetFillColor(0)
leg.SetFillStyle(2)
leg.SetTextFont(40)

for i in tqdm(range(3)):

    # Take from each file
    f = ROOT.TFile.Open(flist[i], 'READ')
    openfiles.append(f)
    hist = f.Get(a+runs[i])
    
    f2 = ROOT.TFile.Open(flist2[i], 'READ')
    openfiles2.append(f2)
    hist2 = f2.Get(b+runs[i])

    hist.SetLineColor(int(lineColors[i]))
    hist.SetMarkerColor(int(lineColors[i]))
    hist.SetMarkerStyle(8)
    hist.SetMarkerSize(0.5)
    hist.SetTitle("")
    hist.GetXaxis().SetTitle("CICADA Threshold")
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

    
    hist2.SetLineColor(int(lineColors2[i]))
    hist2.SetMarkerColor(int(lineColors2[i]))
    hist2.SetMarkerStyle(8)
    hist2.SetMarkerSize(0.5)
    hist2.SetTitle("")
    hist2.GetXaxis().SetTitle("CICADA Threshold")
    hist2.GetXaxis().SetTitleSize(0.045)
    hist2.GetXaxis().SetTitleOffset(0.9)
    hist2.GetYaxis().SetTitleSize(0.045)
    hist2.GetYaxis().SetTitleOffset(0.9)
    #xMax = hist.GetXaxis().GetXmax() * 1.75
    yMax2 = hist2.GetMaximum() * 1.25
    hist2.SetMaximum(yMax2)
    #hist.GetXaxis().SetLimits(1, xMax)
    hist2.SetMinimum(0.1)
    hists2.append(hist2)


    hists[i].GetXaxis().SetRangeUser(0.01,1.0)
    hists2[i].GetXaxis().SetRangeUser(0.01,1.0)

    if i == 0:
        print("First Histogram")
        hists[i].Draw("E1")
        hists2[i].Draw("SAME E1")
    else:
        print("Duplicate Histograms")
        hists[i].Draw("SAME E1")
        hists2[i].Draw("SAME E1")
    leg.AddEntry(hists[i], "True Run " + runs[i], "l")
    leg.AddEntry(hists2[i], "Predicted Run " + runs[i], "l")

leg.Draw()
canvas.Draw()
canvas.SaveAs('PilvPred.png')
