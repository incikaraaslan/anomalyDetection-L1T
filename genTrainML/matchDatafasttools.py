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
import matplotlib.pyplot as plt
import h5py

tt = ["trainshuf", "testshuf"]

canvas = ROOT.TCanvas('canvas', '', 500, 500)
hjets = ROOT.TH1F("Total Number of Jets", "Total Number of Jets", 100000, 0.0, 1000000.0)
hmatched = ROOT.TH1F("Number of Matched Jets", "Number of Matched Jets", 100000, 0.0, 10000000.0)
hdf5_file_name = 'phiringsub100_dataset.h5'
hdf5_file = h5py.File("output/"+ hdf5_file_name, 'w')
counters = [0, 0, 0, 0, 0, 0]
def createMatchedAndUnmatchedJets(triggerJets, puppiJets, energyfortrigs, tjet):
    unmatchedPuppiJets = []
    unmatchedTriggerJets = triggerJets
    matchedJets = []
    et_fortrigmatched = []
    tjetmatched = []
    # print("Start Matching!")
    for puppiJetIndex, puppiJet in enumerate(puppiJets):
        distances = []
        for triggerJetIndex, triggerJet in enumerate(unmatchedTriggerJets):
            distances.append((triggerJetIndex, puppiJet.DeltaR(triggerJet)))
        distances.sort(key=lambda x: x[1])
        # print(distances)
        # Sort the distances, and remove any trigger jets that don't meet our criteria.
        for i in range(len(distances)):
            if distances[i][1] > 0.4:
                distances = distances[:i]
                break
        # print(distances)
        # if we have no appropriate trigger jets at this point, this is an unmatched puppi jet
        if len(distances) == 0:
            unmatchedPuppiJets.append(puppiJet)
            continue
        # Now we go through and check trigger jet pts
        # We will accept the highest one.
        highestPt = 0.0
        highestIndex = None
        for triggerJetIndex, DeltaR in distances:
            # print(triggerJetIndex, DeltaR)
            # print(unmatchedTriggerJets[triggerJetIndex].Pt())

            if unmatchedTriggerJets[triggerJetIndex].Pt() > highestPt:
                highestIndex = triggerJetIndex
        
        triggerJet = unmatchedTriggerJets.pop(highestIndex)
        tjetmatched = tjet.pop(highestIndex)
    
        """for i in range(len(energyfortrigs[highestIndex])):"""
        matchedJets.append((triggerJet, puppiJet))
        et_fortrigmatched.append(energyfortrigs.pop(highestIndex))
        counters[c+4] += 1
        """if len(matchedJets) == 5:
            print(et_fortrigmatched)
            break"""
    return matchedJets, unmatchedTriggerJets, unmatchedPuppiJets, et_fortrigmatched, tjetmatched


for c in tqdm(range(len(tt))):
    print(tt[c])
    # Lists
    tjet = []
    tcg_matched = []
    ttrig_unmatched = []
    tpuppi_unmatched = []
    tet_fortrigmatched = []
    # Import Files from Data

    # Get all of the file
    # f = open('output/'+tt[c]+'.txt', 'r')

    # Get the first n files from training and test
    with open('output/'+tt[c]+'.txt', 'r') as f:
        head = [next(f) for k in range(100)]

    for x in tqdm(head):
        x = x[:-1]
        chains = pc.prepChains(x)
        """print(chains['puppiJet'].GetEntries())
        print(chains['trigJet'].GetEntries())"""
        counters[c] += 1

        # Match Jet with PUPPI
        for i in tqdm(range(chains['puppiJet'].GetEntries())): # chains['genJet'].GetEntries() - 100000 events if you can
            trigJetptarr = []
            puppiJetptarr = []
            et_fortrig = []
            # phiRing = []
            chains['puppiJet'].GetEntry(i)
            chains['trigJet'].GetEntry(i)
            chains['regionEt'].GetEntry(i)
        
            # Each p_t, eta, phi, transverse mass entry has multiple jets in the form of vector<double>.
            for j in range(chains['puppiJet'].etaVector.size()):
                puppiJet = ROOT.TVector3()
                puppiJet.SetPtEtaPhi(chains['puppiJet'].ptVector[j], chains['puppiJet'].etaVector[j], chains['puppiJet'].phiVector[j])
                puppiJetptarr.append(puppiJet)
            for j in range(chains['trigJet'].jetEta.size()):
                # Preparing Dataset
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
                    if etList == []:
                        print("Empty:")
                        print(chains['trigJet'].jetRawEt[j] * 0.5 ,chains['trigJet'].jetEta[j], chains['trigJet'].jetPhi[j])
                    else:
                        et_fortrig.append(etList)

                        # Fill for Total Jets
                        tjet.append(chains['trigJet'].nJets)
                        hjets.Fill(chains['trigJet'].nJets)
                        counters[c+2] += 1
                else:
                    continue

                # Create the trigJet vectors
                trigJet = ROOT.TVector3()
                # uncalibrated no-PU-subtracted jet Et= (jetRawEt) x 0.5
                # calibrated no-PU-subtracted jet Et = jetRawEt x SF x 0.5
                jetEt = chains['trigJet'].jetRawEt[j] * 0.5
                trigJet.SetPtEtaPhi(jetEt, chains['trigJet'].jetEta[j], chains['trigJet'].jetPhi[j]) # chains['trigJet'].jetEt[j]
                trigJetptarr.append(trigJet)

            # Matching vectors via deltaR < 0.4
            cg_matched, trig_unmatched, puppi_unmatched, et_fortrigmatched, tjetmatched = createMatchedAndUnmatchedJets(trigJetptarr, puppiJetptarr, et_fortrig, tjet)
            if cg_matched != []:
                tcg_matched.append(cg_matched)
                ttrig_unmatched.append(trig_unmatched)
                tpuppi_unmatched.append(tpuppi_unmatched)
                tet_fortrigmatched.append(et_fortrigmatched)

    # Draw Histograms
    # Ratio of Number of Matched to the Total Number of Events
    for i in range(len(tjetmatched)):
        hmatched.Fill(tjetmatched[i])
    
    hmatchedvtotal = hmatched.Clone()
    hmatchedvtotal.Divide(hjets)

    hmatchedvtotal.SetMarkerStyle(8)
    hmatchedvtotal.SetMarkerSize(0.2)
    hmatchedvtotal.SetTitle("")
    hmatchedvtotal.GetYaxis().SetTitle("Frequency")
    hmatchedvtotal.GetXaxis().SetTitle("Ratio of Matched to Total Jets")
    hmatchedvtotal.GetXaxis().SetTitleSize(0.045)
    hmatchedvtotal.GetXaxis().SetTitleOffset(1.1)
    hmatchedvtotal.GetYaxis().SetTitleSize(0.045)
    hmatchedvtotal.GetYaxis().SetTitleOffset(1.0)

    hmatchedvtotal.Draw()
    canvas.Draw()
    canvas.SaveAs("matchedvtotal"+tt[c]+".png")
    canvas.Clear()

    # Average/Absolute pt, eta, phi error for matched jets
    """pterror = []
    etaerror = []
    phierror = []
    for i in range(len(tcg_matched)):
        pterror.append(tcg_matched[i][0][1].Pt() - tcg_matched[i][0][0].Pt())
        etaerror.append(tcg_matched[i][0][1].Eta() - tcg_matched[i][0][0].Eta())
        phierror.append(tcg_matched[i][0][1].Phi() - tcg_matched[i][0][0].Phi())
    
    averagept_error = np.mean(np.asarray(pterror))
    averageeta_error = np.mean(np.asarray(etaerror))
    averagephi_error = np.mean(np.asarray(phierror))
    
    plt.figure(figsize=(10, 5))
    plt.hist(pterror, bins=50, color='red', alpha=0.7, label=tt[c]+'TRIG/PUPPI pT Error')
    plt.title('Histogram of Absolute Errors ('+tt[c]+' Average Error: {:.2f})'.format(averagept_error))
    plt.xlabel('Absolute Errors')
    plt.ylabel('Frequency')
    plt.savefig('ErrorPUPPIvTrigPt'+tt[c]+'.png')
    plt.figure(figsize=(10, 5))
    plt.hist(etaerror, bins=50, color='red', alpha=0.7, label=tt[c]+'TRIG/PUPPI eta Error')
    plt.title('Histogram of Absolute Errors ('+tt[c]+' Average Error: {:.2f})'.format(averageeta_error))
    plt.xlabel('Absolute Errors')
    plt.ylabel('Frequency')
    plt.savefig('ErrorPUPPIvTrigeta'+tt[c]+'.png')
    plt.figure(figsize=(10, 5))
    plt.hist(phierror, bins=50, color='red', alpha=0.7, label=tt[c]+'TRIG/PUPPI phi Error')
    plt.title('Histogram of Absolute Errors ('+tt[c]+' Average Error: {:.2f})'.format(averagephi_error))
    plt.xlabel('Absolute Errors')
    plt.ylabel('Frequency')
    plt.savefig('ErrorPUPPIvTrigphi'+tt[c]+'.png')"""
    

