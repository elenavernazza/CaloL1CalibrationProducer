#librairies utiles
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import mplhep, json, glob
plt.style.use(mplhep.style.CMS)

min_ = -0.2
max_ = 2.2

def export_legend(legend, filename="legend.png", expand=[-5,-5,5,5]):
    fig  = legend.figure
    fig.canvas.draw()
    bbox  = legend.get_window_extent()
    bbox = bbox.from_extents(*(bbox.extents + np.array(expand)))
    bbox = bbox.transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(filename, dpi="figure", bbox_inches=bbox)

def PlotSF (SF_matrix, bins, odir, v_sample, eta_towers, i_epoch = None):

    if i_epoch != None: epoch = '_{}'.format(i_epoch)
    else: epoch = ''

    plt.figure(figsize=(12,10))
    colors = plt.cm.viridis_r(np.linspace(0,1,len(bins)))
    for i in range(len(bins) - 1):
        plt.plot(eta_towers, SF_matrix[i,:], 'o--', color=colors[i], label = f"{bins[i]} $\leq E_T <$ {bins[i+1]}")
    plt.xlabel('i$\eta$', fontsize=20)
    plt.ylabel('{} Calibration Constant'.format(v_sample), fontsize=20)
    plt.grid(linestyle='dotted')
    mplhep.cms.label(data=True, rlabel='(13.6 TeV)', fontsize=20)
    savefile = odir + '/Calib_vs_Eta_'+v_sample+epoch
    plt.ylim(min_,max_)
    plt.savefig(savefile+'.png')
    plt.savefig(savefile+'.pdf')
    print(savefile)
    # plt.ylim(0,13)
    # legend = plt.legend(fontsize=10, ncol=8, loc = 'upper center')
    # savefile = odir + '/Calib_vs_Eta_'+v_sample+'_legend.png'
    # export_legend(legend, savefile)
    # print(savefile)
    
def PlotSF2D (SF_matrix, odir, et_binning, eta_binning, v_sample, i_epoch = None):

    eta_axis = [int(x) for x in eta_binning[eta_binning < 29]] + [int(x+1) for x in eta_binning[eta_binning >= 29]]
    et_axis = ["{}-{}".format(et_binning[i],et_binning[i+1]) for i in range(0,len(et_binning)-1)]

    if i_epoch != None: epoch = '_{}'.format(i_epoch)
    else: epoch = ''

    fig, ax = plt.subplots(1, 1, figsize=(14,12))

    im = plt.pcolormesh(eta_binning, et_binning[:-1], SF_matrix, cmap='viridis', edgecolor='black', vmin=min_, vmax=max_)
    ax.set_xticks(eta_binning)
    ax.set_xticklabels(eta_axis, fontsize=11, rotation=90)
    ax.set_yticks(et_binning[:-1])
    ax.set_yticklabels(et_axis, fontsize=11, rotation=0)

    colorbar = plt.colorbar(im, label=str(v_sample+' SFs'))
    nticks = 10
    # colorbar.set_ticks(np.linspace(min_, max_, nticks))
    # colorbar.ax.tick_params(which='minor', width=0, length=0)
    plt.tick_params(which='both', width=0, length=0)

    plt.ylabel(f'$Et$ $[GeV]$')
    plt.xlabel(f'$i\eta$')
    savefile = odir + '/SFs_2D_'+v_sample+epoch
    plt.savefig(savefile+'.png')
    plt.savefig(savefile+'.pdf')
    print(savefile)
   
    return True


### To run:
### python3 SFPlots.py --indir 1

if __name__ == "__main__" :

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--indir",    dest="indir",   help="Input folder with trained model",     default=None)
    parser.add_option("--tag",      dest="tag",     help="tag of the training folder",          default="")
    parser.add_option("--out",      dest="odir",    help="Output folder",                       default=None)
    parser.add_option("--v",        dest="v",       help="Ntuple type ('ECAL' or 'HCAL')",      default='HCAL')
    parser.add_option("--addtag",   dest="addtag",  help="Add tag to distinguish different trainings",  default="",)
    (options, args) = parser.parse_args()
    print(options)
 
    # Definition of the trained model
    # indir = '/data_CMS/cms/motta/CaloL1calibraton/' + options.indir + '/' + options.v + 'training' + options.tag
    indir = options.indir
    # Definition of output folder 
    # odir = modeldir + '/SFs_' + str(options.energystep) + 'iEt' + '/SFplots'
    # os.system('mkdir -p '+ odir)
    odir = options.indir

    #######################################################
    ################# Scale Factors plots #################
    #######################################################

    SF_filename = indir + '/ScaleFactors_{}.csv'.format(options.v)
    if options.v == "ECAL": cols = 28
    if options.v == "HCAL": cols = 40
    ScaleFactors = np.loadtxt(open(SF_filename, "rb"), delimiter=',', usecols=range(0,cols))
    eta_binning = np.arange(1,cols+1)

    # Definition of energy bin edges from the header
    with open(SF_filename) as f:
        header = f.readline().rstrip()
    header = header.split("[")[1].split("]")[0]
    et_binning = header.split(',')
    et_binning = [float(i) for i in et_binning]
    
    PlotSF(ScaleFactors, et_binning, odir, options.v, eta_binning)
    PlotSF2D(ScaleFactors, odir, et_binning, eta_binning, options.v)

    #######################################################
    ################# Loss History plots ##################
    #######################################################

    json_path = indir + '/training.json'
    with open(json_path, 'r') as json_file: data = json.load(json_file)
    ep = list(data["TrainLoss"].keys())
    ep = np.array([int(i) for i in ep])
    train_loss = list(data["TrainLoss"].values())
    test_loss = list(data["TestLoss"].values())

    plt.figure(figsize=(10,10))
    plt.plot(ep, train_loss, 'o--', color='red', label="Train Loss")
    plt.plot(ep, test_loss, 'o--', color='blue', label="Test Loss")
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(linestyle='dotted')
    mplhep.cms.label(data=True, rlabel='(13.6 TeV)', fontsize=20)
    savefile = odir + '/Loss'
    plt.savefig(savefile+'.png')
    plt.savefig(savefile+'.pdf')
    print(savefile)
