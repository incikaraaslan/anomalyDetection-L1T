import h5py
import numpy as np
import sklearn
import sklearn.model_selection as skms
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error
import math

# Read files from Andrew's large file
directory = '/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genTrainML/output/'
f = h5py.File(directory, 'r')
x_train = f['PhiRingEttrain']
x_test = f['PhiRingEttest']
y_train = f['PuppiTrigEtDifftrain']
y_test = f['PuppiTrigEtDifftest']
f.close()

# Model Construction
# Thin Wrapper for Keras Conv2D callable in order to call on the activation function etc.
DConv1D = partial(tf.keras.layers.Conv1D, kernel_size = 3, strides = 2, padding = "same", activation = "relu")
# Group the linear stack of layers into a tf.keras.Model
model = tf.keras.Sequential(
    [
        DConv1D(filters = 4, input_shape = (18, 1)), 
        tf.keras.layers.Flatten(), 
        tf.keras.layers.Dense(units = 20, activation = "relu"),
        tf.keras.layers.Dense(units  = 1, activation = "relu")
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
    epochs = 10
)


# Test Model
mse_test, rmse_test = model.evaluate(x_test, y_test)
cicada_new = x_test[:]
pileup_pred = model.predict(cicada_new)
print(mse_test, rmse_test, pileup_pred)

"""
MSE: 27.94085693359375 RMSE: 5.2859110832214355
"""

# Draw Learning Curve
eval_metric(model, trainHistory)
plt.savefig("learnCurvephiSub.png")

# Calling `save('my_model')` creates a SavedModel folder `my_model`.
model.save("PhiSub_NN")
