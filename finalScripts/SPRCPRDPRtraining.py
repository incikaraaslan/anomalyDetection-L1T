import numpy as np
import tensorflow as tf
import h5py
import sklearn
import sklearn.model_selection as skms
from functools import partial
import matplotlib.pyplot as plt 
import pandas as pd
from evalNN import eval_metric
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from array import array

# Prevent Keras from using all vram when running with GPU
"""gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],[tf.config.experimental.VirtualDeviceConfiguration(memory_limit=5120)])
  except RuntimeError as e:
    print(e)"""

# Read files
directory = '/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genTrainML/output/phiring_dataset.h5'
f = h5py.File(directory, 'r')
#print(list(f.keys()))

x = f['PhiRingEt'][:]
x = x.reshape(-1, 18, 1) #(1, 18, 1) # len() = 7573

y = f['PuppiTrigEtDiff'][:]
y = y.reshape(-1, 1, 1)
f.close()


x_train, x_test, y_train, y_test = skms.train_test_split(x, y, test_size=0.20, train_size = 0.80, random_state =1234)
x_test, x_val, y_test, y_val = skms.train_test_split(x_test, y_test, test_size=0.10, train_size = 0.90, random_state =1234)
"""num_rows = len(x_test)
num_columns = len(x_test[0]) 
shape = (num_rows, num_columns)
print(shape)"""

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
        DConv1D(filters = 16, input_shape = (18,1)),
        tf.keras.layers.Flatten(), 
        tf.keras.layers.Dense(units = 32, activation = "relu"),
        # tf.keras.layers.Dense(units = 32, activation = "relu"),
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
    batch_size = 32, 
    epochs = 20,
    validation_data=(x_val,y_val)
)


# Test Model
mse_test, rmse_test = model.evaluate(x_test, y_test)
x_new = x_test[:]
y_pred = model.predict(x_new)
print(mse_test, rmse_test, y_pred)


# Draw Learning Curve
eval_metric(model, trainHistory)
plt.savefig("learningCurvephiSubt-1l-u32-bs32-ks7-s1-flatten.png")
print("Mean:" + str(np.mean(y_test))+ " , Predicted Mean: " + str(np.mean(y_pred)) + '\n')
print("Median:" + str(np.median(y_test))+ " , Predicted Median: " + str(np.median(y_pred)) + '\n')
"""print("Total Prediction MSE: " + str(mean_squared_error(y_test, y_pred)) + '\n')
print("Total Prediction RMSE: " + str(math.sqrt(mean_squared_error(y_test, y_pred))) + '\n')"""

# Calling `save('my_model')` creates a SavedModel folder `my_model`.
tf.keras.utils.plot_model(model, to_file="phiSubt-1l-u32-bs32-ks7-s1-flatten.png", show_shapes=True)
model.save("PhiRingSubt-1l-u32-bs32-ks7-s1-flatten_NN")
print("Done!")