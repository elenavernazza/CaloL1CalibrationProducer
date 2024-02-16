#!/usr/bin/bash

number=$1

############################################################################################################################
############################################################################################################################
############################################################################################################################

# python3 ../L1Plotting/rate.py --indir EphemeralZeroBias__Run2023D-v1__RAW__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data \
#  --outdir 2024_02_15_NtuplesV58/JAX_ECAL/NtuplesVuncL1pt --target ele --raw --nEvts 100000 --no_plot

# python3 ../L1Plotting/rate.py --indir EphemeralZeroBias__Run2023D-v1__RAW__GT130XdataRun3Promptv4_CaloParams2023v04_data \
#  --outdir 2024_02_15_NtuplesV58/JAX_ECAL/NtuplesVoldL1pt --target ele --raw --nEvts 100000 --no_plot

python3 ../L1Plotting/rate.py --indir EphemeralZeroBias__Run2023D-v1__RAW__GT130XdataRun3Promptv4_CaloParams2023"${number}"_data \
 --outdir 2024_02_15_NtuplesV58/"${number}"/NtuplesVnew --target ele --raw --nEvts 100000 --no_plot --tag L1pt

# python3 ../L1Plotting/turnOn.py --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
#  --outdir 2024_02_15_NtuplesV58/JAX_ECAL/NtuplesVuncL1pt --reco --target ele --raw --LooseEle --nEvts 100000

# python3 ../L1Plotting/turnOn.py --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023v04_data_reco_json/GoodNtuples \
#  --outdir 2024_02_15_NtuplesV58/JAX_ECAL/NtuplesVoldL1pt --reco --target ele --raw --LooseEle --nEvts 100000

python3 ../L1Plotting/turnOn.py --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023"${number}"_data_reco_json \
 --outdir 2024_02_15_NtuplesV58/"${number}"/NtuplesVnew --reco --target ele --raw --LooseEle --nEvts 100000 --tag L1pt

# python3 ../L1Plotting/resolutions.py --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
#  --outdir 2024_02_15_NtuplesV58/JAX_ECAL/NtuplesVuncL1pt --reco --target ele --raw --LooseEle --nEvts 100000 --no_plot

# python3 ../L1Plotting/resolutions.py --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023v04_data_reco_json/GoodNtuples \
#  --outdir 2024_02_15_NtuplesV58/JAX_ECAL/NtuplesVoldL1pt --reco --target ele --raw --LooseEle --nEvts 100000 --no_plot

python3 ../L1Plotting/resolutions.py --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023"${number}"_data_reco_json \
 --outdir 2024_02_15_NtuplesV58/"${number}"/NtuplesVnew --reco --target ele --raw --LooseEle --nEvts 100000 --no_plot --tag L1pt

python3 ../L1Plotting/comparisonPlots.py --indir 2024_02_15_NtuplesV58/"${number}"/NtuplesVnew  --target jet --reco \
 --old 2024_02_15_NtuplesV58/JAX_ECAL/NtuplesVoldL1pt \
 --unc 2024_02_15_NtuplesV58/JAX_ECAL/NtuplesVuncL1pt \
 --thrsFixRate 10 --thrsFixRate 12 --thrsFixRate 20 --thrsFixRate 40 --tag L1pt

# python3 ../L1Plotting/rate.py --indir EphemeralZeroBias__Run2023D-v1__RAW__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data \
#  --outdir 2024_02_15_NtuplesV58/JAX_ECAL/NtuplesVuncL1pt --target ele --raw --nEvts 100000 --no_plot --offline

# python3 ../L1Plotting/rate.py --indir EphemeralZeroBias__Run2023D-v1__RAW__GT130XdataRun3Promptv4_CaloParams2023v04_data \
#  --outdir 2024_02_15_NtuplesV58/JAX_ECAL/NtuplesVoldL1pt --target ele --raw --nEvts 100000 --no_plot --offline

python3 ../L1Plotting/rate.py --indir EphemeralZeroBias__Run2023D-v1__RAW__GT130XdataRun3Promptv4_CaloParams2023"${number}"_data \
 --outdir 2024_02_15_NtuplesV58/"${number}"/NtuplesVnew --target ele --raw --nEvts 100000 --no_plot --offline --tag L1pt

python3 ../L1Plotting/comparisonPlots.py --indir 2024_02_15_NtuplesV58/"${number}"/NtuplesVnew  --target ele --reco \
 --old 2024_02_15_NtuplesV58/JAX_HCAL/NtuplesVoldL1pt \
 --unc 2024_02_15_NtuplesV58/JAX_HCAL/NtuplesVuncL1pt \
 --thrsFixRate 10 --thrsFixRate 12 --thrsFixRate 20 --thrsFixRate 40 --tag L1pt --offline --doResponse False --doResolution False
