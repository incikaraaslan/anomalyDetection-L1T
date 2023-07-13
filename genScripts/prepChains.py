import ROOT
from tqdm import tqdm
import os

def prepChains(directory):
    chains = {
'anomalyChain': ROOT.TChain("L1TCaloSummaryTestNtuplizer/L1TCaloSummaryOutput"), 
'PUChain': ROOT.TChain("pileupNetworkNtuplizer/pileupTree"),
'cicadaChain': ROOT.TChain("CICADAv1ntuplizer/L1TCaloSummaryOutput"),
'newPUChain': ROOT.TChain("inciSNAILv0p1Ntuplizer/pileupTree"),
'pileupInfo': ROOT.TChain("pileupInformationNtuplizer/pileupInformation"),
'caloJet': ROOT.TChain("caloStage2JetNtuplizer/L1CaloJetInformation"),
'genJet': ROOT.TChain("genJetInformationNtuplizer/genJetInformation")}
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        for chainname in chains:
            chains[chainname].Add(f)
    return chains

