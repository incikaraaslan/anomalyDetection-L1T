import ROOT
from time import perf_counter
import os
import math
import statistics
import random
import argparse
from tqdm import tqdm
from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as plt
import h5py
import tensorflow as tf 
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

    def findMatchedJetEnergyDifferences(self):
        etDeltas = []
        for triggerJet, puppiJet in self.matchedJets:
            etDeltas.append(puppiJet.lorentzVector.Et()-(triggerJet.lorentzVector.Et())) #  + self.correctionpred()
        return etDeltas
    
    """def correctionpred(self):
        model = tf.keras.models.load_model('simplethesis_NN')
        x = np.column_stack((self.totalTP, self.totalTPEnergy))
        y = np.asarray(model.predict(x)).astype(float)
        return y[0][0]"""


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
hdf5_file_name = 'NN_orig.h5'
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

# Match PUPPI and TRIG jets --> Draw Histogram vs. # HCAL+ECAL tps --> LinReg get fit + get x, y values 
# --> get the offset of these two --> create dataset or lookup table with bins vs. offset
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
    for fileName in track(allFiles, description="Adding files..."):
        eventChain.Add(fileName)
        puppiJetChain.Add(fileName)
        triggerJetChain.Add(fileName)
        regionChain.Add(fileName)
        towerChain.Add(fileName)
    eventChain.AddFriend(puppiJetChain)
    eventChain.AddFriend(triggerJetChain)
    eventChain.AddFriend(regionChain)
    eventChain.AddFriend(towerChain)

    # df = ROOT.RDataFrame(eventChain)

    # console.print(f'Available columns: \n{df.GetColumnNames()}')
    

    numEvents = eventChain.GetEntries()
    if args.maxEvents is not None:
        numEvents = min(numEvents, args.maxEvents)
    console.print(f'Processing {numEvents} events...', style='underline')

    #histogram counting number of jets per nECAL/nHCAL TPs
    nBins = 100
    minTPs = 0.0
    maxTPs = 2000.0

    minTPEnergy = 0.0
    maxTPEnergy = 4000.0

    nMatchedPairsHist = ROOT.TH1D(
        "nMatchedPairsHist",
        "nMatchedPairsHist",
        nBins,
        minTPs,
        maxTPs
    )
    #histogram weighted by the energy delta
    energyDeltasHist = ROOT.TH1D(
        "energyDeltasHist",
        "energyDeltasHist",
        nBins,
        minTPs,
        maxTPs
    )

    nMatchedPairs_TPET_Hist = ROOT.TH1D(
        "nMatchedPairs_TPET_Hist",
        "nMatchedPairs_TPET_Hist",
        nBins,
        minTPEnergy,
        maxTPEnergy,
    )
    energyDeltas_TPET_Hist = ROOT.TH1D(
        "energyDeltas_TPET_Hist",
        "energyDeltas_TPET_Hist",
        nBins,
        minTPEnergy,
        maxTPEnergy,
    )

    for i in track(range(1000), description="Scrolling events"): #numEvents
    #for i in track(range(100), description="scrolling events"):
        # Grab the event
        eventChain.GetEntry(i)

        event = eventData(eventChain)

        if event.matchedJets == []: #if we have no matched jets, we're done here
            continue

        #let's figure out how many matched jets we have and the number of TPs
        nMatchedJets = len(event.matchedJets)
        totalTPs = event.totalTP
        totalTPEnergy = event.totalTPEnergy

        #fill the histogram with the number of jets we got for this number of TPs
        nMatchedPairsHist.Fill(totalTPs, nMatchedJets)

        #let's find the differences between matched jets in the event data
        energyDeltas = event.findMatchedJetEnergyDifferences()
        #let's find the total energy delta
        energyDelta = sum(energyDeltas)
        
        #now let's fill the histogram
        energyDeltasHist.Fill(totalTPs, energyDelta)

        nMatchedPairs_TPET_Hist.Fill(totalTPEnergy, nMatchedJets)
        energyDeltas_TPET_Hist.Fill(totalTPEnergy, energyDelta)
    
    #then to get average, you divide the bins of the energy deltas hist
    #by the bin contents of the number of matched jets hists
    averageJetEnergyDelta = makeAverageHistograms(energyDeltasHist, nMatchedPairsHist, "AverageJetEnergyDelta")
    averageJetEnergyDelta_TPET = makeAverageHistograms(energyDeltas_TPET_Hist, nMatchedPairs_TPET_Hist, "AverageJetEnergyDelta_TPET")
    # loop over bins get the bin error, gen bin error of eD/ get bin content of nMatched
    # ind errs on eD histogram, store it as a hdf5 dataset
    y = []
    y2 = []
    x = []
    x2 = []
    yerr = []
    y2err = []
    for bin_num in range(1, nBins + 1):
        bin_center = averageJetEnergyDelta.GetBinCenter(bin_num)
        bin_content = averageJetEnergyDelta.GetBinContent(bin_num)
        bin_centeret = averageJetEnergyDelta_TPET.GetBinCenter(bin_num)
        bin_contentet = averageJetEnergyDelta_TPET.GetBinContent(bin_num)
        if nMatchedPairsHist.GetBinContent(bin_num) != 0:
            binerror = energyDeltasHist.GetBinError(bin_num) / nMatchedPairsHist.GetBinContent(bin_num)
        else:
            binerror = 0
        if nMatchedPairs_TPET_Hist.GetBinContent(bin_num) != 0:
            binerror2 = energyDeltas_TPET_Hist.GetBinError(bin_num) / nMatchedPairs_TPET_Hist.GetBinContent(bin_num)
        else:
            binerror2 = 0
        
        yerr.append(binerror)
        y2err.append(binerror2)
        x.append(bin_center)
        x2.append(bin_centeret)
        y.append(bin_content)
        y2.append(bin_contentet)
    
    # Model Variables
    x = np.asarray(x).reshape(-1, 1)
    x2 = np.asarray(x).reshape(-1, 1)
    y = np.asarray(y)
    y2 = np.asarray(y2)


    # Write File
    hdf5_file.create_dataset('TPno', data=np.asarray(x))
    hdf5_file.create_dataset('TPet', data=np.asarray(x2))
    hdf5_file.create_dataset('AvgDelOffsettp', data=np.asarray(y))
    hdf5_file.create_dataset('AvgDelOffsettpet', data=np.asarray(y2))
    hdf5_file.create_dataset('AvgDelOffsettperr', data=np.asarray(yerr))
    hdf5_file.create_dataset('AvgDelOffsettpeterr', data=np.asarray(y2err))
    hdf5_file.close()

    # Plot
    """plt.scatter(x2, y2, color='blue', label='Original Data')
    plt.plot(x2, y_pred2, color='red', label='Linear Fit')
    plt.xlabel('HCAL + ECAL TPET')
    plt.ylabel(f'Average $\Delta(PUPPI P_T, TRIG P_T)$')
    plt.title('Linear Regression Fit')
    plt.legend()
    plt.savefig('linear_regression_plot.png')
    plt.show()"""
    

        
    # print(x,y)


    """makeDebugTable(averageJetEnergyDelta, minTPs, maxTPs, nBins, "nTPs")

    makeDebugTable(averageJetEnergyDelta_TPET, minTPEnergy, maxTPEnergy, nBins, "Total TP Energy")        

    outputFile = ROOT.TFile(args.outputFileName, "RECREATE")
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