import os,sys

#######################################################################
######################### SCRIPT BODY #################################
#######################################################################

# python3 MoveToEos.py --addtag _A --indir 1
# python3 MoveToEos.py --addtag _B --indir 2,3,4

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--indir",        dest="indir",       default='1,2,3,4')
parser.add_option("--addtag",       dest="addtag",      default=''       )
(options, args) = parser.parse_args()

run = True
indir1 = '2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95'
indir2 = '2023_12_13_NtuplesV56/Input2/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot70'
indir3 = '2023_12_13_NtuplesV56/Input3/JetMET_PuppiJet_BarrelEndcap_Pt60_HoTot70'
indir4 = '2023_12_13_NtuplesV56/Input4/JetMET_PuppiJet_BarrelEndcap_PtRaw60_HoTot70'

indirs = [indir1, indir2, indir3, indir4]

for i in options.indir.split(','):
    indir = indirs[int(i)-1]

    # move plots to eos
    maindir = '/data_CMS/cms/motta/CaloL1calibraton/' + indir + '/HCALtrainingDataReco/model_HCAL' + options.addtag
    label = 'Jet_data_reco'
    perfdir_PNG = maindir + f'/NtuplesVnew_Raw_Puppi_BarrelEndcap_Pt30/PerformancePlots/{label}/PNGs/comparisons_{label}_jet/'
    perfdir_PDF = maindir + f'/NtuplesVnew_Raw_Puppi_BarrelEndcap_Pt30/PerformancePlots/{label}/PDFs/comparisons_{label}_jet/'
    eosdir = '/eos/home-e/evernazz/www/L1Trigger/PerformancePlots/Input' + i + '/model_HCAL' + options.addtag
    os.system('mkdir -p '+eosdir)
    os.system('cp '+eosdir+'/../index.php '+eosdir)
    for dir in ['ptBins', 'etaBins', 'HoTotBins', 'Resolution', 'Losses']:
        os.system('mkdir -p '+eosdir+'/'+dir)
        os.system('cp '+eosdir+'/../index.php '+eosdir+'/'+dir)

    os.system('cp '+maindir+'/loss_plots/trainLosses.* '+eosdir+'/Losses')
    os.system('cp '+maindir+'/loss_plots/testLosses.* '+eosdir+'/Losses')
    for dir in [perfdir_PNG, perfdir_PDF]:
        os.system('cp '+dir+f'response_inclusive_res_{label}_jet.* '+eosdir)
        os.system('cp '+dir+f'resolution_etaBins_{label}_jet.* '+eosdir+'/Resolution')
        os.system('cp '+dir+f'resolution_HoTotBins_{label}_jet.* '+eosdir+'/Resolution')
        os.system('cp '+dir+f'resolution_ptBins_{label}_jet.* '+eosdir+'/Resolution')
        os.system('cp '+dir+f'scale_etaBins_{label}_jet.* '+eosdir+'/Resolution')
        os.system('cp '+dir+f'scale_HoTotBins_{label}_jet.* '+eosdir+'/Resolution')
        os.system('cp '+dir+f'scale_ptBins_{label}_jet.* '+eosdir+'/Resolution')
        os.system('cp '+dir+f'rate_Obj_{label}_jet.* '+eosdir)
        os.system('cp '+dir+f'rate_ObjEr2p5_{label}_jet.* '+eosdir)
        os.system('cp '+dir+f'turnon* '+eosdir)

        os.system('cp '+dir+f'response_*pt*_{label}_jet.* '+eosdir+'/ptBins')
        os.system('cp '+dir+f'response_*eta*_{label}_jet.* '+eosdir+'/etaBins')
        os.system('cp '+dir+f'response_*HoTot*_{label}_jet.* '+eosdir+'/HoTotBins')