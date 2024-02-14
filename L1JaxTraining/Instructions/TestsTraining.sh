#!/usr/bin/bash
# An NVIDIA GPU may be present on this machine, but a CUDA-enabled jaxlib is not installed. Falling back to cpu.

number=$1

#################################################################################
# TRAINING 
#################################################################################

# energy binning is defined here and propagated everywhere
# python3 JaxOptimizerRate.py --odir Trainings/$number --jetsLim 1000000 --lr 0.5 --bs 2048 --ep 50
# python3 JaxOptimizer.py --odir Trainings/$number --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 50 --scale 0.75 --norm
# python3 JaxOptimizerBinSize.py --odir Trainings/$number --jetsLim 1000000 --lr 1.5 --bs 4096 --ep 50

python3 SFPlots.py --indir Trainings/$number

python3 ProduceCaloParams.py --name caloParams_2023_JAX"${number}"_newCalib_cfi --HCAL ./Trainings/"${number}"/ScaleFactors_HCAL.csv

#################################################################################
# TESTING PLOTS
#################################################################################

python3 RDF_ResolutionFast.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
 --reco --target jet --do_HoTot --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot \
 --HCALcalib --caloParam caloParams_2023_JAX"${number}"_newCalib_cfi.py --outdir Trainings/"${number}"/NtuplesVnew

# python3 RDF_Resolution.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
#  --reco --target jet --do_HoTot --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot \
#  --HCALcalib --caloParam caloParams_2023_v0_2_cfi.py --outdir 0/NtuplesVold
# cp 0/NtuplesVold $number

# python3 RDF_Resolution.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
#  --reco --target jet --do_HoTot --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot \
#  --outdir 0/NtuplesVunc
# cp 0/NtuplesVunc $number

python3 comparisonPlotsFast.py --indir Trainings/"${number}"/NtuplesVnew --target jet --reco \
 --old Trainings/0/NtuplesVold --unc Trainings/0/NtuplesVunc \
 --do_HoTot --doRate False --doTurnOn False

#################################################################################
# RE-EMULATION 
#################################################################################

alias cd_launch='cd /data_CMS/cms/vernazza/L1TCalibration/CMSSW_13_1_0_pre4_Fix/CMSSW_13_1_0_pre4/src/CaloL1CalibrationProducer/L1NtupleLauncher'

cd_launch

python3 submitOnTier3.py --inFileList EphemeralZeroBias0__Run2022G-v1__Run362617__RAW \
 --outTag GT130XdataRun3Promptv3_CaloParams2023JAX"${number}"_data \
 --nJobs 31 --queue short --maxEvts 5000 \
 --globalTag 130X_dataRun3_Prompt_v3 --data \
 --caloParams caloParams_2023_JAX"${number}"_newCalib_cfi

tag+="_reco_json"
python3 submitOnTier3.py --inFileList JetMET__Run2022G-PromptReco-v1__Run362617__AOD \
 --outTag GT130XdataRun3Promptv3_CaloParams2023JAX"${number}"_data_reco_json \
 --nJobs 31 --queue short --maxEvts 5000 --inJson Cert_Collisions2022_355100_362760_Golden \
 --globalTag 130X_dataRun3_Prompt_v3 --data --recoFromAOD \
 --caloParams caloParams_2023_JAX"${number}"_newCalib_cfi

alias cd_back='cd /data_CMS/cms/vernazza/L1TCalibration/CMSSW_13_1_0_pre4_Fix/CMSSW_13_1_0_pre4/src/CaloL1CalibrationProducer/L1JaxTraining'

cd_back

# #################################################################################
# # REFERENCE 
# #################################################################################

# # '''
# # python3 JaxOptimizer.py --odir 6 --filesLim 20 --lr 0.001 --bs 1 --ep 50 --mask
# # python3 SFPlots.py --indir 6
# # python3 ProduceCaloParams.py --name caloParams_2023_JAX6_newCalib_cfi --HCAL 6/ScaleFactors_HCAL.csv

# # python3 RDF_Resolution.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
# #  --reco --target jet --do_HoTot --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot \
# #  --HCALcalib --caloParam caloParams_2023_JAX6_newCalib_cfi.py --outdir 6/NtuplesVnew
# # python3 comparisonPlots.py --target jet --reco \
# #  --old 0/NtuplesVold --unc 0/NtuplesVunc \
# #  --do_HoTot --doRate False --doTurnOn False --indir 6/NtuplesVnew

# # python3 submitOnTier3.py --inFileList JetMET__Run2022G-PromptReco-v1__Run362617__AOD \
# #  --outTag GT130XdataRun3Promptv3_CaloParams2023JAX34_data_reco_json \
# #  --nJobs 31 --queue short --maxEvts 5000 --inJson Cert_Collisions2022_355100_362760_Golden \
# #  --globalTag 130X_dataRun3_Prompt_v3 --data --recoFromAOD \
# #  --caloParams caloParams_2023_JAX34_newCalib_cfi 

# # python3 submitOnTier3.py --inFileList EphemeralZeroBias0__Run2022G-v1__Run362617__RAW \
# #  --outTag GT130XdataRun3Promptv3_CaloParams2023JAX34_data \
# #  --nJobs 31 --queue short --maxEvts 5000 \
# #  --globalTag 130X_dataRun3_Prompt_v3 --data \
# #  --caloParams caloParams_2023_JAX34_newCalib_cfi 
# # # '''