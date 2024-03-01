#!/usr/bin/bash

ECAL=$1
HCAL=$2
re_emu=$3

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
alias cd_launch='cd '"${SCRIPT_DIR}"'/../../L1NtupleLauncher/'
alias cd_back='cd '"${SCRIPT_DIR}"'/../../L1JaxTraining/'

#################################################################################
# TESTING 
#################################################################################

python3 ProduceCaloParams.py --name caloParams_2023_JAX_"${ECAL}"_"${HCAL}"_newCalib_cfi \
 --HCAL Trainings_2023/JAX_"${HCAL}"/ScaleFactors_HCAL.csv \
 --HF Trainings_2023/JAX_"${HCAL}"/ScaleFactors_HCAL.csv \
 --ECAL Trainings_2023/JAX_"${ECAL}"/ScaleFactors_ECAL.csv \
 --base caloParams_2023_v0_4_cfi.py

python3 ProduceCaloParams.py --name caloParams_2023_JAX_"${ECAL}"_"${HCAL}"_Phys_newCalib_cfi \
 --HCAL Trainings_2023/JAX_"${HCAL}"/ScaleFactors_HCAL_Phys.csv \
 --HF Trainings_2023/JAX_"${HCAL}"/ScaleFactors_HCAL_Phys.csv \
 --ECAL Trainings_2023/JAX_"${ECAL}"/ScaleFactors_ECAL_Phys.csv \
 --base caloParams_2023_v0_4_cfi.py

# plot Jet
python3 RDF_ResolutionFast.py --indir JetMET__Run2023B-PromptReco-v1__Run367079__AOD__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
 --reco --target jet --do_HoTot --raw --PuppiJet --jetPtcut 30 --nEvts 100000 --no_plot \
 --HCALcalib --caloParam caloParams_2023_JAX_"${ECAL}"_"${HCAL}"_newCalib_cfi.py --outdir Trainings_2023/FullCalib/JAX_"${ECAL}"_"${HCAL}"/NtuplesVnew --no_Satu
python3 comparisonPlotsFast.py --target jet --reco --do_HoTot \
 --old Trainings_2023/JAX_HCAL_0/NtuplesVold --unc Trainings_2023/JAX_HCAL_0/NtuplesVunc \
 --indir Trainings_2023/FullCalib/JAX_"${ECAL}"_"${HCAL}"/NtuplesVnew

# plot EGamma
python3 RDF_ResolutionFast.py --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
 --reco --target ele --do_EoTot --raw --LooseEle --nEvts 100000 --no_plot \
 --ECALcalib --caloParam caloParams_2023_JAX_"${ECAL}"_"${HCAL}"_newCalib_cfi.py --outdir Trainings_2023/FullCalib/JAX_"${ECAL}"_"${HCAL}"/NtuplesVnew 
python3 comparisonPlotsFast.py --target ele --reco \
 --old Trainings_2023/JAX_ECAL_0/NtuplesVold --unc Trainings_2023/JAX_ECAL_0/NtuplesVunc \
 --do_HoTot --doRate False --doTurnOn False \
 --indir Trainings_2023/FullCalib/JAX_"${ECAL}"_"${HCAL}"/NtuplesVnew

#################################################################################
# RE-EMULATION 
#################################################################################

if [ "$re_emu" != "NO" ]; then

cd_launch

python3 submitOnTier3.py --inFileList EphemeralZeroBias__Run2023D-v1__Run369870__RAW \
 --outTag GT130XdataRun3Promptv4_CaloParams2023JAX_"${ECAL}"_"${HCAL}"_data \
 --nJobs 151 --queue short --maxEvts 2000 \
 --globalTag 130X_dataRun3_Prompt_v4 --data \
 --caloParams caloParams_2023_JAX_"${ECAL}"_"${HCAL}"_Phys_newCalib_cfi

python3 submitOnTier3.py --inFileList JetMET__Run2023B-PromptReco-v1__Run367079__AOD \
 --outTag GT130XdataRun3Promptv4_CaloParams2023JAX_"${ECAL}"_"${HCAL}"_data_reco_json \
 --inJson Cert_Collisions2023_366442_370790_Golden \
 --nJobs 39 --queue short --maxEvts 3000 \
 --globalTag 130X_dataRun3_Prompt_v4 --data --recoFromAOD \
 --caloParams caloParams_2023_JAX_"${ECAL}"_"${HCAL}"_Phys_newCalib_cfi

python submitOnTier3.py --inFileList EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO \
    --outTag GT130XdataRun3Promptv4_CaloParams2023JAX_"${ECAL}"_"${HCAL}"_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --globalTag 130X_dataRun3_Prompt_v4 \
    --nJobs 300 --queue short --maxEvts -1 --data --recoFromSKIM \
    --caloParams caloParams_2023_JAX_"${ECAL}"_"${HCAL}"_Phys_newCalib_cfi

cd_back

fi