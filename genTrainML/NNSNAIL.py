import numpy as np
import tensorflow as tf
import h5py
import sklearn
import sklearn.model_selection as skms
from functools import partial
import matplotlib.pyplot as plt 
import pandas as pd
from evalNN import eval_metric
import random
import math
from sklearn.metrics import mean_squared_error

# Set random seeds
np.random.seed(1234)
tf.random.set_seed(1234)
random.seed(1234)

# Prevent Keras from using all vram when running with GPU
"""gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],[tf.config.experimental.VirtualDeviceConfiguration(memory_limit=5120)])
  except RuntimeError as e:
    print(e)"""

# Read files
directory = '/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genTrainML/output/delputrvtotaln_dataset.h5'
f = h5py.File(directory, 'r')
#print(list(f.keys()))

y = f['avgpuppitrigEt'][:]
x = f['totalTPno'][:]
x = x.reshape(len(x), -1, 1)  # Reshape x to (num_samples, num_features, num_channels)
y = y.reshape(len(y), -1, 1)

print(len(y), len(x))
print(y, x)
f.close()

x_train, x_test, y_train, y_test = skms.train_test_split(x, y, test_size=0.20, train_size = 0.80, random_state =1234)
x_train, x_val, y_train, y_val = skms.train_test_split(x_train, y_train, test_size=0.10, train_size = 0.90, random_state =1234)

input_shape = x.shape[1:] 

# Hyperparameter Scan
# https://keras.io/keras_tuner/
# Data might not be predictive. Larger phi areas, areas around the jet, try to be more predictive. 
# With my test set of trigger jets and puppi jets, how big is the average error, run some predictive,
# Corrective TRIG jet pt v. PUPPI jet pt to check, make historgrams average error, pt spectrum of the actual puppi things

# Model Construction
# Thin Wrapper for Keras Conv2D callable in order to call on the activation function etc.
DConv1D = partial(tf.keras.layers.Conv1D, kernel_size = 7, strides = 1, padding = "same", activation = "relu")
# Group the linear stack of layers into a tf.keras.Model
model = tf.keras.Sequential(
    [
        DConv1D(filters = 8, input_shape = input_shape),
        tf.keras.layers.Flatten(), 
        tf.keras.layers.Dense(units = 32, activation = "relu"),
        # tf.keras.layers.Dense(units = 16, activation = "relu"),
        tf.keras.layers.Dense(units  = 1) # linear combination: y < 0. ReLU(a*x_1 + b*x_2+... w_n*x_n) >= 0, 
        # but a*x_1 + b*x_2 + ... w_n*x_n can be any value depending on the weights!
    ]
)

# Compile Model
# optimizer = tf.keras.optimizers.Adam(learning_rate = 1e-3)
model.compile(loss = "mean_squared_error", metrics = ["RootMeanSquaredError"])

# Training Model
trainHistory = model.fit(
    x_train, 
    y_train, 
    batch_size = 256, 
    epochs = 10,
    validation_data=(x_val,y_val)
)


# Test Model
mse_test, rmse_test = model.evaluate(x_test, y_test)
x_new = x_test[:]
y_pred = model.predict(x_new)
print(mse_test, rmse_test, y_pred)

print("Mean:" + str(np.mean(y_test))+ " , Predicted Mean: " + str(np.mean(y_pred)))
print("Median:" + str(np.median(y_test))+ " , Predicted Median: " + str(np.median(y_pred)))
print("Total Prediction MSE: " + str(mean_squared_error(y_pred.flatten(), y_test.flatten())))
print("Total Prediction RMSE: " + str(mean_squared_error(y_pred.flatten(), y_test.flatten(), squared = False)))

# Draw Learning Curve
eval_metric(model, trainHistory)
plt.savefig("learningCurvetot-1l-u32-bs128-ks7-s1-flatten.png")

# Calling `save('my_model')` creates a SavedModel folder `my_model`.
tf.keras.utils.plot_model(model, to_file="tot-1l-u32-bs128-ks7-s1-flatten.png", show_shapes=True)
model.save("tot-1l-u32-bs128-ks7-s1-flatten_NN")
print("Done!")