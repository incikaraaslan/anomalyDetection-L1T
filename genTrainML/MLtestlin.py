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
directory = '/hdfs/store/user/aloeliger/largeInputFile_manyInput_CICADAv2.hdf5'
f = h5py.File(directory, 'r')
cicadaInput = f['cicadaInput'][:10000000] # len() -> 32316864
cicadaInput = cicadaInput.reshape(10000000, 252)
pileup = f['pileup'][:10000000] # len() -> 32316864
f.close()

# It will have 4 datasets inside, but the ones you care about will be called "cicadaInput" and "pileup".
cicada_train, cicada_test, pileup_train, pileup_test = skms.train_test_split(cicadaInput, pileup, test_size=0.20, random_state =1234)
lin_regr = LinearRegression().fit(cicada_train, pileup_train)
p = lin_regr.predict(cicada_test)

print("Mean:" + str(np.mean(pileup_test))+ " , Predicted Mean: " + str(np.mean(p)))
print("Median:" + str(np.median(pileup_test))+ " , Predicted Median: " + str(np.median(p)))
print("Total Prediction MSE: " + str(math.sqrt(mean_squared_error(p, pileup_test))))
print("Total Prediction RMSE: " + str(math.sqrt(mean_squared_error(p, pileup_test, squared = False))))
#### Larger Data Sizes ####
### 1000000 Entries ###
"""
Mean:30.795815 , Predicted Mean: 30.795448
Median:30.0 , Predicted Median: 29.836254
Total Prediction MSE: 5.5037788934098675
"""
### 10000000 Entries ###
"""
Mean:30.325575 , Predicted Mean: 30.36218
Median:30.0 , Predicted Median: 29.395414
Total Prediction MSE: 5.3991636900204965
"""