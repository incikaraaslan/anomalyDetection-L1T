import ROOT
import os
import numpy as np
from tqdm import tqdm

ROOT.gStyle.SetOptStat(0)

runs = ["A", "C", "D"]
lineColors = np.asarray([46, 30, 38])
lineColors2 = np.asarray([45, 31, 37])
black = 1
ROOT.gStyle.SetOptStat(False)
 
o = "/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/newhistFiles/"
a = "histPileup_run"
b = "histPred_run"
b2 = "histPileupPred_run"
c = "histPredPileup_run"


flist = [o+a+runs[0]+'.root', o+a+runs[1]+'.root', o+a+runs[2]+'.root']
flist2 = [o+b+runs[0]+'.root', o+b+runs[1]+'.root', o+b+runs[2]+'.root']
flist3 = [o+c+runs[0]+'.root', o+c+runs[1]+'.root', o+c+runs[2]+'.root']
openfiles = []
openfiles2 = []
openfiles3 = []
hists = []
hists2 = []
hists3 = []

# Creating Canvas Pads

canvas = ROOT.TCanvas('C', 'Canvas', 500, 500)

pileupPad = ROOT.TPad("Pad 1", "Pad 1", 0, 0.5, 0.5, 1.0)
pileupPad.SetLogy()
# canvas.SetLogx()
# pileg = pileupPad.BuildLegend()
"""pileg.SetBorderSize(1)
pileg.SetFillColor(0)
pileg.SetFillStyle(2)
pileg.SetTextFont(40)"""
pileupPad.Draw()

canvas.cd()
predictionPad = ROOT.TPad("Pad 2", "Pad 2", 0.5, 0.5, 1.0, 1.0)
predictionPad.SetLogy()
# predleg = predictionPad.BuildLegend()
"""predleg.SetBorderSize(1)
predleg.SetFillColor(0)
predleg.SetFillStyle(2)
predleg.SetTextFont(40)"""
predictionPad.Draw()

canvas.cd()
predvpileupPad = ROOT.TPad("Pad 3", "Pad 3", 0, 0, 1, 0.5)
predvpileupPad.SetLogy()
# ppleg = predvpileupPad.BuildLegend()
"""ppleg.SetBorderSize(1)
ppleg.SetFillColor(0)
ppleg.SetFillStyle(2)
ppleg.SetTextFont(40)"""
predvpileupPad.Draw()
canvas.cd()

# Legend Setup
"""leg = ROOT.TLegend() # 0.63, 0.7, 0.885, 0.88
leg.SetBorderSize(1)
leg.SetFillColor(0)
leg.SetFillStyle(2)
leg.SetTextFont(40)"""

for i in tqdm(range(3)):

    # Take from each file
    f = ROOT.TFile.Open(flist[i], 'READ')
    openfiles.append(f)
    hist = f.Get(a+runs[i])
    hist.SetName("Run " + runs[i])
    
    f2 = ROOT.TFile.Open(flist2[i], 'READ')
    openfiles2.append(f2)
    hist2 = f2.Get(b2+runs[i])
    hist2.SetName("Run " + runs[i])

    f3 = ROOT.TFile.Open(flist3[i], 'READ')
    openfiles3.append(f3)
    hist3 = f3.Get(c+runs[i])
    hist3.SetName("Run " + runs[i])

    hist.SetLineColor(int(lineColors[i]))
    hist.SetMarkerColor(int(lineColors[i]))
    hist.SetMarkerStyle(8)
    hist.SetMarkerSize(0.2)
    hist.SetTitle("")
    hist.GetYaxis().SetTitle("True Pileup")
    hist.GetXaxis().SetTitle("CICADA Threshold")
    hist.GetXaxis().SetTitleSize(0.045)
    hist.GetXaxis().SetTitleOffset(1.1)
    hist.GetYaxis().SetTitleSize(0.045)
    hist.GetYaxis().SetTitleOffset(1.0)
    #xMax = hist.GetXaxis().GetXmax() * 1.75
    yMax = hist.GetMaximum() * 1.75
    hist.SetMaximum(yMax)
    #hist.GetXaxis().SetLimits(1, xMax)
    yMin = hist.GetMinimum() * 1.75
    if yMin == 0:
        hist.SetMinimum(0.01)
    else:
        hist.SetMinimum(yMin)
    hists.append(hist)

    
    hist2.SetLineColor(int(lineColors[i]))
    hist2.SetMarkerColor(int(lineColors[i]))
    hist2.SetMarkerStyle(8)
    hist2.SetMarkerSize(0.2)
    hist2.SetTitle("")
    hist2.GetYaxis().SetTitle("SNAIL Prediction")
    hist2.GetXaxis().SetTitle("CICADA Threshold")
    hist2.GetXaxis().SetTitleSize(0.045)
    hist2.GetXaxis().SetTitleOffset(1.2)
    hist2.GetYaxis().SetTitleSize(0.045)
    hist2.GetYaxis().SetTitleOffset(1.0)
    #xMax = hist.GetXaxis().GetXmax() * 1.75
    yMax2 = hist2.GetMaximum() * 1.75
    hist2.SetMaximum(yMax2)
    #hist.GetXaxis().SetLimits(1, xMax)
    yMin2 = hist.GetMinimum() * 1.75
    if yMin2 == 0:
        hist2.SetMinimum(0.01)
    else:
        hist2.SetMinimum(yMin2)
    hists2.append(hist2)

    hist3.SetLineColor(int(lineColors[i]))
    hist3.SetMarkerColor(int(lineColors[i]))
    hist3.SetMarkerStyle(8)
    hist3.SetMarkerSize(0.2)
    hist3.SetTitle("")
    hist3.GetYaxis().SetTitle("SNAIL/True Pileup")
    hist3.GetXaxis().SetTitle("CICADA Threshold")
    hist3.GetXaxis().SetTitleSize(0.045)
    hist3.GetXaxis().SetTitleOffset(1.0)
    hist3.GetYaxis().SetTitleSize(0.045)
    hist3.GetYaxis().SetTitleOffset(1.0)
    #xMax = hist.GetXaxis().GetXmax() * 1.75
    yMax3 = hist3.GetMaximum() * 1.75
    hist3.SetMaximum(yMax3)
    #hist.GetXaxis().SetLimits(1, xMax)
    yMin3 = hist.GetMinimum() * 1.75
    if yMin3 == 0:
        hist3.SetMinimum(0.01)
    else:
        hist3.SetMinimum(yMin3)
    hists3.append(hist3)
    
    # hists.append(hist2)
    hists[i].GetXaxis().SetRangeUser(0.0,10.0)
    hists2[i].GetXaxis().SetRangeUser(0.0,10.0)
    hists3[i].GetXaxis().SetRangeUser(0.0,10.0)

    if i == 0:
        pileupPad.cd()
        hists[i].Draw("E1")
        # hists[i].Draw("SAME HIST")
        # pileupPad.Update()
        
        canvas.cd()
        predictionPad.cd()
        hists2[i].Draw("E1")
        # hists2[i].Draw("SAME HIST")
        # predictionPad.Update()

        canvas.cd()
        predvpileupPad.cd()
        hists3[i].Draw("E1")
        # hists3[i].Draw("SAME HIST")
        # predvpileupPad.Update()
        canvas.cd()

    else:
        pileupPad.cd()
        hists[i].Draw("SAME E1")
        # hists[i].Draw("SAME HIST")
        # pileupPad.Update()

        canvas.cd()
        predictionPad.cd()
        hists2[i].Draw("SAME E1")
        # hists2[i].Draw("SAME HIST")
        # predictionPad.Update()

        canvas.cd()
        predvpileupPad.cd()
        hists3[i].Draw("SAME E1")
        # hists3[i].Draw("SAME HIST")
        # predvpileupPad.Update()
        canvas.cd()
    
    
    """leg.AddEntry(hists2[i], "Run " + runs[i], "l")
    leg.AddEntry(hists3[i], "Run " + runs[i], "l")

    canvas.cd()
    predictionPad.cd()
    

    canvas.cd()
    predvpileupPad.cd()
    
    canvas.cd()"""


predvpileupPad.cd()
ppleg = predvpileupPad.BuildLegend(0.7, 0.25, 0.87, 0.37)
ppleg.Draw()

predictionPad.cd()
predleg = predictionPad.BuildLegend(0.7, 0.25, 0.87, 0.37)
predleg.Draw()

pileupPad.cd()
pileg = pileupPad.BuildLegend(0.7, 0.25, 0.87, 0.37)
pileg.Draw()

canvas.Draw()
canvas.SaveAs('SNAILPileup.png')
