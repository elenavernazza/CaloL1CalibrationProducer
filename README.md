# CaloL1CalibrationProducer

This repository contains all the packages and scripts to produce and test the Layer-1 Trigger Towers (TT) calibration.

### Introduction

This guide contains the instructions to extract the calibration from 2023 data to be applied to 2024 data taking.

## Installation

```bash
cmsrel CMSSW_13_3_0
cd CMSSW_13_3_0/src
cmsenv
git cms-init
git cms-addpkg L1Trigger/L1TCalorimeter
git cms-addpkg L1Trigger/L1TNtuples
git cms-addpkg L1Trigger/Configuration
git cms-addpkg L1Trigger/L1TGlobal
git cms-addpkg L1Trigger/L1TCommon
git cms-addpkg L1Trigger/L1TZDC
mkdir L1Trigger/L1TZDC/data
cd L1Trigger/L1TZDC/data
wget https://raw.githubusercontent.com/cms-data/L1Trigger-L1TCalorimeter/master/zdcLUT_HI_v0_1.txt
cd -
git clone https://github.com/cms-l1t-offline/L1Trigger-L1TCalorimeter.git L1Trigger/L1TCalorimeter/data
git clone git@github.com:elenavernazza/CaloL1CalibrationProducer.git
git cms-checkdeps -A -a
scram b -j 8 
cd CaloL1CalibrationProducer
```

## 1. Re-emulate data with the latest data taking conditions

The first step is to re-emulate data acquired during 2023 with the latest data taking conditions.
The data samples can be found on [CMSDAS](https://cmsweb.cern.ch/das/).
We will use either RAW or RAW-RECO for the re-emulation, the other versions do not contain enough information.
Since these formats are quite heavy, always check that the files are actually available and not on TAPE.

Three datasets will be considered:
- EGamma for the calibration of ECAL [2023 datasets](https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FEGamma*%2FRun2023*ZElectron*%2FRAW-RECO)
- JetMET for the calibration of HCAL and HF [2023 datasets]()
- ZeroBias for the rate simulation

Once the list of files for the three datasets is finalized, copy the list to a txt file inside the `L1NtupleLauncher/inputFiles` folder.
- EGamma: 
`L1NtupleLauncher/inputFiles/EGamma__Run2023A-ZElectron-PromptReco-v2__RAW-RECO.txt`
`L1NtupleLauncher/inputFiles/EGamma__Run2023B-ZElectron-PromptReco-v1__RAW-RECO.txt`
`L1NtupleLauncher/inputFiles/EGamma__Run2023C-ZElectron-PromptReco-v4__RAW-RECO.txt`
`L1NtupleLauncher/inputFiles/EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO.txt` (for testing)
- JetMET:
`L1NtupleLauncher/inputFiles/JetMET__Run2023A-JetHTJetPlusHOFilter-PromptReco-v2__RAW_RECO.txt`
`L1NtupleLauncher/inputFiles/JetMET__Run2023B-JetHTJetPlusHOFilter-PromptReco-v1__RAW_RECO.txt`
`L1NtupleLauncher/inputFiles/JetMET__Run2023C-JetHTJetPlusHOFilter-PromptReco-v4__RAW_RECO.txt`
`L1NtupleLauncher/inputFiles/JetMET__Run2023D-JetHTJetPlusHOFilter-PromptReco-v2__RAW_RECO.txt` (for testing)
- ZeroBias:
`EphemeralZeroBias__Run2023D-v1__RAW` (for testing)

The latest data taking conditions are defined by:
- CMSSW version (CMSSW_13_3_0)
- globalTag (130X_dataRun3_Prompt_v4)
- current caloParams file (caloParams_2023_v0_4_noL1Calib_cfi)
- certification json [reference](https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions23/PromptReco/Cert_Collisions2023_366442_370790_Golden.json)

Note: This re-emulation calcels all the old calibration applied, so check that all the SFs are 1 in the caloParams_2023_v0_4_noL1Calib_cfi (except for the Zero Suppression). If not, change them manually.
Copy your certification json to `/L1NtupleLauncher/DataCertificationJsons`.
Copy your caloParams_2023_v0_4_noL1Calib_cfi.py to `src/L1Trigger/L1TCalorimeter/python/`.

### Re-emulate EGamma

```bash
cd L1NtupleLauncher

```

### Re-emulate JetMET

```bash
cd L1NtupleLauncher
voms-proxy-init --rfc --voms cms -valid 192:00
python submitOnTier3.py --inFileList JetMET__Run2023A-JetHTJetPlusHOFilter-PromptReco-v2__RAW_RECO \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --caloParams caloParams_2023_v0_4_noL1Calib_cfi \
    --globalTag 130X_dataRun3_Prompt_v4 \
    --nJobs 9 --queue short --maxEvts -1 --data --recoFromSKIM (--no_exec)
```

<!-- cmsRun L1Ntuple_cfg.py maxEvents=-1 inputFiles_load=/data_CMS/cms/motta/CaloL1calibraton/L1NTuples/JetMET__Run2023A-JetHTJetPlusHOFilter-PromptReco-v2__RAW_RECO__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/filelist_0.txt outputFile=Ntuple_0.root caloParams=caloParams_2023_v0_4_noL1Calib_cfi globalTag=130X_dataRun3_Prompt_v4 reco=1 data=1 JSONfile=/grid_mnt/data__data.polcms/cms/vernazza/L1TCalibration/2024_02_14/CMSSW_13_3_0/src/CaloL1CalibrationProducer/L1NtupleLauncher/DataCertificationJsons/Cert_Collisions2023_366442_370790_Golden.json -->

### Re-emulate data (ZB) with the current Global Tag

 cmsDriver.py l1Ntuple -s RAW2DIGI --python_filename=data.py -n 100 --no_output --era=Run3 --data --conditions=130X_dataRun3_Prompt_v4 --customise=L1Trigger/Configuration/customiseReEmul.L1TReEmulFromRAW  --customise=L1Trigger/L1TNtuples/customiseL1Ntuple.L1NtupleRAWEMU --customise=L1Trigger/Configuration/customiseSettings.L1TSettingsToCaloParams_2023_v0_4 --filein=/store/data/Run2023D/EphemeralZeroBias0/RAW/v1/000/370/293/00000/0545057e-416f-49e0-8ffb-fdca37061d4e.root 

 cmsRun L1Ntuple_cfg.py maxEvents=5000 inputFiles_load=/data_CMS/cms/motta/CaloL1calibraton/L1NTuples/EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023JAX7_data/filelist_0.txt outputFile=/data_CMS/cms/motta/CaloL1calibraton/L1NTuples/EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023JAX7_data/Ntuple_0.root caloParams=caloParams_2023_JAX7_newCalib_cfi globalTag=130X_dataRun3_Prompt_v3 data=1 >& /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/EphemeralZeroBias0__Run2022G-v1__Run362617__RAW__GT130XdataRun3Promptv3_CaloParams2023JAX7_data/log_0.txt

cmsRun L1Ntuple_cfg.py maxEvents=-1 inputFiles_load=/data_CMS/cms/motta/CaloL1calibraton/L1NTuples/JetMET__Run2023A-JetHTJetPlusHOFilter-PromptReco-v2__RAW_RECO__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/filelist_0.txt outputFile=/data_CMS/cms/motta/CaloL1calibraton/L1NTuples/JetMET__Run2023A-JetHTJetPlusHOFilter-PromptReco-v2__RAW_RECO__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/Ntuple_0.root caloParams=caloParams_2023_v0_4_noL1Calib_cfi globalTag=130X_dataRun3_Prompt_v4 reco=1 data=1 JSONfile=/grid_mnt/data__data.polcms/cms/vernazza/L1TCalibration/2024_02_14/CMSSW_13_3_0/src/CaloL1CalibrationProducer/L1NtupleLauncher/DataCertificationJsons/Cert_Collisions2023_366442_370790_Golden.json