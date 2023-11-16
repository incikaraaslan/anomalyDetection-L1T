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

print(len(run_list))

# Prepping Chains
for i in range(len(run_list)):
    chains = pc.prepChains(run_list[i])


hists = []

# Creating Canvas Pads
canvas = ROOT.TCanvas('C', 'Canvas', 500, 500)

ptPad = ROOT.TPad("Pad 1", "Pad 1", 0, 0.33, 0.5, 1.0)
ptPad.SetLogy()
histpt = ROOT.TH1F("PUPPI P_t", "P_T (GeV)", 100, 0.0, 170.0)
ptPad.Draw()

canvas.cd()
phiPad = ROOT.TPad("Pad 2", "Pad 2", 0.5, 0.33, 1.0, 1.0)
phiPad.SetLogy()
histphi = ROOT.TH1F("PUPPI Phi", "Phi", 100, -4.0, 4.0)
phiPad.Draw()

canvas.cd()
etaPad = ROOT.TPad("Pad 3", "Pad 3", 0, 0, 1, 0.33)
etaPad.SetLogy()
histeta = ROOT.TH1F("PUPPI Eta", "Eta", 100, -5.0, 5.0)
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
        hists[i].GetYaxis().SetTitle("Events")
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
        hists[i].GetYaxis().SetTitle("Events")
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
        hists[i].GetYaxis().SetTitle("Events")
        """hists[i].GetXaxis().SetTitleSize(0.045)
        hists[i].GetXaxis().SetTitleOffset(0.9)
        hists[i].GetYaxis().SetTitleSize(0.045)
        hists[i].GetYaxis().SetTitleOffset(0.9)"""

        hists[i].Draw("SAME HIST")
        canvas.cd()

canvas.Draw()
canvas.SaveAs('../genTrainML/controlPlots/PUPPIJet_ControlPlotnew.png')
print("PUPPI Done")

hists2 = []

# Creating Canvas Pads
canvas2 = ROOT.TCanvas('C', 'Canvas', 500, 500)

ptPad2 = ROOT.TPad("TPad 1", "Pad 1", 0, 0.33, 0.5, 1.0)
ptPad2.SetLogy()
histpt2 = ROOT.TH1F("TRIG P_t", "P_t", 100, 0.0, 170.0)
ptPad2.Draw()

canvas2.cd()
phiPad2 = ROOT.TPad("TPad 2", "Pad 2", 0.5, 0.33, 1.0, 1.0)
phiPad2.SetLogy()
histphi2 = ROOT.TH1F("TRIG Phi", "Phi", 100, -4.0, 4.0)
phiPad2.Draw()

canvas2.cd()
etaPad2 = ROOT.TPad("TPad 3", "Pad 3", 0, 0, 1, 0.33)
etaPad2.SetLogy()
histeta2 = ROOT.TH1F("TRIG Eta", "Eta", 100, -5.0, 5.0)
etaPad2.Draw()
canvas2.cd()


for i in tqdm(range(chains['trigJet'].GetEntries())): # used to be 'caloJet'
    # chains['caloJet'].GetEntry(i)
    chains['trigJet'].GetEntry(i)
    for j in range(chains['trigJet'].jetEt.size()):
        ptPad2.cd()
        # jetEt = chains['trigJet'].jetRawEt[j] * 0.5
        histpt2.Fill(chains['trigJet'].jetEt[j])

    for k in range(chains['trigJet'].jetPhi.size()):
        canvas2.cd()
        phiPad2.cd()
        histphi2.Fill(chains['trigJet'].jetPhi[k])

    for m in range(chains['trigJet'].jetEta.size()):
        canvas2.cd()
        etaPad2.cd()
        histeta2.Fill(chains['trigJet'].jetEta[m])

hists2.append(histpt2)
hists2.append(histphi2)
hists2.append(histeta2)

for i in range(3):
    if i == 0:
        print("First Histogram")
        ptPad2.cd()
        
        hists2[i].SetLineColor(46)
        hists2[i].SetMarkerColor(46)
        hists2[i].SetMarkerStyle(8)
        hists2[i].SetMarkerSize(0.5)
        hists2[i].SetTitle("")
        hists2[i].GetXaxis().SetTitle("P_T")
        hists2[i].GetYaxis().SetTitle("Events")
        hists2[i].GetXaxis().SetTitleSize(0.045)
        hists2[i].GetXaxis().SetTitleOffset(0.9)
        hists2[i].GetYaxis().SetTitleSize(0.045)
        hists2[i].GetYaxis().SetTitleOffset(0.9)
        
        hists2[i].Draw("HIST")
        canvas2.cd()
    elif i == 1:
        print("Duplicate Histogram")
        phiPad2.cd()

        hists2[i].SetLineColor(46)
        hists2[i].SetMarkerColor(46)
        hists2[i].SetMarkerStyle(8)
        hists2[i].SetMarkerSize(0.5)
        hists2[i].SetTitle("")
        hists2[i].GetYaxis().SetTitle("Events")
        hists2[i].GetXaxis().SetTitle("Phi")
        hists2[i].GetXaxis().SetTitleSize(0.045)
        hists2[i].GetXaxis().SetTitleOffset(0.9)
        hists2[i].GetYaxis().SetTitleSize(0.045)
        hists2[i].GetYaxis().SetTitleOffset(0.9)

        hists2[i].Draw("SAME HIST")
        canvas2.cd()
    elif i == 2:
        print("Duplicate Histogram")
        etaPad2.cd()

        hists2[i].SetLineColor(46)
        hists2[i].SetMarkerColor(46)
        hists2[i].SetMarkerStyle(8)
        hists2[i].SetMarkerSize(0.5)
        hists2[i].SetTitle("")
        hists2[i].GetXaxis().SetTitle("Eta")
        hists2[i].GetYaxis().SetTitle("Events")
        """hists[i].GetXaxis().SetTitleSize(0.045)
        hists[i].GetXaxis().SetTitleOffset(0.9)
        hists[i].GetYaxis().SetTitleSize(0.045)
        hists[i].GetYaxis().SetTitleOffset(0.9)"""

        hists2[i].Draw("SAME HIST")
        canvas2.cd()

canvas2.Draw()
canvas2.SaveAs('../genTrainML/controlPlots/TRIGJet_ControlPlotnew.png')
print("Trig Done.")