# Make an improved NTuple format for SNAIL
import ROOT
from time import perf_counter
import numpy as np
import awkward as ak
import os
import math
import statistics
import random
import argparse
import h5py
from rich.console import Console
from rich.progress import track
from rich.traceback import install
from rich.table import Table
install(show_locals=True)

from iEtaiPhiBinning import iEtaiPhiBinCollection

console = Console()
iEtaiPhiMap = iEtaiPhiBinCollection()

class jet():
    def __init__(self, pt, eta, phi, m):
        self.pt = pt
        self.eta = eta
        self.phi = phi
        self.m = m
        self.lorentzVector = ROOT.TLorentzVector()
        self.lorentzVector.SetPtEtaPhiM(self.pt, self.eta, self.phi, self.m)
    
        self.iEta, self.iPhi = iEtaiPhiMap.iEtaiPhi(self.eta, self.phi)

    # def DeltaR(self, otherJet) -> float:
    #     return self.lorentzVector.DeltaR(otherJet.lorentzVector)
    def DeltaR(self, otherJet):
        deltaPhi = self.phi - otherJet.phi
        while deltaPhi < -1.0*math.pi:
            deltaPhi += math.pi
        while deltaPhi > math.pi:
            deltaPhi -= math.pi
        deltaEta = self.eta - otherJet.eta
        deltaR = math.sqrt(deltaPhi**2 + deltaEta**2)
        return deltaR

class puppiJet(jet):
    def __init__(self, theChain: ROOT.TChain, entryNum: int):
        super().__init__(
            theChain.ptVector[entryNum],
            theChain.etaVector[entryNum],
            theChain.phiVector[entryNum],
            theChain.massVector[entryNum],
        )

class triggerJet(jet):
    def __init__(self, theChain: ROOT.TChain, entryNum: int):
        super().__init__(
            theChain.L1Upgrade.jetEt[entryNum],
            theChain.L1Upgrade.jetEta[entryNum],
            theChain.L1Upgrade.jetPhi[entryNum],
            0.0
        )
        self.rawEt = theChain.L1Upgrade.jetRawEt[entryNum]
        self.puEt = theChain.L1Upgrade.jetPUEt[entryNum]
        self.seedEt = theChain.L1Upgrade.jetSeedEt[entryNum]
        self.BX = theChain.L1Upgrade.jetBx[entryNum]
        self.HWQuality = theChain.L1Upgrade.jetHwQual[entryNum]

class noPUTriggerJet(triggerJet):
    def __init__(self, theChain: ROOT.TChain, entryNum: int):
        super().__init__(theChain, entryNum)
        self.lorentzVector.SetPtEtaPhiM(
            self.rawEt * 0.5,
            self.eta,
            self.phi,
            0.0
        )
        

class eventData():
    def __init__(self, theChain: ROOT.TChain):
        self.chain = theChain
        self.matchedJets, self.unmatchedTriggerJets, self.unmatchedPuppiJets = createMatchedAndUnmatchedJets(*createTriggerAndPuppiJets(self.chain))
        self.nECALTP = self.chain.CaloTP.nECALTP
        self.nHCALTP = self.chain.CaloTP.nHCALTP
        self.totalTP = self.nECALTP + self.nHCALTP
        self.totalTPEnergy = 0.0
        self.totalTPEnergy += sum(self.chain.CaloTP.ecalTPet)
        self.totalTPEnergy += sum(self.chain.CaloTP.hcalTPet)
        
        for phi in range(18):
            for eta in range(14):
                if self.chain.regionEt[eta + phi * 14] != 0:
                    self.nCICADAregions += 1
                    self.totalCICADAet += self.chain.regionEt[eta + phi * 14]

        
        # self.nCICADAregions += self.chain.modelInput
        #for i in range(self.nECALTP):
        #    self.totalTPEnergy += self.chain.CaloTP.ecalTPet[i]
        #for i in range(self.nHCALTP):
        #    self.totalTPEnergy += self.chain.CaloTP.hcalTPet[i]

    def findMatchedJetEnergyDifferences(self):
        etDeltas = []
        for triggerJet, puppiJet in self.matchedJets:
            etDeltas.append(puppiJet.lorentzVector.Et()-triggerJet.lorentzVector.Et())
        return etDeltas

def createTriggerAndPuppiJets(theChain):
    triggerJets = []
    puppiJets = []

    for entryNum in range(theChain.nObjects):
        puppiJets.append(puppiJet(theChain, entryNum))
    for entryNum in range(theChain.L1Upgrade.nJets):
        triggerJets.append(noPUTriggerJet(theChain, entryNum))
    
    return triggerJets, puppiJets

# basic idea here, pick a puppi jet
# find all trigger jets within 0.4 of it
# If there are none, this puppi jet is unmatched.
# Select this highest pt trigger jet
# these two are now matched, remove them from their lists
# Then we move on to the next
# At the end of this we hand back matched pairs, and unmatched jets

# Write on a File

hdf5_file_name = 'delputrvtotalntotalet_dataset.h5'
hdf5_file = h5py.File("output/"+ hdf5_file_name, 'w')

def createMatchedAndUnmatchedJets(triggerJets, puppiJets):
    unmatchedPuppiJets = []
    unmatchedTriggerJets = triggerJets
    matchedJets = []
    for puppiJetIndex, puppiJet in enumerate(puppiJets):
        distances = []
        for triggerJetIndex, triggerJet in enumerate(unmatchedTriggerJets):
            distances.append((triggerJetIndex, puppiJet.DeltaR(triggerJet)))
        distances.sort(key=lambda x: x[1])
        # Sort the distances, and remove any trigger jets that don't meet our criteria.
        for i in range(len(distances)):
            if distances[i][1] > 0.4:
                distances = distances[:i]
                break
        # if we have no appropriate trigger jets at this point, this is an unmatched puppi jet
        if len(distances) == 0:
            unmatchedPuppiJets.append(puppiJet)
            continue
        # Now we go through and check trigger jet pts
        # We will accept the highest one.
        highestPt = 0.0
        highestIndex = None
        for triggerJetIndex, DeltaR in distances:
            if unmatchedTriggerJets[triggerJetIndex].pt > highestPt:
                highestIndex = triggerJetIndex
        triggerJet = unmatchedTriggerJets.pop(highestIndex)
        matchedJets.append((triggerJet, puppiJet))
    return matchedJets, unmatchedTriggerJets, unmatchedPuppiJets

def makeAverageHistograms(energyDeltaHist, nMatchedPairsHist, nameTitle):
    averageHist = energyDeltaHist.Clone()
    averageHist.Divide(nMatchedPairsHist)

    averageHist.SetName(nameTitle)
    averageHist.SetName(nameTitle)

    return averageHist

def makeDebugTable(averagePlot, minX, maxX, nBins, columnName):
    outputTable = Table(title="Average(Puppi ET - Trigger ET)")
    outputTable.add_column(columnName, justify="center")
    outputTable.add_column("Energy Delta", justify="center")

    for i in range (1, averagePlot.GetNbinsX()+1):
        rangeLow = int((i-1)*(maxX-minX)/nBins)
        rangeHigh = int(i*(maxX-minX)/nBins)
        energyDelta = averagePlot.GetBinContent(i)
        outputTable.add_row(f"{rangeLow}-{rangeHigh}", f'{energyDelta}')

    console.print(outputTable)

def cut_data_into_bins(data, num_bins, bin_range):
    # Define the bin edges based on the user-defined range and number of bins
    bin_edges = np.linspace(bin_range[0], bin_range[1], num_bins + 1)

    # Use numpy's digitize function to assign each data point to a bin
    bin_indices = np.digitize(data, bin_edges, right=True)
    
    # Create a dictionary to store the data points in each bin
    bins = {}
    for i in range(1, num_bins + 1):
        bins[i] = data[bin_indices == i]
    
    return bins

def main(args):
    filePaths = [
        "/hdfs/store/user/aloelige/EphemeralZeroBias0/SNAIL_2023RunD_EZB0_18Oct2023/231018_205626/",
        # "/hdfs/store/user/aloelige/EphemeralZeroBias2/SNAIL_2023RunD_EZB2_18Oct2023/231018_205829/",
        "/hdfs/store/user/aloelige/EphemeralZeroBias2/SNAIL_2023RunD_EZB2_19Oct2023/231019_080917/",
        "/hdfs/store/user/aloelige/EphemeralZeroBias3/SNAIL_2023RunD_EZB3_18Oct2023/231018_205910/",
        "/hdfs/store/user/aloelige/EphemeralZeroBias4/SNAIL_2023RunD_EZB4_18Oct2023/231018_205953/",
        "/hdfs/store/user/aloelige/EphemeralZeroBias5/SNAIL_2023RunD_EZB5_18Oct2023/231018_210031/",
        "/hdfs/store/user/aloelige/EphemeralZeroBias6/SNAIL_2023RunD_EZB6_18Oct2023/231018_210109/",
        "/hdfs/store/user/aloelige/EphemeralZeroBias7/SNAIL_2023RunD_EZB7_19Oct2023/231019_080954/",
    ]
    
    allFiles = []
    for path in filePaths:
        console.print(f'Path: {path}')
        for dirpath, _ , fileNames in os.walk(path):
            for fileName in fileNames:
                allFiles.append(dirpath+'/'+fileName)
    console.print(f'Total number of files: {len(allFiles)}')

    eventChain = ROOT.TChain('l1EventTree/L1EventTree')
    puppiJetChain = ROOT.TChain('puppiJetNtuplizer/PuppiJets')
    triggerJetChain = ROOT.TChain('l1UpgradeEmuTree/L1UpgradeTree')
    regionChain = ROOT.TChain('L1RegionNtuplizer/L1EmuRegions')
    towerChain = ROOT.TChain('l1CaloTowerTree/L1CaloTowerTree')
    cicadaChain = ROOT.TChain('CICADAv1ntuplizer/L1TCaloSummaryOutput')


    for fileName in track(allFiles, description="Adding files..."):
        eventChain.Add(fileName)
        puppiJetChain.Add(fileName)
        triggerJetChain.Add(fileName)
        regionChain.Add(fileName)
        towerChain.Add(fileName)
        # cicadaChain.Add(fileName)
    eventChain.AddFriend(puppiJetChain)
    eventChain.AddFriend(triggerJetChain)
    eventChain.AddFriend(regionChain)
    eventChain.AddFriend(towerChain)
    # eventChain.AddFriend(cicadaChain)

    # df = ROOT.RDataFrame(eventChain)

    # console.print(f'Available columns: \n{df.GetColumnNames()}')

    numEvents = eventChain.GetEntries()
    if args.maxEvents is not None:
        numEvents = min(numEvents, args.maxEvents)
    console.print(f'Processing {numEvents} events...', style='underline')

    #histogram counting number of jets per nECAL/nHCAL TPs
    nBins = 10
    TPs_range = (0.0, 2000.0)

    minTPEnergy = 0.0
    maxTPEnergy = 4000.0

    eD = []
    nM = []
    tTP= []
    tTPET = []
    tnCICADA = []
    tCICADAet = []

    for i in track(range(1), description="Scrolling events"): #numEvents
        # Grab the event
        eventChain.GetEntry(i)

        event = eventData(eventChain)
        
        if event.matchedJets == []: #if we have no matched jets, we're done here
            continue

        # How many matched jets we have
        nMatchedJets = len(event.matchedJets)
        nM.append(nMatchedJets)

        # The number of TPs
        totalTPs = event.totalTP
        tTP.append(totalTPs)

        # TP E_Ts
        totalTPEnergy = event.totalTPEnergy
        tTPET.append(totalTPEnergy)

        # Del(PUPPI,TRIG)
        energyDeltas = event.findMatchedJetEnergyDifferences()
        energyDelta = sum(energyDeltas)
        eD.append(energyDelta)

        # nCICADAentries
        nCICADA = event.nCICADAregions
        tnCICADA.append(nCICADA)

        # CICADA ET
        CICADAets = event.totalCICADAet
        tCICADAet.append(CICADAets)


    eD = np.asarray(eD)
    nM = np.asarray(nM)
    tTP = np.asarray(tTP)
    tTPET = np.asarray(tTPET)
    tnCICADA = np.asarray(tnCICADA)
    tCICADAet = np.asarray(tCICADAet)

    #Avg(Del(PUPPI, TRIG)) = y:
    y = eD/nM
    x1 = tTP
    x2 = tTPET
    x3 = tnCICADA
    x4 = tCICADAet
    
    # Write File
    hdf5_file.create_dataset('totalTPno', data=np.asarray(x1))
    hdf5_file.create_dataset('totalTPET', data=np.asarray(x2))
    hdf5_file.create_dataset('totalCICADAno', data=np.asarray(x3))
    hdf5_file.create_dataset('totalCICADAET', data=np.asarray(x4))
    hdf5_file.create_dataset('avgpuppitrigEt', data=np.asarray(y))

    hdf5_file.close()
    
    print("File Created.")

    """delputrigbin = cut_data_into_bins(eD, nBins, TPs_range)
    nMatchedbin = cut_data_into_bins(nM, nBins, TPs_range)
    # Perform bin-by-bin division
    avgdelputrig = {}
    for i in range(1, nBins + 1):
        avgdelputrig[i] = np.divide(delputrigbin[i], nMatchedbin[i], out=np.zeros_like(delputrigbin[i]), where=nMatchedbin[i] != 0).astype(float)
        
    # Print the resulting bins after division
    for bin_num, bin_data in avgdelputrig.items():
        print(f'Bin {bin_num}: {bin_data}')"""


    """makeDebugTable(averageJetEnergyDelta, minTPs, maxTPs, nBins, "nTPs")

    makeDebugTable(averageJetEnergyDelta_TPET, minTPEnergy, maxTPEnergy, nBins, "Total TP Energy") """       

    """outputFile = ROOT.TFile(args.outputFileName, "RECREATE")
    nMatchedPairsHist.Write()
    energyDeltasHist.Write()
    averageJetEnergyDelta.Write()
    
    nMatchedPairs_TPET_Hist.Write()
    energyDeltas_TPET_Hist.Write()
    averageJetEnergyDelta_TPET.Write()"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Make Jet Delta vs nTPs")

    parser.add_argument(
        "--maxEvents",
        "-m",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--outputFileName",
        "-o",
        default="./averageJetEnergyFile.root",
    )

    args=parser.parse_args()

    main(args)
