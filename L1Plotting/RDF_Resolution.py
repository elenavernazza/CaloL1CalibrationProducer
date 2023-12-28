import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(000000)
import sys, os, matplotlib, glob, sys
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

#######################################################################
######################### SCRIPT BODY #################################
#######################################################################

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--indir",     dest="indir",    default=None)
parser.add_option("--tag",       dest="tag",      default='')
parser.add_option("--outdir",    dest="outdir",   default=None)
parser.add_option("--label",     dest="label",    default=None)
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
parser.add_option("--norm",      dest="norm",     action='store_true', default=False)
(options, args) = parser.parse_args()

cmap = plt.get_cmap('Set1')

# get/create folders
indir = "/data_CMS/cms/motta/CaloL1calibraton/L1NTuples/"+options.indir
outdir = "/data_CMS/cms/motta/CaloL1calibraton/"+options.outdir
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

    # [FIXME] Yet to be implemented
    if options.target == 'ele' and options.LooseEle:
        sys.exit(" ERROR: This is not implemented yet")
    #     df = df.Define("isLooseElectron", "Electron.isLooseElectron")

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

    df = df.Filter("(good_L1_id != -1) && (good_Of_id != -1)")
    df = df.Define("good_L1_pt",    "L1_pt.at(good_L1_id)")
    df = df.Define("good_L1_eta",   "L1_eta.at(good_L1_id)")
    df = df.Define("good_L1_phi",   "L1_phi.at(good_L1_id)")
    df = df.Define("good_Of_pt",    "Offline_pt_cut.at(good_Of_id)")
    df = df.Define("good_Of_eta",   "Offline_eta_cut.at(good_Of_id)")
    df = df.Define("good_Of_phi",   "Offline_phi_cut.at(good_Of_id)")

    # Define response for matched jets
    df = df.Define("Response", "good_L1_pt / good_Of_pt")

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

    df = df.Define("HoTot", "CD_ihad/CD_iet")
    df = df.Define("EoTot", "CD_iem/CD_iet")

    # Define response for chunky donuts
    df = df.Define("Response_CD", "CD_iet / good_Of_pt")
    df = df.Define("Ratio", "CD_iet / good_L1_pt")
    
    df_b = df.Filter("abs(good_Of_eta) < 1.305")
    df_e = df.Filter("(abs(good_Of_eta) > 1.479)")

    # print(" ### INFO: Plotting")

    # c = ROOT.TCanvas()
    # histo1 = df.Histo2D(("Ratio", "", 50, 0, 2, 500, 0, 500), "Ratio", "good_L1_pt")
    # histo1.Draw()
    # c.SaveAs("ratio_l1pt_pt.png")

    # c = ROOT.TCanvas()
    # histo1 = df.Histo2D(("Ratio", "", 50, 0, 2, 50, -5, 5), "Ratio", "good_L1_eta")
    # histo1.Draw()
    # c.SaveAs("ratio_l1pt_eta.png")

    ##################################################################    
    ########################### HISTOGRAMS ###########################

    print(" ### INFO: Define response histograms")

    # INCLUSIVE HISTOGRAMS
    pt_response_ptInclusive = df.Histo1D(("pt_response_ptInclusive", 
        "pt_response_ptInclusive", res_bins, 0, 3), "Response")
    pt_barrel_resp_ptInclusive = df_b.Histo1D(("pt_barrel_resp_ptInclusive",
        "pt_barrel_resp_ptInclusive", res_bins, 0, 3), "Response")
    pt_endcap_resp_ptInclusive = df_e.Histo1D(("pt_endcap_resp_ptInclusive",
        "pt_endcap_resp_ptInclusive", res_bins, 0, 3), "Response") 

    pt_response_ptInclusive_CD = df.Histo1D(("pt_response_ptInclusive_CD", 
        "pt_response_ptInclusive_CD", res_bins, 0, 3), "Response_CD")
    pt_barrel_resp_ptInclusive_CD = df_b.Histo1D(("pt_barrel_resp_ptInclusive_CD",
        "pt_barrel_resp_ptInclusive", res_bins, 0, 3), "Response_CD")
    pt_endcap_resp_ptInclusive_CD = df_e.Histo1D(("pt_endcap_resp_ptInclusive_CD",
        "pt_endcap_resp_ptInclusive", res_bins, 0, 3), "Response_CD") 

    # PT RESPONSE - PT BINS HISTOGRAMS
    response_ptBins = []
    barrel_response_ptBins = []
    endcap_response_ptBins = []
    for i in range(len(ptBins)-1):

        df_PtBin = df.Filter("(good_Of_pt > {}) && (good_Of_pt < {})".format(ptBins[i], ptBins[i+1]))
        name = "pt_resp_ptBin"+str(ptBins[i])+"to"+str(ptBins[i+1])
        response_ptBins.append(df_PtBin.Histo1D((name, name, res_bins, 0, 3), "Response"))

        df_barrel_PtBin = df_b.Filter("(good_Of_pt > {}) && (good_Of_pt < {})".format(ptBins[i], ptBins[i+1]))
        name = "pt_barrel_resp_ptBin"+str(ptBins[i])+"to"+str(ptBins[i+1])
        barrel_response_ptBins.append(df_barrel_PtBin.Histo1D((name, name, res_bins, 0, 3), "Response"))

        df_endcap_PtBin = df_e.Filter("(good_Of_pt > {}) && (good_Of_pt < {})".format(ptBins[i], ptBins[i+1]))
        name = "pt_endcap_resp_ptBin"+str(ptBins[i])+"to"+str(ptBins[i+1])
        endcap_response_ptBins.append(df_endcap_PtBin.Histo1D((name, name, res_bins, 0, 3), "Response"))

    # PT RESPONSE -  ETA BINS HISTIGRAMS
    absEta_response_ptBins = []
    minusEta_response_ptBins = []
    plusEta_response_ptBins = []
    for i in range(len(etaBins)-1):

        df_EtaBin = df.Filter("(abs(good_Of_eta) > {}) && (abs(good_Of_eta) < {})".format(etaBins[i], etaBins[i+1]))
        name = "pt_resp_AbsEtaBin"+str(etaBins[i])+"to"+str(etaBins[i+1])
        absEta_response_ptBins.append(df_EtaBin.Histo1D((name, name, res_bins, 0, 3), "Response"))

        df_MinusEtaBin = df.Filter("(good_Of_eta < -{}) && (good_Of_eta > -{})".format(etaBins[i], etaBins[i+1]))
        name = "pt_resp_MinusEtaBin"+str(etaBins[i])+"to"+str(etaBins[i+1])
        minusEta_response_ptBins.append(df_MinusEtaBin.Histo1D((name, name, res_bins, 0, 3), "Response"))

        df_PlusEtaBin = df.Filter("(good_Of_eta > {}) && (good_Of_eta < {})".format(etaBins[i], etaBins[i+1]))
        name = "pt_resp_PlusEtaBin"+str(etaBins[i])+"to"+str(etaBins[i+1])
        plusEta_response_ptBins.append(df_PlusEtaBin.Histo1D((name, name, res_bins, 0, 3), "Response"))

    # PT RESPONSE -  H/TOT BINS HISTIGRAMS
    if options.do_HoTot:
        response_HoTotBins = []
        for i in range(len(HoTotBins)-1):
            df_HoTotBin = df.Filter("(HoTot > {}) && (HoTot < {})".format(HoTotBins[i], HoTotBins[i+1]))
            name = "pt_resp_HoTotBin"+str(HoTotBins[i])+"to"+str(HoTotBins[i+1])
            response_HoTotBins.append(df_HoTotBin.Histo1D((name, name, res_bins, 0, 3), "Response"))

    # PT RESPONSE -  E/TOT BINS HISTIGRAMS
    if options.do_EoTot:
        response_EoTotBins = []
        for i in range(len(EoTotBins)-1):
            df_EoTotBin = df.Filter("(EoTot > {}) && (EoTot < {})".format(EoTotBins[i], EoTotBins[i+1]))
            name = "pt_resp_EoTotBin"+str(EoTotBins[i])+"to"+str(EoTotBins[i+1])
            response_EoTotBins.append(df_EoTotBin.Histo1D((name, name, res_bins, 0, 3), "Response"))

    ##################################################################    
    ########################### RESOLUTION ###########################
        
    print(" ### INFO: Compute resolution and scale")

    # make resolution plots
    pt_resol_fctPt = ROOT.TH1F("pt_resol_fctPt","pt_resol_fctPt",len(ptBins)-1, array('f',ptBins))
    pt_resol_barrel_fctPt = ROOT.TH1F("pt_resol_barrel_fctPt","pt_resol_barrel_fctPt",len(ptBins)-1, array('f',ptBins))
    pt_resol_endcap_fctPt = ROOT.TH1F("pt_resol_endcap_fctPt","pt_resol_endcap_fctPt",len(ptBins)-1, array('f',ptBins))
    pt_resol_fctEta = ROOT.TH1F("pt_resol_fctEta","pt_resol_fctEta",len(signedEtaBins)-1, array('f',signedEtaBins))

    pt_scale_fctPt = ROOT.TH1F("pt_scale_fctPt","pt_scale_fctPt",len(ptBins)-1, array('f',ptBins))
    pt_scale_fctEta = ROOT.TH1F("pt_scale_fctEta","pt_scale_fctEta",len(signedEtaBins)-1, array('f',signedEtaBins))

    pt_scale_max_fctPt = ROOT.TH1F("pt_scale_max_fctPt","pt_scale_max_fctPt",len(ptBins)-1, array('f',ptBins))
    pt_scale_max_fctEta = ROOT.TH1F("pt_scale_max_fctEta","pt_scale_max_fctEta",len(signedEtaBins)-1, array('f',signedEtaBins))

    if options.do_HoTot:
        pt_resol_fctHoTot = ROOT.TH1F("pt_resol_fctHoTot","pt_resol_fctHoTot",len(HoTotBins)-1, array('f',HoTotBins))
        pt_scale_fctHoTot = ROOT.TH1F("pt_scale_fctHoTot","pt_scale_fctHoTot",len(HoTotBins)-1, array('f',HoTotBins))
        pt_scale_max_fctHoTot = ROOT.TH1F("pt_scale_max_fctHoTot","pt_scale_max_fctHoTot",len(HoTotBins)-1, array('f',HoTotBins))

    if options.do_EoTot:
        pt_resol_fctEoTot = ROOT.TH1F("pt_resol_fctEoTot","pt_resol_fctEoTot",len(EoTotBins)-1, array('f',EoTotBins))
        pt_scale_fctEoTot = ROOT.TH1F("pt_scale_fctEoTot","pt_scale_fctEoTot",len(EoTotBins)-1, array('f',EoTotBins))
        pt_scale_max_fctEoTot = ROOT.TH1F("pt_scale_max_fctEoTot","pt_scale_max_fctEoTot",len(EoTotBins)-1, array('f',EoTotBins))

    for i in range(len(barrel_response_ptBins)):
        pt_scale_fctPt.SetBinContent(i+1, response_ptBins[i].GetMean())
        pt_scale_fctPt.SetBinError(i+1, response_ptBins[i].GetMeanError())

        pt_scale_max_fctPt.SetBinContent(i+1, response_ptBins[i].GetBinCenter(response_ptBins[i].GetMaximumBin()))
        pt_scale_max_fctPt.SetBinError(i+1, response_ptBins[i].GetBinWidth(response_ptBins[i].GetMaximumBin()))

        if response_ptBins[i].GetMean() > 0:
            pt_resol_fctPt.SetBinContent(i+1, response_ptBins[i].GetRMS()/response_ptBins[i].GetMean())
            pt_resol_fctPt.SetBinError(i+1, response_ptBins[i].GetRMSError()/response_ptBins[i].GetMean())
        else:
            pt_resol_fctPt.SetBinContent(i+1, 0)
            pt_resol_fctPt.SetBinError(i+1, 0)

        if barrel_response_ptBins[i].GetMean() > 0:
            pt_resol_barrel_fctPt.SetBinContent(i+1, barrel_response_ptBins[i].GetRMS()/barrel_response_ptBins[i].GetMean())
            pt_resol_endcap_fctPt.SetBinError(i+1, barrel_response_ptBins[i].GetRMSError()/barrel_response_ptBins[i].GetMean())
        else:
            pt_resol_barrel_fctPt.SetBinContent(i+1, 0)
            pt_resol_endcap_fctPt.SetBinError(i+1, 0)        

        if endcap_response_ptBins[i].GetMean() > 0:
            pt_resol_endcap_fctPt.SetBinContent(i+1, endcap_response_ptBins[i].GetRMS()/endcap_response_ptBins[i].GetMean())
            pt_resol_endcap_fctPt.SetBinError(i+1, endcap_response_ptBins[i].GetRMSError()/endcap_response_ptBins[i].GetMean())
        else:
            pt_resol_endcap_fctPt.SetBinContent(i+1, 0)
            pt_resol_endcap_fctPt.SetBinError(i+1, 0)

    for i in range(len(minusEta_response_ptBins)):
        pt_scale_fctEta.SetBinContent(len(etaBins)-1-i, minusEta_response_ptBins[i].GetMean())
        pt_scale_fctEta.SetBinError(len(etaBins)-1-i, minusEta_response_ptBins[i].GetMeanError())
        pt_scale_fctEta.SetBinContent(i+len(etaBins), plusEta_response_ptBins[i].GetMean())
        pt_scale_fctEta.SetBinError(i+len(etaBins), plusEta_response_ptBins[i].GetMeanError())

        pt_scale_max_fctEta.SetBinContent(len(etaBins)-1-i, minusEta_response_ptBins[i].GetBinCenter(minusEta_response_ptBins[i].GetMaximumBin()))
        pt_scale_max_fctEta.SetBinError(len(etaBins)-1-i, minusEta_response_ptBins[i].GetBinWidth(minusEta_response_ptBins[i].GetMaximumBin()))
        pt_scale_max_fctEta.SetBinContent(i+len(etaBins), plusEta_response_ptBins[i].GetBinCenter(plusEta_response_ptBins[i].GetMaximumBin()))
        pt_scale_max_fctEta.SetBinError(i+len(etaBins), plusEta_response_ptBins[i].GetBinWidth(plusEta_response_ptBins[i].GetMaximumBin()))

        if minusEta_response_ptBins[i].GetMean() > 0:
            pt_resol_fctEta.SetBinContent(len(etaBins)-1-i, minusEta_response_ptBins[i].GetRMS()/minusEta_response_ptBins[i].GetMean())
            pt_resol_fctEta.SetBinError(len(etaBins)-1-i, minusEta_response_ptBins[i].GetRMSError()/minusEta_response_ptBins[i].GetMean())
        else:
            pt_resol_fctEta.SetBinContent(len(etaBins)-1-i, 0)
            pt_resol_fctEta.SetBinError(len(etaBins)-1-i, 0)

        if plusEta_response_ptBins[i].GetMean() > 0:
            pt_resol_fctEta.SetBinContent(i+len(etaBins), plusEta_response_ptBins[i].GetRMS()/plusEta_response_ptBins[i].GetMean())
            pt_resol_fctEta.SetBinError(i+len(etaBins), plusEta_response_ptBins[i].GetRMSError()/plusEta_response_ptBins[i].GetMean())
        else:
            pt_resol_fctEta.SetBinContent(i+len(etaBins), 0)
            pt_resol_fctEta.SetBinError(i+len(etaBins), 0)

    if options.do_HoTot:
        for i in range(len(HoTotBins)-1):
            pt_scale_fctHoTot.SetBinContent(i+1, response_HoTotBins[i].GetMean())
            pt_scale_fctHoTot.SetBinError(i+1, response_HoTotBins[i].GetMeanError())
            pt_scale_max_fctHoTot.SetBinContent(i+1, response_HoTotBins[i].GetBinCenter(response_HoTotBins[i].GetMaximumBin()))
            pt_scale_max_fctHoTot.SetBinError(i+1, response_HoTotBins[i].GetBinWidth(response_HoTotBins[i].GetMaximumBin()))
            if response_HoTotBins[i].GetMean() > 0:
                pt_resol_fctHoTot.SetBinContent(i+1, response_HoTotBins[i].GetRMS()/response_HoTotBins[i].GetMean())
                pt_resol_fctHoTot.SetBinError(i+1, response_HoTotBins[i].GetRMSError()/response_HoTotBins[i].GetMean())
            else:
                pt_resol_fctHoTot.SetBinContent(i+1, 0)
                pt_resol_fctHoTot.SetBinError(i+1, 0)

    if options.do_EoTot:
        for i in range(len(EoTotBins)-1):
            pt_scale_fctEoTot.SetBinContent(i+1, response_EoTotBins[i].GetMean())
            pt_scale_fctEoTot.SetBinError(i+1, response_EoTotBins[i].GetMeanError())
            pt_scale_max_fctEoTot.SetBinContent(i+1, response_EoTotBins[i].GetBinCenter(response_EoTotBins[i].GetMaximumBin()))
            pt_scale_max_fctEoTot.SetBinError(i+1, response_EoTotBins[i].GetBinWidth(response_EoTotBins[i].GetMaximumBin()))
            if response_EoTotBins[i].GetMean() > 0:
                pt_resol_fctEoTot.SetBinContent(i+1, response_EoTotBins[i].GetRMS()/response_EoTotBins[i].GetMean())
                pt_resol_fctEoTot.SetBinError(i+1, response_EoTotBins[i].GetRMSError()/response_EoTotBins[i].GetMean())
            else:
                pt_resol_fctEoTot.SetBinContent(i+1, 0)
                pt_resol_fctEoTot.SetBinError(i+1, 0)

    print(" ### INFO: Saving to root format")
    fileout = ROOT.TFile(outdir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs/resolution_graphs_'+label+'_'+options.target+'.root','RECREATE')
    pt_response_ptInclusive.Write()
    pt_barrel_resp_ptInclusive.Write()
    pt_endcap_resp_ptInclusive.Write()
    pt_response_ptInclusive_CD.Write()
    pt_barrel_resp_ptInclusive_CD.Write()
    pt_endcap_resp_ptInclusive_CD.Write()
    for i in range(len(ptBins)-1):
        response_ptBins[i].Write()
        barrel_response_ptBins[i].Write()
        endcap_response_ptBins[i].Write()
    for i in range(len(etaBins)-1):
        absEta_response_ptBins[i].Write()
        minusEta_response_ptBins[i].Write()
        plusEta_response_ptBins[i].Write()
    pt_scale_fctPt.Write()
    pt_scale_max_fctPt.Write()
    pt_resol_fctPt.Write()
    pt_scale_fctEta.Write()
    pt_scale_max_fctEta.Write()
    pt_resol_fctEta.Write()
    pt_resol_barrel_fctPt.Write()
    pt_resol_endcap_fctPt.Write()
    if options.do_HoTot:
        for i in range(len(response_HoTotBins)):
            response_HoTotBins[i].Write()
        pt_scale_fctHoTot.Write()
        pt_scale_max_fctHoTot.Write()
        pt_resol_fctHoTot.Write()
    if options.do_EoTot:
        for i in range(len(response_EoTotBins)):
            response_EoTotBins[i].Write()
        pt_scale_fctEoTot.Write()
        pt_scale_max_fctEoTot.Write()
        pt_resol_fctEoTot.Write()

    ############################################################################################
    ############################################################################################
    ############################################################################################

else:
    print(" ### INFO: Read existing root files")
    filein = ROOT.TFile(outdir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs/resolution_graphs_'+label+'_'+options.target+'.root')
    pt_scale_fctPt = filein.Get('pt_scale_fctPt')
    pt_scale_fctEta = filein.Get('pt_scale_fctEta')
    if options.do_HoTot:
        pt_scale_fctHoTot = filein.Get('pt_scale_fctHoTot')
        pt_scale_max_fctHoTot = filein.Get('pt_scale_max_fctHoTot')
        pt_resol_fctHoTot = filein.Get('pt_resol_fctHoTot')
    if options.do_EoTot:
        pt_scale_fctEoTot = filein.Get('pt_scale_fctEoTot')
        pt_scale_max_fctEoTot = filein.Get('pt_scale_max_fctEoTot')
        pt_resol_fctEoTot = filein.Get('pt_resol_fctEoTot')
    pt_scale_max_fctPt = filein.Get('pt_scale_max_fctPt')
    pt_scale_max_fctEta = filein.Get('pt_scale_max_fctEta')
    pt_resol_fctPt = filein.Get('pt_resol_fctPt')
    pt_resol_barrel_fctPt = filein.Get('pt_resol_barrel_fctPt')
    pt_resol_endcap_fctPt = filein.Get('pt_resol_endcap_fctPt')
    pt_resol_fctEta = filein.Get('pt_resol_fctEta')
    pt_response_ptInclusive = filein.Get('pt_response_ptInclusive')
    pt_barrel_resp_ptInclusive = filein.Get('pt_barrel_resp_ptInclusive')
    pt_endcap_resp_ptInclusive = filein.Get('pt_endcap_resp_ptInclusive')
    pt_response_ptInclusive_CD = filein.Get('pt_response_ptInclusive_CD')
    pt_barrel_resp_ptInclusive_CD = filein.Get('pt_barrel_resp_ptInclusive_CD')
    pt_endcap_resp_ptInclusive_CD = filein.Get('pt_endcap_resp_ptInclusive_CD')
    response_ptBins = []
    barrel_response_ptBins = []
    endcap_response_ptBins = []
    for i in range(len(ptBins)-1):
        response_ptBins.append(filein.Get("pt_resp_ptBin"+str(ptBins[i])+"to"+str(ptBins[i+1])))
        barrel_response_ptBins.append(filein.Get("pt_barrel_resp_ptBin"+str(ptBins[i])+"to"+str(ptBins[i+1])))
        endcap_response_ptBins.append(filein.Get("pt_endcap_resp_ptBin"+str(ptBins[i])+"to"+str(ptBins[i+1])))
    absEta_response_ptBins = []
    minusEta_response_ptBins = []
    plusEta_response_ptBins = []
    for i in range(len(etaBins)-1):
        absEta_response_ptBins.append(filein.Get("pt_resp_AbsEtaBin"+str(etaBins[i])+"to"+str(etaBins[i+1])))
        minusEta_response_ptBins.append(filein.Get("pt_resp_MinusEtaBin"+str(etaBins[i])+"to"+str(etaBins[i+1])))
        plusEta_response_ptBins.append(filein.Get("pt_resp_PlusEtaBin"+str(etaBins[i])+"to"+str(etaBins[i+1])))
    if options.do_HoTot:
        response_HoTotBins = []
        for i in range(len(HoTotBins)-1):
            response_HoTotBins.append(filein.Get("pt_resp_HoTotBin"+str(HoTotBins[i])+"to"+str(HoTotBins[i+1])))
    if options.do_EoTot:
        response_EoTotBins = []
        for i in range(len(EoTotBins)-1):
            response_EoTotBins.append(filein.Get("pt_resp_EoTotBin"+str(EoTotBins[i])+"to"+str(EoTotBins[i+1])))

if options.norm:
    y_label_response = 'a.u.'
    for i in range(len(response_ptBins)):
        if response_ptBins[i].Integral() > 0:
            response_ptBins[i].Scale(1.0/response_ptBins[i].Integral())
        if barrel_response_ptBins[i].Integral() > 0:
            barrel_response_ptBins[i].Scale(1.0/barrel_response_ptBins[i].Integral())
        if endcap_response_ptBins[i].Integral() > 0:
            endcap_response_ptBins[i].Scale(1.0/endcap_response_ptBins[i].Integral())

    for i in range(len(minusEta_response_ptBins)):
        if minusEta_response_ptBins[i].Integral() > 0:
            minusEta_response_ptBins[i].Scale(1.0/minusEta_response_ptBins[i].Integral())
        if plusEta_response_ptBins[i].Integral() > 0:
            plusEta_response_ptBins[i].Scale(1.0/plusEta_response_ptBins[i].Integral())
        if absEta_response_ptBins[i].Integral() > 0:
            absEta_response_ptBins[i].Scale(1.0/absEta_response_ptBins[i].Integral())

    if options.do_HoTot:
        for i in range(len(response_HoTotBins)):
            if response_HoTotBins[i].Integral() > 0:
                response_HoTotBins[i].Scale(1.0/response_HoTotBins[i].Integral())

    if options.do_EoTot:
        for i in range(len(response_EoTotBins)):
            if response_EoTotBins[i].Integral() > 0:
                response_EoTotBins[i].Scale(1.0/response_EoTotBins[i].Integral())

else:
    y_label_response = 'Entries'

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

def SetStyle(ax, x_label, y_label, x_lim, y_lim, leg_title=''):
    leg = plt.legend(loc = 'upper right', fontsize=20, title=leg_title, title_fontsize=18)
    leg._legend_box.align = "left"
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xlim(x_lim)
    plt.ylim(y_lim)
    plt.grid()
    for xtick in ax.xaxis.get_major_ticks():
        xtick.set_pad(10)
    if options.reco: mplhep.cms.label(data=False, rlabel='(13.6 TeV)')
    else:            mplhep.cms.label('Preliminary', data=True, rlabel=r'110 pb$^{-1}$ (13.6 TeV)') ## 110pb-1 is Run 362617

def AddRectangles(ax, Ymax):
    rect1 = patches.Rectangle((-1.479, 0), 0.174, Ymax*1.3, linewidth=1, edgecolor='gray', facecolor='gray', zorder=2)
    rect2 = patches.Rectangle((1.305, 0), 0.174, Ymax*1.3, linewidth=1, edgecolor='gray', facecolor='gray', zorder=2)
    ax.add_patch(rect1)
    ax.add_patch(rect2)  

############################################################################################
print(" ### INFO: Produce plots inclusive")
############################################################################################

############################################################################################
## response inclusive 

fig, ax = plt.subplots(figsize=(10,10))
X,Y,X_err,Y_err = GetArraysFromHisto(pt_barrel_resp_ptInclusive)
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=barrel_label, lw=2, marker='o', color=cmap(0))
Ymax = max(Y)
X,Y,X_err,Y_err = GetArraysFromHisto(pt_endcap_resp_ptInclusive)
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=endcap_label, lw=2, marker='o', color=cmap(1))
Ymax = max(Ymax, max(Y))
X,Y,X_err,Y_err = GetArraysFromHisto(pt_response_ptInclusive)
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label="Inclusive", lw=2, marker='o', color=cmap(2))
Ymax = max(Ymax, max(Y))
SetStyle(ax, x_label_response, y_label_response, x_lim_response, (0,1.3*Ymax))
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/response_ptInclusive_'+label+'_'+options.target+'.pdf')
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/response_ptInclusive_'+label+'_'+options.target+'.png')
plt.close()

############################################################################################
## response inclusive CD

fig, ax = plt.subplots(figsize=(10,10))
X,Y,X_err,Y_err = GetArraysFromHisto(pt_barrel_resp_ptInclusive_CD)
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=barrel_label, lw=2, marker='o', color=cmap(0))
Ymax = max(Y)
X,Y,X_err,Y_err = GetArraysFromHisto(pt_endcap_resp_ptInclusive_CD)
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=endcap_label, lw=2, marker='o', color=cmap(1))
Ymax = max(Ymax, max(Y))
X,Y,X_err,Y_err = GetArraysFromHisto(pt_response_ptInclusive_CD)
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label="Inclusive", lw=2, marker='o', color=cmap(2))
Ymax = max(Ymax, max(Y))
SetStyle(ax, x_label_response, y_label_response, x_lim_response, (0,1.3*Ymax))
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/response_ptInclusive_CD_'+label+'_'+options.target+'.pdf')
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/response_ptInclusive_CD_'+label+'_'+options.target+'.png')
plt.close()

############################################################################################
print(" ### INFO: Produce plots in pt bins")
############################################################################################

############################################################################################
## response in pt bins

for i in range(len(barrel_response_ptBins)):
    fig, ax = plt.subplots(figsize=(10,10))
    X,Y,X_err,Y_err = GetArraysFromHisto(barrel_response_ptBins[i])
    ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=barrel_label, lw=2, marker='o', color=cmap(0))
    Ymax = max(Y)
    X,Y,X_err,Y_err = GetArraysFromHisto(endcap_response_ptBins[i])
    ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=endcap_label, lw=2, marker='o', color=cmap(1))
    Ymax = max(Ymax, max(Y))
    SetStyle(ax, x_label_response, y_label_response, x_lim_response, (0,1.3*Ymax), str(ptBins[i])+legend_label_pt+str(ptBins[i+1]))
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/response_'+str(ptBins[i])+"pt"+str(ptBins[i+1])+'_'+label+'_'+options.target+'.pdf')
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/response_'+str(ptBins[i])+"pt"+str(ptBins[i+1])+'_'+label+'_'+options.target+'.png')
    plt.close()

############################################################################################
## resolution in pt bins

fig, ax = plt.subplots(figsize=(10,10))
X,Y,X_err,Y_err = GetArraysFromHisto(pt_resol_barrel_fctPt)
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=barrel_label, lw=2, marker='o', color=cmap(0))
Ymax = max(Y)
X,Y,X_err,Y_err = GetArraysFromHisto(pt_resol_endcap_fctPt)
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=endcap_label, lw=2, marker='o', color=cmap(1))
Ymax = max(Ymax, max(Y))
SetStyle(ax, x_label_pt, y_label_resolution, x_lim_pt, (0,1.3*Ymax))
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/resolution_ptBins_'+label+'_'+options.target+'.pdf')
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/resolution_ptBins_'+label+'_'+options.target+'.png')
plt.close()

############################################################################################
## scale in pt bins

fig, ax = plt.subplots(figsize=(10,10))
X,Y,X_err,Y_err = GetArraysFromHisto(pt_scale_fctPt)
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, lw=2, marker='o', color=cmap(0))
SetStyle(ax, x_label_pt, y_label_scale, x_lim_pt, y_lim_scale)
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/scale_ptBins_'+label+'_'+options.target+'.pdf')
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/scale_ptBins_'+label+'_'+options.target+'.png')
plt.close()

############################################################################################
## scale from maximum in pt bins

fig, ax = plt.subplots(figsize=(10,10))
X,Y,X_err,Y_err = GetArraysFromHisto(pt_scale_max_fctPt)
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, lw=2, marker='o', color=cmap(0))
SetStyle(ax, x_label_pt, y_label_scale, x_lim_pt, y_lim_scale)
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/scale_max_ptBins_'+label+'_'+options.target+'.pdf')
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/scale_max_ptBins_'+label+'_'+options.target+'.png')
plt.close()

############################################################################################
print(" ### INFO: Produce plots in eta bins")
############################################################################################      

############################################################################################
## response in eta bins

for i in range(len(absEta_response_ptBins)):
    fig, ax = plt.subplots(figsize=(10,10))
    X,Y,X_err,Y_err = GetArraysFromHisto(absEta_response_ptBins[i])
    ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=str(etaBins[i])+legend_label_eta+str(etaBins[i+1]), lw=2, marker='o', color=cmap(0))
    Ymax = max(Y)
    SetStyle(ax, x_label_response, y_label_response, x_lim_response, (0,1.3*Ymax))
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/response_'+str(etaBins[i])+"eta"+str(etaBins[i+1])+'_'+label+'_'+options.target+'.pdf')
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/response_'+str(etaBins[i])+"eta"+str(etaBins[i+1])+'_'+label+'_'+options.target+'.png')
    plt.close()

############################################################################################
## resolution in eta bins

fig, ax = plt.subplots(figsize=(10,10))
X,Y,X_err,Y_err = GetArraysFromHisto(pt_resol_fctEta)
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, ls='None', lw=2, marker='o', color=cmap(0), zorder=1)
Ymax = max(Y)
AddRectangles(ax,Ymax)
SetStyle(ax, x_label_eta, y_label_resolution, x_lim_eta, (0,1.3*Ymax))
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/resolution_etaBins_'+label+'_'+options.target+'.pdf')
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/resolution_etaBins_'+label+'_'+options.target+'.png')
plt.close()

############################################################################################
## scale in eta bins

fig, ax = plt.subplots(figsize=(10,10))
X,Y,X_err,Y_err = GetArraysFromHisto(pt_scale_fctEta)
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, lw=2, marker='o', color=cmap(0), zorder=1)
AddRectangles(ax,max(Y))
SetStyle(ax, x_label_eta, y_label_scale, x_lim_eta, y_lim_scale)
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/scale_etaBins_'+label+'_'+options.target+'.pdf')
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/scale_etaBins_'+label+'_'+options.target+'.png')
plt.close()

############################################################################################
## scale from maximum in eta bins

fig, ax = plt.subplots(figsize=(10,10))
X,Y,X_err,Y_err = GetArraysFromHisto(pt_scale_max_fctEta)
ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, lw=2, marker='o', color=cmap(0), zorder=1)
AddRectangles(ax,max(Y))
SetStyle(ax, x_label_eta, y_label_scale, x_lim_eta, y_lim_scale)
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/scale_max_etaBins_'+label+'_'+options.target+'.pdf')
plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/scale_max_etaBins_'+label+'_'+options.target+'.png')
plt.close()

if options.do_HoTot:

    ############################################################################################
    print(" ### INFO: Produce plots in H/Tot bins")
    ############################################################################################

    ############################################################################################
    ## response in HoTot bins

    fig, ax = plt.subplots(figsize=(10,10))
    Ymax = 0
    for i in range(len(response_HoTotBins)):
        X,Y,X_err,Y_err = GetArraysFromHisto(response_HoTotBins[i])
        ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=str(HoTotBins[i])+legend_label_Hotot+str(HoTotBins[i+1]), lw=2, marker='o', color=cmap(i))
        Ymax = max(max(Y), Ymax)        
    SetStyle(ax, x_label_response, y_label_response, x_lim_response, (0,1.3*Ymax))
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/response_HoTot_'+label+'_'+options.target+'.pdf')
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/response_HoTot_'+label+'_'+options.target+'.png')
    plt.ylim(0.1, Ymax*1.3)
    plt.yscale('log')
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/response_HoTot_'+label+'_'+options.target+'_log.pdf')
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/response_HoTot_'+label+'_'+options.target+'_log.png')
    plt.close()

    ############################################################################################
    ## resolution in HoTot bins

    fig, ax = plt.subplots(figsize=(10,10))
    X,Y,X_err,Y_err = GetArraysFromHisto(pt_resol_fctHoTot)
    ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, ls='None', lw=2, marker='o', color=cmap(0), zorder=1)
    Ymax = max(Y)
    SetStyle(ax, x_label_Hotot, y_label_resolution, x_lim_Hotot, (0,1.3*Ymax))
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/resolution_HoTotBins_'+label+'_'+options.target+'.pdf')
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/resolution_HoTotBins_'+label+'_'+options.target+'.png')
    plt.close()

    ############################################################################################
    ## scale in HoTot bins

    fig, ax = plt.subplots(figsize=(10,10))
    X,Y,X_err,Y_err = GetArraysFromHisto(pt_scale_fctHoTot)
    ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, lw=2, marker='o', color=cmap(0))
    SetStyle(ax, x_label_Hotot, y_label_scale, x_lim_Hotot, y_lim_scale)
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/scale_HoTotBins_'+label+'_'+options.target+'.pdf')
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/scale_HoTotBins_'+label+'_'+options.target+'.png')
    plt.close()

    ############################################################################################
    ## scale from maximum in HoTot bins

    fig, ax = plt.subplots(figsize=(10,10))
    X,Y,X_err,Y_err = GetArraysFromHisto(pt_scale_max_fctHoTot)
    ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, lw=2, marker='o', color=cmap(0))
    SetStyle(ax, x_label_Hotot, y_label_scale, x_lim_Hotot, y_lim_scale)
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/scale_max_HoTotBins_'+label+'_'+options.target+'.pdf')
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/scale_max_HoTotBins_'+label+'_'+options.target+'.png')
    plt.close()

if options.do_EoTot:

    ############################################################################################
    print(" ### INFO: Produce plots in H/Tot bins")
    ############################################################################################

    ############################################################################################
    ## response in EoTot bins

    fig, ax = plt.subplots(figsize=(10,10))
    Ymax = 0
    for i in range(len(response_EoTotBins)):
        X,Y,X_err,Y_err = GetArraysFromHisto(response_EoTotBins[i])
        ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=str(EoTotBins[i])+legend_label_Eotot+str(EoTotBins[i+1]), lw=2, marker='o', color=cmap(i))
        Ymax = max(max(Y), Ymax)        
    SetStyle(ax, x_label_response, y_label_response, x_lim_response, (0,1.3*Ymax))
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/response_EoTot'+label+'_'+options.target+'.pdf')
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/response_EoTot'+label+'_'+options.target+'.png')
    plt.ylim(0.1, Ymax*1.3)
    plt.yscale('log')
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/response_EoTot'+label+'_'+options.target+'_log.pdf')
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/response_EoTot'+label+'_'+options.target+'_log.png')
    plt.close()

    ############################################################################################
    ## resolution in EoTot bins

    fig, ax = plt.subplots(figsize=(10,10))
    X,Y,X_err,Y_err = GetArraysFromHisto(pt_resol_fctEoTot)
    ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, ls='None', lw=2, marker='o', color=cmap(0), zorder=1)
    Ymax = max(Y)
    SetStyle(ax, x_label_Eotot, y_label_resolution, x_lim_Eotot, (0,1.3*Ymax))
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/resolution_EoTotBins_'+label+'_'+options.target+'.pdf')
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/resolution_EoTotBins_'+label+'_'+options.target+'.png')
    plt.close()

    ############################################################################################
    ## scale in EoTot bins

    fig, ax = plt.subplots(figsize=(10,10))
    X,Y,X_err,Y_err = GetArraysFromHisto(pt_scale_fctEoTot)
    ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, lw=2, marker='o', color=cmap(0))
    SetStyle(ax, x_label_Eotot, y_label_scale, x_lim_Eotot, y_lim_scale)
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/scale_EoTotBins_'+label+'_'+options.target+'.pdf')
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/scale_EoTotBins_'+label+'_'+options.target+'.png')
    plt.close()

    ############################################################################################
    ## scale from maximum in EoTot bins

    fig, ax = plt.subplots(figsize=(10,10))
    X,Y,X_err,Y_err = GetArraysFromHisto(pt_scale_max_fctEoTot)
    ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, lw=2, marker='o', color=cmap(0))
    SetStyle(ax, x_label_Eotot, y_label_scale, x_lim_Eotot, y_lim_scale)
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PDFs/scale_max_EoTotBins_'+label+'_'+options.target+'.pdf')
    plt.savefig(outdir+'/PerformancePlots'+options.tag+'/'+label+'/PNGs/scale_max_EoTotBins_'+label+'_'+options.target+'.png')
    plt.close()
