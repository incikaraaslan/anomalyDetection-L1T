import ROOT
from tqdm import tqdm
import os
import prepChains as pc
import numpy as np
import math
import matplotlib.pyplot as plt
from array import array

# ROOT.gStyle.SetOptStat(0)

# Multiple Files
run_list = []
m_dir = ["/hdfs/store/user/aloelige/EphemeralZeroBias0/SNAIL_2023RunD_EZB0_18Oct2023/231018_205626/",
"/hdfs/store/user/aloelige/EphemeralZeroBias2/SNAIL_2023RunD_EZB2_19Oct2023/231019_080917/", 
"/hdfs/store/user/aloelige/EphemeralZeroBias3/SNAIL_2023RunD_EZB3_18Oct2023/231018_205910/", 
"/hdfs/store/user/aloelige/EphemeralZeroBias4/SNAIL_2023RunD_EZB4_18Oct2023/231018_205953/", 
"/hdfs/store/user/aloelige/EphemeralZeroBias5/SNAIL_2023RunD_EZB5_18Oct2023/231018_210031/",
"/hdfs/store/user/aloelige/EphemeralZeroBias6/SNAIL_2023RunD_EZB6_18Oct2023/231018_210109/",
"/hdfs/store/user/aloelige/EphemeralZeroBias7/SNAIL_2023RunD_EZB7_19Oct2023/231019_080954/"]


# Multi File - Run Differentiation
for i in tqdm(range(7)):
    # Run Differentiation
    add = [f.path for f in os.scandir(m_dir[i]) if f.is_dir()]
    # run_list = [a.path for a in os.scandir(add[0]) if a.is_dir()]
    for j in tqdm(range(len(add))): # tqdm(range(len(run_list)))
        for k in tqdm(range(len(os.listdir(add[j])))):
            dir_list = os.listdir(add[j])
            run_list.append(str(add[j]) +"/" + str(dir_list[k]))
            
# Prepping Chains
for i in range(len(run_list)):
    chains = pc.prepChains(run_list[i])


# Canvas and Formatting
canvas = ROOT.TCanvas('C', 'Canvas', 500, 500)
hcalnpv = ROOT.TH2F("nHCALtpvnpv", "nHCALtp v. npv", 100, 0.0, 80, 100, 0.0, 1200)
totaletnpv = ROOT.TH2F("totalEtvnpv", "totalEt v. npv", 100, 0.0, 80, 100, 0.0, 30e6)
# phiringetnpv = ROOT.TH1F("PUPPI P_T", "P_T (GeV)", 100, 0.0, 170.0)
npv = []
for i in tqdm(range(chains['PUChainPUPPI'].GetEntries())):
    hcaltpet = 0.0
    chains['PUChainPUPPI'].GetEntry(i)
    chains['caloTower'].GetEntry(i)

    hcalnpv.Fill(chains['PUChainPUPPI'].npv, chains['caloTower'].CaloTP.nHCALTP)
    for j in range(chains['caloTower'].CaloTP.hcalTPet.size()):
        hcaltpet += chains['caloTower'].CaloTP.hcalTPet[j]
    
    totaletnpv.Fill(chains['PUChainPUPPI'].npv, hcaltpet)
    
    """for j in range(chains['caloTower'].nHCALTP.size()):
        npv.append(chains['PUChainPUPPI'].npv[j])
        nHCALTP.append(chains['caloTower'].nHCALTP[j])"""

hcalnpv.SetLineColor(46)
hcalnpv.SetMarkerColor(46)
hcalnpv.SetMarkerStyle(8)
hcalnpv.SetMarkerSize(0.5)
hcalnpv.SetTitle("nHCALtp v. npv")
hcalnpv.GetXaxis().SetTitle("npv")
hcalnpv.GetYaxis().SetTitle("nHCALTP")
hcalnpv.GetXaxis().SetTitleSize(0.045)
hcalnpv.GetXaxis().SetTitleOffset(0.9)
hcalnpv.GetYaxis().SetTitleSize(0.045)
hcalnpv.GetYaxis().SetTitleOffset(0.9)
hcalnpv.Draw("HIST")
canvas.Draw()
canvas.SaveAs('controlPlots/nHCALtpvnpv.png')
print("Hist 1 Done.")

canvas.Clear()

totaletnpv.SetLineColor(46)
totaletnpv.SetMarkerColor(46)
totaletnpv.SetMarkerStyle(8)
totaletnpv.SetMarkerSize(0.5)
totaletnpv.SetTitle("jetEt v. npv")
totaletnpv.GetXaxis().SetTitle("npv")
totaletnpv.GetYaxis().SetTitle("jetEt")
totaletnpv.GetXaxis().SetTitleSize(0.045)
totaletnpv.GetXaxis().SetTitleOffset(0.9)
totaletnpv.GetYaxis().SetTitleSize(0.045)
totaletnpv.GetYaxis().SetTitleOffset(0.9)
totaletnpv.Draw("HIST")
canvas.Draw()
canvas.SaveAs('controlPlots/jetEtvnpv.png')
print("Hist 2 Done.")

    


