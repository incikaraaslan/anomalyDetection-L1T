import ROOT
from tqdm import tqdm
import os

def prepChains(directory):
    chains = {
'anomalyChain': ROOT.TChain("L1TCaloSummaryTestNtuplizer/L1TCaloSummaryOutput"), 
'PUChain': ROOT.TChain("pileupNetworkNtuplizer/pileupTree")}
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        for chainname in chains:
            chains[chainname].Add(f)
    return chains

