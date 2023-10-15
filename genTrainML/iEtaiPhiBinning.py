# some utilities to make handling iEta iPhi mapping to genuine phi easier
# these map regions, not necessarily towers.

import math

class iPhiBin():
    def __init__(self, iPhi: int, lowEdge: float, highEdge: float):
        self.iPhi = iPhi
        self.lowEdge = lowEdge
        self.highEdge = highEdge

    def isInBin(self, phi: float) -> bool:
        if phi > math.pi:
            return self.isInBin(phi=(phi-math.pi))
        elif phi < -1.0*math.pi:
            return self.isInBin(phi=(phi+math.pi))
        elif self.highEdge < self.lowEdge: # the loop around point
            if phi > self.lowEdge or phi <= self.highEdge:
                return True
            else:
                return False
        else:
            if phi >= self.lowEdge and phi < self.highEdge:
                return True
            else:
                return False
    def getValue(self)->int:
        return self.iPhi
        
class iEtaBin():
    def __init__(self, iEta: int, lowEdge: float, highEdge: float):
        self.iEta = iEta
        self.lowEdge = lowEdge
        self.highEdge = highEdge
    
    def isInBin(self, eta: float) -> bool:
        if eta >= self.lowEdge and eta < self.highEdge:
            return True
        else:
            return False
    def getValue(self)->int:
        return self.iEta

regionPhiBinMapping = {
    0: (-0.1745, 0.1745),
    1: (0.1745, 0.5235),
    2: (0.5235, 0.8726),
    3: (0.8726, 1.221),
    4: (1.221, 1.570),
    5: (1.570, 1.919),
    6: (1.919, 2.269),
    7: (2.269, 2.618),
    8: (2.618, 2.967),
    9: (2.967, -2.967),
    10: (-2.967, -2.618),
    11: (-2.618, -2.269),
    12: (-2.269, -1.919),
    13: (-1.919, -1.570),
    14: (-1.570, -1.221),
    15: (-1.221, -0.8726),
    16: (-0.8726, 0.5235),
    17: (-0.5235, -0.1745),
}

regionEtaBinMapping = {
    0: (-5.0, 4.5),
    1: (-4.5, -4.0),
    2: (-4.0, -3.5),
    3: (-3.5, -3.0),
    4: (-3.0, -2.172),
    5: (-2.172, -1.74),
    6: (-1.74, -1.392),
    7: (-1.392, -1.044),
    8: (-1.044, -0.696),
    9: (-0.696, -0.348),
    10: (-0.348, 0.0),
    11: (0.0, 0.348),
    12: (0.348, 0.696),
    13: (0.696, 1.044),
    14: (1.044, 1.392),
    15: (1.392, 1.74),
    16: (1.74, 2.172),
    17: (2.172, 3.0),
    18: (3.0, 3.5),
    19: (3.5, 4.0),
    20: (4.0, 4.5),
    21: (4.5, 5.0)
}

etaTowerEdges = [
    0.0,  # begin edge of 0 bin
    0.087,      
    0.174, 
    0.261,
    0.348, # end edge of 0 bin, begin edge 1 bin
    0.435,
    0.522,
    0.609,
    0.696, # end
    0.783,
    0.870,
    0.957,
    1.044,
    1.131,
    1.218,
    1.305,
    1.392,
    1.479,
    1.566,
    1.653,
    1.74,
    1.848,
    1.956, 
    2.064,
    2.172,
    2.379,
    2.586,
    2.793,
    3.0,
    3.250, 
    3.50,
    3.750,
    4.0,
    4.250,
    4.50,
    4.750,
    5.0,
]
def generateEtaBinMapping():
    allEdges = []
    for edge in etaTowerEdges:
        allEdges.append(edge)
        if edge != 0.0:
            allEdges.insert(0, -1.0*edge)
    edgeMapping = {}
    for i in range(len(allEdges)-1):
        edgeMapping[i] = (allEdges[i],allEdges[i+1])
    # print(edgeMapping)
    return edgeMapping

#comes up with 64 bins, zero indexing: 5-58 inclusive are region towers
towerEtaBinMapping = generateEtaBinMapping() #56 towers in eta

def generatePhiBinMapping():
    edgeMapping = {}
    increment = math.pi/36.0
    for i in range(36):
        edgeMapping[i] = (i*increment, (i+1)*increment)
    for i in range(36,72):
        edgeMapping[i] = (-1.0*math.pi+(i-36)*increment, -1.0*math.pi+(i-35)*increment)
    # print(edgeMapping)
    return edgeMapping

towerPhiBinMapping = generatePhiBinMapping() #72 towers in phi

    
class iEtaiPhiBinCollection():
    def __init__(
        self,
        phiBinMapping = regionPhiBinMapping,   
        etaBinMapping = regionEtaBinMapping,
    ):
        self.phiBinMapping = phiBinMapping
        self.etaBinMapping = etaBinMapping

        self.iphiBins = [iPhiBin(iPhi=iPhi, lowEdge=self.phiBinMapping[iPhi][0], highEdge=self.phiBinMapping[iPhi][1]) for iPhi in self.phiBinMapping]
        self.ietaBins = [iEtaBin(iEta=iEta, lowEdge=self.etaBinMapping[iEta][0], highEdge=self.etaBinMapping[iEta][1]) for iEta in self.etaBinMapping]
    
    #search through our phi bins for the appropriate phi bin. to return
    #unfortunately, due to the cyclical, un-ordinally-sorted nature of the phi bins
    #We have to check them one at a time.
    #O(N) is pretty terrible...
    def findAppropriatePhiBin(self, value: float)->iPhiBin:
        returnBin = None
        for bin in self.iphiBins:
            if bin.isInBin(value):
                returnBin = bin
                break
        return returnBin

    #
    def searchAppropriateBin(self, value: float, listToSearch: list)->iEtaBin:
        #if the list is only one element, check it
        if len(listToSearch) == 1:
            if listToSearch[0].isInBin(value):
                return listToSearch[0]
            else:
                return None
        #otherwise determine a central element
        else:
            centralValue = len(listToSearch) // 2
            #if we're in the bin at the central value, then good
            if listToSearch[centralValue].isInBin(value):
                return listToSearch[centralValue]
            #otherwise, we need to determine a new half of the list to search
            else:
                if value >= listToSearch[centralValue].highEdge:
                    return self.searchAppropriateBin(value=value, listToSearch=listToSearch[centralValue+1:])
                elif value < listToSearch[centralValue].lowEdge:
                    return self.searchAppropriateBin(value=value, listToSearch=listToSearch[:centralValue])
                else: #something has gone very wrong, but we should return out. This should never get called
                    return None

    #eta bins are ordinally sorted and have no cyclical nature, 
    #so we can search these sensibly
    def findAppropriateEtaBin(self, value)->iEtaBin:
        return self.searchAppropriateBin(value=value, listToSearch=self.ietaBins[:])
    
    def iEta(self, eta: float) -> int:
        theBin = self.findAppropriateEtaBin(value=eta)
        if theBin != None:
            return theBin.getValue()
        else:
            return None
    
    def iPhi(self, phi:float) -> int:
        theBin = self.findAppropriatePhiBin(value=phi)
        if theBin != None:
            return theBin.getValue()
        else:
            return None
    
    def iEtaiPhi(self, eta: float, phi: float)->tuple:
        return self.iEta(eta=eta),self.iPhi(phi=phi)
