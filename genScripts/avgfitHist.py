
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
a = 'avgforEachP_run'
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
    
avgforEachP = f.Get("avgforEachP_run"+run)
avgforEachP.Draw("SAME")

canvas.Draw()
canvas.SaveAs('INCI'+a+'.png')


