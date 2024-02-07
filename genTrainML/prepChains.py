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
'regionEt': ROOT.TChain("L1RegionNtuplizer/L1EmuRegions"),
'PUChainPUPPI': ROOT.TChain("PUVertexNtuplizer/PUVertexNtuple"),
'caloTower': ROOT.TChain("l1CaloTowerTree/L1CaloTowerTree")}
    # f = os.path.join(directory, filename)
    for chainname in chains:
        chains[chainname].Add(filename)
    return chains

"""tt = ["trainshuf", "testshuf"]
f = open('output/'+tt[0]+'.txt', 'r')
score = 0
score2 = 0
for x in tqdm(f):
    x = x[:-1]
    chains = prepChains(x)
    if x[:-1] == "\n":
        x = x[:-1]
        chains = prepChains(x)
    else:
        chains = prepChains(x)
    score += chains['puppiJet'].GetEntries()
    score2 += chains['trigJet'].GetEntries()

print(score2)
print(score)"""