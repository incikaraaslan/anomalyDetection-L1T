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

# Read files
directory = '/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genTrainML/output/ggHtobb_dataset.h5'
f = h5py.File(directory, 'r')
#print(list(f.keys()))

x_grid = f['CICADAEt'][:200000]
x_grid = x_grid.reshape(-1, 18, 14, 1) #(1, 18, 1) # len() = 7573

x1 = f['TPno'][:200000]
x1 = x1.reshape((-1,1))
x2 = f['TPet'][:200000]
x2 = x2.reshape((-1,1))
x1 = np.append(x1, x2, axis = 1)

y = f['PuppiTrigEtDiff'][:200000]
y = y.reshape(-1, 1, 1)
f.close()


xg_train, xg_test, x1_train, x1_test, y_train, y_test = skms.train_test_split(x_grid, x1, y, test_size=0.20, train_size = 0.80, random_state =1234)
xg_test, xg_val, x1_test, x1_val, y_test, y_val = skms.train_test_split(xg_test, x1_test, y_test, test_size=0.10, train_size = 0.90, random_state =1234)


# Model Construction
# Thin Wrapper for Keras Conv2D callable in order to call on the activation function etc.
x_gridinput = tf.keras.Input(shape = xg_train.shape[1:])
layer1 = tf.keras.layers.Conv2D(filters = 16, kernel_size = 5, activation = "relu", padding = "valid")(x_gridinput)
globalmax = tf.keras.layers.GlobalMaxPooling2D()(layer1)
x1input = tf.keras.Input(shape = x1_train.shape[1:])
concat = tf.keras.layers.Concatenate()([x1input, globalmax])
layer2 = tf.keras.layers.Dense(32, activation = "relu")(concat)
output = tf.keras.layers.Dense(1)(layer2)

model = tf.keras.Model(inputs=(x_gridinput, x1input), outputs=output, name="multi-conv2d-f16-k3-d32")
model.compile(loss = "mean_squared_error", metrics = ["RootMeanSquaredError"])
model.summary()
# Training Model
trainHistory = model.fit(
    (xg_train, x1_train), 
    y_train, 
    batch_size = 32, 
    epochs = 10,
    validation_data=((xg_val, x1_val), y_val)
)

# Test Model
x_test = (xg_test, x1_test)
mse_test, rmse_test = model.evaluate(x_test, y_test)
x_new = x_test[:]
y_pred = model.predict(x_new)
#print(mse_test, rmse_test)


# Draw Learning Curve
eval_metric(model, trainHistory)
plt.savefig("lCmulti-conv2d-f16-k3-d32.png")
print("Mean:" + str(np.mean(y_test))+ " , Predicted Mean: " + str(np.mean(y_pred)) + '\n')
print("Median:" + str(np.median(y_test))+ " , Predicted Median: " + str(np.median(y_pred)) + '\n')
"""print("Total Prediction MSE: " + str(mean_squared_error(y_test, y_pred)) + '\n')
print("Total Prediction RMSE: " + str(math.sqrt(mean_squared_error(y_test, y_pred))) + '\n')"""

# Calling `save('my_model')` creates a SavedModel folder `my_model`.
tf.keras.utils.plot_model(model, to_file="multi-conv2d-f16-k3-d32.png", show_shapes=True)
model.save("multi-conv2d-f16-k3-d32_NN")
print("Done!")