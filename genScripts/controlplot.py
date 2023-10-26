import ROOT
from tqdm import tqdm
import os
import prepChainsFile as pc # change when working with calo/genJet instead of trig/PUPPI
import numpy as np
import math
import matplotlib.pyplot as plt
from array import array

ROOT.gStyle.SetOptStat(0)

# run = input("Which Run?")
# Multiple Files
run_list = []
m_dir = ["/hdfs/store/user/aloelige/EphemeralZeroBias0/SNAIL_2023RunD_EZB0_18Oct2023/231018_205626/",
"/hdfs/store/user/aloelige/EphemeralZeroBias2/SNAIL_2023RunD_EZB2_19Oct2023/231019_080917/", 
"/hdfs/store/user/aloelige/EphemeralZeroBias3/SNAIL_2023RunD_EZB3_18Oct2023/231018_205910/", 
"/hdfs/store/user/aloelige/EphemeralZeroBias4/SNAIL_2023RunD_EZB4_18Oct2023/231018_205953/", 
"/hdfs/store/user/aloelige/EphemeralZeroBias5/SNAIL_2023RunD_EZB5_18Oct2023/231018_210031/",
"/hdfs/store/user/aloelige/EphemeralZeroBias6/SNAIL_2023RunD_EZB6_18Oct2023/231018_210109/",
"/hdfs/store/user/aloelige/EphemeralZeroBias7/SNAIL_2023RunD_EZB7_19Oct2023/231019_080954/"]
# Single File
""" /hdfs/store/user/aloelige/ZeroBias/CICADA_2018Run"+run+"_ZB_07Jul2023 """

# Multi File - Run Differentiation
for i in tqdm(range(7)):
    # Run Differentiation
    add = [f.path for f in os.scandir(m_dir[i]) if f.is_dir()]
    # run_list = [a.path for a in os.scandir(add[0]) if a.is_dir()]
    for j in tqdm(range(len(add))): # tqdm(range(len(run_list)))
        for k in tqdm(range(len(os.listdir(add[j])))):
            dir_list = os.listdir(add[j])
            run_list.append(str(add[j]) +"/" + str(dir_list[k]))
            
# Single File - Run Differentiation
"""add = [f.path for f in os.scandir(m_dir) if f.is_dir()]
run_list = [a.path for a in os.scandir(add[0]) if a.is_dir()]"""

# Prepping Chains
for i in range(len(run_list)):
    chains = pc.prepChains(run_list[i])


hists = []

# Creating Canvas Pads
canvas = ROOT.TCanvas('C', 'Canvas', 500, 500)

ptPad = ROOT.TPad("Pad 1", "Pad 1", 0, 0.33, 0.5, 1.0)
ptPad.SetLogy()
histpt = ROOT.TH1F("PUPPIJet P_t", "P_t", 100, 0.0, 170.0)
ptPad.Draw()

canvas.cd()
phiPad = ROOT.TPad("Pad 2", "Pad 2", 0.5, 0.33, 1.0, 1.0)
phiPad.SetLogy()
histphi = ROOT.TH1F("PUPPIJet Phi", "Phi", 100, -4.0, 4.0)
phiPad.Draw()

canvas.cd()
etaPad = ROOT.TPad("Pad 3", "Pad 3", 0, 0, 1, 0.33)
etaPad.SetLogy()
histeta = ROOT.TH1F("PUPPIJet Eta", "Eta", 100, -5.0, 5.0)
etaPad.Draw()
canvas.cd()


for i in tqdm(range(chains['puppiJet'].GetEntries())): # used to be 'caloJet'
    # chains['caloJet'].GetEntry(i)
    chains['puppiJet'].GetEntry(i)
    for j in range(chains['puppiJet'].ptVector.size()):
        ptPad.cd()
        # jetEt = chains['trigJet'].jetRawEt[j] * 0.5
        histpt.Fill(chains['puppiJet'].ptVector[j])

    for k in range(chains['puppiJet'].phiVector.size()):
        canvas.cd()
        phiPad.cd()
        histphi.Fill(chains['puppiJet'].phiVector[k])

    for m in range(chains['puppiJet'].etaVector.size()):
        canvas.cd()
        etaPad.cd()
        histeta.Fill(chains['puppiJet'].etaVector[m])

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
canvas.SaveAs('../genTrainML/controlPlots/PUPPIJet_ControlPlot.png')
    