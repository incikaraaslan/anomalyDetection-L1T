import ROOT
import os
import numpy as np
from tqdm import tqdm

ROOT.gStyle.SetOptStat(0)

runs = ["", "A", "C", "D"]
lineColors = np.asarray([46, 30, 38, 40])
lineColors2 = np.asarray([45, 31, 37, 41])
black = 1
ROOT.gStyle.SetOptStat(False)
 
o = "/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genScripts/"
a = "histPileup_run"
b = "histPred_run"
# b2 = "histPileupPred_run"
c = "histPredPileup_run"


flist = [o+a+runs[0]+'.root', o+a+runs[1]+'.root', o+a+runs[2]+'.root', o+a+runs[3]+'.root']
flist2 = [o+b+runs[0]+'.root', o+b+runs[1]+'.root', o+b+runs[2]+'.root', o+b+runs[3]+'.root']
flist3 = [o+c+runs[0]+'.root', o+c+runs[1]+'.root', o+c+runs[2]+'.root', o+c+runs[3]+'.root']
openfiles = []
openfiles2 = []
openfiles3 = []
hists = []
hists2 = []
hists3 = []
maxlist1 = []
maxlist2 = []
maxlist3 = []

# Creating Canvas Pads

canvas = ROOT.TCanvas('C', 'Canvas', 500, 500)
mcratioPad = ROOT.TPad("Pad 1", "Pad 1", 0, 0.5, 1, 1)
mcratioPad.SetLogy()
mcratioPad.Draw()

canvas.cd()
dataratioPad = ROOT.TPad("Pad 3", "Pad 3", 0, 0, 1, 0.5)
dataratioPad.SetLogy()
dataratioPad.Draw()
canvas.cd()

leg = ROOT.TLegend(0.63, 0.60, 0.90, 0.90) # 0.72, 0.68, 0.89, 0.80
leg.SetBorderSize(1)
leg.SetFillColor(10)
leg.SetFillStyle(2)
leg.SetTextFont(40)

for i in tqdm(range(4)):

    # Take from each file
    f = ROOT.TFile.Open(flist[i], 'READ')
    openfiles.append(f)
    hist = f.Get(a+runs[i])
    hist.SetName("Run " + runs[i])
    
    f2 = ROOT.TFile.Open(flist2[i], 'READ')
    openfiles2.append(f2)
    hist2 = f2.Get(b+runs[i])
    hist2.SetName("Run " + runs[i])

    hist.SetLineColor(int(lineColors[i]))
    hist.SetMarkerColor(int(lineColors[i]))
    hist.SetMarkerStyle(8)
    hist.SetMarkerSize(0.2)
    hist.SetTitle("")
    hist.GetYaxis().SetTitle("Events")
    hist.GetXaxis().SetTitle("Pileup")
    hist.GetXaxis().SetTitleSize(0.045)
    hist.GetXaxis().SetTitleOffset(1.1)
    hist.GetYaxis().SetTitleSize(0.045)
    hist.GetYaxis().SetTitleOffset(1.0)
    #xMax = hist.GetXaxis().GetXmax() * 1.75
    yMax = hist.GetMaximum() * 1.75
    maxlist1.append(yMax)
    if i == 2:
        yMaxn = np.max(np.asarray(maxlist1))
        hist.SetMaximum(yMaxn)
    hist.SetMinimum(0.1)
    hists.append(hist)

    
    hist2.SetLineColor(int(lineColors2[i]))
    hist2.SetMarkerColor(int(lineColors2[i]))
    hist2.SetMarkerStyle(8)
    hist2.SetMarkerSize(0.2)
    hist2.SetTitle("")
    hist2.GetYaxis().SetTitle("Events")
    hist2.GetXaxis().SetTitle("SNAIL Prediction")
    hist2.GetXaxis().SetTitleSize(0.045)
    hist2.GetXaxis().SetTitleOffset(1.1)
    hist2.GetYaxis().SetTitleSize(0.045)
    hist2.GetYaxis().SetTitleOffset(1.0)
    yMax2 = hist2.GetMaximum() * 1.75
    maxlist2.append(yMax2)
    if i == 2:
        yMax2n = np.max(np.asarray(maxlist2))
        hist2.SetMaximum(yMax2n * 1.75)
    hist2.SetMinimum(0.1)
    hists2.append(hist2)

    hist3 = hist2.Clone()
    hist3.Divide(hist)
    hist3.SetLineColor(int(lineColors[i]))
    hist3.SetMarkerColor(int(lineColors[i]))
    hist3.SetMarkerStyle(8)
    hist3.SetMarkerSize(0.2)
    hist3.SetTitle("")
    hist3.GetYaxis().SetTitle("Events")
    hist3.GetXaxis().SetTitle("Ratio")
    hist3.GetXaxis().SetTitleSize(0.06)
    hist3.GetXaxis().SetTitleOffset(0.7)
    hist3.GetYaxis().SetTitleSize(0.06)
    hist3.GetYaxis().SetTitleOffset(0.4)
    yMax3 = hist3.GetMaximum() * 1.75
    maxlist3.append(yMax3)
    if i == 2:
        yMax3n = np.max(np.asarray(maxlist3))
        hist3.SetMaximum(yMax3n)
    #hist.GetXaxis().SetLimits(1, xMax)
    # yMin3 = hist.GetMinimum() * 1.75
    hist3.SetMinimum(0.1)
    """if yMin3 == 0:
        hist3.SetMinimum(1)
    else:
        hist3.SetMinimum(yMin3)"""
    hists3.append(hist3)
    
    # hists.append(hist2)
    hists[i].GetXaxis().SetRangeUser(1.0,90.0)
    hists2[i].GetXaxis().SetRangeUser(1.0,90.0)
    hists3[i].GetXaxis().SetRangeUser(1.0,90.0)

    if i == 0:
        """pileupPad.cd()"""
        """hists[i].Draw()"""
        # hists[i].Draw("SAME HIST")
        # pileupPad.Update()
        
        """canvas.cd()
        predictionPad.cd()"""
        """hists2[i].Draw("SAME")"""
        # hists2[i].Draw("SAME HIST")
        # predictionPad.Update()

        """canvas.cd()"""
        mcratioPad.cd()
        hists3[i].Draw("E1")

        # hists3[i].Draw("SAME HIST")
        # predvpileupPad.Update()
        canvas.cd()

    else:
        """pileupPad.cd()"""
        """hists[i].Draw("SAME")"""
        # hists[i].Draw("SAME HIST")
        # pileupPad.Update()

        """canvas.cd()
        predictionPad.cd()"""
        """hists2[i].Draw("SAME")"""
        # hists2[i].Draw("SAME HIST")
        # predictionPad.Update()

        canvas.cd()
        dataratioPad.cd()
        if i == 1:
            hists3[i].Draw("E1")
        else:
            hists3[i].Draw("SAME E1")
        # hists3[i].Draw("SAME HIST")
        # predvpileupPad.Update()
        canvas.cd()
    
    """if i == 0:
        leg.AddEntry(hists[i], "MC Sample True" + runs[i], "l")
        leg.AddEntry(hists2[i], "MC Sample Predicted" + runs[i], "l")
    else: 
        leg.AddEntry(hists[i], "True Run " + runs[i], "l")
        leg.AddEntry(hists2[i], "Predicted Run " + runs[i], "l")"""

    """canvas.cd()
    predictionPad.cd()
    

    canvas.cd()
    predvpileupPad.cd()
    
    canvas.cd()"""


"""mcratioPad.cd()
ppleg = mcratioPad.BuildLegend(0.7, 0.75, 0.87, 0.87)
ppleg.Draw()"""

dataratioPad.cd()
predleg = dataratioPad.BuildLegend(0.7, 0.75, 0.87, 0.87)
predleg.Draw()

"""pileupPad.cd()
pileg = pileupPad.BuildLegend(0.7, 0.75, 0.87, 0.87)
pileg.Draw()
leg.Draw()"""
canvas.Draw()
canvas.SaveAs('INCItruevpileupratios.png')
