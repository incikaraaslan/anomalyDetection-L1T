import ROOT
from tqdm import tqdm
import os
import prepChains as pc

run = input("Which Run?")
m_dir = /hdfs/store/user/aloelige/TT_TuneCP5_13p6TeV_powheg-pythia8/CICADA_2022_TT_07Jul2023/
# "/hdfs/store/user/aloelige/ZeroBias/CICADA_2018Run"+run+"_ZB_07Jul2023"
#"/hdfs/store/user/aloelige/ZeroBias/CICADA_Ztoee_wMINIAOD_RAW_Run"+run+"_08Jun2023/"

# There's probably a better way to do this ngl - Run Differentiation
add = [f.path for f in os.scandir(m_dir) if f.is_dir()]
run_list = [a.path for a in os.scandir(add[0]) if a.is_dir()]

# Prepping Chains
for i in range(len(run_list)):
    chains = pc.prepChains(run_list[i])


"""directory = "/hdfs/store/user/aloeliger/uGTComparisons/v_2/Run"+run+"/" 
chains = pc.prepChains(directory)"""

h1run = ROOT.TH1F("Run"+run+" H1", "anomalyScore", 100, 0.0, 10.0)
h2run = ROOT.TH1F("Run"+run+" H2", "anomalyScore/pileupPrediction", 100, 0.0, 1.0)
h3run = ROOT.TH1F("Run"+run+" H3", "anomalyScore/pileupPrediction^2", 100, 0.0, 1.0)

for i in tqdm(range(chains['cicadaChain'].GetEntries())): #chains['anomalyChain'].GetEntries())
    """chains['anomalyChain'].GetEntry(i)
    chains['PUChain'].GetEntry(i)"""
    chains['cicadaChain'].GetEntry(i)
    chains['newPUChain'].GetEntry(i)
    a = chains['cicadaChain'].anomalyScore
    d = chains['newPUChain'].pileupPrediction
    if d != 0:
        b = a / d
        c = a / (d)**2
    else:
        b = a
        c = a
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
