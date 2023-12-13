from sklearn.model_selection import train_test_split
from optparse import OptionParser
from tensorflow import keras
from TowerGeometry import *
import tensorflow as tf
import pandas as pd
import numpy as np
import zipfile
import pickle
import glob
import sys
import os

sys.path.insert(0,'..')
from L1Training.NNModel_RegAndRate import Fgrad

# split list l in sublists of length n each
def splitInBlocks (l, n):
    r = len(l) % n

    i = 0
    blocks = []
    while i < len(l):
        if len(blocks)<r:
            blocks.append(l[i:i+n+1])
            i += n+1
        else:
            blocks.append(l[i:i+n])
            i += n

    return blocks

# convert training sample to have correct shape and order of tensor entries
def convert_train_samples(X, Y, version):
    # Y vector columns: jetPt, jetEta, jetPhi, trainingPt
    # keep only the trainingPt
    Y = Y[:,3]

    # X vector columns: iem, ihad, iesum, ieta
    if version == 'ECAL':
        X = np.delete(X, 2, axis=2) # delete iesum column (always start deleting from right columns)
        X[:,:,[0,1]] = X[:,:,[1,0]] # order iem and ihad to have iem on the right

    elif version == 'HCAL' or version == 'HF':
        X = np.delete(X, 2, axis=2) # delete iesum column (always start deleting from right columns)
        
    return X, Y

# convert rate sample to have correct shape and order of tensor entries
def convert_rate_samples(Z, version):
    # Z vector columns: iem, ihad, iesum, ieta
    if version == 'ECAL':
        Z = np.delete(Z, 2, axis=2) # delete iesum column (always start deleting from right columns)
        # print(len(Z))
        # Z = Z[ np.sum(Z[:,:,0], axis=1) >= 29 ] # remove EGAMMAs that have iEM<=29 : 29 = (50-(50*0.12))/1.5 = (egThr-(egThr*hoeThrEB))/bigSF
        # the cut at 15 GeV is already defined in the clustering and uses the offline JetPt information
        Z[:,[0,1]] = Z[:,[1,0]] # order iem and ihad to have iem on the right
        # print(len(Z))

    elif version == 'HCAL' or version == 'HF':
        Z = Z[ np.sum(Z[:,:,2], axis=1) >= 50 ] # remove JETs that have E<=50 : 50 ~ (100/n)/1.66*n = (jetThr/nActiveTT)/bigSF*nActiveTT
        Z = np.delete(Z, 2, axis=2) # delete iesum column (always start deleting from right columns)

    return Z

# application of ECAL calibration to the HCAL rate proxy samples
def applyECALcalib(Z, TTP):
    xDim = Z.shape[0] ; yDim = 81 ; zDim = 42
    Z = Z.reshape(xDim*yDim, zDim) # reshape so that every TT becomes an event
    Z[:,[0,1]] = Z[:,[1,0]] # order iem and ihad to have the needed one on the right
    TT_em_pred = TTP.predict(Z[:,1:], batch_size=2048)
    Z[:,[0,1]] = Z[:,[1,0]] # order iem and ihad to have the needed one on the right
    Z[:,[0]] = TT_em_pred
    Z = Z.reshape(xDim, yDim, zDim) # reshape so that 81xTT becomes an event again
    return Z

# application of HCAL calibration to the ECAL rate proxy samples
def applyHCALcalib(Z, TTP):
    Z[:,[0,1]] = Z[:,[1,0]] # order iem and ihad to have the needed one on the right
    TT_had_pred = TTP.predict(Z[:,1:], batch_size=2048)
    Z[:,[0,1]] = Z[:,[1,0]] # order iem and ihad to have the needed one on the right
    Z[:,[0]] = TT_had_pred
    return Z

# tf.train.example serialization function to store in TFRecord
def serialize_example(x, y):
    # create feature dictionary
    feature = {
      'chuncky_donut': tf.train.Feature(bytes_list=tf.train.BytesList(value=[tf.io.serialize_tensor(x).numpy()])),
      'trainingPt'   : tf.train.Feature(float_list=tf.train.FloatList(value=[y]))
    }

    # create example protocol buffer
    example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
    return example_proto.SerializeToString()

# dataset serialization function to store in TFRecord
def tf_serialize_example(x, y):
    tf_string = tf.py_function( serialize_example, (x, y), tf.string )
    return tf.reshape(tf_string, ()) # The result is a scalar.

#######################################################################
######################### SCRIPT BODY #################################
#######################################################################

if __name__ == "__main__" :

    # read the batched input tensors to the NN and merge them
    parser = OptionParser()
    parser.add_option("--indir",                  dest="indir",                  default=None,                         help="Base-folder with files to be merged")
    parser.add_option("--batchdir",               dest="batchdir",               default=None,                         help="Sub-folder with npz files to be merged")
    parser.add_option("--ratedir",                dest="ratedir",                default=None,                         help="Sub-folder with npz files for the rate")
    parser.add_option("--odir",                   dest="odir",                   default=None,                         help="Output tag of the output folder")
    parser.add_option("--v",                      dest="v",                      default=None,                         help="Ntuple type (ECAL, HCAL, or HF)")
    parser.add_option("--rate_only",              dest="rate_only",              default=0,       type=int,            help="Make only rate datasets to reach this stats value")
    parser.add_option("--fix_stats",              dest="fix_stats",              default=0,       type=int,            help="Fix the total amount of jets to be used")
    parser.add_option("--filesLim",               dest="filesLim",               default=1000000, type=int,            help="Maximum number of npz files to use")
    parser.add_option("--filesPerRecord",         dest="filesPerRecord",         default=500,     type=int,            help="Maximum number of npz files per TFRecord")
    parser.add_option("--validation_split",       dest="validation_split",       default=0.20,    type=float,          help="Fraction of events to be used for testing")
    parser.add_option("--flattenEtaDistribution", dest="flattenEtaDistribution", default=False,   action='store_true', help="Flatten eta distribution")
    parser.add_option("--ECALcalib4rate",         dest="ECALcalib4rate",         default=None,                         help="Model for ECAL calibration in HCAL rate proxy dataset ('/data_CMS/cms/motta/CaloL1calibraton/'+options.ECALcalib4rate+'/model_ECAL/TTP')")
    parser.add_option("--HCALcalib4rate",         dest="HCALcalib4rate",         default=None,                         help="Model for HCAL calibration in ECAL rate proxy dataset ('/data_CMS/cms/motta/CaloL1calibraton/'+options.HCALcalib4rate+'/model_HCAL/TTP')")
    parser.add_option("--ljetPtcut",              dest="ljetPtcut",              default=None,                         help="Lower jet pt cut (in iET units)")
    parser.add_option("--ujetPtcut",              dest="ujetPtcut",              default=None,                         help="Upper jet pt cut (in iET units)")
    parser.add_option("--selectResp",             dest="selectResp",             default=False,   action='store_true', help="Apply selections about uncalib response")
    parser.add_option("--noRate",                 dest="noRate",                 default=False,   action='store_true', help="Do only Train and Test")
    (options, args) = parser.parse_args()
    print(options)

    filedir = '/data_CMS/cms/motta/CaloL1calibraton/'+options.indir
    training_folder = filedir + '/{0}training{1}'.format(options.v, options.odir)
    os.system('mkdir -p ' + training_folder + '/trainTFRecords/')
    os.system('mkdir -p ' + training_folder + '/testTFRecords/')
    os.system('mkdir -p ' + training_folder + '/rateTFRecords/')

    if not options.rate_only:
        # read inputs and split them in blocks
        InFilesTrain = glob.glob(filedir+'/'+options.batchdir+'/tensors/towers_*.npz')
        InFilesTrainBlocks = splitInBlocks(InFilesTrain, options.filesPerRecord)

    if not options.noRate:
        if not os.path.isdir(options.ratedir): sys.exit(" ### ERROR: Rate directory not existing")
        InFilesRate = glob.glob(options.ratedir+'/tensors/towers_*.npz')
        InFilesRateBlocks = splitInBlocks(InFilesRate, options.filesPerRecord)

    with tf.device('/CPU:0'):
        if not options.rate_only:
            print('********************************************')
            print('********************************************')
            print('CREATING TRAIN/TEST TFRecords')

            print('\nUsing', len(InFilesTrain), 'files batched in', len(InFilesTrainBlocks), 'blocks\n')

            train_total_dimension = 0
            test_total_dimension = 0

            stats = 0

            # for each block create a TFRecordDataset
            for blockIdx, block in enumerate(InFilesTrainBlocks):

                if options.fix_stats != 0:
                    if stats >= options.fix_stats:
                        break

                print('--------------------------------------')
                print('reading block', blockIdx)
                XsToConcatenate = []
                YsToConcatenate = []

                for fileIdx, file in enumerate(block):

                    if options.fix_stats != 0:
                        if stats >= options.fix_stats:
                            break

                    if not fileIdx%10: print('    reading batch', fileIdx)
                    try:
                        # filex: n_ev * 81 * 43 [iem, ihad, iesum, one hot encoding]
                        filex = np.load(file, allow_pickle=True)['arr_0']
                        # filex: n_ev * 4 [jetPt, jetEta, jetPhi, targetPt]
                        filey = np.load(file.replace('towers_', 'jets_'), allow_pickle=True)['arr_0']

                    except FileNotFoundError:
                        print('** INFO: file idx '+str(fileIdx)+' not found --> skipping')
                        continue
                    except pickle.UnpicklingError:
                        print('** INFO: file idx '+str(fileIdx)+' unpickling error --> skipping')
                        continue
                    except zipfile.BadZipFile:
                        print('** INFO: file idx '+str(fileIdx)+' unzipping error --> skipping')
                        continue
                    except OSError:
                        print('** INFO: file idx '+str(fileIdx)+' Failed to interpret file as a pickle --> skipping')
                        continue
                    if filex.shape[1:] != (81,43) or filey.shape[1:] != (4,):
                        print('** INFO: file idx '+str(fileIdx)+' corrupted --> skipping')
                        continue

                    # Apply cuts
                    def CheckResponse(filex, filey):
                        L1Energy = np.sum(filex[:,:,2], axis=1)
                        JetEnergy = filey[:,3]
                        Response = L1Energy / JetEnergy
                        sel = (Response < 3) & (Response > 0.3)
                        return filex[sel], filey[sel]

                    def ApplyPtCuts(filex, filey, ljetPtcut = None, ujetPtcut = None):
                        JetEnergy = filey[:,0]
                        if ljetPtcut:
                            sel = JetEnergy > float(ljetPtcut)
                            filex = filex[sel]
                            filey = filey[sel]
                        if ujetPtcut:
                            sel = JetEnergy < float(ljetPtcut)
                            filex = filex[sel]
                            filey = filey[sel]
                        return filex, filey

                    if options.selectResp: filex, filey = CheckResponse(filex, filey)
                    if options.ljetPtcut or options.ujetPtcut: filex, filey = ApplyPtCuts(filex, filey, options.ljetPtcut, options.ujetPtcut)

                    if options.fix_stats != 0:
                        if stats + len(filey) >= int(options.fix_stats):
                            # only add number of events missing to reach the fixed stats
                            stop = options.fix_stats - stats
                            filex = filex[:stop]
                            filey = filey[:stop]

                    XsToConcatenate.append(filex)
                    YsToConcatenate.append(filey)

                    stats += len(filey)

                X = np.concatenate(XsToConcatenate)
                Y = np.concatenate(YsToConcatenate)
                del XsToConcatenate, YsToConcatenate

                # pre-process to have correct shape and entires
                X, Y = convert_train_samples(X, Y, options.v)

                ## DEBUG
                # print('    block dimensions', len(X))
                # print('    block dimensions', len(Y))

                # split train and testing
                x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=options.validation_split, random_state=7)
                del X, Y

                # update total dimension
                train_total_dimension += len(y_train)
                test_total_dimension += len(y_test)

                # make tensorflow datasets
                Xtrain = tf.convert_to_tensor(x_train, dtype=tf.float32)
                Ytrain = tf.convert_to_tensor(y_train, dtype=tf.float32)
                del  x_train, y_train
                train_dataset = tf.data.Dataset.from_tensor_slices((Xtrain, Ytrain))
                del Xtrain, Ytrain

                Xtest  = tf.convert_to_tensor(x_test, dtype=tf.float32)
                Ytest  = tf.convert_to_tensor(y_test, dtype=tf.float32)
                del x_test, y_test
                test_dataset  = tf.data.Dataset.from_tensor_slices((Xtest, Ytest))
                del Xtest, Ytest

                # serialize the datasets
                serialized_train_dataset = train_dataset.map(tf_serialize_example)
                serialized_test_dataset  = test_dataset.map(tf_serialize_example)
                del train_dataset, test_dataset

                # store TFRecords
                train_filename = training_folder+'/trainTFRecords/record_'+str(blockIdx)+'.tfrecord'
                train_writer = tf.data.experimental.TFRecordWriter(train_filename)
                train_writer.write(serialized_train_dataset)
                del serialized_train_dataset

                test_filename  = training_folder+'/testTFRecords/record_'+str(blockIdx)+'.tfrecord'
                test_writer = tf.data.experimental.TFRecordWriter(test_filename)
                test_writer.write(serialized_test_dataset)
                del serialized_test_dataset

            print('')
            print(' ### INFO: Total statistics =', stats)
            print(' ### INFO: Training sample total domension =', train_total_dimension)
            print(' ### INFO: Testint sample total domension =', test_total_dimension)

        ################################################################################
        ################################################################################
        ################################################################################

        if not options.noRate:
            print('********************************************')
            print('********************************************')
            print('CREATING RATE TFRecords')

            print('\nUsing', len(InFilesRate), 'files batched in', len(InFilesRateBlocks), 'blocks\n')

            if options.rate_only: train_total_dimension = options.rate_only
            rate_dimensions = []

            stats = 0

            # for each block create a TFRecordDataset
            for blockIdx, block in enumerate(InFilesRateBlocks):

                if stats >= train_total_dimension:
                    break

                print('--------------------------------------')
                print('reading block', blockIdx)
                ZsToConcatenate = []

                for fileIdx, file in enumerate(block):

                    if stats >= train_total_dimension:
                        break

                    if not fileIdx%10: print('    reading batch', fileIdx)
                    try:
                        filex = np.load(file, allow_pickle=True)['arr_0']

                    except FileNotFoundError:
                        print('** INFO: file idx '+str(fileIdx)+' not found --> skipping')
                        continue
                    except pickle.UnpicklingError:
                        print('** INFO: file idx '+str(fileIdx)+' unpickling error --> skipping')
                        continue
                    except zipfile.BadZipFile:
                        print('** INFO: file idx '+str(fileIdx)+' unzipping error --> skipping')
                        continue
                    except OSError:
                        print('** INFO: file idx '+str(fileIdx)+' Failed to interpret file as a pickle --> skipping')
                        continue
                    if filex.shape[1:] != (81,43):
                        print('** INFO: file idx '+str(fileIdx)+' corrupted --> skipping')
                        continue

                    if stats + len(filex) >= train_total_dimension:
                        # only add number of events missing to reach the fixed stats
                        stop = train_total_dimension - stats
                        filex = filex[:stop]

                    ZsToConcatenate.append(filex)

                    stats += len(filex)

                Z = np.concatenate(ZsToConcatenate)
                del ZsToConcatenate

                # pre-process to have correct shape and entires
                Z = convert_rate_samples(Z, options.v)
                _ = np.zeros(len(Z))

                if options.ECALcalib4rate and options.v == 'HCAL':
                    ECAL_TTPmodel = keras.models.load_model('/data_CMS/cms/motta/CaloL1calibraton/'+options.ECALcalib4rate+'/model_ECAL/TTP', compile=False, custom_objects={'Fgrad': Fgrad})
                    Z = applyECALcalib(Z, ECAL_TTPmodel)
                    del ECAL_TTPmodel

                if options.HCALcalib4rate and options.v == 'ECAL':
                    HCAL_TTPmodel = keras.models.load_model('/data_CMS/cms/motta/CaloL1calibraton/'+options.HCALcalib4rate+'/model_HCAL/TTP', compile=False, custom_objects={'Fgrad': Fgrad})
                    Z = applyHCALcalib(Z, HCAL_TTPmodel)
                    del HCAL_TTPmodel

                ## DEBUG
                rate_dimensions.append(len(Z))
                # print('    block dimensions', len(Z))

                # make tensorflow datasets
                Z = tf.convert_to_tensor(Z, dtype=tf.float32)
                _ = tf.convert_to_tensor(_, dtype=tf.float32)
                rate_dataset = tf.data.Dataset.from_tensor_slices((Z, _))
                del Z, _

                # serialize the datasets
                serialized_rate_dataset = rate_dataset.map(tf_serialize_example)
                del rate_dataset

                # store TFRecords
                rate_filename = training_folder+'/rateTFRecords/record_'+str(blockIdx)+'.tfrecord'
                rate_writer = tf.data.experimental.TFRecordWriter(rate_filename)
                rate_writer.write(serialized_rate_dataset)
                del serialized_rate_dataset

                # directly break as soon as the dimension is met
                # print(' ### INFO: Total statistics =', stats)

            rate_total_dimension = np.sum(rate_dimensions)
            
            # generally the rate datasets are smaller than the raining datasets therefore we need to 
            # copy the rate TFRecords to have their final dimenion equal to the train sample
            repeatIdx = 0
            records = glob.glob(training_folder+'/rateTFRecords/record_*.tfrecord')
            print('--------------------------------------------')
            while stats < train_total_dimension:
                repeatIdx += 1
                print('Copying rate datasets '+str(repeatIdx)+'th time')
                for record, recordDim in zip(records, rate_dimensions):
                    recordCopy = record.replace('.tfrecord', '_'+str(repeatIdx)+'.tfrecord')
                    os.system('cp '+record+' '+recordCopy)

                    stats += recordDim
                    # directly break as soon as the dimension is met
                    if stats > train_total_dimension: break

            print('')
            print(' ### INFO: Rate sample total domension =', stats)

