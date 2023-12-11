import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import matplotlib, random, mplhep, json, time, glob, os, sys
plt.style.use(mplhep.style.CMS)

from tensorflow.keras.initializers import RandomNormal as RN
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers as lay
from tensorflow.keras.layers import Dense
from tensorflow import keras
import tensorflow as tf

import imageio

sys.path.insert(0,'..')
from L1Calibrator.CalibrationFactor import ExtractSFs

random.seed(7)
np.random.seed(7)
tf.random.set_seed(7)
tf.compat.v1.set_random_seed(7)
os.system('export PYTHONHASHSEED=7')

def PlotSF1D (ScaleFactors, bin_edges, eta_towers, odir, VERSION, i_epoch = None):

    if i_epoch: epoch = '_{}'.format(i_epoch)
    else: epoch = '' 

    plt.figure(figsize=(12,10))
    colors = plt.cm.viridis_r(np.linspace(0,1,len(bin_edges)))
    for i in range(len(bin_edges) - 1):
        plt.plot(eta_towers, ScaleFactors[i,:], 'o--', color=colors[i], label = f"{bin_edges[i]} $\leq E_T <$ {bin_edges[i+1]}")
    plt.xlabel('i$\eta$', fontsize=20)
    plt.ylabel('{} Calibration Constant'.format(VERSION), fontsize=20)
    plt.ylim(-0.1,5)
    plt.grid(linestyle='dotted')
    plt.title('Epoch {}'.format(i_epoch), loc='left', ha='left')
    savefile = odir + '/SFs_1D_' + VERSION + epoch + '.png'
    plt.savefig(savefile)
    plt.close()

    return savefile

def PlotSF2D (ScaleFactors, odir, VERSION, i_epoch = None):

    if i_epoch: epoch = '_{}'.format(i_epoch)
    else: epoch = ''

    cmap = cm.get_cmap("plasma")
    if VERSION == 'ECAL': min_=0; max_=1.5; cticks=10; xticks=np.linspace(1,28,28); figsize=(18,14)
    if VERSION == 'HCAL': min_=0; max_=3.0; cticks=10; xticks=np.linspace(1,40,40); figsize=(23,14)
    
    plt.figure(figsize=figsize)
    im = plt.pcolormesh(ScaleFactors, cmap=cmap, edgecolor='black', vmin=min_, vmax=max_)
    colorbar = plt.colorbar(im)
    colorbar.set_ticks(np.linspace(min_, max_, cticks))
    colorbar.ax.tick_params(which='minor', width=0, length=0)
    plt.tick_params(which='both', width=0, length=0)
    plt.xticks(xticks, ha='right')
    plt.ylabel(f'$Et$ $[GeV]$')
    plt.xlabel(f'$i\eta$')
    plt.title('Epoch {}'.format(i_epoch), loc='left', ha='left')
    savefile = odir + '/SFs_2D_' + VERSION + epoch + '.png'
    plt.savefig(savefile)
    plt.close()
   
    return savefile

def RunPlotSF(odir, i_epoch, VERSION, SF_filename_1, SF_filename_2 = None):

    def ReadSF(SF_filename, reg):

        if reg == 'ECAL' or reg == 'HCAL':
            ScaleFactors = np.loadtxt(open(SF_filename, "rb"), delimiter=',', usecols=range(0,28))
        if reg == 'HF':
            ScaleFactors = np.loadtxt(open(SF_filename_2, "rb"), delimiter=',', usecols=range(0,12))

        eta_towers = range(1, len(ScaleFactors[1])+1)
        with open(SF_filename) as f:
            header = f.readline().rstrip()
        bin_edges = header.split(',')[1:]
        bin_edges[-1] = bin_edges[-1][:-1]
        if int(bin_edges[-1]) == 256: bin_edges[-1] = '200'
        bin_edges = [ int(x) for x in bin_edges ]
        bin_edges = bin_edges[:np.array(ScaleFactors).shape[0]]
        
        return ScaleFactors, bin_edges, eta_towers

    if VERSION == "ECAL":

        SF_ECAL, bin_edges, eta_towers = ReadSF(SF_filename_1, 'ECAL')
        plot_1D = PlotSF1D (SF_ECAL, bin_edges, eta_towers, odir, "ECAL", i_epoch)
        plot_2d = PlotSF2D(SF_ECAL, odir, "ECAL", i_epoch)

    if VERSION == "HCAL":

        SF_HCAL, bin_edges, eta_towers = ReadSF(SF_filename_1, 'HCAL')
        SF_HF, _, _ = ReadSF(SF_filename_2, 'HF')
        SF_HCALpHF = np.concatenate([SF_HCAL, SF_HF], axis=1)
        plot_1D = plot_1D = PlotSF1D (SF_HCALpHF, bin_edges, range(1, 40+1), odir, "HCAL", i_epoch)
        plot_2d = PlotSF2D(SF_HCALpHF, odir, "HCAL", i_epoch)

    return plot_1D, plot_2d

### To run:
### python3 LossProgression.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --addtag _A_MSE_20ep --epochs 20

if __name__ == "__main__" :

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--indir",        dest="indir",       help="Input folder with trained model",     default=None)
    parser.add_option("--v",            dest="v",           help="Ntuple type ('ECAL' or 'HCAL')",      default='HCAL')
    parser.add_option("--tag",          dest="tag",         help="tag of the training folder",          default="")
    parser.add_option("--addtag",       dest="addtag",      help="Add tag for different trainings",     default="")
    parser.add_option("--model_type",   dest="model_type",  help="Model [Reg,RegAndRate]",              default='RegAndRate')
    parser.add_option("--epochs",       dest="epochs",      help="Number of epochs for the training",   default=20,    type=int)
    (options, args) = parser.parse_args()
    print(options)

    model_type = 'RegAndRate' # or 'Reg'
    if model_type == 'RegAndRate': from L1Training.NNModel_RegAndRate import *
    if model_type == 'Reg': from L1Training.NNModel_Reg import *

    VERSION = options.v
    MAX_LEARNING_RATE = 1E-3 # [FIXME]
    EPOCHS = options.epochs

    print("MAX_LEARNING_RATE = %f" %MAX_LEARNING_RATE)

    indir = '/data_CMS/cms/motta/CaloL1calibraton/' + options.indir + '/' + options.v + 'training' + options.tag + '/model_' + options.v + options.addtag
    odir = indir + '/progression_plots'
    os.system('mkdir -p '+ odir)
    print('\nOutput dir = {}\n'.format(odir))

    SFdir = indir + '/progression_plots/ScaleFactors'
    os.system('mkdir -p '+ SFdir)
    SFPlotsdir = indir + '/progression_plots/ScaleFactorsPlots'
    os.system('mkdir -p '+ SFPlotsdir)

    model = keras.models.load_model(indir + '/model', compile=False, custom_objects={'Fgrad': Fgrad})
    TTP = keras.models.load_model(indir + '/TTP', compile=False, custom_objects={'Fgrad': Fgrad})

    plot_1D_list = []
    plot_2D_list = []

    for epoch in range(EPOCHS):

        i = epoch + 1

        optimizer = keras.optimizers.Adam(learning_rate=MAX_LEARNING_RATE)
        checkpoint = tf.train.Checkpoint(optimizer=optimizer, model=TTP)

        # Restore model at that epoch
        CKPTdir = indir+'/training_checkpoints'
        CKPTpf = os.path.join(CKPTdir, "ckpt")
        status = checkpoint.restore(CKPTpf + "-" + str(i))
        status.expect_partial()

        # Extract and save SFs
        min_energy = 1; max_energy = 200; energy_step = 2
        if VERSION == 'HCAL':
            SF_filename_1 = ExtractSFs(TTP, 'HCAL', min_energy, max_energy, energy_step, SFdir, i)
            SF_filename_2 = ExtractSFs(TTP, 'HF', min_energy, max_energy, energy_step, SFdir, i)
            plot_1D, plot_2d = RunPlotSF(SFPlotsdir, i, VERSION, SF_filename_1, SF_filename_2)

        if VERSION == 'ECAL':
            SF_filename = ExtractSFs(TTP, 'ECAL', min_energy, max_energy, energy_step, SFdir, i)
            plot_1D, plot_2d = RunPlotSF(SFPlotsdir, i, VERSION, SF_filename)
        
        plot_1D_list.append(plot_1D)
        plot_2D_list.append(plot_2d)

    plot_1D_map = list(map(lambda plot_1D: imageio.imread(plot_1D), plot_1D_list))
    plot_2D_map = list(map(lambda plot_2D: imageio.imread(plot_2D), plot_2D_list))
    imageio.mimsave(SFPlotsdir+'/SFs_1D_'+VERSION+'.gif', plot_1D_map, format='GIF', duration=500)
    imageio.mimsave(SFPlotsdir+'/SFs_2D_'+VERSION+'.gif', plot_2D_map, format='GIF', duration=500)

