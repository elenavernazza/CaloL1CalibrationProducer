#!/usr/bin/env python

import jax.numpy as jnp
import numpy as np
from optparse import OptionParser
import matplotlib.pyplot as plt
import glob, os, json, matplotlib, sys

import mplhep
plt.style.use(mplhep.style.CMS)

#######################################################################
######################### SCRIPT BODY #################################
#######################################################################

if __name__ == "__main__" :

    parser = OptionParser()
    parser.add_option("--indir",                  dest="indir",                  default=""  ,                         help="Input directory with tensors")
    parser.add_option("--odir",                   dest="odir",                   default="./",                         help="Output tag of the output folder")
    parser.add_option("--v",                      dest="v",                      default="HCAL",                       help="Calibration target (ECAL, HCAL)")
    parser.add_option("--jetsLim",                dest="jetsLim",                default=None,       type=int,         help="Fix the total amount of jets to be used")
    parser.add_option("--filesLim",               dest="filesLim",               default=None,       type=int,         help="Maximum number of npz files to use")
    (options, args) = parser.parse_args()
    print(options)

    #######################################################################
    ## READING INPUT
    #######################################################################

    if options.indir == "": sys.exit("Input directory is not specified")
    indir = '/data_CMS/cms/motta/CaloL1calibraton/' + options.indir
    print(indir)
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
            # print("Reading file {}, {}".format(list_towers_files[ifile], training_stat))
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

    towers = jnp.concatenate(list_train_towers)
    jets = jnp.concatenate(list_train_jets)

    print(" ### INFO: Training on {} jets".format(len(jets)))

    if options.v == "HCAL":
        eta_binning = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
        et_binning  = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 256]
    elif options.v == "ECAL":
        eta_binning = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
        et_binning  = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 256]

    eta_binning = np.array(eta_binning)
    et_binning = np.array(et_binning)
    eta_axis = [int(x) for x in eta_binning[eta_binning < 29]] + [int(x+1) for x in eta_binning[eta_binning >= 29]]

    print(" ### INFO: Eta binning = ", eta_binning)
    print(" ### INFO: Energy binning = ", et_binning)

    ieta = np.argmax(towers[:, :, 3: ], axis=2) + 1
    ieta = ieta.ravel()
    ihad = towers[:, :, 1].ravel()
    iem = towers[:, :, 0].ravel()

    #######################################################################
    ## TOWERS HISTOGRAM
    #######################################################################

    if options.v == 'HCAL':
        hist, xedges, yedges = np.histogram2d(ieta, ihad, bins=[eta_binning, et_binning])
    elif options.v == 'ECAL':
        hist, xedges, yedges = np.histogram2d(ieta, iem, bins=[eta_binning, et_binning])
    hist[hist == 0] = -1
    min_ = 1
    # max_ = int(np.max(hist)/20) # for 9x9 CD
    # max_ = int(np.max(hist)/5) # for 3x3 CD
    max_ = int(np.max(hist)) # for Cluster

    fig, ax = plt.subplots(1, 1, figsize=(14,12))
    cmap = matplotlib.cm.get_cmap("viridis")
    cmap.set_under(color='white') 
    im = plt.pcolormesh(xedges[:-1], yedges[:-1], hist.T, cmap=cmap, edgecolor='black', vmin=min_, vmax=max_)
    plt.colorbar()
    ax.set_xticks(eta_binning[:-1])
    ax.set_xticklabels([int(x) for x in eta_axis[:-1]], fontsize=11, rotation=90)
    ax.set_yticks(et_binning[:-1])
    ax.set_yticklabels([int(x) for x in et_binning[:-1]], fontsize=11, rotation=0)
    # colorbar.set_ticks(np.linspace(min_, max_, nticks))
    # colorbar.ax.tick_params(which='minor', width=0, length=0)
    plt.tick_params(which='both', width=0, length=0)

    plt.ylabel(f'$Et$ $[GeV]$')
    plt.xlabel(f'$i\eta$')
    savefile = odir + '/InputTowers'
    plt.savefig(savefile+'.png')
    plt.savefig(savefile+'.pdf')
    print(savefile)

    L1Energy = np.sum(towers[:,:,0], axis=1) + np.sum(towers[:,:,1], axis=1)
    JetEnergy = jets[:, 3]
    Response = np.array(L1Energy/JetEnergy)

    fig, ax = plt.subplots(1, 1, figsize=(10,10))
    bins_pt = np.linspace(0,200,200)
    plt.hist(JetEnergy/2, bins=bins_pt, histtype='step', stacked=True, linewidth=2, color='black')
    plt.xlabel(r'$p_{T}$ [GeV]')
    plt.ylabel('Entries')
    plt.grid(linestyle='dotted')
    savefile = odir + '/InputJetPt'
    plt.savefig(savefile+'.png')
    plt.savefig(savefile+'.pdf')
    print(savefile)

    fig, ax = plt.subplots(1, 1, figsize=(10,10))
    bins_res = np.linspace(0,3,200)
    plt.hist(Response, bins=bins_res, histtype='step', stacked=True, linewidth=2, color='black')
    plt.xlabel(r'Response')
    plt.ylabel('Entries')
    plt.grid(linestyle='dotted')
    savefile = odir + '/InputResponse'
    plt.savefig(savefile+'.png')
    plt.savefig(savefile+'.pdf')
    print(savefile)

    fig, ax = plt.subplots(1, 1, figsize=(10,10))
    bins_res = np.linspace(0,3,200)
    eta = np.array(np.abs(jets[:,1]))
    plt.hist(Response[(eta < 1.305)], bins=bins_res, histtype='step', stacked=True, linewidth=2, color='blue', label='Barrel')
    plt.hist(Response[(eta >= 1.305) & (eta < 3)], bins=bins_res, histtype='step', stacked=True, linewidth=2, color='green', label='Endcap')
    plt.hist(Response[(eta >= 3)], bins=bins_res, histtype='step', stacked=True, linewidth=2, color='purple', label='Forward')
    plt.xlabel(r'Response')
    plt.ylabel('Entries')
    plt.grid(linestyle='dotted')
    plt.legend()
    savefile = odir + '/InputResponseSplit'
    plt.savefig(savefile+'.png')
    plt.savefig(savefile+'.pdf')
    print(savefile)

    os.system('mkdir -p '+ odir + '/EtaBins')
    if options.v == "ECAL":
        etaBins = [0., 0.5, 1.0, 1.305, 1.479, 2.0, 2.5, 3.0]
    if options.v == "HCAL":
        etaBins = [0., 0.5, 1.0, 1.305, 1.479, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.191]
    for i,etaBin in enumerate(etaBins[:-1]):
        fig, ax = plt.subplots(1, 1, figsize=(10,10))
        bins_res = np.linspace(0,3,200)
        eta = np.array(np.abs(jets[:,1]))
        plt.hist(Response[(eta >= etaBins[i]) & (eta < etaBins[i+1])], bins=bins_res, histtype='step', stacked=True, linewidth=2, color='black', label='Barrel')
        plt.xlabel(r'Response')
        plt.ylabel('Entries')
        plt.grid(linestyle='dotted')
        plt.legend(title=str(etaBins[i])+r'$<|\eta|<$'+str(etaBins[i+1]))
        savefile = odir + '/EtaBins/InputResponse_'+str(etaBins[i])+'eta'+str(etaBins[i+1])
        plt.savefig(savefile+'.png')
        plt.savefig(savefile+'.pdf')
        print(savefile)