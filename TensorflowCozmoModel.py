from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections

import numpy as np
import tensorflow as tf
import pandas as pd
import math
import h5py
import matplotlib.pyplot as plt
import scipy
from PIL import Image
from scipy import ndimage
import tensorflow as tf
from tensorflow.python.framework import ops
from sklearn import preprocessing
import time


df = pd.read_csv("~/Documents/csv_files/TensorflowCozmoRetentionModelUS.csv")


#remove NaNs
df = df.fillna(0)

msk = np.random.rand(len(df)) <=0.7
train_file = df[msk]
test_file = df[~msk]

BATCH_SIZE = 64

def generate_input_fn(filename, num_epochs=None, shuffle=True, batch_size=BATCH_SIZE):
    filename = filename
    labels = filename["high_2wd"]
    del filename["high_2wd"] # Labels column, already saved to labels variable
    
    return tf.estimator.inputs.pandas_input_fn(
        x=filename,
        y=labels,
        batch_size=batch_size,
        num_epochs=num_epochs,
        shuffle=shuffle)


def create_model_dir(model_type):
    return '~/Documents/models/model_' + model_type + '_' + str(int(time.time()))


#create feature columns list and set to numeric

columns = df.columns.tolist()
columns.remove('high_2wd')

deep_columns = []

for i in columns:
    x = tf.feature_column.numeric_column(i)
    deep_columns.append(x)
    

# If new_model=False, pass in the desired model_dir 
def get_model(model_type, new_model=False, model_dir=None):
    if new_model or model_dir is None:
        model_dir = create_model_dir(model_type) # Comment out this line to continue training a existing model
    print("Model directory = %s" % model_dir)
    
    m = None
    
    # Linear Classifier
    if model_type == 'WIDE':
        m = tf.estimator.LinearClassifier(
            model_dir=model_dir, 
            feature_columns=wide_columns)

    # Deep Neural Net Classifier
    if model_type == 'DEEP':
        m = tf.estimator.DNNClassifier(
            model_dir=model_dir,
            feature_columns=deep_columns,
            hidden_units=[150, 100, 75, 50])

    # Combined Linear and Deep Classifier
    if model_type == 'WIDE_AND_DEEP':
        m = tf.estimator.DNNLinearCombinedClassifier(
                model_dir=model_dir,
                linear_feature_columns=wide_columns,
                dnn_feature_columns=deep_columns,
                dnn_hidden_units=[100, 70, 50, 25])
        
    print('estimator built')
    
    return m, model_dir

MODEL_TYPE = 'DEEP'
model_dir = create_model_dir(model_type=MODEL_TYPE)
m, model_dir = get_model(model_type = MODEL_TYPE, model_dir=model_dir)

m.train(input_fn=generate_input_fn(train_file), steps=1000)

print('training done')

results = m.evaluate(input_fn=generate_input_fn(test_file, num_epochs=1, shuffle=False), 
                     steps=None)
print('evaluate done')
print('\nAccuracy: %s' % results['accuracy'])