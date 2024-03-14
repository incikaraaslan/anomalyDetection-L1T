import ROOT
from tqdm import tqdm
import os
import prepChains as pc
import iEtaiPhiBinning
import numpy as np
import pandas as pd
import math
import random
import matplotlib.pyplot as plt
import h5py

tt = ["trainshuf", "testshuf"]

canvas = ROOT.TCanvas('canvas', '', 500, 500)
counters = [0, 0, 0, 0, 0, 0]
gev1npv = ROOT.TH2F("jete1npv", "Jet E_T Above 1 GeV v. npv", 100, 0.0, 80, 100, 0.0, 150)
gev2npv = ROOT.TH2F("jete2npv", "Jet E_T Above 2 GeV v. npv", 100, 0.0, 80, 100, 0.0, 150)
gev3npv = ROOT.TH2F("jete3npv", "Jet E_T Above 3 GeV v. npv", 100, 0.0, 80, 100, 0.0, 150)
gev5npv = ROOT.TH2F("jete5npv", "Jet E_T Above 5 GeV v. npv", 100, 0.0, 80, 100, 0.0, 150)
gev10npv = ROOT.TH2F("jete10npv", "Jet E_T Above 10 GeV v. npv", 100, 0.0, 80, 100, 0.0, 150)
gev30npv = ROOT.TH2F("jete30npv", "Jet E_T Above 30 GeV v. npv", 100, 0.0, 80, 100, 0.0, 150)

for c in tqdm(range(len(tt))):
    print(tt[c])
    # Lists

    # Import Files from Data
    # Get all of the file
    """f = open('output/'+tt[c]+'.txt', 'r')"""

    # Get the first n files from training and test
    with open('output/'+tt[c]+'.txt', 'r') as f:
        head = [next(f) for k in range(50)]
    for x in tqdm(head):
        x = x[:-1]
        chains = pc.prepChains(x)
        
        for i in tqdm(range(chains['trigJet'].GetEntries())):

            chains['trigJet'].GetEntry(i)
            chains['regionEt'].GetEntry(i)
            chains['PUChainPUPPI'].GetEntry(i)
            chains['caloTower'].GetEntry(i)

            # Singular Calculation
            npv = chains['PUChainPUPPI'].npv
            print("nTower: " + str(chains['caloTower'].L1CaloTower.nTower/4))

            for j in range(chains['trigJet'].jetEta.size()):

                # Create the trigJet vectors
                trigJet = ROOT.TVector3()

                # uncalibrated no-PU-subtracted jet Et= (jetRawEt) x 0.5
                # calibrated no-PU-subtracted jet Et = jetRawEt x SF x 0.5
                jetEt = chains['trigJet'].jetRawEt[j] * 0.5
                if jetEt >= 1:
                    gev1npv.Fill(npv, jetEt)
                
                if jetEt >= 2:
                    gev2npv.Fill(npv, jetEt)
                
                if jetEt >= 3:
                    gev3npv.Fill(npv, jetEt)
                
                if jetEt >= 5:
                    gev5npv.Fill(npv, jetEt)
                
                if jetEt >= 10:
                    gev10npv.Fill(npv, jetEt)

                if jetEt >= 30:
                    gev30npv.Fill(npv, jetEt)
    


    gev1npv.Fit("pol1")
    gev1npv.GetFunction("pol1").SetLineColor(1)
    gev1npv.SetLineColor(46)
    gev1npv.SetMarkerColor(46)
    gev1npv.SetMarkerStyle(8)
    gev1npv.SetMarkerSize(0.5)
    gev1npv.SetTitle("Jet E_T Above 1 GeV v. npv")
    gev1npv.GetXaxis().SetTitle("npv")
    gev1npv.GetYaxis().SetTitle("Jet E_T Above 1 GeV")
    gev1npv.GetXaxis().SetTitleSize(0.045)
    gev1npv.GetXaxis().SetTitleOffset(0.9)
    gev1npv.GetYaxis().SetTitleSize(0.045)
    gev1npv.GetYaxis().SetTitleOffset(0.9)
    gev1npv.Draw("COLZ")
    canvas.Draw()
    canvas.SaveAs('controlPlots/gev1npv'+str(tt[c])+'.png')
    print("Hist 1 Done.")

    gev2npv.Fit("pol1")
    gev2npv.GetFunction("pol1").SetLineColor(1)
    gev2npv.SetLineColor(46)
    gev2npv.SetMarkerColor(46)
    gev2npv.SetMarkerStyle(8)
    gev2npv.SetMarkerSize(0.5)
    gev2npv.SetTitle("Jet E_T Above 2 GeV v. npv")
    gev2npv.GetXaxis().SetTitle("npv")
    gev2npv.GetYaxis().SetTitle("Jet E_T Above 2 GeV")
    gev2npv.GetXaxis().SetTitleSize(0.045)
    gev2npv.GetXaxis().SetTitleOffset(0.9)
    gev2npv.GetYaxis().SetTitleSize(0.045)
    gev2npv.GetYaxis().SetTitleOffset(0.9)
    gev2npv.Draw("COLZ")
    canvas.Draw()
    canvas.SaveAs('controlPlots/gev2npv'+str(tt[c])+'.png')
    print("Hist 2 Done.")

    gev3npv.Fit("pol1")
    gev3npv.GetFunction("pol1").SetLineColor(1)
    gev3npv.SetLineColor(46)
    gev3npv.SetMarkerColor(46)
    gev3npv.SetMarkerStyle(8)
    gev3npv.SetMarkerSize(0.5)
    gev3npv.SetTitle("Jet E_T Above 3 GeV v. npv")
    gev3npv.GetXaxis().SetTitle("npv")
    gev3npv.GetYaxis().SetTitle("Jet E_T Above 3 GeV")
    gev3npv.GetXaxis().SetTitleSize(0.045)
    gev3npv.GetXaxis().SetTitleOffset(0.9)
    gev3npv.GetYaxis().SetTitleSize(0.045)
    gev3npv.GetYaxis().SetTitleOffset(0.9)
    gev3npv.Draw("COLZ")
    canvas.Draw()
    canvas.SaveAs('controlPlots/gev3npv'+str(tt[c])+'.png')
    print("Hist 3 Done.")

    gev5npv.Fit("pol1")
    gev5npv.GetFunction("pol1").SetLineColor(1)
    gev5npv.SetLineColor(46)
    gev5npv.SetMarkerColor(46)
    gev5npv.SetMarkerStyle(8)
    gev5npv.SetMarkerSize(0.5)
    gev5npv.SetTitle("Jet E_T Above 5 GeV v. npv")
    gev5npv.GetXaxis().SetTitle("npv")
    gev5npv.GetYaxis().SetTitle("Jet E_T Above 5 GeV")
    gev5npv.GetXaxis().SetTitleSize(0.045)
    gev5npv.GetXaxis().SetTitleOffset(0.9)
    gev5npv.GetYaxis().SetTitleSize(0.045)
    gev5npv.GetYaxis().SetTitleOffset(0.9)
    gev5npv.Draw("COLZ")
    canvas.Draw()
    canvas.SaveAs('controlPlots/gev5npv'+str(tt[c])+'.png')
    print("Hist 5 Done.")

    gev10npv.Fit("pol1")
    gev10npv.GetFunction("pol1").SetLineColor(1)
    gev10npv.SetLineColor(46)
    gev10npv.SetMarkerColor(46)
    gev10npv.SetMarkerStyle(8)
    gev10npv.SetMarkerSize(0.5)
    gev10npv.SetTitle("Jet E_T Above 10 GeV v. npv")
    gev10npv.GetXaxis().SetTitle("npv")
    gev10npv.GetYaxis().SetTitle("Jet E_T Above 10 GeV")
    gev10npv.GetXaxis().SetTitleSize(0.045)
    gev10npv.GetXaxis().SetTitleOffset(0.9)
    gev10npv.GetYaxis().SetTitleSize(0.045)
    gev10npv.GetYaxis().SetTitleOffset(0.9)
    gev10npv.Draw("COLZ")
    canvas.Draw()
    canvas.SaveAs('controlPlots/gev10npv'+str(tt[c])+'.png')
    print("Hist 10 Done.")

    gev30npv.Fit("pol1")
    gev30npv.GetFunction("pol1").SetLineColor(1)
    gev30npv.SetLineColor(46)
    gev30npv.SetMarkerColor(46)
    gev30npv.SetMarkerStyle(8)
    gev30npv.SetMarkerSize(0.5)
    gev30npv.SetTitle("Jet E_T Above 30 GeV v. npv")
    gev30npv.GetXaxis().SetTitle("npv")
    gev30npv.GetYaxis().SetTitle("Jet E_T Above 30 GeV")
    gev30npv.GetXaxis().SetTitleSize(0.045)
    gev30npv.GetXaxis().SetTitleOffset(0.9)
    gev30npv.GetYaxis().SetTitleSize(0.045)
    gev30npv.GetYaxis().SetTitleOffset(0.9)
    gev30npv.Draw("COLZ")
    canvas.Draw()
    canvas.SaveAs('controlPlots/gev30npv'+str(tt[c])+'.png')
    print("Hist 30 Done.")
                
                    

