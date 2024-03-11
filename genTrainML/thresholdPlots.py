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


for c in tqdm(range(len(tt))):
    print(tt[c])
    # Lists

    # Import Files from Data
    # Get all of the file
    """f = open('output/'+tt[c]+'.txt', 'r')"""

    # Get the first n files from training and test
    with open('output/'+tt[c]+'.txt', 'r') as f:
        head = [next(f) for k in range(1)]

    for x in tqdm(head):
        x = x[:-1]
        chains = pc.prepChains(x)
        
        for i in tqdm(range(chains['trigJet'].GetEntries())):
            
            chains['trigJet'].GetEntry(i)
            chains['regionEt'].GetEntry(i)
            chains['PUChainPUPPI'].GetEntry(i)

            # Singular Calculation
            npv = chains['PUChainPUPPI'].npv
            
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
                    # print(chains['regionEt'].regionEt.size())
                    etList = []
                    trigiPhi = round((chains['trigJet'].jetIPhi[j]-jet_regionIndex)/14)
                    for iPhi in range(18):
                        # No Subtraction where the Trigger Jet Hits
                        etList.append(chains['regionEt'].regionEt[iPhi*14 + jet_regionIndex])

                        # Subtract where the Trigger Jet Hits
                        """if iPhi == trigiPhi:
                            continue
                        else:
                            etList.append(chains['regionEt'].regionEt[iPhi*14 + jet_regionIndex])"""

                        # Only take a circular region from Trigger Jet Hits
                        """if iPhi == trigiPhi:
                            # a = np.asarray(chains['regionEt'].regionEt).reshape(14,18)
                            # etList.append(chains['regionEt'].regionEt[iPhi*14 + jet_regionIndex])
                            circleofPhi(iPhi, jet_regionIndex)
                            circleofPhi(iPhi, jet_regionIndex + 1)
                            circleofPhi(iPhi, jet_regionIndex - 1)
                            # print(etList)
                        else:
                            continue"""
                    
                    # If no specific circle
                    if etList == []:
                        print("Empty:")
                        print(chains['trigJet'].jetRawEt[j] * 0.5 ,chains['trigJet'].jetEta[j], chains['trigJet'].jetPhi[j])
                    else:
                        et_fortrig.append(etList)
                        # print(et_fortrig, len(et_fortrig))
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