##################################################################################################################################################################
# TRAINING

# reduce learning rate (at epoch 14 it is lie at epoch 2 for LR=1E-3)
python3 NNModel_RegAndRate.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 \
    --v HCAL --tag DataReco --MaxLR 1E-4 --addtag _Test1 --batch_size 256 --epochs 20 --ThrRate 40 --TargetRate 0.33569892616499036
python3 ProgressionSFs.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --addtag _Test1 --epochs 20
python3 ProgressionPerformance.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --addtag _Test1 --epochs 20 \
    --set Train --eventLim 20000 (--FromDF)
python3 ProgressionPerformance.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --addtag _Test1 --epochs 20 \
    --set Test --eventLim 20000 (--FromDF)
python3 PrepareReEmulation.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 \
    --v HCAL --tag DataReco --addtag _Test1 --applyECAL False --modelRate

# reduce network size
python3 NNModel_RegAndRate_2.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 \
    --v HCAL --tag DataReco --MaxLR 1E-4 --addtag _Test2 --batch_size 256 --epochs 20 --ThrRate 40 --TargetRate 0.33569892616499036
python3 ProgressionSFs.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --addtag _Test2 --epochs 20
python3 ProgressionPerformance.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --addtag _Test2 --epochs 20 \
    --set Train --eventLim 20000 (--FromDF)
python3 ProgressionPerformance.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --addtag _Test2 --epochs 20 \
    --set Test --eventLim 20000 (--FromDF)

# (mean_uncalib=0.767)*target
python3 NNModel_RegAndRate_3.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 \
    --v HCAL --tag DataReco --MaxLR 1E-4 --addtag _Test3 --batch_size 256 --epochs 20 --ThrRate 40 --TargetRate 0.33569892616499036
python3 ProgressionSFs.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --addtag _Test3 --epochs 20
python3 ProgressionPerformance.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --addtag _Test3 --epochs 20 \
    --set Train --eventLim 20000 (--FromDF)
python3 ProgressionPerformance.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --addtag _Test3 --epochs 20 \
    --set Test --eventLim 20000 (--FromDF)

# constrain SFs to always be < 2
python3 NNModel_RegAndRate_4.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 \
    --v HCAL --tag DataReco --MaxLR 1E-4 --addtag _Test4 --batch_size 256 --epochs 20 --ThrRate 40 --TargetRate 0.33569892616499036
python3 ProgressionSFs.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --addtag _Test4 --epochs 20
python3 ProgressionPerformance.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --addtag _Test4 --epochs 20 \
    --set Train --eventLim 20000 (--FromDF)
python3 ProgressionPerformance.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --addtag _Test4 --epochs 20 \
    --set Test --eventLim 20000 (--FromDF)

##################################################################################################################################################################
# RE-EMULATION

python3 PrepareReEmulation.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 \
    --v HCAL --tag DataReco --addtag _Test2 --applyECAL False --modelRate

python3 ProduceCaloParams.py --name caloParams_2023_v51_Test3_newCalib_cfi \
    --base caloParams_2023_v0_2_noL1Calib_cfi.py \
    --HCAL /data_CMS/cms/motta/CaloL1calibraton/2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/data_Test3/ScaleFactors_HCAL_energystep2iEt.csv

cmsenv
voms
python submitOnTier3.py --inFileList JetMET__Run2022G-PromptReco-v1__Run362617__AOD \
    --outTag GT130XdataRun3Promptv3_CaloParams2023v51Test3_data_reco_json \
    --nJobs 31 \
    --queue short \
    --maxEvts 5000 \
    --inJson Cert_Collisions2022_355100_362760_Golden \
    --caloParams caloParams_2023_v51_Test3_newCalib_cfi \
    --globalTag 130X_dataRun3_Prompt_v3 \
    --data \
    --recoFromAOD
python submitOnTier3.py --inFileList EphemeralZeroBias0__Run2022G-v1__Run362617__RAW \
    --outTag GT130XdataRun3Promptv3_CaloParams2023v51Test3_data \
    --nJobs 31 \
    --queue short \
    --maxEvts 5000 \
    --caloParams caloParams_2023_v51_Test3_newCalib_cfi \
    --globalTag 130X_dataRun3_Prompt_v3 \
    --data

python3 resolutions.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v51Test3_data_reco_json \
 --outdir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95_CaloParams2023v51Test3 --label Muon_data_reco --reco --nEvts 100000 --target jet --raw --PuppiJet --etacut 3 --jetPtcut 30 --do_HoTot
python3 turnOn.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v51Test3_data_reco_json \
 --outdir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95_CaloParams2023v51Test3 --label Muon_data_reco --reco --nEvts 100000 --target jet --raw --PuppiJet --jetPtcut 15 --er 1.305
python3 rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v51Test3_data \
 --outdir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95_CaloParams2023v51Test3 --label Muon_data_reco --nEvts 100000 --target jet --raw --er 1.305
python3 comparisonPlots.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95_CaloParams2023v51Test3 --label Muon_data_reco  --target jet --reco \
 --thrsFixRate 35 --thrsFixRate 40 --thrsFixRate 45 --thrsFixRate 50 --thrsFixRate 60 --thrsFixRate 80 \
 --old 2023_12_05_NtuplesV54/NtuplesVcur_Raw_Puppi_BarrelEndcap_Pt30 --unc 2023_12_05_NtuplesV54/NtuplesVunc_Raw_Puppi_BarrelEndcap_Pt30 --do_HoTot --er 1.305
