from array import array
import ROOT
ROOT.gROOT.SetBatch(True)
import os, sys 

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.transforms import ScaledTranslation
import numpy as np
import mplhep
plt.style.use(mplhep.style.CMS)

import warnings
warnings.simplefilter(action='ignore')

def GetArraysFromHisto(histo):
    X = [] ; Y = [] ; X_err = [] ; Y_err = []
    for ibin in range(0,histo.GetNbinsX()):
        X.append(histo.GetBinLowEdge(ibin+1) + histo.GetBinWidth(ibin+1)/2.)
        Y.append(histo.GetBinContent(ibin+1))
        X_err.append(histo.GetBinWidth(ibin+1)/2.)
        Y_err.append(histo.GetBinError(ibin+1))
    return X,Y,X_err,Y_err

def GetArraysFromGraph(graph):
    X = [] ; Y = [] ; Y_low = [] ; Y_high = []
    for ibin in range(0,graph.GetN()):
        X.append(graph.GetPointX(ibin))
        Y.append(graph.GetPointY(ibin))
        Y_low.append(graph.GetErrorYlow(ibin))
        Y_high.append(graph.GetErrorYhigh(ibin))
    return X,Y,Y_low,Y_high

def SetStyle(ax, x_label, y_label, x_lim, y_lim, leg_title='', turnon=False):
    if turnon:
        leg = plt.legend(loc='lower right', fontsize=17, title=leg_title, title_fontsize=18)
    else:
        leg = plt.legend(loc = 'upper right', fontsize=20, title=leg_title, title_fontsize=18)
    leg._legend_box.align = "left"
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xlim(x_lim)
    plt.ylim(y_lim)
    plt.grid()
    for xtick in ax.xaxis.get_major_ticks():
        xtick.set_pad(10)
    if options.reco: mplhep.cms.label('Preliminary', data=True, rlabel='(13.6 TeV)')
    else:            mplhep.cms.label('Preliminary', data=True, rlabel=r'110 pb$^{-1}$ (13.6 TeV)') ## 110pb-1 is Run 362617

def AddRectangles(ax, Ymax):
    rect1 = patches.Rectangle((-1.479, 0), 0.174, Ymax*1.3, linewidth=1, edgecolor='gray', facecolor='gray', zorder=2)
    rect2 = patches.Rectangle((1.305, 0), 0.174, Ymax*1.3, linewidth=1, edgecolor='gray', facecolor='gray', zorder=2)
    ax.add_patch(rect1)
    ax.add_patch(rect2)  

def GetText(inclusive_resp):
    s = round(inclusive_resp.GetRMS(),3)
    m = round(inclusive_resp.GetMean(),3)
    return r'$%s/%s=%s$' % (s, m, round(s/m,3))

NewCalibLabel = "New Calibration"
OldCalibLabel = "Old Calibration"
NoCalibLabel = "No Calibration"

#######################################################################
######################### SCRIPT BODY #################################
#######################################################################

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--indir",       dest="indir",                            default=None)
parser.add_option("--tag",         dest="tag",                              default='')
parser.add_option("--ref",         dest="ref",                              default='')
parser.add_option("--label",       dest="label",                            default='')
parser.add_option("--target",      dest="target",                           default=None)
parser.add_option("--reco",        dest="reco",        action='store_true', default=False)
parser.add_option("--gen",         dest="gen",         action='store_true', default=False)
parser.add_option("--thrsFixRate", dest="thrsFixRate", action='append',     default=None)
parser.add_option("--old",         dest="olddir_name",                      default='0000_00_00_NtuplesVold')
parser.add_option("--unc",         dest="uncdir_name",                      default='0000_00_00_NtuplesVunc')
parser.add_option("--doResponse",  dest="doResponse",                       default=True)
parser.add_option("--doResolution",dest="doResolution",                     default=True)
parser.add_option("--doTurnOn",    dest="doTurnOn",                         default=True)
parser.add_option("--doRate",      dest="doRate",                           default=True)
parser.add_option("--do_HoTot",    dest="do_HoTot",    action='store_true', default=False)
parser.add_option("--do_EoTot",    dest="do_EoTot",    action='store_true', default=False)
parser.add_option("--er",          dest="er",                               default=None) #eta restriction
parser.add_option("--offline",     dest="offline",     action='store_true', default=False)
(options, args) = parser.parse_args()

# get/create folders
basedir = "/data_CMS/cms/motta/CaloL1calibraton/"
olddir = basedir+"/"+options.olddir_name+"/"
uncdir = basedir+"/"+options.uncdir_name+"/"
indir = basedir+options.indir
outdir = indir
print(" ### INFO: UnCalib dir  = {}".format(uncdir))
print(" ### INFO: OldCalib dir = {}".format(olddir))
print(" ### INFO: NewCalib dir = {}".format(indir))

label = options.label
target = options.target
O2O = "_O2O" if options.offline else ""
os.system('mkdir -p '+outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/comparisons_'+label+O2O+'_'+target+options.ref)
os.system('mkdir -p '+outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/comparisons_'+label+O2O+'_'+target+options.ref)

#defining binning of histogram
if options.target == 'jet':
    ptBins  = [30, 35, 40, 45, 50, 60, 70, 90, 110, 130, 160, 200, 500]
    etaBins = [0., 0.5, 1.0, 1.305, 1.479, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.191]
    x_lim_response = (0.,3.)
if options.target == 'ele':
    ptBins  = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 90, 110, 130, 160, 200]
    etaBins = [0., 0.5, 1.0, 1.305, 1.479, 2.0, 2.5, 3.0]
    x_lim_response = (0.2,1.5)
HoTotBins = [0, 0.4, 0.8, 0.95, 1.0]
EoTotBins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

############################################################################################
############################################################################################
############################################################################################

if options.reco:    targ_name = 'offline'
elif options.gen:   targ_name = 'gen'
if options.target == 'jet':     part_name = 'jet'
elif options.target == 'ele':   part_name = 'e'
elif options.target == 'met':   part_name = 'MET'

barrel_label = r'Barrel $|\eta^{%s, %s}|<1.305$' % (part_name, targ_name)
endcap_label = r'Endcap $1.305<|\eta^{%s, %s}|<3$' % (part_name, targ_name)
forward_label = r'Forward $3<|\eta^{%s, %s}|<5.191$' % (part_name, targ_name)
inclusive_label = r'Inclusive $|\eta^{%s, %s}|<5.191$' % (part_name, targ_name)

x_label_pt      = r'$p_{T}^{%s, %s}$' % (part_name, targ_name)
x_label_eta     = r'$\eta^{%s, %s}$' % (part_name, targ_name)
x_label_Hotot   = r'$H/Tot$'
x_label_Eotot   = r'$E/Tot$'

if target == 'ele': x_lim_pt        = (0,110) 
if target == 'jet': x_lim_pt        = (0,200) 
x_lim_eta       = (-5.2,5.2) # (-3.01,3.01)
x_lim_Hotot     = (0,1)
x_lim_Eotot     = (0,1)

legend_label_pt     = r'$<|p_{T}^{%s, %s}|<$' % (part_name, targ_name)
legend_label_eta    = r'$<|\eta^{%s, %s}|<$' % (part_name, targ_name)
legend_label_Hotot  = r'$<H/Tot<$'
legend_label_Eotot  = r'$<E/Tot<$'

x_label_response = r'$E_{T}^{%s, L1} / p_{T}^{%s, %s}$' % (part_name,part_name, targ_name)
y_label_response = 'Entries'

y_label_resolution  = 'Energy resolution'
y_label_fwhm  = 'FWHM / mean'
y_label_scale       = 'Energy scale (Mean)'
y_label_scale_max   = 'Energy scale (Maximum)'
y_lim_scale = (0.5,1.5)

x_label_rate = r'$E_{T}^{%s, Offline}$' % (part_name) if options.offline else r'$E_{T}^{%s, L1}$' % (part_name)
x_label_turnon = r'$E_{T}^{%s, %s}$' % (part_name, targ_name)

############################################################################################
############################################################################################
############################################################################################

if options.doResponse == True or options.doResolution == True:
    file_unCalib  = ROOT.TFile(uncdir+'/PerformancePlots/'+label+'/ROOTs/resolution_graphs_'+label+'_'+target+'.root', 'r')
    file_oldCalib = ROOT.TFile(olddir+'/PerformancePlots/'+label+'/ROOTs/resolution_graphs_'+label+'_'+target+'.root', 'r')
    file_newCalib = ROOT.TFile(indir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs/resolution_graphs_'+label+'_'+target+'.root', 'r')

if options.doResponse == True:

    print("\n *** COMPARING RESPONSE")
    print(" ### INFO: UnCalib file  = {}".format(uncdir+'/PerformancePlots/'+label+'/ROOTs/resolution_graphs_'+label+'_'+target+'.root'))
    print(" ### INFO: OldCalib file = {}".format(olddir+'/PerformancePlots/'+label+'/ROOTs/resolution_graphs_'+label+'_'+target+'.root'))
    print(" ### INFO: NewCalib file = {}".format(indir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs/resolution_graphs_'+label+'_'+target+'.root'))

    # for histo_name in ["pt_response_ptInclusive", "pt_response_ptInclusive_CD"]:
    for histo_name in ["pt_response_ptInclusive", "pt_barrel_resp_ptInclusive", 
                       "pt_endcap_resp_ptInclusive", "pt_forward_resp_ptInclusive"]:

        if options.target == "ele": 
            if histo_name == "pt_forward_resp_ptInclusive": continue
        if histo_name == "pt_response_ptInclusive": name = ''
        if histo_name == "pt_response_ptInclusive_CD": name = '_CD'

        inclusive_resp_unCalib  = file_unCalib.Get(histo_name)
        inclusive_resp_oldCalib = file_oldCalib.Get(histo_name)
        inclusive_resp_newCalib = file_newCalib.Get(histo_name)

        if histo_name == "pt_response_ptInclusive": region = "inclusive"
        else: region = histo_name.split("_")[1]

        for legend_type in ['w', 'w/o']:

            text = ''; legend_label_response = ''; leg = ''

            if legend_type == 'w': # with numbers
                legend_label_response = '{} '.format(region.capitalize()) + r'Resolution: $\sigma / \mu$'
                leg = '_res'

            fig, ax = plt.subplots(figsize=(10,10))
            X,Y,X_err,Y_err = GetArraysFromHisto(inclusive_resp_unCalib)
            if legend_type == 'w': text = ': '+ GetText(inclusive_resp_unCalib)
            ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=NoCalibLabel+text, ls='None', lw=2, marker='o', color='black', zorder=0)
            ax.step(np.array((np.array(X[:-1])+np.array(X[1:]))/2), np.array(Y[:-1]), color='black')
            Ymax = max(Y)
            X,Y,X_err,Y_err = GetArraysFromHisto(inclusive_resp_oldCalib)
            if legend_type == 'w': text = ': '+ GetText(inclusive_resp_oldCalib)
            ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=OldCalibLabel+text, ls='None', lw=2, marker='o', color='red', zorder=1)
            ax.step(np.array((np.array(X[:-1])+np.array(X[1:]))/2), np.array(Y[:-1]), color='red')
            Ymax = max(Ymax, max(Y))
            X,Y,X_err,Y_err = GetArraysFromHisto(inclusive_resp_newCalib)
            if legend_type == 'w': text = ': '+ GetText(inclusive_resp_newCalib)
            ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=NewCalibLabel+text, ls='None', lw=2, marker='o', color='green', zorder=2)
            ax.step(np.array((np.array(X[:-1])+np.array(X[1:]))/2), np.array(Y[:-1]), color='green')
            Ymax = max(Ymax, max(Y))
            SetStyle(ax, x_label_response, y_label_response, x_lim_response, (0., Ymax*1.3), legend_label_response)
            plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/comparisons_'+label+'_'+target+options.ref+'/response_'+region+name+leg+'_'+label+'_'+target+'.pdf')
            plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/comparisons_'+label+'_'+target+options.ref+'/response_'+region+name+leg+'_'+label+'_'+target+'.png')
            print(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/comparisons_'+label+'_'+target+options.ref+'/response_'+region+name+leg+'_'+label+'_'+target+'.png')
            plt.close()

    list_bins = ['ptBin', 'AbsEtaBin']
    if options.do_HoTot: list_bins.append('HoTotBin')
    if options.do_EoTot: list_bins.append('EoTotBin')

    for bins in list_bins:
        if bins == 'ptBin':
            Bins = ptBins
            legend_label = legend_label_pt
            name = 'pt'
        if bins == 'AbsEtaBin':
            Bins = etaBins
            legend_label = legend_label_eta
            name = 'eta'
        if bins == 'HoTotBin':
            Bins = HoTotBins
            legend_label = legend_label_Hotot
            name = 'HoTot'
        if bins == 'EoTotBin':
            Bins = EoTotBins
            legend_label = legend_label_Eotot
            name = 'EoTot'

        for i in range(len(Bins)-1):
            # print(" ### DEBUG ", "pt_resp_"+bins+str(Bins[i])+"to"+str(Bins[i+1]))
            Bins_resp_unCalib = file_unCalib.Get("pt_resp_"+bins+str(Bins[i])+"to"+str(Bins[i+1]))
            Bins_resp_oldCalib = file_oldCalib.Get("pt_resp_"+bins+str(Bins[i])+"to"+str(Bins[i+1]))
            Bins_resp_newCalib = file_newCalib.Get("pt_resp_"+bins+str(Bins[i])+"to"+str(Bins[i+1]))

            fig, ax = plt.subplots(figsize=(10,10))
            X,Y,X_err,Y_err = GetArraysFromHisto(Bins_resp_unCalib)
            ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=NoCalibLabel, ls='None', lw=2, marker='o', color='black', zorder=0)
            ax.step(np.array((np.array(X[:-1])+np.array(X[1:]))/2), np.array(Y[:-1]), color='black')
            Ymax = max(Y)
            X,Y,X_err,Y_err = GetArraysFromHisto(Bins_resp_oldCalib)
            ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=OldCalibLabel, ls='None', lw=2, marker='o', color='red', zorder=1)
            ax.step(np.array((np.array(X[:-1])+np.array(X[1:]))/2), np.array(Y[:-1]), color='red')
            Ymax = max(Ymax, max(Y))
            X,Y,X_err,Y_err = GetArraysFromHisto(Bins_resp_newCalib)
            ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=NewCalibLabel, ls='None', lw=2, marker='o', color='green', zorder=2)
            ax.step(np.array((np.array(X[:-1])+np.array(X[1:]))/2), np.array(Y[:-1]), color='green')
            Ymax = max(Ymax, max(Y))
            SetStyle(ax, x_label_response, y_label_response, x_lim_response, (0., Ymax*1.3), str(Bins[i])+legend_label+str(Bins[i+1]))
            plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/comparisons_'+label+'_'+target+options.ref+'/response_'+str(Bins[i])+name+str(Bins[i+1])+"_"+label+'_'+target+'.pdf')
            plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/comparisons_'+label+'_'+target+options.ref+'/response_'+str(Bins[i])+name+str(Bins[i+1])+"_"+label+'_'+target+'.png')
            print(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/comparisons_'+label+'_'+target+options.ref+'/response_'+str(Bins[i])+name+str(Bins[i+1])+"_"+label+'_'+target+'.png')
            plt.close()

############################################################################################
############################################################################################
############################################################################################
# for DEBUG

if options.doTurnOn == True:
    file_turnon_unCalib  = ROOT.TFile(uncdir+'/PerformancePlots/'+label+'/ROOTs/efficiency_graphs_'+label+'_'+target+'.root', 'r')
    file_turnon_oldCalib = ROOT.TFile(olddir+'/PerformancePlots/'+label+'/ROOTs/efficiency_graphs_'+label+'_'+target+'.root', 'r')
    file_turnon_newCalib = ROOT.TFile(indir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs/efficiency_graphs_'+label+'_'+target+'.root', 'r')

    print("\n *** COMPARING TURN ONS")
    print(" ### INFO: UnCalib file  = {}".format(uncdir+'/PerformancePlots/'+label+'/ROOTs/efficiency_graphs_'+label+'_'+target+'.root'))
    print(" ### INFO: OldCalib file = {}".format(olddir+'/PerformancePlots/'+label+'/ROOTs/efficiency_graphs_'+label+'_'+target+'.root'))
    print(" ### INFO: NewCalib file = {}".format(indir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs/efficiency_graphs_'+label+'_'+target+'.root'))

    y_label_turnon = 'Efficiency'
    if target == 'ele': x_lim_turnon = (0, 100); x_lim_rate = (0, 100)
    if target == 'jet': x_lim_turnon = (0, 200); x_lim_rate = (0, 200)
    y_lim_turnon = (0, 1.05)

    eta_range_list = ['', 'er2p5']
    if options.er: eta_range_list.append("er"+options.er.replace(".", "p"))

    if target == 'jet': thr_list = [30,50,70,100]
    if target == 'ele': thr_list = [10,15,20,36]

    for eta_range in eta_range_list:

        if eta_range == '': 
            er_label = ''
            er_name = ''
        else:
            er_name = eta_range.capitalize()
            er_label = '_' + er_name

        for thr in thr_list:
            turnon_unCalib  = file_turnon_unCalib.Get("divide_passing"+er_label+'_'+str(int(thr))+"_by_total"+er_label)
            turnon_oldCalib = file_turnon_oldCalib.Get("divide_passing"+er_label+'_'+str(int(thr))+"_by_total"+er_label)
            turnon_newCalib = file_turnon_newCalib.Get("divide_passing"+er_label+'_'+str(int(thr))+"_by_total"+er_label)
            fig, ax = plt.subplots(figsize=(10,10))
            X,Y,Y_low,Y_high = GetArraysFromGraph(turnon_unCalib)
            ax.errorbar(X, Y, xerr=1, yerr=[Y_low, Y_high], label=NoCalibLabel+R': $p_{T}^{L1}>$'+str(int(thr))+' GeV', lw=2, marker='o', color='black', zorder=0)
            X,Y,Y_low,Y_high = GetArraysFromGraph(turnon_oldCalib)
            ax.errorbar(X, Y, xerr=1, yerr=[Y_low, Y_high], label=OldCalibLabel+R': $p_{T}^{L1}>$'+str(int(thr))+' GeV', lw=2, marker='o', color='red', zorder=1)
            X,Y,Y_low,Y_high = GetArraysFromGraph(turnon_newCalib)
            ax.errorbar(X, Y, xerr=1, yerr=[Y_low, Y_high], label=NewCalibLabel+R': $p_{T}^{L1}>$'+str(int(thr))+' GeV', lw=2, marker='o', color='green', zorder=2)
            SetStyle(ax, x_label_turnon, y_label_turnon, x_lim_turnon, y_lim_turnon, 'Turn On Fixed Threshold '+er_name, turnon=True)
            plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/comparisons_'+label+'_'+target+options.ref+'/turnon'+er_name+'_'+str(thr)+'_'+label+'_'+target+'.pdf')
            plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/comparisons_'+label+'_'+target+options.ref+'/turnon'+er_name+'_'+str(thr)+'_'+label+'_'+target+'.png')
            print(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/comparisons_'+label+'_'+target+options.ref+'/turnon'+er_name+'_'+str(thr)+'_'+label+'_'+target+'.png')
            plt.close()

############################################################################################
############################################################################################
############################################################################################

if options.doResolution == True:

    print("** COMPARING RESOLUTIONS AND SCALES")

    list_vars = ['Pt', 'Eta']
    if options.do_HoTot: list_vars.append('HoTot')
    if options.do_EoTot: list_vars.append('EoTot')

    for var in list_vars:

        X_r_uncalib, X_s_uncalib = [], []

        for quantity in ['resol', 'scale', 'scale_max', 'fwhm']:

            if var == 'Pt':
                x_label = x_label_pt
                x_lim = x_lim_pt
                name_x = 'pt'
            if var == 'Eta':
                x_label = x_label_eta
                x_lim = x_lim_eta
                name_x = 'eta'
            if var == 'HoTot':
                x_label = x_label_Hotot
                x_lim = x_lim_Hotot
                name_x = 'HoTot'
            if var == 'EoTot':
                x_label = x_label_Eotot
                x_lim = x_lim_Eotot
                name_x = 'EoTot'

            if quantity == 'resol': 
                y_label = y_label_resolution
                y_lim = None
                name_y = 'resolution'
                if var == "Pt" and target == "jet": regions = ["", "_barrel", "_endcap", "_forward"]
                elif var == "Pt" and target == "ele": regions = ["", "_barrel", "_endcap"]
                else: regions = [""]

            if quantity == 'fwhm': 
                y_label = y_label_fwhm
                y_lim = None
                name_y = 'fwhm'
                if var == "Pt" and target == "jet": regions = ["", "_barrel", "_endcap", "_forward"]
                elif var == "Pt" and target == "ele": regions = ["", "_barrel", "_endcap"]
                else: regions = [""]

            if quantity == 'scale': 
                y_label = y_label_scale
                y_lim = y_lim_scale
                name_y = 'scale'
                if var == "Pt" and target == "jet": regions = ["", "_barrel", "_endcap", "_forward"]
                elif var == "Pt" and target == "ele": regions = ["", "_barrel", "_endcap"]
                else: regions = [""]
            if quantity == 'scale_max': 
                y_label = y_label_scale_max
                y_lim = y_lim_scale
                name_y = 'scale_max'
                regions = [""]

            for region in regions:

                Bins_resol_unCalib  = file_unCalib.Get("pt_"+quantity+region+"_fct"+var)
                Bins_resol_oldCalib = file_oldCalib.Get("pt_"+quantity+region+"_fct"+var)
                Bins_resol_newCalib = file_newCalib.Get("pt_"+quantity+region+"_fct"+var)

                fig, ax = plt.subplots(figsize=(10,10))
                X,Y,X_err,Y_err = GetArraysFromHisto(Bins_resol_unCalib)
                ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=NoCalibLabel, ls='None', lw=2, marker='o', color='black', zorder=0)
                if quantity == 'resol' and region == '': X_r_uncalib = X; Y_r_uncalib = Y
                if quantity == 'fwhm' and region == '': X_r_uncalib = X; Y_r_uncalib = Y
                if quantity == 'scale' and region == '': X_s_uncalib = X; Y_s_uncalib = Y
                Ymax = max(Y)
                X,Y,X_err,Y_err = GetArraysFromHisto(Bins_resol_oldCalib)
                ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=OldCalibLabel, ls='None', lw=2, marker='o', color='red', zorder=1)
                if quantity == 'resol' and region == '': X_r_oldcalib = X; Y_r_oldcalib = Y
                if quantity == 'fwhm' and region == '': X_r_oldcalib = X; Y_r_oldcalib = Y
                if quantity == 'scale' and region == '': X_s_oldcalib = X; Y_s_oldcalib = Y
                Ymax = max(Ymax, max(Y))
                X,Y,X_err,Y_err = GetArraysFromHisto(Bins_resol_newCalib)
                ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=NewCalibLabel, ls='None', lw=2, marker='o', color='green', zorder=2)
                if quantity == 'resol' and region == '': X_r_newcalib = X; Y_r_newcalib = Y
                if quantity == 'fwhm' and region == '': X_r_newcalib = X; Y_r_newcalib = Y
                if quantity == 'scale' and region == '': X_s_newcalib = X; Y_s_newcalib = Y
                Ymax = max(Ymax, max(Y))
                if var == 'Eta': AddRectangles(ax,Ymax)
                if y_lim: SetStyle(ax, x_label, y_label, x_lim, y_lim)
                else: SetStyle(ax, x_label, y_label, x_lim, (0., 1.3*Ymax))
                plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/comparisons_'+label+'_'+target+options.ref+'/'+name_y+region+'_'+name_x+'Bins_'+label+'_'+target+'.pdf')
                plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/comparisons_'+label+'_'+target+options.ref+'/'+name_y+region+'_'+name_x+'Bins_'+label+'_'+target+'.png')
                print(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/comparisons_'+label+'_'+target+options.ref+'/'+name_y+region+'_'+name_x+'Bins_'+label+'_'+target+'.png')
                plt.close()

                if len(X_r_uncalib) > 0 and len(X_s_uncalib) > 0:

                    fig, ax = plt.subplots(figsize=(14,10))
                    trans_l = ax.transData + ScaledTranslation(-4/72, 0, fig.dpi_scale_trans)
                    trans_r = ax.transData + ScaledTranslation(+4/72, 0, fig.dpi_scale_trans)
                    ax.errorbar(X_s_uncalib, Y_s_uncalib, yerr=Y_r_uncalib, label=NoCalibLabel, ls='None', lw=2, marker='v', capsize=3, color='black', zorder=0, transform=trans_l)
                    ax.errorbar(X_s_oldcalib, Y_s_oldcalib, yerr=Y_r_oldcalib, label=OldCalibLabel, ls='None', lw=2, marker='^', capsize=3, color='red', zorder=1)
                    ax.errorbar(X_s_newcalib, Y_s_newcalib, yerr=Y_r_newcalib, label=NewCalibLabel, ls='None', lw=2, marker='o', capsize=3, color='green', zorder=2, transform=trans_r)
                    SetStyle(ax, x_label, 'Energy scale ($\mu \pm \sigma$)', x_lim, (0.3, 1.8))
                    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/comparisons_'+label+'_'+target+options.ref+'/scale_res_'+var+'Bins_'+label+'_'+target+'.pdf')
                    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/comparisons_'+label+'_'+target+options.ref+'/scale_res_'+var+'Bins_'+label+'_'+target+'.png')
                    print(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/comparisons_'+label+'_'+target+options.ref+'/scale_res_'+var+'Bins_'+label+'_'+target+'.png')
                    plt.close()

                    X_r_uncalib, X_s_uncalib = [], []

if options.doResponse == True or options.doResolution == True:
    file_unCalib.Close() 
    file_oldCalib.Close() 
    file_newCalib.Close() 

############################################################################################
############################################################################################
############################################################################################

if options.doRate == True or options.doTurnOn == True:

    file_rate_unCalib  = ROOT.TFile(uncdir+'/PerformancePlots/'+label+'/ROOTs/rate_graphs_'+label+O2O+'_'+target+'.root', 'r')
    file_rate_oldCalib = ROOT.TFile(olddir+'/PerformancePlots/'+label+'/ROOTs/rate_graphs_'+label+O2O+'_'+target+'.root', 'r')
    file_rate_newCalib = ROOT.TFile(indir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs/rate_graphs_'+label+O2O+'_'+target+'.root', 'r')

    file_turnon_unCalib  = ROOT.TFile(uncdir+'/PerformancePlots/'+label+'/ROOTs/efficiency_graphs_'+label+'_'+target+'.root', 'r')
    file_turnon_oldCalib = ROOT.TFile(olddir+'/PerformancePlots/'+label+'/ROOTs/efficiency_graphs_'+label+'_'+target+'.root', 'r')
    file_turnon_newCalib = ROOT.TFile(indir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs/efficiency_graphs_'+label+'_'+target+'.root', 'r')

if options.doRate == True:

    print("\n *** COMPARING RATES")
    print(" ### INFO: UnCalib file  = {}".format(uncdir+'/PerformancePlots/'+label+'/ROOTs/rate_graphs_'+label+O2O+'_'+target+'.root'))
    print(" ### INFO: OldCalib file = {}".format(olddir+'/PerformancePlots/'+label+'/ROOTs/rate_graphs_'+label+O2O+'_'+target+'.root'))
    print(" ### INFO: NewCalib file = {}".format(indir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs/rate_graphs_'+label+O2O+'_'+target+'.root'))
    
    y_label_turnon = 'Efficiency'
    if target == 'ele': x_lim_turnon = (0, 100); x_lim_rate = (0, 100)
    if target == 'jet': x_lim_turnon = (0, 200); x_lim_rate = (0, 200)
    # x_lim_turnon = (0, 200) #plt.xlim(0, 60) if int(thr) < 30 else plt.xlim(0, 200)
    y_lim_turnon = (0, 1.05)
    y_lim_rate = (0.1, 1E5)

    eta_range_list = ['', 'er2p5']
    if options.er: eta_range_list.append("er"+options.er.replace(".", "p"))

    for rate in ['rateDi', 'rate']:

        for eta_range in eta_range_list:

            rate_unCalib  = file_rate_unCalib.Get(rate + 'Progression0' + eta_range)
            rate_oldCalib = file_rate_oldCalib.Get(rate + 'Progression0' + eta_range)
            rate_newCalib = file_rate_newCalib.Get(rate + 'Progression0' + eta_range)

            if rate == 'rateDi':
                y_label_rate = 'Rate DiObject ' + eta_range.capitalize() + ' [kHz]'
                name = 'DiObj'
            if rate == 'rate':
                y_label_rate = 'Rate SingleObject ' + eta_range.capitalize() + ' [kHz]'
                name = 'Obj'

            if eta_range == '': 
                er_label = ''
                er_name = ''
            else:
                er_name = eta_range.capitalize()
                er_label = '_' + er_name
        
            fig, ax = plt.subplots(figsize=(10,10))
            X,Y,X_err,Y_err = GetArraysFromHisto(rate_unCalib)
            ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=NoCalibLabel, ls='None', lw=2, marker='o', color='black', zorder=0)
            X,Y,X_err,Y_err = GetArraysFromHisto(rate_oldCalib)
            ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=OldCalibLabel, ls='None', lw=2, marker='o', color='red', zorder=1)
            X,Y,X_err,Y_err = GetArraysFromHisto(rate_newCalib)
            ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=NewCalibLabel, ls='None', lw=2, marker='o', color='green', zorder=2)
            SetStyle(ax, x_label_rate, y_label_rate, x_lim_rate, y_lim_rate)
            plt.yscale('log')
            plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/comparisons_'+label+O2O+'_'+target+options.ref+'/rate_'+name+er_name+'_'+label+O2O+'_'+target+'.pdf')
            plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/comparisons_'+label+O2O+'_'+target+options.ref+'/rate_'+name+er_name+'_'+label+O2O+'_'+target+'.png')
            print(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/comparisons_'+label+O2O+'_'+target+options.ref+'/rate_'+name+er_name+'_'+label+O2O+'_'+target+'.png')
            plt.close()

            if options.doTurnOn == True:

                print("\n *** COMPARING TURN ONS")
                print(" ### INFO: UnCalib file  = {}".format(uncdir+'/PerformancePlots/'+label+'/ROOTs/efficiency_graphs_'+label+'_'+target+'.root'))
                print(" ### INFO: OldCalib file = {}".format(olddir+'/PerformancePlots/'+label+'/ROOTs/efficiency_graphs_'+label+'_'+target+'.root'))
                print(" ### INFO: NewCalib file = {}".format(indir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs/efficiency_graphs_'+label+'_'+target+'.root'))

                for thr in options.thrsFixRate:
                    rateOldCalibAtThr = rate_oldCalib.GetBinContent(int(thr)+1)

                    thrNewCalib = 0
                    for i in range(1,240):
                        if rate_newCalib.GetBinContent(i) <= rateOldCalibAtThr:
                            thrNewCalib = rate_newCalib.GetBinLowEdge(i-1)
                            break

                    thrUnCalib = 0
                    for i in range(1,240):
                        if rate_unCalib.GetBinContent(i) <= rateOldCalibAtThr:
                            thrUnCalib = rate_unCalib.GetBinLowEdge(i-1)
                            break
                    
                    if thrUnCalib == 0 or thrNewCalib == 0: continue

                    # print(" ### DEBUG: Thersholds = ", thrUnCalib, thr, thrNewCalib)
                    turnon_unCalib  = file_turnon_unCalib.Get("divide_passing"+er_label+'_'+str(int(thrUnCalib))+"_by_total"+er_label)
                    turnon_oldCalib = file_turnon_oldCalib.Get("divide_passing"+er_label+'_'+str(int(thr))+"_by_total"+er_label)
                    turnon_newCalib = file_turnon_newCalib.Get("divide_passing"+er_label+'_'+str(int(thrNewCalib))+"_by_total"+er_label)

                    fig, ax = plt.subplots(figsize=(10,10))
                    X,Y,Y_low,Y_high = GetArraysFromGraph(turnon_unCalib)
                    ax.errorbar(X, Y, xerr=1, yerr=[Y_low, Y_high], label=NoCalibLabel+R': $p_{T}^{L1}>$'+str(int(thrUnCalib))+' GeV', lw=2, marker='o', color='black', zorder=0)
                    X,Y,Y_low,Y_high = GetArraysFromGraph(turnon_oldCalib)
                    ax.errorbar(X, Y, xerr=1, yerr=[Y_low, Y_high], label=OldCalibLabel+R': $p_{T}^{L1}>$'+str(int(thr))+' GeV', lw=2, marker='o', color='red', zorder=1)
                    X,Y,Y_low,Y_high = GetArraysFromGraph(turnon_newCalib)
                    ax.errorbar(X, Y, xerr=1, yerr=[Y_low, Y_high], label=NewCalibLabel+R': $p_{T}^{L1}>$'+str(int(thrNewCalib))+' GeV', lw=2, marker='o', color='green', zorder=2)
                    SetStyle(ax, x_label_turnon, y_label_turnon, x_lim_turnon, y_lim_turnon, 'Fixed '+name+'ect Rate '+er_name+': '+str(round(rateOldCalibAtThr,2))+' kHz', turnon=True)
                    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/comparisons_'+label+O2O+'_'+target+options.ref+'/turnon_fixed'+name+'Rate'+er_name+'_'+thr+'_'+label+O2O+'_'+target+'.pdf')
                    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/comparisons_'+label+O2O+'_'+target+options.ref+'/turnon_fixed'+name+'Rate'+er_name+'_'+thr+'_'+label+O2O+'_'+target+'.png')
                    print(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/comparisons_'+label+O2O+'_'+target+options.ref+'/turnon_fixed'+name+'Rate'+er_name+'_'+thr+'_'+label+O2O+'_'+target+'.png')
                    plt.close()

                # print("\n *** COMPARING INTEGRAL OF TURN ONS")

                # integrals_unCalib = []
                # integrals_oldCalib = []
                # integrals_newCalib = []
                # thr_range = np.arange(30,80+1)

                # for thr in thr_range:

                #     rateOldCalibAtThr = rate_oldCalib.GetBinContent(int(thr)+1)

                #     thrNewCalib = 0
                #     for i in range(1,240):
                #         if rate_newCalib.GetBinContent(i) < rateOldCalibAtThr:
                #             thrNewCalib = rate_newCalib.GetBinLowEdge(i-1)
                #             break

                #     thrUnCalib = 0
                #     for i in range(1,240):
                #         if rate_unCalib.GetBinContent(i) < rateOldCalibAtThr:
                #             thrUnCalib = rate_unCalib.GetBinLowEdge(i-1)
                #             break
                    
                #     if thrUnCalib == 0 or thrNewCalib == 0: continue

                #     print(" *** Thresholds", thr, thrNewCalib, thrUnCalib)

                #     turnon_unCalib  = file_turnon_unCalib.Get("divide_passing"+er_label+'_'+str(int(thrUnCalib))+"_by_total"+er_label)
                #     turnon_oldCalib = file_turnon_oldCalib.Get("divide_passing"+er_label+'_'+str(int(thr))+"_by_total"+er_label)
                #     turnon_newCalib = file_turnon_newCalib.Get("divide_passing"+er_label+'_'+str(int(thrNewCalib))+"_by_total"+er_label)

                #     def GetIntegralEfficiency(graph):
                #         bin_start = 0
                #         for ibin in range(0,graph.GetN()):
                #             if graph.GetPointY(ibin) > 0.5: 
                #                 bin_start = ibin
                #                 break
                #         return graph.Integral(bin_start,graph.GetN())
                    
                #     integrals_unCalib.append(GetIntegralEfficiency(turnon_unCalib))
                #     integrals_oldCalib.append(GetIntegralEfficiency(turnon_oldCalib))
                #     integrals_newCalib.append(GetIntegralEfficiency(turnon_newCalib))

                # fig, ax = plt.subplots(figsize=(10,10))
                # ax.errorbar(thr_range, integrals_unCalib, xerr=1, yerr=1, label=NoCalibLabel, lw=2, marker='o', color='black', zorder=0)
                # ax.errorbar(thr_range, integrals_oldCalib, xerr=1, yerr=1, label=OldCalibLabel, lw=2, marker='o', color='red', zorder=1)
                # ax.errorbar(thr_range, integrals_newCalib, xerr=1, yerr=1, label=NewCalibLabel, lw=2, marker='o', color='green', zorder=2)
                # y_min = 0.9*min(np.min(integrals_unCalib), np.min(integrals_newCalib))
                # y_max = 1.1*max(np.max(integrals_unCalib), np.max(integrals_newCalib))
                # SetStyle(ax, 'Threshold [GeV]', 'Efficiency integral', (thr_range[0],thr_range[-1]), (y_min,y_max))
                # plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/comparisons_'+label+'_'+target+options.ref+'/turnon_all_fixed'+name+'Rate'+er_name+'_'+label+'_'+target+'.pdf')
                # plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/comparisons_'+label+'_'+target+options.ref+'/turnon_all_fixed'+name+'Rate'+er_name+'_'+label+'_'+target+'.png')
                # print(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/comparisons_'+label+'_'+target+options.ref+'/turnon_all_fixed'+name+'Rate'+er_name+'_'+label+'_'+target+'.png')
                # plt.close()
