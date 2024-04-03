import h5py
import numpy as np
import sklearn
import sklearn.model_selection as skms
from sklearn.linear_model import LinearRegression
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error
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


# Read files from Andrew's large file
directory = '/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genTrainML/output/delputrvtotaln_dataset.h5'
f = h5py.File(directory, 'r')
y = f['avgpuppitrigEt'][:]
x = f['totalTPno'][:],
x = x.reshape(-1, 1)
y = y.reshape(-1, 1)
"""x = x.reshape(len(x), 1, 1)  # Reshape x to (num_samples, num_features, num_channels)
y = y.reshape(len(y), 1, 1)"""
f.close()

# It will have 4 datasets inside, but the ones you care about will be called "cicadaInput" and "pileup".
x_train, x_test, y_train, y_test = skms.train_test_split(x, y, test_size=0.20, train_size = 0.80, random_state =1234)
lin_regr = LinearRegression().fit(x_train, y_train)
p = lin_regr.predict(x_test)

print("Mean:" + str(np.mean(y_test))+ " , Predicted Mean: " + str(np.mean(p)))
print("Median:" + str(np.median(y_test))+ " , Predicted Median: " + str(np.median(p)))
print("Total Prediction MSE: " + str(math.sqrt(mean_squared_error(p, y_test))))
print("Total Prediction RMSE: " + str(math.sqrt(mean_squared_error(p, y_test, squared = False))))