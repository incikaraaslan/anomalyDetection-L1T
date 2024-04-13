import numpy as np
import tensorflow as tf
import h5py
import sklearn
import matplotlib.pyplot as plt
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
directory = '/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genTrainML/output/delputrvtotalntotalet1000000_dataset.h5'
f = h5py.File(directory, 'r')

y = f['avgpuppitrigEt'][:]
x_1 = f['totalTPno'][:]
x_2 = f['totalTPET'][:]

# np.column_stack((x_1, x_2))
x_train, x_test, y_train, y_test = skms.train_test_split(np.column_stack((x_1, x_2)), y, test_size=0.20, train_size = 0.80, random_state =1234)

model = tf.keras.Sequential(
[
   tf.keras.layers.BatchNormalization(input_shape=(2,)),
   tf.keras.layers.Dense(2, input_shape=x_train.shape[1:], activation = 'relu'),
   tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss = "mean_squared_error", metrics = ["RootMeanSquaredError"])

# Train Model and Save History
history = model.fit(x_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Test Model
mse_test, rmse_test = model.evaluate(x_test, y_test)
x_new = x_test[:]
p = model.predict(x_new)

# Plot History
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Learning Curve')
plt.legend()
plt.show()
plt.savefig("learningCurvetot-2f-1l-u2-bs32wrelu.png")

# Results
with open('./output/NNtrialoutputs.txt', 'a') as file:
    file.write("Batch Norm - Dense(2) - Dense(1) Fit with Two Features [nTP, TPET] with ReLU:\n")
    file.write("Mean:" + str(np.mean(y_test))+ " , Predicted Mean: " + str(np.mean(p)) + '\n')
    file.write("Median:" + str(np.median(y_test))+ " , Predicted Median: " + str(np.median(p)) + '\n')
    file.write("Total Prediction MSE: " + str(mean_squared_error(p, y_test)) + '\n')
    file.write("Total Prediction RMSE: " + str(math.sqrt(mean_squared_error(p, y_test))) + '\n')

# Calling `save('my_model')` creates a SavedModel folder `my_model`.
tf.keras.utils.plot_model(model, to_file="tot-2f-1l-u2-bs32wrelu.png", show_shapes=True)
model.save("tot-2f-1l-u2-bs32wrelu_NN")
print("Done!")

