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

# Draw the Histogram
h = ROOT.TH1F("resocaloResPlot", "Resolution Plot", 100, -4.0, 4.0)

# Lists
cg_matched = []
cg_unmatched = []

# Lorentz Vector Matching
for i in tqdm(range(100000)): # chains['genJet'].GetEntries() - 100000 events if you can
    caloJetptarr = []
    recoJetptarr = []
    chains['recoJet'].GetEntry(i)
    chains['caloJet'].GetEntry(i)
    # Each p_t, eta, phi, transverse mass entry has multiple jets in the form of vector<double>.
    # start = datetime.now()
    """t1_start = perf_counter()"""
    for j in range(chains['recoJet'].etaVector.size()):
        recoJet = ROOT.TLorentzVector()
        # genJet.SetPtEtaPhiM(chains['genJet'].genJetPt[j], chains['genJet'].genJetEta[j], chains['genJet'].genJetPhi[j], chains['genJet'].genJetMass[j])
        recoJet.SetPtEtaPhiM(chains['recoJet'].ptVector[j], chains['recoJet'].etaVector[j], chains['recoJet'].phiVector[j], chains['recoJet'].massVector[j])
        recoJetptarr.append(recoJet)
    for j in range(chains['caloJet'].etaVector.size()):
        caloJet = ROOT.TLorentzVector()
        caloJet.SetPtEtaPhiM(chains['caloJet'].ptVector[j], chains['caloJet'].etaVector[j], chains['caloJet'].phiVector[j], chains['caloJet'].massVector[j])
        caloJetptarr.append(caloJet)
    """t1_stop = perf_counter()
    print("Lorentz Block:", t1_stop - t1_start)""" # 174 ms
    """end = datetime.now()
    td = (end - start).total_seconds() * 10**3"""
    # print(f"The time of execution of above program is : {td:.03f}ms") # 244.007 ms / 147

    # Matching vectors via deltaR < 0.3
    j = 0
    """t2_start = perf_counter()"""
    """start3 = datetime.now()"""
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
        """t3_stop = perf_counter()
        print("Neighbor Search:", t3_stop-t3_start)""" # 159 ms
        """end1 = datetime.now()
        td1 = (end1 - start1).total_seconds() * 10**3
        print(f"The time of execution of above program is : {td1:.03f}ms")""" # 254.120 ms / 167 / 

        # Place into matched and unmatched
        """t4_start = perf_counter()"""
        """ start2 = datetime.now()"""
        if minindex:
            cg_matched.append((recoJetptarr.pop(0), caloJetptarr.pop(minindex)))
            # print("Popped!")
        else:
            cg_unmatched.append(recoJetptarr.pop(0))
        """end2 = datetime.now()
        td2 = (end2 - start2).total_seconds() * 10**3"""
        # print(f"The time of execution of above program is : {td2:.03f}ms") # 0.03 ms / 0.023
        """t4_stop = perf_counter()
        print("Matched Unmatched:", t4_stop-t4_start)"""
        
        # Just in Case :)
        if not caloJetptarr:
            if recoJetptarr:
                cg_unmatched.append(recoJetptarr.pop(0))

    """t2_stop = perf_counter()
    print("While Loop:", t2_stop-t2_start)""" # 4 ms
    """end3 = datetime.now()
    td3 = (end3 - start3).total_seconds() * 10**3"""
    # print(f"The time of execution of above program is : {td3:.03f}ms") #6.69 ms? / 4.416 ms
        



# for j in range(len(genJetptarr)):      
"""print("Matched Arr: " + str(cg_matched))
print("Unmatched Arr: " + str(cg_unmatched))"""

# Draw the Histogram
for i in cg_matched:
    reso = (i[1].Pt() - i[0].Pt())/(i[0].Pt())
    h.Fill(reso)

resoh = ROOT.TFile("resocaloResPlot"+run+".root", "RECREATE")
resoh.WriteObject(h, "resocaloResPlot"+run)
print("Histogram Created.")



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
            

