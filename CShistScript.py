import ROOT
from tqdm import tqdm
import os
import prepChains as pc

runs = ["B","C", "D"]

for i in tqdm(range(3)):
    directory = "/hdfs/store/user/aloeliger/uGTComparisons/v_2/Run"+runs[i]+"/" 
    chains = pc.prepChains(directory)
    h1run = ROOT.TH1F("Run"+runs[i]+" H2", "anomalyScore/pileupPrediction", 100, 0.0, 1.0)
    for j in tqdm(range(chains['anomalyChain'].GetEntries())):
        chains['anomalyChain'].GetEntry(j)
        chains['PUChain'].GetEntry(j)
        a = chains['anomalyChain'].anomalyScore
        b = a / chains['PUChain'].pileupPrediction
        h1run.Fill(b)
        
    hist1F = ROOT.TFile("histCS_run"+runs[i]+".root", "CREATE")
    hist1F.WriteObject(h1run, "histCS_run"+runs[i])
    print("Histogram for Run"+runs[i]+" Created.")
