import ROOT
from tqdm import tqdm
import os

def prepChains(filename):
    chains = {
'anomalyChain': ROOT.TChain("L1TCaloSummaryTestNtuplizer/L1TCaloSummaryOutput"), 
'PUChain': ROOT.TChain("pileupNetworkNtuplizer/pileupTree"),
'cicadaChain': ROOT.TChain("CICADAv1ntuplizer/L1TCaloSummaryOutput"),
'newPUChain': ROOT.TChain("inciSNAILv0p1Ntuplizer/pileupTree"),
'pileupInfo': ROOT.TChain("pileupInformationNtuplizer/pileupInformation"),
'caloJet': ROOT.TChain("caloStage2JetNtuplizer/L1CaloJetInformation"),
'genJet': ROOT.TChain("genJetInformationNtuplizer/genJetInformation"),
'recoJet': ROOT.TChain("jetCounter/objectInfo"),
'trigJet': ROOT.TChain("l1UpgradeEmuTree/L1UpgradeTree"),
'puppiJet': ROOT.TChain("puppiJetNtuplizer/PuppiJets"),
'regionEt': ROOT.TChain("L1RegionNtuplizer/L1EmuRegions")}
    # f = os.path.join(directory, filename)
    for chainname in chains:
        chains[chainname].Add(filename)
    return chains

