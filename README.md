# CaloL1CalibrationProducer

This repository contains all the packages and scripts to produce and test the Layer-1 Trigger Towers (TT) calibration.

### Introduction

This guide contains the instructions to extract the calibration from 2023 data to be applied to 2024 data taking.
It is divided into:
- [Installation](#introduction)
- [1. Re-emulate data with the latest data taking conditions](#1-re-emulate-data-with-the-latest-data-taking-conditions)
- [2. Read jets a prepare inputs](#2-read-jets-a-prepare-inputs)
- [3. Train the model and extract the Scale Factors](#3-train-the-model-and-extract-the-scale-factors)
- [4. Re-emulate and compare with old calibration](#4-re-emulate-and-compare-with-old-calibration)

## Installation

<details>
<summary>Instructions</summary>

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

Activating the latest HCAL response corrections: [GoogleDOC](https://docs.google.com/document/d/1T0ileOTXzM7kgJx0V_dbJzcWr_JNbyi1V5mvssnigAI/edit)

```bash
mkdir L1NtupleLauncher/HCALResponseCorrections
scp evernazz@lxplus.cern.ch:/afs/cern.ch/user/m/mkrohn/public/ForLaurent/HcalRespCorrs_2023_v3.0_data.txt L1NtupleLauncher/HCALResponseCorrections
scp evernazz@lxplus.cern.ch:/afs/cern.ch/user/m/mkrohn/public/ForLaurent/HcalGains_2023_v2.0_data.txt L1NtupleLauncher/HCALResponseCorrections
```
</details>

## 1. Re-emulate data with the latest data taking conditions

The first step is to re-emulate data acquired during 2023 with the latest data taking conditions.
The data samples can be found on [CMSDAS](https://cmsweb.cern.ch/das/).

We will use either RAW or RAW-RECO for the re-emulation, the other versions do not contain enough information.
Since these formats are quite heavy, always check that the files are actually available and not on TAPE.

Three datasets will be considered:
- EGamma for the calibration of ECAL
- JetMET for the calibration of HCAL and HF
- ZeroBias for the rate simulation

<details>
<summary>File list</summary>

Once the list of files for the three datasets is finalized, copy the list to a txt file inside the `L1NtupleLauncher/inputFiles` folder.

- EGamma

```bash
dasgoclient --query=="file dataset=/EGamma0/Run2023D-ZElectron-PromptReco-v2/RAW-RECO" >> L1NtupleLauncher/inputFiles/EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO.txt
dasgoclient --query=="file dataset=/EGamma1/Run2023D-ZElectron-PromptReco-v2/RAW-RECO" >> L1NtupleLauncher/inputFiles/EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO.txt
```

Choose the runs you want to keep for the testing (around 150 files for EGamma): here 370774, 370775, 370776.
```bash
grep -v -E '370/(774|775|776)' L1NtupleLauncher/inputFiles/EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO.txt > L1NtupleLauncher/inputFiles/EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__Training.txt
grep -E '370/(774|775|776)' L1NtupleLauncher/inputFiles/EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO.txt > L1NtupleLauncher/inputFiles/EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__Testing.txt
```

- JetMET

```bash
dasgoclient --query=="file dataset=/JetMET0/Run2023D-PromptReco-v2/AOD" >> L1NtupleLauncher/inputFiles/JetMET__Run2023D-PromptReco-v2__AOD.txt
dasgoclient --query=="file dataset=/JetMET1/Run2023D-PromptReco-v2/AOD" >> L1NtupleLauncher/inputFiles/JetMET__Run2023D-PromptReco-v2__AOD.txt
```

Choose the runs you want to keep for the testing (around 30 files for Jet): here 370775.
```bash
grep -v -E '370/775' L1NtupleLauncher/inputFiles/JetMET__Run2023D-PromptReco-v2__AOD.txt > L1NtupleLauncher/inputFiles/JetMET__Run2023D-PromptReco-v2__AOD__Training.txt
grep -E '370/775' L1NtupleLauncher/inputFiles/JetMET__Run2023D-PromptReco-v2__AOD.txt > L1NtupleLauncher/inputFiles/JetMET__Run2023D-PromptReco-v2__AOD__Testing.txt
```

- ZeroBias (around 30 files only for testing)

```bash
dasgoclient --query=="file dataset=/EphemeralZeroBias0/Run2023D-v1/RAW" >> L1NtupleLauncher/inputFiles/EphemeralZeroBias__Run2023D-v1__RAW__Testing.txt
```

</details>

The latest data taking conditions are defined by:
- CMSSW version (CMSSW_13_3_0)
- globalTag (130X_dataRun3_Prompt_v4)
- current caloParams file (caloParams_2023_v0_4_noL1Calib_cfi)
- certification json [reference](https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions23/PromptReco/Cert_Collisions2023_366442_370790_Golden.json)

Note: This re-emulation cancels all the old calibration applied, so check that all the SFs are 1 in the caloParams_2023_v0_4_noL1Calib_cfi (except for the Zero Suppression). If not, change them manually.
Copy your certification json to `/L1NtupleLauncher/DataCertificationJsons`.
Copy your caloParams_2023_v0_4_noL1Calib_cfi.py to `src/L1Trigger/L1TCalorimeter/python/`.

### Re-emulate EGamma

```bash
cd L1NtupleLauncher
voms-proxy-init --rfc --voms cms -valid 192:00
python submitOnTier3.py --inFileList EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__Training \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --caloParams caloParams_2023_v0_4_noL1Calib_cfi \
    --globalTag 130X_dataRun3_Prompt_v4 \
    --nJobs 1489 --queue short --maxEvts -1 --data --recoFromSKIM
```

### Re-emulate JetMET

```bash
cd L1NtupleLauncher
voms-proxy-init --rfc --voms cms -valid 192:00
python submitOnTier3.py --inFileList JetMET__Run2023D-PromptReco-v2__AOD__Training \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --caloParams caloParams_2023_v0_4_noL1Calib_cfi \
    --globalTag 130X_dataRun3_Prompt_v4 \
    --nJobs 3478 --queue short --maxEvts -1 --data --recoFromAOD
```

<details>
<summary>Check samples</summary>

Since many files are on TAPE, some jobs will fail due to error opening the file.
To only select the good files and eventually resubmit non-finished jobs use:

```bash
python3 resubmit_Unfinished.py /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__Training__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json
```
```bash
python3 resubmit_Unfinished.py /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/JetMET__Run2023D-PromptReco-v2__AOD__Training__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json
```

You can plot the re-emulated samples using:

```bash
cd L1Plotting
python3 resolutions.py --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__Training__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
 --outdir 2024_03_05_NtuplesV59/TestInput_EGamma2023D --label EGamma_data_reco --reco --nEvts 50000 --target ele \
 --raw --LooseEle --do_EoTot --tag _LooseEle_50K_Raw
```
```bash
python3 resolutions.py --indir JetMET__Run2023D-PromptReco-v2__AOD__Training__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
 --outdir 2024_03_05_NtuplesV59/TestInput_JetMET2023D --label Jet_data_reco --reco --nEvts 50000 --target jet \
 --raw --PuppiJet --jetPtcut 30 --do_HoTot --tag _PuppiJet_50K_Pt30_Raw
```

</details>

## 2. Read jets a prepare inputs

At this point we can read the re-emulated samples to extract the 9x9 chunky donut / Cluster describing the EGamma and Jets at Layer-1.

The reader will loop over all the jets and save the input to `*.npz` tensors directly compatible with the training script.
Some selections are applied:
- DeltaR separation between two objects
- Matching between L1 object and Offline object
- Electromagnetic (ecalcut) or Hadronic (hcalcut) fraction
- For EGamma, only electrons passing the LooseEle flag are considered
- For Jets, minimum JetPt at 30 GeV
- If specified, maximum JetPt and maximum Eta 

### Read EGamma (Cluster)

```bash
cd L1NtupleReader
python3 batchSubmitOnTier3.py --indir /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__Training__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
    --outdir /data_CMS/cms/motta/CaloL1calibraton/2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster \
    --target reco --type ele --chunk_size 5000 \
    --queue short \
    --ecalcut 0.80 --applyCut_3_6_9 True --LooseEle --matching --ClusterFilter
```

### Read Jet (9x9 chunky donut)

```bash
cd L1NtupleReader
python3 batchSubmitOnTier3.py --indir /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/JetMET__Run2023D-PromptReco-v2__AOD__Training__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
    --outdir /data_CMS/cms/motta/CaloL1calibraton/2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70 \
    --target reco --type jet --chunk_size 5000 \
    --queue short \
    --hcalcut 0.70 --lJetPtCut 30 --PuppiJet --matching
```

## 3. Train the model and extract the Scale Factors

Before training the model, check the distribution of the input towers with:

```bash
cd L1JaxTraining
python3 TowersJetsCounter.py --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/TestInputEGamma_Cluster --jetsLim 1000000 --v ECAL
python3 TowersJetsCounter.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/TestInputJetMET --jetsLim 1000000 --v HCAL
```

If everything looks good, proceed with the calibration. The full list of trainings can be stored in `L1JaxTraining/Instructions/RunTrainings.sh`.

```bash
python3 JaxOptimizer.py \
    --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_X --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --scaleB 0.95 --scaleE 0.9 --v ECAL
```
```bash
python3 JaxOptimizer.py \
    --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_Y --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --v HCAL --maskHF
```

## 4. Re-emulate and compare with old calibration

You can now test the performance by plotting the SFs and re-emulating on the testing sample.

```bash
cd L1JaxTraining
voms-proxy-init --rfc --voms cms -valid 192:00
source Instructions/TestsTrainingECAL.sh JAX_ECAL_X
python3 PlotHistory.py --indir Trainings_2023/JAX_ECAL_X --v ECAL 
```
```bash
cd L1JaxTraining
voms-proxy-init --rfc --voms cms -valid 192:00
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_Y
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_Y --v HCAL 
```

<details>
<summary>Full commands ECAL</summary>

#### Testing

```bash
cd L1NtupleLauncher
voms-proxy-init --rfc --voms cms -valid 192:00
python submitOnTier3.py --inFileList EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__Testing \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --globalTag 130X_dataRun3_Prompt_v4 \
    --nJobs 174 --queue short --maxEvts -1 --data --recoFromSKIM \
    --caloParams caloParams_2023_v0_4_noL1Calib_cfi
python3 resubmit_Unfinished.py /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json
```

```bash
cd L1JaxTraining
voms-proxy-init --rfc --voms cms -valid 192:00
python3 SFPlots.py --indir Trainings_2023/JAX_ECAL_X --v ECAL
python3 ProduceCaloParams.py --name caloParams_2023_JAX_ECAL_X_newCalib_cfi \
 --ECAL Trainings_2023/JAX_ECAL_X/ScaleFactors_ECAL.csv \
 --base caloParams_2023_v0_4_noL1Calib_cfi.py

python3 RDF_ResolutionFast.py --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
 --reco --target ele --do_EoTot --raw --LooseEle --nEvts 100000 --no_plot \
 --ECALcalib --caloParam caloParams_2023_JAX_ECAL_X_newCalib_cfi.py --outdir Trainings_2023/JAX_ECAL_X/NtuplesVnew

python3 RDF_ResolutionFast.py --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
 --reco --target ele --do_EoTot --raw --LooseEle --nEvts 100000 --no_plot \
 --ECALcalib --caloParam caloParams_2023_v0_4_cfi.py \
 --outdir Trainings_2023/JAX_ECAL_0/NtuplesVold

python3 RDF_ResolutionFast.py --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
 --reco --target ele --do_EoTot --raw --LooseEle --nEvts 100000 --no_plot \
 --ECALcalib --caloParam caloParams_2023_v0_4_noL1Calib_cfi.py \
 --outdir Trainings_2023/JAX_ECAL_0/NtuplesVunc

python3 comparisonPlotsFast.py --target ele --reco \
 --old Trainings_2023/JAX_ECAL_0/NtuplesVold --unc Trainings_2023/JAX_ECAL_0/NtuplesVunc \
 --do_EoTot --doRate False --doTurnOn False \
 --indir Trainings_2023/JAX_ECAL_X/NtuplesVnew
```

#### Submit re-emulation

```bash
cd L1NtupleLauncher
voms-proxy-init --rfc --voms cms -valid 192:00
python3 submitOnTier3.py --inFileList EphemeralZeroBias__Run2023D-v1__RAW__Testing \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data \
    --nJobs 151 --queue short --maxEvts 2000 \
    --globalTag 130X_dataRun3_Prompt_v4 --data \
    --caloParams caloParams_2023_v0_4_noL1Calib_cfi
python3 submitOnTier3.py --inFileList EphemeralZeroBias__Run2023D-v1__RAW__Testing \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_data \
    --nJobs 151 --queue short --maxEvts 2000 \
    --globalTag 130X_dataRun3_Prompt_v4 --data \
    --caloParams caloParams_2023_v0_4_cfi
python3 submitOnTier3.py --inFileList EphemeralZeroBias__Run2023D-v1__RAW__Testing \
    --outTag GT130XdataRun3Promptv4_CaloParams2023JAX_ECAL_X_data \
    --nJobs 151 --queue short --maxEvts 2000 \
    --globalTag 130X_dataRun3_Prompt_v4 --data \
    --caloParams caloParams_2023_JAX_ECAL_X_newCalib_cfi

python submitOnTier3.py --inFileList EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__Testing \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --globalTag 130X_dataRun3_Prompt_v4 \
    --nJobs 174 --queue short --maxEvts -1 --data --recoFromSKIM \
    --caloParams caloParams_2023_v0_4_cfi
python submitOnTier3.py --inFileList EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__Testing \
    --outTag GT130XdataRun3Promptv4_CaloParams2023JAX_ECAL_X_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --globalTag 130X_dataRun3_Prompt_v4 \
    --nJobs 174 --queue short --maxEvts -1 --data --recoFromSKIM \
    --caloParams caloParams_2023_JAX_ECAL_X_newCalib_cfi
```

#### Select good files

```bash
python3 resubmit_Unfinished.py /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json
python3 resubmit_Unfinished.py /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_data_reco_json
```
</details>

<details>
<summary>Full commands HCAL</summary>

#### Testing

```bash
cd L1NtupleLauncher
voms-proxy-init --rfc --voms cms -valid 192:00
python3 submitOnTier3.py --inFileList JetMET__Run2023D-PromptReco-v2__AOD__Testing \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --nJobs 39 --queue short --maxEvts 3000 \
    --globalTag 130X_dataRun3_Prompt_v4 --data --recoFromAOD \
    --caloParams caloParams_2023_v0_4_noL1Calib_cfi
```

```bash
cd L1JaxTraining
python3 SFPlots.py --indir Trainings_2023/JAX_HCAL_Y
python3 ProduceCaloParams.py --name caloParams_2023_JAX_HCAL_Y_newCalib_cfi \
    --HCAL ./Trainings_2023/JAX_HCAL_Y/ScaleFactors_HCAL.csv --HF ./Trainings_2023/JAX_HCAL_Y/ScaleFactors_HCAL.csv \
    --base caloParams_2023_v0_4_noL1Calib_cfi.py

python3 RDF_ResolutionFast.py --indir JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
 --reco --target jet --do_HoTot --raw --PuppiJet --jetPtcut 30 --nEvts 100000 --no_plot \
 --HCALcalib --caloParam caloParams_2023_v0_4_cfi.py \
 --outdir Trainings_2023/JAX_HCAL_0/NtuplesVold --no_Satu
python3 RDF_ResolutionFast.py --indir JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
 --reco --target jet --do_HoTot --raw --PuppiJet --jetPtcut 30 --nEvts 100000 --no_plot \
 --HCALcalib --caloParam caloParams_2023_v0_4_noL1Calib_cfi.py \
 --outdir Trainings_2023/JAX_HCAL_0/NtuplesVunc --no_Satu
python3 RDF_ResolutionFast.py --indir JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
 --reco --target jet --do_HoTot --raw --PuppiJet --jetPtcut 30 --nEvts 100000 --no_plot \
 --HCALcalib --caloParam caloParams_2023_JAX_HCAL_Y_newCalib_cfi.py \
 --outdir Trainings_2023/JAX_HCAL_Y/NtuplesVnew --no_Satu

python3 comparisonPlotsFast.py --target jet --reco \
 --old Trainings_2023/JAX_HCAL_0/NtuplesVold --unc Trainings_2023/JAX_HCAL_0/NtuplesVunc \
 --do_HoTot --doRate False --doTurnOn False \
 --indir Trainings_2023/JAX_HCAL_Y/NtuplesVnew
```

#### Submit re-emulation

```bash
cd L1NtupleLauncher
voms-proxy-init --rfc --voms cms -valid 192:00
python3 submitOnTier3.py --inFileList EphemeralZeroBias__Run2023D-v1__RAW__Testing \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data \
    --nJobs 151 --queue short --maxEvts 2000 \
    --globalTag 130X_dataRun3_Prompt_v4 --data \
    --caloParams caloParams_2023_v0_4_noL1Calib_cfi
python3 submitOnTier3.py --inFileList EphemeralZeroBias__Run2023D-v1__RAW__Testing \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_data \
    --nJobs 151 --queue short --maxEvts 2000 \
    --globalTag 130X_dataRun3_Prompt_v4 --data \
    --caloParams caloParams_2023_v0_4_cfi
python3 submitOnTier3.py --inFileList EphemeralZeroBias__Run2023D-v1__RAW__Testing \
    --outTag GT130XdataRun3Promptv4_CaloParams2023JAX_HCAL_Y_data \
    --nJobs 151 --queue short --maxEvts 2000 \
    --globalTag 130X_dataRun3_Prompt_v4 --data \
    --caloParams caloParams_2023_JAX_HCAL_Y_newCalib_cfi

python3 submitOnTier3.py --inFileList JetMET__Run2023D-PromptReco-v2__AOD__Testing \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --nJobs 39 --queue short --maxEvts 3000 \
    --globalTag 130X_dataRun3_Prompt_v4 --data --recoFromAOD \
    --caloParams caloParams_2023_v0_4_noL1Calib_cfi
python3 submitOnTier3.py --inFileList JetMET__Run2023D-PromptReco-v2__AOD__Testing \
    --outTag GT130XdataRun3Promptv4_CaloParams2023v04_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --nJobs 39 --queue short --maxEvts 3000 \
    --globalTag 130X_dataRun3_Prompt_v4 --data --recoFromAOD \
    --caloParams caloParams_2023_v0_4_cfi
python3 submitOnTier3.py --inFileList JetMET__Run2023D-PromptReco-v2__AOD__Testing \
    --outTag GT130XdataRun3Promptv4_CaloParams2023JAX_HCAL_Y_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --nJobs 39 --queue short --maxEvts 3000 \
    --globalTag 130X_dataRun3_Prompt_v4 --data --recoFromAOD \
    --caloParams caloParams_2023_JAX_HCAL_Y_newCalib_cfi
```

#### Select good files

```bash
python3 resubmit_Unfinished.py /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json
python3 resubmit_Unfinished.py /data_CMS/cms/motta/CaloL1calibraton/L1NTuples/JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_data_reco_json
```

<!-- #### HCAL corrections

```bash
cd L1NtupleLauncher
voms-proxy-init --rfc --voms cms -valid 192:00
python3 submitOnTier3.py --inFileList EphemeralZeroBias__Run2023D-v1__RAW__Testing \
    --outTag GT130XdataRun3Promptv4_HCALCorr_CaloParams2023v04_noL1Calib_data \
    --nJobs 151 --queue short --maxEvts 2000 \
    --globalTag 130X_dataRun3_Prompt_v4 --data \
    --caloParams caloParams_2023_v0_4_noL1Calib_cfi
python3 submitOnTier3.py --inFileList EphemeralZeroBias__Run2023D-v1__RAW__Testing \
    --outTag GT130XdataRun3Promptv4_HCALCorr_CaloParams2023v04_data \
    --nJobs 151 --queue short --maxEvts 2000 \
    --globalTag 130X_dataRun3_Prompt_v4 --data \
    --caloParams caloParams_2023_v0_4_cfi

python submitOnTier3.py --inFileList EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO \
    --outTag GT130XdataRun3Promptv4_HCALCorr_CaloParams2023v04_noL1Calib_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --globalTag 130X_dataRun3_Prompt_v4 \
    --nJobs 300 --queue short --maxEvts -1 --data --recoFromSKIM \
    --caloParams caloParams_2023_v0_4_noL1Calib_cfi
python submitOnTier3.py --inFileList EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO \
    --outTag GT130XdataRun3Promptv4_HCALCorr_CaloParams2023v04_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --globalTag 130X_dataRun3_Prompt_v4 \
    --nJobs 300 --queue short --maxEvts -1 --data --recoFromSKIM \
    --caloParams caloParams_2023_v0_4_cfi

python3 submitOnTier3.py --inFileList JetMET__Run2023D-PromptReco-v2__AOD__Testing \
    --outTag GT130XdataRun3Promptv4_HCALCorr_CaloParams2023v04_noL1Calib_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --nJobs 39 --queue short --maxEvts 3000 \
    --globalTag 130X_dataRun3_Prompt_v4 --data --recoFromAOD \
    --caloParams caloParams_2023_v0_4_noL1Calib_cfi
python3 submitOnTier3.py --inFileList JetMET__Run2023D-PromptReco-v2__AOD__Testing \
    --outTag GT130XdataRun3Promptv4_HCALCorr_CaloParams2023v04_data_reco_json \
    --inJson Cert_Collisions2023_366442_370790_Golden \
    --nJobs 39 --queue short --maxEvts 3000 \
    --globalTag 130X_dataRun3_Prompt_v4 --data --recoFromAOD \
    --caloParams caloParams_2023_v0_4_cfi
``` -->

</details>

Plot the performance comparison between the unCalib, oldCalib, newCalib.

```bash
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_X
```
```bash
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_Y
```

<details>
<summary>Full commands ECAL</summary>

```bash
cd L1Plotting
python3 rate.py \
    --indir EphemeralZeroBias__Run2023D-v1__RAW__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data \
    --outdir 2024_03_05_NtuplesV59/JAX_ECAL/NtuplesVuncL1pt --target ele --raw --nEvts 100000 --no_plot
python3 rate.py \
    --indir EphemeralZeroBias__Run2023D-v1__RAW__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_data \
    --outdir 2024_03_05_NtuplesV59/JAX_ECAL/NtuplesVoldL1pt --target ele --raw --nEvts 100000 --no_plot
python3 rate.py \
    --indir EphemeralZeroBias__Run2023D-v1__RAW__Testing__GT130XdataRun3Promptv4_CaloParams2023JAX_ECAL_X_data \
    --outdir 2024_03_05_NtuplesV59/JAX_ECAL_X/NtuplesVnew --target ele --raw --nEvts 100000 --no_plot --tag L1pt

python3 turnOn.py \
    --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
    --outdir 2024_03_05_NtuplesV59/JAX_ECAL/NtuplesVuncL1pt --reco --target ele --raw --LooseEle --nEvts 100000
python3 turnOn.py \
    --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023v04_data_reco_json/GoodNtuples \
    --outdir 2024_03_05_NtuplesV59/JAX_ECAL/NtuplesVoldL1pt --reco --target ele --raw --LooseEle --nEvts 100000
python3 turnOn.py \
    --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023JAX_ECAL_X_data_reco_json \
    --outdir 2024_03_05_NtuplesV59/JAX_ECAL_X/NtuplesVnew --reco --target ele --raw --LooseEle --nEvts 100000 --tag L1pt

python3 resolutions.py \
    --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
    --outdir 2024_03_05_NtuplesV59/JAX_ECAL/NtuplesVuncL1pt --reco --target ele --raw --LooseEle --nEvts 100000 --no_plot
python3 resolutions.py \
    --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023v04_data_reco_json/GoodNtuples \
    --outdir 2024_03_05_NtuplesV59/JAX_ECAL/NtuplesVoldL1pt --reco --target ele --raw --LooseEle --nEvts 100000 --no_plot
python3 resolutions.py \
    --indir EGamma__Run2023D-ZElectron-PromptReco-v2__RAW-RECO__GT130XdataRun3Promptv4_CaloParams2023JAX_ECAL_X_data_reco_json \
    --outdir 2024_03_05_NtuplesV59/JAX_ECAL_X/NtuplesVnew --reco --target ele --raw --LooseEle --nEvts 100000 --no_plot --tag L1pt

python3 comparisonPlots.py \
    --indir 2024_03_05_NtuplesV59/JAX_ECAL_X/NtuplesVnew  --target ele --reco \
    --old 2024_03_05_NtuplesV59/JAX_ECAL/NtuplesVoldL1pt \
    --unc 2024_03_05_NtuplesV59/JAX_ECAL/NtuplesVuncL1pt \
    --thrsFixRate 10 --thrsFixRate 12 --thrsFixRate 20 --thrsFixRate 36 --tag L1pt

python3 rate.py \
    --indir EphemeralZeroBias__Run2023D-v1__RAW__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data \
    --outdir 2024_03_05_NtuplesV59/JAX_ECAL/NtuplesVuncL1pt --target ele --raw --nEvts 100000 --no_plot --offline
python3 rate.py \
    --indir EphemeralZeroBias__Run2023D-v1__RAW__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_data \
    --outdir 2024_03_05_NtuplesV59/JAX_ECAL/NtuplesVoldL1pt --target ele --raw --nEvts 100000 --no_plot --offline
python3 rate.py \
    --indir EphemeralZeroBias__Run2023D-v1__RAW__Testing__GT130XdataRun3Promptv4_CaloParams2023JAX_ECAL_X_data \
    --outdir 2024_03_05_NtuplesV59/JAX_ECAL_X/NtuplesVnew --target ele --raw --nEvts 100000 --no_plot --offline --tag L1pt

python3 comparisonPlots.py \
    --indir 2024_03_05_NtuplesV59/JAX_ECAL_X/NtuplesVnew  --target ele --reco \
    --old 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVoldL1pt \
    --unc 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVuncL1pt \
    --thrsFixRate 20 --thrsFixRate 30 --thrsFixRate 40 --tag L1pt --offline --doResponse False --doResolution False
```
</details>

<details>
<summary>Full commands HCAL</summary>

```bash
cd L1Plotting
python3 rate.py \
    --indir EphemeralZeroBias__Run2023D-v1__RAW__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data \
    --outdir 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVuncL1ptNoSatu --target jet --raw --nEvts 100000 --no_plot
python3 rate.py \
    --indir EphemeralZeroBias__Run2023D-v1__RAW__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_data \
    --outdir 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVoldL1ptNoSatu --target jet --raw --nEvts 100000 --no_plot
python3 rate.py \
    --indir EphemeralZeroBias__Run2023D-v1__RAW__Testing__GT130XdataRun3Promptv4_CaloParams2023JAX_HCAL_Y_data \
    --outdir 2024_03_05_NtuplesV59/JAX_HCAL_Y/NtuplesVnew --target jet --raw --nEvts 100000 --no_plot --tag L1ptNoSatu

python3 turnOn.py \
    --indir JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
    --outdir 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVuncL1ptNoSatu --reco --target jet --raw --PuppiJet --nEvts 100000
python3 turnOn.py \
    --indir JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_data_reco_json/GoodNtuples \
    --outdir 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVoldL1ptNoSatu --reco --target jet --raw --PuppiJet --nEvts 100000
python3 turnOn.py \
    --indir JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_CaloParams2023JAX_HCAL_Y_data_reco_json \
    --outdir 2024_03_05_NtuplesV59/JAX_HCAL_Y/NtuplesVnew --reco --target jet --raw --PuppiJet --nEvts 100000 --tag L1ptNoSatu

python3 resolutions.py \
    --indir JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
    --outdir 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVuncL1ptNoSatu --reco --target jet --raw --PuppiJet --jetPtcut 30 --nEvts 100000 --no_plot --no_Satu
python3 resolutions.py \
    --indir JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_data_reco_json/GoodNtuples \
    --outdir 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVoldL1ptNoSatu --reco --target jet --raw --PuppiJet --jetPtcut 30 --nEvts 100000 --no_plot --no_Satu
python3 resolutions.py \
    --indir JetMET__Run2023D-PromptReco-v2__AOD__Testing__GT130XdataRun3Promptv4_CaloParams2023JAX_HCAL_Y_data_reco_json \
    --outdir 2024_03_05_NtuplesV59/JAX_HCAL_Y/NtuplesVnew --reco --target jet --raw --PuppiJet --jetPtcut 30 --nEvts 100000 --no_plot --tag L1ptNoSatu --no_Satu

python3 comparisonPlots.py \
    --indir 2024_03_05_NtuplesV59/JAX_HCAL_Y/NtuplesVnew  --target jet --reco \
    --old 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVoldL1ptNoSatu \
    --unc 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVuncL1ptNoSatu \
    --thrsFixRate 40 --thrsFixRate 60 --thrsFixRate 80 --thrsFixRate 100 --tag L1ptNoSatu

python3 rate.py \
    --indir EphemeralZeroBias__Run2023D-v1__RAW__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data \
    --outdir 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVuncL1ptNoSatu --target jet --raw --nEvts 100000 --no_plot --offline
python3 rate.py \
    --indir EphemeralZeroBias__Run2023D-v1__RAW__Testing__GT130XdataRun3Promptv4_CaloParams2023v04_data \
    --outdir 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVoldL1ptNoSatu --target jet --raw --nEvts 100000 --no_plot --offline
python3 rate.py \
    --indir EphemeralZeroBias__Run2023D-v1__RAW__Testing__GT130XdataRun3Promptv4_CaloParams2023JAX_HCAL_Y_data \
    --outdir 2024_03_05_NtuplesV59/JAX_HCAL_Y/NtuplesVnew --target jet --raw --nEvts 100000 --no_plot --offline --tag L1ptNoSatu

python3 comparisonPlots.py \
    --indir 2024_03_05_NtuplesV59/JAX_HCAL_Y/NtuplesVnew  --target jet --reco \
    --old 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVoldL1ptNoSatu \
    --unc 2024_03_05_NtuplesV59/JAX_HCAL/NtuplesVuncL1ptNoSatu \
    --thrsFixRate 60 --thrsFixRate 70 --thrsFixRate 80 --tag L1ptNoSatu --offline --doResponse False --doResolution False
```
</details>

Re-emulate with ECAL and HCAL calibrations together.

```bash
source Instructions/TestTrainingCombination.sh ECAL_X HCAL_Y
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_X_HCAL_Y
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_X_HCAL_Y
```
