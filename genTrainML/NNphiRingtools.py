import numpy as np
import tensorflow as tf
import keras
import matplotlib.pyplot as plt
import h5py
import sklearn
import sklearn.model_selection as skms
from functools import partial
import matplotlib.pyplot as plt 
import pandas as pd
from evalNN import eval_metric

# Import Model
model = tf.keras.models.load_model('PhiRingSub-1l-u32-bs128-ks7-s1-flatten_NN')

# Import Data
directory = '/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genTrainML/output/phiringsubnewJetEt_dataset.h5'
f = h5py.File(directory, 'r')
x_test = f['PhiRingEttestshuf'][:]
x_train = f['PhiRingEttrainshuf'][:]
x_train = x_train.reshape(-1, 18, 1)
x_test = x_test.reshape(-1, 18, 1)

y_test = f['PuppiTrigEtDifftestshuf'][:]
y_train = f['PuppiTrigEtDifftrainshuf'][:]
y_train = y_train.reshape(-1, 1)
y_test = y_test.reshape(-1, 1)

print(len(x_train), len(x_test))
print(len(y_train), len(y_test))
y_trainpred = model.predict(x_train)
y_testpred = model.predict(x_test)

# Draw Histograms
# Histogram of the Predicted and True Distribution of pT
value_range = (-20,30)

# Training
plt.figure(figsize=(10, 5))
plt.hist(y_train, bins=50, range=value_range, color='blue', alpha=0.7, label='Matched Training TRIG/PUPPI pT Values')
plt.hist(y_trainpred.flatten(), bins=50, range=value_range, color='orange', alpha=0.7, label='Predicted Training TRIG pT Values')
plt.title('Histogram of Matched TRIG Jet pT v. SNAIL Jet pT Values')
plt.xlabel('Values')
plt.ylabel('Frequency')
plt.legend()
# Save the plot
plt.savefig('PUPPITrigvSNAILTrigTraining'+'PhiRingSub-1l-u32-bs128-ks7-s1-flatten_NN'+'.png')

# Test
plt.figure(figsize=(10, 5))
plt.hist(y_test, bins=50, range=value_range, color='purple', alpha=0.7, label='Matched Test TRIG/PUPPI pT Values')
plt.hist(y_testpred.flatten(), bins=50, range=value_range, color='red', alpha=0.7, label='Predicted Test TRIG pT Values')
plt.title('Histogram of Matched TRIG Jet pT v. SNAIL Jet pT Values')
plt.xlabel('Values')
plt.ylabel('Frequency')
# plt.ylim(0, 1.04e6)
plt.legend()
# Save the plot
plt.savefig('PUPPITrigvSNAILTrigTest'+'PhiRingSub-1l-u32-bs128-ks7-s1-flatten_NN'+'.png')

# Average Error plot between pT values
trainerrors = np.abs(y_trainpred - y_train)
testerrors = np.abs(y_testpred - y_test)
trainaverage_error = np.mean(trainerrors)
testaverage_error = np.mean(testerrors)
value_range = (-40,40)

plt.figure(figsize=(10, 5))
plt.hist(trainerrors, bins=50, range=value_range, color='red', alpha=0.7, label='Training TRIG/PUPPI pT Error')
plt.hist(testerrors, bins=50, range=value_range, color='blue', alpha=0.7, label='Test TRIG/PUPPI pT Error')
plt.title('Histogram of Absolute Errors (Training Average Error: {:.2f})'.format(trainaverage_error) + '(Test Average Error: {:.2f})'.format(testaverage_error))
plt.xlabel('Absolute Errors')
plt.ylabel('Frequency')

plt.legend()

# Save the plot
plt.savefig('ErrorPUPPITrigvSNAILTrig'+'PhiRingSub-1l-u32-bs128-ks7-s1-flatten_NN'+'.png')

