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
counters = [0, 0, 0, 0, 0, 0]
delputrigvnpv = ROOT.TH2F("delputrigvnpv", "del(PUPPI P_T, TRIG P_T) v. npv", 100, 0.0, 80, 100, -20.0, 20)
hcaldelputrig = ROOT.TH2F("nHCALtpvEtdelputrig", "nHCALtp v. del(PUPPI P_T, TRIG P_T)", 100, -70.0, 70, 100, 0.0, 1200)
totalhcaletdelputrig = ROOT.TH2F("totalhcalEtvEtdelputrig", "totalhcaltpEt v. del(PUPPI P_T, TRIG P_T)", 100, -70.0, 70, 100, 0.0, 1500)
phiringetnpv = ROOT.TH2F("phiringEtnpv", "totalphiringEt v. npv", 100, 0.0, 70, 100, 0.0, 300)
phiringetdelputrig = ROOT.TH2F("phiringEtdelputrig", "totalphiringEt v. del(PUPPI P_T, TRIG P_T)", 100, -70.0, 70, 100, 0.0, 300)
phiringsubtrigetnpv = ROOT.TH2F("phiringsubtrigEtnpv", "Total (phiring-trigiphi) E_T v. npv", 100, 0.0, 70, 100, 0.0, 300)
phiringsubtrigetputrig = ROOT.TH2F("phiringsubtrigEtnpv", "Total (phiring-trigiphi) E_T v. del(PUPPI P_T, TRIG P_T)", 100, -70.0, 70, 100, 0.0, 300)

def createMatchedAndUnmatchedJets(triggerJets, puppiJets, energyfortrigs):
    unmatchedPuppiJets = []
    indexunmatched = []
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
            indexunmatched.append(puppiJetIndex)
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
        matchedJets.append((triggerJet, puppiJet))
        et_fortrigmatched.append(energyfortrigs.pop(highestIndex))
        counters[c+4] += 1
        """if len(matchedJets) == 5:
            print(et_fortrigmatched)
            break"""
    return matchedJets, unmatchedTriggerJets, unmatchedPuppiJets, et_fortrigmatched, indexunmatched

def circleofPhi(iPhi, jet_regionIndex):
    if iPhi*14 <= (iPhi*14 + jet_regionIndex) <= iPhi*14 + 13:
        etList.append(chains['regionEt'].regionEt[iPhi*14 + jet_regionIndex])
        if 0 <= ((iPhi-1)*14 + jet_regionIndex) < len(chains['regionEt'].regionEt):
            etList.append(chains['regionEt'].regionEt[(iPhi-1)*14 + jet_regionIndex])
        if 0 <= ((iPhi+1)*14 + jet_regionIndex) < len(chains['regionEt'].regionEt):
            etList.append(chains['regionEt'].regionEt[(iPhi+1)*14 + jet_regionIndex])


for c in tqdm(range(len(tt))):
    print(tt[c])
    # Lists
    tcg_matched = []
    ttrig_unmatched = []
    tpuppi_unmatched = []
    tet_fortrigmatched = []
    tindexunmatched = []
    t_npv = []
    """t_hcaltpet = []
    t_nHCALTP = []"""
    # Import Files from Data

    # Get all of the file
    # f = open('output/'+tt[c]+'.txt', 'r')

    # Get the first n files from training and test
    with open('output/'+tt[c]+'.txt', 'r') as f:
        head = [next(f) for k in range(100)]

    for x in tqdm(head):
        x = x[:-1]
        chains = pc.prepChains(x)
        counters[c] += 1

        # Match Jet with PUPPI
        for i in tqdm(range(chains['puppiJet'].GetEntries())): # chains['genJet'].GetEntries() - 100000 events if you can
            trigJetptarr = []
            puppiJetptarr = []
            et_fortrig = []
            npvs = []
            """hcaltpets = []
            nHCALTPs = []"""

            chains['puppiJet'].GetEntry(i)
            chains['trigJet'].GetEntry(i)
            chains['regionEt'].GetEntry(i)
            chains['PUChainPUPPI'].GetEntry(i)
            chains['caloTower'].GetEntry(i)
            
            # Singular Calculation
            npv = chains['PUChainPUPPI'].npv
            """nHCALTP = chains['caloTower'].CaloTP.nHCALTP
            hcaltpet = 0.0
            for j in range(chains['caloTower'].CaloTP.hcalTPet.size()):
                hcaltpet += chains['caloTower'].CaloTP.hcalTPet[j]"""
            
        
            # Each p_t, eta, phi, transverse mass entry has multiple jets in the form of vector<double>.
            for j in range(chains['puppiJet'].etaVector.size()):
                puppiJet = ROOT.TVector3()
                puppiJet.SetPtEtaPhi(chains['puppiJet'].ptVector[j], chains['puppiJet'].etaVector[j], chains['puppiJet'].phiVector[j])
                puppiJetptarr.append(puppiJet)
                npvs.append(npv)
                """hcaltpets.append(hcaltpet)
                nHCALTPs.append(nHCALTP)"""
            
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

            # Matching vectors via deltaR < 0.4
            cg_matched, trig_unmatched, puppi_unmatched, et_fortrigmatched, indexunmatched = createMatchedAndUnmatchedJets(trigJetptarr, puppiJetptarr, et_fortrig)
            indexunmatched = np.asarray(indexunmatched)
            if cg_matched != []:
                tcg_matched.append(cg_matched)
                ttrig_unmatched.append(trig_unmatched)
                tpuppi_unmatched.append(tpuppi_unmatched)
                tet_fortrigmatched.append(et_fortrigmatched)
        
            # print(indexunmatched, npvs)
            for index in sorted(indexunmatched, reverse=True):
                if 0 <= index < len(npvs):
                    del npvs[index]
                    """del hcaltpets[index]
                    del nHCALTPs[index]"""
            if npvs != []:
                t_npv.append(npvs)
                """t_hcaltpet.append(hcaltpets)
                t_nHCALTP.append(nHCALTPs)"""
            # print(len(t_npv), t_npv)
            # print(len(npvs), npvs)
                     
            
    # Draw Histograms
# HCALEt and nHCALTP v. Del(PUPPI - TRIG) P_T
    """delputrig = []
    for i in range(len(tcg_matched)):
        for j in range(len(tet_fortrigmatched[i])):
            delputrig.append(tcg_matched[i][0][1].Pt() - tcg_matched[i][0][0].Pt())
    
    hcaltpetss =[]
    for a in range(len(t_hcaltpet)):
        for b in range(len(t_hcaltpet[a])):
            hcaltpetss.append(t_hcaltpet[a][b])
    
    nHCALTPss =[]
    for a in range(len(t_nHCALTP)):
        for b in range(len(t_nHCALTP[a])):
            hcaltpetss.append(t_nHCALTP[a][b])

    print(len(delputrig), len(hcaltpetss), len(nHCALTPss))
    
    for a in range(len(hcaltpetss)):
        totalhcaletdelputrig.Fill(delputrig[a], hcaltpetss[a])

    totalhcaletdelputrig.Fit("pol1")
    totalhcaletdelputrig.GetFunction("pol1").SetLineColor(1)
    totalhcaletdelputrig.SetLineColor(46)
    totalhcaletdelputrig.SetMarkerColor(46)
    totalhcaletdelputrig.SetMarkerStyle(8)
    totalhcaletdelputrig.SetMarkerSize(0.5)
    totalhcaletdelputrig.SetTitle("HCAL E_T v. Del(PUPPI - TRIG) P_T")
    totalhcaletdelputrig.GetXaxis().SetTitle("Del(PUPPI - TRIG) P_T")
    totalhcaletdelputrig.GetYaxis().SetTitle("HCAL E_T")
    totalhcaletdelputrig.GetXaxis().SetTitleSize(0.045)
    totalhcaletdelputrig.GetXaxis().SetTitleOffset(0.9)
    totalhcaletdelputrig.GetYaxis().SetTitleSize(0.045)
    totalhcaletdelputrig.GetYaxis().SetTitleOffset(0.9)
    totalhcaletdelputrig.Draw("COLZ")
    canvas.Draw()
    canvas.SaveAs('controlPlots/totalhcaletdelputrig'+str(tt[c])+'.png')
    print("Hist 1 Done.")

    canvas.Clear()

    for a in range(len(nHCALTPss)):
        hcaldelputrig.Fill(delputrig[a], nHCALTPss[a])

    hcaldelputrig.Fit("pol1")
    hcaldelputrig.GetFunction("pol1").SetLineColor(1)
    hcaldelputrig.SetLineColor(46)
    hcaldelputrig.SetMarkerColor(46)
    hcaldelputrig.SetMarkerStyle(8)
    hcaldelputrig.SetMarkerSize(0.5)
    hcaldelputrig.SetTitle("nHCALTP E_T v. Del(PUPPI - TRIG) P_T")
    hcaldelputrig.GetXaxis().SetTitle("Del(PUPPI - TRIG) P_T")
    hcaldelputrig.GetYaxis().SetTitle("nHCALTP E_T")
    hcaldelputrig.GetXaxis().SetTitleSize(0.045)
    hcaldelputrig.GetXaxis().SetTitleOffset(0.9)
    hcaldelputrig.GetYaxis().SetTitleSize(0.045)
    hcaldelputrig.GetYaxis().SetTitleOffset(0.9)
    hcaldelputrig.Draw("COLZ")
    canvas.Draw()
    canvas.SaveAs('controlPlots/hcaldelputrig'+str(tt[c])+'.png')
    print("Hist 2 Done.")
    """

# PhiRing Circle E_t v Del(PUPPI - TRIG) P_T
    """summ = []
    for a in range(len(tet_fortrigmatched)):
        for b in range(len(tet_fortrigmatched[a])):
            summ.append(np.sum(np.asarray(tet_fortrigmatched[a][b])))

    delputrig = []
    
    for i in range(len(tcg_matched)):
        for j in range(len(tet_fortrigmatched[i])):
            delputrig.append(tcg_matched[i][0][1].Pt() - tcg_matched[i][0][0].Pt())
    
    print(len(summ), len(delputrig))

    for a in range(len(summ)):
        phiringetdelputrig.Fill(delputrig[a], summ[a])
    
    phiringetdelputrig.Fit("pol1")
    phiringetdelputrig.GetFunction("pol1").SetLineColor(1)
    phiringetdelputrig.SetLineColor(46)
    phiringetdelputrig.SetMarkerColor(46)
    phiringetdelputrig.SetMarkerStyle(8)
    phiringetdelputrig.SetMarkerSize(0.5)
    phiringetdelputrig.SetTitle("Phi Ring Circle E_T v. del(PUPPI P_T, TRIG P_T)")
    phiringetdelputrig.GetYaxis().SetTitle("Phi Ring Circle E_T")
    phiringetdelputrig.GetXaxis().SetTitle("del(PUPPI P_T, TRIG P_T)")
    phiringetdelputrig.GetXaxis().SetTitleSize(0.045)
    phiringetdelputrig.GetXaxis().SetTitleOffset(0.9)
    phiringetdelputrig.GetYaxis().SetTitleSize(0.045)
    phiringetdelputrig.GetYaxis().SetTitleOffset(0.9)
    phiringetdelputrig.Draw("COLZ")
    canvas.Draw()
    canvas.SaveAs('controlPlots/phiringcircetdelputrig'+str(tt[c])+'.png')
    print("Hist 1 Done.")

    canvas.Clear()"""

# PhiRing Circle E_t v npv
    """summ = []
    for a in range(len(tet_fortrigmatched)):
        for b in range(len(tet_fortrigmatched[a])):
            summ.append(np.sum(np.asarray(tet_fortrigmatched[a][b])))
    
    npvss =[]
    for a in range(len(t_npv)):
        for b in range(len(t_npv[a])):
            npvss.append(t_npv[a][b])

    print(len(summ), len(npvss))
    
    for a in range(len(npvss)):
        phiringetnpv.Fill(npvss[a], summ[a])
    
    phiringetnpv.Fit("pol1")
    phiringetnpv.GetFunction("pol1").SetLineColor(1)
    phiringetnpv.SetLineColor(46)
    phiringetnpv.SetMarkerColor(46)
    phiringetnpv.SetMarkerStyle(8)
    phiringetnpv.SetMarkerSize(0.5)
    phiringetnpv.SetTitle("Phi Ring Circle E_T v. npv")
    phiringetnpv.GetXaxis().SetTitle("npv")
    phiringetnpv.GetYaxis().SetTitle("Phi Ring Circle E_T")
    phiringetnpv.GetXaxis().SetTitleSize(0.045)
    phiringetnpv.GetXaxis().SetTitleOffset(0.9)
    phiringetnpv.GetYaxis().SetTitleSize(0.045)
    phiringetnpv.GetYaxis().SetTitleOffset(0.9)
    phiringetnpv.Draw("COLZ")
    canvas.Draw()
    canvas.SaveAs('controlPlots/phiringetnpv'+str(tt[c])+'.png')
    print("Hist 2 Done.")"""

# Total PhiRing E_t v Del(PUPPI - TRIG) P_T
    """
    summ = []
    for a in range(len(tet_fortrigmatched)):
        for b in range(len(tet_fortrigmatched[a])):
            summ.append(np.sum(np.asarray(tet_fortrigmatched[a][b])))

    delputrig = []
    for i in range(len(tcg_matched)):
        for j in range(len(tet_fortrigmatched[i])):
            delputrig.append(tcg_matched[i][0][1].Pt() - tcg_matched[i][0][0].Pt())
    
    for a in range(len(summ)):
        phiringetdelputrig.Fill(delputrig[a], summ[a])
    
    phiringetdelputrig.Fit("pol1")
    phiringetdelputrig.GetFunction("pol1").SetLineColor(1)
    phiringetdelputrig.SetLineColor(46)
    phiringetdelputrig.SetMarkerColor(46)
    phiringetdelputrig.SetMarkerStyle(8)
    phiringetdelputrig.SetMarkerSize(0.5)
    phiringetdelputrig.SetTitle("Phi Ring Total E_T v. del(PUPPI P_T, TRIG P_T)")
    phiringetdelputrig.GetYaxis().SetTitle("del(PUPPI P_T, TRIG P_T)")
    phiringetdelputrig.GetXaxis().SetTitle("Phi Ring Total E_T")
    phiringetdelputrig.GetXaxis().SetTitleSize(0.045)
    phiringetdelputrig.GetXaxis().SetTitleOffset(0.9)
    phiringetdelputrig.GetYaxis().SetTitleSize(0.045)
    phiringetdelputrig.GetYaxis().SetTitleOffset(0.9)
    phiringetdelputrig.Draw("COLZ")
    canvas.Draw()
    canvas.SaveAs('controlPlots/phiringetdelputrig'+str(tt[c])+'.png')
    print("Hist 1 Done.")

    canvas.Clear()

    # Total PhiRing E_t v npv
    summ = []
    for a in range(len(tet_fortrigmatched)):
        for b in range(len(tet_fortrigmatched[a])):
            summ.append(np.sum(np.asarray(tet_fortrigmatched[a][b])))
    
    npvss =[]
    for a in range(len(t_npv)):
        for b in range(len(t_npv[a])):
            npvss.append(t_npv[a][b])

    print(len(summ), len(npvss))
    
    for a in range(len(npvss)):
        phiringetnpv.Fill(npvss[a], summ[a])
    
    phiringetnpv.Fit("pol1")
    phiringetnpv.GetFunction("pol1").SetLineColor(1)
    phiringetnpv.SetLineColor(46)
    phiringetnpv.SetMarkerColor(46)
    phiringetnpv.SetMarkerStyle(8)
    phiringetnpv.SetMarkerSize(0.5)
    phiringetnpv.SetTitle("Phi Ring Total E_T v. npv")
    phiringetnpv.GetXaxis().SetTitle("npv")
    phiringetnpv.GetYaxis().SetTitle("Phi Ring Total E_T")
    phiringetnpv.GetXaxis().SetTitleSize(0.045)
    phiringetnpv.GetXaxis().SetTitleOffset(0.9)
    phiringetnpv.GetYaxis().SetTitleSize(0.045)
    phiringetnpv.GetYaxis().SetTitleOffset(0.9)
    phiringetnpv.Draw("COLZ")
    canvas.Draw()
    canvas.SaveAs('controlPlots/phiringetnpv'+str(tt[c])+'.png')
    print("Hist 2 Done.")
    """
    
# Total PhiRing E_T - Subtract Energy where the Trig Jet Landed v npv
    """summ = []
    for a in range(len(tet_fortrigmatched)):
        for b in range(len(tet_fortrigmatched[a])):
            summ.append(np.sum(np.asarray(tet_fortrigmatched[a][b])))

    npvss =[]
    for a in range(len(t_npv)):
        for b in range(len(t_npv[a])):
            npvss.append(t_npv[a][b])

    print(len(summ), len(npvss))
    for a in range(len(npvss)):
        phiringsubtrigetnpv.Fill(npvss[a], summ[a])

    phiringsubtrigetnpv.Fit("pol1")
    phiringsubtrigetnpv.GetFunction("pol1").SetLineColor(1)
    phiringsubtrigetnpv.SetLineColor(46)
    phiringsubtrigetnpv.SetMarkerColor(46)
    phiringsubtrigetnpv.SetMarkerStyle(8)
    phiringsubtrigetnpv.SetMarkerSize(0.5)
    phiringsubtrigetnpv.SetTitle("Total (iPhi Ring - Trig iPhi) E_T v. npv")
    phiringsubtrigetnpv.GetXaxis().SetTitle("npv")
    phiringsubtrigetnpv.GetYaxis().SetTitle("iPhi Ring - Trig iPhi Total E_T")
    phiringsubtrigetnpv.GetXaxis().SetTitleSize(0.045)
    phiringsubtrigetnpv.GetXaxis().SetTitleOffset(0.9)
    phiringsubtrigetnpv.GetYaxis().SetTitleSize(0.045)
    phiringsubtrigetnpv.GetYaxis().SetTitleOffset(0.9)
    phiringsubtrigetnpv.Draw("COLZ")
    canvas.Draw()
    canvas.SaveAs('controlPlots/ELphiringsubtrigetnpv'+str(tt[c])+'.png')
    print("Hist 1 Done.")

    # f = ROOT.TF1("f", "[1] * (x ** (0.5)) + [0]")
    # phiringsubtrigetnpv.Fit("f")

    canvas.Clear()

    # Total PhiRing E_T - Subtract Energy where the Trig Jet Landed v Del(PUPPI - TRIG) P_T
    summ = []
    for a in range(len(tet_fortrigmatched)):
        for b in range(len(tet_fortrigmatched[a])):
            summ.append(np.sum(np.asarray(tet_fortrigmatched[a][b])))

    delputrig = []
    for i in range(len(tcg_matched)):
        for j in range(len(tet_fortrigmatched[i])):
            delputrig.append(tcg_matched[i][0][1].Pt() - tcg_matched[i][0][0].Pt())
    
    for a in range(len(summ)):
        phiringsubtrigetputrig.Fill(delputrig[a],summ[a])
    
    phiringsubtrigetputrig.Fit("pol1")
    phiringsubtrigetputrig.GetFunction("pol1").SetLineColor(1)
    phiringsubtrigetputrig.SetLineColor(46)
    phiringsubtrigetputrig.SetMarkerColor(46)
    phiringsubtrigetputrig.SetMarkerStyle(8)
    phiringsubtrigetputrig.SetMarkerSize(0.5)
    phiringsubtrigetputrig.SetTitle("Total (iPhi Ring - Trig iPhi) E_T v. del(PUPPI P_T, TRIG P_T)")
    phiringsubtrigetputrig.GetXaxis().SetTitle("del(PUPPI P_T, TRIG P_T)")
    phiringsubtrigetputrig.GetYaxis().SetTitle("iPhi Ring - Trig iPhi Total E_T")
    phiringsubtrigetputrig.GetXaxis().SetTitleSize(0.045)
    phiringsubtrigetputrig.GetXaxis().SetTitleOffset(0.9)
    phiringsubtrigetputrig.GetYaxis().SetTitleSize(0.045)
    phiringsubtrigetputrig.GetYaxis().SetTitleOffset(0.9)
    phiringsubtrigetputrig.Draw("COLZ")
    canvas.Draw()
    canvas.SaveAs('controlPlots/ELphiringsubtrigetputrig'+str(tt[c])+'.png')
    print("Hist 2 Done.")"""

# Del(PUPPI - TRIG) P_T v. npv
    npvss =[]
    for a in range(len(t_npv)):
        for b in range(len(t_npv[a])):
            npvss.append(t_npv[a][b])

    delputrig = []
    for i in range(len(tcg_matched)):
        for j in range(len(tet_fortrigmatched[i])):
            delputrig.append(tcg_matched[i][0][1].Pt() - tcg_matched[i][0][0].Pt())
    
    print(len(delputrig), len(npvss))

    a = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    b = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    f = [0,0,0,0,0,0,0,0]
    for i in range(len(delputrig)):
        if 0 <= npvss[i] <= 10:
            f[0] += 1
            a[0] += npvss[i]
            b[0] += delputrig[i]
        if 10 < npvss[i] <= 20:
            f[1] += 1
            a[1] += npvss[i]
            b[1] += delputrig[i]
        if 20 < npvss[i] <= 30:
            f[2] += 1
            a[2] += npvss[i]
            b[2] += delputrig[i]
        if 30 < npvss[i] <= 40:
            f[3] += 1
            a[3] += npvss[i]
            b[3] += delputrig[i]
        if 40 < npvss[i] <= 50:
            f[4] += 1
            a[4] += npvss[i]
            b[4] += delputrig[i]
        if 50 < npvss[i] <= 60:
            f[5] += 1
            a[5] += npvss[i]
            b[5] += delputrig[i]
        if 60 < npvss[i] <= 70:
            f[6] += 1
            a[6] += npvss[i]
            b[6] += delputrig[i]
        if 70 < npvss[i] <= 80:
            f[7] += 1
            a[7] += npvss[i]
            b[7] += delputrig[i]

    for i in range(len(b)):
        delputrigvnpv.Fill(np.asarray(a[i])/np.asarray(f[i]), np.asarray(b[i])/np.asarray(f[i]))
        
    delputrigvnpv.SetLineColor(46)
    delputrigvnpv.SetMarkerColor(46)
    delputrigvnpv.SetMarkerStyle(8)
    delputrigvnpv.SetMarkerSize(0.5)
    delputrigvnpv.SetTitle("Averaged del(PUPPI P_T, TRIG P_T) v. npv")
    delputrigvnpv.GetXaxis().SetTitle("npv")
    delputrigvnpv.GetYaxis().SetTitle("Averaged Del(PUPPI - TRIG) P_T")
    delputrigvnpv.GetXaxis().SetTitleSize(0.045)
    delputrigvnpv.GetXaxis().SetTitleOffset(0.9)
    delputrigvnpv.GetYaxis().SetTitleSize(0.045)
    delputrigvnpv.GetYaxis().SetTitleOffset(0.9)
    delputrigvnpv.Draw("PLC PMC")
    canvas.Draw()
    canvas.SaveAs('controlPlots/delputrigvnpvlinedhist'+str(tt[c])+'.png')
    print("Hist 1 Done.")
    canvas.Clear()

    delputrigvnpv.SetLineColor(46)
    delputrigvnpv.SetMarkerColor(46)
    delputrigvnpv.SetMarkerStyle(8)
    delputrigvnpv.SetMarkerSize(0.5)
    delputrigvnpv.SetTitle("Averaged del(PUPPI P_T, TRIG P_T) v. npv")
    delputrigvnpv.GetXaxis().SetTitle("npv")
    delputrigvnpv.GetYaxis().SetTitle("Averaged Del(PUPPI - TRIG) P_T")
    delputrigvnpv.GetXaxis().SetTitleSize(0.045)
    delputrigvnpv.GetXaxis().SetTitleOffset(0.9)
    delputrigvnpv.GetYaxis().SetTitleSize(0.045)
    delputrigvnpv.GetYaxis().SetTitleOffset(0.9)
    delputrigvnpv.Draw("PLC PMC")
    canvas.Draw()
    canvas.SaveAs('controlPlots/avgdelputrigvnpvnolinehist'+str(tt[c])+'.png')
    print("Hist 2 Done.")
    

# Save ROOT File
    """matchDatatools = ROOT.TFile("controlPlots/tools3"+str(tt[c])+".root", "RECREATE")
    matchDatatools.WriteObject(phiringetdelputrig, "phiringetdelputrig"+str(tt[c]))
    matchDatatools.WriteObject(phiringetnpv, "phiringetnpv"+str(tt[c]))
    # matchDatatools.WriteObject(phiringsubtrigetnpv, "phiringsubtrigetnpv"+str(tt[c]))
    matchDatatools.WriteObject(phiringsubtrigetputrig, "phiringsubtrigetnpv"+str(tt[c]))
    print("Histograms and ROOT file Created.")"""

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
    

