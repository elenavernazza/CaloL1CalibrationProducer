loadGPUtf 

python3 NNModel_RegAndRate_AddEt.py --indir 2023_12_13_NtuplesV56/Input3/JetMET_PuppiJet_BarrelEndcap_Pt60_HoTot70 \
 --v HCAL --tag DataReco --addtag _B --epochs 20 \
 --MaxLR 1E-3 --batch_size 256 --ThrRate 40

python3 CalibrationFactor.py --indir 2023_12_13_NtuplesV56/Input3/JetMET_PuppiJet_BarrelEndcap_Pt60_HoTot70 --v HCAL --tag DataReco --reg HCAL --energystep 2 --addtag _B

python3 CalibrationFactor.py --indir 2023_12_13_NtuplesV56/Input3/JetMET_PuppiJet_BarrelEndcap_Pt60_HoTot70 --v HCAL --tag DataReco --reg HF --energystep 2 --addtag _B

python3 ProduceCaloParams.py --name caloParams_2023_v56_B_Input3_cfi \
 --base caloParams_2023_v0_2_noL1Calib_cfi.py \
 --ECAL /data_CMS/cms/motta/CaloL1calibraton/2023_03_06_NtuplesV33/ECALtrainingDataReco_normalOrder/data/ScaleFactors_ECAL_energystep2iEt.csv \
 --HCAL /data_CMS/cms/motta/CaloL1calibraton/2023_12_13_NtuplesV56/Input3/JetMET_PuppiJet_BarrelEndcap_Pt60_HoTot70/HCALtrainingDataReco/model_HCAL_B/SFs_2iEt/ScaleFactors_HCAL_energystep2iEt.csv \
 --HF   /data_CMS/cms/motta/CaloL1calibraton/2023_12_13_NtuplesV56/Input3/JetMET_PuppiJet_BarrelEndcap_Pt60_HoTot70/HCALtrainingDataReco/model_HCAL_B/SFs_2iEt/ScaleFactors_HF_energystep2iEt.csv 

cd ../L1NtupleLauncher 

python3 submitOnTier3.py --inFileList JetMET__Run2022G-PromptReco-v1__Run362617__AOD \
 --outTag GT130XdataRun3Promptv3_CaloParams2023v56_B_Input3_data_reco_json \
 --nJobs 31 --queue short --maxEvts 5000 --inJson Cert_Collisions2022_355100_362760_Golden \
 --globalTag 130X_dataRun3_Prompt_v3 --data --recoFromAOD \
 --caloParams caloParams_2023_v56_B_Input3_cfi 

python3 submitOnTier3.py --inFileList EphemeralZeroBias0__Run2022G-v1__Run362617__RAW \
 --outTag GT130XdataRun3Promptv3_CaloParams2023v56_B_Input3_data \
 --nJobs 31 --queue short --maxEvts 5000 \
 --globalTag 130X_dataRun3_Prompt_v3 --data \
 --caloParams caloParams_2023_v56_B_Input3_cfi 

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

