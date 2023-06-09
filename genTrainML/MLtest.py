import h5py
import numpy as np

# Read files from Andrew's large file
directory = 
with h5py.File('random.hdf5', 'w') as f:
    dset = f.create_dataset("default", data=arr)