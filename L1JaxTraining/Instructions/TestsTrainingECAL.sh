#!/usr/bin/bash
# An NVIDIA GPU may be present on this machine, but a CUDA-enabled jaxlib is not installed. Falling back to cpu.

number=$1
re_emu=$2
SCRIPT_DIR_ECAL=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
alias cd_launch_ECAL='cd '"${SCRIPT_DIR_ECAL}"'/../../L1NtupleLauncher/'
alias cd_back_ECAL='cd '"${SCRIPT_DIR}"'/../../L1JaxTraining/'

#################################################################################
# TRAINING 
#################################################################################

python3 SFPlots.py --indir Trainings_2023/"${number}" --v ECAL

python3 ProduceCaloParams.py --name caloParams_2023_"${number}"_newCalib_cfi \
 --ECAL Trainings_2023/"${number}"/ScaleFactors_ECAL.csv \
 --base caloParams_2023_v0_4_cfi.py

#################################################################################
# TESTING PLOTS
#################################################################################

python3 RDF_ResolutionFast.py --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
 --reco --target ele --do_EoTot --raw --LooseEle --nEvts 100000 --no_plot \
 --ECALcalib --caloParam caloParams_2023_"${number}"_newCalib_cfi.py --outdir Trainings_2023/"${number}"/NtuplesVnew

# python3 RDF_ResolutionFast.py --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
#  --reco --target ele --do_EoTot --raw --LooseEle --nEvts 100000 --no_plot \
#  --ECALcalib --caloParam caloParams_2023_v0_4_cfi.py \
#  --outdir Trainings_2023/JAX_ECAL_0/NtuplesVold

# python3 RDF_ResolutionFast.py --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
#  --reco --target ele --do_EoTot --raw --LooseEle --nEvts 100000 --no_plot \
#  --ECALcalib --caloParam caloParams_2023_v0_4_noL1Calib_cfi.py \
#  --outdir Trainings_2023/JAX_ECAL_0/NtuplesVunc

python3 comparisonPlotsFast.py --indir Trainings_2023/"${number}"/NtuplesVnew --target ele --reco \
 --old Trainings_2023/JAX_ECAL_0/NtuplesVold --unc Trainings_2023/JAX_ECAL_0/NtuplesVunc \
 --do_EoTot --doRate False --doTurnOn False

#################################################################################
# RE-EMULATION 
#################################################################################

if [ "$re_emu" != "NO" ]; then

cd_launch_ECAL

# python3 submitOnTier3.py --inFileList EphemeralZeroBias__Run2023D-v1__Run369870__RAW \
#     --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data \
#     --nJobs 151 --queue short --maxEvts 2000 \
#     --globalTag 130X_dataRun3_Prompt_v4 --data \
#     --caloParams caloParams_2023_v0_4_noL1Calib_cfi
# python3 submitOnTier3.py --inFileList EphemeralZeroBias__Run2023D-v1__Run369870__RAW \
#     --outTag GT130XdataRun3Promptv4_CaloParams2023v04_data \
#     --nJobs 151 --queue short --maxEvts 2000 \
#     --globalTag 130X_dataRun3_Prompt_v4 --data \
#     --caloParams caloParams_2023_v0_4_cfi
python3 submitOnTier3.py --inFileList EphemeralZeroBias__Run2023D-v1__Run369870__RAW \
 --outTag GT130XdataRun3Promptv4_CaloParams2023"${number}"_data \
 --nJobs 151 --queue short --maxEvts 2000 \
 --globalTag 130X_dataRun3_Prompt_v4 --data \
 --caloParams caloParams_2023_"${number}"_newCalib_cfi

# python submitOnTier3.py --inFileList EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO \
#     --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json \
#     --inJson Cert_Collisions2023_366442_370790_Golden \
#     --globalTag 130X_dataRun3_Prompt_v4 \
#     --nJobs 300 --queue short --maxEvts -1 --data --recoFromSKIM \
#     --caloParams caloParams_2023_v0_4_noL1Calib_cfi
# python submitOnTier3.py --inFileList EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO \
#     --outTag GT130XdataRun3Promptv4_CaloParams2023v04_data_reco_json \
#     --inJson Cert_Collisions2023_366442_370790_Golden \
#     --globalTag 130X_dataRun3_Prompt_v4 \
#     --nJobs 300 --queue short --maxEvts -1 --data --recoFromSKIM \
#     --caloParams caloParams_2023_v0_4_cfi
python submitOnTier3.py --inFileList EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO \
    --outTag GT130XdataRun3Promptv4_CaloParams2023"${number}"_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --globalTag 130X_dataRun3_Prompt_v4 \
    --nJobs 300 --queue short --maxEvts -1 --data --recoFromSKIM \
    --caloParams caloParams_2023_"${number}"_newCalib_cfi

cd_back_ECAL

fi