import os,sys

#######################################################################
######################### SCRIPT BODY #################################
#######################################################################

# python3 RunPerformance.py --addtag _A

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--addtag",       dest="addtag",      default=''      )
(options, args) = parser.parse_args()

run = True
indir1 = '2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95'
indir2 = '2023_12_13_NtuplesV56/Input2/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot70'
indir3 = '2023_12_13_NtuplesV56/Input3/JetMET_PuppiJet_BarrelEndcap_Pt60_HoTot70'
indir4 = '2023_12_13_NtuplesV56/Input4/JetMET_PuppiJet_BarrelEndcap_PtRaw60_HoTot70'

for i, indir in enumerate([indir1, indir2, indir3, indir4]):
    log_file = os.getcwd() + '/RunInstructions/Instructions_Input' + str(i+1) + options.addtag + '.sh'

    # cmd = 'loadGPUtf \n\n'
    # cmd += 'python3 CalibrationFactor.py --indir ' + indir1 + ' --v HCAL --tag DataReco --reg HCAL --energystep 2 --addtag ' + options.addtag + '\n\n'
    # cmd += 'python3 CalibrationFactor.py --indir ' + indir1 + ' --v HCAL --tag DataReco --reg HF --energystep 2 --addtag ' + options.addtag + '\n\n'

    # cmd += 'python3 ProduceCaloParams.py --name caloParams_2023_v56' + options.addtag + '_Input' + str(i+1) + '_cfi \ \n'
    # cmd += ' --base caloParams_2023_v0_2_noL1Calib_cfi.py \ \n'
    # cmd += ' --ECAL /data_CMS/cms/motta/CaloL1calibraton/2023_03_06_NtuplesV33/ECALtrainingDataReco_normalOrder/data/ScaleFactors_ECAL_energystep2iEt.csv \ \n'
    # cmd += ' --HCAL /data_CMS/cms/motta/CaloL1calibraton/' + indir + '/HCALtrainingDataReco/model_HCAL' + options.addtag + '/SFs_2iEt/ScaleFactors_HCAL_energystep2iEt.csv \ \n'
    # cmd += ' --HF   /data_CMS/cms/motta/CaloL1calibraton/' + indir + '/HCALtrainingDataReco/model_HCAL' + options.addtag + '/SFs_2iEt/ScaleFactors_HF_energystep2iEt.csv \ \n\n'
    
    # resolution plots uncalib
    cmd = []
    cmd.append('cmsenv \n')
    uncalib_outdir = indir + '/HCALtrainingDataReco/model_HCAL' + options.addtag + '/NtuplesVunc_Raw_Puppi_BarrelEndcap_Pt30'
    cmd.append('python3 RDF_Resolution.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \\')
    cmd.append(' --outdir ' + uncalib_outdir + ' --label Muon_data_reco --reco --target jet --do_HoTot \\')
    cmd.append(' --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot \n')
    # resolution plots oldcalib
    oldcalib_outdir = indir + '/HCALtrainingDataReco/model_HCAL' + options.addtag + '/NtuplesVold_Raw_Puppi_BarrelEndcap_Pt30'
    cmd.append('python3 RDF_Resolution.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \\')
    cmd.append(' --outdir ' + oldcalib_outdir + ' --label Muon_data_reco --reco --target jet --do_HoTot \\')
    cmd.append(' --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot --HCALcalib --ECALcalib --caloParam caloParams_2023_v0_2_cfi.py \n')
    # resolution plots newcalib
    newcalib_outdir = indir + '/HCALtrainingDataReco/model_HCAL' + options.addtag + '/NtuplesVnew_Raw_Puppi_BarrelEndcap_Pt30'
    cmd.append('python3 RDF_Resolution.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \\')
    cmd.append(' --outdir ' + newcalib_outdir + ' --label Muon_data_reco --reco --target jet --do_HoTot \\')
    cmd.append(' --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot --HCALcalib --ECALcalib --caloParam caloParams_2023_v56' + options.addtag + '_Input' + str(i+1) + '_cfi.py \n')

    # comparison plots
    cmd.append('python3 comparisonPlots.py --indir ' + newcalib_outdir + ' --label Muon_data_reco  --target jet --reco \\')
    cmd.append(' --old ' + oldcalib_outdir + ' \\')
    cmd.append(' --unc ' + uncalib_outdir + ' \\')
    cmd.append(' --do_HoTot --doTurnOn False --doRate False \n')

    file = open (log_file, 'w')
    for line in cmd:
        file.write(line + '\n')
    file.close()
