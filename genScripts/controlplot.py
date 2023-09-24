import ROOT
from tqdm import tqdm
import os
import prepChains as pc
import numpy as np
import math
import matplotlib.pyplot as plt
from array import array

ROOT.gStyle.SetOptStat(0)

run = input("Which Run?")
m_dir = "/hdfs/store/user/aloelige/ZeroBias/CICADA_2018Run"+run+"_ZB_07Jul2023"

# There's probably a better way to do this ngl - Run Differentiation
add = [f.path for f in os.scandir(m_dir) if f.is_dir()]
run_list = [a.path for a in os.scandir(add[0]) if a.is_dir()]

# Prepping Chains
for i in range(len(run_list)):
    chains = pc.prepChains(run_list[i])


hists = []

# Creating Canvas Pads
canvas = ROOT.TCanvas('C', 'Canvas', 500, 500)

ptPad = ROOT.TPad("Pad 1", "Pad 1", 0, 0.33, 0.5, 1.0)
ptPad.SetLogy()
histpt = ROOT.TH1F("Run"+run+" P_t", "P_t", 1000, 0.0, 300.0)
ptPad.Draw()

canvas.cd()
phiPad = ROOT.TPad("Pad 2", "Pad 2", 0.5, 0.33, 1.0, 1.0)
phiPad.SetLogy()
histphi = ROOT.TH1F("Run"+run+" Phi", "Phi", 1000, -4.0, 4.0)
phiPad.Draw()

canvas.cd()
etaPad = ROOT.TPad("Pad 3", "Pad 3", 0, 0, 1, 0.33)
etaPad.SetLogy()
histeta = ROOT.TH1F("Run"+run+" Eta", "Eta", 1000, -4.0, 4.0)
etaPad.Draw()
canvas.cd()


for i in tqdm(range(chains['caloJet'].GetEntries())):
    chains['caloJet'].GetEntry(i)
    
    for j in range(chains['caloJet'].ptVector.size()):
        ptPad.cd()
        histpt.Fill(chains['caloJet'].ptVector[j])

    for k in range(chains['caloJet'].phiVector.size()):
        canvas.cd()
        phiPad.cd()
        histphi.Fill(chains['caloJet'].phiVector[k])

    for m in range(chains['caloJet'].etaVector.size()):
        canvas.cd()
        etaPad.cd()
        histeta.Fill(chains['caloJet'].etaVector[m])

hists.append(histpt)
hists.append(histphi)
hists.append(histeta)

for i in range(3):
    if i == 0:
        print("First Histogram")
        ptPad.cd()
        
        hists[i].SetLineColor(46)
        hists[i].SetMarkerColor(46)
        hists[i].SetMarkerStyle(8)
        hists[i].SetMarkerSize(0.5)
        hists[i].SetTitle("")
        hists[i].GetXaxis().SetTitle("P_T")
        hists[i].GetXaxis().SetTitleSize(0.045)
        hists[i].GetXaxis().SetTitleOffset(0.9)
        hists[i].GetYaxis().SetTitleSize(0.045)
        hists[i].GetYaxis().SetTitleOffset(0.9)
        
        hists[i].Draw("HIST")
        canvas.cd()
    elif i == 1:
        print("Duplicate Histogram")
        phiPad.cd()

        hists[i].SetLineColor(46)
        hists[i].SetMarkerColor(46)
        hists[i].SetMarkerStyle(8)
        hists[i].SetMarkerSize(0.5)
        hists[i].SetTitle("")
        hists[i].GetXaxis().SetTitle("Phi")
        hists[i].GetXaxis().SetTitleSize(0.045)
        hists[i].GetXaxis().SetTitleOffset(0.9)
        hists[i].GetYaxis().SetTitleSize(0.045)
        hists[i].GetYaxis().SetTitleOffset(0.9)

        hists[i].Draw("SAME HIST")
        canvas.cd()
    elif i == 2:
        print("Duplicate Histogram")
        etaPad.cd()

        hists[i].SetLineColor(46)
        hists[i].SetMarkerColor(46)
        hists[i].SetMarkerStyle(8)
        hists[i].SetMarkerSize(0.5)
        hists[i].SetTitle("")
        hists[i].GetXaxis().SetTitle("Eta")
        hists[i].GetXaxis().SetTitleSize(0.045)
        hists[i].GetXaxis().SetTitleOffset(0.9)
        hists[i].GetYaxis().SetTitleSize(0.045)
        hists[i].GetYaxis().SetTitleOffset(0.9)

        hists[i].Draw("SAME HIST")
        canvas.cd()

canvas.Draw()
canvas.SaveAs('Run'+run+'controlplot.png')
    