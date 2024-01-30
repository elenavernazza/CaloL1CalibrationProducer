import matplotlib.pyplot as plt
import numpy as np
import sys, glob, os
import pandas as pd
import math, warnings, mplhep
from matplotlib.transforms import ScaledTranslation
plt.style.use(mplhep.style.CMS)
warnings.simplefilter(action='ignore')
from NNModel_RegAndRate_AddEt_4 import *

c_uncalib = 'black'; c_oldcalib = 'red'; c_newcalib = 'green'
leg_uncalib = 'No calib'; leg_oldcalib = 'Old calib'; leg_newcalib = 'New calib'

feature_description = {
    'chuncky_donut': tf.io.FixedLenFeature([], tf.string, default_value=''), # byteslist to be read as string 
    'trainingPt'   : tf.io.FixedLenFeature([], tf.float32, default_value=0)  # single float values
}

# parse proto input based on description
def parse_function(example_proto):
    example = tf.io.parse_single_example(example_proto, feature_description)
    chuncky_donut = tf.io.parse_tensor(example['chuncky_donut'], out_type=tf.float32) # decode byteslist to original 81x43 tensor
    return chuncky_donut, example['trainingPt']

### To run:
### python3 ApplicationPlots_PredictTF.py --indir 2023_12_13_NtuplesV56/Input2/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot70 --v HCAL --tag DataReco --addtag _ScanTest_3

if __name__ == "__main__" :

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--indir",        dest="indir",       help="Input folder with trained model",     default=None)
    parser.add_option("--tag",          dest="tag",         help="tag of the training folder",          default="")
    parser.add_option("--out",          dest="odir",        help="Output folder",                       default=None)
    parser.add_option("--v",            dest="v",           help="Ntuple type ('ECAL' or 'HCAL')",      default='ECAL')
    parser.add_option("--filesLim",     dest="filesLim",    help="Maximum number of npz files to use",  default=1000000, type=int)
    parser.add_option("--eventLim",     dest="eventLim",    help="Maximum number of events to use",     default=None)
    parser.add_option("--addtag",       dest="addtag",      help="Add tag for different trainings",     default="")
    (options, args) = parser.parse_args()
    print(options)

    indir = '/data_CMS/cms/motta/CaloL1calibraton/' + options.indir + '/' + options.v + 'training' + options.tag
    odir = '/data_CMS/cms/motta/CaloL1calibraton/' + options.indir + '/' + options.v + 'training' + options.tag + '/model_' + options.v + options.addtag + '/PredictPlots'
    os.system('mkdir -p '+ odir)

    ######################################################################################
    # READING INPUTS
    ######################################################################################

    print('\n ### Reading TF records from: ' + indir + '/testTFRecords/record_*.tfrecord')
    InTestRecords = glob.glob(indir+'/testTFRecords/record_*.tfrecord')[:options.filesLim]
    dataset = tf.data.TFRecordDataset(InTestRecords)
    batch_size = len(list(dataset))
    parsed_dataset = dataset.map(parse_function)
    data = parsed_dataset.batch(batch_size).as_numpy_iterator().next()
    print('\n ### N events in the dataset: ' + str(len(list(dataset))))

    if options.eventLim:
        print('\n ### Reading {} events'.format(options.eventLim))
        n_events = int(options.eventLim)
        Towers = data[0][:int(options.eventLim)]
        Jets = data[1][:int(options.eventLim)]
    else:
        n_events = len(list(dataset))
        Towers = data[0]
        Jets = data[1]
    del data

    print('\n ### Reading TF records from: ' + indir + '/rateTFRecords/record_*.tfrecord')
    InTestRecords = glob.glob(indir+'/rateTFRecords/record_*.tfrecord')[:options.filesLim]
    dataset = tf.data.TFRecordDataset(InTestRecords)
    batch_size = len(list(dataset))
    parsed_dataset = dataset.map(parse_function)
    data = parsed_dataset.batch(batch_size).as_numpy_iterator().next()
    print('\n ### N events in the dataset: ' + str(len(list(dataset))))

    if options.eventLim:
        print('\n ### Reading {} events'.format(options.eventLim))
        n_events_rate = int(options.eventLim)
        RateTowers = data[0][:n_events_rate]
    else:
        print('\n ### Reading {} events'.format(n_events))
        RateTowers = data[0][:n_events]
    del data

    ######################################################################################
    # APPLYING MODEL
    ######################################################################################
    # There is a difference between applying the model and applying the SFs, 
    # given the energy binning in 2 iEt

    print('\n ### Applying model')
    modeldir = indir + '/model_' + options.v + options.addtag
    model = keras.models.load_model(modeldir + '/model', compile=False, custom_objects={'Fgrad': Fgrad})
    model_output = model.predict([Towers, RateTowers]) # 3 outputs: TTP_output, rate_output, OtherET
    TTP_output  = model_output[0] # iEt
    rate_output = model_output[1] # iEt
    OtherET     = model_output[2] # iEt

    ######################################################################################
    # PLOTTING RATE
    ######################################################################################

    def SetSimpleStyle(x_label, y_label, leg_title=''):
        leg = plt.legend(loc = 'upper right', fontsize=20, title=leg_title, title_fontsize=15)
        leg._legend_box.align = "left"
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(linestyle='dotted')
        mplhep.cms.label(data=False, rlabel='(13.6 TeV)', fontsize=20)
    
    def SaveAndClose(savefile):
        plt.savefig(savefile)
        print(savefile)
        plt.close()       

    rate_iesum = np.sum(RateTowers[:, :, [0, 1]], axis=2) # iEt
    rate_seed  = np.max(rate_iesum, axis=1) # iEt
    rate_et    = np.sum(RateTowers[:, :, 1], axis=1) + np.sum(RateTowers[:, :, 0], axis=1) # iEt
    jetPt_uncalib  = rate_et * (rate_seed > 8) / 2. # GeV
    jetPt_newcalib = rate_output / 2. # GeV

    rate_bins = np.linspace(0,200,101)
    b_center = np.array((rate_bins[:-1] + rate_bins[1:])/2)
    e_uncalib, _   = np.histogram(jetPt_uncalib, bins=rate_bins)
    e_newcalib, _  = np.histogram(jetPt_newcalib, bins=rate_bins)
    rate_uncalib  = np.array([np.sum(e_uncalib[b_center > i])/np.sum(e_uncalib) for i in b_center])
    rate_newcalib = np.array([np.sum(e_newcalib[b_center > i])/np.sum(e_newcalib) for i in b_center])

    thr_un = 40 # GeV

    v_sample = options.v
    fig = plt.figure(figsize = [10,10])
    plt.hist(jetPt_uncalib,  bins=rate_bins, histtype='step', stacked=True, linewidth=2, label=leg_uncalib,  color=c_uncalib)
    plt.hist(jetPt_newcalib, bins=rate_bins, histtype='step', stacked=True, linewidth=2, label=leg_newcalib, color=c_newcalib)
    SetSimpleStyle(r'$p_{T}^{jet, L1} [GeV]$', 'Entries', leg_title='')
    SaveAndClose(odir + '/Rate_PtProgression_{}.png'.format(v_sample))

    fig = plt.figure(figsize = [10,10])
    text_1 = leg_uncalib + ": ProxyRate 40 Gev = {:.4f}".format(np.sum(e_uncalib[b_center > thr_un])/np.sum(e_uncalib))
    plt.plot(b_center, rate_uncalib, label=text_1, marker='o', linestyle='dashed', linewidth=2, color=c_uncalib)
    text_3 = leg_newcalib + ": ProxyRate 40 Gev = {:.4f}".format(np.sum(e_newcalib[b_center > thr_un])/np.sum(e_newcalib))
    plt.plot(b_center, rate_newcalib, label=text_3, marker='o', linestyle='dashed', linewidth=2, color=c_newcalib)
    plt.yscale("log")
    SetSimpleStyle(r'$p_{T}^{jet, L1} [GeV]$', 'Rate Proxy', leg_title='')
    SaveAndClose(odir + '/Rate_Progression_{}.png'.format(v_sample))

    # Compute turn on proxy for fixed rate
    rate_uncalib_fix = rate_uncalib[b_center >= thr_un][0]
    thr_new = b_center[np.argmax(rate_newcalib <= rate_uncalib_fix)]
    print(" ### UNCALIB RATE:  Threshold = {:.2f} ---> Rate Proxy = {:.4f}".format(thr_un, rate_uncalib_fix))
    print(" ### NEWCALIB RATE: Threshold = {:.2f} ---> Rate Proxy = {:.4f}".format(thr_new, rate_uncalib_fix))

    ######################################################################################
    # PLOTTING RESPONSE
    ######################################################################################
    
    ietas = np.argmax(Towers[:, :, 2:], axis=2) + 1
    ieta = ietas[:, 0]

    unCalib  = np.sum(Towers[:, :, 0], axis=1) + np.sum(Towers[:, :, 1], axis=1) / 2. # GeV
    newCalib = (TTP_output + OtherET).reshape(-1) / 2. # GeV
    TargetPt = Jets / 2. # GeV

    unRes  = unCalib/TargetPt
    newRes = newCalib/TargetPt

    bins_res = np.linspace(0,3,240)

    fig = plt.figure(figsize = [10,10])
    text_1 = leg_uncalib+r': ${:.3f}/{:.3f}={:.3f}$'.format(unRes.std(), unRes.mean(), unRes.std()/unRes.mean())
    plt.hist(unRes, bins=bins_res, label=text_1, histtype='step', stacked=True, linewidth=2, color=c_uncalib)
    text_2 = leg_newcalib+r': ${:.3f}/{:.3f}={:.3f}$'.format(newRes.std(), newRes.mean(), newRes.std()/newRes.mean())
    plt.hist(newRes, bins=bins_res, label=text_2, histtype='step', stacked=True, linewidth=2, color=c_newcalib)
    SetSimpleStyle('Response', 'Entries', leg_title='')
    SaveAndClose(odir + '/Response_{}.png'.format(v_sample))

    # ######################################################################################
    # # PLOTTING RESPONSE PTBINS
    # ######################################################################################

    # mean_vs_pt_unc = []
    # res_vs_pt_unc = []
    # mean_vs_pt_new = []
    # res_vs_pt_new = []

    # ptBins = [30, 40, 50, 75, 100, 150, 200, 500]
    # for i in range(len(ptBins)-1):

    #     sel = (TargetPt >= ptBins[i]) & (TargetPt < ptBins[i+1])
    #     fig = plt.figure(figsize=(10,10))
    #     text_1 = leg_uncalib+r': ${:.3f}/{:.3f}={:.3f}$'.format(unRes[sel].std(), unRes[sel].mean(), unRes[sel].std()/unRes[sel].mean())
    #     plt.hist(unRes[sel], bins=bins_res, label=text_1, histtype='step', stacked=True, linewidth=2, color=c_uncalib)
    #     text_2 = leg_newcalib+r': ${:.3f}/{:.3f}={:.3f}$'.format(newRes[sel].std(), newRes[sel].mean(), newRes[sel].std()/newRes[sel].mean())
    #     plt.hist(newRes[sel], bins=bins_res, label=text_2, histtype='step', stacked=True, linewidth=2, color=c_newcalib)
    #     SetSimpleStyle(r'$E_{T}^{jet, L1} / p_{T}^{jet, offline}$', 'Entries', leg_title=str(ptBins[i])+r'$<p_{T}^{jet, offline}<$'+str(ptBins[i+1]))
    #     SaveAndClose(odir + '/Response_{}pt{}_{}.png'.format(ptBins[i],ptBins[i+1],v_sample))

    #     mean_vs_pt_unc.append(unRes[sel].mean())
    #     res_vs_pt_unc.append(unRes[sel].std()/unRes[sel].mean())
    #     mean_vs_pt_new.append(newRes[sel].mean())
    #     res_vs_pt_new.append(newRes[sel].std()/newRes[sel].mean())

    # ffig, ax = plt.subplots(figsize=(10,10))
    # X = [(ptBins[i] + ptBins[i+1])/2 for i in range(len(ptBins)-1)]
    # X_err = [(ptBins[i+1] - ptBins[i])/2 for i in range(len(ptBins)-1)]
    # trans_l = ax.transData + ScaledTranslation(-4/72, 0, fig.dpi_scale_trans)
    # plt.errorbar(X, mean_vs_pt_unc, xerr=X_err, yerr=res_vs_pt_unc, label=leg_uncalib, ls='None', lw=2, marker='o', color=c_uncalib, zorder=0, transform=trans_l)
    # plt.errorbar(X, mean_vs_pt_new, xerr=X_err, yerr=res_vs_pt_new, label=leg_newcalib, ls='None', lw=2, marker='o', color=c_newcalib, zorder=1)
    # SetSimpleStyle(r'$p_{T}^{jet, offline}$', r'$\mu\pm$\sigma', leg_title=str(ptBins[i])+r'$<p_{T}^{jet, offline}<$'+str(ptBins[i+1]))
    # SaveAndClose(odir + '/Resolution_ptBins_{}.png'.format(v_sample))

    # ######################################################################################
    # # PLOTTING RESPONSE ETABINS
    # ######################################################################################

    # mean_vs_ieta_unc = []
    # res_vs_ieta_unc = []
    # mean_vs_ieta_new = []
    # res_vs_ieta_new = []

    # ietaBins = [1, 5, 10, 15, 20, 25, 30]
    # for i in range(len(ietaBins)-1):
    #     sel = (ieta >= ietaBins[i]) & (ieta < ietaBins[i+1])
    #     fig = plt.figure(figsize=(10,10))
    #     text_1 = leg_uncalib+r': ${:.3f}/{:.3f}={:.3f}$'.format(unRes[sel].std(), unRes[sel].mean(), unRes[sel].std()/unRes[sel].mean())
    #     plt.hist(unRes[sel], bins=bins_res, label=text_1, histtype='step', stacked=True, linewidth=2, color=c_uncalib)
    #     text_2 = leg_newcalib+r': ${:.3f}/{:.3f}={:.3f}$'.format(newRes[sel].std(), newRes[sel].mean(), newRes[sel].std()/newRes[sel].mean())
    #     plt.hist(newRes[sel], bins=bins_res, label=text_2, histtype='step', stacked=True, linewidth=2, color=c_newcalib)
    #     SetSimpleStyle(r'$E_{T}^{jet, L1} / p_{T}^{jet, offline}$', 'Entries', leg_title=str(ietaBins[i])+r'$<i\eta^{jet, offline}<$'+str(ietaBins[i+1]))
    #     SaveAndClose(odir + '/Response_{}ieta{}_{}.png'.format(ietaBins[i],ietaBins[i+1],v_sample))

    #     mean_vs_ieta_unc.append(unRes[sel].mean())
    #     res_vs_ieta_unc.append(unRes[sel].std()/unRes[sel].mean())
    #     mean_vs_ieta_new.append(newRes[sel].mean())
    #     res_vs_ieta_new.append(newRes[sel].std()/newRes[sel].mean())

    # fig = plt.figure(figsize = [10,10])
    # X = [(ietaBins[i] + ietaBins[i+1])/2 for i in range(len(ietaBins)-1)]
    # X_err = [(ietaBins[i+1] - ietaBins[i])/2 for i in range(len(ietaBins)-1)]
    # plt.errorbar(X, mean_vs_ieta_unc, xerr=X_err, yerr=res_vs_ieta_unc, label=leg_uncalib, ls='None', lw=2, marker='o', color=c_uncalib, zorder=0)
    # plt.errorbar(X, mean_vs_ieta_new, xerr=X_err, yerr=res_vs_ieta_new, label=leg_newcalib, ls='None', lw=2, marker='o', color=c_newcalib, zorder=0)
    # SetSimpleStyle(r'$i\eta^{jet, offline}$', r'$\mu\pm$\sigma', leg_title=str(ietaBins[i])+r'$<i\eta^{jet, offline}<$'+str(ietaBins[i+1]))
    # SaveAndClose(odir + '/Resolution_ietaBins_{}.png'.format(v_sample))

    ###################################################################################################
    # PLOT TURN ON
    ###################################################################################################

    eff_bins = np.linspace(0,200,50)
    b_center = (eff_bins[:-1] + eff_bins[1:])/2
    b_center = np.array(b_center)

    h_off, _ = np.histogram(TargetPt, bins=eff_bins)
    h_unc, _ = np.histogram(TargetPt[unCalib > thr_un], bins=eff_bins)
    h_new, _ = np.histogram(TargetPt[newCalib > thr_new], bins=eff_bins)

    fig = plt.figure(figsize = [10,10])
    plt.hist(TargetPt, bins=eff_bins, label="Offline Inclusive", histtype='step', linewidth=2, color='Blue')
    text_1 = leg_uncalib + ": L1 jet Pt > {} Gev ".format(thr_un)
    plt.hist(TargetPt[unCalib > thr_un], bins=eff_bins, label=text_1, histtype='step', linewidth=2, color=c_uncalib)
    text_3 = leg_newcalib + ": L1 jet Pt > {} Gev ".format(int(thr_new))
    plt.hist(TargetPt[newCalib > thr_new], bins=eff_bins, label=text_3, histtype='step', linewidth=2, color=c_newcalib)
    SetSimpleStyle(r'$p_{T}^{jet, offline} [GeV]$', 'Entries', leg_title='')
    SaveAndClose(odir + '/Efficiency_{}.png'.format(v_sample))

    turn_on_unc = np.array([h_unc[i]/h_off[i] for i in range(len(h_off))])
    turn_on_new = np.array([h_new[i]/h_off[i] for i in range(len(h_off))])

    fig = plt.figure(figsize = [10,10])
    text_1 = leg_uncalib + ": L1 jet Pt > {} Gev".format(thr_un)
    plt.plot(b_center, turn_on_unc, label=text_1, marker='o', linestyle='dashed', linewidth=2, color=c_uncalib)
    text_3 = leg_newcalib + ": L1 jet Pt > {} Gev".format(thr_new)
    plt.plot(b_center, turn_on_new, label=text_3, marker='o', linestyle='dashed', linewidth=2, color=c_newcalib)
    SetSimpleStyle(r'$p_{T}^{jet, offline} [GeV]$', 'Efficiency', leg_title='')
    SaveAndClose(odir + '/Efficiency_TurnOn_{}.png'.format(v_sample))

    ###################################################################################################
    # SAVE TO JSON
    ###################################################################################################

    json_odir = odir + '/JSON'
    os.system('mkdir -p '+ json_odir)
    json_path = json_odir + '/Performance.json'

    rate_bin = rate_bins
    rate_unc = rate_uncalib
    rate_new = rate_newcalib

    eff_bin = eff_bins
    eff_unc = turn_on_unc
    eff_new = turn_on_new

    res_unc = [float(unRes.mean()), float(unRes.std())]
    res_new = [float(newRes.mean()), float(newRes.std())]

    int_unc = np.sum(eff_unc[7:])
    int_new = np.sum(eff_new[7:])

    data = {
        'rate_bin'  : rate_bin.tolist(),
        'rate_unc'  : rate_unc.tolist(),
        'rate_new'  : rate_new.tolist(),
        'eff_bin'   : eff_bin.tolist(),
        'eff_unc'   : eff_unc.tolist(),
        'eff_new'   : eff_new.tolist(),
        'res_unc'   : res_unc,
        'res_new'   : res_new,
        'int_unc'   : int_unc,
        'int_new'   : int_new,
    }

    json_data = json.dumps(data, indent=2)
    with open(json_path, "w") as json_file:
        json_file.write(json_data)

