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

directory = '/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genTrainML/output/curiousggHtobb_dataset.h5'

# Load data from HDF5 file
with h5py.File(directory, 'r') as hf:
    x_grid_data = hf['PhiRingEt'][:]
    x_linear1_data = hf['TPno'][:]
    x_linear2_data = hf['TPet'][:]
    y_data = hf['PuppiTrigEtDiff'][:]
print(x_grid_data.shape,x_linear1_data.shape, x_linear2_data.shape, y_data.shape)
exit()
# Define a partial function for Conv1D with specific parameters
DConv1D = partial(tf.keras.layers.Conv1D, kernel_size=7, strides=1, padding="same", activation="relu")

# Split the data into training, validation, and testing sets
x_grid_train, x_grid_test, x_linear1_train, x_linear1_test, x_linear2_train, x_linear2_test, y_train, y_test = \
    skms.train_test_split(x_grid_data, x_linear1_data, x_linear2_data, y_data, test_size=0.20, train_size=0.80, random_state=1234)
x_grid_test, x_grid_val, x_linear1_test, x_linear1_val, x_linear2_test, x_linear2_val, y_test, y_val = \
    skms.train_test_split(x_grid_test, x_linear1_test, x_linear2_test, y_test, test_size=0.10, train_size=0.90, random_state=1234)

# Define input shapes for each feature
input_shape_linear1 = (1,)  # Scalar feature 1
input_shape_linear2 = (1,)  # Scalar feature 2
input_shape_grid = x_grid_train.shape[1:]  # Grid feature shape based on training data

# Define input layers
input_linear1 = tf.keras.layers.Input(shape=input_shape_linear1, name='input_linear1')
input_linear2 = tf.keras.layers.Input(shape=input_shape_linear2, name='input_linear2')
input_grid = tf.keras.layers.Input(shape=input_shape_grid, name='input_grid')

# Define the convolutional layers
conv1 = DConv1D(filters=16)(input_grid)
flatten = tf.keras.layers.Flatten()(conv1)

# Concatenate the flattened grid feature with linear features
concatenated = tf.keras.layers.Concatenate()([flatten, input_linear1, input_linear2])

# Add dense layers
dense1 = tf.keras.layers.Dense(units=32, activation='relu')(concatenated)
output = tf.keras.layers.Dense(units=1)(dense1)  # Linear output

# Create the model
model = tf.keras.models.Model(inputs=[input_linear1, input_linear2, input_grid], outputs=output)

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

# Train the model
history = model.fit(
    [x_linear1_train, x_linear2_train, x_grid_train],  # Pass the input data as a list
    y_train,
    epochs=10,
    batch_size=32,
    validation_data=([x_linear1_val, x_linear2_val, x_grid_val], y_val),
)

# Evaluate the model on the test set
test_loss, test_mae = model.evaluate([x_linear1_test, x_linear2_test, x_grid_test], y_test)
eval_metric(model, history)
plt.savefig("learningCurvecuriousggHbb-1l-u32-bs32-ks7-s1-flatten.png")
print(f"Test Loss: {test_loss}, Test MAE: {test_mae}")
model.save("curiousggHbb-1l-u32-bs32-ks7-s1-flatten_NN")
print("Done!")