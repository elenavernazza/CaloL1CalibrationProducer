cmsenv 

python3 RDF_Resolution.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
 --outdir 2023_12_13_NtuplesV56/Input4/JetMET_PuppiJet_BarrelEndcap_PtRaw60_HoTot70/HCALtrainingDataReco/model_HCAL_A/NtuplesVunc_Raw_Puppi_BarrelEndcap_Pt30 --label Muon_data_reco --reco --target jet --do_HoTot \
 --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot 

python3 RDF_Resolution.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
 --outdir 2023_12_13_NtuplesV56/Input4/JetMET_PuppiJet_BarrelEndcap_PtRaw60_HoTot70/HCALtrainingDataReco/model_HCAL_A/NtuplesVold_Raw_Puppi_BarrelEndcap_Pt30 --label Muon_data_reco --reco --target jet --do_HoTot \
 --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot --HCALcalib --ECALcalib --caloParam caloParams_2023_v0_2_cfi.py 

python3 RDF_Resolution.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
 --outdir 2023_12_13_NtuplesV56/Input4/JetMET_PuppiJet_BarrelEndcap_PtRaw60_HoTot70/HCALtrainingDataReco/model_HCAL_A/NtuplesVnew_Raw_Puppi_BarrelEndcap_Pt30 --label Muon_data_reco --reco --target jet --do_HoTot \
 --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot --HCALcalib --ECALcalib --caloParam caloParams_2023_v56_A_Input4_cfi.py 

python3 comparisonPlots.py --indir 2023_12_13_NtuplesV56/Input4/JetMET_PuppiJet_BarrelEndcap_PtRaw60_HoTot70/HCALtrainingDataReco/model_HCAL_A/NtuplesVnew_Raw_Puppi_BarrelEndcap_Pt30 --label Muon_data_reco  --target jet --reco \
 --old 2023_12_13_NtuplesV56/Input4/JetMET_PuppiJet_BarrelEndcap_PtRaw60_HoTot70/HCALtrainingDataReco/model_HCAL_A/NtuplesVold_Raw_Puppi_BarrelEndcap_Pt30 \
 --unc 2023_12_13_NtuplesV56/Input4/JetMET_PuppiJet_BarrelEndcap_PtRaw60_HoTot70/HCALtrainingDataReco/model_HCAL_A/NtuplesVunc_Raw_Puppi_BarrelEndcap_Pt30 \
 --do_HoTot --doTurnOn False --doRate False 

