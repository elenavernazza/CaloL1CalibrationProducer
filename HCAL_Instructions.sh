Instructions for the training of HCAL and HF (V52)

cmsrel CMSSW_13_1_0_pre4
cd CMSSW_13_1_0_pre4/src
cmsenv
git cms-init
git remote add cms-l1t-offline git@github.com:cms-l1t-offline/cmssw.git
git fetch cms-l1t-offline l1t-integration-CMSSW_13_1_0_pre4
git cms-merge-topic -u cms-l1t-offline:l1t-integration-v156
git clone https://github.com/cms-l1t-offline/L1Trigger-L1TCalorimeter.git L1Trigger/L1TCalorimeter/data
git cms-checkdeps -A -a
scram b -j 8
git clone git@github.com:elenavernazza/CaloL1CalibrationProducer.git
git checkout -b CleanUp

1) Produce input jets:

- Re-emulate data (JetMET) with the current Global Tag

'''
python submitOnTier3.py --inFileList JetMET__Run2022G-PromptReco-v1__AOD \
    --outTag GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json \
    --inJson Cert_Collisions2022_355100_362760_Golden \
    --caloParams caloParams_2023_v0_2_noL1Calib_cfi \
    --globalTag 130X_dataRun3_Prompt_v3 \
    --nJobs 5603 --queue short --maxEvts -1 --data --recoFromAOD
'''

- Re-emulate data (ZB) with the current Global Tag

'''
python submitOnTier3.py --inFileList EphemeralZeroBias*__Run2022G-v1__RAW \
    --outTag GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data \
    --caloParams caloParams_2023_v0_2_noL1Calib_cfi \
    --globalTag 130X_dataRun3_Prompt_v3 \
    --nJobs 946 --queue short --maxEvts -1 --data
'''

- Plot the jets and check that the CD energy distribution is the same as the RawEt energy distribution

'''
python3 resolutions.py --indir JetMET__Run2022G-PromptReco-v1__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
 --outdir 2023_12_13_NtuplesV56/Input1/TestInput_JetMET2022G --label Muon_data_reco --reco --nEvts 100000 --target jet \
 --raw --PuppiJet --jetPtcut 30 --do_HoTot --tag _PuppiJet_100K_Pt30_Raw
'''

2) Read jets and produce inputs:

- Extract CD and target jet energy from the ntuples

################################################################
# Input 1 :     jetPt > 30      HoTot > 95%     0.3 < Resp < 3
################################################################
''' # DONE
python3 batchSubmitOnTier3.py --indir /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/JetMET__Run2022G-PromptReco-v1__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
    --outdir /data_CMS/cms/motta/CaloL1calibraton/2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 \
    --target reco --type jet --chunk_size 5000 \
    --queue short \
    --hcalcut 0.95 --lJetPtCut 30 --PuppiJet --matching --etacut 28
'''

################################################################
# Input 2 :     jetPt > 30      HoTot > 70%     0.3 < Resp < 3
################################################################
''' # DONE
python3 batchSubmitOnTier3.py --indir /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/JetMET__Run2022G-PromptReco-v1__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
    --outdir /data_CMS/cms/motta/CaloL1calibraton/2023_12_13_NtuplesV56/Input2/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot70 \
    --target reco --type jet --chunk_size 5000 \
    --queue short \
    --hcalcut 0.70 --lJetPtCut 30 --PuppiJet --matching --etacut 28
'''

################################################################
# Input 3 :     jetPt > 60      HoTot > 70%     0.3 < Resp < 3
################################################################
''' # DONE
python3 batchSubmitOnTier3.py --indir /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/JetMET__Run2022G-PromptReco-v1__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
    --outdir /data_CMS/cms/motta/CaloL1calibraton/2023_12_13_NtuplesV56/Input3/JetMET_PuppiJet_BarrelEndcap_Pt60_HoTot70 \
    --target reco --type jet --chunk_size 5000 \
    --queue short \
    --hcalcut 0.70 --lJetPtCut 60 --PuppiJet --matching --etacut 28
'''

################################################################################
# Input 4 :     jetPt > 60      rawPt > 60      HoTot > 70%     0.3 < Resp < 3
################################################################################
''' # DONE
python3 batchSubmitOnTier3.py --indir /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/JetMET__Run2022G-PromptReco-v1__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
    --outdir /data_CMS/cms/motta/CaloL1calibraton/2023_12_13_NtuplesV56/Input4/JetMET_PuppiJet_BarrelEndcap_PtRaw60_HoTot70 \
    --target reco --type jet --chunk_size 5000 \
    --queue short \
    --hcalcut 0.70 --lJetPtCut 60 --lRawPtCut 60 --PuppiJet --matching --etacut 28
''' 

- Extract sample for the jet rate proxy

''' # DONE
python3 batchSubmitOnTier3.py \
    --indir /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/EphemeralZeroBias0__Run2022G-v1__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data \
    --outdir /data_CMS/cms/motta/CaloL1calibraton/2023_12_13_NtuplesV56/EphemeralZeroBias_BarrelEndcap_Pt30To1000 \
    --target emu --type jet --chunk_size 5000 \
    --queue short \
    --lJetPtCut 30 --uJetPtCut 1000 --etacut 28
python3 batchSubmitOnTier3.py \
    --indir /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/EphemeralZeroBias1__Run2022G-v1__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data \
    --outdir /data_CMS/cms/motta/CaloL1calibraton/2023_12_13_NtuplesV56/EphemeralZeroBias_BarrelEndcap_Pt30To1000 \
    --target emu --type jet --chunk_size 5000 \
    --queue short \
    --lJetPtCut 30 --uJetPtCut 1000 --etacut 28
python3 batchSubmitOnTier3.py \
    --indir /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/EphemeralZeroBias2__Run2022G-v1__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data \
    --outdir /data_CMS/cms/motta/CaloL1calibraton/2023_12_13_NtuplesV56/EphemeralZeroBias_BarrelEndcap_Pt30To1000 \
    --target emu --type jet --chunk_size 5000 \
    --queue short \
    --lJetPtCut 30 --uJetPtCut 1000 --etacut 28
python3 batchSubmitOnTier3.py \
    --indir /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/EphemeralZeroBias3__Run2022G-v1__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data \
    --outdir /data_CMS/cms/motta/CaloL1calibraton/2023_12_13_NtuplesV56/EphemeralZeroBias_BarrelEndcap_Pt30To1000 \
    --target emu --type jet --chunk_size 5000 \
    --queue short \
    --lJetPtCut 30 --uJetPtCut 1000 --etacut 28
'''

- Merge CD into tensorflow and save the input size

################################################################
# Input 1 :     jetPt > 30      HoTot > 95%     0.3 < Resp < 3
################################################################
''' (Training: 52946, Testing: 13241)
python3 batchMerger.py --indir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 \
    --batchdir GoodNtuples --v HCAL --odir DataReco --filesPerRecord 200 --selectResp --fix_stats 100000 \
    --ratedir /data_CMS/cms/motta/CaloL1calibraton/2023_12_13_NtuplesV56/EphemeralZeroBias_BarrelEndcap_Pt30To1000/EphemeralZeroBias*__Run2022G-v1__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data
'''

################################################################
# Input 2 :     jetPt > 30      HoTot > 70%     0.3 < Resp < 3
################################################################
''' (Training: 79999, Testing: 20001)
python3 batchMerger.py --indir 2023_12_13_NtuplesV56/Input2/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot70 \
    --batchdir GoodNtuples --v HCAL --odir DataReco --filesPerRecord 50 --selectResp --fix_stats 100000 \
    --ratedir /data_CMS/cms/motta/CaloL1calibraton/2023_12_13_NtuplesV56/EphemeralZeroBias_BarrelEndcap_Pt30To1000/EphemeralZeroBias*__Run2022G-v1__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data
'''

################################################################
# Input 3 :     jetPt > 60      HoTot > 70%     0.3 < Resp < 3
################################################################
''' (Training: 79999, Testing: 20001)
python3 batchMerger.py --indir 2023_12_13_NtuplesV56/Input3/JetMET_PuppiJet_BarrelEndcap_Pt60_HoTot70 \
    --batchdir GoodNtuples --v HCAL --odir DataReco --filesPerRecord 50 --selectResp --fix_stats 100000 \
    --ratedir /data_CMS/cms/motta/CaloL1calibraton/2023_12_13_NtuplesV56/EphemeralZeroBias_BarrelEndcap_Pt30To1000/EphemeralZeroBias*__Run2022G-v1__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data
'''

################################################################################
# Input 4 :     jetPt > 60      rawPt > 60      HoTot > 70%     0.3 < Resp < 3
################################################################################
''' (Training: 79999, Testing: 20001)
python3 batchMerger.py --indir 2023_12_13_NtuplesV56/Input4/JetMET_PuppiJet_BarrelEndcap_PtRaw60_HoTot70 \
    --batchdir GoodNtuples --v HCAL --odir DataReco --filesPerRecord 50 --selectResp --fix_stats 100000 \
    --ratedir /data_CMS/cms/motta/CaloL1calibraton/2023_12_13_NtuplesV56/EphemeralZeroBias_BarrelEndcap_Pt30To1000/EphemeralZeroBias*__Run2022G-v1__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data
'''

3) Training:

'''
cd L1Training # we can add the target rate proxy inside the training
python3 TargetRateProxy.py --indir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco
python3 TargetRateProxy.py --indir 2023_12_13_NtuplesV56/Input2/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot70 --v HCAL --tag DataReco
python3 TargetRateProxy.py --indir 2023_12_13_NtuplesV56/Input3/JetMET_PuppiJet_BarrelEndcap_Pt60_HoTot70 --v HCAL --tag DataReco
python3 TargetRateProxy.py --indir 2023_12_13_NtuplesV56/Input4/JetMET_PuppiJet_BarrelEndcap_PtRaw60_HoTot70 --v HCAL --tag DataReco

python3 RunTraining.py --addtag _A --indir 1
source RunInstructions/Training_Input1_A.sh

python3 RunTraining.py --addtag _B --indir 2,3,4 
source RunInstructions/Training_Input2_B.sh
source RunInstructions/Training_Input3_B.sh
source RunInstructions/Training_Input4_B.sh
'''

4) Performance:

'''
cd L1Plotting
python3 RunPerformance.py --addtag _A --indir 1
source RunInstructions/Performance_Input1_A.sh
'''


#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################

- Plot the inputs and check that the built CD energy distribution corresponds to the previous one # [FIXME] Make everything faster with npz instead of dataframes

''' 
python3 PlotResponseTF.py --indir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 \
    --v HCAL --tag DataReco --PlotRate
python3 PlotResponseTF.py --indir 2023_12_13_NtuplesV56/Input2/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot70 \
    --v HCAL --tag DataReco --PlotRate
python3 PlotResponseTF.py --indir 2023_12_13_NtuplesV56/Input3/JetMET_PuppiJet_BarrelEndcap_Pt60_HoTot70 \
    --v HCAL --tag DataReco --PlotRate
python3 PlotResponseTF.py --indir 2023_12_13_NtuplesV56/Input4/JetMET_PuppiJet_BarrelEndcap_PtRaw60_HoTot70 \
    --v HCAL --tag DataReco --PlotRate
'''

3) Training:

- Compute target rate

'''
python3 TargetRateProxy.py --indir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco
python3 TargetRateProxy.py --indir 2023_12_13_NtuplesV56/Input2/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot70 --v HCAL --tag DataReco
python3 TargetRateProxy.py --indir 2023_12_13_NtuplesV56/Input3/JetMET_PuppiJet_BarrelEndcap_Pt60_HoTot70 --v HCAL --tag DataReco
python3 TargetRateProxy.py --indir 2023_12_13_NtuplesV56/Input4/JetMET_PuppiJet_BarrelEndcap_PtRaw60_HoTot70 --v HCAL --tag DataReco
'''

- Train the model with rate proxy

'''
python3 NNModel_RegAndRate.py --indir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 \
    --v HCAL --tag DataReco --MaxLR 1E-3 --batch_size 256 --epochs 20 --ThrRate 40 --addtag Test0
python3 ProgressionSFs.py --indir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --addtag Test0 --epochs 20
python3 ProgressionPerformance.py --indir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --addtag Test0 --epochs 20 \
    --set Test --eventLim 20000 --filesLim 1

python3 NNModel_RegAndRate_AddEt.py --indir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 \
    --v HCAL --tag DataReco --MaxLR 1E-3 --batch_size 256 --epochs 20 --ThrRate 40 --addtag Test1
python3 ProgressionSFs.py --indir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --addtag Test1 --epochs 20
python3 ProgressionPerformance.py --indir 2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95 --v HCAL --tag DataReco --addtag Test1 --epochs 20 \
    --set Test --eventLim 20000 --filesLim 1
'''

4) Extract SFs, plot SFs and plot performance from testing sample: # [FIXME] Make everything faster with npz instead of dataframes

'''
python3 PrepareReEmulation.py --indir 2023_12_10_NtuplesV55/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot70_MinusIem \
    --v HCAL --tag DataReco_200 --applyECAL False --modelRate --addtag Test1 --filesLim 1

python3 ProduceCaloParams.py --name caloParams_2023_v55_newCalib_cfi \
    --base caloParams_2023_v0_2_noL1Calib_cfi.py \
    --ECAL /data_CMS/cms/motta/CaloL1calibraton/2023_03_06_NtuplesV33/ECALtrainingDataReco_normalOrder/data/ScaleFactors_ECAL_energystep2iEt.csv \
    --HCAL /data_CMS/cms/motta/CaloL1calibraton/2023_12_10_NtuplesV55/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot70_MinusIem/HCALtrainingDataReco_200/data/ScaleFactors_HCAL_energystep2iEt.csv \
    --HF   /data_CMS/cms/motta/CaloL1calibraton/2023_12_10_NtuplesV55/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot70_MinusIem/HCALtrainingDataReco_200/data/ScaleFactors_HF_energystep2iEt.csv
'''

5) Re-emulate:

- Create caloParams file
- Copy the file to the src/L1Trigger/L1TCalorimeter/python/ folder
- Launche re-emulation:

'''
python submitOnTier3.py --inFileList JetMET__Run2022G-PromptReco-v1__Run362617__AOD \
    --outTag GT130XdataRun3Promptv3_CaloParams2023v52_data_reco_json \
    --nJobs 31 \
    --queue short \
    --maxEvts 5000 \
    --inJson Cert_Collisions2022_355100_362760_Golden \
    --caloParams caloParams_2023_v52_newCalib_cfi \
    --globalTag 130X_dataRun3_Prompt_v3 \
    --data \
    --recoFromAOD
python submitOnTier3.py --inFileList EphemeralZeroBias0__Run2022G-v1__Run362617__RAW \
    --outTag GT130XdataRun3Promptv3_CaloParams2023v52newCalib_data \
    --nJobs 31 \
    --queue short \
    --maxEvts 5000 \
    --caloParams caloParams_2023_v52_newCalib_cfi \
    --globalTag 130X_dataRun3_Prompt_v3 \
    --data

python submitOnTier3.py --inFileList JetMET__Run2022G-PromptReco-v1__Run362617__AOD \
    --outTag GT130XdataRun3Promptv3_CaloParams2023v52_HF3x3_data_reco_json \
    --nJobs 31 \
    --queue short \
    --maxEvts 5000 \
    --inJson Cert_Collisions2022_355100_362760_Golden \
    --caloParams caloParams_2023_v52_HF3x3_newCalib_cfi \
    --globalTag 130X_dataRun3_Prompt_v3 \
    --data \
    --recoFromAOD
python submitOnTier3.py --inFileList EphemeralZeroBias0__Run2022G-v1__Run362617__RAW \
    --outTag GT130XdataRun3Promptv3_CaloParams2023v52HF3x3newCalib_data \
    --nJobs 31 \
    --queue short \
    --maxEvts 5000 \
    --caloParams caloParams_2023_v52_HF3x3_newCalib_cfi \
    --globalTag 130X_dataRun3_Prompt_v3 \
    --data

python submitOnTier3.py --inFileList JetMET__Run2022G-PromptReco-v1__Run362617__AOD \
    --outTag GT130XdataRun3Promptv3_CaloParams2023ECALv33HCALv51HFv52_data_reco_json \
    --nJobs 31 \
    --queue short \
    --maxEvts 5000 \
    --inJson Cert_Collisions2022_355100_362760_Golden \
    --caloParams caloParams_2023_ECALv33_HCALv51_HFv52_newCalib_cfi \
    --globalTag 130X_dataRun3_Prompt_v3 \
    --data \
    --recoFromAOD
python submitOnTier3.py --inFileList EphemeralZeroBias0__Run2022G-v1__Run362617__RAW \
    --outTag GT130XdataRun3Promptv3_CaloParams2023ECALv33HCALv51HFv52newCalib_data \
    --nJobs 31 \
    --queue short \
    --maxEvts 5000 \
    --caloParams caloParams_2023_ECALv33_HCALv51_HFv52_newCalib_cfi \
    --globalTag 130X_dataRun3_Prompt_v3 \
    --data
'''

6) Performance evaluation:

'''
python3 resolutions_CD.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v52_data_reco_json/GoodNtuples \
 --outdir 2023_12_10_NtuplesV55/JetMET_PuppiJet_Pt30_HoTot95 --label Muon_data_reco --reco --nEvts 100000 --target jet \
 --raw --PuppiJet --jetPtcut 30 --HoTotcut 0.95 --OnlyIhad --tag _PuppiJet_100K_Barrel_Pt30_HoTot95_OnlyIhad_CD
python3 resolutions_CD.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v52_data_reco_json/GoodNtuples \
 --outdir 2023_12_10_NtuplesV55/JetMET_PuppiJet_Pt30_HoTot95 --label Muon_data_reco --reco --nEvts 100000 --target jet \
 --raw --PuppiJet --jetPtcut 30 --HoTotcut 0.95 --tag _PuppiJet_100K_Barrel_Pt30_HoTot95_CD
python3 resolutions_CD.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v52_data_reco_json/GoodNtuples \
 --outdir 2023_12_10_NtuplesV55/JetMET_PuppiJet_Pt30_HoTot95 --label Muon_data_reco --reco --nEvts 100000 --target jet \
 --raw --PuppiJet --jetPtcut 30 --tag _PuppiJet_100K_Barrel_Pt30_CD

# UnCalib
python3 resolutions.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
 --outdir 2023_12_10_NtuplesV55/NtuplesVunc_Raw_Puppi_Pt30 --label Muon_data_reco --reco --nEvts 100000 --target jet --raw --PuppiJet --jetPtcut 30 --do_HoTot
python3 turnOn.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples \
 --outdir 2023_12_10_NtuplesV55/NtuplesVunc_Raw_Puppi_Pt30 --label Muon_data_reco --reco --nEvts 100000 --target jet --raw --PuppiJet --jetPtcut 15 --er 1.305
python3 rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data \
 --outdir 2023_12_10_NtuplesV55/NtuplesVunc_Raw_Puppi_Pt30 --label Muon_data_reco --nEvts 100000 --target jet --raw --er 1.305
# OldCalib
python3 resolutions.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_data_reco_json/GoodNtuples \
 --outdir 2023_12_10_NtuplesV55/NtuplesVcur_Raw_Puppi_Pt30 --label Muon_data_reco --reco --nEvts 100000 --target jet --raw --PuppiJet --jetPtcut 30 --do_HoTot
python3 turnOn.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_data_reco_json/GoodNtuples \
 --outdir 2023_12_10_NtuplesV55/NtuplesVcur_Raw_Puppi_Pt30 --label Muon_data_reco --reco --nEvts 100000 --target jet --raw --PuppiJet --jetPtcut 15 --er 1.305
python3 rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v02_data \
 --outdir 2023_12_10_NtuplesV55/NtuplesVcur_Raw_Puppi_Pt30 --label Muon_data_reco --nEvts 100000 --target jet --raw --er 1.305

# NewCalib 52
python3 RemoveBadNtuples_Muon.py /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v52_data_reco_json
python3 resolutions.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v52_data_reco_json/GoodNtuples \
 --outdir 2023_12_10_NtuplesV55/NtuplesV52new_Raw_Puppi_Pt30 --label Muon_data_reco --reco --nEvts 100000 --target jet --raw --PuppiJet --jetPtcut 30 --do_HoTot
python3 turnOn.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v52_data_reco_json/GoodNtuples \
 --outdir 2023_12_10_NtuplesV55/NtuplesV52new_Raw_Puppi_Pt30 --label Muon_data_reco --reco --nEvts 100000 --target jet --raw --PuppiJet --jetPtcut 15 --er 1.305
python3 rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023v52newCalib_data \
 --outdir 2023_12_10_NtuplesV55/NtuplesV52new_Raw_Puppi_Pt30 --label Muon_data_reco --nEvts 100000 --target jet --raw --er 1.305
python3 comparisonPlots.py --indir 2023_12_10_NtuplesV55/NtuplesV52new_Raw_Puppi_Pt30 --label Muon_data_reco  --target jet --reco \
 --thrsFixRate 40 --thrsFixRate 60 --thrsFixRate 80 --thrsFixRate 100 \
 --old 2023_12_10_NtuplesV55/NtuplesVcur_Raw_Puppi_Pt30 --unc 2023_12_10_NtuplesV55/NtuplesVunc_Raw_Puppi_Pt30 --do_HoTot --er 1.305

# NewCalib ECALv33_HCALv51_HFv52
python3 RemoveBadNtuples_Muon.py /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023ECALv33HCALv51HFv52_data_reco_json
python3 resolutions.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023ECALv33HCALv51HFv52_data_reco_json/GoodNtuples \
 --outdir 2023_12_10_NtuplesV55/NtuplesECALV33_HCALV51_HFV52_Raw_Puppi_Pt30 --label Muon_data_reco --reco --nEvts 100000 --target jet --raw --PuppiJet --jetPtcut 30 --do_HoTot
python3 turnOn.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023ECALv33HCALv51HFv52_data_reco_json/GoodNtuples \
 --outdir 2023_12_10_NtuplesV55/NtuplesECALV33_HCALV51_HFV52_Raw_Puppi_Pt30 --label Muon_data_reco --reco --nEvts 100000 --target jet --raw --PuppiJet --jetPtcut 15 --er 1.305
python3 rate.py --indir EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023ECALv33HCALv51HFv52newCalib_data \
 --outdir 2023_12_10_NtuplesV55/NtuplesECALV33_HCALV51_HFV52_Raw_Puppi_Pt30 --label Muon_data_reco --nEvts 100000 --target jet --raw --er 1.305
python3 comparisonPlots.py --indir 2023_12_10_NtuplesV55/NtuplesECALV33_HCALV51_HFV52_Raw_Puppi_Pt30 --label Muon_data_reco  --target jet --reco \
 --thrsFixRate 40 --thrsFixRate 60 --thrsFixRate 80 \
 --old 2023_12_10_NtuplesV55/NtuplesVcur_Raw_Puppi_Pt30 --unc 2023_12_10_NtuplesV55/NtuplesVunc_Raw_Puppi_Pt30 --do_HoTot --er 1.305
'''

'''
python3 comparisonPlots_old.py --indir 2023_03_06_NtuplesV33 --label EGamma_data_reco --target ele --reco \
 --thrsFixRate 10 --thrsFixRate 12 --thrsFixRate 15 --thrsFixRate 30 --thrsFixRate 36 --thrsFixRate 40 \
 --old 0000_00_00_NtuplesVcur --unc 0000_00_00_NtuplesVunc --ref _currCalib --tag _normalOrder
/data_CMS/cms/motta/CaloL1calibraton/2023_03_06_NtuplesV33/PerformancePlots_normalOrder_LooseElectron_raw
'''

'''
### 
python3 resolutions.py --indir EGamma__Run2022G-ZElectron-PromptReco-v1__Run362617__RAW-RECO__GT124XdataRun3Promptv10_CaloParams2022v33newCalibNew_data_reco_json \
 --outdir 2023_09_11_NtuplesV33/NtuplesECALV33_WS --label EGamma_data_reco --reco --nEvts 100000 --target ele --raw --LooseEle --do_EoTot
python3 resolutions.py --indir EGamma__Run2022G-ZElectron-PromptReco-v1__Run362617__RAW-RECO__GT124XdataRun3Promptv10_CaloParams2022v06_noL1Calib_data_reco_json \
 --outdir 2023_09_11_NtuplesV33/NtuplesECALNoCalib_WS --label EGamma_data_reco --reco --nEvts 100000 --target ele --raw --LooseEle --do_EoTot
python3 resolutions.py --indir EGamma__Run2022G-ZElectron-PromptReco-v1__Run362616__RAW-RECO__GT124XdataRun3Promptv10_CaloParams2022v06_data_reco_json \
 --outdir 2023_09_11_NtuplesV33/NtuplesECALCurCalib_WS --label EGamma_data_reco --reco --nEvts 100000 --target ele --raw --LooseEle --do_EoTot
python3 resolutions.py --indir EGamma__Run2022G-ZElectron-PromptReco-v1__Run362617__RAW-RECO__GT124XdataRun3Promptv10_CaloParams2022v06oldHcalL1Calib_data_reco_json \
 --outdir 2023_09_11_NtuplesV33/NtuplesECALOldCalib_WS --label EGamma_data_reco --reco --nEvts 100000 --target ele --raw --LooseEle --do_EoTot

#
python3 resolutions.py --indir EGamma__Run2022G-ZElectron-PromptReco-v1__Run362617__RAW-RECO__GT124XdataRun3Promptv10_CaloParams2022v33newCalibNew_data_reco_json \
 --outdir 2023_09_11_NtuplesV33/L1Workshop/NtuplesECALV33 --label EGamma_data_reco --reco --nEvts 60000 --target ele
python3 resolutions.py --indir EGamma__Run2022G-ZElectron-PromptReco-v1__Run362617__RAW-RECO__GT124XdataRun3Promptv10_CaloParams2022v06_noL1Calib_data_reco_json \
 --outdir 2023_09_11_NtuplesV33/L1Workshop/NtuplesECALNoCalib --label EGamma_data_reco --reco --nEvts 60000 --target ele
python3 resolutions.py --indir EGamma__Run2022G-ZElectron-PromptReco-v1__Run362616__RAW-RECO__GT124XdataRun3Promptv10_CaloParams2022v06_data_reco_json \
 --outdir 2023_09_11_NtuplesV33/L1Workshop/NtuplesECALCurCalib --label EGamma_data_reco --reco --nEvts 60000 --target ele
python3 resolutions.py --indir EGamma__Run2022G-ZElectron-PromptReco-v1__Run362617__RAW-RECO__GT124XdataRun3Promptv10_CaloParams2022v06oldHcalL1Calib_data_reco_json \
 --outdir 2023_09_11_NtuplesV33/L1Workshop/NtuplesECALOldCalib --label EGamma_data_reco --reco --nEvts 60000 --target ele
python3 comparisonPlots_old.py --indir 2023_09_11_NtuplesV33/L1Workshop/NtuplesECALV33 --label EGamma_data_reco  --target ele --reco \
 --old 2023_09_11_NtuplesV33/L1Workshop/NtuplesECALOldCalib --unc 2023_09_11_NtuplesV33/L1Workshop/NtuplesECALNoCalib \
 --doRate False --doTurnOn False --ref _oldCalib
python3 comparisonPlots_old.py --indir 2023_09_11_NtuplesV33/L1Workshop/NtuplesECALV33 --label EGamma_data_reco  --target ele --reco \
 --old 2023_09_11_NtuplesV33/L1Workshop/NtuplesECALCurCalib --unc 2023_09_11_NtuplesV33/L1Workshop/NtuplesECALNoCalib \
 --doRate False --doTurnOn False --ref _curCalib
# NO

#
python3 resolutions.py --indir EGamma__Run2022G-ZElectron-PromptReco-v1__Run362617__RAW-RECO__GT130XdataRun3Promptv3_CaloParams2023ECALv33_data_reco_json \
 --outdir 2023_09_11_NtuplesV33/L1Workshop_GT130X_Run362617/NtuplesECALV33 --label EGamma_data_reco --reco --nEvts 60000 --target ele
python3 resolutions.py --indir EGamma__Run2022G-ZElectron-PromptReco-v1__Run362617__RAW-RECO__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json \
 --outdir 2023_09_11_NtuplesV33/L1Workshop_GT130X_Run362617/NtuplesECALNoCalib --label EGamma_data_reco --reco --nEvts 60000 --target ele
python3 resolutions.py --indir EGamma__Run2022G-ZElectron-PromptReco-v1__Run362617__RAW-RECO__GT130XdataRun3Promptv3_CaloParams2023v02_data_reco_json \
 --outdir 2023_09_11_NtuplesV33/L1Workshop_GT130X_Run362617/NtuplesECALCurCalib --label EGamma_data_reco --reco --nEvts 60000 --target ele
python3 comparisonPlots_old.py --indir 2023_09_11_NtuplesV33/L1Workshop_GT130X_Run362617/NtuplesECALV33 --label EGamma_data_reco  --target ele --reco \
 --old 2023_09_11_NtuplesV33/L1Workshop_GT130X_Run362617/NtuplesECALCurCalib --unc 2023_09_11_NtuplesV33/L1Workshop_GT130X_Run362617/NtuplesECALNoCalib \
 --doRate False --doTurnOn False
# NO

#
python3 resolutions.py --indir EGamma__Run2022G-ZElectron-PromptReco-v1__Run362616__RAW-RECO__GT130XdataRun3Promptv3_CaloParams2023v51A_ECALv33_data_reco_json \
 --outdir 2023_09_11_NtuplesV33/L1Workshop_GT130X_Run362616/NtuplesECALV33 --label EGamma_data_reco --reco --nEvts 60000 --target ele
python3 resolutions.py --indir EGamma__Run2022G-ZElectron-PromptReco-v1__Run362616__RAW-RECO__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json \
 --outdir 2023_09_11_NtuplesV33/L1Workshop_GT130X_Run362616/NtuplesECALNoCalib --label EGamma_data_reco --reco --nEvts 60000 --target ele
python3 resolutions.py --indir EGamma__Run2022G-ZElectron-PromptReco-v1__Run362616__RAW-RECO__GT130XdataRun3Promptv3_CaloParams2023v02_data_reco_json \
 --outdir 2023_09_11_NtuplesV33/L1Workshop_GT130X_Run362616/NtuplesECALCurCalib --label EGamma_data_reco --reco --nEvts 60000 --target ele
python3 comparisonPlots_old.py --indir 2023_09_11_NtuplesV33/L1Workshop_GT130X_Run362616/NtuplesECALV33 --label EGamma_data_reco  --target ele --reco \
 --old 2023_09_11_NtuplesV33/L1Workshop_GT130X_Run362616/NtuplesECALCurCalib --unc 2023_09_11_NtuplesV33/L1Workshop_GT130X_Run362616/NtuplesECALNoCalib \
 --doRate False --doTurnOn False
#


python3 comparisonPlots_old.py --indir 2023_09_11_NtuplesV33/NtuplesECALV33_WS --label EGamma_data_reco  --target ele --reco \
 --old 2023_09_11_NtuplesV33/NtuplesECALCurCalib_WS --unc 2023_09_11_NtuplesV33/NtuplesECALNoCalib_WS --do_EoTot \
 --doRate False --doTurnOn False --ref _currCalib
python3 comparisonPlots_old.py --indir 2023_09_11_NtuplesV33/NtuplesECALV33_WS --label EGamma_data_reco  --target ele --reco \
 --old 2023_09_11_NtuplesV33/NtuplesECALOldCalib_WS --unc 2023_09_11_NtuplesV33/NtuplesECALNoCalib_WS --do_EoTot \
 --doRate False --doTurnOn False --ref _oldCalib

python3 comparisonPlots_old.py --indir 2023_03_06_NtuplesV33 --label EGamma_data_reco --target ele --reco \
 --thrsFixRate 10 --thrsFixRate 12 --thrsFixRate 15 --thrsFixRate 30 --thrsFixRate 36 --thrsFixRate 40 \
 --old 0000_00_00_NtuplesVcur --unc 0000_00_00_NtuplesVunc --ref _currCalib --tag _normalOrder
'''