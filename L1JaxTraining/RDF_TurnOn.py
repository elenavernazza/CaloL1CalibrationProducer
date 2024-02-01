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

def GetArraysFromHisto(histo):
    X = [] ; Y = [] ; X_err = [] ; Y_err = []
    for ibin in range(0,histo.GetNbinsX()):
        X.append(histo.GetBinLowEdge(ibin+1) + histo.GetBinWidth(ibin+1)/2.)
        Y.append(histo.GetBinContent(ibin+1))
        X_err.append(histo.GetBinWidth(ibin+1)/2.)
        Y_err.append(histo.GetBinError(ibin+1))
    return X,Y,X_err,Y_err

'''
python3 RDF_Resolution.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
 --reco --target jet --do_HoTot --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot \
 --HCALcalib --caloParam caloParams_2023_JAX4_newCalib_cfi.py --outdir 4
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
parser.add_option("--reco",      dest="reco",     action='store_true', default=False)
parser.add_option("--gen",       dest="gen",      action='store_true', default=False)
parser.add_option("--unpacked",  dest="unpacked", action='store_true', default=False)
parser.add_option("--raw",       dest="raw",      action='store_true', default=False)
parser.add_option("--LooseEle",  dest="LooseEle", action='store_true', default=False)
parser.add_option("--PuppiJet",  dest="PuppiJet", action='store_true', default=False)
parser.add_option("--plot_only", dest="plot_only",action='store_true', default=False)
parser.add_option("--no_plot",   dest="no_plot",  action='store_true', default=False)
parser.add_option("--norm",      dest="norm",     action='store_true', default=False)
parser.add_option("--HCALcalib", dest="HCALcalib",action='store_true', default=False)
parser.add_option("--ECALcalib", dest="ECALcalib",action='store_true', default=False)
parser.add_option("--caloParam", dest="caloParam",type=str,   default='')
parser.add_option("--no_CD",     dest="no_CD",   action='store_true', default=False)
(options, args) = parser.parse_args()

cmap = plt.get_cmap('Set1')

# get/create folders
indir = "/data_CMS/cms/motta/CaloL1calibraton/L1NTuples/"+options.indir
outdir = options.outdir
label = options.label
os.system('mkdir -p '+outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs')
os.system('mkdir -p '+outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs')
os.system('mkdir -p '+outdir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs')

#defining binning of histogram
if options.target == 'jet':
    ptBins  = [15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 90, 110, 130, 160, 200, 500]
    etaBins = [0., 0.5, 1.0, 1.305, 1.479, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.191]
    signedEtaBins = [-5.191, -4.5, -4.0, -3.5, -3.0, -2.5, -2.0, -1.479, -1.305, -1.0, -0.5, 0., 0.5, 1.0, 1.305, 1.479, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.191]
if options.target == 'ele':
    ptBins  = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 90, 110, 130, 160, 200]
    etaBins = [0., 0.5, 1.0, 1.305, 1.479, 2.0, 2.5, 3.0]
    signedEtaBins = [-3.0, -2.5, -2.0, -1.479, -1.305, -1.0, -0.5, 0., 0.5, 1.0, 1.305, 1.479, 2.0, 2.5, 3.0]
if options.target == 'met':
    ptBins  = [10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 90, 110, 130, 160, 200, 500]
    etaBins = [0., 5.191]
    signedEtaBins = [-5.191, 0., 5.191]
HoTotBins = [0, 0.4, 0.8, 0.95, 1.0]
EoTotBins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
x_lim_response = (0,3)
res_bins = 240

thresholds = np.arange(8,150+1)
thresholds2plot = [10, 20, 35, 50, 100, 150]

if not options.plot_only:

    print(" ### INFO: Start loading data")

    # define targetTree
    if options.reco:
        if options.target == 'jet': targetTree = ROOT.TChain("l1JetRecoTree/JetRecoTree")
        if options.target == 'ele': targetTree = ROOT.TChain("l1ElectronRecoTree/ElectronRecoTree")
        if options.target == 'met': targetTree = ROOT.TChain("l1JetRecoTree/JetRecoTree")
    if options.gen:
        targetTree = ROOT.TChain("l1GeneratorTree/L1GenTree")
    targetTree.Add(indir+"/Ntuple*.root")

    # define level1Tree
    if options.unpacked: level1TreeName = "l1UpgradeTree/L1UpgradeTree"
    else:                level1TreeName = "l1UpgradeEmuTree/L1UpgradeTree"
    level1Tree = ROOT.TChain(level1TreeName)
    level1Tree.Add(indir+"/Ntuple*.root")
    targetTree.AddFriend(level1Tree, level1TreeName)

    # define towersTree
    towersTreeName = "l1CaloTowerEmuTree/L1CaloTowerTree"
    towersTree = ROOT.TChain(towersTreeName)
    towersTree.Add(indir+"/Ntuple*.root")
    targetTree.AddFriend(towersTree, towersTreeName)

    df = ROOT.RDataFrame(targetTree)

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

        # offline
        if options.PuppiJet:
            df = df.Define("Offline_n",     "Jet.puppi_nJets")
            df = df.Define("Offline_pt",    "Jet.puppi_etCorr")
            df = df.Define("Offline_eta",   "Jet.puppi_eta")
            df = df.Define("Offline_phi",   "Jet.puppi_phi")
        else:
            df = df.Define("Offline_n",     "Jet.nJets")
            df = df.Define("Offline_pt",    "Jet.etCorr")
            df = df.Define("Offline_eta",   "Jet.eta")
            df = df.Define("Offline_phi",   "Jet.phi")

    ##################################################################
    ##################################################################
            
    if options.target == 'ele':
        
        # online
        df = df.Define("L1_n",      "L1Upgrade.nEGs")
        df = df.Define("L1_eta",    "L1Upgrade.egEta")
        df = df.Define("L1_phi",    "L1Upgrade.egPhi")
        if options.raw: df = df.Define("L1_pt",     "L1Upgrade.egRawEt / 2")
        else:           df = df.Define("L1_pt",     "L1Upgrade.egEt")

        # offline
        df = df.Define("Offline_n",     "Electron.nElectrons")
        df = df.Define("Offline_pt",    "Electron.et")
        df = df.Define("Offline_eta",   "Electron.eta")
        df = df.Define("Offline_phi",   "Electron.phi")

    ##################################################################
    ##################################################################
        
    if options.target == 'met':

        # online
        df = df.Define("L1_n",      "L1Upgrade.nSums")
        df = df.Define("L1_eta",    0)
        df = df.Define("L1_phi",    0)
        df = df.Define("L1_pt",     "L1Upgrade.sumIEt / 2").Filter("L1Upgrade.sumType == 8")
        
        # offline
        df = df.Define("Offline_n",     1)
        df = df.Define("Offline_eta",   0)
        df = df.Define("Offline_phi",   0)
        if options.PuppiJet:
            df = df.Define("Offline_pt", "Sums.puppi_metNoMu")
        else:
            df = df.Define("Offline_pt", "Sums.pfMetNoMu")

    ##################################################################    
    ########################### MATCHING #############################

    df = df.Define("good_L1_id", "Matching(Offline_pt, Offline_eta, Offline_phi, L1_pt, L1_eta, L1_phi).at(1)")
    df = df.Define("good_Of_id", "Matching(Offline_pt, Offline_eta, Offline_phi, L1_pt, L1_eta, L1_phi).at(0)")

    df = df.Filter("(good_L1_id.size() > 0) && (good_Of_id.size() > 0)")

    df = df.Define("good_L1_pt",    "SelectGood (L1_pt, good_L1_id)")
    df = df.Define("good_L1_eta",   "SelectGood (L1_eta, good_L1_id)")
    df = df.Define("good_L1_phi",   "SelectGood (L1_phi, good_L1_id)")
    df = df.Define("good_Of_pt",    "SelectGood (Offline_pt, good_Of_id)")
    df = df.Define("good_Of_eta",   "SelectGood (Offline_eta, good_Of_id)")
    df = df.Define("good_Of_phi",   "SelectGood (Offline_phi, good_Of_id)")

    print(" ### INFO: Number of good events = ", df.Count().GetValue())

    # Define response for matched jets
    df = df.Define("Response", "GetRatio (good_L1_pt, good_Of_pt)")
    # DEBUG df = df.Redefine("Response", "vector<float>(Response.begin(), Response.end())")
    # DEBUG df.Snapshot("Events", "./test.root", {"good_L1_pt", "good_Of_pt", "Response"})

    ##################################################################    
    ######################### CHUNKY DONUT ###########################

    df = df.Define("TT_ieta", "L1CaloTower.ieta")
    df = df.Define("TT_iphi", "L1CaloTower.iphi")
    df = df.Define("TT_iem",  "L1CaloTower.iem")
    df = df.Define("TT_ihc",  "L1CaloTower.ihad")
    df = df.Define("TT_iet",  "L1CaloTower.iet")
    # Define overall hcalET information, ihad for ieta < 29 and iet for ieta > 29
    df = df.Define("TT_ihad", "SumHCAL (TT_ihc, TT_iet, TT_ieta)")

    df = df.Define("good_L1_ieta", "FindIeta(good_L1_eta)")
    df = df.Define("good_L1_iphi", "FindIphi(good_L1_phi)")

    df = df.Define("CD_iem",  "ChunkyDonutEnergy (good_L1_ieta, good_L1_iphi, TT_ieta, TT_iphi, TT_iem, TT_ihad, TT_iet).at(0)")
    df = df.Define("CD_ihad", "ChunkyDonutEnergy (good_L1_ieta, good_L1_iphi, TT_ieta, TT_iphi, TT_iem, TT_ihad, TT_iet).at(1)")
    df = df.Define("CD_iet",  "ChunkyDonutEnergy (good_L1_ieta, good_L1_iphi, TT_ieta, TT_iphi, TT_iem, TT_ihad, TT_iet).at(2)")

    df = df.Define("CD_iesum", "GetSum (CD_iem, CD_ihad)")

    df = df.Define("HoTot", "GetRatio (CD_ihad, CD_iet)")
    df = df.Define("EoTot", "GetRatio (CD_iem, CD_iet)")

    # Define response for chunky donuts
    df = df.Define("Response_CD", "GetRatio (CD_iesum, good_Of_pt)")

    if options.no_CD: response_name = 'Response'
    else: response_name = 'Response_CD'

    if options.HCALcalib or options.ECALcalib:
        response_name = "Response_CD_calib"
        from RDF_Calibration import *
        caloParams_file = "/data_CMS/cms/vernazza/L1TCalibration/CMSSW_13_1_0_pre4_Fix/CMSSW_13_1_0_pre4/src/CaloL1CalibrationProducer/caloParams/" + options.caloParam
        save_folder = outdir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs'

        ROOT.load_HCAL_SFs(caloParams_file, save_folder)
        ROOT.load_HF_SFs(caloParams_file, save_folder)
        df = df.Define("TT_ihad_calib", "CalibrateIhad(TT_ieta, TT_ihad, {})".format(str(options.HCALcalib).lower()))
        
        ROOT.load_ECAL_SFs(caloParams_file, save_folder)
        df = df.Define("TT_iem_calib", "CalibrateIem(TT_ieta, TT_iem, {})".format(str(options.ECALcalib).lower()))
        
        df = df.Define("CD_iem_calib", "ChunkyDonutEnergy (good_L1_ieta, good_L1_iphi, TT_ieta, TT_iphi, TT_iem_calib, TT_ihad_calib, TT_iet).at(0)")
        df = df.Define("CD_ihad_calib", "ChunkyDonutEnergy (good_L1_ieta, good_L1_iphi, TT_ieta, TT_iphi, TT_iem_calib, TT_ihad_calib, TT_iet).at(1)")
        df = df.Define("CD_iesum_calib", "GetSum (CD_iem_calib, CD_ihad_calib)")
        df = df.Define("Response_CD_calib", "GetRatio (CD_iesum_calib, good_Of_pt)")
    
    # else:
    #     # [FIXME] understand why sometimes they are different
    #     df = df.Filter("(CD_iet == good_L1_pt) && (CD_iesum == good_L1_pt)")

    df_b = df.Redefine("good_Of_pt", "SelectBarrel (good_Of_pt, good_Of_eta)")
    df_b = df_b.Redefine("good_Of_eta", "SelectBarrel (good_Of_eta, good_Of_eta)")
    df_b = df_b.Redefine(response_name, "SelectBarrel ({}, good_Of_eta)".format(response_name))
    df_e = df.Redefine("good_Of_pt", "SelectEndcap (good_Of_pt, good_Of_eta)")
    df_e = df_e.Redefine("good_Of_eta", "SelectEndcap (good_Of_eta, good_Of_eta)")
    df_e = df_e.Redefine(response_name, "SelectEndcap ({}, good_Of_eta)".format(response_name))
    
    ##################################################################    
    ########################### DEBUGGING ############################

    # print("Test iem 1,1 =",ROOT.TestCalibrateIem(1,1))
    # print("Test ihad 1,1 =",ROOT.TestCalibrateIhad(1,1))

    # df = df.Define("Ratio", "GetRatio (CD_iesum, CD_iet)")
    # df = df.Define("Ratio", "GetRatio (CD_iesum, good_L1_pt)")

    # histo1 = df.Histo1D("Ratio")
    # histo2 = df.Histo2D(("Ratio2", "", 50, 0, 2, 50, 0, 500), "Ratio", "good_L1_pt")
    # histo3 = df.Histo2D(("Ratio3", "", 50, 0, 2, 50, -5, 5), "Ratio", "good_L1_eta")
    # histo4 = df.Histo2D(("Ratio4", "", 50, 0, 2, 50, -5, 5), "Ratio", "good_L1_phi")
    # histo5 = df.Histo2D(("Ieta", "", 42, 0, 41, 50, -5, 5), "good_L1_ieta", "good_L1_eta")
    # histo6 = df.Histo2D(("Iphi", "", 73, 0, 72, 50, -5, 5), "good_L1_iphi", "good_L1_phi")

    # f = ROOT.TFile("./test.root","RECREATE")
    # histo1.Write(); histo2.Write(); histo3.Write(); histo4.Write(); histo5.Write(); histo6.Write()
    # f.Close()

    ##################################################################    
    ########################### TURN ON CURVES #######################

    print("\n ### INFO: Computing turn ons for thresholds [{}, ... {}]".format(thresholds[0], thresholds[-1]))
    bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 100, 120, 150, 180, 250]

    L1Pt_name = "CD_iesum"
    if options.HCALcalib or options.ECALcalib:
        L1Pt_name = "CD_iesum_calib"
    if options.no_CD: L1Pt_name = 'good_L1_pt'

    OffEta_name = "good_Of_eta"
    OffPt_name = "good_Of_pt"

    total = df.Histo1D(("total", "total", len(bins)-1, array('f',bins)), OffPt_name)

    df_er2p5 = df.Redefine(OffEta_name, "SelectBinAbs ({}, {}, 0, 2.5)".format(OffEta_name, OffEta_name))
    df_er2p5 = df_er2p5.Redefine(OffPt_name, "SelectBinAbs ({}, {}, 0, 2.5)".format(OffPt_name, OffEta_name))
    df_er2p5 = df_er2p5.Redefine(L1Pt_name, "SelectBinAbs ({}, {}, 0, 2.5)".format(L1Pt_name, OffEta_name))
    total_er2p5 = df_er2p5.Histo1D(("total_Er2p5", "total_Er2p5", len(bins)-1, array('f',bins)), OffPt_name)

    df_er1p305 = df.Redefine(OffEta_name, "SelectBinAbs ({}, {}, 0, 1.305)".format(OffEta_name, OffEta_name))
    df_er1p305 = df_er1p305.Redefine(OffPt_name, "SelectBinAbs ({}, {}, 0, 1.305)".format(OffPt_name, OffEta_name))
    df_er1p305 = df_er1p305.Redefine(L1Pt_name, "SelectBinAbs ({}, {}, 0, 1.305)".format(L1Pt_name, OffEta_name))
    total_er1p305 = df_er1p305.Histo1D(("total_Er1p305", "total_Er1p305", len(bins)-1, array('f',bins)), OffPt_name)

    passing = []
    for i, threshold in enumerate(thresholds):
        df_cut = df.Redefine(OffPt_name, "PassThreshold ({}, {}, {})".format(OffPt_name, L1Pt_name, threshold))
        name = "passing_"+str(int(threshold))
        passing.append(df_cut.Histo1D((name, name, len(bins)-1, array('f',bins)), OffPt_name))

    passing_er2p5 = []
    for i, threshold in enumerate(thresholds):
        df_er2p5_cut = df_er2p5.Redefine(OffPt_name, "PassThreshold ({}, {}, {})".format(OffPt_name, L1Pt_name, threshold))
        name = "passing_Er2p5_"+str(int(threshold))
        passing_er2p5.append(df_er2p5_cut.Histo1D((name, name, len(bins)-1, array('f',bins)), OffPt_name))

    passing_er1p305 = []
    for i, threshold in enumerate(thresholds):
        df_er1p305_cut = df_er1p305.Redefine(OffPt_name, "PassThreshold ({}, {}, {})".format(OffPt_name, L1Pt_name, threshold))
        name = "passing_Er1p305_"+str(int(threshold))
        passing_er1p305.append(df_er1p305_cut.Histo1D((name, name, len(bins)-1, array('f',bins)), OffPt_name))

    print(" ### INFO: Saving turn on to root format")
    fileout = ROOT.TFile(outdir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs/efficiency_histos_'+label+'_'+options.target+'.root','RECREATE')
    total.Write()
    total_er2p5.Write()
    total_er1p305.Write()
    for i, thr in enumerate(thresholds): 
        passing[i].Write()
        passing_er2p5[i].Write()
        passing_er1p305[i].Write()
    fileout.Close()

    filein = ROOT.TFile(outdir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs/efficiency_histos_'+label+'_'+options.target+'.root')
    total = filein.Get('total')
    total_er2p5 = filein.Get('total_Er2p5')
    total_er1p305 = filein.Get('total_Er1p305')
    passing = []
    turnons = []
    passing_er2p5 = []
    turnons_er2p5 = []
    passing_er1p305 = []
    turnons_er1p305 = []
    for i, thr in enumerate(thresholds): 
        passing.append(filein.Get("passing_"+str(int(thr))))
        turnons.append(ROOT.TGraphAsymmErrors(passing[i], total, "cp"))
        passing_er2p5.append(filein.Get("passing_Er2p5_"+str(int(thr))))
        turnons_er2p5.append(ROOT.TGraphAsymmErrors(passing_er2p5[i], total_er2p5, "cp"))
        passing_er1p305.append(filein.Get("passing_Er1p305_"+str(int(thr))))
        turnons_er1p305.append(ROOT.TGraphAsymmErrors(passing_er1p305[i], total_er1p305, "cp"))
    filein.Close()

    fileout = ROOT.TFile(outdir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs/efficiency_graphs_'+label+'_'+options.target+'.root','RECREATE')
    for i, thr in enumerate(thresholds): 
        turnons[i].Write()
        turnons_er2p5[i].Write()
        turnons_er1p305[i].Write()
    fileout.Close()

    if options.no_plot:
        sys.exit()

    ############################################################################################
    ############################################################################################
    ############################################################################################

############################################################################################
print(" ### INFO: Produce plots turn ons")
############################################################################################

filein = ROOT.TFile(outdir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs/efficiency_graphs_'+label+'_'+options.target+'.root')
turnons = []
turnons_er2p5 = []
turnons_er1p305 = []
for i, thr in enumerate(thresholds): 
    turnons.append(filein.Get(f'divide_passing_{thr}_by_total'))
    turnons_er2p5.append(filein.Get(f'divide_passing_Er2p5_{thr}_by_total_Er2p5'))
    turnons_er1p305.append(filein.Get(f'divide_passing_Er1p305_{thr}_by_total_Er1p305'))
filein.Close()

if options.reco:
    if options.target == 'jet': x_label = '$E_{T}^{jet, offline}$ [GeV]'
    if options.target == 'ele': x_label = '$E_{T}^{e, offline}$ [GeV]'
    if options.target == 'met': x_label = '$MET_{\mu corrected}^{offline}$ [GeV]'
if options.gen:
    x_label = '$E_{T}^{jet, gen}$ [GeV]'

def SetStyle(ax, x_label):
    for xtick in ax.xaxis.get_major_ticks():
        xtick.set_pad(10)
    leg = plt.legend(loc = 'lower right', fontsize=20)
    leg._legend_box.align = "left"
    plt.xlabel(x_label)
    plt.ylabel('Efficiency')
    plt.xlim(0, 220)
    plt.ylim(0, 1.05)
    plt.grid()
    if options.reco: mplhep.cms.label(data=False, rlabel='(13.6 TeV)')
    else:            mplhep.cms.label('Preliminary', data=True, rlabel=r'110 pb$^{-1}$ (13.6 TeV)') ## 110pb-1 is Run 362617

thresholds = list(thresholds)
# cmap = matplotlib.cm.get_cmap('tab20c')
fig, ax = plt.subplots(figsize=(10,10))
for i, thr in enumerate(thresholds2plot):
    X = [] ; Y = [] ; Y_low = [] ; Y_high = []
    turnon = turnons[thresholds.index(thr)]
    for ibin in range(0,turnon.GetN()):
        X.append(turnon.GetPointX(ibin))
        Y.append(turnon.GetPointY(ibin))
        Y_low.append(turnon.GetErrorYlow(ibin))
        Y_high.append(turnon.GetErrorYhigh(ibin))
    ax.errorbar(X, Y, xerr=1, yerr=[Y_low, Y_high], label="$p_{T}^{L1} > $"+str(thr)+" GeV", lw=2, marker='o', color=cmap(i))
SetStyle(ax, x_label)
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/turnOns_'+label+'_'+options.target+'.pdf')
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/turnOns_'+label+'_'+options.target+'.png')
plt.close()

fig, ax = plt.subplots(figsize=(10,10))
for i, thr in enumerate(thresholds2plot):
    X = [] ; Y = [] ; Y_low = [] ; Y_high = []
    turnon = turnons_er2p5[thresholds.index(thr)]
    for ibin in range(0,turnon.GetN()):
        X.append(turnon.GetPointX(ibin))
        Y.append(turnon.GetPointY(ibin))
        Y_low.append(turnon.GetErrorYlow(ibin))
        Y_high.append(turnon.GetErrorYhigh(ibin))
    ax.errorbar(X, Y, xerr=1, yerr=[Y_low, Y_high], label="$p_{T}^{L1} > $"+str(thr)+" GeV", lw=2, marker='o', color=cmap(i))
SetStyle(ax, x_label)
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/turnOns_Er2p5_'+label+'_'+options.target+'.pdf')
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/turnOns_Er2p5_'+label+'_'+options.target+'.png')
plt.close()

fig, ax = plt.subplots(figsize=(10,10))
for i, thr in enumerate(thresholds2plot):
    X = [] ; Y = [] ; Y_low = [] ; Y_high = []
    turnon = turnons_er1p305[thresholds.index(thr)]
    for ibin in range(0,turnon.GetN()):
        X.append(turnon.GetPointX(ibin))
        Y.append(turnon.GetPointY(ibin))
        Y_low.append(turnon.GetErrorYlow(ibin))
        Y_high.append(turnon.GetErrorYhigh(ibin))
    ax.errorbar(X, Y, xerr=1, yerr=[Y_low, Y_high], label="$p_{T}^{L1} > $"+str(thr)+" GeV", lw=2, marker='o', color=cmap(i))
SetStyle(ax, x_label)
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/turnOns_Er1p305_'+label+'_'+options.target+'.pdf')
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/turnOns_Er1p305_'+label+'_'+options.target+'.png')
plt.close()

