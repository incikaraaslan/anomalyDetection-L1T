import ROOT
from ROOT import RooRealVar, RooFit, RooArgList, RooArgSet
import os
import numpy as np
from tqdm import tqdm

ROOT.gStyle.SetOptStat(2210)
ROOT.gStyle.SetStatW(0.3)
ROOT.gStyle.SetStatH(0.105)

o = "/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genTrainML/output/"
b = "hp" # "anomalyScore"
# newhistFiles/
a = ["010exp", "1020exp", "2030exp", "3040exp", "4050exp", "5060exp", "6070exp", "7080exp"]
flist = []
# Running the histograms
# runs = ["A","C","D"]
pnames = []


for j in range(8):
    flist.append(o+b+str(a[j])+'.root')
    pnames.append(b+str(a[j]))

openfiles = []
hists = []

lineColors = np.asarray([46, 30]) # , 38, 40
black = 1
canvas = ROOT.TCanvas('canvas', '', 500, 500)
# canvas.SetLogy()
leg = ROOT.TLegend(0.7, 0.65, 0.87, 0.77)
leg.SetBorderSize(1)
leg.SetFillColor(0)
leg.SetFillStyle(2)
leg.SetTextFont(40)

for i in tqdm(range(8)):
    f = ROOT.TFile.Open(flist[i], 'READ')
    openfiles.append(f)
    hist = f.Get(pnames[i])

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
    """xmin = 3 * hist.GetXaxis().GetXmin()
    xmax = 5 * hist.GetXaxis().GetXmax()
    ymin = hist.GetMinimum()
    ymax = 3 * hist.GetMaximum()"""
    
    hists.append(hist)
    hists[i].Fit("gaus")
    fit = hists[i].GetFunction("gaus")

    """xmin = 1.5 * min(hist.GetXaxis().GetXmin(), fit.GetXaxis().GetXmin())
    xmax = 3 * max(hist.GetXaxis().GetXmax(), fit.GetXaxis().GetXmax())
    ymin = 1.5 * min(hist.GetMinimum(),fit.GetMinimum())
    ymax = 1.5 * max(hist.GetMaximum(),fit.GetMaximum())
    hist.GetXaxis().SetRangeUser(xmin, xmax)
    hist.GetYaxis().SetRangeUser(ymin, ymax)"""

    hists[i].Draw("E1")
    leg.AddEntry(hists[i], "True Pileup", "l")
    leg.AddEntry(fit, "Gaussian Fit True", "l")
    
    # Additional Elts/Fits (if needed)
    l = ROOT.TLine(0.0, 0.0, 0.0, 200)
    l.Draw("SAME")

    ROOT.gPad.Update()
    
    leg.Draw()
    canvas.Draw()
    canvas.SaveAs("./output/"+pnames[i]+'.png')
    leg.Clear()
    canvas.Clear()