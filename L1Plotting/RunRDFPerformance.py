import os,sys

#######################################################################
######################### SCRIPT BODY #################################
#######################################################################

# python3 RunPerformance.py --addtag _A

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--indir",            dest="indir",                                                                  default='1,2,3,4'                    )
parser.add_option("--addtag",       dest="addtag",      default=''      )
(options, args) = parser.parse_args()

run = True
indir1 = '2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95'
indir2 = '2023_12_13_NtuplesV56/Input2/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot70'
indir3 = '2023_12_13_NtuplesV56/Input3/JetMET_PuppiJet_BarrelEndcap_Pt60_HoTot70'
indir4 = '2023_12_13_NtuplesV56/Input4/JetMET_PuppiJet_BarrelEndcap_PtRaw60_HoTot70'

indirs = [indir1, indir2, indir3, indir4]

for i in options.indir.split(','):

    indir = indirs[int(i)-1]
    log_file = os.getcwd() + '/RunInstructions/RDFPerformance_Input' + i + options.addtag + '.sh'

    # resolution and turn on plots uncalib
    cmd = []
    cmd.append('cmsenv \n')
    uncalib_outdir = indir + '/HCALtrainingDataReco/model_HCAL' + options.addtag + '/NtuplesVunc_Raw_Puppi_BarrelEndcap_Pt30'
    cmd.append('python3 RDF_Resolution.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \\')
    cmd.append(' --outdir ' + uncalib_outdir + ' --label CD_data_reco --reco --target jet --do_HoTot \\')
    cmd.append(' --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot \n')
    # resolution and turn on plots oldcalib
    oldcalib_outdir = indir + '/HCALtrainingDataReco/model_HCAL' + options.addtag + '/NtuplesVold_Raw_Puppi_BarrelEndcap_Pt30'
    cmd.append('python3 RDF_Resolution.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \\')
    cmd.append(' --outdir ' + oldcalib_outdir + ' --label CD_data_reco --reco --target jet --do_HoTot \\')
    cmd.append(' --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot --HCALcalib --ECALcalib --caloParam caloParams_2023_v0_2_cfi.py \n')
    # resolution and turn on plots newcalib
    newcalib_outdir = indir + '/HCALtrainingDataReco/model_HCAL' + options.addtag + '/NtuplesVnew_Raw_Puppi_BarrelEndcap_Pt30'
    cmd.append('python3 RDF_Resolution.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \\')
    cmd.append(' --outdir ' + newcalib_outdir + ' --label CD_data_reco --reco --target jet --do_HoTot \\')
    cmd.append(' --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot --HCALcalib --ECALcalib --caloParam caloParams_2023_v56' + options.addtag + '_Input' + str(i+1) + '_cfi.py \n')

    # rate plots uncalib
    uncalib_outdir = indir + '/HCALtrainingDataReco/model_HCAL' + options.addtag + '/NtuplesVunc_Raw_Puppi_BarrelEndcap_Pt30'
    cmd.append('python3 RDF_Rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data \\')
    cmd.append(' --outdir ' + uncalib_outdir + ' --label CD_data_reco --target jet \\')
    cmd.append(' --raw --nEvts 100000 --no_plot \n')
    # rate plots oldcalib
    oldcalib_outdir = indir + '/HCALtrainingDataReco/model_HCAL' + options.addtag + '/NtuplesVold_Raw_Puppi_BarrelEndcap_Pt30'
    cmd.append('python3 RDF_Rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data \\')
    cmd.append(' --outdir ' + oldcalib_outdir + ' --label CD_data_reco --target jet \\')
    cmd.append(' --raw --nEvts 100000 --no_plot --HCALcalib --ECALcalib --caloParam caloParams_2023_v0_2_cfi.py \n')
    # rate plots newcalib
    newcalib_outdir = indir + '/HCALtrainingDataReco/model_HCAL' + options.addtag + '/NtuplesVnew_Raw_Puppi_BarrelEndcap_Pt30'
    cmd.append('python3 RDF_Rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data \\')
    cmd.append(' --outdir ' + newcalib_outdir + ' --label CD_data_reco --target jet \\')
    cmd.append(' --raw --nEvts 100000 --no_plot --HCALcalib --ECALcalib --caloParam caloParams_2023_v56' + options.addtag + '_Input' + str(i+1) + '_cfi.py \n')

    # comparison plots
    cmd.append('python3 comparisonPlots.py --indir ' + newcalib_outdir + ' --label CD_data_reco  --target jet --reco \\')
    cmd.append(' --old ' + oldcalib_outdir + ' \\')
    cmd.append(' --unc ' + uncalib_outdir + ' \\')
    cmd.append(' --do_HoTot --thrsFixRate 30 --thrsFixRate 40 --thrsFixRate 60 --thrsFixRate 80 \n')

    file = open (log_file, 'w')
    for line in cmd:
        file.write(line + '\n')
    file.close()
