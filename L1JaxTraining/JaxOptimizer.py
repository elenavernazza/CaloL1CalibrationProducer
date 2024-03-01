#!/usr/bin/env python

from sklearn.model_selection import train_test_split
import jax.numpy as jnp
from jax.scipy import optimize
import numpy as np
from optparse import OptionParser
from jax import grad, jacobian
import matplotlib.pyplot as plt
import glob, os, json, sys

#######################################################################
######################### SCRIPT BODY #################################
#######################################################################

'''
python3 JaxOptimizer.py --indir 2023_12_13_NtuplesV56/Input2/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot70/GoodNtuples/tensors \
 --odir Trainings/51 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scaleB 0.5

source Instructions/TestsTraining.sh 51
'''

if __name__ == "__main__" :

    parser = OptionParser()
    parser.add_option("--indir",                  dest="indir",                  default=""  ,                         help="Input directory with tensors")
    parser.add_option("--odir",                   dest="odir",                   default="./",                         help="Output tag of the output folder")
    parser.add_option("--v",                      dest="v",                      default="HCAL",                       help="Calibration target (ECAL, HCAL)")
    parser.add_option("--jetsLim",                dest="jetsLim",                default=None,       type=int,         help="Fix the total amount of jets to be used")
    parser.add_option("--filesLim",               dest="filesLim",               default=None,       type=int,         help="Maximum number of npz files to use")
    parser.add_option("--bs",                     dest="bs",                     default=1,          type=int,         help="Batch size")
    parser.add_option("--lr",                     dest="lr",                     default=0.001,      type=float,       help="Learning rate")
    parser.add_option("--ep",                     dest="ep",                     default=5,          type=int,         help="Number of epochs")
    parser.add_option("--mask",                   dest="mask",                   default=False,   action='store_true', help="Mask low energy SFs")
    parser.add_option("--maskHF",                 dest="maskHF",                 default=False,   action='store_true', help="Mask HF for iEt <= 3.5 GeV")
    parser.add_option("--test",                   dest="test",                   default=0.1,        type=float,       help="Testing fraction")
    parser.add_option("--norm",                   dest="norm",                   default=False,   action='store_true', help="Normalize by number of towers in each bin")
    parser.add_option("--scaleF",                 dest="scaleF",                 default=1.,         type=float,       help="Target scale HF")
    parser.add_option("--scaleE",                 dest="scaleE",                 default=1.,         type=float,       help="Target scale Endcap")
    parser.add_option("--scaleB",                 dest="scaleB",                 default=1.,         type=float,       help="Target scale Barrel")
    parser.add_option("--ECALCalib",              dest="ECALCalib",              default=None,       type=str,         help="Path to ECAL SFs on the fly")
    (options, args) = parser.parse_args()
    print(options)

    #######################################################################
    ## READING INPUT
    #######################################################################

    if options.indir == "": sys.exit("Input directory is not specified")
    indir = '/data_CMS/cms/motta/CaloL1calibraton/' + options.indir
    odir = options.odir
    os.system('mkdir -p '+ odir)

    list_towers_files = glob.glob(indir + "/towers_*.npz")
    list_jets_files = glob.glob(indir + "/jets_*.npz")

    list_train_towers = []
    list_train_jets = []
    training_stat = 0

    # Limiting the number of files
    if options.filesLim:
        for ifile in range(0, options.filesLim):
            # print("Reading file {}".format(ifile))
            x = jnp.load(list_towers_files[ifile], allow_pickle=True)['arr_0']
            y = jnp.load(list_jets_files[ifile], allow_pickle=True)['arr_0']
            list_train_towers.append(x)
            list_train_jets.append(y)
            training_stat += len(y)

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
                training_stat += stop
                break
            else:
                list_train_towers.append(x)
                list_train_jets.append(y)
                training_stat += len(y)

    # No limitation
    else:
        for ifile in range(0, len(list_towers_files)):
            print("Reading training file {}".format(ifile))
            x = jnp.load(list_towers_files[ifile], allow_pickle=True)['arr_0']
            y = jnp.load(list_jets_files[ifile], allow_pickle=True)['arr_0']
            list_train_towers.append(x)
            list_train_jets.append(y)
            training_stat += len(y)

    X = jnp.concatenate(list_train_towers)
    Y = jnp.concatenate(list_train_jets)

    print(" ### INFO: Loading files: testing fraction = {:.1f}%".format(options.test*100))
    towers, test_towers, jets, test_jets = train_test_split(X, Y, test_size=options.test, random_state=7)

    print(" ### INFO: Training on {} jets".format(len(jets)))
    print(" ### INFO: Testing on {} jets".format(len(test_jets)))

    #######################################################################
    ## CUT ON UNCALIB RESPONSE
    #######################################################################    

    L1Energy = np.sum(towers[:,:,2], axis=1)
    JetEnergy = jets[:,3]
    Response = L1Energy / JetEnergy
    sel = (Response < 3) & (Response > 0.3)
    towers = towers[sel]
    jets = jets[sel]

    L1Energy = np.sum(test_towers[:,:,2], axis=1)
    JetEnergy = test_jets[:,3]
    Response = L1Energy / JetEnergy
    sel = (Response < 3) & (Response > 0.3)
    test_towers = test_towers[sel]
    test_jets = test_jets[sel]

    #######################################################################
    ## INITIALIZING SCALE FACTORS
    #######################################################################

    if options.v == "HCAL":
        eta_binning = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
        en_binning  = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 256]
    elif options.v == "ECAL":
        eta_binning = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
        en_binning  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 26, 28, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 256]
    # et_binning  = [i for i in range(1,101)]
    eta_binning = jnp.array(eta_binning)
    et_binning = jnp.array(en_binning) + 0.1 # this shift allows to have et = 1 in the first bin
    print(" ### INFO: Eta binning = ", eta_binning)
    print(" ### INFO: Energy binning = ", et_binning)
    l_eta = len(eta_binning)
    l_et = len(et_binning)

    SFs = jnp.ones(shape=(len(eta_binning),len(et_binning)))
    if options.v == 'HCAL':
        # Apply ZS to ieta <= 15 and iet == 1
        SFs = jnp.where((eta_binning[:, None] <= 15) & (et_binning[None, :] == 1 + 0.1), 0, SFs)
        print(" ### INFO: Zero Suppression applied to ieta <= 15, et == 1")
    if options.v == 'ECAL':
        # Apply ZS to 3_6_9 region
        SFs = jnp.where((eta_binning[:, None] == 26) & (et_binning[None, :] <= 6 + 0.1), 0, SFs)
        SFs = jnp.where((eta_binning[:, None] == 27) & (et_binning[None, :] <= 12 + 0.1), 0, SFs)
        SFs = jnp.where((eta_binning[:, None] == 28) & (et_binning[None, :] <= 18 + 0.1), 0, SFs)
        print(" ### INFO: Zero Suppression applied to TT 26 (iEt<=6),27 (iEt<=12), 28 (iEt<=18)")
    if options.maskHF:
        SFs = jnp.where((eta_binning[:, None] > 28) & (et_binning[None, :] <= 7 + 0.1), 0, SFs)
        SFs = jnp.where((eta_binning[:, None] == 28) & (et_binning[None, :] <= 1 + 0.1), 1, SFs)
        print(" ### INFO: Zero Suppression applied HF for iEt <= 3.5 GeV")
    SFs_flat = SFs.ravel()

    mask = jnp.ones(shape=(len(eta_binning),len(et_binning)))
    if options.maskHF:
        mask = jnp.where((eta_binning[:, None] > 28) & (et_binning[None, :] <= 7 + 0.1), 0, mask)
        mask = jnp.where((eta_binning[:, None] == 28) & (et_binning[None, :] <= 1 + 0.1), 0, mask)
        print(" ### INFO: Masking applied HF for iEt <= 3.5 GeV")
    # mask_eta = 28
    # print(" ### INFO: Masking applied to eta > {}".format(mask_eta))
    # eta_binning_reshaped = jnp.expand_dims(eta_binning, axis=1)
    # eta_binning_reshaped = jnp.tile(eta_binning_reshaped, (1, len(et_binning)))
    # mask = jnp.where(eta_binning_reshaped > mask_eta, 0, mask)
    mask = mask.ravel()

    # Samples for training
    ietas = jnp.argmax(towers[:, :, 3: ], axis=2) + 1
    ietas_idx = jnp.argmax(towers[:, :, 3: ], axis=2)

    ihad = towers[:, :, 1]
    iem = towers[:, :, 0]
    ihad_idx = np.digitize(ihad, et_binning)
    iem_idx = np.digitize(iem, et_binning)

    # Samples for testing
    test_ietas = jnp.argmax(test_towers[:, :, 3: ], axis=2) + 1
    test_ietas_idx = jnp.argmax(test_towers[:, :, 3: ], axis=2)

    test_ihad = test_towers[:, :, 1]
    test_iem = test_towers[:, :, 0]
    test_ihad_idx = np.digitize(test_ihad, et_binning)
    test_iem_idx = np.digitize(test_iem, et_binning)

    if options.norm:
        # Normalization by number of towers
        hist_eta_binning = jnp.append(0,eta_binning)
        hist_et_binning = jnp.append(0.1,et_binning)
        if options.v == 'HCAL':
            hist, xedges, yedges = jnp.histogram2d(ietas_idx.ravel(), ihad.ravel(), bins=[hist_eta_binning, hist_et_binning])
        elif options.v == 'ECAL':
            hist, xedges, yedges = jnp.histogram2d(ietas_idx.ravel(), iem.ravel(), bins=[hist_eta_binning, hist_et_binning])
        norm_batch_stat = np.where(hist==0, 1, hist/np.sum(hist)*100)
        norm_batch_stat = norm_batch_stat.ravel()
    else:
        norm_batch_stat = jnp.ones(shape=(len(eta_binning),len(et_binning))).ravel()

    #######################################################################
    ## DEFINING LOSS FUNCTION
    #######################################################################

    def ComputeResponse(ietas_idx, ihad_idx, ihad, iem, jets, SFs):
    
        l_eta = len(eta_binning)
        l_et = len(et_binning)
        SFs = SFs.reshape(l_eta,l_et)

        jet_energies = jets[:,3]
        l1_jet_energies = jnp.zeros_like(jet_energies)

        ihad_flat = ihad.flatten()
        ietas_idx_flat = ietas_idx.flatten()
        ihad_idx_flat = ihad_idx.flatten()
        SF_for_these_towers_flat = SFs[ietas_idx_flat, ihad_idx_flat]
        ihad_calib_flat = jnp.multiply(ihad_flat, SF_for_these_towers_flat)
        ihad_calib = ihad_calib_flat.reshape(len(ihad_idx),81)
        l1_jet_energies = jnp.sum(ihad_calib[:], axis=1)
        l1_jet_em_energies = jnp.sum(iem[:], axis=1)

        if options.v == "HCAL":
            return jnp.divide((l1_jet_energies + l1_jet_em_energies), jet_energies)
        elif options.v == "ECAL":
            return jnp.divide((l1_jet_energies), jet_energies)

    def LossFunction(ietas_idx, ihad_idx, ihad, iem, jets, SFs):
    
        l_eta = len(eta_binning)
        l_et = len(et_binning)
        SFs = SFs.reshape(l_eta,l_et)

        jet_energies = jets[:,3]
        l1_jet_energies = jnp.zeros_like(jet_energies)

        ihad_flat = ihad.flatten()
        ietas_idx_flat = ietas_idx.flatten()
        ihad_idx_flat = ihad_idx.flatten()
        SF_for_these_towers_flat = SFs[ietas_idx_flat, ihad_idx_flat]
        # [FIXME] This should be rounded down with int
        ihad_calib_flat = jnp.multiply(ihad_flat, SF_for_these_towers_flat)
        ihad_calib = ihad_calib_flat.reshape(len(ihad_idx),81)
        l1_jet_energies = jnp.sum(ihad_calib[:], axis=1)
        l1_jet_em_energies = jnp.sum(iem[:], axis=1)

        if options.v == "HCAL":
            scale = options.scaleB * (jets[:,1] < 1.305) + options.scaleE * ((jets[:,1] >= 1.305) & (jets[:,1] < 3)) + options.scaleF * (jets[:,1] >= 3)
            DIFF = jnp.abs((l1_jet_energies + l1_jet_em_energies) - scale*jet_energies)
        elif options.v == "ECAL":
            scale = options.scaleB * (jets[:,1] < 1.305) + options.scaleE * (jets[:,1] >= 1.305)
            DIFF = jnp.abs((l1_jet_energies) - scale*jet_energies)
        # DIFF_2 = jnp.square(DIFF)
        MAPE = jnp.divide(DIFF, scale*jet_energies)
        MAPE_s = jnp.divide(jnp.sum(MAPE), len(jets))
        return MAPE_s

    def ReadECALScaleFactors(ECAL_SFs_name, cols=28):
        ECAL_SFs = np.loadtxt(open(ECAL_SFs_name, "rb"), delimiter=',', usecols=range(0,cols))
        ECAL_SFs = np.transpose(ECAL_SFs)
        eta_binning = np.arange(1,cols+1)
        with open(ECAL_SFs_name) as f:
            header = f.readline().rstrip()
        header = header.split("[")[1].split("]")[0]
        en_binning = header.split(',')
        en_binning = [float(i) for i in en_binning]
        en_binning = np.array(en_binning)
        return ECAL_SFs, eta_binning, en_binning

    #######################################################################
    ## TRAINING
    #######################################################################

    nb_epochs = options.ep
    bs = options.bs
    lvals = []
    dvals = []
    lr = options.lr

    TrainingInfo = {}
    TrainingInfo["Version"] = options.v
    TrainingInfo["LossType"] = "MAPE"
    TrainingInfo["Target Scale"] = "B={}, E={}, F={}".format(options.scaleB, options.scaleE, options.scaleF)
    TrainingInfo["NJets"] = len(jets)
    TrainingInfo["NEpochs"] = nb_epochs
    TrainingInfo["BS"] = bs
    TrainingInfo["LR"] = lr
    TrainingInfo["TestingFraction"] = options.test
    TrainingInfo["Masking"] = options.mask
    TrainingInfo["Normalization"] = options.norm

    LossHistory = {}
    TestLossHistory = {}
    history_dir = odir + '/History'
    os.system("mkdir -p {}".format(history_dir))

    min_energy = np.min(en_binning)
    max_energy = np.max(en_binning)
    energy_step = 1

    head_text = 'energy bins iEt       = [0'
    for i in en_binning: head_text = head_text + ' ,{}'.format(i)
    head_text = head_text + "]\n"

    head_text = head_text + 'energy bins GeV       = [0'
    for i in en_binning: head_text = head_text + ' ,{}'.format(i/2)
    head_text = head_text + "]\n"

    head_text = head_text + 'energy bins GeV (int) = [0'
    for i in en_binning: head_text = head_text + ' ,{}'.format(int(i/2))
    head_text = head_text + "]\n"

    print(" ### INFO: Start training with LR = {}, EPOCHS = {}".format(lr, nb_epochs))

    if options.v == "HCAL":
        calib_idx = ihad_idx;   test_calib_idx = test_ihad_idx
        calib = ihad;           test_calib = test_ihad

        if options.ECALCalib:
            ECAL_SFs, ECAL_eta_binning, ECAL_en_binning = ReadECALScaleFactors(options.ECALCalib)
            ECAL_et_binning = jnp.array(ECAL_en_binning[:1]) + 0.1

            def CalibrateIem (iem, ietas_idx):
                iem_idx = np.digitize(iem, ECAL_et_binning)
                iem_idx_flat = iem_idx.flatten()
                ietas_idx_flat = ietas_idx.flatten()
                ietas_idx_flat = ietas_idx_flat.at[ietas_idx_flat > 27].set(27)
                iem_flat = iem.flatten()
                SF_for_iem_towers_flat = ECAL_SFs[ietas_idx_flat, iem_idx_flat]
                iem_calib_flat = jnp.multiply(iem_flat, SF_for_iem_towers_flat)
                iem_calib_flat = jnp.floor(iem_calib_flat)
                iem_calib = iem_calib_flat.reshape(len(iem_idx),81)
                return iem_calib
            
            uncalib = CalibrateIem(iem, ietas_idx);     test_uncalib = CalibrateIem(test_iem, test_ietas_idx)
        else:
            uncalib = iem;                              test_uncalib = test_iem
    elif options.v == "ECAL":
        calib_idx = iem_idx;    test_calib_idx = test_iem_idx
        calib = iem;            test_calib = test_iem
        uncalib = ihad;         test_uncalib = test_ihad

    # print(LossFunction(ietas_idx, calib_idx, calib, uncalib, jets, SFs_flat))

    for ep in range(nb_epochs):
        print("\n *** Starting Epoch", ep)
        for i in np.arange(0, len(jets), bs):
            if i == len(jets) - 1: break
            # calculate the loss
            jac = jacobian(LossFunction, argnums=5)(ietas_idx[i:i+bs], calib_idx[i:i+bs], calib[i:i+bs], uncalib[i:i+bs], jets[i:i+bs], SFs_flat)
            # apply derivative
            SFs_flat = SFs_flat - lr*jac*mask/norm_batch_stat
            SFs_flat = jnp.maximum(SFs_flat, 0)
            # print loss for each batch
            loss_value = float(LossFunction(ietas_idx[i:i+bs], calib_idx[i:i+bs], calib[i:i+bs], uncalib[i:i+bs], jets[i:i+bs], SFs_flat))
            if i%1000 == 0: print("Looped over {} jets: Loss = {:.4f}".format(i, loss_value))
        # save loss history
        np.savez(history_dir+"/TrainResp_{}".format(ep), ComputeResponse(ietas_idx, calib_idx, calib, uncalib, jets, SFs_flat))
        LossHistory[ep] = float(LossFunction(ietas_idx, calib_idx, calib, uncalib, jets, SFs_flat))
        np.savez(history_dir+"/TestResp_{}".format(ep), ComputeResponse(test_ietas_idx, test_calib_idx, test_calib, test_uncalib, test_jets, SFs_flat))
        TestLossHistory[ep] = float(LossFunction(test_ietas_idx, test_calib_idx, test_calib, test_uncalib, test_jets, SFs_flat))
        SFs = SFs_flat.reshape(len(eta_binning),len(et_binning))
        SFs_inv = np.transpose(SFs)
        SFOutFile = history_dir+'/ScaleFactors_{}_{}.csv'.format(options.v, ep)
        np.savetxt(SFOutFile, SFs_inv, delimiter=",", newline=',\n', header=head_text, fmt=','.join(['%1.4f']*len(eta_binning)))

    SFs = SFs_flat.reshape(len(eta_binning),len(et_binning))
    SFs_inv = np.transpose(SFs)

    SFOutFile = odir + '/ScaleFactors_{}.csv'.format(options.v)
    np.savetxt(SFOutFile, SFs_inv, delimiter=",", newline=',\n', header=head_text, fmt=','.join(['%1.4f']*len(eta_binning)))
    print('\nScale Factors saved to: {}'.format(SFOutFile))

    TrainingInfo["TrainLoss"] = LossHistory
    TrainingInfo["TestLoss"] = TestLossHistory
    json_path = odir + '/training.json'
    json_data = json.dumps(TrainingInfo, indent=2)
    with open(json_path, "w") as json_file:
        json_file.write(json_data)
