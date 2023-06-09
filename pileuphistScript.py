import ROOT
from tqdm import tqdm
import os
import prepChains as pc

run = input("Which Run?")
directory = "/hdfs/store/user/aloeliger/uGTComparisons/v_2/Run"+run+"/" 
chains = pc.prepChains(directory)

h1run = ROOT.TH1F("Run"+run+" H1", "anomalyScore", 100, 0.0, 10.0)
h2run = ROOT.TH1F("Run"+run+" H2", "anomalyScore/pileupPrediction", 100, 0.0, 1.0)
h3run = ROOT.TH1F("Run"+run+" H3", "anomalyScore/pileupPrediction^2", 100, 0.0, 1.0)

for i in tqdm(range(chains['anomalyChain'].GetEntries())):
    chains['anomalyChain'].GetEntry(i)
    chains['PUChain'].GetEntry(i)
    a = chains['anomalyChain'].anomalyScore
    b = a / chains['PUChain'].pileupPrediction
    c = a / (chains['PUChain'].pileupPrediction)**2
    h1run.Fill(a)
    h2run.Fill(b)
    h3run.Fill(c)
    

hist1F = ROOT.TFile("histCICADA_run"+run+".root", "CREATE")
hist2F = ROOT.TFile("histCS_run"+run+".root", "CREATE")
hist3F = ROOT.TFile("histCS2_run"+run+".root", "CREATE")
hist1F.WriteObject(h1run, "histCICADA_run"+run)
print("Histogram 1 Created.") 
hist2F.WriteObject(h2run, "histCS_run"+run)
print("Histogram 2 Created.")  
hist3F.WriteObject(h3run, "histCS2_run"+run) 
print("Histogram 3 Created.") 
