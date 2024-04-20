import h5py
import numpy as np
import tensorflow as tf 
import sklearn
import sklearn.model_selection as skms


directory = '/afs/hep.wisc.edu/home/incik/CMSSW_13_1_0_pre2/src/genTrainML/output/nn_dataset.h5'
f = h5py.File(directory, 'r')

y_actual = f['DelPUPPITRIG'][:]
x1 = f['TPno'][:]
x2 = f['TPet'][:]
"""x1 = x1.reshape((-1,1))
x2 = x2.reshape((-1,1))"""
x = np.stack((x1, x2), axis = 1)

x_train, x_test, y_train, y_test = skms.train_test_split(x, y_actual, test_size=0.2, random_state=42)
x_test, x_val, y_test, y_val = skms.train_test_split(x_test, y_test, test_size=0.5, random_state=42)
print(x_train.shape, x_train, x.shape)
print(y_train.shape, y_train)

model = tf.keras.Sequential(
    [
        tf.keras.layers.Input(shape = x_train.shape[1:]),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(units  = 4, activation = "relu"),
        tf.keras.layers.Dense(units  = 1)
    ]
)
# CICADAregions, CICADAregiontotalet, have the entire 18 x 14 grid and do CNN on it.
model.compile(loss = "mean_squared_error", metrics = ["RootMeanSquaredError"], optimizer = "adam")
model.summary()
model.fit(
    x_train, y_train, 
    validation_data = (x_val, y_val),
    epochs = 20
    )

predictions = model.predict(x_test)
mse_test, rmse_test = model.evaluate(x_test, y_test)
print(predictions, predictions.shape, mse_test, rmse_test)
# model.save("simplethesis_NN")