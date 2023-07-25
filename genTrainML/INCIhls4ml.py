# Simple hls4ml version of the newSNAIL, a CICADA-like NN model for pileup prediction
import numpy as np
import plottingg
import h5py
import tensorflow as tf 
from functools import partial
from tensorflow.keras.utils import to_categorical
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score
import sklearn.model_selection as skms
import matplotlib.pyplot as plt 
from matplotlib.lines import Line2D
from matplotlib.legend import Legend
import pandas as pd
import hls4ml

# LOAD Dataset
# Read files from Andrew's large file
directory = '/hdfs/store/user/aloeliger/largeInputFile_manyInput_CICADAv2.hdf5'
f = h5py.File(directory, 'r')
cicadaInput = f['cicadaInput'][:1000000] # len() -> 32316864
cicadaInput = cicadaInput.reshape(-1, 18, 14, 1)
pileup = f['pileup'][:1000000] # len() -> 32316864
le = LabelEncoder()
le.fit(pileup)
f.close()


# Split Data - 70-20-10 // Train-Val-Test
cicada_train, cicada_test, pileup_train, pileup_test = skms.train_test_split(cicadaInput, pileup, test_size=0.10, random_state =1234)
cicada_train, cicada_val, pileup_train, pileup_val = skms.train_test_split(cicada_train, pileup_train, test_size=0.20, random_state =1234)


# LOAD Model + Predict via Keras
model = tf.keras.models.load_model('CICADA-like_NN')
cicada_new = cicada_test[:]
pileup_pred = model.predict(cicada_new)

# HLS4ML CONFIG
config = hls4ml.utils.config_from_keras_model(model, granularity='model')
cfg = hls4ml.converters.create_config(part="xc7vx690tffg1927-2")

cfg['IOType'] = 'io_parallel'
cfg['HLSConfig'] = config
cfg['KerasModel'] = model
cfg['ClockPeriod']  = 6.25
cfg['OutputDir']  = 'hls4mlCICADA-like_NN/newSNAIL_prj'
cfg['Part'] = 'xc7vx690tffg1927-2'

"""hls_model = hls4ml.converters.convert_from_keras_model(
    model, hls_config=config, output_dir='hls4mlCICADA-like_NN/newSNAIL_prj', part='xc7vx690tffg1927-2'
)"""
hls_model = hls4ml.converters.keras_to_hls(cfg)

# Compile Model
hls_model.compile()

# Plottings
hls4ml.utils.plot_model(hls_model, show_shapes=False, show_precision=True, to_file="foo.png")

# Test Model
cicada_new = np.ascontiguousarray(cicada_test[:])
pileup_predhls = hls_model.predict(cicada_new)

# Plottings Accuracy
print("Keras  Accuracy: {}".format(accuracy_score(np.argmax(pileup_test, axis=1), np.argmax(pileup_pred, axis=1))))
print("hls4ml Accuracy: {}".format(accuracy_score(np.argmax(pileup_test, axis=1), np.argmax(pileup_predhls, axis=1))))

"""fig, ax = plt.subplots(figsize=(9, 9))
_ = plottingg.makeRoc(pileup_test, pileup_pred, le.classes_)
plt.gca().set_prop_cycle(None)  # reset the colors
_ = plottingg.makeRoc(pileup_test, pileup_predhls, le.classes_, linestyle='--')

lines = [Line2D([0], [0], ls='-'), Line2D([0], [0], ls='--')]
leg = Legend(ax, lines, labels=['keras', 'hls4ml'], loc='lower right', frameon=False)
ax.add_artist(leg)
plt.savefig("foo2.png")"""

# Build and Export Model
hls_model.build(csim=False, export=True)

# Print Report
hls4ml.report.read_vivado_report('hls4mlCICADA-like_NN/newSNAIL_prj/')
