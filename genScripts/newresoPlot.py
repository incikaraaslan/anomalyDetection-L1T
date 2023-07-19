import ROOT
from tqdm import tqdm
import os
import prepChains as pc
import numpy as np
import math

ROOT.gStyle.SetOptStat(0)

m_dir = "/hdfs/store/user/aloelige/TT_TuneCP5_13p6TeV_powheg-pythia8/CICADA_2022_TT_07Jul2023/"
# "/hdfs/store/user/aloelige/ZeroBias/CICADA_2018Run"+run+"_ZB_07Jul2023"
# "/hdfs/store/user/aloelige/ZeroBias/CICADA_Ztoee_wMINIAOD_RAW_Run"+run+"_08Jun2023/"

# There's probably a better way to do this ngl - Run Differentiation
add = [f.path for f in os.scandir(m_dir) if f.is_dir()]
run_list = [a.path for a in os.scandir(add[0]) if a.is_dir()]

# Prepping Chains
for i in range(len(run_list)):
    chains = pc.prepChains(run_list[i])

# Draw the Histogram
h = ROOT.TH1F("gencaloResPlot", "Resolution Plot", 100, 0.0, 100.0)

# Lists
caloJetptarr = []
genJetptarr = []
cg_matched = []
cg_unmatched = []

# Lorentz Vector Matching
for i in tqdm(range(chains['genJet'].GetEntries())):
    chains['genJet'].GetEntry(i)
    chains['caloJet'].GetEntry(i)
    # Each p_t, eta, phi, transverse mass entry has multiple jets in the form of vector<double>.
    for j in range(chains['genJet'].genJetEta.size()):
        genJet = ROOT.TLorentzVector()
        genJet.SetPtEtaPhiM(chains['genJet'].genJetPt[j], chains['genJet'].genJetEta[j], chains['genJet'].genJetPhi[j], chains['genJet'].genJetMass[j])
        genJetptarr.append(genJet)
    for j in range(chains['caloJet'].etaVector.size()):
        caloJet = ROOT.TLorentzVector()
        caloJet.SetPtEtaPhiM(chains['caloJet'].ptVector[j], chains['caloJet'].etaVector[j], chains['caloJet'].phiVector[j], chains['caloJet'].massVector[j])
        caloJetptarr.append(caloJet)

# Matching vectors via deltaR < 0.3   
while tqdm(genJetptarr):
    for i in range(len(genJetptarr)):
        for j in range(len(caloJetptarr)):
            mincalojet = None
            delR = None
            if delR == None:
                delR = ROOT.Math.VectorUtil.DeltaR(genJetptarr[i], caloJetptarr[j])
            elif (delR <= 0.3) & (ROOT.Math.VectorUtil.DeltaR(genJetptarr[i], caloJetptarr[j]) < delR):
                delR = ROOT.Math.VectorUtil.DeltaR(genJetptarr[i], caloJetptarr[j])
                mincalojet = caloJetptarr[j]
        
        # Place into matched and unmatched
        if mincalojet != None:
            cg_matched.append((genJetptarr.pop(i), caloJetptarr.pop(j)))
        elif mincalojet == None:
            cg_unmatched.append(genJetptarr.pop(i))
        
print("Matched Arr: " + str(cg_matched))
print("Unmatched Arr: " + str(cg_unmatched))

# Draw the Histogram
for i in cg_matched:
    reso = (i[1].Pt - i[0].Pt)/(i[0].Pt)
    h.Fill(reso)

resoh = ROOT.TFile("gencaloResPlot.root", "CREATE")
resoh.WriteObject(h, "gencaloResPlot")
print("Histogram Created.")



            
            

