import numpy as np
import random, json, glob, os, mplhep
import matplotlib.pyplot as plt
plt.style.use(mplhep.style.CMS)

from NNModel_RegAndRate import *
import tensorflow as tf

random.seed(7)
np.random.seed(7)
os.system('export PYTHONHASHSEED=7')

feature_description = {
    'chuncky_donut': tf.io.FixedLenFeature([], tf.string, default_value=''), # byteslist to be read as string 
    'trainingPt'   : tf.io.FixedLenFeature([], tf.float32, default_value=0)  # single float values
}

# parse proto input based on description
def parse_function(example_proto):
    example = tf.io.parse_single_example(example_proto, feature_description)
    chuncky_donut = tf.io.parse_tensor(example['chuncky_donut'], out_type=tf.float32) # decode byteslist to original 81x43 tensor
    return chuncky_donut, example['trainingPt']

def threshold_relaxation_sigmoid(x, mean, sharpness):
    k = sharpness * (x - mean)
    return tf.sigmoid(k, name="sigmoid")

def RateProxyJets (cd, seedThr, jetThr):

    seedThr = seedThr - 0.1
    jetThr = jetThr - 0.1
    numThr = 1 - 0.1

    # for each tower apply sigmoid cut on the seed at seedThr (8): if tower energy > 8 jet_seed_found = 1, else 0
    TT_iesum = cd[:,:,1] + cd[:,:,0]
    jet_seed_found = threshold_relaxation_sigmoid(TT_iesum, seedThr, 1000.)
    # for each jet compute how many seeds were found
    jet_seed_number = tf.reduce_sum(jet_seed_found, axis=1, keepdims=True)
    # for each jet check the presence of at least one seed
    jet_seed_passing = threshold_relaxation_sigmoid(jet_seed_number, numThr, 1000.)

    # predict jet energy and apply threshold: sum all the ihad energies cd[:,:,1] of the 9x9 and all the iem energies cd[:,:,0] of the 9x9
    jet_sum = tf.reduce_sum(cd[:,:,1], axis=1, keepdims=True) + tf.reduce_sum(cd[:,:,0], axis=1, keepdims=True)
    # for each entry of jet, apply sigmoid cut on the sum at jetThr (50): if jet_sum > 50 jet_sum_passing = 1, else 0
    jet_sum_passing = threshold_relaxation_sigmoid(jet_sum, jetThr, 10.)
    # compute the number of jets passing both selections
    jet_passing = tf.reduce_sum(jet_seed_passing * jet_sum_passing, keepdims=False)
    # print("### INFO: " + str(jet_passing) + " / " + str(cd.shape[0]) + " = " + str(jet_passing/cd.shape[0]))

    return jet_passing / cd.shape[0]

def RateProxyEGs (cd, egThr):

    egThr = egThr - 0.1

    # predict eg energy and apply threshold: sum all the iem energies cd[:,:,1] of the 9x9
    eg_sum = tf.reduce_sum(cd[:,:,1], axis=1, keepdims=True) + tf.reduce_sum(cd[:,:,0], axis=1, keepdims=True)
    # for each entry of eg, apply sigmoid cut on the sum at egThr (10): if eg_sum > 10 eg_sum_passing = 1, else 0
    eg_sum_passing = threshold_relaxation_sigmoid(eg_sum, egThr, 10.)
    # compute the number of jets passing both selections
    eg_passing = tf.reduce_sum(eg_sum_passing, keepdims=False)
    # print("### INFO: " + str(jet_passing) + " / " + str(cd.shape[0]) + " = " + str(jet_passing/cd.shape[0]))
    return eg_passing / cd.shape[0]

# python3 TargetRateProxy.py --indir 2023_06_08_NtuplesV50/JetMET_PuppiJet_Barrel_Pt30_HoTot95 --v HCAL --tag DataReco

##############################################################################
################################## MAIN BODY #################################
##############################################################################

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--indir",    dest="indir",    help="Input folder with TFRecords",                    default=None  )
parser.add_option("--v",        dest="v",        help="Which training to perform: ECAL or HCAL?",       default=None  )
parser.add_option("--tag",      dest="tag",      help="Tag of the training folder",                     default=""    )
(options, args) = parser.parse_args()

indir = '/data_CMS/cms/motta/CaloL1calibraton/' + options.indir + '/' + options.v + 'training' + options.tag
if options.v == 'ECAL':                      batch_size = 150
if options.v == 'HCAL' or options.v == 'HF': batch_size = 500

# read raw rate dataset and parse it 
print('\n ### Reading TF records from: ' + indir + '/rateTFRecords/record_*.tfrecord')
InTrainRecords = glob.glob(indir+'/rateTFRecords/record_*.tfrecord')
raw_train_dataset = tf.data.TFRecordDataset(InTrainRecords)
train_dataset = raw_train_dataset.map(parse_function)
train_dataset = train_dataset.batch(batch_size, drop_remainder=True)
del InTrainRecords, raw_train_dataset

num_batches = 0
if options.v == 'HCAL' or options.v == 'HF':
    thr_list = np.arange(30,100) # GeV
    rate_list = np.zeros(len(thr_list))
if options.v == 'ECAL':
    thr_list = np.arange(10,50) # GeV
    rate_list = np.zeros(len(thr_list))

# remember the thresholds are in HW units!)
for train_batch in train_dataset:
    if not num_batches%100: print('at batch', num_batches)
    num_batches += 1
    cd, _ = train_batch
    if options.v == 'HCAL' or options.v == 'HF':
        for i, thr in enumerate(thr_list):
            rate_list[i] += float(RateProxyJets(cd, 8, 2*thr))

    if options.v == 'ECAL':
        for i, thr in enumerate(thr_list):
            rate_list[i] += float(RateProxyEGs(cd, 2*thr))    

# if options.v == 'HCAL' or options.v == 'HF':
#     for i, thr in enumerate(thr_list):
#         print("### INFO: Compute percentage of jets passing seed at 4 GeV & sum > "+str(thr)+" GeV : ", rate_list[i]/num_batches)

# if options.v == 'ECAL':
#     for i, thr in enumerate(thr_list):
#         print("### INFO: Compute percentage of jets passing sum > "+str(thr)+" GeV : ", rate_list[i]/num_batches)

odir = '/data_CMS/cms/motta/CaloL1calibraton/' + options.indir + '/' + options.v + 'training' + options.tag + '/InputPlots/RateProxy'
os.system('mkdir -p '+ odir)
json_path = odir + '/rate_proxy.json'

data = {float(thr): float(rate/num_batches) for thr, rate in zip(thr_list, rate_list)}

json_data = json.dumps(data, indent=2)
with open(json_path, "w") as json_file:
    json_file.write(json_data)

fig = plt.figure(figsize = [10,10])
plt.plot(thr_list, rate_list/num_batches, marker='o', linestyle='dashed', linewidth=2)
plt.xlabel(r'$p_{T}^{jet, offline} [GeV]$')
plt.ylabel('Rate Proxy')
plt.grid(linestyle='dotted')
plt.legend(fontsize=15, loc='lower right')
plt.savefig(odir + '/rate_proxy.png')
plt.close() 