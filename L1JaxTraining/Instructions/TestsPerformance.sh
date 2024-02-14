#!/usr/bin/bash

# Check if the number of arguments provided is correct
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <number>"
    exit 1
fi

version="$1"

# # # python3 rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data \
# # #  --outdir /data_CMS/cms/motta/CaloL1calibraton/2024_02_01_NtuplesV57/JAX/NtuplesVunc --target jet --raw --nEvts 100000 --no_plot --er 1.305 

# # # python3 rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_data \
# # #  --outdir /data_CMS/cms/motta/CaloL1calibraton/2024_02_01_NtuplesV57/JAX/NtuplesVold --target jet --raw --nEvts 100000 --no_plot --er 1.305 

# python3 rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023JAX"${version}"_data \
#  --outdir /data_CMS/cms/motta/CaloL1calibraton/2024_02_01_NtuplesV57/JAX"${version}"/NtuplesVnew --target jet --raw --nEvts 100000 --no_plot 

# # python3 RDF_Resolution.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
# #  --no_CD --outdir /data_CMS/cms/motta/CaloL1calibraton/2024_02_01_NtuplesV57/JAX/NtuplesVunc \
# #  --reco --target jet --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --do_HoTot --no_plot

# # python3 RDF_TurnOn.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
# #  --no_CD --outdir /data_CMS/cms/motta/CaloL1calibraton/2024_02_01_NtuplesV57/JAX/NtuplesVunc \
# #  --reco --target jet --raw --PuppiJet --nEvts 100000 --no_plot

# # python3 RDF_Resolution.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_data_reco_json \
# #  --no_CD --outdir /data_CMS/cms/motta/CaloL1calibraton/2024_02_01_NtuplesV57/JAX/NtuplesVold \
# #  --reco --target jet --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --do_HoTot --no_plot

# # python3 RDF_TurnOn.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_data_reco_json \
# #  --no_CD --outdir /data_CMS/cms/motta/CaloL1calibraton/2024_02_01_NtuplesV57/JAX/NtuplesVold \
# #  --reco --target jet --raw --PuppiJet --nEvts 100000 --no_plot

# python3 RDF_Resolution.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023JAX"${version}"_data_reco_json \
#  --no_CD --outdir /data_CMS/cms/motta/CaloL1calibraton/2024_02_01_NtuplesV57/JAX"${version}"/NtuplesVnew \
#  --reco --target jet --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --do_HoTot --no_plot

# python3 RDF_TurnOn.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023JAX"${version}"_data_reco_json \
#  --no_CD --outdir /data_CMS/cms/motta/CaloL1calibraton/2024_02_01_NtuplesV57/JAX"${version}"/NtuplesVnew \
#  --reco --target jet --raw --PuppiJet --nEvts 100000 --no_plot

# python3 comparisonPlots.py --indir /data_CMS/cms/motta/CaloL1calibraton/2024_02_01_NtuplesV57/JAX"${version}"/NtuplesVnew  --target jet --reco \
#  --old /data_CMS/cms/motta/CaloL1calibraton/2024_02_01_NtuplesV57/JAX/NtuplesVold \
#  --unc /data_CMS/cms/motta/CaloL1calibraton/2024_02_01_NtuplesV57/JAX/NtuplesVunc \
#  --thrsFixRate 40 --thrsFixRate 60 --thrsFixRate 80

############################################################################################################################
############################################################################################################################
############################################################################################################################

# python3 ../L1Plotting/rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data \
#  --outdir 2024_02_01_NtuplesV57/JAX/NtuplesVuncL1pt --target jet --raw --nEvts 100000 --no_plot

# python3 ../L1Plotting/rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_data \
#  --outdir 2024_02_01_NtuplesV57/JAX/NtuplesVoldL1pt --target jet --raw --nEvts 100000 --no_plot

python3 ../L1Plotting/rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023JAX"${version}"_data \
 --outdir 2024_02_01_NtuplesV57/JAX"${version}"/NtuplesVnew --target jet --raw --nEvts 100000 --no_plot --tag L1pt

# python3 ../L1Plotting/turnOn.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
#  --outdir 2024_02_01_NtuplesV57/JAX/NtuplesVuncL1pt --reco --target jet --raw --PuppiJet --nEvts 100000

# python3 ../L1Plotting/turnOn.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_data_reco_json \
#  --outdir 2024_02_01_NtuplesV57/JAX/NtuplesVoldL1pt --reco --target jet --raw --PuppiJet --nEvts 100000

python3 ../L1Plotting/turnOn.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023JAX"${version}"_data_reco_json \
 --outdir 2024_02_01_NtuplesV57/JAX"${version}"/NtuplesVnew --reco --target jet --raw --PuppiJet --nEvts 100000 --tag L1pt

# python3 ../L1Plotting/resolutions.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
#  --outdir 2024_02_01_NtuplesV57/JAX/NtuplesVuncL1pt --reco --target jet --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot

# python3 ../L1Plotting/resolutions.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_data_reco_json \
#  --outdir 2024_02_01_NtuplesV57/JAX/NtuplesVoldL1pt --reco --target jet --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot

python3 ../L1Plotting/resolutions.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023JAX"${version}"_data_reco_json \
 --outdir 2024_02_01_NtuplesV57/JAX"${version}"/NtuplesVnew --reco --target jet --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot --tag L1pt

python3 ../L1Plotting/comparisonPlots.py --indir 2024_02_01_NtuplesV57/JAX"${version}"/NtuplesVnew  --target jet --reco \
 --old 2024_02_01_NtuplesV57/JAX/NtuplesVoldL1pt \
 --unc 2024_02_01_NtuplesV57/JAX/NtuplesVuncL1pt \
 --thrsFixRate 40 --thrsFixRate 60 --thrsFixRate 80 --tag L1pt

# python3 ../L1Plotting/rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data \
#  --outdir 2024_02_01_NtuplesV57/JAX/NtuplesVuncL1pt --target jet --raw --nEvts 100000 --no_plot --offline

# python3 ../L1Plotting/rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_data \
#  --outdir 2024_02_01_NtuplesV57/JAX/NtuplesVoldL1pt --target jet --raw --nEvts 100000 --no_plot --offline

python3 ../L1Plotting/rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023JAX"${version}"_data \
 --outdir 2024_02_01_NtuplesV57/JAX"${version}"/NtuplesVnew --target jet --raw --nEvts 100000 --no_plot --tag L1pt --offline

python3 ../L1Plotting/comparisonPlots.py --indir 2024_02_01_NtuplesV57/JAX"${version}"/NtuplesVnew  --target jet --reco \
 --old 2024_02_01_NtuplesV57/JAX/NtuplesVoldL1pt \
 --unc 2024_02_01_NtuplesV57/JAX/NtuplesVuncL1pt \
 --thrsFixRate 60 --thrsFixRate 70 --thrsFixRate 80 --tag L1pt --offline --doResponse False --doResolution False