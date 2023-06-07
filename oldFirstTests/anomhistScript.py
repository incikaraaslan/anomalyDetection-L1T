import ROOT
from tqdm import tqdm
import os

chain = ROOT.TChain("L1TCaloSummaryTestNtuplizer/L1TCaloSummaryOutput")
directory = "/hdfs/store/user/aloeliger/uGTComparisons/v_2/RunB/" 
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    chain.AddFile(f)

hrun = ROOT.TH1F("RunB H1", "anomalyScore", 100, 0.0, 10.0)
for i in tqdm(range(chain.GetEntries())):                                            
    chain.GetEntry(i) 
    a = chain.anomalyScore 
    hrun.Fill(a)

histFile = ROOT.TFile("hist_runB.root", "CREATE")
histFile.WriteObject(hrun, "hist_runB")
print("Histogram Created.")
