
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


o = "/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genScripts/"
# newhistFiles/
a = 'maxforEachP_run'
b = 'AnomalyNPileup'

# Running the histograms
run = input("Which Run?") # 'B' whenever I have that for pileup lol
canvas = ROOT.TCanvas('canvas', '', 500, 500)
 
flist = o+a+run+'.root'
openfiles = []
hists = []

f = ROOT.TFile.Open(flist, 'READ')
openfiles.append(f)
    
hist = f.Get(b+run)
hist.SetTitle("")
hist.GetXaxis().SetTitle("Anomaly Score")
hist.GetYaxis().SetTitle("True Pileup")
hist.SetMarkerStyle(8)
hist.SetMarkerSize(0.4)
hist.GetXaxis().SetTitleSize(0.035)
hist.GetXaxis().SetTitleOffset(1.2)
hist.GetYaxis().SetTitleSize(0.035)
hist.GetYaxis().SetTitleOffset(1.2)
hist.Draw("COLZ")
    
avgforEachP = f.Get("maxforEachP_run"+run)
avgforEachP.Fit("pol2")
avgforEachP.Draw("SAME")
"""
Pol2
Chi2                      =      238.864
NDf                       =            7
p0                        =      2.84265   +/-   5.626       
p1                        =      13.0512   +/-   4.69652     
p2                        =     0.630961   +/-   0.801948    
Info in <TCanvas::Print>: png file fittedmaxforEachP_runC.png
Pol1
Minimizer is Linear / Migrad
Chi2                      =      91.5103
NDf                       =            8
p0                        =      2.39545   +/-   2.07876     
p1                        =      16.0285   +/-   0.600174    
Info in <TCanvas::Print>: png file fittedpol1maxforEachP_runA.png has been created
Chi2                      =      259.988
NDf                       =            8
p0                        =    -0.436954   +/-   3.68738     
p1                        =      16.6459   +/-   1.06161     
Info in <TCanvas::Print>: png file fittedmaxforEachP_runC.png has been created
Minimizer is Linear / Migrad
Chi2                      =      8014.16
NDf                       =            8
p0                        =      44.1844   +/-   15.6153     
p1                        =      2.67999   +/-   5.52343     
Info in <TCanvas::Print>: png file fittedpol1maxforEachP_runD.png has been created
"""

canvas.Draw()
canvas.SaveAs('fittedpol2'+a+run+'.png')


