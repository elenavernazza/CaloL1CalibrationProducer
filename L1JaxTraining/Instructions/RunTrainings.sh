########################################################################################################################
# HCAL TRAININGS
########################################################################################################################

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_34 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scaleB 0.75 --scaleE 0.75 --scaleF 0.75 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_34
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_34

########################################################################################################################
# ECAL TRAININGS
########################################################################################################################

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_13 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --v ECAL
source Instructions/TestsTrainingECAL.sh JAX_ECAL_13

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_14 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --scaleB 1 --scaleE 0.95 --v ECAL
source Instructions/TestsTrainingECAL.sh JAX_ECAL_14

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_15 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --scaleB 1 --scaleE 0.9 --v ECAL
source Instructions/TestsTrainingECAL.sh JAX_ECAL_15

python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_16 --jetsLim 1000000 --lr 0.5 --bs 4096 \
    --ep 100 --scaleB 0.95 --scaleE 0.9 --v ECAL
source Instructions/TestsTrainingECAL.sh JAX_ECAL_16
