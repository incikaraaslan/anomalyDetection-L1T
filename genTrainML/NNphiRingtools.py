import numpy as np
import tensorflow as tf
import h5py
import sklearn.model_selection as skms
import matplotlib.pyplot as plt

# Import Model
model = tf.keras.models.load_model('tot-2f-1l-u2-bs32wrelu_NN')

# Import Data
directory = '/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genTrainML/output/delputrvtotalntotaletwcicada_dataset.h5'
f = h5py.File(directory, 'r')
x1 = f["totalTPno"][:]
x2 = f["totalTPET"][:]
y = f["avgpuppitrigEt"][:]

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = skms.train_test_split(np.column_stack((x1, x2)), y, test_size=0.20, random_state=1234)

# Predict using the model
y_trainpred = model.predict(x_train)
y_testpred = model.predict(x_test)

# Calculate the absolute errors
trainerrors = y_trainpred - y_train
testerrors = y_testpred - y_test

# Calculate the average absolute errors
trainaverage_error = np.mean(trainerrors.flatten())
testaverage_error = np.mean(testerrors.flatten())

"""print(trainerrors.flatten(), testerrors.flatten())"""

# Define the value range for the histograms
value_range = (-50, 50) 
# combined_data = np.stack([trainaverage_error, testaverage_error], axis=1)

# Plot the histograms of absolute errors
"""plt.figure(figsize=(10, 5))
plt.hist(trainerrors.flatten(), bins=100, range=value_range, color="red", alpha=0.7, label='Training TRIG/PUPPI pT Error')
plt.hist(testerrors.flatten(), bins=100, range=value_range, color="blue", alpha=0.7, label='Test TRIG/PUPPI pT Error')
plt.title('Histogram of Errors (Training Average Error: {:.2f}, Test Average Error: {:.2f})'.format(trainaverage_error, testaverage_error))
plt.xlabel('Absolute Errors')
plt.ylabel('Frequency')
plt.legend()"""

# Save the plot
plt.savefig('ErrorPUPPITrigvSNAILTrig_tot-2f-1l-u2-bs32wrelu_NNN.png')
plt.show()

