import h5py
import numpy as np
import tensorflow as tf 
import sklearn
import sklearn.model_selection as skms
from functools import partial
import matplotlib.pyplot as plt 
import pandas as pd
from evalNN import eval_metric

# Read files from Andrew's large file
directory = '/hdfs/store/user/aloeliger/largeInputFile_manyInput_CICADAv2.hdf5'
f = h5py.File(directory, 'r')
cicadaInput = f['cicadaInput'][:1000000] # len() -> 32316864
cicadaInput = cicadaInput.reshape(-1, 18, 14, 1)
pileup = f['pileup'][:1000000] # len() -> 32316864
f.close()

# split train data to validation and main training
# take a look at train v validation from the metric. Overfitting check -- employ regularization if overfitting. 

# Split Data - 70-20-10 // Train-Val-Test
cicada_train, cicada_test, pileup_train, pileup_test = skms.train_test_split(cicadaInput, pileup, test_size=0.10, random_state =1234)
cicada_train, cicada_val, pileup_train, pileup_val = skms.train_test_split(cicada_train, pileup_train, test_size=0.20, random_state =1234)

# Model Construction
# Thin Wrapper for Keras Conv2D callable in order to call on the activation function etc.
DConv2D = partial(tf.keras.layers.Conv2D, kernel_size = 3, strides = 2, padding = "same", activation = "relu")
# Group the linear stack of layers into a tf.keras.Model
model = tf.keras.Sequential(
    [
        DConv2D(filters = 4, input_shape = (18, 14, 1)), 
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
    cicada_train, 
    pileup_train, 
    batch_size = 32, 
    epochs = 10,
    validation_data=(cicada_val,pileup_val)
)


# Test Model
mse_test, rmse_test = model.evaluate(cicada_test, pileup_test)
cicada_new = cicada_test[:]
pileup_pred = model.predict(cicada_new)
print(mse_test, rmse_test, pileup_pred)

"""
MSE: 27.94085693359375 RMSE: 5.2859110832214355
"""

# Draw Learning Curve
eval_metric(model, trainHistory)
plt.savefig("learnCurveCICADAlike.png")
# Calling `save('my_model')` creates a SavedModel folder `my_model`.
model.save("CICADA-like_NN")
