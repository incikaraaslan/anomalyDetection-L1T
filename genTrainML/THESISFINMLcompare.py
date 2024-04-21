import ROOT
import h5py
import sklearn
import sklearn.model_selection as skms
import matplotlib.pyplot as plt
import math
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from array import array


ROOT.gStyle.SetOptStat(0)
# Set random seeds
np.random.seed(1234)

# Read files
directory = '/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genTrainML/output/offset_dataset100000.h5'
f = h5py.File(directory, 'r')

y_actual = f['AvgDelOffsettpet'][:]
x = f['TPet'][:]
y_actualerr = f['AvgDelOffsettpeterr'][:]
non_zero_index_axis = np.argmax(y_actual != 0, axis=0)
cut_indices = np.where(x < 1100)[0]
x = x[non_zero_index_axis:]
y_actual = y_actual[non_zero_index_axis:]
y_actualerr = y_actualerr[non_zero_index_axis:]
x = x[cut_indices]
y_actual = y_actual[cut_indices]
y_actualerr = y_actualerr[cut_indices]


directory2 = '/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genTrainML/output/offset_trialet100000.h5'
f2 = h5py.File(directory2, 'r')
y_fit = f2['AvgDelOffsettpet'][:]
xfit = f2['TPet'][:]
y_fiterr = f2['AvgDelOffsettpeterr'][:]
non_zero_index_axis = np.argmax(y_fit != 0, axis=0)
cut_indices = np.where(x < 1100)[0]
xfit = xfit[non_zero_index_axis:]
y_fit = y_fit[non_zero_index_axis:]
y_fiterr = y_fiterr[non_zero_index_axis:]
x = x[cut_indices]
y_actual = y_actual[cut_indices]
y_actualerr = y_actualerr[cut_indices]

# Create ROOT Histogram
canvas = ROOT.TCanvas("canvas", "offsetfit", 800, 600)
leg = ROOT.TLegend(0.75, 0.8, 0.9, 0.9)
lingraph = ROOT.TGraphErrors(len(x))
linfit = ROOT.TGraphErrors(len(xfit))


for i in range(len(x)):
    lingraph.SetPoint(i, x[i], y_actual[i])
    lingraph.SetPointError(i, 0.0, y_actualerr[i])

for i in range(len(xfit)):
    linfit.SetPoint(i, xfit[i], y_fit[i])
    linfit.SetPointError(i, 0.0, y_fiterr[i])


lingraph.SetMarkerStyle(20)
lingraph.SetMarkerColor(ROOT.kRed)
lingraph.SetMarkerSize(1)
lingraph.SetMarkerStyle(ROOT.kFullCircle) 
lingraph.SetTitle("")
lingraph.GetXaxis().SetTitle("Total HCAL E_{T} + ECAL E_{T}") # Number of HCAL+ECAL TPs
lingraph.GetYaxis().SetTitle("Average Matched PUPPI p_{T} - Trigger Jet p_{T}")
linfit.SetMarkerStyle(20)
linfit.SetMarkerColor(ROOT.kBlue)
linfit.SetMarkerSize(1)
linfit.SetMarkerStyle(ROOT.kFullCircle) 
lingraph.GetYaxis().SetRangeUser(-25, 30)

lingraph.Draw("AP")
linfit.Draw("P")
leg.AddEntry(lingraph, "Observed", "P")
leg.AddEntry(linfit, "Corrected", "P")
leg.SetLineWidth(1)
leg.SetFillStyle(0)
leg.Draw()

# Add CMS label after drawing other elements
cmsLatex = ROOT.TLatex()
cmsLatex.SetTextSize(0.05)
cmsLatex.SetNDC(True)
cmsLatex.SetTextAlign(32)
cmsLatex.SetTextColor(ROOT.kBlack) 
cmsLatex.DrawLatex(0.9, 0.92, "#font[61]{CMS} #font[52]{Preliminary}")
canvas.SaveAs("foo2e.png")

# Results
"""with open('./output/NNtrialoutputs.txt', 'a') as file:
    file.write("Linear Regression Fit:\n")
    file.write("Mean:" + str(np.mean(y_test))+ " , Predicted Mean: " + str(np.mean(p)) + '\n')
    file.write("Median:" + str(np.median(y_test))+ " , Predicted Median: " + str(np.median(p)) + '\n')
    file.write("Total Prediction MSE: " + str(mean_squared_error(p, y_test)) + '\n')
    file.write("Total Prediction RMSE: " + str(math.sqrt(mean_squared_error(p, y_test))) + '\n')"""
