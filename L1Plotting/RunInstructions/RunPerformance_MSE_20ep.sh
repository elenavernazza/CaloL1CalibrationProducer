# OldCalib
python3 resolutions.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_data_reco_json/GoodNtuples \
 --outdir 2023_12_05_NtuplesV54/NtuplesVcur_Raw_Puppi_BarrelEndcap_Pt30 --label Muon_data_reco --reco --nEvts 100000 --target jet --raw --PuppiJet --etacut 3 --jetPtcut 30 --do_HoTot
python3 turnOn.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_data_reco_json/GoodNtuples \
 --outdir 2023_12_05_NtuplesV54/NtuplesVcur_Raw_Puppi_BarrelEndcap_Pt30 --label Muon_data_reco --reco --nEvts 100000 --target jet --raw --PuppiJet --jetPtcut 15 --er 1.305
python3 rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_data \
 --outdir 2023_12_05_NtuplesV54/NtuplesVcur_Raw_Puppi_BarrelEndcap_Pt30 --label Muon_data_reco --nEvts 100000 --target jet --raw --er 1.305

python3 resolutions.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v51A_MSE_20ep_data_reco_json \
 --outdir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/Performance_CaloParams2023v51A_MSE_2ep --label Muon_data_reco --reco --nEvts 100000 --target jet --raw --PuppiJet --etacut 3 --jetPtcut 30 --do_HoTot
python3 turnOn.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v51A_MSE_20ep_data_reco_json \
 --outdir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/Performance_CaloParams2023v51A_MSE_2ep --label Muon_data_reco --reco --nEvts 100000 --target jet --raw --PuppiJet --jetPtcut 15 --er 1.305
python3 rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v51A_MSE_20ep_newCalib_data \
 --outdir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/Performance_CaloParams2023v51A_MSE_2ep --label Muon_data_reco --nEvts 100000 --target jet --raw --er 1.305

python3 comparisonPlots.py --indir 2023_12_05_NtuplesV54/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/Performance_CaloParams2023v51A_MSE_2ep --label Muon_data_reco  --target jet --reco \
 --thrsFixRate 40 --thrsFixRate 60 --thrsFixRate 80 \
 --old 2023_12_05_NtuplesV54/NtuplesVcur_Raw_Puppi_BarrelEndcap_Pt30 --unc 2023_12_05_NtuplesV54/NtuplesVunc_Raw_Puppi_BarrelEndcap_Pt30 --do_HoTot --er 1.305
