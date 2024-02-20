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
parser.add_option("--jetPtcut",  dest="jetPtcut", type=float, default=None)
parser.add_option("--etacut",    dest="etacut",   type=float, default=None)
parser.add_option("--LooseEle",  dest="LooseEle", action='store_true', default=False)
parser.add_option("--PuppiJet",  dest="PuppiJet", action='store_true', default=False)
parser.add_option("--do_HoTot",  dest="do_HoTot", action='store_true', default=False)
parser.add_option("--do_EoTot",  dest="do_EoTot", action='store_true', default=False)
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
    ########################### APPLY CUTS ###########################

    # skip jets that cannot be reconstructed by L1 (limit is 5.191)
    cut_pt = -1; cut_eta = 5.0; cut_phi = -1
            
    if options.jetPtcut: 
        cut_pt = float(options.jetPtcut)

    if options.etacut:
        cut_eta = float(options.etacut)

    if options.LooseEle:
        df = df.Define("FlagLooseElectron", "Electron.isLooseElectron")
        df = df.Define("FlaggedLooseElectron",  "GetFlagged (Offline_pt, Offline_eta, Offline_phi, FlagLooseElectron)")
        df = df.Redefine("Offline_pt",  "FlaggedLooseElectron.at(0)")
        df = df.Redefine("Offline_eta", "FlaggedLooseElectron.at(1)")
        df = df.Redefine("Offline_phi", "FlaggedLooseElectron.at(2)")

    df = df.Define("Offline_pt_cut", 
            "CutOffline(Offline_pt, Offline_eta, Offline_phi, {}, {}, {}).at(0)".format(cut_pt, cut_eta, cut_phi))
    df = df.Define("Offline_eta_cut", 
            "CutOffline(Offline_pt, Offline_eta, Offline_phi, {}, {}, {}).at(1)".format(cut_pt, cut_eta, cut_phi))
    df = df.Define("Offline_phi_cut", 
            "CutOffline(Offline_pt, Offline_eta, Offline_phi, {}, {}, {}).at(2)".format(cut_pt, cut_eta, cut_phi))

    ##################################################################    
    ########################### MATCHING #############################

    df = df.Define("good_L1_id", "Matching(L1_pt, L1_eta, L1_phi, Offline_pt_cut, Offline_eta_cut, Offline_phi_cut).at(0)")
    df = df.Define("good_Of_id", "Matching(L1_pt, L1_eta, L1_phi, Offline_pt_cut, Offline_eta_cut, Offline_phi_cut).at(1)")

    df = df.Filter("(good_L1_id.size() > 0) && (good_Of_id.size() > 0)")

    df = df.Define("good_L1_pt",    "SelectGood (L1_pt, good_L1_id)")
    df = df.Define("good_L1_eta",   "SelectGood (L1_eta, good_L1_id)")
    df = df.Define("good_L1_phi",   "SelectGood (L1_phi, good_L1_id)")
    df = df.Define("good_Of_pt",    "SelectGood (Offline_pt_cut, good_Of_id)")
    df = df.Define("good_Of_eta",   "SelectGood (Offline_eta_cut, good_Of_id)")
    df = df.Define("good_Of_phi",   "SelectGood (Offline_phi_cut, good_Of_id)")

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
        caloParams_file = os.getcwd() + "/../caloParams/" + options.caloParam
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

    df = df.Define("FoundSaturation",  "FindSaturation (good_L1_ieta, good_L1_iphi, TT_ieta, TT_iphi, TT_iem, TT_ihad, TT_iet)")
    df_b = df.Define("good_Of_pt_b", "SelectBarrel (good_Of_pt, good_Of_eta)")
    df_b = df_b.Define("good_Of_eta_b", "SelectBarrel (good_Of_eta, good_Of_eta)")
    df_b = df_b.Define(response_name+"_b", "SelectBarrel ({}, good_Of_eta)".format(response_name))
    df_e = df.Define("good_Of_pt_e", "SelectEndcap (good_Of_pt, good_Of_eta)")
    df_e = df_e.Define("good_Of_eta_e", "SelectEndcap (good_Of_eta, good_Of_eta)")
    df_e = df_e.Define(response_name+"_e_", "SelectEndcap ({}, good_Of_eta)".format(response_name))
    df_e = df_e.Define("FoundSaturation_e",  "SelectEndcap (FoundSaturation, good_Of_eta)")
    df_e = df_e.Define(response_name+"_e", "GetFlaggedResponse ({}, FoundSaturation_e)".format(response_name+"_e_"))
    df_f = df.Define("good_Of_pt_f", "SelectForward (good_Of_pt, good_Of_eta)")
    df_f = df_f.Define("good_Of_eta_f", "SelectForward (good_Of_eta, good_Of_eta)")
    df_f = df_f.Define(response_name+"_f_", "SelectForward ({}, good_Of_eta)".format(response_name))
    df_f = df_f.Define("FoundSaturation_f",  "SelectForward (FoundSaturation, good_Of_eta)")
    df_f = df_f.Define(response_name+"_f", "GetFlaggedResponse ({}, FoundSaturation_f)".format(response_name+"_f_"))


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

    #################################################################    
    ########################## HISTOGRAMS ###########################

    print("\n ### INFO: Define energy histograms")

    # INCLUSIVE HISTOGRAMS
    nbins = 100; min = 0; max = 500
    offline_pt = df.Histo1D(("good_Of_pt", "good_Of_pt", nbins, min, max), "good_Of_pt")
    online_pt = df.Histo1D(("good_L1_pt", "good_L1_pt", nbins, min, max), "good_L1_pt")
    CD_iet = df.Histo1D(("CD_iet", "CD_iet", nbins, min, max), "CD_iet")     
    CD_iesum = df.Histo1D(("CD_iesum", "CD_iesum", nbins, min, max), "CD_iesum")
    if options.HCALcalib or options.ECALcalib:
        CD_iet_calib = df.Histo1D(("CD_iesum_calib", "CD_iesum_calib", nbins, min, max), "CD_iesum_calib")

    print(" ### INFO: Define response histograms")

    # INCLUSIVE HISTOGRAMS
    pt_response_ptInclusive = df.Histo1D(("pt_response_ptInclusive", 
        "pt_response_ptInclusive", res_bins, 0, 3), response_name)
    pt_barrel_resp_ptInclusive = df_b.Histo1D(("pt_barrel_resp_ptInclusive",
        "pt_barrel_resp_ptInclusive", res_bins, 0, 3), response_name+"_b")
    pt_endcap_resp_ptInclusive = df_e.Histo1D(("pt_endcap_resp_ptInclusive",
        "pt_endcap_resp_ptInclusive", res_bins, 0, 3), response_name+"_e") 
    pt_forward_resp_ptInclusive = df_f.Histo1D(("pt_forward_resp_ptInclusive",
        "pt_forward_resp_ptInclusive", res_bins, 0, 3), response_name+"_f") 


    ##################################################################    
    ##################################################################    
    ################################################################## 

    print(" ### INFO: Saving resolution to root format")
    fileout = ROOT.TFile(outdir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs/resolution_graphs_'+label+'_'+options.target+'.root','RECREATE')
    offline_pt.Write()
    online_pt.Write()
    CD_iet.Write()
    CD_iesum.Write()
    if options.HCALcalib or options.ECALcalib:
        CD_iet_calib.Write()
    pt_response_ptInclusive.Write()
    pt_barrel_resp_ptInclusive.Write()
    pt_endcap_resp_ptInclusive.Write()
    pt_forward_resp_ptInclusive.Write()
