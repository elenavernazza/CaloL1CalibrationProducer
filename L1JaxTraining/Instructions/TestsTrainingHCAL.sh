#!/usr/bin/bash
# An NVIDIA GPU may be present on this machine, but a CUDA-enabled jaxlib is not installed. Falling back to cpu.

number=$1
re_emu=$2
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
alias cd_launch='cd '"${SCRIPT_DIR}"'/../../L1NtupleLauncher/'
alias cd_back='cd '"${SCRIPT_DIR}"'/../../L1JaxTraining/'

#################################################################################
# TRAINING 
#################################################################################

# energy binning is defined here and propagated everywhere
# python3 JaxOptimizerRate.py --odir Trainings/$number --jetsLim 1000000 --lr 0.5 --bs 2048 --ep 50
# python3 JaxOptimizer.py --odir Trainings/$number --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 50 --scale 0.75 --norm
# python3 JaxOptimizerBinSize.py --odir Trainings/$number --jetsLim 1000000 --lr 1.5 --bs 4096 --ep 50

python3 SFPlots.py --indir Trainings_2023/"${number}" --v HCAL

python3 ProduceCaloParams.py --name caloParams_2023_"${number}"_newCalib_cfi \
 --HCAL Trainings_2023/"${number}"/ScaleFactors_HCAL_Phys.csv \
 --HF Trainings_2023/"${number}"/ScaleFactors_HCAL_Phys.csv \
 --base caloParams_2023_v0_4_cfi.py

#################################################################################
# TESTING PLOTS
#################################################################################

python3 RDF_ResolutionFast.py --indir JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
 --reco --target jet --do_HoTot --raw --PuppiJet --jetPtcut 30 --nEvts 100000 --no_plot \
 --HCALcalib --caloParam caloParams_2023_"${number}"_newCalib_cfi.py --outdir Trainings_2023/"${number}"/NtuplesVnew --no_Satu

# python3 RDF_Resolution.py --indir JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
#  --reco --target jet --do_HoTot --raw --PuppiJet --jetPtcut 30 --nEvts 100000 \
#  --HCALcalib --caloParam caloParams_2023_v0_4_cfi.py \
#  --outdir Trainings_2023/JAX_HCAL_0/NtuplesVold --no_Satu

# python3 RDF_Resolution.py --indir JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
#  --reco --target jet --do_HoTot --raw --PuppiJet --jetPtcut 30 --nEvts 100000 \
#  --HCALcalib --caloParam caloParams_2023_v0_4_noL1Calib_cfi.py \
#  --outdir Trainings_2023/JAX_HCAL_0/NtuplesVunc --no_Satu

python3 comparisonPlotsFast.py --target jet --reco --do_HoTot \
 --old Trainings_2023/JAX_HCAL_0/NtuplesVold --unc Trainings_2023/JAX_HCAL_0/NtuplesVunc \
 --indir Trainings_2023/"${number}"/NtuplesVnew

#################################################################################
# RE-EMULATION 
#################################################################################

if [ "$re_emu" != "NO" ]; then

cd_launch

# python3 submitOnTier3.py --inFileList EphemeralZeroBias__Run2023D-v1__RAW__Testing \
#     --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data \
#     --nJobs 151 --queue short --maxEvts 2000 \
#     --globalTag 130X_dataRun3_Prompt_v4 --data \
#     --caloParams caloParams_2023_v0_4_noL1Calib_cfi
# python3 submitOnTier3.py --inFileList EphemeralZeroBias__Run2023D-v1__RAW__Testing \
#     --outTag GT130XdataRun3Promptv4_CaloParams2023v04_data \
#     --nJobs 151 --queue short --maxEvts 2000 \
#     --globalTag 130X_dataRun3_Prompt_v4 --data \
#     --caloParams caloParams_2023_v0_4_cfi
python3 submitOnTier3.py --inFileList EphemeralZeroBias__Run2023D-v1__RAW__Testing \
 --outTag GT130XdataRun3Promptv4_CaloParams2023"${number}"_data \
 --nJobs 151 --queue short --maxEvts 2000 \
 --globalTag 130X_dataRun3_Prompt_v4 --data \
 --caloParams caloParams_2023_"${number}"_newCalib_cfi

# python3 submitOnTier3.py --inFileList JetMET__Run2023D-PromptReco-v2__AOD__Testing \
#     --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json \
#     --inJson Cert_Collisions2023_366442_370790_Golden \
#     --nJobs 39 --queue short --maxEvts 3000 \
#     --globalTag 130X_dataRun3_Prompt_v4 --data --recoFromAOD \
#     --caloParams caloParams_2023_v0_4_noL1Calib_cfi
# python3 submitOnTier3.py --inFileList JetMET__Run2023D-PromptReco-v2__AOD__Testing \
#     --outTag GT130XdataRun3Promptv4_CaloParams2023v04_data_reco_json \
#     --inJson Cert_Collisions2023_366442_370790_Golden \
#     --nJobs 39 --queue short --maxEvts 3000 \
#     --globalTag 130X_dataRun3_Prompt_v4 --data --recoFromAOD \
#     --caloParams caloParams_2023_v0_4_cfi
python3 submitOnTier3.py --inFileList JetMET__Run2023D-PromptReco-v2__AOD__Testing \
 --outTag GT130XdataRun3Promptv4_CaloParams2023"${number}"_data_reco_json \
 --inJson Cert_Collisions2023_366442_370790_Golden \
 --nJobs 39 --queue short --maxEvts 3000 \
 --globalTag 130X_dataRun3_Prompt_v4 --data --recoFromAOD \
 --caloParams caloParams_2023_"${number}"_newCalib_cfi

cd_back

fi