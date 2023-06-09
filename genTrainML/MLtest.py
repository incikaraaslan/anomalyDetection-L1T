import h5py
import numpy as np

# Read files from Andrew's large file
directory = '/hdfs/store/user/aloeliger/largeInputFile_manyInput_CICADAv2.hdf5'
with h5py.File(directory, 'r') as f:
    cicadaInput = f['cicadaInput']
    pileup = f['pileup']
    print(cicadaInput[:10])
    print(pileup[:10])
    for k in f.keys():
        print(k)

# It will have 4 datasets inside, but the ones you care about will be called "cicadaInput" and "pileup".
