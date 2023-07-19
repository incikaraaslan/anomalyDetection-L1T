
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
a = 'INCImaxforEachP_run'
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
    
avgforEachP = f.Get("INCImaxforEachP_run"+run)
# TF1 *f = new TF1("f", "[2] * x * x + [1] * x + [0]"); g->Fit(f); g->Draw("AL");
f = ROOT.TF1("f", "[1] * (x ** (0.5)) + [0]")
avgforEachP.Fit(f)
# avgforEachP.Fit("pol1")
avgforEachP.Draw("SAME")

canvas.Draw()
canvas.SaveAs('INCIfittedpol12'+a+run+'.png')
"""
OLD DATA

Pol2
Minimizer is Linear / Migrad
Chi2                      =      76.7183
NDf                       =            7
p0                        =      4.71794   +/-   2.8525      
p1                        =      13.3575   +/-   2.37296     
p2                        =     0.467661   +/-   0.402548    
Info in <TCanvas::Print>: png file fittedpol2maxforEachP_runA.png has been created
Chi2                      =      238.864
NDf                       =            7
p0                        =      2.84265   +/-   5.626       
p1                        =      13.0512   +/-   4.69652     
p2                        =     0.630961   +/-   0.801948    
Info in <TCanvas::Print>: png file fittedmaxforEachP_runC.png
Minimizer is Linear / Migrad
Chi2                      =      5348.04
NDf                       =            7
p0                        =      61.5814   +/-   16.5134     
p1                        =     -28.9918   +/-   17.6272     
p2                        =      6.42238   +/-   3.43799     
Info in <TCanvas::Print>: png file fittedpol2maxforEachP_runD.png has been created

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
Chi2                      =      33.3333
NDf                       =            6
p0                        =          2.5   +/-   1.60295     
p1                        =      13.8889   +/-   0.507151    
Info in <TCanvas::Print>: png file fittedpol1maxforEachP_runD.png has been created

Pol1/2
Chi2                      =      472.621
NDf                       =            8
Edm                       =  1.33337e-21
NCalls                    =           35
p0                        =     -22.8233   +/-   6.79643     
p1                        =      45.2489   +/-   3.94369 
Info in <TCanvas::Print>: png file fittedpol12maxforEachP_runA.png has been created
Chi2                      =      731.975
NDf                       =            8
Edm                       =  6.88087e-20
NCalls                    =           31
p0                        =     -26.5615   +/-   8.97152     
p1                        =       46.719   +/-   5.154       
Info in <TCanvas::Print>: png file fittedpol12maxforEachP_runC.png has been created
Chi2                      =      129.856
NDf                       =            6
Edm                       =  1.35589e-20
NCalls                    =           31
p0                        =     -21.4007   +/-   4.76994     
p1                        =      39.8089   +/-   2.90289     
Info in <TCanvas::Print>: png file fittedpol12maxforEachP_runD.png has been created  


NEW DATA
Pol1
Chi2                      =      198.871
NDf                       =            8
p0                        =     -2.63848   +/-   3.32282     
p1                        =      18.2772   +/-   1.0156      
Info in <TCanvas::Print>: png file INCIfittedpol1INCImaxforEachP_runA.png has been created
Chi2                      =      197.969
NDf                       =            8
p0                        =     0.138727   +/-   3.18045     
p1                        =      16.1363   +/-   0.894553    
Info in <TCanvas::Print>: png file INCIfittedpol1INCImaxforEachP_runC.png has been created
Chi2                      =      120.313
NDf                       =            6
p0                        =     -2.28944   +/-   3.36106     
p1                        =      15.3084   +/-   1.07324     
Info in <TCanvas::Print>: png file INCIfittedpol1INCImaxforEachP_runD.png has been created

Pol1/2
Chi2                      =      799.801
NDf                       =            8
Edm                       =  4.61904e-20
NCalls                    =           31
p0                        =     -29.1589   +/-   9.69967     
p1                        =      49.3399   +/-   5.71558     
Info in <TCanvas::Print>: png file INCIfittedpol12INCImaxforEachP_runA.png has been created
Chi2                      =      653.013
NDf                       =            8
Edm                       =  3.07325e-20
NCalls                    =           31
p0                        =      -25.991   +/-   8.37907     
p1                        =      45.9855   +/-   4.76669     
Info in <TCanvas::Print>: png file INCIfittedpol12INCImaxforEachP_runC.png has been created
Chi2                      =      384.283
NDf                       =            6
Edm                       =  6.81157e-20
NCalls                    =           31
p0                        =     -24.7665   +/-   8.85519     
p1                        =       41.123   +/-   5.32778     
Info in <TCanvas::Print>: png file INCIfittedpol12INCImaxforEachP_runD.png has been created
"""




