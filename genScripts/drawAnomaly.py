import ROOT
import os
import numpy as np
from tqdm import tqdm

ROOT.gStyle.SetOptStat(2210)
ROOT.gStyle.SetStatW(0.3)
ROOT.gStyle.SetStatH(0.105)

o = "/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genScripts/pileupresos/"
b = "hp" # "anomalyScore"
# newhistFiles/
a = ["010", "1020", "2030", "3040", "4050", "5060", "6070", "7080"]
flist = []
# Running the histograms
# runs = ["A","C","D"]
pnames = []
ppnames = []


for j in range(8):
    flist.append(o+b+str(a[j])+'.root')
    pnames.append(b+str(a[j]))
    ppnames.append(b+"p"+str(a[j]))

openfiles = []
hists = []
phists = []

lineColors = np.asarray([46, 30]) # , 38, 40
black = 1
canvas = ROOT.TCanvas('canvas', '', 500, 500)
# canvas.SetLogy()
leg = ROOT.TLegend(0.7, 0.75, 0.87, 0.87)
leg.SetBorderSize(1)
leg.SetFillColor(0)
leg.SetFillStyle(2)
leg.SetTextFont(40)

for i in tqdm(range(8)):
    f = ROOT.TFile.Open(flist[i], 'READ')
    openfiles.append(f)
    hist = f.Get(pnames[i])
    phist = f.Get(ppnames[i])

    hist.SetStats(1)
    hist.SetLineColor(int(lineColors[0]))
    hist.SetMarkerColor(int(lineColors[0]))
    hist.SetMarkerStyle(8)
    hist.SetMarkerSize(0.5)
    hist.SetTitle("Pileup " + a[i])
    hist.GetXaxis().SetTitle("Resolution") # "CICADA Score"
    hist.GetXaxis().SetTitleSize(0.045)
    hist.GetXaxis().SetTitleOffset(0.9)
    hist.GetYaxis().SetTitleSize(0.045)
    hist.GetYaxis().SetTitleOffset(0.9)
    #xMax = hist.GetXaxis().GetXmax() * 1.75
    # yMax = hist.GetMaximum() * 1.25
    # hist.SetMaximum(yMax)
    xmin = min(hist.GetXaxis().GetXmin(), phist.GetXaxis().GetXmin())
    xmax = max(hist.GetXaxis().GetXmax(), phist.GetXaxis().GetXmax())
    ymin = min(hist.GetMinimum(), phist.GetMinimum())
    ymax = max(hist.GetMaximum(), phist.GetMaximum())
    
    hist.GetXaxis().SetRangeUser(xmin, xmax)
    hist.GetYaxis().SetRangeUser(ymin, ymax)

    phist.SetStats(1)
    phist.SetLineColor(int(lineColors[1]))
    phist.SetMarkerColor(int(lineColors[1]))
    phist.SetMarkerStyle(8)
    phist.SetMarkerSize(0.5)
    """phist.GetXaxis().SetRangeUser(phist.GetXaxis().GetXmin(), phist.GetXaxis().GetXmax())
    phist.GetYaxis().SetRangeUser(phist.GetMinimum(), phist.GetMaximum())"""
    
    hists.append(hist)
    phists.append(phist)
    hists[i].Draw("E1")
    leg.AddEntry(hists[i], "True Pileup", "l")
    phists[i].Draw("SAME E1")
    leg.AddEntry(phists[i], "Predicted Pileup", "l")
    
    # Additional Elts/Fits (if needed)
    l = ROOT.TLine(0.0, 0.0, 0.0, ymax)


    hists[i].Fit("gaus")
    fit = hists[i].GetFunction("gaus")
    phists[i].Fit("gaus")
    fit2 = phists[i].GetFunction("gaus")
    fit2.SetLineColor(4)
    l.Draw("SAME")
    # hists[i].SetStats(1)

    leg.AddEntry(fit, "Gaussian Fit True", "l")
    leg.AddEntry(fit2, "Gaussian Fit Predicted", "l")
    # leg.AddEntry(l, "Zero Line")
    ROOT.gPad.Update()
    
    leg.Draw()
    canvas.Draw()
    canvas.SaveAs("./pileupresos/"+pnames[i]+'.png')
    leg.Clear()
    canvas.Clear()