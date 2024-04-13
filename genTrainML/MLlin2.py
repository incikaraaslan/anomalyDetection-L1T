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
# Set random seeds
np.random.seed(1234)

# Read files
directory = '/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genTrainML/output/offset_dataset100000.h5'
f = h5py.File(directory, 'r')

y_actual = f['AvgDelOffsettp'][:]
x = f['TPno'][:]

# Create a linear regression model to predict y-values
model_lr = LinearRegression(fit_intercept=False)
model_lr.fit(x, y_actual)

# Predict y-values using the linear regression model
y_predicted = model_lr.predict(x)

# Compute offsets (difference between actual y and predicted y)
offsets = y_actual - y_predicted

# Feature selection (using x values)
features = x  # You can choose which features to use for the secondary model

# Split data into training and testing sets for the secondary model
x_train, x_test, y_train, y_test = train_test_split(features, y_actual, test_size=0.2, random_state=42)

# Standardize features (optional but can improve model performance)
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

# Train a secondary model (e.g., another linear regression model) to predict offsets
secondary_model = LinearRegression()
secondary_model.fit(x_train_scaled, y_train)

# Make predictions on the test set using the secondary model
offsets_predicted = secondary_model.predict(x_test_scaled)

# Correct y-values by subtracting the predicted offsets
# y_corrected = y_test - offsets_predicted
threshold = 1
y_corrected = np.where(y_test >= threshold, y_test - offsets_predicted, y_test)

# Calculate the Mean Squared Error (MSE) of the corrected y-values
print("Mean:" + str(np.mean(y_test))+ " , Predicted Mean: " + str(np.mean(y_corrected)) + '\n')
print("Median:" + str(np.median(y_test))+ " , Predicted Median: " + str(np.median(y_corrected)) + '\n')
print("Total Prediction MSE: " + str(mean_squared_error(y_test, y_corrected)) + '\n')
print("Total Prediction RMSE: " + str(math.sqrt(mean_squared_error(y_test, y_corrected))) + '\n')

# Plot correction
plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
plt.scatter(x_test, y_test, color='red', s=5, label='Original Data')
plt.scatter(x_test, y_test - y_corrected, color='blue', s=5, label='Corrected Data')
plt.xlabel('# HCAL + ECAL TP')
plt.ylabel(f'Average $\Delta(PUPPI P_T, TRIG P_T)$')
plt.title('Linear Regression Fit')
plt.legend()
plt.savefig('offset_plot.png')
plt.show()

# Results
"""with open('./output/NNtrialoutputs.txt', 'a') as file:
    file.write("Linear Regression Fit:\n")
    file.write("Mean:" + str(np.mean(y_test))+ " , Predicted Mean: " + str(np.mean(p)) + '\n')
    file.write("Median:" + str(np.median(y_test))+ " , Predicted Median: " + str(np.median(p)) + '\n')
    file.write("Total Prediction MSE: " + str(mean_squared_error(p, y_test)) + '\n')
    file.write("Total Prediction RMSE: " + str(math.sqrt(mean_squared_error(p, y_test))) + '\n')"""
