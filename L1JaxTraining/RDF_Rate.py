import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(000000)
import sys, os, sys
import numpy as np
from array import array
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import mplhep
plt.style.use(mplhep.style.CMS)
from RDF_Functions import *

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning)

'''
python3 RDF_Rate.py \
 --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data  \
 --outdir 0/NtuplesVunc --target jet --raw --nEvts 100 --no_plot
'''

#######################################################################
######################### SCRIPT BODY #################################
#######################################################################

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--indir",     dest="indir",    default=None)
parser.add_option("--tag",       dest="tag",      default='')
parser.add_option("--outdir",    dest="outdir",   default=None)
parser.add_option("--label",     dest="label",    default='')
parser.add_option("--nEvts",     dest="nEvts",    type=int, default=-1)
parser.add_option("--target",    dest="target",   default=None)
parser.add_option("--raw",       dest="raw",      action='store_true', default=False)
parser.add_option("--unpacked",  dest="unpacked", action='store_true', default=False)
parser.add_option("--no_plot",   dest="no_plot",  action='store_true', default=False)
parser.add_option("--plot_only", dest="plot_only",action='store_true', default=False)
parser.add_option("--HCALcalib", dest="HCALcalib",action='store_true', default=False)
parser.add_option("--ECALcalib", dest="ECALcalib",action='store_true', default=False)
parser.add_option("--caloParam", dest="caloParam",type=str,   default='')
(options, args) = parser.parse_args()
print(options)

cmap = plt.get_cmap('Set1')

# get/create folders
indir = "/data_CMS/cms/motta/CaloL1calibraton/L1NTuples/"+options.indir
outdir = options.outdir
label = options.label
os.system('mkdir -p '+outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs')
os.system('mkdir -p '+outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs')
os.system('mkdir -p '+outdir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs')

if not options.plot_only:

    print(" ### INFO: Start loading data")

    # define level1Tree
    if options.unpacked: level1TreeName = "l1UpgradeTree/L1UpgradeTree"
    else:                level1TreeName = "l1UpgradeEmuTree/L1UpgradeTree"
    level1Tree = ROOT.TChain(level1TreeName)
    level1Tree.Add(indir+"/Ntuple*.root")

    # define towersTree
    towersTreeName = "l1CaloTowerEmuTree/L1CaloTowerTree"
    towersTree = ROOT.TChain(towersTreeName)
    towersTree.Add(indir+"/Ntuple*.root")
    level1Tree.AddFriend(towersTree, towersTreeName)

    df = ROOT.RDataFrame(level1Tree)

    print(" ### INFO: End loading data")

    nEntries = df.Count().GetValue()
    print(" ### INFO: Total entries", nEntries)

    # run on entries specified by user, or only on entries available if that is exceeded
    nevents = options.nEvts
    if (nevents > nEntries) or (nevents==-1): nevents = nEntries
    df = df.Range(nevents)

    print(" ### INFO: Reading", nevents, "events")
    df = df.Range(nevents)

    ##################################################################
    ##################################################################

    if options.target == 'jet':

        # online
        df = df.Define("L1_n",      "L1Upgrade.nJets")
        df = df.Define("L1_eta",    "L1Upgrade.jetEta")
        df = df.Define("L1_phi",    "L1Upgrade.jetPhi")
        if options.raw: df = df.Define("L1_pt",     "L1Upgrade.jetRawEt / 2")
        else:           df = df.Define("L1_pt",     "L1Upgrade.jetEt")

    ##################################################################
    ##################################################################
            
    if options.target == 'ele':
        
        # online
        df = df.Define("L1_n",      "L1Upgrade.nEGs")
        df = df.Define("L1_eta",    "L1Upgrade.egEta")
        df = df.Define("L1_phi",    "L1Upgrade.egPhi")
        if options.raw: df = df.Define("L1_pt",     "L1Upgrade.egRawEt / 2")
        else:           df = df.Define("L1_pt",     "L1Upgrade.egEt")
    
    ##################################################################
    ##################################################################
        
    df = df.Define("TT_ieta", "L1CaloTower.ieta")
    df = df.Define("TT_iphi", "L1CaloTower.iphi")
    df = df.Define("TT_iem",  "L1CaloTower.iem")
    df = df.Define("TT_ihc",  "L1CaloTower.ihad")
    df = df.Define("TT_iet",  "L1CaloTower.iet")
    # Define overall hcalET information, ihad for ieta < 29 and iet for ieta > 29
    df = df.Define("TT_ihad", "SumHCAL (TT_ihc, TT_iet, TT_ieta)")

    if options.HCALcalib or options.ECALcalib:

        from RDF_Calibration import *
        caloParams_file = "/data_CMS/cms/vernazza/L1TCalibration/CMSSW_13_1_0_pre4_Fix/CMSSW_13_1_0_pre4/src/CaloL1CalibrationProducer/caloParams/" + options.caloParam
        save_folder = outdir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs'

        ROOT.load_HCAL_SFs(caloParams_file, save_folder)
        ROOT.load_HF_SFs(caloParams_file, save_folder)
        df = df.Redefine("TT_ihad", "CalibrateIhad(TT_ieta, TT_ihad, {})".format(str(options.HCALcalib).lower()))
        
        ROOT.load_ECAL_SFs(caloParams_file, save_folder)
        df = df.Redefine("TT_iem", "CalibrateIem(TT_ieta, TT_iem, {})".format(str(options.ECALcalib).lower()))

    df = df.Define("TT_iesum", "GetSum (TT_iem, TT_ihad)")

    df = df.Define("lead_jet", "BuildLeadingJets (TT_ieta, TT_iphi, TT_iesum, 2.5).at(0)")
    # df = df.Define("subl_jet", "BuildLeadingJets (TT_ieta, TT_iphi, TT_iesum, 2.5).at(1)")

    df = df.Define("lead_L1_jet", "LeadingJets (L1_pt, L1_eta, L1_phi, 2.5).at(0)")
    # df = df.Define("subl_L1_jet", "LeadingJets (L1_pt, L1_eta, L1_phi, 2.5).at(1)")

    print(" ### Define histograms")
    
    histo1 = df.Histo1D("lead_jet")
    histo2 = df.Histo1D("lead_L1_jet")
    # histo2 = df.Histo2D(("Ratio2", "", 50, 0, 2, 50, 0, 500), "Ratio", "good_L1_pt")

    f = ROOT.TFile("./test.root","RECREATE")
    histo1.Write(); 
    histo2.Write(); 
    f.Close()

    sys.exit()

    ##################################################################
    ##################################################################

    lead_pt_name = "lead_CD_iesum"
    subl_pt_name = "subl_CD_iesum"

    for region in ['Inclusive', 'er2p5', 'er1p305']:
        
        if region == 'Inclusive': etacut = 5;     suf = ''
        if region == 'er2p5':     etacut = 2.5;   suf = '_'+region
        if region == 'er1p305':   etacut = 1.305; suf = '_'+region

        df = df.Define(f"lead_L1_id{suf}", "LeadingJets(L1_pt, L1_eta, L1_phi, {}).at(0)".format(etacut))
        df = df.Define(f"subl_L1_id{suf}", "LeadingJets(L1_pt, L1_eta, L1_phi, {}).at(1)".format(etacut))

        df = df.Filter(f"(lead_L1_id{suf} != -1) && (subl_L1_id{suf} != -1)")
        df = df.Define(f"lead_L1_pt{suf}",    f"L1_pt.at(lead_L1_id{suf})")
        df = df.Define(f"lead_L1_eta{suf}",   f"L1_eta.at(lead_L1_id{suf})")
        df = df.Define(f"lead_L1_phi{suf}",   f"L1_phi.at(lead_L1_id{suf})")
        df = df.Define(f"subl_L1_pt{suf}",    f"L1_pt.at(subl_L1_id{suf})")
        df = df.Define(f"subl_L1_eta{suf}",   f"L1_eta.at(subl_L1_id{suf})")
        df = df.Define(f"subl_L1_phi{suf}",   f"L1_phi.at(subl_L1_id{suf})")

        # ##################################################################    
        # ######################### CHUNKY DONUT ###########################

        df = df.Define(f"lead_L1_ieta{suf}", f"FindIeta(lead_L1_eta{suf})")
        df = df.Define(f"lead_L1_iphi{suf}", f"FindIphi(lead_L1_phi{suf})")
        df = df.Define(f"lead_CD_iem{suf}",  f"ChunkyDonutEnergy (lead_L1_ieta{suf}, lead_L1_iphi{suf}, TT_ieta, TT_iphi, TT_iem, TT_ihad, TT_iet).at(0)")
        df = df.Define(f"lead_CD_ihad{suf}", f"ChunkyDonutEnergy (lead_L1_ieta{suf}, lead_L1_iphi{suf}, TT_ieta, TT_iphi, TT_iem, TT_ihad, TT_iet).at(1)")
        df = df.Define(f"lead_CD_iesum{suf}", f"lead_CD_iem{suf} + lead_CD_ihad{suf}")

        df = df.Define(f"subl_L1_ieta{suf}", f"FindIeta(subl_L1_eta{suf})")
        df = df.Define(f"subl_L1_iphi{suf}", f"FindIphi(subl_L1_phi{suf})")
        df = df.Define(f"subl_CD_iem{suf}",  f"ChunkyDonutEnergy (subl_L1_ieta{suf}, subl_L1_iphi{suf}, TT_ieta, TT_iphi, TT_iem, TT_ihad, TT_iet).at(0)")
        df = df.Define(f"subl_CD_ihad{suf}", f"ChunkyDonutEnergy (subl_L1_ieta{suf}, subl_L1_iphi{suf}, TT_ieta, TT_iphi, TT_iem, TT_ihad, TT_iet).at(1)")
        df = df.Define(f"subl_CD_iesum{suf}", f"subl_CD_iem{suf} + subl_CD_ihad{suf}")

        if options.HCALcalib or options.ECALcalib:
            
            df = df.Define(f"lead_CD_iem_calib{suf}",  f"ChunkyDonutEnergy (lead_L1_ieta{suf}, lead_L1_iphi{suf}, TT_ieta, TT_iphi, TT_iem_calib, TT_ihad_calib, TT_iet).at(0)")
            df = df.Define(f"lead_CD_ihad_calib{suf}", f"ChunkyDonutEnergy (lead_L1_ieta{suf}, lead_L1_iphi{suf}, TT_ieta, TT_iphi, TT_iem_calib, TT_ihad_calib, TT_iet).at(1)")
            df = df.Define(f"lead_CD_iesum_calib{suf}", f"lead_CD_iem_calib{suf} + lead_CD_ihad_calib{suf}")

            df = df.Define(f"subl_CD_iem_calib{suf}",  f"ChunkyDonutEnergy (subl_L1_ieta{suf}, subl_L1_iphi{suf}, TT_ieta, TT_iphi, TT_iem_calib, TT_ihad_calib, TT_iet).at(0)")
            df = df.Define(f"subl_CD_ihad_calib{suf}", f"ChunkyDonutEnergy (subl_L1_ieta{suf}, subl_L1_iphi{suf}, TT_ieta, TT_iphi, TT_iem_calib, TT_ihad_calib, TT_iet).at(1)")
            df = df.Define(f"subl_CD_iesum_calib{suf}", f"subl_CD_iem_calib{suf} + subl_CD_ihad_calib{suf}")

    #################################################################    
    ########################## HISTOGRAMS ###########################

    print("\n ### INFO: Define pt progression histograms")
    
    nbins = 240; min = 0; max = 240
    ptProgression0 = df.Histo1D(("ptProgression0", "ptProgression0", nbins, min, max), lead_pt_name)
    ptDiProgression0 = df.Histo2D(("ptDiProgression0", "ptDiProgression0", nbins, min, max, nbins, min, max), lead_pt_name, subl_pt_name)
    ptProgression0er2p5 = df.Histo1D(("ptProgression0er2p5", "ptProgression0er2p5", nbins, min, max), lead_pt_name+'_er2p5')
    ptDiProgression0er2p5 = df.Histo2D(("ptDiProgression0er2p5", "ptDiProgression0er2p5", nbins, min, max, nbins, min, max), lead_pt_name+'_er2p5', subl_pt_name+'_er2p5')
    ptProgression0er1p305 = df.Histo1D(("ptProgression0er1p305", "ptProgression0er1p305", nbins, min, max), lead_pt_name+'_er1p305')
    ptDiProgression0er1p305 = df.Histo2D(("ptDiProgression0er1p305", "ptDiProgression0er1p305", nbins, min, max, nbins, min, max), lead_pt_name+'_er1p305', subl_pt_name+'_er1p305')

    ##################################################################    
    ############################### RATE #############################
        
    print(" ### INFO: Compute rate")

    nb = 2544.
    scale = 0.001*(nb*11245.6)
    denominator = df.Count().GetValue()

    rateProgression0 = ROOT.TH1F("rateProgression0","rateProgression0",240,0.,240.)
    rateDiProgression0 = ROOT.TH1F("rateDiProgression0","rateDiProgression0",240,0.,240.)
    rateProgression0er2p5 = ROOT.TH1F("rateProgression0er2p5","rateProgression0er2p5",240,0.,240.)
    rateDiProgression0er2p5 = ROOT.TH1F("rateDiProgression0er2p5","rateProgression0er2p5",240,0.,240.)
    rateProgression0er1p305 = ROOT.TH1F("rateProgression0er1p305","rateProgression0er1p305",240,0.,240.)
    rateDiProgression0er1p305 = ROOT.TH1F("rateDiProgression0er1p305","rateDiProgression0er1p305",240,0.,240.)
    for i in range(0,241):
        rateProgression0.SetBinContent(i+1,ptProgression0.Integral(i+1,241)/denominator*scale)
        rateDiProgression0.SetBinContent(i+1,ptDiProgression0.Integral(i+1,241,i+1,241)/denominator*scale)
        rateProgression0er2p5.SetBinContent(i+1,ptProgression0er2p5.Integral(i+1,241)/denominator*scale)
        rateDiProgression0er2p5.SetBinContent(i+1,ptDiProgression0er2p5.Integral(i+1,241,i+1,241)/denominator*scale)
        rateProgression0er1p305.SetBinContent(i+1,ptProgression0er1p305.Integral(i+1,241)/denominator*scale)
        rateDiProgression0er1p305.SetBinContent(i+1,ptDiProgression0er1p305.Integral(i+1,241,i+1,241)/denominator*scale)

    print(" ### INFO: Saving to root format")

    fileout = ROOT.TFile(outdir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs/rate_graphs_'+label+'_'+options.target+'.root','RECREATE')
    ptProgression0.Write()
    ptDiProgression0.Write()
    rateProgression0.Write()
    rateDiProgression0.Write()
    ptProgression0er2p5.Write()
    ptDiProgression0er2p5.Write()
    rateProgression0er2p5.Write()
    rateDiProgression0er2p5.Write()
    ptProgression0er1p305.Write()
    ptDiProgression0er1p305.Write()
    rateProgression0er1p305.Write()
    rateDiProgression0er1p305.Write()
    fileout.Close()

    if options.no_plot:
        sys.exit()

    ############################################################################################
    ############################################################################################
    ############################################################################################

else:
    print(" ### INFO: Read existing root files")
    filein = ROOT.TFile(outdir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs/resolution_graphs_'+label+'_'+options.target+'.root')
    ptProgression0 = filein.Get('ptProgression0')
    ptDiProgression0 = filein.Get('ptDiProgression0')
    rateProgression0 = filein.Get('rateProgression0')
    rateDiProgression0 = filein.Get('rateDiProgression0')
    ptProgression0er2p5 = filein.Get('ptProgression0er2p5')
    ptDiProgression0er2p5 = filein.Get('ptDiProgression0er2p5')
    rateProgression0er2p5 = filein.Get('rateProgression0er2p5')
    rateDiProgression0er2p5 = filein.Get('rateDiProgression0er2p5')
    ptProgression0er1p305 = filein.Get('ptProgression0er1p305')
    ptDiProgression0er1p305 = filein.Get('ptDiProgression0er1p305')
    rateProgression0er1p305 = filein.Get('rateProgression0er1p305')
    rateDiProgression0er1p305 = filein.Get('rateDiProgression0er1p305')

############################################################################################
print(" ### INFO: Produce plots inclusive")
############################################################################################

if options.target == 'jet':
    label_singleObj = r'Single-jet'
    label_doubleObj = r'Double-jet'
    x_label = r'$E_{T}^{jet, L1}$'
if options.target == 'ele':
    label_singleObj = r'Single-$e/\gamma$'
    label_doubleObj = r'Double-$e/\gamma$'
    x_label = r'$E_{T}^{e/\gamma, L1}$'

fig, ax = plt.subplots(figsize=(10,10))

X = [] ; Y = [] ; X_err = [] ; Y_err = []
histo = rateProgression0
for ibin in range(0,histo.GetNbinsX()):
    X.append(histo.GetBinLowEdge(ibin+1) + histo.GetBinWidth(ibin+1)/2.)
    Y.append(histo.GetBinContent(ibin+1))
    X_err.append(histo.GetBinWidth(ibin+1)/2.)
    Y_err.append(histo.GetBinError(ibin+1))
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=label_singleObj, lw=2, marker='o', color=cmap(0))

X = [] ; Y = [] ; X_err = [] ; Y_err = []
histo = rateDiProgression0
for ibin in range(0,histo.GetNbinsX()):
    X.append(histo.GetBinLowEdge(ibin+1) + histo.GetBinWidth(ibin+1)/2.)
    Y.append(histo.GetBinContent(ibin+1))
    X_err.append(histo.GetBinWidth(ibin+1)/2.)
    Y_err.append(histo.GetBinError(ibin+1))
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=label_doubleObj, lw=2, marker='o', color=cmap(1))

for xtick in ax.xaxis.get_major_ticks():
    xtick.set_pad(10)
leg = plt.legend(loc = 'upper right', fontsize=20)
leg._legend_box.align = "left"
plt.xlabel(x_label)
plt.ylabel('Rate [kHz]')
plt.xlim(0, 120)
plt.ylim(0.1, 1E5)
# plt.xscale('symlog')
plt.yscale('log')
for xtick in ax.xaxis.get_major_ticks():
    xtick.set_pad(10)
plt.grid()
mplhep.cms.label('Preliminary', data=True, rlabel=r'110 pb$^{-1}$ (13.6 TeV)') ## 110pb-1 is Run 362617
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/rate_'+label+'_'+options.target+'.pdf')
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/rate_'+label+'_'+options.target+'.png')
plt.close()

############################################################################################
print(" ### INFO: Produce plots Eta restricted 2.5")
############################################################################################

if options.target == 'jet':
    label_singleObj = r'Single-jet $|\eta|<2.5$'
    label_doubleObj = r'Double-jet $|\eta|<2.5$'
    x_label = r'$E_{T}^{jet, L1}$'
if options.target == 'ele':
    label_singleObj = r'Single-$e/\gamma$ $|\eta|<2.5$'
    label_doubleObj = r'Double-$e/\gamma$ $|\eta|<2.5$'
    x_label = r'$E_{T}^{e/\gamma, L1}$'

fig, ax = plt.subplots(figsize=(10,10))

X = [] ; Y = [] ; X_err = [] ; Y_err = []
histo = rateProgression0er2p5
for ibin in range(0,histo.GetNbinsX()):
    X.append(histo.GetBinLowEdge(ibin+1) + histo.GetBinWidth(ibin+1)/2.)
    Y.append(histo.GetBinContent(ibin+1))
    X_err.append(histo.GetBinWidth(ibin+1)/2.)
    Y_err.append(histo.GetBinError(ibin+1))
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=label_singleObj, lw=2, marker='o', color=cmap(0))

X = [] ; Y = [] ; X_err = [] ; Y_err = []
histo = rateDiProgression0er2p5
for ibin in range(0,histo.GetNbinsX()):
    X.append(histo.GetBinLowEdge(ibin+1) + histo.GetBinWidth(ibin+1)/2.)
    Y.append(histo.GetBinContent(ibin+1))
    X_err.append(histo.GetBinWidth(ibin+1)/2.)
    Y_err.append(histo.GetBinError(ibin+1))
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=label_doubleObj, lw=2, marker='o', color=cmap(1))

for xtick in ax.xaxis.get_major_ticks():
    xtick.set_pad(10)
leg = plt.legend(loc = 'upper right', fontsize=20)
leg._legend_box.align = "left"
plt.xlabel(x_label)
plt.ylabel('Rate [kHz]')
plt.xlim(0, 120)
# plt.xscale('symlog')
plt.ylim(0.1, 1E5)
plt.yscale('log')
for xtick in ax.xaxis.get_major_ticks():
    xtick.set_pad(10)
plt.grid()
mplhep.cms.label('Preliminary', data=True, rlabel=r'110 pb$^{-1}$ (13.6 TeV)') ## 110pb-1 is Run 362617
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/rateEr2p5_'+label+'_'+options.target+'.pdf')
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/rateEr2p5_'+label+'_'+options.target+'.png')
plt.close()

############################################################################################
print(" ### INFO: Produce plots Eta restricted 1.305")
############################################################################################

if options.target == 'jet':
    label_singleObj = r'Single-jet $|\eta|<1.305$'
    label_doubleObj = r'Double-jet $|\eta|<1.305$'
    x_label = r'$E_{T}^{jet, L1}$'
if options.target == 'ele':
    label_singleObj = r'Single-$e/\gamma$ $|\eta|<1.305$'
    label_doubleObj = r'Double-$e/\gamma$ $|\eta|<1.305$'
    x_label = r'$E_{T}^{e/\gamma, L1}$'

fig, ax = plt.subplots(figsize=(10,10))

X = [] ; Y = [] ; X_err = [] ; Y_err = []
histo = rateProgression0er1p305
for ibin in range(0,histo.GetNbinsX()):
    X.append(histo.GetBinLowEdge(ibin+1) + histo.GetBinWidth(ibin+1)/2.)
    Y.append(histo.GetBinContent(ibin+1))
    X_err.append(histo.GetBinWidth(ibin+1)/2.)
    Y_err.append(histo.GetBinError(ibin+1))
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=label_singleObj, lw=2, marker='o', color=cmap(0))

X = [] ; Y = [] ; X_err = [] ; Y_err = []
histo = rateDiProgression0er1p305
for ibin in range(0,histo.GetNbinsX()):
    X.append(histo.GetBinLowEdge(ibin+1) + histo.GetBinWidth(ibin+1)/2.)
    Y.append(histo.GetBinContent(ibin+1))
    X_err.append(histo.GetBinWidth(ibin+1)/2.)
    Y_err.append(histo.GetBinError(ibin+1))
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=label_doubleObj, lw=2, marker='o', color=cmap(1))

for xtick in ax.xaxis.get_major_ticks():
    xtick.set_pad(10)
leg = plt.legend(loc = 'upper right', fontsize=20)
leg._legend_box.align = "left"
plt.xlabel(x_label)
plt.ylabel('Rate [kHz]')
plt.xlim(0, 120)
# plt.xscale('symlog')
plt.ylim(0.1, 1E5)
plt.yscale('log')
for xtick in ax.xaxis.get_major_ticks():
    xtick.set_pad(10)
plt.grid()
mplhep.cms.label('Preliminary', data=True, rlabel=r'110 pb$^{-1}$ (13.6 TeV)') ## 110pb-1 is Run 362617
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/rateEr1p305_'+label+'_'+options.target+'.pdf')
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/rateEr1p305_'+label+'_'+options.target+'.png')
plt.close()

