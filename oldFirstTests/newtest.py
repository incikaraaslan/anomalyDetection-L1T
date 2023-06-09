import ROOT
import tqdm
import os
print("ROOT version {ROOT.__version__}")

chain = ROOT.TChain("L1TCaloSummaryTestNtuplizer/L1TCaloSummaryOutput")
directory = "/hdfs/store/user/aloeliger/uGTComparisons/v_2/RunA/"

for filename in os.listdir("/hdfs/store/user/aloeliger/uGTComparisons/v_2/RunA"):
    f = os.path.join(directory, filename)
    chain.AddFile(f)
# Use `chain` as if it was a `TTree`

canvas = ROOT.TCanvas()
h1runA = ROOT.TH1F("RunA H1", "anomalyScore", 100, 0.0, 60.0)

for i in tqdm(range(chain.GetEntries())):
    # Keep in mind that the computer doesn't have the memory to store every entry in the chain so you have to load everytime.
    chain.GetEntry(i)
    a = chain.anomalyScore
    print(a)
    h1runA.Fill(a)

h1runA.Draw()
canvas.Draw()
canvas.SaveAs("h1runA.png")
