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

# Read files
directory = '/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genTrainML/output/delputrvtotalntotalet_dataset.h5'
f = h5py.File(directory, 'r')

y = f['avgpuppitrigEt'][:]
x_1 = f['totalTPno'][:]
x_2 = f['totalTPET'][:]

x_train, x_test, y_train, y_test = skms.train_test_split(np.column_stack((x_1, x_2)), y, test_size=0.20, train_size = 0.80, random_state =1234)

model = tf.keras.Sequential(
[
   tf.keras.layers.BatchNormalization(input_shape=x_train.shape[1:]),
   tf.keras.layers.Dense(2, input_shape=x_train.shape[1:], activation = 'relu'),
   tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss = "mean_squared_error", metrics = ["RootMeanSquaredError"])

# Train Model and Save History
history = model.fit(x_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Test Model
mse_test, rmse_test = model.evaluate(x_test, y_test)
x_new = x_test[:]
y_pred = model.predict(x_new)
print(f'Test Mean Squared Error: {mse_test}' + f' Test Root Mean Squared Error: {rmse_test}' + f'Test Prediction: {y_pred}')

# Plot History
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Learning Curve')
plt.legend()
plt.show()
plt.savefig("learningCurvetot-1l-u2-bs32wrelu.png")

# Calling `save('my_model')` creates a SavedModel folder `my_model`.
tf.keras.utils.plot_model(model, to_file="tot-1l-u2-bs32wrelu.png", show_shapes=True)
model.save("tot-1l-u2-bs32wrelu_NN")
print("Done!")

