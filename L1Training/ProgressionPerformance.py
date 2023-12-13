import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import matplotlib, random, mplhep, json, time, glob, os, sys, math
plt.style.use(mplhep.style.CMS)

import imageio
import warnings
warnings.filterwarnings("ignore")

sys.path.insert(0,'..')

c_uncalib = 'black'
c_oldcalib = 'red'
c_newcalib = 'green'

leg_uncalib = 'No calib'
leg_oldcalib = 'Old calib'
leg_newcalib = 'New calib'

TowersEta = {
    1:  [0,     0.087],    2: [0.087,  0.174],    3: [0.174,  0.261],    4: [0.261,  0.348],    5: [0.348,  0.435],    6: [0.435,  0.522],    7: [0.522,  0.609],    8: [0.609,  0.696],    9: [0.696,  0.783],    10: [0.783,  0.870],
    11: [0.870, 0.957],    12: [0.957, 1.044],    13: [1.044, 1.131],    14: [1.131, 1.218],    15: [1.218, 1.305],    16: [1.305, 1.392],    17: [1.392, 1.479],    18: [1.479, 1.566],    19: [1.566, 1.653],    20: [1.653, 1.740],
    21: [1.740, 1.830],    22: [1.830, 1.930],    23: [1.930, 2.043],    24: [2.043, 2.172],    25: [2.172, 2.322],    26: [2.322, 2.5],      27: [2.5,   2.650],    28: [2.650, 3.],       29: [3., 3.139],       30: [3.139, 3.314],
    31: [3.314, 3.489],    32: [3.489, 3.664],    33: [3.664, 3.839],    34: [3.839, 4.013],    35: [4.013, 4.191],    36: [4.191, 4.363],    37: [4.363, 4.538],    38: [4.538, 4.716],    39: [4.716, 4.889],    40: [4.889, 5.191],}

def GetSFs (VERSION, file_1, file_2 = None):
    SFs = []
    if VERSION == 'ECAL':
        f_ECAL = open(file_1)
        f_ECAL_lines = f_ECAL.readlines()
        for i, line in enumerate(f_ECAL_lines):
            if '#' in line: continue
            sf_line_ECAL = line.split(',\n')[0]
            sf_vec_ECAL = [float(j) for j in sf_line_ECAL.split(',')]
            SFs = SFs + sf_vec_ECAL
    if VERSION == 'HCAL':
        f_HCAL = open(file_1)
        f_HF = open(file_2)
        f_HCAL_lines = f_HCAL.readlines()
        f_HF_lines = f_HF.readlines()
        for i, line in enumerate(f_HCAL_lines):
            if '#' in line: continue
            sf_line_HCAL = line.split(',\n')[0]
            sf_vec_HCAL = [float(j) for j in sf_line_HCAL.split(',')]
            sf_line_HF = f_HF_lines[i].split(',\n')[0]
            sf_vec_HF = [float(j) for j in sf_line_HF.split(',')]
            SFs = SFs + sf_vec_HCAL + sf_vec_HF
    return SFs

def CalibrateTT(df_Towers, SFs, VERSION, i_epoch):

    EnergyBins2iEt = [
        -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
        41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 
        61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 
        81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 256]
    
    EnergyBins2iEt = np.array(EnergyBins2iEt)*2+0.1 # to convert to iEt and shift to center of bin

    if VERSION == 'ECAL':
        et_column = 'iem'
        nEtaBins = 28
    elif VERSION == 'HCAL':
        et_column = 'hcalET'
        nEtaBins = 40

    # Compute the bin indices using digitize
    df_Towers['iBin'] = np.digitize(df_Towers[et_column], EnergyBins2iEt)
    # Calculate the SFs for each row
    df_Towers['SF'] = df_Towers.apply(lambda row: SFs[int(abs(row['ieta']) + nEtaBins * (row['iBin'] - 1)) - 1], axis=1)
    # Use vectorized operations to calculate calibrated energy
    df_Towers['calib_et_%s' %(i_epoch)] = (df_Towers[et_column] * df_Towers['SF']).floordiv(1)
    # Drop unnecessary columns
    df_Towers.drop(columns=["iBin", "SF"], inplace=True)

    return df_Towers

def CreateDataframe(InTFRecords, odir, eventLim, VERSION, type):

    dataset = tf.data.TFRecordDataset(InTFRecords, num_parallel_reads=tf.data.experimental.AUTOTUNE)
    batch_size = len(list(dataset))
    parsed_dataset = dataset.map(parse_function)
    data = parsed_dataset.batch(batch_size).as_numpy_iterator().next()
    print('\n ### N events in the dataset: ' + str(len(list(dataset))))

    if eventLim > -1:
        print('\n ### Reading {} events'.format(eventLim))
        n_events = int(eventLim)
        Towers = data[0][:n_events]
        if not type == 'Rate': Jets = data[1][:int(eventLim)]
    else:
        print('\n ### Reading all events')
        n_events = len(list(dataset))
        Towers = data[0]
        if not type == 'Rate': Jets = data[1]
    del dataset, parsed_dataset, data

    # Extract the iem and hcalET columns from Towers
    if VERSION == 'ECAL':
        iem = Towers[:, :, 1].reshape(-1)
        hcalET = Towers[:, :, 0].reshape(-1)
    elif VERSION == 'HCAL':
        iem = Towers[:, :, 0].reshape(-1)
        hcalET = Towers[:, :, 1].reshape(-1)

    # Extract the ieta column from Towers using argmax
    ieta = np.argmax(Towers[:, :, 2:], axis=2).reshape(-1) + 1

    # Create arrays for the id and jetPt columns
    id_arr = np.repeat(np.arange(len(Towers)), Towers.shape[1])
    iesum = (iem + hcalET)

    # Create the dataframe
    print(" ### INFO: Creating dataframe")
    if not type == 'Rate':
        jetPt_arr = np.repeat(Jets, Towers.shape[1])
        df_Towers = pd.DataFrame({'id': id_arr, 'targetPt': jetPt_arr, 'iem': iem, 'hcalET': hcalET, 'ieta': ieta, 'iesum': iesum})
    else:
        df_Towers = pd.DataFrame({'id': id_arr, 'iem': iem, 'hcalET': hcalET, 'ieta': ieta, 'iesum': iesum})

    DF_dir = odir + '/progression_plots/DataFrames/'
    os.system('mkdir -p '+ DF_dir)
    df_Towers.to_pickle(DF_dir+type+'.pkl')

    return df_Towers

def PlotRateProgression(odir, df_Towers_Rate, binning, VERSION, thr_un, i_epoch = None):

    if i_epoch: epoch = '_{}'.format(i_epoch)
    else: epoch = ''

    df_rate = pd.DataFrame()
    df_rate['jetPt_uncalib']                = df_Towers_Rate.groupby('id')['iesum'].sum() / 2
    if VERSION == 'ECAL':
        df_rate['jetPt_calib%s' %(i_epoch)] = (df_Towers_Rate.groupby('id')['calib_et_%s' %(i_epoch)].sum() + df_Towers_Rate.groupby('id')['hcalET'].sum()) / 2
    if VERSION == 'HCAL':
        df_rate['jetPt_calib%s' %(i_epoch)] = (df_Towers_Rate.groupby('id')['calib_et_%s' %(i_epoch)].sum() + df_Towers_Rate.groupby('id')['iem'].sum()) / 2
    df_rate['jetSeed']                      = df_Towers_Rate.groupby('id')['iesum'].max() / 2
    
    sel_seed = df_rate['jetSeed'] > 4
    h_uncalib, _  = np.histogram(df_rate[sel_seed]['jetPt_uncalib'], bins=binning)
    h_newcalib, _ = np.histogram(df_rate[sel_seed]['jetPt_calib%s' %(i_epoch)], bins=binning)

    b_center = (binning[:-1] + binning[1:])/2
    rate_uncalib  = np.array([np.sum(h_uncalib[b_center > i])/np.sum(h_uncalib) for i in b_center])
    rate_newcalib = np.array([np.sum(h_newcalib[b_center > i])/np.sum(h_newcalib) for i in b_center])

    fig = plt.figure(figsize = [10,10])
    b_center = (binning[:-1] + binning[1:])/2
    text_1 = leg_uncalib + ": ProxyRate 50 Gev = {:.4f}".format(np.sum(h_uncalib[b_center > 50])/np.sum(h_uncalib))
    plt.plot(b_center, rate_uncalib, label=text_1, marker='o', linestyle='dashed', linewidth=2, color=c_uncalib)
    text_2 = leg_newcalib + ": ProxyRate 50 Gev = {:.4f}".format(np.sum(h_newcalib[b_center > 50])/np.sum(h_newcalib))
    plt.plot(b_center, rate_newcalib, label=text_2, marker='o', linestyle='dashed', linewidth=2, color=c_newcalib)
    plt.xlabel(r'$p_{T}^{jet, L1} [GeV]$')
    plt.ylabel('Rate Proxy')
    plt.grid(linestyle='dotted')
    plt.legend(fontsize=15, loc='upper right')
    plt.title('Epoch {}'.format(i_epoch), loc='left', ha='left')
    savefile = odir + '/Rate_Progression' + epoch + '.png'
    plt.savefig(savefile)
    plt.close()

    rate_uncalib_fix = rate_uncalib[b_center >= thr_un][0]
    thr_new = b_center[np.argmax(rate_newcalib <= rate_uncalib_fix)]

    return savefile, thr_new

def PlotTrainProgression(Response_dir, Resolution_dir, Turnon_dir, df_Towers, VERSION, thr_un, thr_new, i_epoch = None, MinusIem = False):

    if i_epoch: epoch = '_{}'.format(i_epoch)
    else: epoch = ''

    # compute sum of the raw energy 
    df_jets = pd.DataFrame()
    df_jets['unCalib']    = df_Towers.groupby('id')['iesum'].sum() 
    if VERSION == 'ECAL':
        df_jets['newCalib'] = df_Towers.groupby('id')['calib_et_%s' %(i_epoch)].sum() + df_Towers.groupby('id').hcalET.sum()
    if VERSION == 'HCAL':
        df_jets['newCalib'] = df_Towers.groupby('id')['iem'].sum() + df_Towers.groupby('id')['calib_et_%s' %(i_epoch)].sum()
    if MinusIem: 
        df_jets['jetPt'] = df_Towers.groupby('id').targetPt.median() + df_Towers.groupby('id').iem.sum()
    else: 
        df_jets['jetPt'] = df_Towers.groupby('id').targetPt.median()

    df_jets['jetIEta']    = df_Towers.groupby('id').ieta.first()
    df_jets['jetEta']     = df_jets.apply(lambda row: (TowersEta[row['jetIEta']][0] + TowersEta[row['jetIEta']][1])/2, axis=1)
    df_jets['jetSeed']    = df_Towers.groupby('id')['iesum'].max() / 2

    # compute resolution
    df_jets['unc_res'] = df_jets.apply(lambda row: row['unCalib']/row['jetPt'], axis=1)
    df_jets['new_res'] = df_jets.apply(lambda row: row['newCalib']/row['jetPt'], axis=1)

    bins_res = np.linspace(0,3,240)

    def GetYLim(num):
        power = 0
        while power + 10 <= num:
            power += 100
        return power

    plt.figure(figsize=(10,10))
    def GetText(df, key): return r': $\mu={:.3f}, res={:.3f}$'.format(df[key].mean(), df[key].std()/df[key].mean())

    text_1 = leg_uncalib+GetText(df_jets, 'unc_res')
    h1 = plt.hist(df_jets['unc_res'], bins=bins_res, label=text_1, histtype='step', stacked=True, linewidth=2, color=c_uncalib)
    text_3 = leg_newcalib+GetText(df_jets, 'new_res')
    h3 = plt.hist(df_jets['new_res'], bins=bins_res, label=text_3, histtype='step', stacked=True, linewidth=2, color=c_newcalib)
    plt.xlabel('Response')
    plt.ylabel('Entries')
    plt.ylim(0, 1.1*GetYLim(max(h1[0].max(), h3[0].max())))
    plt.grid(linestyle='dotted')
    plt.legend(fontsize=15, loc='upper left')
    plt.title('Epoch {}'.format(i_epoch), loc='left', ha='left')
    savefile_1 = Response_dir + '/Response_Progression{}.png'.format(epoch)
    plt.savefig(savefile_1)
    plt.close()

    savefiles_2 = []
    for bin_type in ['pt', 'eta']:
        if bin_type == 'pt':
            keyBins  = [30, 35, 40, 45, 50, 60, 70, 90, 110, 130, 160, 200]
            key = 'jetPt'
            legend_label = r'$<p_{T}^{jet, offline}<$'
            x_label = r'$p_{T}^{jet, offline}$'
        elif bin_type == 'eta':
            keyBins = [0., 0.5, 1.0, 1.305, 1.479, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.191]
            key = 'jetEta'
            legend_label = r'$<|\eta^{jet, offline}|<$'
            x_label = r'$\eta^{jet, offline}$'

        mean_res_unc = []
        mean_res_new = []

        for i in range(len(keyBins)-1):
            
            if bin_type == 'pt': sel_pt = (df_jets[key] > keyBins[i]*2) & (df_jets[key] < keyBins[i+1]*2)
            else: sel_pt = (df_jets[key] > keyBins[i]) & (df_jets[key] < keyBins[i+1])

            def GetMeanAndRMS(df, key): return [df[key].mean(), df[key].std()/df[key].mean()]
            mean_res_unc.append(GetMeanAndRMS(df_jets[sel_pt], 'unc_res'))
            mean_res_new.append(GetMeanAndRMS(df_jets[sel_pt], 'new_res'))
            
        Ymax = 0
        fig, axs = plt.subplots(1, 2, figsize=(18,9), sharey = False)

        X = [(keyBins[i] + keyBins[i+1])/2 for i in range(len(keyBins)-1)]
        X_err = [(keyBins[i+1] - keyBins[i])/2 for i in range(len(keyBins)-1)]

        axs[0].errorbar(X, [a[1] for a in mean_res_unc], xerr=X_err, label=leg_uncalib, ls='None', lw=2, marker='o', color=c_uncalib, zorder=0)
        axs[0].errorbar(X, [a[1] for a in mean_res_new], xerr=X_err, label=leg_newcalib, ls='None', lw=2, marker='o', color=c_newcalib, zorder=0)
        axs[0].set_xlabel(x_label)
        axs[0].set_ylabel('Energy Resolution')
        axs[0].set_ylim(0., 0.7)
        axs[0].grid()
        axs[0].set_title('Epoch {}'.format(i_epoch), loc='left', ha='left')

        axs[1].errorbar(X, [a[0] for a in mean_res_unc], xerr=X_err, label=leg_uncalib, ls='None', lw=2, marker='o', color=c_uncalib, zorder=0)
        axs[1].errorbar(X, [a[0] for a in mean_res_new], xerr=X_err, label=leg_newcalib, ls='None', lw=2, marker='o', color=c_newcalib, zorder=0)
        axs[1].set_xlabel(x_label)
        axs[1].set_ylabel('Energy Mean')
        axs[1].set_ylim(0.5, 1.5)
        axs[1].grid()
        axs[1].legend(loc='upper right', fontsize=20)

        savefile_2 = Resolution_dir+'/Resolution_Progression_'+bin_type+'Bins'+epoch+'.png'
        plt.savefig(savefile_2)
        plt.close()
        savefiles_2.append(savefile_2)

    binning = np.linspace(0,200,50)
    b_center = (binning[:-1] + binning[1:])/2
    b_center = np.array(b_center)

    df_jets['unCalib_GeV'] = df_jets['unCalib'] / 2
    df_jets['newCalib_GeV'] = df_jets['newCalib'] / 2
    df_jets['jetPt_GeV'] = df_jets['jetPt'] / 2

    sel_seed = df_jets['jetSeed'] > 4

    sel_unc = df_jets['unCalib_GeV'] > thr_un
    sel_new = df_jets['newCalib_GeV'] > thr_new
    h_off, _ = np.histogram(df_jets['jetPt_GeV'], bins=binning)
    h_unc, _ = np.histogram(df_jets[sel_seed & sel_unc]['jetPt_GeV'], bins=binning)
    h_new, _ = np.histogram(df_jets[sel_seed & sel_new]['jetPt_GeV'], bins=binning)

    def GetTurnOn(histo_on,histo_off):
        turn_on = []
        for i in range(len(h_off)):
            if h_off[i] != 0: turn_on.append(histo_on[i]/histo_off[i])
            else: turn_on.append(0)
        return np.array(turn_on)
    
    turn_on_unc = GetTurnOn(h_unc, h_off)
    turn_on_new = GetTurnOn(h_new, h_off)

    def GetText(thr, turn_on):
        eff_50 = turn_on[np.where(b_center >= 50)[0][0]]
        eff_70 = turn_on[np.where(b_center >= 70)[0][0]]
        eff_80 = turn_on[np.where(b_center >= 80)[0][0]]
        eff_90 = turn_on[np.where(b_center >= 90)[0][0]]
        return ": L1 jet Pt > {} Gev \n(eff. at 50 GeV {:.4f})\n(eff. at 70 GeV {:.4f})".format(thr, eff_50, eff_70)
    
    fig = plt.figure(figsize = [10,10])
    plt.plot(b_center, turn_on_unc, label=leg_uncalib+GetText(thr_un, turn_on_unc), marker='o', linestyle='dashed', linewidth=2, color=c_uncalib)
    plt.plot(b_center, turn_on_new, label=leg_newcalib+GetText(thr_new, turn_on_new), marker='o', linestyle='dashed', linewidth=2, color=c_newcalib)
    plt.xlabel(r'$p_{T}^{jet, offline} [GeV]$')
    plt.ylabel('Efficiency')
    plt.grid(linestyle='dotted')
    plt.legend(fontsize=15, loc='lower right')
    plt.title('Epoch {}'.format(i_epoch), loc='left', ha='left')
    savefile_3 = Turnon_dir + '/Efficiency_TurnOn{}.png'.format(epoch)
    plt.savefig(savefile_3)
    plt.close() 

    return [savefile_1] + savefiles_2 + [savefile_3]



### To run:
### python3 ProgressionTraining.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --addtag _test_checkpoint --epochs 20 --filesLim 1

if __name__ == "__main__" :

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--indir",        dest="indir",       help="Input folder with trained model",     default=None)
    parser.add_option("--v",            dest="v",           help="Ntuple type ('ECAL' or 'HCAL')",      default='HCAL')
    parser.add_option("--tag",          dest="tag",         help="tag of the training folder",          default="")
    parser.add_option("--addtag",       dest="addtag",      help="Add tag for different trainings",     default="")
    parser.add_option("--model_type",   dest="model_type",  help="Model [Reg,RegAndRate]",              default='RegAndRate')
    parser.add_option("--epochs",       dest="epochs",      help="Number of epochs for the training",   default=20,         type=int)
    parser.add_option("--filesLim",     dest="filesLim",    help="Maximum number of npz files to use",  default=1000000,    type=int)
    parser.add_option("--eventLim",     dest="eventLim",    help="Maximum number of events to use",     default=-1,         type=int)
    parser.add_option("--set",          dest="set",         help="Dataser type [Train, Test]",          default='Train')
    parser.add_option("--ljetPtcut",    dest="ljetPtcut",   help="Apply lowerjetPt cut [GeV]",          default=None)
    parser.add_option("--ujetPtcut",    dest="ujetPtcut",   help="Apply upperjetPt cut [GeV]",          default=None)
    parser.add_option("--MinusIem",     dest="MinusIem",    help="Add Iem to the jetPt target",         default=False,   action='store_true')
    # parser.add_option("--ietacut",      dest="ietacut",     help="Apply ieta cut",                      default=None)
    # parser.add_option("--HoEcut",       dest="HoEcut",      help="Apply HoE cut at 0.95",               default=None)
    parser.add_option("--FromDF",       dest="FromDF",      help="Read from stored DF",                 default=False,   action='store_true')

    (options, args) = parser.parse_args()
    print(options)

    VERSION = options.v
    MAX_LEARNING_RATE = 1E-3 # [FIXME]
    EPOCHS = options.epochs
    SET = options.set

    print("MAX_LEARNING_RATE = %f" %MAX_LEARNING_RATE)

    # model_type = 'RegAndRate' # or 'Reg'
    # if model_type == 'RegAndRate': from L1Training.NNModel_RegAndRate import *
    # if model_type == 'Reg': from L1Training.NNModel_Reg import *
    # model = keras.models.load_model(indir + '/model', compile=False, custom_objects={'Fgrad': Fgrad})
    # TTP = keras.models.load_model(indir + '/TTP', compile=False, custom_objects={'Fgrad': Fgrad})

    indir = '/data_CMS/cms/motta/CaloL1calibraton/' + options.indir + '/' + options.v + 'training' + options.tag + '/model_' + options.v + options.addtag
    odir = indir + '/progression_plots'
    os.system('mkdir -p '+ odir)
    print('\nOutput dir = {}\n'.format(odir))

    Rate_dir = indir + '/progression_plots/Rate'
    os.system('mkdir -p '+ Rate_dir)
    Response_dir = indir + '/progression_plots/' + SET + '/Response'
    os.system('mkdir -p '+ Response_dir)
    Resolution_dir = indir + '/progression_plots/' + SET + '/Resolution'
    os.system('mkdir -p '+ Resolution_dir)
    Turnon_dir = indir + '/progression_plots/' + SET + '/Turnon'
    os.system('mkdir -p '+ Turnon_dir)

    plot_rate_list = []
    plot_respo_list = []
    plot_resol_pt_list = []
    plot_resol_eta_list = []
    plot_turnon_list = []

    energystep = 2
    rate_binning = np.linspace(0,200,101)

    ############################################################################################################
    ############################################################################################################
    ############################################################################################################
    # [FIXME] We are not using a testing dataset for the rate sample: this is not correct

    if not options.FromDF:

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

        feature_description = {
            'chuncky_donut': tf.io.FixedLenFeature([], tf.string, default_value=''), # byteslist to be read as string 
            'trainingPt'   : tf.io.FixedLenFeature([], tf.float32, default_value=0)  # single float values
        }
        # parse proto input based on description
        def parse_function(example_proto):
            example = tf.io.parse_single_example(example_proto, feature_description)
            chuncky_donut = tf.io.parse_tensor(example['chuncky_donut'], out_type=tf.float32) # decode byteslist to original 81x43 tensor
            return chuncky_donut, example['trainingPt']
        tfdir = '/data_CMS/cms/motta/CaloL1calibraton/' + options.indir + '/' + options.v + 'training' + options.tag
        print('\n ### Reading TF records from: ' + tfdir + '/rateTFRecords/record_*.tfrecord')
        InRateRecords = glob.glob(tfdir+'/rateTFRecords/record_*.tfrecord')[:options.filesLim]
        df_Towers_Rate = CreateDataframe(InRateRecords, indir, options.eventLim, options.v, type = 'Rate')
    else:
        df_Towers_Rate = pd.read_pickle(indir+'/progression_plots/DataFrames/Rate.pkl')

    if options.set == 'Train':
        if not options.FromDF:
            tfdir = '/data_CMS/cms/motta/CaloL1calibraton/' + options.indir + '/' + options.v + 'training' + options.tag
            print('\n ### Reading TF records from: ' + tfdir + '/trainTFRecords/record_*.tfrecord')
            InTestRecords = glob.glob(tfdir+'/trainTFRecords/record_*.tfrecord')[:options.filesLim]
            df_Towers_Train = CreateDataframe(InTestRecords, indir, options.eventLim, options.v, type = 'Training')
        else:
            df_Towers_Train = pd.read_pickle(indir+'/progression_plots/DataFrames/Training.pkl')

    if options.set == 'Test':
        if not options.FromDF:
            tfdir = '/data_CMS/cms/motta/CaloL1calibraton/' + options.indir + '/' + options.v + 'training' + options.tag
            print('\n ### Reading TF records from: ' + tfdir + '/testTFRecords/record_*.tfrecord')
            InTestRecords = glob.glob(tfdir+'/testTFRecords/record_*.tfrecord')[:options.filesLim]
            df_Towers_Train = CreateDataframe(InTestRecords, indir, options.eventLim, options.v, type = 'Testing')
        else:
            df_Towers_Train = pd.read_pickle(indir+'/progression_plots/DataFrames/Testing.pkl')

    ############################################################################################################
    ############################################################################################################
    ############################################################################################################

    if options.ljetPtcut:
        df_Towers_Train = df_Towers_Train[df_Towers_Train['targetPt'] > float(options.ljetPtcut)*2]
    if options.ujetPtcut:
        df_Towers_Train = df_Towers_Train[df_Towers_Train['targetPt'] < float(options.ujetPtcut)*2]

    for i_epoch in range(EPOCHS):

        i_epoch = i_epoch + 1
        epoch = '_{}'.format(i_epoch)

        # Get SF file
        print("\n ### INFO: Reading Scale Factors epoch", epoch)
        SFdir = indir + '/progression_plots/ScaleFactors'
        if VERSION == 'ECAL':
            SFFile_ECAL = SFdir + '/ScaleFactors_ECAL_energystep2iEt'+epoch+'.csv'
            SFs = GetSFs (VERSION, SFFile_ECAL)
        if VERSION == 'HCAL':
            SFFile_HCAL = SFdir + '/ScaleFactors_HCAL_energystep2iEt'+epoch+'.csv'
            SFFile_HF = SFdir + '/ScaleFactors_HF_energystep2iEt'+epoch+'.csv'
            SFs = GetSFs (VERSION, SFFile_HCAL, SFFile_HF)

        print(" ### INFO: Calibrating towers for rate")

        thr_un = 50
        df_Towers_Rate = CalibrateTT(df_Towers_Rate, SFs, VERSION, i_epoch)
        plot_rate, thr_new = PlotRateProgression(Rate_dir, df_Towers_Rate, rate_binning, VERSION, thr_un, i_epoch)
        print(" ### INFO: Old threshold {} GeV, New threshold {} GeV".format(thr_un, thr_new))
        plot_rate_list.append(plot_rate)

        df_Towers_Train = CalibrateTT(df_Towers_Train, SFs, VERSION, i_epoch)
        plot_respo, plot_resol_pt, plot_resol_eta, plot_turnon = PlotTrainProgression(Response_dir, Resolution_dir, Turnon_dir, df_Towers_Train, VERSION, thr_un, thr_new, i_epoch)
        plot_respo_list.append(plot_respo)
        plot_resol_pt_list.append(plot_resol_pt)
        plot_resol_eta_list.append(plot_resol_eta)
        plot_turnon_list.append(plot_turnon)

    plot_rate_map = list(map(lambda plot: imageio.imread(plot), plot_rate_list))
    imageio.mimsave(Rate_dir+'/Rate_Progression.gif', plot_rate_map, format='GIF', duration=500)

    plot_respo_map = list(map(lambda plot: imageio.imread(plot), plot_respo_list))
    imageio.mimsave(Response_dir+'/Response_Progression.gif', plot_respo_map, format='GIF', duration=500)

    plot_resol_pt_map = list(map(lambda plot: imageio.imread(plot), plot_resol_pt_list))
    imageio.mimsave(Resolution_dir+'/Resolution_Progression_ptBins.gif', plot_resol_pt_map, format='GIF', duration=500)

    plot_resol_eta_map = list(map(lambda plot: imageio.imread(plot), plot_resol_eta_list))
    imageio.mimsave(Resolution_dir+'/Resolution_Progression_etaBins.gif', plot_resol_eta_map, format='GIF', duration=500)

    plot_turnon_map = list(map(lambda plot: imageio.imread(plot), plot_turnon_list))
    imageio.mimsave(Turnon_dir+'/Efficiency_TurnOn.gif', plot_turnon_map, format='GIF', duration=500)

