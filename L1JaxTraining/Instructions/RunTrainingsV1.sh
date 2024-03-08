########################################################################################################################
# HCAL TRAININGS
########################################################################################################################

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_1 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scaleB 0.75 --scaleE 0.75 --scaleF 0.75 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_1
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_1

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_2 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scaleB 0.8 --scaleE 0.8 --scaleF 0.8 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_2
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_2

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_3 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_3
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_3

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_4 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_4
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_4

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_5 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scaleB 0.75 --scaleE 0.75 --scaleF 1 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_5
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_5

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_6 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scaleB 0.75 --scaleE 0.75 --scaleF 1.5 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_6
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_6

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_7 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scaleB 0.82 --scaleE 0.82 --scaleF 1 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_7
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_7

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_8 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scaleB 0.82 --scaleE 0.82 --scaleF 1.5 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_8
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_8

python3 JaxOptimizerSatu.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70_NoSatu/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_9 --jetsLim 900000 --lr 0.5 --bs 4096 --ep 100 --scaleB 0.82 --scaleE 0.82 --scaleF 1. --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_9
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_9

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_10 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scaleF 1.2 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_10 NO

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_11 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scaleF 1.25 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_11 NO

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_12 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scaleF 1.5 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_12 NO

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_13 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scaleF 1.6 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_13 NO

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_14 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_14

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_15 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF # (adding TT 28 ZS)
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_15 # bugged, forgot to ask masking of TT 28

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_16 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF # (adding TT 28 ZS)
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_16

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_17 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF # (adding TT 28 to 1)
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_17

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt50_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_18 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF # (adding TT 28 to 1)
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_18

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_19 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF \
    --ECALCalib Trainings_2023/JAX_ECAL_11/ScaleFactors_ECAL.csv  # (adding TT 28 to 1)
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_19

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_HCALCorr_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_20 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_20
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_20 HCALCorr

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_HCALCorr_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_21 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF --scaleB 0.95
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_21
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_21 HCALCorr

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_HCALCorr_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_22 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF --scaleB 0.9
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_22
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_22 HCALCorr

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_HCALCorr_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_23 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF --scaleB 0.95 --scaleE 0.95
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_23
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_23 HCALCorr

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_HCALCorr_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_24 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF --scaleB 0.9 --scaleE 0.9
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_24
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_24 HCALCorr # best one so far

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_HCALCorr_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_25 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF --scaleB 0.85 --scaleE 0.85
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_25
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_25 HCALCorr # best in terms of turn on but worse resolution in the barrel

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_HCALCorr_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_26 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF --scaleB 0.8 --scaleE 0.8
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_26
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_26 HCALCorr # to prove that 0.9 is the best and we can't go down too much with the scale otherwise we would affect HF

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_HCALCorr_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_27 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF --scaleB 0.85 --scaleE 0.85 \
    --ECALCalib Trainings_2023/JAX_ECAL_11/ScaleFactors_ECAL.csv
source Instructions/TestTrainingCombination.sh ECAL_11 HCAL_27
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_11_HCAL_27
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_11_HCAL_27 HCALCorr
source Instructions/MoveToEos.sh JAX_ECAL_11_HCAL_27 ECAL
source Instructions/MoveToEos.sh JAX_ECAL_11_HCAL_27 HCAL HCALCorr

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_HCALCorr_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_28 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF --scaleB 0.9 --scaleE 0.9 \
    --ECALCalib Trainings_2023/JAX_ECAL_11/ScaleFactors_ECAL.csv
source Instructions/TestTrainingCombination.sh ECAL_11 HCAL_28
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_11_HCAL_28
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_11_HCAL_28 HCALCorr
source Instructions/MoveToEos.sh JAX_ECAL_11_HCAL_28 ECAL
source Instructions/MoveToEos.sh JAX_ECAL_11_HCAL_28 HCAL HCALCorr

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_HCALCorr_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_29 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF --scaleB 0.95 --scaleE 0.95 \
    --ECALCalib Trainings_2023/JAX_ECAL_11/ScaleFactors_ECAL.csv
source Instructions/TestTrainingCombination.sh ECAL_11 HCAL_29
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_11_HCAL_29
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_11_HCAL_29 HCALCorr
source Instructions/MoveToEos.sh JAX_ECAL_11_HCAL_29 ECAL
source Instructions/MoveToEos.sh JAX_ECAL_11_HCAL_29 HCAL HCALCorr

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_HCALCorr_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_30 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF --scaleB 1.0 --scaleE 1.0 \
    --ECALCalib Trainings_2023/JAX_ECAL_11/ScaleFactors_ECAL.csv
source Instructions/TestTrainingCombination.sh ECAL_11 HCAL_30
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_11_HCAL_30
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_11_HCAL_30 HCALCorr
source Instructions/MoveToEos.sh JAX_ECAL_11_HCAL_30 ECAL
source Instructions/MoveToEos.sh JAX_ECAL_11_HCAL_30 HCAL HCALCorr

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_HCALCorr_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_31 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF --scaleB 1.0 --scaleE 0.85 \
    --ECALCalib Trainings_2023/JAX_ECAL_11/ScaleFactors_ECAL.csv
source Instructions/TestTrainingCombination.sh ECAL_11 HCAL_31
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_11_HCAL_31
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_11_HCAL_31 HCALCorr
source Instructions/MoveToEos.sh JAX_ECAL_11_HCAL_31 ECAL
source Instructions/MoveToEos.sh JAX_ECAL_11_HCAL_31 HCAL HCALCorr

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_HCALCorr_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_32 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF --scaleB 1.0 --scaleE 0.9 \
    --ECALCalib Trainings_2023/JAX_ECAL_11/ScaleFactors_ECAL.csv
source Instructions/TestTrainingCombination.sh ECAL_11 HCAL_32
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_11_HCAL_32
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_11_HCAL_32 HCALCorr
source Instructions/MoveToEos.sh JAX_ECAL_11_HCAL_32 ECAL
source Instructions/MoveToEos.sh JAX_ECAL_11_HCAL_32 HCAL HCALCorr

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_HCALCorr_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_33 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF --scaleB 1.0 --scaleE 0.95 \
    --ECALCalib Trainings_2023/JAX_ECAL_11/ScaleFactors_ECAL.csv
source Instructions/TestTrainingCombination.sh ECAL_11 HCAL_33
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_11_HCAL_33
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_11_HCAL_33 HCALCorr
source Instructions/MoveToEos.sh JAX_ECAL_11_HCAL_33 ECAL
source Instructions/MoveToEos.sh JAX_ECAL_11_HCAL_33 HCAL HCALCorr

# l'obiettivo è avere una buona risoluzione nel barrel mantenendo le turn on ok

# python3 JaxOptimizerFloor.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
#     --odir Trainings_2023/JAX_HCAL_18 --jetsLim 10000 --lr 0.5 --bs 512 --ep 10 --v HCAL --maskHF # (adding TT 28 to 1)
# source Instructions/TestsTrainingHCAL.sh JAX_HCAL_18

# python3 JaxOptimizerFloor.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
#     --odir Trainings_2023/JAX_HCAL_14 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scaleB 0.82 --scaleE 0.82 --scaleF 1. --v HCAL

########################################################################################################################
# ECAL TRAININGS (full stats 5353702)
########################################################################################################################

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/EGamma_Run2023*_LooseEle_EoTot80/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_1 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v ECAL
source Instructions/TestsTrainingECAL.sh JAX_ECAL_1
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_1

python3 JaxOptimizerPtNorm.py --indir 2024_02_15_NtuplesV58/EGamma_Run2023*_LooseEle_EoTot80/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_2 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v ECAL
source Instructions/TestsTrainingECAL.sh JAX_ECAL_2
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_2

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/EGamma_Run2023*_LooseEle_EoTot80/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_3 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scaleB 1.15 --scaleE 1.15 --v ECAL
source Instructions/TestsTrainingECAL.sh JAX_ECAL_3
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_3

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/EGamma_Run2023*_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_4 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --v ECAL # (applying 3_6_9 and new binning)
source Instructions/TestsTrainingECAL.sh JAX_ECAL_4

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/EGamma_Run2023*_LooseEle_EoTot80_CD3x3/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_5 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --v ECAL # (applying 3_6_9 and new binning)
source Instructions/TestsTrainingECAL.sh JAX_ECAL_5

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/EGamma_Run2023*_LooseEle_EoTot80/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_6 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --v ECAL # (applying 3_6_9 and new binning)
source Instructions/TestsTrainingECAL.sh JAX_ECAL_6

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/EGamma_Run2023*_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_7 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --scaleB 0.9 --scaleE 0.9 --v ECAL # (applying 3_6_9 and new binning)
source Instructions/TestsTrainingECAL.sh JAX_ECAL_7

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/EGamma_Run2023*_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_8 --jetsLim 3000000 --lr 0.5 --bs 4096 \
    --ep 100 --scaleB 0.9 --scaleE 0.9 --v ECAL # (applying 3_6_9 and new binning)
source Instructions/TestsTrainingECAL.sh JAX_ECAL_8

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/EGamma_Run2023*_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_9 --jetsLim 3000000 --lr 0.5 --bs 4096 \
    --ep 100 --scaleB 0.95 --scaleE 0.95 --v ECAL # (applying 3_6_9 and new binning)
source Instructions/TestsTrainingECAL.sh JAX_ECAL_9

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/EGamma_Run2023*_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_10 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --scaleB 0.95 --scaleE 0.95 --v ECAL # (applying 3_6_9 and new binning)
source Instructions/TestsTrainingECAL.sh JAX_ECAL_10

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/EGamma_Run2023*_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_11 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --scaleB 0.95 --scaleE 0.9 --v ECAL # (applying 3_6_9 and new binning)
source Instructions/TestsTrainingECAL.sh JAX_ECAL_11

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/EGamma_Run2023*_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_12 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --scaleB 0.95 --scaleE 0.9 --v ECAL --maskECAL # (applying 3_6_9 and new binning and fix first energy bin)
source Instructions/TestsTrainingECAL.sh JAX_ECAL_12 # ECAL_11 is better in any way, the fluctuations don't matter too much

########################################################################################################################
# OLD BEST TRAININGS
########################################################################################################################

source Instructions/TestsTrainingHCAL.sh ECALv33_HCALv51_HFv52_Best
source Instructions/TestsPerformanceHCAL.sh ECALv33_HCALv51_HFv52_Best

source Instructions/TestsTrainingECAL.sh ECALv33_HCALv51_HFv52_Best
source Instructions/TestsPerformanceECAL.sh ECALv33_HCALv51_HFv52_Best

python3 RDF_ResolutionFast.py --indir JetMET__Run2023B-PromptReco-v1__Run367079__AOD__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
 --reco --target jet --do_HoTot --raw --PuppiJet --jetPtcut 30 --nEvts 100000 --no_plot \
 --HCALcalib --ECALcalib --caloParam caloParams_2023_JAX_ECAL_1_HCAL_3_newCalib_cfi.py --outdir Trainings_2023/FullCalib/JAX_ECAL_1_HCAL_3/NtuplesVnew
python3 comparisonPlotsFast.py --indir Trainings_2023/JAX_ECAL_1_HCAL_3/NtuplesVnew --target jet --reco \
 --old Trainings_2023/JAX_HCAL_0/NtuplesVold --unc Trainings_2023/FullCalib/JAX_HCAL_0/NtuplesVunc \
 --do_HoTot --doRate False --doTurnOn False

python3 RDF_ResolutionFast.py --indir JetMET__Run2023B-PromptReco-v1__Run367079__AOD__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
 --reco --target jet --do_HoTot --raw --PuppiJet --jetPtcut 30 --nEvts 100000 --no_plot \
 --HCALcalib --ECALcalib --caloParam caloParams_2023_ECALv33_JAX_HCAL_3_newCalib_cfi.py --outdir Trainings_2023/FullCalib/ECALv33_JAX_HCAL_3/NtuplesVnew
python3 comparisonPlotsFast.py --indir Trainings_2023/FullCalib/ECALv33_JAX_HCAL_3/NtuplesVnew --target jet --reco \
 --old Trainings_2023/JAX_HCAL_0/NtuplesVold --unc Trainings_2023/JAX_HCAL_0/NtuplesVunc \
 --do_HoTot --doRate False --doTurnOn False

python3 RDF_ResolutionFast.py --indir JetMET__Run2023B-PromptReco-v1__Run367079__AOD__GT130XdataRun3Promptv4_CaloParams2023v04_noL1Calib_data_reco_json/GoodNtuples \
 --reco --target jet --do_HoTot --raw --PuppiJet --jetPtcut 30 --nEvts 100000 --no_plot \
 --HCALcalib --ECALcalib --caloParam caloParams_2023_ECALv33_HCALv51_HFv52_Best_newCalib_cfi.py --outdir Trainings_2023/FullCalib/ECALv33_HCALv51_HFv52_Best/NtuplesVnew
python3 comparisonPlotsFast.py --indir Trainings_2023/FullCalib/ECALv33_HCALv51_HFv52_Best/NtuplesVnew --target jet --reco \
 --old Trainings_2023/JAX_HCAL_0/NtuplesVold --unc Trainings_2023/JAX_HCAL_0/NtuplesVunc \
 --do_HoTot --doRate False --doTurnOn False
