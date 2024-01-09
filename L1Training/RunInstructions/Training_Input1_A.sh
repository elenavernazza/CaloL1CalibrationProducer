loadGPUtf 

python3 NNModel_RegAndRate.py --indir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 \
 --v HCAL --tag DataReco --addtag _A --epochs 20 \
 --MaxLR 1E-3 --batch_size 256 --ThrRate 40

python3 CalibrationFactor.py --indir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --reg HCAL --energystep 2 --addtag _A

python3 CalibrationFactor.py --indir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --reg HF --energystep 2 --addtag _A

python3 ProduceCaloParams.py --name caloParams_2023_v56_A_Input1_cfi \
 --base caloParams_2023_v0_2_noL1Calib_cfi.py \
 --ECAL /data_CMS/cms/motta/CaloL1calibraton/2023_03_06_NtuplesV33/ECALtrainingDataReco_normalOrder/data/ScaleFactors_ECAL_energystep2iEt.csv \
 --HCAL /data_CMS/cms/motta/CaloL1calibraton/2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/model_HCAL_A/SFs_2iEt/ScaleFactors_HCAL_energystep2iEt.csv \
 --HF   /data_CMS/cms/motta/CaloL1calibraton/2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/model_HCAL_A/SFs_2iEt/ScaleFactors_HF_energystep2iEt.csv 

cd ../L1NtupleLauncher 

python3 submitOnTier3.py --inFileList JetMET__Run2022G-PromptReco-v1__Run362617__AOD \
 --outTag GT130XdataRun3Promptv3_CaloParams2023v56_A_Input1_data_reco_json \
 --nJobs 31 --queue short --maxEvts 5000 --inJson Cert_Collisions2022_355100_362760_Golden \
 --globalTag 130X_dataRun3_Prompt_v3 --data --recoFromAOD \
 --caloParams caloParams_2023_v56_A_Input1_cfi 

python3 submitOnTier3.py --inFileList EphemeralZeroBias0__Run2022G-v1__Run362617__RAW \
 --outTag GT130XdataRun3Promptv3_CaloParams2023v56_A_Input1_data \
 --nJobs 31 --queue short --maxEvts 5000 \
 --globalTag 130X_dataRun3_Prompt_v3 --data \
 --caloParams caloParams_2023_v56_A_Input1_cfi 

python3 submitOnTier3.py --inFileList JetMET__Run2022G-PromptReco-v1__Run362617__AOD \
 --outTag GT130XdataRun3Promptv3_CaloParams2023v02_data_reco_json \
 --nJobs 31 --queue short --maxEvts 5000 --inJson Cert_Collisions2022_355100_362760_Golden \
 --globalTag 130X_dataRun3_Prompt_v3 --data --recoFromAOD \
 --caloParams caloParams_2023_v0_2_cfi 

python3 submitOnTier3.py --inFileList EphemeralZeroBias0__Run2022G-v1__Run362617__RAW \
 --outTag GT130XdataRun3Promptv3_CaloParams2023v02_data \
 --nJobs 31 --queue short --maxEvts 5000 \
 --globalTag 130X_dataRun3_Prompt_v3 --data \
 --caloParams caloParams_2023_v0_2_cfi 

cd - 

