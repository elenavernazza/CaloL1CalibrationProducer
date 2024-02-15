# CaloL1CalibrationProducer

This repository contains all the packages and scripts to produce and test the Layer-1 Trigger Towers (TT) calibration.

### Introduction

This guide contains the instructions to extract the calibration from 2023 data to be applied to 2024 data taking.
It is divided into:
- [Installation](#introduction)
- [1. Re-emulate data with the latest data taking conditions](#1-re-emulate-data-with-the-latest-data-taking-conditions)
- [2. Read jets a prepare inputs](#2-read-jets-a-prepare-inputs)
- [3. Train the model and extract the Scale Factors](#3-train-the-model-and-extract-the-scale-factors)

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
- EGamma for the calibration of ECAL
- JetMET for the calibration of HCAL and HF
- ZeroBias for the rate simulation

Once the list of files for the three datasets is finalized, copy the list to a txt file inside the `L1NtupleLauncher/inputFiles` folder.

<details>
<summary>File list</summary>

- EGamma

```bash
dasgoclient --query=="file dataset=/EGamma0/Run2023B-ZElectron-PromptReco-v1/RAW-RECO" >> L1NtupleLauncher/inputFiles/EGamma__Run2023B-ZElectron-PromptReco-v1__RAW-RECO.txt
dasgoclient --query=="file dataset=/EGamma1/Run2023B-ZElectron-PromptReco-v1/RAW-RECO" >> L1NtupleLauncher/inputFiles/EGamma__Run2023B-ZElectron-PromptReco-v1__RAW-RECO.txt

dasgoclient --query=="file dataset=/EGamma0/Run2023C-ZElectron-PromptReco-v4/RAW-RECO" >> L1NtupleLauncher/inputFiles/EGamma__Run2023C-ZElectron-PromptReco-v4__RAW-RECO.txt
dasgoclient --query=="file dataset=/EGamma1/Run2023C-ZElectron-PromptReco-v4/RAW-RECO" >> L1NtupleLauncher/inputFiles/EGamma__Run2023C-ZElectron-PromptReco-v4__RAW-RECO.txt

dasgoclient --query=="file dataset=/EGamma0/Run2023D-ZElectron-PromptReco-v2/RAW-RECO" >> L1NtupleLauncher/inputFiles/EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO.txt
dasgoclient --query=="file dataset=/EGamma1/Run2023D-ZElectron-PromptReco-v2/RAW-RECO" >> L1NtupleLauncher/inputFiles/EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO.txt
```

- JetMET

```bash
dasgoclient --query=="file dataset=/JetMET0/Run2023B-PromptReco-v1/AOD" >> L1NtupleLauncher/inputFiles/JetMET__Run2023B-PromptReco-v1__AOD.txt
dasgoclient --query=="file dataset=/JetMET1/Run2023B-PromptReco-v1/AOD" >> L1NtupleLauncher/inputFiles/JetMET__Run2023B-PromptReco-v1__AOD.txt

dasgoclient --query=="file dataset=/JetMET0/Run2023C-PromptReco-v4/AOD" >> L1NtupleLauncher/inputFiles/JetMET__Run2023C-PromptReco-v4__AOD.txt
dasgoclient --query=="file dataset=/JetMET1/Run2023C-PromptReco-v4/AOD" >> L1NtupleLauncher/inputFiles/JetMET__Run2023C-PromptReco-v4__AOD.txt

dasgoclient --query=="file dataset=/JetMET0/Run2023D-PromptReco-v2/AOD" >> L1NtupleLauncher/inputFiles/JetMET__Run2023D-PromptReco-v2__AOD.txt
dasgoclient --query=="file dataset=/JetMET1/Run2023D-PromptReco-v2/AOD" >> L1NtupleLauncher/inputFiles/JetMET__Run2023D-PromptReco-v2__AOD.txt
```

- ZeroBias

```bash
dasgoclient --query=="file dataset=/EphemeralZeroBias0/Run2023D-v1/RAW" >> L1NtupleLauncher/inputFiles/EphemeralZeroBias__Run2023D-v1__RAW.txt
```

</details>

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
voms-proxy-init --rfc --voms cms -valid 192:00

python submitOnTier3.py --inFileList EGamma__Run2023B-ZElectron-PromptReco-v1__RAW-RECO \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --caloParams caloParams_2023_v0_4_noL1Calib_cfi \
    --globalTag 130X_dataRun3_Prompt_v4 \
    --nJobs 1344 --queue short --maxEvts -1 --data --recoFromSKIM

python submitOnTier3.py --inFileList EGamma__Run2023C-ZElectron-PromptReco-v4__RAW-RECO \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --caloParams caloParams_2023_v0_4_noL1Calib_cfi \
    --globalTag 130X_dataRun3_Prompt_v4 \
    --nJobs 11105 --queue short --maxEvts -1 --data --recoFromSKIM

python submitOnTier3.py --inFileList EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --caloParams caloParams_2023_v0_4_noL1Calib_cfi \
    --globalTag 130X_dataRun3_Prompt_v4 \
    --nJobs 1663 --queue short --maxEvts -1 --data --recoFromSKIM
```

### Re-emulate JetMET

```bash
cd L1NtupleLauncher
voms-proxy-init --rfc --voms cms -valid 192:00

python submitOnTier3.py --inFileList JetMET__Run2023B-PromptReco-v1__AOD \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --caloParams caloParams_2023_v0_4_noL1Calib_cfi \
    --globalTag 130X_dataRun3_Prompt_v4 \
    --nJobs 5828 --queue short --maxEvts -1 --data --recoFromAOD

python submitOnTier3.py --inFileList JetMET__Run2023C-PromptReco-v4__AOD \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --caloParams caloParams_2023_v0_4_noL1Calib_cfi \
    --globalTag 130X_dataRun3_Prompt_v4 \
    --nJobs 33373 --queue short --maxEvts -1 --data --recoFromAOD

python submitOnTier3.py --inFileList JetMET__Run2023D-PromptReco-v2__AOD \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --caloParams caloParams_2023_v0_4_noL1Calib_cfi \
    --globalTag 130X_dataRun3_Prompt_v4 \
    --nJobs 3560 --queue short --maxEvts -1 --data --recoFromAOD
```

### Re-emulate data ZeroBias

```bash
cd L1NtupleLauncher
voms-proxy-init --rfc --voms cms -valid 192:00

python submitOnTier3.py --inFileList EphemeralZeroBias__Run2023D-v1__RAW \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --caloParams caloParams_2023_v0_4_noL1Calib_cfi \
    --globalTag 130X_dataRun3_Prompt_v4 \
    --nJobs 772 --queue short --maxEvts -1 --data
```

Since many files are on TAPE, some jobs will fail due to error opening the file.
To only select the good files and eventually resubmit non-finished jobs use:

```bash
python3 resubmit_Unfinished.py /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/EGamma__Run2023B-ZElectron-PromptReco-v1__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json
python3 resubmit_Unfinished.py /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/JetMET__Run2023B-PromptReco-v1__AOD__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json
```

You can plot the re-emulated samples using:

```bash
python3 resolutions.py --indir EGamma__Run2023B-ZElectron-PromptReco-v1__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
 --outdir 2024_02_15_NtuplesV58/TestInput_EGamma2023B --label EGamma_data_reco --reco --nEvts 50000 --target ele \
 --raw --LooseEle --do_EoTot --tag _LooseEle_50K_Raw

python3 resolutions.py --indir JetMET__Run2023B-PromptReco-v1__AOD__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
 --outdir 2024_02_15_NtuplesV58/TestInput_JetMET2023B --label Jet_data_reco --reco --nEvts 50000 --target jet \
 --raw --PuppiJet --jetPtcut 30 --do_HoTot --tag _PuppiJet_50K_Pt30_Raw
```

## 2. Read jets a prepare inputs

At this point we can read the re-emulated samples to extract the 9x9 chunky donut describing the EGamma and Jets at Layer-1.
<!-- We need to add all the samples here (B,C,D) -->

### Read EGamma

```bash
cd L1NtupleReader
python3 batchSubmitOnTier3.py --indir /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/EGamma__Run2023B-ZElectron-PromptReco-v1__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
    --outdir /data_CMS/cms/motta/CaloL1calibraton/2024_02_15_NtuplesV58/EGamma_Run2023B_LooseEle_EoTot80 \
    --target reco --type ele --chunk_size 5000 \
    --queue short \
    --ecalcut 0.80 --applyCut_3_6_9 True --LooseEle --matching
```

### Read Jet

```bash
cd L1NtupleReader
python3 batchSubmitOnTier3.py --indir /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/JetMET__Run2023B-PromptReco-v1__AOD__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
    --outdir /data_CMS/cms/motta/CaloL1calibraton/2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70 \
    --target reco --type jet --chunk_size 5000 \
    --queue short \
    --hcalcut 0.70 --lJetPtCut 30 --PuppiJet --matching
python3 batchSubmitOnTier3.py --indir /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/JetMET__Run2023B-PromptReco-v1__AOD__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
    --outdir /data_CMS/cms/motta/CaloL1calibraton/2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_BarrelEndcap_Pt30_HoTot70 \
    --target reco --type jet --chunk_size 5000 \
    --queue short \
    --hcalcut 0.70 --lJetPtCut 30 --PuppiJet --matching --etacut 28
```

## 3. Train the model and extract the Scale Factors

```bash
cd L1JaxTraining
python3 JaxOptimizer.py --indir 2023_12_13_NtuplesV56/Input2/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot70/GoodNtuples/tensors \
 --odir Trainings_2023 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scale 0.5 --v HCAL
```