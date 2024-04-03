import h5py
import numpy as np
import tensorflow as tf 
import sklearn
import sklearn.model_selection as skms
from functools import partial
import matplotlib.pyplot as plt 
import pandas as pd

def eval_metric(model, history):
    '''
    Function to evaluate a trained model on a chosen metric. 
    Training and validation metric are plotted in a
    line chart for each epoch.
    
    Parameters:
        history : model training history
        metric_name : loss or accuracy
    Output:
        line chart with epochs of x-axis and metric on
        y-axis
    '''
    plt.plot(history.history['loss'], label='Train')
    print("Done!")
    plt.plot(history.history['val_loss'], label='Validation')
    print("Done!")
    # Print the loss values at each epoch
    for epoch, loss in enumerate(history.history['loss'], 1):
        print(f'Epoch {epoch}: Loss = {loss:.4f}')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.title('Model Loss')
    plt.legend(loc='upper right')  
    plt.show()

"""
def eval_LC(model, history, ):
    pd.DataFrame(model.history).plot(figsize = (8,5), grid = True, xlabel = "Epoch", style = ["r--", "r--", "b-", "b-*"])
    plt.savefig("learnCurve.png")
"""