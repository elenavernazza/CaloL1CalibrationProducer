########################################################################################################################
# BIG BIG BUG
########################################################################################################################

Found a big bug in the caloParams definition!
The layer1HCalScaleETBins vector is in GeV! Not in iEt!

1. Correct iEt - GeV
2. Correct matrix of SFs in Jax
3. Correct SFPlots
4. Correct ProduceCaloParams
5. Correct RDFResolution
6. Check Mean Squared Percentage Error as a loss function
7. Retrain everything!

########################################################################################################################
# HCAL
########################################################################################################################

# OLD
JAX binning (iEt) = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 256]
JAX binning (GeV) = [0 ,0.5 ,1.0 ,1.5 ,2.0 ,2.5 ,3.0 ,3.5 ,4.0 ,4.5 ,5.0 ,5.5 ,6.0 ,6.5 ,7.0 ,7.5 ,8.0 ,8.5 ,9.0 ,9.5 ,10.0 ,11.0 ,12.0 ,13.0 ,14.0 ,15.0 ,17.5 ,20.0 ,22.5 ,25.0 ,27.5 ,30.0 ,32.5 ,35.0 ,37.5 ,40.0 ,42.5 ,45.0 ,47.5 ,50.0 ,128.0]

# NEW
Applied to towres = [[1], [2,3], [4,5], [6,7], ...]
JAX binning (iEt) = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 256]
JAX binning (GeV) = [1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15 ,16 ,17 ,18 ,19 ,20 ,21 ,22 ,23 ,24 ,25 ,30 ,35 ,40 ,45 ,50 ,55 ,60 ,65 ,70 ,75 ,80 ,85 ,90 ,95 ,100 ,128]

########################################################################################################################
# TEST HCAL 
########################################################################################################################

# ZS not working an TT28 not at 1
python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_41 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL --maskHF
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_41
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_41 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_41

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_42 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL --maskHF
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_42
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_42 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_42

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_43 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF --MSPE
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_43
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_43 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_43 && source Instructions/MoveToEos.sh JAX_HCAL_43 HCAL

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_44 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF \
    --scaleB 0.95 --scaleE 0.9
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_44
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_44 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_44 && source Instructions/MoveToEos.sh JAX_HCAL_44 HCAL

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_45 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF \
    --scaleB 0.95 --scaleE 0.95
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_45
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_45 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_45 && source Instructions/MoveToEos.sh JAX_HCAL_45 HCAL

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_46 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF \
    --scaleB 1 --scaleE 0.95
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_46
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_46 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_46 && source Instructions/MoveToEos.sh JAX_HCAL_46 HCAL

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_47 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_47
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_47 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_47 && source Instructions/MoveToEos.sh JAX_HCAL_47 HCAL

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_48 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL --maskHF \
    --ECALCalib Trainings_2023/JAX_ECAL_19/ScaleFactors_ECAL_Phys.csv
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_48
source Instructions/TestTrainingCombination.sh ECAL_19 HCAL_48
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_48 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_48
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_19_HCAL_48
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_19_HCAL_48

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_49 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL --maskHF \
    --ECALCalib Trainings_2023/JAX_ECAL_21/ScaleFactors_ECAL_Phys.csv
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_49
source Instructions/TestTrainingCombination.sh ECAL_21 HCAL_49
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_49 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_49
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_21_HCAL_49
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_21_HCAL_49

# 19 is better, but still a problem with HF: mask HF only up to 4 iEt = 1.5 GeV
python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_50 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL --maskHF \
    --ECALCalib Trainings_2023/JAX_ECAL_19/ScaleFactors_ECAL_Phys.csv
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_50
source Instructions/TestTrainingCombination.sh ECAL_19 HCAL_50
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_50 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_50
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_19_HCAL_50
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_19_HCAL_50

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_51 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL \
    --ECALCalib Trainings_2023/JAX_ECAL_19/ScaleFactors_ECAL_Phys.csv
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_51
source Instructions/TestTrainingCombination.sh ECAL_19 HCAL_51
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_51 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_51
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_19_HCAL_51
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_19_HCAL_51

# Test 1: Constrain SFs for iEt = 1 (0 for ieta < 16, 1 for 16 <= ieta <= 28, 0 for ieta > 28)
python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_52 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL \
    --ECALCalib Trainings_2023/JAX_ECAL_19/ScaleFactors_ECAL_Phys.csv --Test1
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_52
source Instructions/TestTrainingCombination.sh ECAL_19 HCAL_52
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_52 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_52
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_19_HCAL_52
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_19_HCAL_52

# Test 2: Constrain SFs for iEt <= 5 to 1
python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_53 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL \
    --ECALCalib Trainings_2023/JAX_ECAL_19/ScaleFactors_ECAL_Phys.csv --maskLE 5
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_53
source Instructions/TestTrainingCombination.sh ECAL_19 HCAL_53
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_53 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_53
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_19_HCAL_53
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_19_HCAL_53

# Test 3: Constrain SFs for iEt <= 10 to 1
python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_54 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL \
    --ECALCalib Trainings_2023/JAX_ECAL_19/ScaleFactors_ECAL_Phys.csv --maskLE 10
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_54
source Instructions/TestTrainingCombination.sh ECAL_19 HCAL_54
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_54 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_54
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_19_HCAL_54
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_19_HCAL_54

# Test 4: Constrain SFs for iEt <= 15 to 1
python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_55 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL \
    --ECALCalib Trainings_2023/JAX_ECAL_19/ScaleFactors_ECAL_Phys.csv --maskLE 15
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_55
source Instructions/TestTrainingCombination.sh ECAL_19 HCAL_55
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_55 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_55
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_19_HCAL_55
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_19_HCAL_55

# Test 5: Constrain SFs for iEt <= 20 to 1
python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_56 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL \
    --ECALCalib Trainings_2023/JAX_ECAL_19/ScaleFactors_ECAL_Phys.csv --maskLE 20
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_56
source Instructions/TestTrainingCombination.sh ECAL_19 HCAL_56
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_56 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_56
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_19_HCAL_56
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_19_HCAL_56

# Test HF masking for Et ≤ 3.5 GeV ( ==>  first 4 bins ==> Et < 4 GeV ==>  Et < 8 iEt)
python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_57 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL \
    --ECALCalib Trainings_2023/JAX_ECAL_19/ScaleFactors_ECAL_Phys.csv --maskHF
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_57
source Instructions/TestTrainingCombination.sh ECAL_19 HCAL_57
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_57 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_57
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_19_HCAL_57
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_19_HCAL_57

# Test HF masking for Et ≤ 4.5 GeV ( ==>  first 5 bins ==> Et < 5 GeV ==>  Et < 10 iEt) # [FIXME] I've changed the JaxOptimizer.py script manually!!
python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_58 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL \
    --ECALCalib Trainings_2023/JAX_ECAL_19/ScaleFactors_ECAL_Phys.csv --maskHF
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_58
source Instructions/TestTrainingCombination.sh ECAL_19 HCAL_58
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_58 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_58
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_19_HCAL_58
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_19_HCAL_58

# Test HF masking for Et ≤ 5.5 GeV ( ==>  first 6 bins ==> Et < 6 GeV ==>  Et < 12 iEt) # [FIXME] I've changed the JaxOptimizer.py script manually!!
python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_59 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL \
    --ECALCalib Trainings_2023/JAX_ECAL_19/ScaleFactors_ECAL_Phys.csv --maskHF
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_59
source Instructions/TestTrainingCombination.sh ECAL_19 HCAL_59
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_59 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_59
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_19_HCAL_59
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_19_HCAL_59


python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_60 --jetsLim 10000 --lr 1 --bs 4096 --ep 50 --v HCAL \
    --ECALCalib Trainings_2023/JAX_ECAL_19/ScaleFactors_ECAL_Phys.csv --maskHF
# Test 6: Use MAPE*alpha + (1-alpha)*STD as loss (alpha = 0.5)
# Plot MAPE for uncalib and STD for uncalib and understand if they have the same magnitude
# If not, divide by the mean of the distribution

########################################################################################################################
# TEST ECAL 
########################################################################################################################

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_19 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v ECAL
source Instructions/TestsTrainingECAL.sh JAX_ECAL_19
python3 PlotHistory.py --indir Trainings_2023/JAX_ECAL_19 --v ECAL --loss
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_19

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_20 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v ECAL --MSPE
source Instructions/TestsTrainingECAL.sh JAX_ECAL_20
python3 PlotHistory.py --indir Trainings_2023/JAX_ECAL_20 --v ECAL --loss
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_20

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_21 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v ECAL --scaleB 0.95 --scaleE 0.9
source Instructions/TestsTrainingECAL.sh JAX_ECAL_21
python3 PlotHistory.py --indir Trainings_2023/JAX_ECAL_21 --v ECAL --loss
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_21

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_22 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v ECAL --scaleB 0.95 --scaleE 0.95
source Instructions/TestsTrainingECAL.sh JAX_ECAL_22
python3 PlotHistory.py --indir Trainings_2023/JAX_ECAL_22 --v ECAL --loss
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_22

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_23 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v ECAL --scaleB 1 --scaleE 0.95
source Instructions/TestsTrainingECAL.sh JAX_ECAL_23
python3 PlotHistory.py --indir Trainings_2023/JAX_ECAL_23 --v ECAL --loss
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_23

