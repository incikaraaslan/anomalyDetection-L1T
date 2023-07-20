import ROOT
import os

directory = '/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genScripts/'

f = ROOT.TFile.Open('gencaloResPlot.root', 'READ')
canvas = ROOT.TCanvas('canvas1', '', 500, 500)
hist = f.Get('gencaloResPlot')

# Formattting (if needed)
hist.Fit("gaus")
yMax = hist.GetMaximum()
l = ROOT.TLine(0.0, 0.0, 0.0, yMax)

hist.Draw()
canvas.Draw()
canvas.SaveAs("gencaloResPlot.png")
print("Image Saved.")