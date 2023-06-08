import ROOT
from tqdm import tqdm
import os
import prepChains as pc

runs = ["B","C", "D"]

for i in tqdm(range(3)):
    directory = "/hdfs/store/user/aloeliger/uGTComparisons/v_2/Run"+runs[i]+"/" 
    chains = pc.prepChains(directory)
    h1run = ROOT.TH1F("Run"+runs[i]+" H3", "anomalyScore/pileupPrediction^2", 100, 0.0, 1.0)
    for j in tqdm(range(chains['anomalyChain'].GetEntries())):
        chains['anomalyChain'].GetEntry(j)
        chains['PUChain'].GetEntry(j)
        a = chains['anomalyChain'].anomalyScore
        b = a / chains['PUChain'].pileupPrediction
        c = a / (chains['PUChain'].pileupPrediction)**2
        h1run.Fill(c)
        
    hist1F = ROOT.TFile("histCS2_run"+runs[i]+".root", "CREATE")
    hist1F.WriteObject(h1run, "histCS2_run"+runs[i])
    print("Histogram for Run"+runs[i]+" Created.")
