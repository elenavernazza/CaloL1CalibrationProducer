#!/usr/bin/bash

number=$1

############################################################################################################################
############################################################################################################################
############################################################################################################################

# python3 ../L1Plotting/rate.py --indir EphemeralZeroBias__Run2023D-v1__Run369870__RAW__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data \
#  --outdir 2024_02_15_NtuplesV58/JAX_HCAL/NtuplesVuncL1ptNoSatu --target jet --raw --nEvts 100000 --no_plot

# python3 ../L1Plotting/rate.py --indir EphemeralZeroBias__Run2023D-v1__Run369870__RAW__GT130XdataRun3Promptv4_CaloParams2023v04_data \
#  --outdir 2024_02_15_NtuplesV58/JAX_HCAL/NtuplesVoldL1ptNoSatu --target jet --raw --nEvts 100000 --no_plot

python3 ../L1Plotting/rate.py --indir EphemeralZeroBias__Run2023D-v1__Run369870__RAW__GT130XdataRun3Promptv4_CaloParams2023"${number}"_data \
 --outdir 2024_02_15_NtuplesV58/"${number}"/NtuplesVnew --target jet --raw --nEvts 100000 --no_plot --tag L1ptNoSatu

# python3 ../L1Plotting/turnOn.py --indir JetMET__Run2023B-PromptReco-v1__Run367079__AOD__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
#  --outdir 2024_02_15_NtuplesV58/JAX_HCAL/NtuplesVuncL1ptNoSatu --reco --target jet --raw --PuppiJet --nEvts 100000

# python3 ../L1Plotting/turnOn.py --indir JetMET__Run2023B-PromptReco-v1__Run367079__AOD__GT130XdataRun3Promptv4_CaloParams2023v04_data_reco_json/GoodNtuples \
#  --outdir 2024_02_15_NtuplesV58/JAX_HCAL/NtuplesVoldL1ptNoSatu --reco --target jet --raw --PuppiJet --nEvts 100000

# python3 ../L1Plotting/turnOn.py --indir JetMET__Run2023B-PromptReco-v1__Run367079__AOD__GT130XdataRun3Promptv4_CaloParams2023"${number}"_data_reco_json \
#  --outdir 2024_02_15_NtuplesV58/"${number}"/NtuplesVnew --reco --target jet --raw --PuppiJet --nEvts 100000 --tag L1ptNoSatu

# python3 ../L1Plotting/resolutions.py --indir JetMET__Run2023B-PromptReco-v1__Run367079__AOD__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
#  --outdir 2024_02_15_NtuplesV58/JAX_HCAL/NtuplesVuncL1ptNoSatu --reco --target jet --raw --PuppiJet --jetPtcut 30 --nEvts 100000 --no_plot --no_Satu

python3 ../L1Plotting/resolutions.py --indir JetMET__Run2023B-PromptReco-v1__Run367079__AOD__GT130XdataRun3Promptv4_CaloParams2023v04_data_reco_json/GoodNtuples \
 --outdir 2024_02_15_NtuplesV58/JAX_HCAL/NtuplesVoldL1ptNoSatu --reco --target jet --raw --PuppiJet --jetPtcut 30 --nEvts 100000 --no_plot --no_Satu

python3 ../L1Plotting/resolutions.py --indir JetMET__Run2023B-PromptReco-v1__Run367079__AOD__GT130XdataRun3Promptv4_CaloParams2023"${number}"_data_reco_json \
 --outdir 2024_02_15_NtuplesV58/"${number}"/NtuplesVnew --reco --target jet --raw --PuppiJet --jetPtcut 30 --nEvts 100000 --no_plot --tag L1ptNoSatu --no_Satu

python3 ../L1Plotting/comparisonPlots.py  --target jet --reco \
 --old 2024_02_15_NtuplesV58/JAX_HCAL/NtuplesVoldL1ptNoSatu \
 --unc 2024_02_15_NtuplesV58/JAX_HCAL/NtuplesVuncL1ptNoSatu \
 --thrsFixRate 40 --thrsFixRate 60 --thrsFixRate 80 --thrsFixRate 100 --tag L1ptNoSatu \
 --indir 2024_02_15_NtuplesV58/"${number}"/NtuplesVnew

# python3 ../L1Plotting/rate.py --indir EphemeralZeroBias__Run2023D-v1__Run369870__RAW__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data \
#  --outdir 2024_02_15_NtuplesV58/JAX_HCAL/NtuplesVuncL1ptNoSatu --target jet --raw --nEvts 100000 --no_plot --offline

# python3 ../L1Plotting/rate.py --indir EphemeralZeroBias__Run2023D-v1__Run369870__RAW__GT130XdataRun3Promptv4_CaloParams2023v04_data \
#  --outdir 2024_02_15_NtuplesV58/JAX_HCAL/NtuplesVoldL1ptNoSatu --target jet --raw --nEvts 100000 --no_plot --offline

python3 ../L1Plotting/rate.py --indir EphemeralZeroBias__Run2023D-v1__Run369870__RAW__GT130XdataRun3Promptv4_CaloParams2023"${number}"_data \
 --outdir 2024_02_15_NtuplesV58/"${number}"/NtuplesVnew --target jet --raw --nEvts 100000 --no_plot --offline --tag L1ptNoSatu

python3 ../L1Plotting/comparisonPlots.py --indir 2024_02_15_NtuplesV58/"${number}"/NtuplesVnew  --target jet --reco \
 --old 2024_02_15_NtuplesV58/JAX_HCAL/NtuplesVoldL1ptNoSatu \
 --unc 2024_02_15_NtuplesV58/JAX_HCAL/NtuplesVuncL1ptNoSatu \
 --thrsFixRate 60 --thrsFixRate 70 --thrsFixRate 80 --tag L1ptNoSatu --offline --doResponse False --doResolution False

