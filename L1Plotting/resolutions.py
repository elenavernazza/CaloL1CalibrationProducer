from array import array
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(000000)
import sys, os, matplotlib
import numpy as np
from tqdm import tqdm

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import mplhep
plt.style.use(mplhep.style.CMS)

sys.path.insert(0,'../Utils')
from TowerGeometry import *

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning)

def NextPhiTower(iphi):
    if iphi == 72: return 1
    else:          return iphi + 1
def PrevPhiTower(iphi):
    if iphi == 1: return 72
    else:         return iphi - 1
def NextEtaTower(ieta):
    if ieta == -1: return 1
    else:          return ieta + 1
def PrevEtaTower(ieta):
    if ieta == 1: return -1
    else:         return ieta - 1

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
parser.add_option("--no_plot",   dest="no_plot",  action='store_true', default=False)
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

if not options.plot_only:
    # define targetTree
    if options.reco:
        if options.target == 'jet': targetTree = ROOT.TChain("l1JetRecoTree/JetRecoTree")
        if options.target == 'ele': targetTree = ROOT.TChain("l1ElectronRecoTree/ElectronRecoTree")
        if options.target == 'met': targetTree = ROOT.TChain("l1JetRecoTree/JetRecoTree")
    if options.gen:
        targetTree = ROOT.TChain("l1GeneratorTree/L1GenTree")
    # define level1Tree
    if options.unpacked: level1Tree = ROOT.TChain("l1UpgradeTree/L1UpgradeTree")
    else:                level1Tree = ROOT.TChain("l1UpgradeEmuTree/L1UpgradeTree")
    # define towersTree
    towersTree = ROOT.TChain("l1CaloTowerEmuTree/L1CaloTowerTree")

    # read input files
    targetTree.Add(indir+"/Ntuple*.root")
    level1Tree.Add(indir+"/Ntuple*.root")
    towersTree.Add(indir+"/Ntuple*.root")

    nEntries = targetTree.GetEntries()
    print(" ### INFO: Total entries ",nEntries)

    # run on entries specified by user, or only on entries available if that is exceeded
    nevents = options.nEvts
    if (nevents > nEntries) or (nevents==-1): nevents = nEntries
    print(" ### INFO: Reading",nevents)

    # PT RESPONSE - INCLUSIVE HISTOGRAMS
    res_bins = 240
    pt_response_ptInclusive = ROOT.TH1F("pt_response_ptInclusive","pt_response_ptInclusive",res_bins,0,3)
    pt_barrel_resp_ptInclusive = ROOT.TH1F("pt_barrel_resp_ptInclusive","pt_barrel_resp_ptInclusive",res_bins,0,3)
    pt_endcap_resp_ptInclusive = ROOT.TH1F("pt_endcap_resp_ptInclusive","pt_endcap_resp_ptInclusive",res_bins,0,3)
    pt_response_ptInclusive_CD = ROOT.TH1F("pt_response_ptInclusive_CD","pt_response_ptInclusive_CD",res_bins,0,3)
    pt_barrel_resp_ptInclusive_CD = ROOT.TH1F("pt_barrel_resp_ptInclusive_CD","pt_barrel_resp_ptInclusive_CD",res_bins,0,3)
    pt_endcap_resp_ptInclusive_CD = ROOT.TH1F("pt_endcap_resp_ptInclusive_CD","pt_endcap_resp_ptInclusive_CD",res_bins,0,3)

    # PT RESPONSE - PT BINS HISTOGRAMS
    response_ptBins = []
    barrel_response_ptBins = []
    endcap_response_ptBins = []
    for i in range(len(ptBins)-1):
        response_ptBins.append(ROOT.TH1F("pt_resp_ptBin"+str(ptBins[i])+"to"+str(ptBins[i+1]),"pt_resp_ptBin"+str(ptBins[i])+"to"+str(ptBins[i+1]),res_bins,0,3))
        barrel_response_ptBins.append(ROOT.TH1F("pt_barrel_resp_ptBin"+str(ptBins[i])+"to"+str(ptBins[i+1]),"pt_barrel_resp_ptBin"+str(ptBins[i])+"to"+str(ptBins[i+1]),res_bins,0,3))
        endcap_response_ptBins.append(ROOT.TH1F("pt_endcap_resp_ptBin"+str(ptBins[i])+"to"+str(ptBins[i+1]),"pt_endcap_resp_ptBin"+str(ptBins[i])+"to"+str(ptBins[i+1]),res_bins,0,3))

    # PT RESPONSE -  ETA BINS HISTIGRAMS
    absEta_response_ptBins = []
    minusEta_response_ptBins = []
    plusEta_response_ptBins = []
    for i in range(len(etaBins)-1):
        absEta_response_ptBins.append(ROOT.TH1F("pt_resp_AbsEtaBin"+str(etaBins[i])+"to"+str(etaBins[i+1]),"pt_resp_AbsEtaBin"+str(etaBins[i])+"to"+str(etaBins[i+1]),res_bins,0,3))
        minusEta_response_ptBins.append(ROOT.TH1F("pt_resp_MinusEtaBin"+str(etaBins[i])+"to"+str(etaBins[i+1]),"pt_resp_MinusEtaBin"+str(etaBins[i])+"to"+str(etaBins[i+1]),res_bins,0,3))
        plusEta_response_ptBins.append(ROOT.TH1F("pt_resp_PlusEtaBin"+str(etaBins[i])+"to"+str(etaBins[i+1]),"pt_resp_PlusEtaBin"+str(etaBins[i])+"to"+str(etaBins[i+1]),res_bins,0,3))

    # PT RESPONSE -  H/TOT BINS HISTIGRAMS
    if options.do_HoTot:
        response_HoTotBins = []
        for i in range(len(HoTotBins)-1):
            response_HoTotBins.append(ROOT.TH1F("pt_resp_HoTotBin"+str(HoTotBins[i])+"to"+str(HoTotBins[i+1]),"pt_resp_HoTotBin"+str(HoTotBins[i])+"to"+str(HoTotBins[i+1]),res_bins,0,3))

    # PT RESPONSE -  E/TOT BINS HISTIGRAMS
    if options.do_EoTot:
        response_EoTotBins = []
        for i in range(len(EoTotBins)-1):
            response_EoTotBins.append(ROOT.TH1F("pt_resp_EoTotBin"+str(EoTotBins[i])+"to"+str(EoTotBins[i+1]),"pt_resp_EoTotBin"+str(EoTotBins[i])+"to"+str(EoTotBins[i+1]),res_bins,0,3))

    print(" ### INFO: Start looping on events")
    for i in tqdm(range(0, nevents)):

        entry2 = level1Tree.GetEntry(i)
        entry3 = targetTree.GetEntry(i)
        entry4 = towersTree.GetEntry(i)

        L1_nObjs = 0
        if options.target == 'jet':
            L1_nObjs = level1Tree.L1Upgrade.nJets
            if options.PuppiJet:
                target_nObjs = targetTree.Jet.puppi_nJets
            else:
                target_nObjs = targetTree.Jet.nJets
        if options.target == 'ele':
            L1_nObjs = level1Tree.L1Upgrade.nEGs
            target_nObjs = targetTree.Electron.nElectrons
        if options.target == 'met':
            L1_nObjs = level1Tree.L1Upgrade.nSums #only one MET per event
            # L1_nObjs = 1
            target_nObjs = 1 #only one MET per event


        # loop on target jets
        for itargJet in range(0,target_nObjs):

            if options.target == 'jet':
                targetObj = ROOT.TLorentzVector()
                if options.PuppiJet:
                    targetObj.SetPtEtaPhiM(targetTree.Jet.puppi_etCorr[itargJet], targetTree.Jet.puppi_eta[itargJet], targetTree.Jet.puppi_phi[itargJet], 0)
                else:
                    targetObj.SetPtEtaPhiM(targetTree.Jet.etCorr[itargJet], targetTree.Jet.eta[itargJet], targetTree.Jet.phi[itargJet], 0)

            elif options.target == 'ele':
                targetObj = ROOT.TLorentzVector()
                targetObj.SetPtEtaPhiM(targetTree.Electron.et[itargJet], targetTree.Electron.eta[itargJet], targetTree.Electron.phi[itargJet], 0)

            elif options.target == 'met':
                targetObj = ROOT.TLorentzVector()
                if options.PuppiJet:
                    targetObj.SetPtEtaPhiM(targetTree.Sums.puppi_metNoMu, 0, targetTree.Sums.puppi_metNoMuPhi, 0)
                else:
                    targetObj.SetPtEtaPhiM(targetTree.Sums.pfMetNoMu, 0, targetTree.Sums.pfMetNoMuPhi, 0)

            # skip jets that cannot be reconstructed by L1 (limit is 5.191)
            if targetObj.Eta() > 5.0: continue
            
            ################# APPLY CUTS #################
            if options.jetPtcut: 
                if targetObj.Pt() < float(options.jetPtcut): continue
            if options.etacut: 
                if np.abs(targetObj.Eta()) > float(options.etacut): continue
            if options.target == 'ele' and options.LooseEle:
                if targetTree.Electron.isLooseElectron[itargJet] == 0: continue
            #############################################

            # loop on L1 jets to find match
            matched = False
            highestL1Pt = -99.
            myGood_iL1Obj = 0
            myGoodLevel1Obj = ROOT.TLorentzVector()
            # print("Event ", i)
            # print([level1Tree.L1Upgrade.sumType[iL1Obj] for iL1Obj in range(0, L1_nObjs)])
            for iL1Obj in range(0, L1_nObjs):
                level1Obj = ROOT.TLorentzVector()
                if options.target == 'jet': 
                    if options.raw:
                        # new method of plotting results by just looking at the raw output from the Layer-1
                        level1Obj.SetPtEtaPhiM(level1Tree.L1Upgrade.jetRawEt[iL1Obj]/2, level1Tree.L1Upgrade.jetEta[iL1Obj], level1Tree.L1Upgrade.jetPhi[iL1Obj], 0)
                    else:
                        level1Obj.SetPtEtaPhiM(level1Tree.L1Upgrade.jetEt[iL1Obj], level1Tree.L1Upgrade.jetEta[iL1Obj], level1Tree.L1Upgrade.jetPhi[iL1Obj], 0)
                elif options.target == 'ele': 
                    if options.raw:
                        # new method of plotting results by just looking at the raw output from the Layer-1
                        level1Obj.SetPtEtaPhiM(level1Tree.L1Upgrade.egRawEt[iL1Obj]/2, level1Tree.L1Upgrade.egEta[iL1Obj], level1Tree.L1Upgrade.egPhi[iL1Obj], 0)
                    else:
                        level1Obj.SetPtEtaPhiM(level1Tree.L1Upgrade.egEt[iL1Obj], level1Tree.L1Upgrade.egEta[iL1Obj], level1Tree.L1Upgrade.egPhi[iL1Obj], 0)
                elif options.target == 'met':
                    if level1Tree.L1Upgrade.sumType[iL1Obj] == 8:
                        # level1Obj.SetPtEtaPhiM(level1Tree.L1Upgrade.sumEt[iL1Obj], 0, 0, 0)
                        level1Obj.SetPtEtaPhiM(level1Tree.L1Upgrade.sumIEt[iL1Obj]/2, 0, 0, 0)
                        matched = True
                        myGoodLevel1Obj = level1Obj
                        break
                
                #check matching
                if targetObj.DeltaR(level1Obj)<0.5:
                    matched = True
                    #keep only L1 match with highest pT
                    if level1Obj.Pt() > highestL1Pt:
                        myGoodLevel1Obj = level1Obj
                        myGood_iL1Obj = iL1Obj
                        highestL1Pt = level1Obj.Pt()
        
            # print(targetObj.Pt(), level1Obj.Pt())

            if matched:

                L1Pt = myGoodLevel1Obj.Pt()
                # print(L1Pt, targetObj.Pt())

                iem_sum = 0
                ihad_sum = 0
                if options.do_HoTot or options.do_EoTot:
                    # find Chunky Donut center
                    jetIEta = FindIeta(targetObj.Eta())
                    jetIPhi = FindIphi(targetObj.Phi())
                    jetIEta_L1 = FindIeta(myGoodLevel1Obj.Eta())
                    jetIPhi_L1 = FindIphi(myGoodLevel1Obj.Phi())
                    
                    max_IEta = NextEtaTower(NextEtaTower(NextEtaTower(NextEtaTower(jetIEta))))
                    min_IEta = PrevEtaTower(PrevEtaTower(PrevEtaTower(PrevEtaTower(jetIEta))))
                    max_IPhi = NextPhiTower(NextPhiTower(NextPhiTower(NextPhiTower(jetIPhi))))
                    min_IPhi = PrevPhiTower(PrevPhiTower(PrevPhiTower(PrevPhiTower(jetIPhi))))

                    nTowers = towersTree.L1CaloTower.nTower
                    if min_IPhi <= max_IPhi:
                        for iTower in range(0, nTowers):
                            ieta = towersTree.L1CaloTower.ieta[iTower]
                            iphi = towersTree.L1CaloTower.iphi[iTower]
                            if ((ieta <= max_IEta) & (ieta >= min_IEta) & (iphi <= max_IPhi) & (iphi >= min_IPhi)):
                                iem_sum += towersTree.L1CaloTower.iem[iTower]
                                ihad_sum += towersTree.L1CaloTower.ihad[iTower]
                    else: # when iphi > 72
                        for iTower in range(0, nTowers):
                            ieta = towersTree.L1CaloTower.ieta[iTower]
                            iphi = towersTree.L1CaloTower.iphi[iTower]
                            if ((ieta <= max_IEta) & (ieta >= min_IEta) & ((iphi >= min_IPhi) | (iphi <= max_IPhi))):
                                iem_sum += towersTree.L1CaloTower.iem[iTower]
                                ihad_sum += towersTree.L1CaloTower.ihad[iTower]
                    # print(ihad_sum, iem_sum)
                    if ihad_sum+iem_sum != 0:
                        HoTot = ihad_sum/(ihad_sum+iem_sum)
                        EoTot = iem_sum/(ihad_sum+iem_sum)
                    else:
                        HoTot = 0
                        EoTot = 0

                    # print("Res = {:2f}".format(L1Pt/targetObj.Pt()))

                    ##########################################################################################

                    if options.do_HoTot:
                        for i in range(len(HoTotBins)-1):
                            if HoTot > HoTotBins[i] and HoTot <= HoTotBins[i+1]:
                                response_HoTotBins[i].Fill(L1Pt/targetObj.Pt())
                    if options.do_EoTot:
                        for i in range(len(EoTotBins)-1):
                            if EoTot > EoTotBins[i] and EoTot <= EoTotBins[i+1]:
                                response_EoTotBins[i].Fill(L1Pt/targetObj.Pt())
                    
                    ##########################################################################################

                # fill histograms

                pt_response_ptInclusive.Fill(L1Pt/targetObj.Pt())
                pt_response_ptInclusive_CD.Fill((iem_sum+ihad_sum)/targetObj.Pt()/2)

                if abs(targetObj.Eta()) < 1.305:
                    pt_barrel_resp_ptInclusive.Fill(L1Pt/targetObj.Pt())
                    pt_barrel_resp_ptInclusive_CD.Fill((iem_sum+ihad_sum)/targetObj.Pt()/2)
                elif abs(targetObj.Eta()) < 5.191 and abs(targetObj.Eta()) > 1.479:
                    pt_endcap_resp_ptInclusive.Fill(L1Pt/targetObj.Pt())
                    pt_endcap_resp_ptInclusive_CD.Fill((iem_sum+ihad_sum)/targetObj.Pt()/2)

                for i in range(len(ptBins)-1):
                    if targetObj.Pt() > ptBins[i] and targetObj.Pt() <= ptBins[i+1]:
                        response_ptBins[i].Fill(L1Pt/targetObj.Pt())
                        
                        if abs(targetObj.Eta()) < 1.305:
                            barrel_response_ptBins[i].Fill(L1Pt/targetObj.Pt())
                        elif abs(targetObj.Eta()) < 5.191 and abs(targetObj.Eta()) > 1.479:
                            endcap_response_ptBins[i].Fill(L1Pt/targetObj.Pt())

                for i in range(len(etaBins)-1):
                    if abs(targetObj.Eta()) > etaBins[i] and abs(targetObj.Eta()) < etaBins[i+1]:
                        absEta_response_ptBins[i].Fill(L1Pt/targetObj.Pt())

                    if targetObj.Eta() > etaBins[i] and targetObj.Eta() < etaBins[i+1]:
                        plusEta_response_ptBins[i].Fill(L1Pt/targetObj.Pt())

                    elif targetObj.Eta() < -etaBins[i] and targetObj.Eta() > -etaBins[i+1]:
                        minusEta_response_ptBins[i].Fill(L1Pt/targetObj.Pt())

    ############################################################################################
    ############################################################################################
    ############################################################################################

    print(" ### INFO: Compute resolution and scale")

    # make resolution plots
    pt_resol_fctPt = ROOT.TH1F("pt_resol_fctPt","pt_resol_fctPt",len(ptBins)-1, array('f',ptBins))
    pt_resol_barrel_fctPt = ROOT.TH1F("pt_resol_barrel_fctPt","pt_resol_barrel_fctPt",len(ptBins)-1, array('f',ptBins))
    pt_resol_endcap_fctPt = ROOT.TH1F("pt_resol_endcap_fctPt","pt_resol_endcap_fctPt",len(ptBins)-1, array('f',ptBins))
    pt_resol_fctAbsEta = ROOT.TH1F("pt_resol_fctAbsEta","pt_resol_fctAbsEta",len(etaBins)-1, array('f',etaBins))
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

    ############################################################################################
    ############################################################################################
    ############################################################################################

    print(" ### INFO: Saving to root format")
    fileout = ROOT.TFile(outdir+'/PerformancePlots'+options.tag+'/'+label+'/ROOTs/resolution_graphs_'+label+'_'+options.target+'.root','RECREATE')
    pt_scale_fctPt.Write()
    pt_scale_fctEta.Write()
    if options.do_HoTot:
        pt_scale_fctHoTot.Write()
        pt_scale_max_fctHoTot.Write()
        pt_resol_fctHoTot.Write()
    if options.do_EoTot:
        pt_scale_fctEoTot.Write()
        pt_scale_max_fctEoTot.Write()
        pt_resol_fctEoTot.Write()
    pt_scale_max_fctPt.Write()
    pt_scale_max_fctEta.Write()
    pt_resol_fctPt.Write()
    pt_resol_barrel_fctPt.Write()
    pt_resol_endcap_fctPt.Write()
    pt_resol_fctAbsEta.Write()
    pt_resol_fctEta.Write()
    pt_response_ptInclusive.Write()
    pt_barrel_resp_ptInclusive.Write()
    pt_endcap_resp_ptInclusive.Write()
    pt_response_ptInclusive_CD.Write()
    pt_barrel_resp_ptInclusive_CD.Write()
    pt_endcap_resp_ptInclusive_CD.Write()
    for i in range(len(response_ptBins)):
        response_ptBins[i].Write()
        barrel_response_ptBins[i].Write()
        endcap_response_ptBins[i].Write()
    for i in range(len(minusEta_response_ptBins)):
        absEta_response_ptBins[i].Write()
        minusEta_response_ptBins[i].Write()
        plusEta_response_ptBins[i].Write()
    if options.do_HoTot:
        for i in range(len(response_HoTotBins)):
            response_HoTotBins[i].Write()
    if options.do_EoTot:
        for i in range(len(response_EoTotBins)):
            response_EoTotBins[i].Write()

    if options.no_plot:
        sys.exit()

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
    pt_resol_fctAbsEta = filein.Get('pt_resol_fctAbsEta')
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

def GetArraysFromHisto(histo):
    X = [] ; Y = [] ; X_err = [] ; Y_err = []
    for ibin in range(0,histo.GetNbinsX()):
        X.append(histo.GetBinLowEdge(ibin+1) + histo.GetBinWidth(ibin+1)/2.)
        Y.append(histo.GetBinContent(ibin+1))
        X_err.append(histo.GetBinWidth(ibin+1)/2.)
        Y_err.append(histo.GetBinError(ibin+1))
    return X,Y,X_err,Y_err

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
