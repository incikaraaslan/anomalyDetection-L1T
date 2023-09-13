import ROOT
from tqdm import tqdm
import os
import prepChains as pc
import numpy as np
import math
from time import perf_counter

ROOT.gStyle.SetOptStat(0)

run = input("Log in the Run A, C, D:")
m_dir = "/hdfs/store/user/aloelige/ZeroBias/CICADA_2018Run"+run+"_ZB_07Jul2023"
# "/hdfs/store/user/aloelige/TT_TuneCP5_13p6TeV_powheg-pythia8/CICADA_2022_TT_07Jul2023/"
# "/hdfs/store/user/aloelige/ZeroBias/CICADA_2018Run"+run+"_ZB_07Jul2023"
# "/hdfs/store/user/aloelige/ZeroBias/CICADA_Ztoee_wMINIAOD_RAW_Run"+run+"_08Jun2023/"

# There's probably a better way to do this ngl - Run Differentiation
add = [f.path for f in os.scandir(m_dir) if f.is_dir()]
run_list = [a.path for a in os.scandir(add[0]) if a.is_dir()]

# Prepping Chains
for i in range(len(run_list)):
    chains = pc.prepChains(run_list[i])

# Creating the Histograms
canvas = ROOT.TCanvas()
hp = ROOT.TH1F("recocaloResPlot", "Resolution Plot", 100, -1.0, 1.0)
hpp = ROOT.TH1F("precocaloResPlot", "Resolution Plot", 100, -1.0, 1.0)
hp010 = ROOT.TH1F("recocaloResPlot 0-10", "Resolution Plot 0-10", 100, -1.0, 1.0)
hp1020 = ROOT.TH1F("recocaloResPlot 10-20", "Resolution Plot 10-20", 100, -1.0, 1.0)
hp2030 = ROOT.TH1F("recocaloResPlot 20-30", "Resolution Plot 20-30", 100, -1.0, 1.0)
hp3040 = ROOT.TH1F("recocaloResPlot 30-40", "Resolution Plot 30-40", 100, -1.0, 1.0)
hp4050 = ROOT.TH1F("recocaloResPlot 40-50", "Resolution Plot 40-50", 100, -1.0, 1.0)
hp5060 = ROOT.TH1F("recocaloResPlot 50-60", "Resolution Plot 50-60", 100, -1.0, 1.0)
hp6070 = ROOT.TH1F("recocaloResPlot 60-70", "Resolution Plot 60-70", 100, -1.0, 1.0)
hp7080 = ROOT.TH1F("recocaloResPlot 70-80", "Resolution Plot 70-80", 100, -1.0, 1.0)
hpp010 = ROOT.TH1F("precocaloResPlot 0-10", "Resolution Plot 0-10", 100, -1.0, 1.0)
hpp1020 = ROOT.TH1F("precocaloResPlot 10-20", "Resolution Plot 10-20", 100, -1.0, 1.0)
hpp2030 = ROOT.TH1F("precocaloResPlot 20-30", "Resolution Plot 20-30", 100, -1.0, 1.0)
hpp3040 = ROOT.TH1F("precocaloResPlot 30-40", "Resolution Plot 30-40", 100, -1.0, 1.0)
hpp4050 = ROOT.TH1F("precocaloResPlot 40-50", "Resolution Plot 40-50", 100, -1.0, 1.0)
hpp5060 = ROOT.TH1F("precocaloResPlot 50-60", "Resolution Plot 50-60", 100, -1.0, 1.0)
hpp6070 = ROOT.TH1F("precocaloResPlot 60-70", "Resolution Plot 60-70", 100, -1.0, 1.0)
hpp7080 = ROOT.TH1F("precocaloResPlot 70-80", "Resolution Plot 70-80", 100, -1.0, 1.0)

# Lists
cg_matched = []
cg_unmatched = []
truePileuparr = []
predPileuparr = []

# Lorentz Vector Matching
for i in tqdm(range(100000)): # chains['genJet'].GetEntries() - 100000 events if you can
    caloJetptarr = []
    recoJetptarr = []
    chains['recoJet'].GetEntry(i)
    chains['caloJet'].GetEntry(i)
    chains['pileupInfo'].GetEntry(i)
    chains['newPUChain'].GetEntry(i)
    predictedPileup = math.floor(chains['newPUChain'].pileupPrediction)
    truePileup = chains['pileupInfo'].npv
    
    # Each p_t, eta, phi, transverse mass entry has multiple jets in the form of vector<double>.
    for j in range(chains['recoJet'].etaVector.size()):
        recoJet = ROOT.TLorentzVector()
        # genJet.SetPtEtaPhiM(chains['genJet'].genJetPt[j], chains['genJet'].genJetEta[j], chains['genJet'].genJetPhi[j], chains['genJet'].genJetMass[j])
        recoJet.SetPtEtaPhiM(chains['recoJet'].ptVector[j], chains['recoJet'].etaVector[j], chains['recoJet'].phiVector[j], chains['recoJet'].massVector[j])
        recoJetptarr.append(recoJet)
    for j in range(chains['caloJet'].etaVector.size()):
        caloJet = ROOT.TLorentzVector()
        caloJet.SetPtEtaPhiM(chains['caloJet'].ptVector[j], chains['caloJet'].etaVector[j], chains['caloJet'].phiVector[j], chains['caloJet'].massVector[j])
        caloJetptarr.append(caloJet)

    # Matching vectors via deltaR < 0.3
    j = 0

    while tqdm(len(recoJetptarr) != 0, leave=False):
        minindex = None
        delR = None

        """t3_start = perf_counter()"""
        """start1 = datetime.now()"""
        for k in range(len(caloJetptarr)):
            current_delR = ROOT.Math.VectorUtil.DeltaR(recoJetptarr[j], caloJetptarr[k])
            if current_delR > 0.3:
                continue
             
            if delR == None:
                delR = current_delR
                minindex = k
            
            else:
                if current_delR < delR:
                    delR = current_delR
                    minindex = k
                else:
                    continue 

        # Place into matched and unmatched
        if minindex:
            cg_matched.append((recoJetptarr.pop(0), caloJetptarr.pop(minindex)))
            truePileuparr.append(truePileup)
            predPileuparr.append(predictedPileup)
        else:
            cg_unmatched.append(recoJetptarr.pop(0))
        
        # Just in Case :)
        if not caloJetptarr:
            if recoJetptarr:
                cg_unmatched.append(recoJetptarr.pop(0))

        

# Draw the Histogram
c = 0
for i in cg_matched:
    reso = (i[1].Pt() - i[0].Pt())/(i[0].Pt())
    tPileup = truePileuparr[c]
    predPileup = predPileuparr[c]
    c += 1
    if tPileup in range(0,10):
        hp010.Fill(reso)
    elif tPileup in range(10,20):
        hp1020.Fill(reso)
    elif tPileup in range(20,30):
        hp2030.Fill(reso)
    elif tPileup in range(30,40):
        hp3040.Fill(reso)
    elif tPileup in range(40,50):
        hp4050.Fill(reso)
    elif tPileup in range(50,60):
        hp5060.Fill(reso)
    elif tPileup in range(60,70):
        hp6070.Fill(reso)
    elif tPileup in range(70,80):
        hp7080.Fill(reso)
    else:
        pass

    if predPileup in range(0,10):
        hpp010.Fill(reso)
    elif predPileup in range(10,20):
        hpp1020.Fill(reso)
    elif predPileup in range(20,30):
        hpp2030.Fill(reso)
    elif predPileup in range(30,40):
        hpp3040.Fill(reso)
    elif predPileup in range(40,50):
        hpp4050.Fill(reso)
    elif predPileup in range(50,60):
        hpp5060.Fill(reso)
    elif predPileup in range(60,70):
        hpp6070.Fill(reso)
    elif predPileup in range(70,80):
        hpp7080.Fill(reso)
    else:
        pass

fp010 = ROOT.TFile("pileupresos/"+run+"hp010.root", "RECREATE")
fp010.WriteObject(hp010, run+"hp010")
fp010.WriteObject(hpp010, run+"hpp010")
print("Histogram 010 Created.") 
fp1020 = ROOT.TFile("pileupresos/"+run+"hp1020.root", "RECREATE")
fp1020.WriteObject(hp1020, run+"hp1020")
fp1020.WriteObject(hpp1020, run+"hpp1020")
print("Histogram 1020 Created.") 
fp2030 = ROOT.TFile("pileupresos/"+run+"hp2030.root", "RECREATE")
fp2030.WriteObject(hp2030, ""+run+"hp2030")
fp2030.WriteObject(hpp2030, ""+run+"hpp2030")
print("Histogram 2030 Created.")
fp3040 = ROOT.TFile("pileupresos/"+run+"hp3040.root", "RECREATE")
fp3040.WriteObject(hp3040, run+"hp3040")
fp3040.WriteObject(hpp3040, run+"hpp3040")
print("Histogram 3040 Created.") 
fp4050 = ROOT.TFile("pileupresos/"+run+"hp4050.root", "RECREATE")
fp4050.WriteObject(hp4050, run+"hp4050")
fp4050.WriteObject(hpp4050, run+"hpp4050")
print("Histogram 4050 Created.") 
fp5060 = ROOT.TFile("pileupresos/"+run+"hp5060.root", "RECREATE")
fp5060.WriteObject(hp5060, run+"hp5060")
fp5060.WriteObject(hpp5060, run+"hpp5060")
print("Histogram 5060 Created.") 
fp6070 = ROOT.TFile("pileupresos/"+run+"hp6070.root", "RECREATE")
fp6070.WriteObject(hp6070, run+"hp6070")
fp6070.WriteObject(hpp6070, run+"hpp6070")
print("Histogram 6070 Created.") 
fp7080 = ROOT.TFile("pileupresos/"+run+"hp7080.root", "RECREATE")
fp7080.WriteObject(hp7080, run+"hp7080")
fp7080.WriteObject(hpp7080, run+"hpp7080")
print("Histogram 7080 Created.") 



"""
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
    j = 0 
    k = 0 
    while (len(genJetptarr) != 0):
        print(len(genJetptarr),len(caloJetptarr))
        mincalojet = None
        delR = None
        for k in range(len(caloJetptarr)):
            print(ROOT.Math.VectorUtil.DeltaR(genJetptarr[j], caloJetptarr[k]))
            print(j, k)
            if delR == None:
                print("wat")
                delR = ROOT.Math.VectorUtil.DeltaR(genJetptarr[j], caloJetptarr[k])
            
            elif (ROOT.Math.VectorUtil.DeltaR(genJetptarr[j], caloJetptarr[k]) <= 0.3):
                print("wait so" +  str(delR))
                delR = min(ROOT.Math.VectorUtil.DeltaR(genJetptarr[j], caloJetptarr[k]), delR)
                mincalojet = caloJetptarr[k]
                minindex = k

            else:
                pass
            
            # Place into matched and unmatched
            if mincalojet != None:
                print("Popped!")
                elementgen = genJetptarr.pop(j)
                elementcalo = caloJetptarr.pop(minindex)
                genJetptarr.insert(0, elementgen)
                caloJetptarr.insert(0, elementcalo)

                cg_matched.append((genJetptarr.pop(0), caloJetptarr.pop(0)))
                # print("Popped!")
            elif mincalojet == None:
                print("Popped but not matched :(( wompwomp")
                elementgen = genJetptarr.pop(j)
                genJetptarr.insert(0, elementgen)

                if genJetptarr:
                    cg_unmatched.append(genJetptarr.pop(0))
                else:
                    pass


"""
"""
 j = 0 
    k = 0 
    while (len(genJetptarr) != 0):
        print(len(genJetptarr), len(caloJetptarr))
        mincalojet = None
        delR = None
        while (len(caloJetptarr) != 0):
            if delR == None:
                print("wat")
                delR = ROOT.Math.VectorUtil.DeltaR(genJetptarr[j], caloJetptarr[k])
            
            elif (ROOT.Math.VectorUtil.DeltaR(genJetptarr[j], caloJetptarr[k]) <= 0.3):
                print("wait so" +  str(delR))
                delR = min(ROOT.Math.VectorUtil.DeltaR(genJetptarr[j], caloJetptarr[k]), delR)
                mincalojet = caloJetptarr[k]
                minindex = k

            else:
                pass
            
            # Place into matched and unmatched
            if mincalojet != None:
                print("Popped!")
                elementgen = genJetptarr.pop(j)
                elementcalo = caloJetptarr.pop(minindex)
                genJetptarr.insert(0, elementgen)
                caloJetptarr.insert(0, elementcalo)

                cg_matched.append((genJetptarr.pop(0), caloJetptarr.pop(0)))
                # print("Popped!")
            elif mincalojet == None:
                print("Popped but not matched :(( wompwomp")
                elementgen = genJetptarr.pop(j)
                genJetptarr.insert(0, elementgen)
                if genJetptarr:
                    cg_unmatched.append(genJetptarr.pop(0))
                else:
                    break
        if not caloJetptarr:
            cg_unmatched.append(genJetptarr.pop(0))
            break
""" 

"""
- NO POP
    for j in range(len(genJetptarr)):
        mincalojet = None
        delR = None
        for k in range(len(caloJetptarr)):
            print(ROOT.Math.VectorUtil.DeltaR(genJetptarr[j], caloJetptarr[k]))
            print(j, k)
            if delR == None:
                print("wat")
                delR = ROOT.Math.VectorUtil.DeltaR(genJetptarr[j], caloJetptarr[k])
            
            elif (ROOT.Math.VectorUtil.DeltaR(genJetptarr[j], caloJetptarr[k]) <= 0.3):
                print("wait so" +  str(delR))
                delR = min(ROOT.Math.VectorUtil.DeltaR(genJetptarr[j], caloJetptarr[k]), delR)
                mincalojet = caloJetptarr[k]
                minindex = k

            else:
                pass
            
            # Place into matched and unmatched
            if mincalojet != None:
                cg_matched.append((genJetptarr[j], caloJetptarr[minindex]))
            elif mincalojet == None:
                cg_unmatched.append(genJetptarr[j])
"""
            

