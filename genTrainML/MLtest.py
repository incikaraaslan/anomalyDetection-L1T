import h5py
import numpy as np
import sklearn
import sklearn.model_selection as skms
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error
import math

# Read files from Andrew's large file
directory = '/hdfs/store/user/aloeliger/largeInputFile_manyInput_CICADAv2.hdf5'
f = h5py.File(directory, 'r')
cicadaInput = f['cicadaInput'][:100000] # len() -> 32316864
cicadaInput = cicadaInput.reshape((-1,1,18*14,))
pileup = f['pileup'][:100000] # len() -> 32316864
f.close()

# It will have 4 datasets inside, but the ones you care about will be called "cicadaInput" and "pileup".
cicada_train, cicada_test, pileup_train, pileup_test = skms.train_test_split(cicadaInput, pileup, test_size=0.20, random_state =1234)
print(cicada_train.shape)
print(pileup_train.shape)

# Mean - Train
dummy_regr = DummyRegressor(strategy="mean")
dummy_regr.fit(cicada_train, pileup_train)

# Mean - Predict and Score
mean_arr = []
for i in np.arange(np.size(pileup_test)):
    mean_arr.append(np.sum(pileup_test) / np.size(pileup_test))
mean_arr = np.asarray(mean_arr)

p = dummy_regr.predict(cicada_test)
s = dummy_regr.score(cicada_test, mean_arr)
# mse = sklearn.metrics.mean_squared_error(cicada_test, mean_arr)
# rmse = sklearn.metrics.mean_squared_error(cicada_test, mean_arr, squared = False)
print(p, mean_arr, s)
print(math.sqrt(mean_squared_error(p, pileup_test, squared = False)))
# print(mse, rmse)
# [29.718613 ... 29.718613] [29.7853 ... 29.7853] 0.0

# A constant model that always predicts the expected value of y, disregarding the input features, 
# would get a R^2 score of 0.0.
# The best possible score is 1.0 and it can be negative (because the model can be arbitrarily worse).

# Median
dummy_regr2 = DummyRegressor(strategy="median")
dummy_regr2.fit(cicada_train, pileup_train)

# Median - Predict and Score
med_arr = []
for i in np.arange(np.size(pileup_test)):
    med_arr.append(np.median(pileup_test))
med_arr = np.asarray(med_arr)

p2 = dummy_regr2.predict(cicada_test)
s2 = dummy_regr2.score(cicada_test, med_arr)
# mse2 = sklearn.metrics.mean_squared_error(cicada_test, med_arr)
# rmse2 = sklearn.metrics.mean_squared_error(cicada_test, med_arr, squared = False)
#print(pileup_test[:100])
#print(p2, med_arr, s2)
# print(mse2, rmse2)
# [29. 29. 29. ... 29. 29. 29.] [29. 29. 29. ... 29. 29. 29.] 1.0

print(p2, med_arr, s2)
print(math.sqrt(mean_squared_error(p2, pileup_test, squared=False)))

print(f"first event: {cicada_test[0]} {pileup_test[0]} {dummy_regr2.predict(cicada_test[0])}")

### RESULTS: ###
"""
(80000, 1, 252)
(80000, 1)

MEAN:
[29.733376 29.733376 29.733376 ... 29.733376 29.733376 29.733376] [29.72625 29.72625 29.72625 ... 29.72625 29.72625 29.72625] 0.0
8.102095966193572

MEDIAN:
[29. 29. 29. ... 29. 29. 29.] [29. 29. 29. ... 29. 29. 29.] 1.0
8.13457734438473

first event: [[ 0.  0.  0.  1.  5.  0.  1.  1.  1.  2.  2.  0.  2.  0.  1.  0.  0.  0.
  14.  7.  2.  3.  1.  1.  2.  0.  0.  0.  3.  1.  1.  0.  1.  1.  1.  2.
   1.  0.  4.  0.  2.  0.  1.  3.  0.  2.  2.  1.  1.  5.  3.  2.  0.  0.
   0.  0.  2.  1.  0.  2.  1.  3.  2.  3. 10.  0.  7.  0.  2.  0.  0.  0.
   0.  3.  2.  3.  4.  3.  0.  0.  0.  0.  0.  0.  7.  0.  0.  2.  2.  7.
   4.  3.  2.  1.  0.  0.  1.  0.  0.  1.  3.  2.  3.  0.  0.  5.  2.  0.
   4.  0.  1.  0.  2.  0.  1.  2.  0.  2. 11.  2.  1.  0.  0.  1.  2.  0.
   3.  1.  1.  1.  2.  2.  4.  3. 16.  0.  0.  1.  0.  0.  6.  0.  0.  0.
   1.  3.  4.  0.  1.  3.  3.  0.  2.  0.  3.  2.  0.  4.  2.  1.  4.  1.
   1.  1.  0.  0.  0.  0.  0.  0.  0.  5.  2.  1.  2.  8.  4.  0.  0.  0.
   0.  0.  0.  0.  0.  2.  1.  1.  2.  4.  4.  0.  1.  0.  0.  1.  0.  0.
   0.  0.  2.  1.  6.  3.  7.  2. 17.  0.  0.  0.  0.  1.  0.  4.  0.  4.
   4.  2.  0.  1. 10.  0.  0.  2.  0.  2.  0.  0.  1.  2.  1.  3.  2.  2.
   4.  0.  2.  0.  2.  0.  0.  5.  5.  1.  3.  6.  0.  0.  4.  0.  0.  0.]] [16.] [29.]
"""