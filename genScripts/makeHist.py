import ROOT
import os


run = input("Log in the Run A, C, D:")
directory = '/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genScripts/'

f = ROOT.TFile.Open("resocaloResPlot"+run+".root", 'READ')
canvas = ROOT.TCanvas('canvas1', '', 500, 500)
hist = f.Get("resocaloResPlot"+run)

# Formatting
ROOT.gStyle.SetOptStat(2210)
ROOT.gStyle.SetStatW(0.3)
ROOT.gStyle.SetStatH(0.105)
hist.SetTitle("")
hist.GetXaxis().SetTitle("Resolution")
hist.GetYaxis().SetTitle("Number of Entries")

leg = ROOT.TLegend(0.72, 0.68, 0.89, 0.80)
leg.SetBorderSize(1)
leg.SetFillColor(10)
leg.SetFillStyle(2)
leg.SetTextFont(40)

# Additional Elts/Fits (if needed)
yMax = hist.GetMaximum()
l = ROOT.TLine(0.0, 0.0, 0.0, yMax)


hist.Fit("gaus")
fit = hist.GetFunction("gaus")
hist.Draw()
l.Draw("SAME")
hist.SetStats(1)

leg.AddEntry(hist, "Histogram")
leg.AddEntry(fit, "Gaussian Fit", "l")
# leg.AddEntry(l, "Zero Line")
ROOT.gPad.Update()

leg.Draw()
canvas.Draw()
canvas.SaveAs("resocaloResPlot"+run+".png")
print("Image Saved.")

"""
FCN=188.957 FROM MIGRAD    STATUS=CONVERGED      79 CALLS          80 TOTAL
                     EDM=2.48735e-07    STRATEGY= 1      ERROR MATRIX ACCURATE 
  EXT PARAMETER                                   STEP         FIRST   
  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE 
   1  Constant     3.96274e+02   9.00501e+00   4.39409e-02   3.46364e-05
   2  Mean         1.01352e-02   5.12168e-03   3.29505e-05   7.00965e-02
   3  Sigma        2.96766e-01   4.65422e-03   2.16342e-05  -1.02170e-01
"""


