#!/usr/bin/bash

number=$1
if [ -n "$2" ]; then
    suffix=$2
    dataset_tag="${suffix}_"
else
    suffix="L1ptNoSatu"
    dataset_tag=""
fi

############################################################################################################################
############################################################################################################################
############################################################################################################################

# python3 ../L1Plotting/rate.py --indir EphemeralZeroBias__Run2023D-v1__RAW__Testing__GT130XdataRun3Promptv4_"${dataset_tag}"CaloParams2023v04_noL1Calib_data \
#  --outdir 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVunc"${suffix}" --target jet --raw --nEvts 100000 --no_plot

# python3 ../L1Plotting/rate.py --indir EphemeralZeroBias__Run2023D-v1__RAW__Testing__GT130XdataRun3Promptv4_"${dataset_tag}"CaloParams2023v04_data \
#  --outdir 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVold"${suffix}" --target jet --raw --nEvts 100000 --no_plot

python3 ../L1Plotting/rate.py --indir EphemeralZeroBias__Run2023D-v1__RAW__Testing__GT130XdataRun3Promptv4_CaloParams2023"${number}"_data \
 --outdir 2024_03_05_NtuplesV59/"${number}"/NtuplesVnew --target jet --raw --nEvts 100000 --no_plot --tag "${suffix}"

# python3 ../L1Plotting/turnOn.py --indir JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_"${dataset_tag}"CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
#  --outdir 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVunc"${suffix}" --reco --target jet --raw --PuppiJet --nEvts 100000

# python3 ../L1Plotting/turnOn.py --indir JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_"${dataset_tag}"CaloParams2023v04_data_reco_json/GoodNtuples \
#  --outdir 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVold"${suffix}" --reco --target jet --raw --PuppiJet --nEvts 100000

python3 ../L1Plotting/turnOn.py --indir JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_CaloParams2023"${number}"_data_reco_json \
 --outdir 2024_03_05_NtuplesV59/"${number}"/NtuplesVnew --reco --target jet --raw --PuppiJet --nEvts 100000 --tag "${suffix}"

# python3 ../L1Plotting/resolutions.py --indir JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_"${dataset_tag}"CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
#  --outdir 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVunc"${suffix}" --reco --target jet --raw --PuppiJet --jetPtcut 30 --nEvts 100000 --no_plot --no_Satu

# python3 ../L1Plotting/resolutions.py --indir JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_"${dataset_tag}"CaloParams2023v04_data_reco_json/GoodNtuples \
#  --outdir 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVold"${suffix}" --reco --target jet --raw --PuppiJet --jetPtcut 30 --nEvts 100000 --no_plot --no_Satu

python3 ../L1Plotting/resolutions.py --indir JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_CaloParams2023"${number}"_data_reco_json \
 --outdir 2024_03_05_NtuplesV59/"${number}"/NtuplesVnew --reco --target jet --raw --PuppiJet --jetPtcut 30 --nEvts 100000 --no_plot --tag "${suffix}" --no_Satu

python3 ../L1Plotting/comparisonPlots.py  --target jet --reco \
 --old 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVold"${suffix}" \
 --unc 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVunc"${suffix}" \
 --thrsFixRate 40 --thrsFixRate 60 --thrsFixRate 80 --thrsFixRate 100 --tag "${suffix}" \
 --indir 2024_03_05_NtuplesV59/"${number}"/NtuplesVnew

# python3 ../L1Plotting/rate.py --indir EphemeralZeroBias__Run2023D-v1__RAW__Testing__GT130XdataRun3Promptv4_"${dataset_tag}"CaloParams2023v04_noL1Calib_data \
#  --outdir 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVunc"${suffix}" --target jet --raw --nEvts 100000 --no_plot --offline

# python3 ../L1Plotting/rate.py --indir EphemeralZeroBias__Run2023D-v1__RAW__Testing__GT130XdataRun3Promptv4_"${dataset_tag}"CaloParams2023v04_data \
#  --outdir 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVold"${suffix}" --target jet --raw --nEvts 100000 --no_plot --offline

python3 ../L1Plotting/rate.py --indir EphemeralZeroBias__Run2023D-v1__RAW__Testing__GT130XdataRun3Promptv4_CaloParams2023"${number}"_data \
 --outdir 2024_03_05_NtuplesV59/"${number}"/NtuplesVnew --target jet --raw --nEvts 100000 --no_plot --offline --tag "${suffix}"

python3 ../L1Plotting/comparisonPlots.py --indir 2024_03_05_NtuplesV59/"${number}"/NtuplesVnew  --target jet --reco \
 --old 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVold"${suffix}" \
 --unc 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVunc"${suffix}" \
 --thrsFixRate 60 --thrsFixRate 70 --thrsFixRate 80 --tag "${suffix}" --offline --doResponse False --doResolution False

