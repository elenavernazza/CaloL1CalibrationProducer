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
    for ibin in range(1,histo.GetNbinsX()):
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
(options, args) = parser.parse_args()

# get/create folders
basedir = "/data_CMS/cms/motta/CaloL1calibraton/"
olddir = options.olddir_name+"/"
uncdir = options.uncdir_name+"/"
indir = options.indir
outdir = indir
print(" ### INFO: UnCalib dir  = {}".format(uncdir))
print(" ### INFO: OldCalib dir = {}".format(olddir))
print(" ### INFO: NewCalib dir = {}".format(indir))

label = options.label
target = options.target
os.system('mkdir -p '+outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/comparisons_'+label+'_'+target+options.ref)
os.system('mkdir -p '+outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/comparisons_'+label+'_'+target+options.ref)

#defining binning of histogram
if options.target == 'jet':
    ptBins  = [15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 90, 110, 130, 160, 200, 500]
    etaBins = [0., 0.5, 1.0, 1.305, 1.479, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.191]
    x_lim_response = (0.,3.)
if options.target == 'ele':
    ptBins  = [0, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 90, 110, 130, 160, 200]
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
endcap_label = r'Endcap $1.479<|\eta^{%s, %s}|<5.191$' % (part_name, targ_name)
inclusive_label = r'Inclusive $|\eta^{%s, %s}|<5.191$' % (part_name, targ_name)

x_label_pt      = r'$p_{T}^{%s, %s}$' % (part_name, targ_name)
x_label_eta     = r'$\eta^{%s, %s}$' % (part_name, targ_name)
x_label_Hotot   = r'$H/Tot$'
x_label_Eotot   = r'$E/Tot$'

x_lim_pt        = (0,150)
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
y_label_scale       = 'Energy scale (Mean)'
y_label_scale_max   = 'Energy scale (Maximum)'
y_lim_scale = (0.5,1.5)

x_label_rate = r'$E_{T}^{%s, L1}$' % (part_name)
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
                legend_label_response = r'Resolution: $\sigma / \mu$'
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

