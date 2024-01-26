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

tt = ["trainshuf", "testshuf"]

hdf5_file_name = 'phiringsub100_dataset.h5'
hdf5_file = h5py.File("output/"+ hdf5_file_name, 'w')
counters = [0, 0, 0, 0, 0, 0]
def createMatchedAndUnmatchedJets(triggerJets, puppiJets, energyfortrigs):
    unmatchedPuppiJets = []
    unmatchedTriggerJets = triggerJets
    matchedJets = []
    et_fortrigmatched = []
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
        """for i in range(len(energyfortrigs[highestIndex])):"""
        matchedJets.append((triggerJet, puppiJet))
        et_fortrigmatched.append(energyfortrigs.pop(highestIndex))
        counters[c+4] += 1
        """if len(matchedJets) == 5:
            print(et_fortrigmatched)
            break"""
    return matchedJets, unmatchedTriggerJets, unmatchedPuppiJets, et_fortrigmatched


for c in tqdm(range(len(tt))):
    print(tt[c])
    # Lists
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
            cg_matched, trig_unmatched, puppi_unmatched, et_fortrigmatched = createMatchedAndUnmatchedJets(trigJetptarr, puppiJetptarr, et_fortrig)
            if cg_matched != []:
                tcg_matched.append(cg_matched)
                ttrig_unmatched.append(trig_unmatched)
                tpuppi_unmatched.append(tpuppi_unmatched)
                tet_fortrigmatched.append(et_fortrigmatched)

    # Construct the HDF5 Dataset
    print(len(tcg_matched), len(tet_fortrigmatched)) # 46790 46790 # 7064 7064

    # Input: The energy deposit across the Phi Ring --> et_fortrigmatched
    x = []
    for a in range(len(tet_fortrigmatched)):
        for b in range(len(tet_fortrigmatched[a])):
            x.append(tet_fortrigmatched[a][b])
    # Construct the Output/y/Goal: difference between the uncalibrated trigger jet pt, and the PUPPI Pt
    y = []
    for i in range(len(tcg_matched)):
        for j in range(len(tet_fortrigmatched[i])):
            y.append(tcg_matched[i][0][1].Pt() - tcg_matched[i][0][0].Pt())
    print(len(y), len(x)) #7064 8153 multiple ET regions for a PUPPI jet value --> 
    hdf5_file.create_dataset('PhiRingEt'+tt[c], data=x)
    hdf5_file.create_dataset('PuppiTrigEtDiff'+tt[c], data=y)
    f.close()
    
hdf5_file.close()
print("Number of files Training: "+ str(counters[0]) + " Test: " + str(counters[1])) 
print("Number of etaphiring acceptable Training: "+ str(counters[2]) + " Test: " + str(counters[3])) 
print("Number of matched Training: "+ str(counters[4]) + " Test: " + str(counters[5])) 
print("File Created.")
print("File Created.")
