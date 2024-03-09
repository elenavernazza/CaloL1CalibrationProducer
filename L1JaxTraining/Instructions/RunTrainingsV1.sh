# Test previous best trainings on EraD

source Instructions/TestTrainingCombination.sh ECAL_11 HCAL_32
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_11_HCAL_32_Phys
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_11_HCAL_32_Phys
source Instructions/MoveToEos.sh JAX_ECAL_11_HCAL_32_Phys ECAL

source Instructions/TestTrainingCombination.sh ECAL_11 HCAL_17
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_11_HCAL_17_Phys
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_11_HCAL_17_Phys
source Instructions/MoveToEos.sh JAX_ECAL_11_HCAL_17_Phys ECAL

########################################################################################################################
# HCAL TRAININGS
########################################################################################################################

Investigate:
 - loss function
 - learning rate

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_34 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF --scaleB 1.0 --scaleE 0.9
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_34 # DIFF_2
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_34

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_35 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF --scaleB 1.0 --scaleE 0.9
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_35 # MSE
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_35

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_36 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --v HCAL --maskHF --scaleB 1.0 --scaleE 0.9
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_36 # MAPE
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_36

# Test MAPE
python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_37 --jetsLim 1000000 --lr 2.5 --bs 4096 --ep 20 --v HCAL --maskHF
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_37 NO
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_37 --v HCAL --loss

# Test MSPE
python3 JaxOptimizer1.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_38 --jetsLim 1000000 --lr 2.5 --bs 4096 --ep 20 --v HCAL --maskHF
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_38
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_38 --v HCAL --loss

python3 JaxOptimizer1.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_39 --jetsLim 1000000 --lr 2.5 --bs 4096 --ep 2 --v HCAL --maskHF
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_39
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_39 --v HCAL --loss

# Try to cure HF
python3 JaxOptimizer1.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_40 --jetsLim 1000000 --lr 2.5 --bs 4096 --ep 20 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_40
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_40 --v HCAL --loss

########################################################################################################################
# ECAL TRAININGS
########################################################################################################################

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_13 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --v ECAL
source Instructions/TestsTrainingECAL.sh JAX_ECAL_13
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_13

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_14 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --scaleB 1 --scaleE 0.95 --v ECAL
source Instructions/TestsTrainingECAL.sh JAX_ECAL_14
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_14

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_15 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --scaleB 1 --scaleE 0.9 --v ECAL
source Instructions/TestsTrainingECAL.sh JAX_ECAL_15
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_15

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_16 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --scaleB 0.95 --scaleE 0.9 --v ECAL
source Instructions/TestsTrainingECAL.sh JAX_ECAL_16
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_16

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_17 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --scaleB 1 --scaleE 0.9 --v ECAL # DIFF_2
source Instructions/TestsTrainingECAL.sh JAX_ECAL_17
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_17

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_18 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --scaleB 1 --scaleE 0.9 --v ECAL # MAPE_2
source Instructions/TestsTrainingECAL.sh JAX_ECAL_18
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_18