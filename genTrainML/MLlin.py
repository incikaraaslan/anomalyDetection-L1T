import h5py
import numpy as np
import sklearn
import sklearn.model_selection as skms
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import math

"""
- Look at other regression models, classical ML methods
- mlflow if you wanna check it out
- GridSearchCV
- PCA, Robust PCA --> it could work for noise removal --> pileup//noise removal
- if you had a dataset with sample w and sample wo pileup, how to substract pileup
- pileup is theoretically uniformly distributed across the sample --> A doesn't think it's true, might be nondeterministic
- Still varies from event to event. Discuss this with Andrew
"""


# Set random seeds
np.random.seed(1234)

# Read files
directory = '/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genTrainML/output/offset_dataset.h5'
f = h5py.File(directory, 'r')

y = f['AvgDelOffsettp'][:]
x_1 = f['TPno'][:]
# x_2 = f['totalTPET'][:]

# np.column_stack((x_1, x_2))
x_train, x_test, y_train, y_test = skms.train_test_split(x_1, y, test_size=0.20, train_size = 0.80, random_state =1234)

scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# Initialize Linear Regression model
lin_regr = LinearRegression(fit_intercept=False)

# Lists to store training loss
train_loss = []

# Train Model
lin_regr.fit(x_train, y_train)  # fit the model

p = lin_regr.predict(x_test) # Prediction
offset_pred = y_test - p # Offset should be y_test - y_test = 0

# RMSE
print("Mean:" + str(np.mean(y_test))+ " , Predicted Mean: " + str(np.mean(p)) + '\n')
print("Median:" + str(np.median(y_test))+ " , Predicted Median: " + str(np.median(p)) + '\n')
print("Total Prediction MSE: " + str(mean_squared_error(p, y_test)) + '\n')
print("Total Prediction RMSE: " + str(math.sqrt(mean_squared_error(p, y_test))) + '\n')

# Plot correction
plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
plt.scatter(x_test, y_test, color='red', s=5, label='Original Data')
plt.scatter(x_test, p, color='blue', s=5, label='Corrected Data')
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
