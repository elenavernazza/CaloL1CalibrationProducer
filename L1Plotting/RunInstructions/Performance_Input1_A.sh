cmsenv 

# python3 rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data \
#  --outdir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/model_HCAL_A/NtuplesVunc_Raw_Puppi_BarrelEndcap_Pt30 --label Jet_data_reco --target jet \
#  --raw --nEvts 100000 --no_plot --er 1.305 

# python3 rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_data \
#  --outdir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/model_HCAL_A/NtuplesVold_Raw_Puppi_BarrelEndcap_Pt30 --label Jet_data_reco --target jet \
#  --raw --nEvts 100000 --no_plot --er 1.305 

# python3 rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v56_A_Input1_data \
#  --outdir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/model_HCAL_A/NtuplesVnew_Raw_Puppi_BarrelEndcap_Pt30 --label Jet_data_reco --target jet \
#  --raw --nEvts 100000 --no_plot --er 1.305 

# python3 turnOn.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
#  --outdir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/model_HCAL_A/NtuplesVunc_Raw_Puppi_BarrelEndcap_Pt30 --label Jet_data_reco --reco --target jet \
#  --raw --PuppiJet --nEvts 100000 --er 1.305 

# python3 turnOn.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_data_reco_json \
#  --outdir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/model_HCAL_A/NtuplesVold_Raw_Puppi_BarrelEndcap_Pt30 --label Jet_data_reco --reco --target jet \
#  --raw --PuppiJet --nEvts 100000 --er 1.305 

# python3 turnOn.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v56_A_Input1_data_reco_json \
#  --outdir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/model_HCAL_A/NtuplesVnew_Raw_Puppi_BarrelEndcap_Pt30 --label Jet_data_reco --reco --target jet \
#  --raw --PuppiJet --nEvts 100000 --er 1.305 

# python3 comparisonPlots.py --indir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/model_HCAL_A/NtuplesVnew_Raw_Puppi_BarrelEndcap_Pt30 --label Jet_data_reco  --target jet --reco \
#  --old 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/model_HCAL_A/NtuplesVold_Raw_Puppi_BarrelEndcap_Pt30 \
#  --unc 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/model_HCAL_A/NtuplesVunc_Raw_Puppi_BarrelEndcap_Pt30 \
#  --do_HoTot --thrsFixRate 40 --thrsFixRate 60 --thrsFixRate 80 --er 1.305 --doResolution False --doResponse False 

python3 resolutions.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
 --outdir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/model_HCAL_A/NtuplesVunc_Raw_Puppi_BarrelEndcap_Pt30 --label Jet_data_reco --reco --target jet --do_HoTot \
 --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot 

python3 resolutions.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_data_reco_json \
 --outdir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/model_HCAL_A/NtuplesVold_Raw_Puppi_BarrelEndcap_Pt30 --label Jet_data_reco --reco --target jet --do_HoTot \
 --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot 

python3 resolutions.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v56_A_Input1_data_reco_json \
 --outdir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/model_HCAL_A/NtuplesVnew_Raw_Puppi_BarrelEndcap_Pt30 --label Jet_data_reco --reco --target jet --do_HoTot \
 --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot 

python3 comparisonPlots.py --indir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/model_HCAL_A/NtuplesVnew_Raw_Puppi_BarrelEndcap_Pt30 --label Jet_data_reco  --target jet --reco \
 --old 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/model_HCAL_A/NtuplesVold_Raw_Puppi_BarrelEndcap_Pt30 \
 --unc 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/model_HCAL_A/NtuplesVunc_Raw_Puppi_BarrelEndcap_Pt30 \
 --do_HoTot --doRate False --doTurnOn False  

