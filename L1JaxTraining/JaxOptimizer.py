#!/usr/bin/env python

import jax.numpy as jnp
from jax.scipy import optimize
import numpy as np
from optparse import OptionParser
from jax import grad, jacobian
import matplotlib.pyplot as plt
import glob, os, json

#######################################################################
######################### SCRIPT BODY #################################
#######################################################################

# python3 JaxOptimizer.py --filesLim 1 --odir test

if __name__ == "__main__" :

    parser = OptionParser()
    parser.add_option("--odir",                   dest="odir",                   default="./",                         help="Output tag of the output folder")
    parser.add_option("--v",                      dest="v",                      default="HCAL",                       help="Calibration target (ECAL, HCAL)")
    parser.add_option("--jetsLim",                dest="jetsLim",                default=None,       type=int,         help="Fix the total amount of jets to be used")
    parser.add_option("--filesLim",               dest="filesLim",               default=None,       type=int,         help="Maximum number of npz files to use")
    parser.add_option("--bs",                     dest="bs",                     default=1,          type=int,         help="Batch size")
    parser.add_option("--lr",                     dest="lr",                     default=0.001,      type=float,       help="Learning rate")
    parser.add_option("--ep",                     dest="ep",                     default=5,          type=int,         help="Number of epochs")
    parser.add_option("--mask",                   dest="mask",                   default=False,   action='store_true', help="Mask low energy SFs")
    (options, args) = parser.parse_args()
    print(options)

    #######################################################################
    ## READING INPUT
    #######################################################################

    indir = '/data_CMS/cms/motta/CaloL1calibraton/2023_12_13_NtuplesV56/Input2/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot70/GoodNtuples/tensors'
    odir = options.odir
    os.system('mkdir -p '+ odir)

    list_towers_files = glob.glob(indir + "/towers_*.npz")
    list_jets_files = glob.glob(indir + "/jets_*.npz")

    towers = jnp.load(list_towers_files[0], allow_pickle=True)['arr_0']
    jets = jnp.load(list_jets_files[0], allow_pickle=True)['arr_0']

    list_train_towers = []
    list_train_jets = []
    training_stat = 0

    list_test_towers = []
    list_test_jets = []
    testing_stat = 0

    testing_fraction = 0.1
    end_file = 0
    print(" ### INFO: Loading files: testing fraction = {:.1f}%".format(testing_fraction*100))

    # Limiting the number of files
    if options.filesLim:
        for ifile in range(0, options.filesLim):
            # print("Reading file {}".format(ifile))
            x = jnp.load(list_towers_files[ifile], allow_pickle=True)['arr_0']
            y = jnp.load(list_jets_files[ifile], allow_pickle=True)['arr_0']
            list_train_towers.append(x)
            list_train_jets.append(y)
            training_stat += len(y)
            end_file = ifile
        testLim = testing_fraction*training_stat
        for ifile in range(end_file, len(list_towers_files)):
            x = jnp.load(list_towers_files[ifile], allow_pickle=True)['arr_0']
            y = jnp.load(list_jets_files[ifile], allow_pickle=True)['arr_0']            
            if testing_stat + len(y) > testLim:
                stop = testLim - training_stat
                list_test_towers.append(x[:stop])
                list_test_jets.append(y[:stop])
                break
            else:
                list_test_towers.append(x)
                list_test_jets.append(y)
                testing_stat += len(y)

    # Limiting the number of jets
    elif options.jetsLim:
        training_stat = 0
        for ifile in range(0, len(list_towers_files)):
            # print("Reading file {}, {}".format(ifile, training_stat))
            x = jnp.load(list_towers_files[ifile], allow_pickle=True)['arr_0']
            y = jnp.load(list_jets_files[ifile], allow_pickle=True)['arr_0']
            if training_stat + len(y) > options.jetsLim:
                stop = options.jetsLim - training_stat
                list_train_towers.append(x[:stop])
                list_train_jets.append(y[:stop])
                end_file = ifile
                break
            else:
                list_train_towers.append(x)
                list_train_jets.append(y)
                training_stat += len(y)
        testLim = int(testing_fraction*options.jetsLim)
        for ifile in range(end_file, len(list_towers_files)):
            x = jnp.load(list_towers_files[ifile], allow_pickle=True)['arr_0']
            y = jnp.load(list_jets_files[ifile], allow_pickle=True)['arr_0']            
            if testing_stat + len(y) > testLim:
                stop = testLim - testing_stat
                list_test_towers.append(x[:stop])
                list_test_jets.append(y[:stop])
                break
            else:
                list_test_towers.append(x)
                list_test_jets.append(y)
                testing_stat += len(y)

    # No limitation
    else:
        for ifile in range(0, int((1-testing_fraction)*len(list_towers_files))):
            print("Reading training file {}".format(ifile))
            x = jnp.load(list_towers_files[ifile], allow_pickle=True)['arr_0']
            y = jnp.load(list_jets_files[ifile], allow_pickle=True)['arr_0']
            list_train_towers.append(x)
            list_train_jets.append(y)
            training_stat += len(y)
        for ifile in range(int((1-testing_fraction)*len(list_towers_files)), len(list_towers_files)):
            print("Reading testing file {}".format(ifile))
            x = jnp.load(list_towers_files[ifile], allow_pickle=True)['arr_0']
            y = jnp.load(list_jets_files[ifile], allow_pickle=True)['arr_0']
            list_test_towers.append(x)
            list_test_jets.append(y)
            testing_stat += len(y)

    towers = jnp.concatenate(list_train_towers)
    jets = jnp.concatenate(list_train_jets)
    # print(len(towers), len(jets))

    test_towers = jnp.concatenate(list_test_towers)
    test_jets = jnp.concatenate(list_test_jets)
    # print(len(test_towers), len(test_jets))

    print(" ### INFO: Training on {} jets".format(len(jets)))
    print(" ### INFO: Testing on {} jets".format(len(test_jets)))

    #######################################################################
    ## INITIALIZING SCALE FACTORS
    #######################################################################

    eta_binning = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
    # et_binning  = [i for i in range(1,101)]
    et_binning  = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 256]
    eta_binning = jnp.array(eta_binning)
    et_binning = jnp.array(et_binning) + 0.1 # this shift allows to have et = 1 in the first bin
    print(" ### INFO: Eta binning = ", eta_binning)
    print(" ### INFO: Energy binning = ", et_binning)

    SFs = jnp.ones(shape=(len(eta_binning),len(et_binning)))
    # Apply ZS to ieta <= 15 and iet == 1
    SFs = jnp.where((eta_binning[:, None] <= 15) & (et_binning[None, :] == 1 + 0.1), 0, SFs)
    SFs_flat = SFs.ravel()
    print(" ### INFO: Zero Suppression applied to ieta <= 15, et == 1")

    mask = jnp.ones(shape=(len(eta_binning),len(et_binning)))
    if options.mask:
        mask_energy = 8 + 0.1
        mask = jnp.where(jnp.array(et_binning) <= mask_energy, 0, mask)
        print(" ### INFO: Masking applied to et < {}".format(mask_energy))
    mask = mask.ravel()

    # Samples for training
    ietas = jnp.argmax(towers[:, :, 3: ], axis=2) + 1
    ietas_index = jnp.argmax(towers[:, :, 3: ], axis=2)

    ihad = towers[:, :, 1]
    iem = towers[:, :, 0]
    ihad_index = np.digitize(ihad, et_binning)

    # Samples for testing
    test_ietas = jnp.argmax(test_towers[:, :, 3: ], axis=2) + 1
    test_ietas_index = jnp.argmax(test_towers[:, :, 3: ], axis=2)

    test_ihad = test_towers[:, :, 1]
    test_iem = test_towers[:, :, 0]
    test_ihad_index = np.digitize(test_ihad, et_binning)

    # Normalization by number of towers
    hist_eta_binning = jnp.append(0,eta_binning)
    hist_et_binning = jnp.append(0.1,et_binning)
    hist, xedges, yedges = jnp.histogram2d(ietas_index.ravel(), ihad.ravel(), bins=[hist_eta_binning, hist_et_binning])
    norm_batch_stat = np.where(hist==0, 1, hist/np.sum(hist)*100)
    norm_batch_stat = norm_batch_stat.ravel()

    #######################################################################
    ## DEFINING LOSS FUNCTION
    #######################################################################

    def LossFunction(ietas_index, ihad_index, ihad, iem, jets, SFs):
    
        l_eta = len(eta_binning)
        l_et = len(et_binning)
        SFs = SFs.reshape(l_eta,l_et)

        jet_energies = jets[:,3]
        l1_jet_energies = jnp.zeros_like(jet_energies)

        ihad_flat = ihad.flatten()
        ietas_index_flat = ietas_index.flatten()
        ihad_index_flat = ihad_index.flatten()
        SF_for_these_towers_flat = SFs[ietas_index_flat, ihad_index_flat]
        # [FIXME] This should be rounded down with int
        ihad_calib_flat = jnp.multiply(ihad_flat, SF_for_these_towers_flat)
        ihad_calib = ihad_calib_flat.reshape(len(ihad_index),81)
        l1_jet_energies = jnp.sum(ihad_calib[:], axis=1)
        l1_jet_em_energies = jnp.sum(iem[:], axis=1)

        DIFF = jnp.abs((l1_jet_energies + l1_jet_em_energies) - jet_energies)
        # DIFF_2 = jnp.square(DIFF)
        MAPE = jnp.divide(DIFF, jet_energies)
        MAPE_s = jnp.divide(jnp.sum(MAPE), len(ietas_index))
        return MAPE_s

    # test = LossFunction(ietas_index, ihad_index, ihad, iem, jets, SFs_flat)
    # print(test)

    #######################################################################
    ## TRAINING
    #######################################################################

    nb_epochs = options.ep
    bs = options.bs
    lvals = []
    dvals = []
    lr = options.lr

    TrainingInfo = {}
    TrainingInfo["LossType"] = "MAPE"
    TrainingInfo["NJets"] = len(jets)
    TrainingInfo["NEpochs"] = nb_epochs
    TrainingInfo["BS"] = bs
    TrainingInfo["LR"] = lr

    LossHistory = {}
    TestLossHistory = {}
    history_dir = odir + '/History'
    os.system("mkdir -p {}".format(history_dir))

    min_energy = np.min(et_binning)
    max_energy = np.max(et_binning)
    energy_step = 1

    head_text = 'energy bins iEt       = [0'
    for i in et_binning: head_text = head_text + ' ,{}'.format(i)
    head_text = head_text + "]\n"

    head_text = head_text + 'energy bins GeV       = [0'
    for i in et_binning: head_text = head_text + ' ,{}'.format(i/2)
    head_text = head_text + "]\n"

    head_text = head_text + 'energy bins GeV (int) = [0'
    for i in et_binning: head_text = head_text + ' ,{}'.format(int(i/2))
    head_text = head_text + "]\n"

    print(" ### INFO: Start training with LR = {}, EPOCHS = {}".format(lr, nb_epochs))

    for ep in range(nb_epochs):
        print("\n *** Starting Epoch", ep)
        for i in np.arange(0, len(ihad), bs):
            if i == len(ihad) - 1: break
            # calculate the loss
            jac = jacobian(LossFunction, argnums=5)(ietas_index[i:i+bs], ihad_index[i:i+bs], ihad[i:i+bs], iem[i:i+bs], jets[i:i+bs], SFs_flat)
            # apply derivative
            SFs_flat = SFs_flat - lr*jac*mask/norm_batch_stat
            # print loss for each batch
            loss_value = float(np.mean(LossFunction(ietas_index[i:i+bs], ihad_index[i:i+bs], ihad[i:i+bs], iem[i:i+bs], jets[i:i+bs], SFs_flat)))
            if i%1000 == 0: print("Looped over {} jets: Loss = {:.4f}".format(i, loss_value))
        # save loss history
        LossHistory[ep] = float(np.mean(LossFunction(ietas_index, ihad_index, ihad, iem, jets, SFs_flat)))
        TestLossHistory[ep] = float(np.mean(LossFunction(test_ietas_index, test_ihad_index, test_ihad, test_iem, test_jets, SFs_flat)))
        SFs = SFs_flat.reshape(len(eta_binning),len(et_binning))
        SFs_inv = np.transpose(SFs)
        SFOutFile = history_dir+'/ScaleFactors_{}_{}.csv'.format(options.v, ep)
        np.savetxt(SFOutFile, SFs_inv, delimiter=",", newline=',\n', header=head_text, fmt=','.join(['%1.4f']*len(eta_binning)))
        # fill 2D histogram with number of jets for each et-eta bin

    SFs = SFs_flat.reshape(len(eta_binning),len(et_binning))
    SFs_inv = np.transpose(SFs)

    SFOutFile = odir + '/ScaleFactors_{}.csv'.format(options.v)
    np.savetxt(SFOutFile, SFs_inv, delimiter=",", newline=',\n', header=head_text, fmt=','.join(['%1.4f']*len(eta_binning)))
    print('\nScale Factors saved to: {}'.format(SFOutFile))
    # jnp.save(options.odir + 'test', SFs)

    TrainingInfo["TrainLoss"] = LossHistory
    TrainingInfo["TestLoss"] = TestLossHistory
    json_path = odir + '/training.json'
    json_data = json.dumps(TrainingInfo, indent=2)
    with open(json_path, "w") as json_file:
        json_file.write(json_data)

    # SF_for_these_towers_flat = SFs[ietas_index_flat, ihad_index_flat]