import ROOT
from tqdm import tqdm
import os
import prepChains as pc
import numpy as np
import pandas as pd
import math
import random
from time import perf_counter

# Import Files from Data
f = open('output/train.txt', 'r')
for x in f:
    chains = pc.prepChains(x)

"""
# Create the Histogram
h = ROOT.TH1F("calopuppiResPlot", "Resolution Plot", 100, -4.0, 4.0)
"""
# Create Pileup Histograms
canvas = ROOT.TCanvas()
hp = ROOT.TH1F("calopuppiResPlot", "Resolution Plot", 100, -1.0, 1.0)
hpp = ROOT.TH1F("pcalopuppiResPlot", "Resolution Plot", 100, -1.0, 1.0)
hp010 = ROOT.TH1F("calopuppiResPlot 0-10", "Resolution Plot 0-10", 100, -1.0, 1.0)
hp1020 = ROOT.TH1F("calopuppiResPlot 10-20", "Resolution Plot 10-20", 100, -1.0, 1.0)
hp2030 = ROOT.TH1F("calopuppiResPlot 20-30", "Resolution Plot 20-30", 100, -1.0, 1.0)
hp3040 = ROOT.TH1F("calopuppiResPlot 30-40", "Resolution Plot 30-40", 100, -1.0, 1.0)
hp4050 = ROOT.TH1F("calopuppiResPlot 40-50", "Resolution Plot 40-50", 100, -1.0, 1.0)
hp5060 = ROOT.TH1F("calopuppiResPlot 50-60", "Resolution Plot 50-60", 100, -1.0, 1.0)
hp6070 = ROOT.TH1F("calopuppiResPlot 60-70", "Resolution Plot 60-70", 100, -1.0, 1.0)
hp7080 = ROOT.TH1F("calopuppiResPlot 70-80", "Resolution Plot 70-80", 100, -1.0, 1.0)
hpp010 = ROOT.TH1F("pcalopuppiResPlot 0-10", "Resolution Plot 0-10", 100, -1.0, 1.0)
hpp1020 = ROOT.TH1F("pcalopuppiResPlot 10-20", "Resolution Plot 10-20", 100, -1.0, 1.0)
hpp2030 = ROOT.TH1F("pcalopuppiResPlot 20-30", "Resolution Plot 20-30", 100, -1.0, 1.0)
hpp3040 = ROOT.TH1F("pcalopuppiResPlot 30-40", "Resolution Plot 30-40", 100, -1.0, 1.0)
hpp4050 = ROOT.TH1F("pcalopuppiResPlot 40-50", "Resolution Plot 40-50", 100, -1.0, 1.0)
hpp5060 = ROOT.TH1F("pcalopuppiResPlot 50-60", "Resolution Plot 50-60", 100, -1.0, 1.0)
hpp6070 = ROOT.TH1F("pcalopuppiResPlot 60-70", "Resolution Plot 60-70", 100, -1.0, 1.0)
hpp7080 = ROOT.TH1F("pcalopuppiResPlot 70-80", "Resolution Plot 70-80", 100, -1.0, 1.0)

# Lists
cg_matched = []
cg_unmatched = []
phiRingInfo = []
# uphiRingInfo = []

# For Drawing Pileup Histograms
truePileuparr = []
predPileuparr = []

# Next: what iPhi ring in the regions the trigger jet we have just used belongs to
# Then: get the regions that correspond to this ring from my quick ntuplizer for the regions L1RegionNtuplizer 
# (stored in iEta then iPhi indices ([14][18]), you may have to reconstruct it from flat). 
# For now, simply take every phi energy deposit across the ring (all 18). 

# Match Jet with PUPPI
for i in tqdm(range(chains['trigJet'].GetEntries())): # chains['genJet'].GetEntries() - 100000 events if you can
    trigJetptarr = []
    puppiJetptarr = []
    phiRing = []
    chains['puppiJet'].GetEntry(i)
    chains['trigJet'].GetEntry(i)
    chains['regionEt'].GetEntry(i)

    # For Drawing Pileup Histograms
    chains['pileupInfo'].GetEntry(i)
    chains['newPUChain'].GetEntry(i)
    predictedPileup = math.floor(chains['newPUChain'].pileupPrediction)
    truePileup = chains['pileupInfo'].npv

    print(chains['regionEt'].regionEt)
    
    # Each p_t, eta, phi, transverse mass entry has multiple jets in the form of vector<double>.
    for j in range(chains['puppiJet'].etaVector.size()):
        puppiJet = ROOT.TVector3()
        puppiJet.SetPtEtaPhi(chains['puppiJet'].ptVector[j], chains['puppiJet'].etaVector[j], chains['puppiJet'].phiVector[j])
        puppiJetptarr.append(puppiJet)
    for j in range(chains['trigJet'].jetEta.size()):
        trigJet = ROOT.TVector3()
        trigJet.SetPtEtaPhi(chains['trigJet'].jetEt[j], chains['trigJet'].jetEta[j], chains['trigJet'].jetPhi[j])
        trigJetptarr.append(trigJet)
    for j in range(chains['trigJet'].jetIEta.size()):
        phiR = int(chains['trigJet'].jetIEta[j])
        phiRing.append(phiR)

    
    # Matching vectors via deltaR < 0.3
    j = 0
    while tqdm(len(puppiJetptarr) != 0, leave=False):
        minindex = None
        delR = None

        for k in range(len(trigJetptarr)):
            current_delR = ROOT.Math.VectorUtil.DeltaR(puppiJetptarr[j], trigJetptarr[k])
            if current_delR > 0.3:
                continue
             
            if delR == None:
                delR = current_delR
                minindex = k
            
            else:
                if current_delR < delR:
                    delR = current_delR
                    minindex = k
                else:
                    continue
        
        # Place into matched and unmatched
        if minindex:
            cg_matched.append((puppiJetptarr.pop(0), trigJetptarr.pop(minindex)))
            phiRingInfo.append(phiRing.pop(0))

            # For Matching Pileup
            truePileuparr.append(truePileup)
            predPileuparr.append(predictedPileup)
            # print("Popped!")
        else:
            cg_unmatched.append(puppiJetptarr.pop(0))

        
        # Just in Case :)
        if not trigJetptarr:
            if puppiJetptarr:
                cg_unmatched.append(puppiJetptarr.pop(0))

# Construct the Output/y/Goal: difference between the uncalibrated trigger jet pt, and the PUPPI Pt
"""for i in cg_matched:
    y = (i[1].Pt() - i[0].Pt())"""

# Draw Pileup Histograms
c = 0
for i in cg_matched:
    reso = (i[1].Pt() - i[0].Pt())/(i[0].Pt())
    tPileup = truePileuparr[c]
    predPileup = predPileuparr[c]
    c += 1
    if tPileup in range(0,10):
        hp010.Fill(reso)
    elif tPileup in range(10,20):
        hp1020.Fill(reso)
    elif tPileup in range(20,30):
        hp2030.Fill(reso)
    elif tPileup in range(30,40):
        hp3040.Fill(reso)
    elif tPileup in range(40,50):
        hp4050.Fill(reso)
    elif tPileup in range(50,60):
        hp5060.Fill(reso)
    elif tPileup in range(60,70):
        hp6070.Fill(reso)
    elif tPileup in range(70,80):
        hp7080.Fill(reso)
    else:
        pass

    if predPileup in range(0,10):
        hpp010.Fill(reso)
    elif predPileup in range(10,20):
        hpp1020.Fill(reso)
    elif predPileup in range(20,30):
        hpp2030.Fill(reso)
    elif predPileup in range(30,40):
        hpp3040.Fill(reso)
    elif predPileup in range(40,50):
        hpp4050.Fill(reso)
    elif predPileup in range(50,60):
        hpp5060.Fill(reso)
    elif predPileup in range(60,70):
        hpp6070.Fill(reso)
    elif predPileup in range(70,80):
        hpp7080.Fill(reso)
    else:
        pass

fp010 = ROOT.TFile("output/hp010.root", "RECREATE")
fp010.WriteObject(hp010, "hp010")
fp010.WriteObject(hpp010, "hpp010")
print("Histogram 010 Created.") 
fp1020 = ROOT.TFile("output/hp1020.root", "RECREATE")
fp1020.WriteObject(hp1020, "hp1020")
fp1020.WriteObject(hpp1020, "hpp1020")
print("Histogram 1020 Created.") 
fp2030 = ROOT.TFile("output/hp2030.root", "RECREATE")
fp2030.WriteObject(hp2030, ""+"hp2030")
fp2030.WriteObject(hpp2030, ""+"hpp2030")
print("Histogram 2030 Created.")
fp3040 = ROOT.TFile("output/hp3040.root", "RECREATE")
fp3040.WriteObject(hp3040, "hp3040")
fp3040.WriteObject(hpp3040, "hpp3040")
print("Histogram 3040 Created.") 
fp4050 = ROOT.TFile("output/hp4050.root", "RECREATE")
fp4050.WriteObject(hp4050, "hp4050")
fp4050.WriteObject(hpp4050, "hpp4050")
print("Histogram 4050 Created.") 
fp5060 = ROOT.TFile("output/hp5060.root", "RECREATE")
fp5060.WriteObject(hp5060, "hp5060")
fp5060.WriteObject(hpp5060, "hpp5060")
print("Histogram 5060 Created.") 
fp6070 = ROOT.TFile("output/hp6070.root", "RECREATE")
fp6070.WriteObject(hp6070, "hp6070")
fp6070.WriteObject(hpp6070, "hpp6070")
print("Histogram 6070 Created.") 
fp7080 = ROOT.TFile("output/hp7080.root", "RECREATE")
fp7080.WriteObject(hp7080, "hp7080")
fp7080.WriteObject(hpp7080, "hpp7080")
print("Histogram 7080 Created.") 



"""
# Draw the Histogram
for i in cg_matched:
    reso = (i[1].Pt() - i[0].Pt())/(i[0].Pt())
    h.Fill(reso)

resoh = ROOT.TFile("calopuppiResPlot.root", "RECREATE")
resoh.WriteObject(h, "calopuppiResPlot")
print("Histogram Created.")
"""