import ROOT
from tqdm import tqdm
import os
import prepChains as pc
import iEtaiPhiBinning
import numpy as np
import pandas as pd
import math
import random
from time import perf_counter
import h5py

tt = ["train", "test"]

hdf5_file_name = 'phiringsub_dataset.h5'
hdf5_file = h5py.File("output/"+ hdf5_file_name, 'w')

for c in tqdm(range(len(tt))):
    print(tt[c])
    # Import Files from Data
    f = open('output/'+tt[c]+'.txt', 'r')
    for x in f:
        chains = pc.prepChains(x)

    """
    # Create the Histogram
    h = ROOT.TH1F("calopuppiResPlot", "Resolution Plot", 100, -4.0, 4.0)
    # Create Pileup Histograms
    canvas = ROOT.TCanvas()
    hp = ROOT.TH1F("calopuppiResPlot", "Resolution Plot", 100, -1.0, 1.0)
    hp010 = ROOT.TH1F("calopuppiResPlot 0-10", "Resolution Plot 0-10", 100, -1.0, 1.0)
    hp1020 = ROOT.TH1F("calopuppiResPlot 10-20", "Resolution Plot 10-20", 100, -1.0, 1.0)
    hp2030 = ROOT.TH1F("calopuppiResPlot 20-30", "Resolution Plot 20-30", 100, -1.0, 1.0)
    hp3040 = ROOT.TH1F("calopuppiResPlot 30-40", "Resolution Plot 30-40", 100, -1.0, 1.0)
    hp4050 = ROOT.TH1F("calopuppiResPlot 40-50", "Resolution Plot 40-50", 100, -1.0, 1.0)
    hp5060 = ROOT.TH1F("calopuppiResPlot 50-60", "Resolution Plot 50-60", 100, -1.0, 1.0)
    hp6070 = ROOT.TH1F("calopuppiResPlot 60-70", "Resolution Plot 60-70", 100, -1.0, 1.0)
    hp7080 = ROOT.TH1F("calopuppiResPlot 70-80", "Resolution Plot 70-80", 100, -1.0, 1.0)"""

    # Lists
    cg_matched = []
    cg_unmatched = []
    et_fortrigmatched = []
    # phiRingInfo = []
    # uphiRingInfo = []

    # For Drawing Pileup Histograms
    """truePileuparr = []"""


    # Next: what iPhi ring in the regions the trigger jet we have just used belongs to
    # Then: get the regions that correspond to this ring from my quick ntuplizer for the regions L1RegionNtuplizer 
    # (stored in iEta then iPhi indices ([14][18]), you may have to reconstruct it from flat). 
    # For now, simply take every phi energy deposit across the ring (all 18). 

    # Match Jet with PUPPI
    for i in tqdm(range(chains['trigJet'].GetEntries())): # chains['genJet'].GetEntries() - 100000 events if you can
        trigJetptarr = []
        puppiJetptarr = []
        et_fortrig = []
        # phiRing = []
        chains['puppiJet'].GetEntry(i)
        chains['trigJet'].GetEntry(i)
        chains['regionEt'].GetEntry(i)

        # For Drawing Pileup Histograms
        """chains['PUChainPUPPI'].GetEntry(i)
        truePileup = chains['PUChainPUPPI'].npv"""
        
        # Each p_t, eta, phi, transverse mass entry has multiple jets in the form of vector<double>.
        for j in range(chains['puppiJet'].etaVector.size()):
            puppiJet = ROOT.TVector3()
            puppiJet.SetPtEtaPhi(chains['puppiJet'].ptVector[j], chains['puppiJet'].etaVector[j], chains['puppiJet'].phiVector[j])
            puppiJetptarr.append(puppiJet)
        for j in range(chains['trigJet'].jetEta.size()):
            # Regular detector iEta into Our Region iEta
            jetEta = float(chains['trigJet'].jetEta[j])
            the_iEtaiPhiBinCollection = iEtaiPhiBinning.iEtaiPhiBinCollection()
            jet_iEta = the_iEtaiPhiBinCollection.iEta(jetEta)
            if jet_iEta is not None:
                jet_regionIndex = jet_iEta - 4  #take values 0-13, discard anything else.
            else:
                continue
            # Now for each iEta we have a phiRing associated with it. Get all Phi vals for that phiRing
            if 0 <= jet_regionIndex <= 13:
                #print(chains['regionEt'].regionEt.size())
                etList = []
                for iPhi in range(18):
                    etList.append(chains['regionEt'].regionEt[iPhi*14 + jet_regionIndex])
                et_fortrig.append(etList)
            else:
                continue

            # Create the trigJet vectors
            trigJet = ROOT.TVector3()
            jetEt = chains['trigJet'].jetRawEt[j] + chains['trigJet'].jetPUEt[j]
            trigJet.SetPtEtaPhi(jetEt, chains['trigJet'].jetEta[j], chains['trigJet'].jetPhi[j]) # chains['trigJet'].jetEt[j]
            trigJetptarr.append(trigJet)

        
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
                et_fortrigmatched.append(et_fortrig.pop(minindex))
                # phiRingInfo.append(phiRing.pop(0))

                # For Matching Pileup
                """truePileuparr.append(truePileup)"""
                # print("Popped!")
            else:
                cg_unmatched.append(puppiJetptarr.pop(0))

            
            # Just in Case :)
            if not trigJetptarr:
                if puppiJetptarr:
                    cg_unmatched.append(puppiJetptarr.pop(0))

    # Construct the HDF5 Dataset
    # Construct the Output/y/Goal: difference between the uncalibrated trigger jet pt, and the PUPPI Pt
    y = []
    for i in cg_matched:
        y.append(i[1].Pt() - i[0].Pt())

    # Input: The energy deposit across the Phi Ring --> et_fortrigmatched
    print(tt[c])
    hdf5_file.create_dataset('PhiRingEt'+tt[c], data=et_fortrigmatched)
    hdf5_file.create_dataset('PuppiTrigEtDiff'+tt[c], data=y)
    f.close()
hdf5_file.close()

# Draw Pileup Histograms
"""c = 0
for i in cg_matched:
    reso = (i[1].Pt() - i[0].Pt())/(i[0].Pt())
    tPileup = truePileuparr[c]
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
        pass"""

"""fp010 = ROOT.TFile("output/hp010PURAW.root", "RECREATE")
fp010.WriteObject(hp010, "hp010PURAW")
print("Histogram 010 Created.") 
fp1020 = ROOT.TFile("output/hp1020PURAW.root", "RECREATE")
fp1020.WriteObject(hp1020, "hp1020PURAW")
print("Histogram 1020 Created.") 
fp2030 = ROOT.TFile("output/hp2030PURAW.root", "RECREATE")
fp2030.WriteObject(hp2030, "hp2030PURAW")
print("Histogram 2030 Created.")
fp3040 = ROOT.TFile("output/hp3040PURAW.root", "RECREATE")
fp3040.WriteObject(hp3040, "hp3040PURAW")
print("Histogram 3040 Created.") 
fp4050 = ROOT.TFile("output/hp4050PURAW.root", "RECREATE")
fp4050.WriteObject(hp4050, "hp4050PURAW")
print("Histogram 4050 Created.") 
fp5060 = ROOT.TFile("output/hp5060PURAW.root", "RECREATE")
fp5060.WriteObject(hp5060, "hp5060PURAW")
print("Histogram 5060 Created.") 
fp6070 = ROOT.TFile("output/hp6070PURAW.root", "RECREATE")
fp6070.WriteObject(hp6070, "hp6070PURAW")
print("Histogram 6070 Created.") 
fp7080 = ROOT.TFile("output/hp7080PURAW.root", "RECREATE")
fp7080.WriteObject(hp7080, "hp7080PURAW")
print("Histogram 7080 Created.") """

"""
# Draw the Histogram
for i in cg_matched:
    reso = (i[1].Pt() - i[0].Pt())/(i[0].Pt())
    h.Fill(reso)

resoh = ROOT.TFile("./output/calopuppiResPlotPURAW.root", "RECREATE")
resoh.WriteObject(h, "calopuppiResPlotPURAW")
print("Histogram Created.")
"""