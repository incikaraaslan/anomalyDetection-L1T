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

y_actual = f['AvgDelOffsettp'][:]
x = f['TPno'][:]
y_actualerr = f['AvgDelOffsettperr'][:]
non_zero_index_axis = np.argmax(y_actual != 0, axis=0)
x = x[non_zero_index_axis:]
y_actual = y_actual[non_zero_index_axis:]
y_actualerr = y_actualerr[non_zero_index_axis:]

# Create ROOT Histogram
canvas = ROOT.TCanvas("canvas", "offsetfit", 800, 600)
leg = ROOT.TLegend(0.75, 0.8, 0.9, 0.9)
lingraph = ROOT.TGraphErrors(len(x))
linfit = ROOT.TGraphErrors(100)

# Create a linear regression model to predict y-values
model_lr = LinearRegression()
model_lr.fit(x, y_actual, 1/y_actualerr)

# Predict y-values using the linear regression model
y_predicted = model_lr.predict(x)

for i in range(len(x)):
    lingraph.SetPoint(i, x[i], y_actual[i])
    lingraph.SetPointError(i, 0.0, y_actualerr[i])

for i in range(100):
    linfit.SetPoint(i, i*25, model_lr.predict([[i*25]]))


lingraph.SetMarkerStyle(20)
lingraph.SetMarkerColor(ROOT.kRed)
lingraph.SetMarkerSize(1)
lingraph.SetMarkerStyle(ROOT.kFullCircle) 
lingraph.SetTitle("")
lingraph.GetXaxis().SetTitle("Number of HCAL+ECAL TPs")
lingraph.GetYaxis().SetTitle("Average Matched PUPPI p_{T}- Trigger Jet p_{T}")
linfit.SetMarkerColor(ROOT.kBlue)
linfit.SetLineWidth(3)


lingraph.Draw("AP")
linfit.Draw("L")
leg.AddEntry(lingraph, "Data", "P")
leg.AddEntry(linfit, "Fit", "L")
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
canvas.SaveAs("foo.png")

# Calculate the Mean Squared Error (MSE) of the corrected y-values
print("Mean:" + str(np.mean(y_actual))+ " , Predicted Mean: " + str(np.mean(y_predicted)) + '\n')
print("Median:" + str(np.median(y_actual))+ " , Predicted Median: " + str(np.median(y_predicted)) + '\n')
print("Total Prediction MSE: " + str(mean_squared_error(y_actual, y_predicted)) + '\n')
print("Total Prediction RMSE: " + str(math.sqrt(mean_squared_error(y_actual, y_predicted))) + '\n')
print("Model Coeff:" + str(model_lr.coef_) + " Intercept:" + str(model_lr.intercept_))

# Create profile histograms along x and y directions to get error bars
"""profileX = histfit.ProfileX()
profileY = histfit.ProfileY()

# Create a TGraphErrors object for x and y error bars
graphX = ROOT.TGraphErrors(profileX)
graphY = ROOT.TGraphErrors(profileY)
graphX.SetMarkerStyle(20)
graphY.SetMarkerStyle(20)
print(graphX.GetN(), histfit.GetEntries(), x_test, y_offset)"""

# Adjust the bin centers for x and y error bars
"""for binX in range(1, len(x_test) + 1):
    binContent = histfit.GetBinContent(binX, binX)
    binError = histfit.GetBinError(binX, binX)
    # Calculate bin center for x and y directions
    print(x_test[binX-1],y_offset[binX-1])
    x_center = x_test[binX-1]
    y_center = y_offset[binX-1]
    # Add point to the TGraphErrors with corresponding errors
    graphX.SetPoint(graphX.GetN(), x_center, y_center)
    graphX.SetPointError(graphX.GetN() - 1, binError, 0)  # Error in x direction
    graphY.SetPoint(graphX.GetN(), x_center, y_center)
    graphY.SetPointError(graphY.GetN() - 1, 0, binError)"""

# Set colors and styles for histograms
"""histfit.SetMarkerSize(0.7)
histfit.SetLineColor(ROOT.kBlue)
histfit.SetMarkerStyle(ROOT.kFullCircle)
histfit.SetMarkerColor(ROOT.kBlue)  
histdat.SetMarkerSize(0.7)
histdat.SetLineColor(ROOT.kRed)
histdat.SetMarkerStyle(ROOT.kFullCircle)
histdat.SetMarkerColor(ROOT.kRed)  

# Draw histograms and TGraphErrors object on canvas
histfit.Draw("COLZ")
graphX.Draw("same e1")
graphY.Draw("same e1")
histdat.Draw("SAME")


# Set axis labels and title
histfit.SetTitle("")
histfit.GetXaxis().SetTitle("Number of HCAL+ECAL TPs")
histfit.GetYaxis().SetTitle("Average Matched Puppi - Trigger Jet p_{T}")

# Add CMS label
cmsLatex = ROOT.TLatex()
cmsLatex.SetTextSize(0.05)
cmsLatex.SetNDC(True)
cmsLatex.SetTextAlign(32)
cmsLatex.DrawLatex(0.9,0.92, "#font[61]{CMS} #font[52]{Preliminary}")

# Add a horizontal dashed line at y=0
line = ROOT.TLine(0, 0, 2000, 0)  
line.SetLineStyle(ROOT.kDashed)
line.Draw()

# Save the canvas as an image
canvas.SaveAs("offset_plotroot.png")"""

"""plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
plt.scatter(x_test, y_test, color='red', s=5, label='Original Data')
plt.scatter(x_test, y_test - y_corrected, color='blue', s=5, label='Corrected Data')
plt.xlabel('# HCAL + ECAL TP')
plt.ylabel(f'Average $\Delta(PUPPI P_T, TRIG P_T)$')
plt.title('Linear Regression Fit')
plt.legend()
plt.savefig('offset_plot.png')
plt.show()"""

# Results
"""with open('./output/NNtrialoutputs.txt', 'a') as file:
    file.write("Linear Regression Fit:\n")
    file.write("Mean:" + str(np.mean(y_test))+ " , Predicted Mean: " + str(np.mean(p)) + '\n')
    file.write("Median:" + str(np.median(y_test))+ " , Predicted Median: " + str(np.median(p)) + '\n')
    file.write("Total Prediction MSE: " + str(mean_squared_error(p, y_test)) + '\n')
    file.write("Total Prediction RMSE: " + str(math.sqrt(mean_squared_error(p, y_test))) + '\n')"""
