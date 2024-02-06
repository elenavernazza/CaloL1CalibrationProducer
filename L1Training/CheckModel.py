import sys

import numpy as np
import os, sys, glob, time, json, random

from tensorflow.keras.initializers import RandomNormal as RN
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers as lay
from tensorflow.keras.layers import Dense
from tensorflow import keras
import tensorflow as tf

random.seed(7)
np.random.seed(7)
tf.random.set_seed(7)
tf.compat.v1.set_random_seed(7)
os.system('export PYTHONHASHSEED=7')

sys.path.insert(0,'..')
from Utils.PlotLosses import *
from NNModel_RegAndRate_AddEt import create_model,threshold_relaxation_sigmoid

feature_description = {
    'chuncky_donut': tf.io.FixedLenFeature([], tf.string, default_value=''), # byteslist to be read as string 
    'trainingPt'   : tf.io.FixedLenFeature([], tf.float32, default_value=0)  # single float values
}

# parse proto input based on description
def parse_function(example_proto):
    example = tf.io.parse_single_example(example_proto, feature_description)
    chuncky_donut = tf.io.parse_tensor(example['chuncky_donut'], out_type=tf.float32) # decode byteslist to original 81x43 tensor
    return chuncky_donut, example['trainingPt']



i = 1
BATCH_SIZE_PER_REPLICA = 1
GLOBAL_BATCH_SIZE = 2

indir = '/data_CMS/cms/motta/CaloL1calibraton/2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco'

print('\n ### Reading TF records from: ' + indir + '/testTFRecords/record_*.tfrecord')
InTestRecords = glob.glob(indir+'/testTFRecords/record_*.tfrecord')[0]
dataset = tf.data.TFRecordDataset(InTestRecords)
batch_size = len(list(dataset))
parsed_dataset = dataset.map(parse_function)
data = parsed_dataset.batch(batch_size).as_numpy_iterator().next()
print('\n ### N events in the dataset: ' + str(len(list(dataset))))
dataset_inputs = parsed_dataset.batch(GLOBAL_BATCH_SIZE).as_numpy_iterator().next()

Towers = data[0]
TTP_input = Towers[i:i+1]

print('\n ### Reading TF records from: ' + indir + '/rateTFRecords/record_*.tfrecord')
InTestRecords = glob.glob(indir+'/rateTFRecords/record_*.tfrecord')
dataset = tf.data.TFRecordDataset(InTestRecords)
batch_size = len(list(dataset))
parsed_dataset = dataset.map(parse_function)
data = parsed_dataset.batch(batch_size).as_numpy_iterator().next()
print('\n ### N events in the dataset: ' + str(len(list(dataset))))
rate_inputs = parsed_dataset.batch(GLOBAL_BATCH_SIZE).as_numpy_iterator().next()

Towers = data[0]
Rate_input = Towers[i:i+1]

print(TTP_input)
print(Rate_input)

model, TTP = create_model('HCAL', seedThr=8.)

# dummy_rateProxy_input = np.repeat([np.repeat([np.zeros(42)], 81, axis=0)], n_events, axis=0)
modelPt = model.predict([TTP_input, Rate_input], 1)

print(modelPt[0])
print(modelPt[1])
print(modelPt[2])

print(np.sum(TTP_input[:,:,0]))

####################################################################################################
####################################################################################################
####################################################################################################

def regressionLoss(y, y_pred, other):
    MAPE = tf.keras.losses.MeanAbsolutePercentageError(reduction=tf.keras.losses.Reduction.NONE)
    Total_ET = tf.math.add(y_pred, other)
    print(y_pred)
    print(other)
    print(Total_ET)
    # return tf.reshape(MAPE(y, Total_ET), (1, 1)) * 500 # FIXME: scaling to be defined
    return MAPE(y, Total_ET) # FIXME: scaling to be defined

# part of the loss that controls the weights overtraining
# def weightsLoss():
#     modelWeights = model.trainable_weights
#     modelWeights_ss = float( tf.math.reduce_sum(tf.math.abs(modelWeights[0]), keepdims=True) +
#                             tf.math.reduce_sum(tf.math.abs(modelWeights[1]), keepdims=True) +
#                             tf.math.reduce_sum(tf.math.abs(modelWeights[2]), keepdims=True)
#                             )             
#     return  modelWeights_ss * 1 # FIXME: scaling to be optimized

# part of the loss that controls the rate
def rateLoss(z, z_pred, jetThr, targetRate):

    # z_unc = (tf.reduce_sum(z[:,:,1], axis=1, keepdims=True) + tf.reduce_sum(z[:,:,0], axis=1, keepdims=True))
    # z_response = z_pred / z_unc
    # scale = tf.reduce_sum(z_response, axis=0) / BATCH_SIZE_PER_REPLICA
    # print(z_unc.shape, z_pred.shape, z_response.shape, scale.shape) # DEBUG
    
    scale = 1.
    jetThr = scale*jetThr - 0.1
    # compute fraction of passing events and multiply by rate scaling
    jets_passing_threshold = threshold_relaxation_sigmoid(z_pred, jetThr, 10.)
    proxyRate = tf.reduce_sum(jets_passing_threshold, keepdims=True) / BATCH_SIZE_PER_REPLICA
    realtive_diff = (proxyRate - targetRate) / targetRate
    return tf.cosh(1.0 * realtive_diff) * 1
    # sharpness of 10 corresponds to +/- 1 kHz
    # return threshold_relaxation_sigmoid(proxyRate, targetRate, 0.1) # FIXME: scaling to be optimized

# GPU distribution friendly loss computation
def compute_losses(y, y_pred, other, z, z_pred):

    regressionLoss_value = regressionLoss(y, y_pred, other)
    # weightsLoss_value = weightsLoss()
    rateLoss_value = rateLoss(z, z_pred, 40*2, 0.16026735515333712)

    fullLoss = regressionLoss_value + rateLoss_value

    return [tf.nn.compute_average_loss(fullLoss,             global_batch_size=GLOBAL_BATCH_SIZE),
            tf.nn.compute_average_loss(regressionLoss_value, global_batch_size=GLOBAL_BATCH_SIZE),
            tf.nn.compute_average_loss(rateLoss_value,       global_batch_size=GLOBAL_BATCH_SIZE)]

def custom_train_step(inputs, rate_inputs):
    x, y = inputs
    z, _ = rate_inputs
    with tf.GradientTape() as tape:
        y_pred, z_pred, other = model([x, z], training=True)
        losses = compute_losses(y, y_pred, other, z, z_pred)

    return losses

print(custom_train_step(dataset_inputs, rate_inputs))
