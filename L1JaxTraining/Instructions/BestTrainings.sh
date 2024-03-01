########################################################################################################################
# HCAL TRAININGS
########################################################################################################################

# First training provided for Layer-2 validation (19/2/2024 L1 DPG meeting)
python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_3 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scale 1 --scaleHF 1 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_3
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_3

# Training with HF ZS (best one so far)
python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_14 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scale 1 --scaleHF 1 --v HCAL --maskHF
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_14
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_14

# Training with HF ZS (slightly worse than 14 but still good and no spike at TT28)
python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_17 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scale 1 --scaleHF 1 --v HCAL --maskHF
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_17
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_17

########################################################################################################################
# ECAL TRAININGS
########################################################################################################################

# Best training in terms of resolution, but still problems with the turn on at fixed rate due to large scale
python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/EGamma_Run2023*_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_4 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --scale 1 --v ECAL 
source Instructions/TestsTrainingECAL.sh JAX_ECAL_4
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_4

# Best training in terms of everything
python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/EGamma_Run2023*_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_11 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --scaleB 0.95 --scaleE 0.9 --v ECAL
source Instructions/TestsTrainingECAL.sh JAX_ECAL_11
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_11

########################################################################################################################
# COMBINATIONS
########################################################################################################################

source Instructions/TestTrainingCombination.sh ECAL_11 HCAL_17
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_11_HCAL_17
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_11_HCAL_17

source Instructions/TestTrainingCombination.sh ECAL_11 HCAL_19
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_11_HCAL_19
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_11_HCAL_19

source Instructions/TestTrainingCombination.sh ECAL_11 HCAL_20
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_11_HCAL_20
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_11_HCAL_20